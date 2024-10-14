# Welcome to LCR Session

<p align="center">
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
[Requests](https://requests.readthedocs.io/en/latest/) package to drive the web
connection, though I do plan on switching to
[Niquests](https://niquests.readthedocs.io/en/stable/) at some point. It is a more
modern and updated fork of Requests and includes HTTP/2 and HTTP/3 support.

This library can also save the cookies from an established session, which means that
once you authenticate you can repeatedly use your scripts without have to
reauthenticate.

!!! note

    This in an unofficial and independent project. In no way is this officially
    associated with The Church of Jesus Christ of Latter-Day Saints.

# Quick Start

Here's a very simple and quick illustration of how to use the API. Note that some URL's
require parameters, like the unit number in this example. The common parameters are
auto-substituted. Additional templated parameters must be supplied to the API.

```python
import pprint
from lcr_session import LcrSession

api = LcrSession(USERNAME, PASSWORD, cookie_jar_file="cookies.txt")
resp = api.get_json("https://lcr.churchofjesuschrist.org/api/report/members-with-callings?unitNumber={unit}")
pprint.pprint(resp)
```

These are the automatically supplied template values.

* `{unit}` -- Your assigned unit number (Ward or Branch).
* `{parent_unit}` -- The parent of your unit (Stake, District, or Mission).
* `{member_id}` -- Your assigned LCR membership ID.
* `{uuid}` -- Your unique Church UUID. A few of the API calls use this.

As a shortcut, since the base URL for all endpoints is the same, there is a convenience
class [ChurchUrl](api/urls.md) that could be used like this:

```python
import pprint
from lcr_session import LcrSession, ChurchUrl

endpoint_url = ChurchUrl("lcr", "api/report/members-with-callings?unitNumber={unit}")
api = LcrSession(USERNAME, PASSWORD, cookie_jar_file="cookies.txt")
resp = api.get_json(endpoint_url)
pprint.pprint(resp)
```

The end result is the same, but it might be more convenient to use the `ChurchUrl` class
in some cases.

# Project Goals

The goal of this project is to serve as a foundation for other scripts or libraries. As
such it provides very little functionality beyond authentication, GET, and POST.
