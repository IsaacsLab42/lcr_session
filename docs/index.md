# Welcome to LCR Session

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

As it stands this API is functional, though not up to my standards. I plan to smooth out
some of the rough edges and add a lot of comments and documentation. But, it does work.

# Quick Start

Here's a very simple and quick illustration of how to use the API:

```python
import pprint
from lcr_session import LcrSession, WELL_KNOWN_URLS

api = LcrSession(USERNAME, PASSWORD, cookie_jar_file="cookies.txt")
resp = api.get_json(WELL_KNOWN_URLS["members-with-callings"])
pprint.pprint(resp)
```
