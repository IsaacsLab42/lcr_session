from dataclasses import dataclass


BASE_URL: str = "https://{subdomain}.churchofjesuschrist.org/{path}"


@dataclass
class ChurchUrl:
    subdomain: str
    path: str = ""

    def render(self, **kwargs) -> str:
        path = self.path.format(**kwargs)
        return BASE_URL.format(subdomain=self.subdomain, path=path, **kwargs)


WELL_KNOWN_URLS = {
    "users_me": ChurchUrl("id", "api/v1/users/me"),
    "user": ChurchUrl("directory", "api/v4/user"),
    "members-with-callings": ChurchUrl(
        "lcr", "api/report/members-with-callings?unitNumber={unit}"
    ),
}
