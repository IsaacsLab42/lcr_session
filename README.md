# LCR Session

This library provides session authentication to the [Church of Jesus Christ of Latter
Day Saints](https://www.churchofjesuschrist.org) Leader and Clerk Resources (LCR)
System. This uses the very capable
[Requests](https://requests.readthedocs.io/en/latest/) package to drive the web
connection.

This library can also save the cookies from an established session, which means that
once you authenticate you can repeatedly use your scripts without have to
reauthenticate.

> This in an unofficial and independent project. In no way is this officially
> associated with The Church of Jesus Christ of Latter-Day Saints. 

As it stands this API is functional, though not up to my standards. I plan to smooth out
some of the rough edges and add a lot of comments and documentation. But, it does work.

## Quick Start

Here's a very simple and quick illustration of how to use the API:

```python
import pprint
from lcr_session import LcrSession, WELL_KNOWN_URLS

api = LcrSession(USERNAME, PASSWORD, cookie_jar_file="cookies.txt")
resp = api.get_json(WELL_KNOWN_URLS["members-with-callings"])
pprint.pprint(resp)
```

## History

The Leader and Clerk Resources (LCR) system for the Church of Jesus Christ of Latter-Day
Saints is a very capable system, though after working with it for a while I quickly ran
into some limitations. This project started to form as an idea while I was serving in
the Young Men's organization. One of the responsibilities I had was to send a weekly
email to all of the young men, their parents, and their leaders. I kept a file with the
basic template, and updated it each week. I found that pasting preformatted messages
into that little text box on the web interface wasn't pleasant. Formatting would get
lost, or altered. And I'd end up reformatting everything.

This didn't take a lot of time, but as a professional software developer I am always
looking for ways to automate repetitive tasks. I think it's just in my DNA. At first I
looked into how the authentication happened between a web browser and the Church web
servers. It was more complex than I expected. So I looked around for any existing GitHub
projects. Most that I found were old and defunct. However, I did finally find [Church of
Jesus Christ API](https://github.com/mackliet/church_of_jesus_christ_api).
It worked, and so I started on my project to automate emails. Then I was released from
my calling, and no longer worked with the young men, so the project was neglected.

In my new calling, as ward clerk, I found myself again needing to create reports and do
tasks that can be automated. So, I started looking at the Church API again, only to
discover that at some point the Church ~~broke~~ changed their authentication, which
broke the aforementioned API. After several long sessions dissecting the authentication
I wrote some [fairly detailed
notes](https://github.com/mackliet/church_of_jesus_christ_api/issues/16). He took my
notes and implemented them, for which I am grateful.

After working with his library for a while I wanted to make something a bit more
generic, and that had the capability to save sessions to eliminate reauthentication on
every single run of the script. I mean no disrespect. The Church of Jesus Christ API
project is excellent, but didn't quite fit my personal needs.

Anyway, that's how this library got started. I hope someone finds it useful.

## Future Plans

* Documentation
* Easier to use API
* Replace Requests with Niquests
* More "well known URL's"
* More examples
* Saving more of the session state
* What else? Please open an issue with suggestions or problems encountered. I do want to
  keep this library fairly generic. This is meant to serve as a foundation for other
  people to write scripts around.
