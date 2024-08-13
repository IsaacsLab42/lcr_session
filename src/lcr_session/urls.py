from dataclasses import dataclass
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

__all__ = ["ChurchUrl", "BASE_URL"]

BASE_URL: str = "https://{subdomain}.churchofjesuschrist.org/{path}"


@dataclass
class ChurchUrl:
    """
    Wrapper class around Church URL's. The Church API's all have the same base of
    churchofjesuschrist.org, so this class acts as a lightweight abstraction layer. It
    fills in some of the common required template variables in Church URL's. For example,
    many of the API's require these fields:

    * `{unit}` -- Your assigned unit number (Ward or Branch).
    * `{parent_unit}` -- The parent of your unit (Stake, District, or Mission).
    * `{member_id}` -- Your assigned LCR membership ID.
    * `{uuid}` -- Your unique Church UUID. A few of the API calls use this.

    As an example, the _Members With Callings_ report is at the URL:

        https://lcr.churchofjesuschrist.org/api/report/members-with-callings?unitNumber={unit}

    In this case the `subdomain` is `lcr` and the `path` is
    `api/report/members-with-callings?unitNumber={unit}`.

    Args:
        subdomain: The subdomain portion of the URL.
        path: The full path of the API, including any template parameters.
    """

    subdomain: str
    """Subdomain portion of URL"""

    path: str = ""
    """Path of the API, including templated parameters."""

    def render(self, **kwargs: Any) -> str:
        """
        Renders the contained URL fragments into a fully qualified URL, suitable for use
        in a network request.

        Note: This is typically called by the `get_json` method of the `LcrSession`
        class.

        Args:
            kwargs: Key/value pairs of the template items to replace.

        Returns:
            Rendered URL, with all templated parameters replaced.
        """
        # "raw" as in not fully rendered
        raw_url_str = BASE_URL.format(subdomain=self.subdomain, path=self.path)
        cooked_url_str = raw_url_str.format(**kwargs)
        url_parts = urlsplit(cooked_url_str)
        query_dict = dict(parse_qsl(url_parts.query))
        query_dict["lang"] = "eng"
        url_parts = url_parts._replace(query=urlencode(query_dict))
        return urlunsplit(url_parts)
