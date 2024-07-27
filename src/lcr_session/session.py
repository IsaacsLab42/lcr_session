__all__ = ["ChurchUrl", "LcrSession"]

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import requests

from .cache import FileCache, SavedSession, SessionCache

BASE_URL: str = "https://{subdomain}.churchofjesuschrist.org/{path}"


@dataclass
class ChurchUrl:
    subdomain: str
    path: str = ""

    def render(self, **kwargs) -> str:
        return BASE_URL.format(subdomain=self.subdomain, path=self.path, **kwargs)


AUTH_URLS = {
    "login": ChurchUrl("www", "services/platform/v4/login"),
    "introspect": ChurchUrl("id", "idp/idx/introspect"),
    "identify": ChurchUrl("id", "idp/idx/identify"),
    "challenge_answer": ChurchUrl("id", "idp/idx/challenge/answer"),
}


class LcrSession:
    def __init__(
        self,
        username: str,
        password: str,
        cache: SessionCache | None = None,
        timeout_sec: int = 30,
    ) -> None:
        if not isinstance(username, str):
            raise TypeError("username must be a string")
        if not isinstance(password, str):
            raise TypeError("password must be a string")
        if cache is not None and not isinstance(cache, SessionCache):
            raise TypeError("cache must be a SessionCache object")

        self._username = username
        self._password = password
        self._cache = cache
        self._session = requests.Session()
        self._saved_sesssion = self._load_saved_session()
        self._timeout = timeout_sec

    def _load_saved_session(self) -> SavedSession:
        if self._cache is not None:
            ss = self._cache.load_session()
            self._session.cookies.update(requests.utils.cookiejar_from_dict(ss.cookies))
            return ss
        return SavedSession()

    def _connect(self) -> None:
        if not self.is_expired():
            return

        self._session.close()
        self._session = requests.Session()

        # Get the initial cookies and state token
        resp = self._session.get(AUTH_URLS["login"].render(), timeout=self._timeout)
        resp.raise_for_status()
        content = resp.content.decode("unicode_escape")

        # Extract the state token.
        token_match = re.search(r"\"stateToken\":\"([^\"]+)\"", content)
        if token_match is None:
            raise Exception("Could not find stateToken")
        state_token = token_match.groups()[0]

        # Not sure why, but the web auth does this so we will too
        resp = self._session.post(
            AUTH_URLS["introspect"].render(),
            timeout=self._timeout,
            json={"stateToken": state_token},
        )
        resp.raise_for_status()

        # Now we need to post the username and get something called a state handle in
        # return.
        resp = self._session.post(
            AUTH_URLS["identify"].render(),
            timeout=self._timeout,
            json={"identifier": self._username, "stateHandle": state_token},
        )
        resp.raise_for_status()
        state_handle = resp.json()["stateHandle"]

        # Post the password
        resp = self._session.post(
            AUTH_URLS["challenge_answer"].render(),
            timeout=self._timeout,
            json={
                "credentials": {"passcode": self._password},
                "stateHandle": state_handle,
            },
        )
        resp.raise_for_status()
        # We get a new URL in the response that we need to hit
        resp_url = resp.json()["success"]["href"]
        resp = self._session.get(resp_url)
        resp.raise_for_status()

        # Extract the access token
        for cookie in self._session.cookies:
            if cookie.name == "oauth_id_token" and cookie.expires is not None:
                self._saved_sesssion.expires = datetime.fromtimestamp(cookie.expires)
                self._saved_sesssion.token = str(cookie.value)
                break
        else:
            raise Exception("Access token not found in web response")

        self._session.cookies.set("owp", self._saved_sesssion.token)
        self._saved_sesssion.cookies = self._session.cookies.get_dict()
        if self._cache is not None:
            self._cache.save_session(self._saved_sesssion)

        # Does lcr and directory login stuff
        self._session.get(ChurchUrl("lcr").render())
        self._session.get(ChurchUrl("directory").render())

    def is_expired(self) -> bool:
        now = datetime.now()
        if (
            len(self._saved_sesssion.cookies) == 0
            or len(self._saved_sesssion.token) == 0
            or now > self._saved_sesssion.expires
        ):
            return True
        return False

    def get_session(self) -> requests.Session:
        return self._session

    def get_json(self, url: ChurchUrl, **kwargs) -> Any:
        self._connect()
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self._saved_sesssion.token}",
        }
        resp = self._session.get(
            url.render(**kwargs), timeout=self._timeout, headers=headers
        )
        resp.raise_for_status()
        if self._cache is not None:
            self._cache.save_session(self._saved_sesssion)
        return resp.json()
