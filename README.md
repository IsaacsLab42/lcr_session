# LCR Session

<p>
    <a href="https://lcr-session.readthedocs.io/en/stable/">
        <img src="https://img.shields.io/readthedocs/lcr-session"/>
    </a>
    <a href="https://pypi.org/project/lcr-session/">
        <img src="https://img.shields.io/pypi/v/lcr-session"/>
    </a>
    <a href="https://pypi.org/project/lcr-session/">
        <img src="https://img.shields.io/pypi/wheel/lcr-session"/>
    </a>
    <a href="https://pypi.org/project/lcr-session/">
        <img src="https://img.shields.io/pypi/pyversions/lcr-session"/>
    </a>
    <a href="https://github.com/IsaacsLab42/lcr_session/">
        <img src="https://img.shields.io/github/license/IsaacsLab42/lcr_session"/>
    </a>
    <a href="https://black.readthedocs.io/en/stable/">
        <img src="https://img.shields.io/badge/code_style-black-black"/>
    </a>
</p>

---

This library provides session authentication to the [Church of Jesus Christ of Latter
Day Saints](https://www.churchofjesuschrist.org) Leader and Clerk Resources (LCR)
System. This uses the very capable
[Requests](https://requests.readthedocs.io/en/stable/) package to drive the web
connection.

This library can also save the cookies from an established session, which means that
once you authenticate you can repeatedly use your scripts without have to
reauthenticate.

> This in an unofficial and independent project. In no way is this officially
> associated with The Church of Jesus Christ of Latter-Day Saints.

## Quick Start

Here's a very simple and quick illustration of how to use the API:

```python
import pprint
from lcr_session import LcrSession, ChurchUrl

endpoint_url = ChurchUrl("lcr", "api/report/members-with-callings?unitNumber={unit}")
api = LcrSession(USERNAME, PASSWORD, cookie_jar_file="cookies.txt")
resp = api.get_json(endpoint_url)
pprint.pprint(resp)
```

See the documentation at: https://lcr-session.readthedocs.io/en/stable/.
