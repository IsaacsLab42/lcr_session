"""
Main session interface of this package.
"""

__all__ = ["UserDetails", "LcrSession"]

import re
from dataclasses import asdict, dataclass
from http.cookiejar import Cookie, MozillaCookieJar
from pathlib import Path
from typing import Any

import requests
from requests.cookies import create_cookie

from .urls import ChurchUrl, WELL_KNOWN_URLS
from .utils import get_user_agent, merge_dict

_AUTH_URLS = {
    "login": ChurchUrl("www", "services/platform/v4/login"),
    "introspect": ChurchUrl("id", "idp/idx/introspect"),
    "identify": ChurchUrl("id", "idp/idx/identify"),
    "challenge_answer": ChurchUrl("id", "idp/idx/challenge/answer"),
}


@dataclass
class UserDetails:
    """
    Holds information pertaining to the logged in user.
    """

    unit: int
    """Assigned unit number. For example, the Ward unit number."""

    parent_unit: int
    """Parent unit number, for example the stake."""

    member_id: int
    """Member ID according to LCR"""

    uuid: str
    """Unique UUID for the user."""


class LcrSession:
    """
    Session class used for interacting with the Church of Jesus Christ of Latter-Day
    Saints LCR system.
    """

    def __init__(
        self,
        username: str,
        password: str,
        timeout_sec: int = 30,
        user_agent: str | None = None,
        cookie_jar_file: str | Path | None = None,
    ) -> None:
        """
        Args:
            username: Username for LCR
            password: Password for LCR
            timeout_sec: HTTPS response timeout (seconds).
            user_agent: Custom User-Agent to send in all HTTPS requests. If `None` then
                a user agent string will be generated using the `fake_useragent` Python
                package.
            cookie_jar_file: File to store/load the session cookies. This allows
                sessions to persist.

        Raises:
            TypeError: When one of the parameters is an invalid type.
        """
        if not isinstance(username, str):
            raise TypeError("username must be a string")
        if not isinstance(password, str):
            raise TypeError("password must be a string")

        self._username = username
        self._password = password
        self._timeout = timeout_sec
        self._user_agent = user_agent or get_user_agent()

        if cookie_jar_file is not None:
            self._cookie_jar_file = Path(cookie_jar_file)
            self._cookie_jar = MozillaCookieJar(self._cookie_jar_file)
        else:
            self._cookie_jar_file = None
            self._cookie_jar = None

        self._token = None
        self._user_details = None
        self._session = requests.Session()
        self._new_session()

    def expired(self) -> bool:
        """
        Check to see if the existing session has expired. By default Church sessions
        expire after one hour. This will check the cookie expiration.

        Returns:
            `True` if the session has expired. `False` otherwise.
        """
        for cookie in self._session.cookies:
            if cookie.name == "oauth_id_token":
                return cookie.is_expired()
        return True

    def get_user_details(self) -> UserDetails:
        """
        Get the object containing the current user details.

        Returns:
            UserDetails object.
        """
        return self._user_details  # type: ignore

    def get_session(self) -> requests.Session:
        """
        Get a copy of the `Requests` session.

        Returns:
            The currently authentication Requests session.
        """
        return self._session

    def get_json(self, url: ChurchUrl, **kwargs: dict[str, str]) -> Any:
        """
        Perform a GET request on the specified URL and return the resulting JSON.

        Many of the Church API URL's require additional templated parameters. As an
        example, to get the _Members With Callings_ report the URL is:

            https://lcr.churchofjesuschrist.org/api/report/members-with-callings?unitNumber={unit}

        In this case the unit number, for example the Ward or Branch, must be supplied.
        This `get_json` method automatically supplies the values for these templated
        parts of URL's. Any additional templated parameters need to be passed in by you.

        * `{unit}` -- Your assigned unit number (Ward or Branch).
        * `{parent_unit}` -- The parent of your unit (Stake, District, or Mission).
        * `{member_id}` -- Your assigned LCR membership ID.
        * `{uuid}` -- Your unique Church UUID. A few of the API calls use this.

        Args:
            url: A ChurchUrl object containing the API endpoint.
            kwargs: Additional arguments that will be used to fill in templated URL's.

        Returns:
            Parsed JSON data as a Python dictionary.
        """
        self._connect()
        args = merge_dict(asdict(self._user_details), kwargs)  # type: ignore
        return self._real_get_json(url, **args)

    def _get_json_str_url(self, url: str, **kwargs) -> Any:
        pass

    def _get_json_church_url(self, url: ChurchUrl, **kwargs) -> Any:
        pass

    def _real_get_json(self, url: ChurchUrl, **kwargs) -> Any:
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self._token}",
        }
        resp = self._session.get(
            url.render(**kwargs), timeout=self._timeout, headers=headers
        )
        resp.raise_for_status()
        self._save_cookies()

        return resp.json()

    def _new_session(self) -> None:
        self._session.close()
        session = requests.Session()
        session.headers.update({"User-Agent": self._user_agent})
        self._session = session
        self._load_cookies()

    def _load_cookies(self) -> None:
        if self._cookie_jar is not None and self._cookie_jar_file is not None:
            self._session.cookies = self._cookie_jar  # type: ignore
            if self._cookie_jar_file.exists():
                self._cookie_jar.load(ignore_discard=True, ignore_expires=True)

    def _save_cookies(self) -> None:
        if self._cookie_jar is not None and self._cookie_jar_file is not None:
            self._cookie_jar.save(ignore_discard=True, ignore_expires=True)

    def _get_token_from_cookies(self) -> None:
        if self._token is None:
            for cookie in self._session.cookies:
                if cookie.name == "oauth_id_token":
                    self._token = cookie.value
                    break
            else:
                raise Exception("Could not find auth token")

    def _get_user_details(self) -> None:
        if self._user_details is None:
            # Get details for the current user
            user = self._real_get_json(WELL_KNOWN_URLS["user"])
            self._user_details = UserDetails(
                unit=user["homeUnits"][0],
                parent_unit=user["parentUnits"][0],
                member_id=user["individualId"],
                uuid=user["uuid"],
            )

    def _connect(self) -> None:
        if not self.expired():
            self._get_token_from_cookies()
            self._get_user_details()
            return

        self._new_session()

        # Get the initial cookies and state token
        resp = self._session.get(_AUTH_URLS["login"].render(), timeout=self._timeout)
        resp.raise_for_status()
        content = resp.content.decode("unicode_escape")

        # Extract the state token.
        token_match = re.search(r"\"stateToken\":\"([^\"]+)\"", content)
        if token_match is None:
            raise Exception("Could not find stateToken")
        state_token = token_match.groups()[0]

        # Not sure why, but the web auth does this so we will too
        resp = self._session.post(
            _AUTH_URLS["introspect"].render(),
            timeout=self._timeout,
            json={"stateToken": state_token},
        )
        resp.raise_for_status()

        # Now we need to post the username and get something called a state handle in
        # return.
        resp = self._session.post(
            _AUTH_URLS["identify"].render(),
            timeout=self._timeout,
            json={"identifier": self._username, "stateHandle": state_token},
        )
        resp.raise_for_status()
        state_handle = resp.json()["stateHandle"]

        # Post the password
        resp = self._session.post(
            _AUTH_URLS["challenge_answer"].render(),
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

        # Extract the access token and copy it to a new cookie
        self._get_token_from_cookies()
        cookie = create_cookie(name="owp", value=self._token)
        self._session.cookies.set_cookie(cookie)

        # Do the lcr and directory login stuff
        headers = {"Authorization": f"Bearer {self._token}"}
        resp = self._session.get(ChurchUrl("lcr").render(), headers=headers)
        resp.raise_for_status()

        resp = self._session.get(ChurchUrl("directory").render(), headers=headers)
        resp.raise_for_status()

        self._get_user_details()

        self._save_cookies()
