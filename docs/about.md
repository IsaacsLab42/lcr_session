# Some History

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
Jesus Christ API](https://github.com/mackliet/church_of_jesus_christ_api). It worked,
and so I started on my project to automate emails. Then I was released from my calling,
and no longer worked with the young men, so the project was neglected.

In my new calling, as ward clerk, I found myself again needing to create reports and do
tasks that can be automated. So, I started looking at the Church API again, only to
discover that at some point the Church ~~broke~~ changed their authentication, which
broke the aforementioned API. After several long sessions dissecting the authentication
I wrote some [fairly detailed
notes](https://github.com/mackliet/church_of_jesus_christ_api/issues/16) for the author
of that package. He took my notes and implemented them, for which I am grateful.

After working with his library for a while I wanted to make something a bit more
generic, and that had the capability to save sessions to eliminate reauthentication on
every single run of the script. I mean no disrespect. The Church of Jesus Christ API
project is excellent, but didn't quite fit my personal needs.

Anyway, that's how this library got started. I hope someone finds it useful.

## Future Plans

* Better Documentation
* Easier to use API
* Replace Requests with Niquests
* More "well known URL's"
* More examples
* Saving more of the session state
* What else? Please open an issue with suggestions or problems encountered. I do want to
  keep this library fairly generic. This is meant to serve as a foundation for other
  people to write scripts around.
