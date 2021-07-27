# Princeton COS Courses Scraper

This is a web scraper that produces machine-processable JSON feeds
of Princeton University's Department of Computer Science course schedule history,
sourced from
[the official, publicly available schedule](https://www.cs.princeton.edu/courses/schedule).

You can see [the JSON feed by clicking here](https://jlumbroso.github.io/princeton-scraper-cos-courses/feeds/).

These feeds are all updated _every week on Saturday_. Read on to learn more.

## Accessing the static feeds

You can access the main (regularly updated) JSON feed directly from this URL:

```text
https://jlumbroso.github.io/princeton-scraper-cos-courses/feeds/
```

For example using Python, you can use the `requests` package to
get the JSON feed:

```python
import requests
r = requests.get("https://jlumbroso.github.io/princeton-scraper-cos-courses/feeds/")
if r.ok:
    data = r.json()["data"]
```

## Feed format

This feed provides most people in the directory as a JSON dictionary with
the following fields:

```json
{
  "course": "COS 521",
  "title": "Advanced Algorithm Design",
  "people": ["M. Braverman", "M. Weinberg"],
  "hours": "TTh 1:30-2:50",
  "room": "",
  "term": {
    "year": 2021,
    "period": "Fall",
    "term": "Fall 2021",
    "internal": "fall21",
    "sortkey": "2021_1"
  }
}
```

Some fields may not always be known (such as `room`).

## Backstory

Previously, I had implemented
[JSON feeds to programmatically obtain the faculty of
Princeton's School of Engineering and Applied Sciences](https://github.com/jlumbroso/princeton-scraper-seas-faculty/),
to build the web portal for the BSE 2024 First Year Advising program; and
[JSON feeds to programmatically obtain the members of
Princeton's Department of Computer Science](https://github.com/jlumbroso/princeton-scraper-seas-faculty/)
to build an automated Slack management system for
[our grad students' Slack](https://gradslack.cs.princeton.edu/),
which I run.

This time, [@adamfinkelstein](https://github.com/adamfinkelstein) and Matt Weinberg are
building a matching system to match grad students to course TA-ships. The feed will help
document the courses that are available and the faculty who are managing them.

## License

This repository is licensed under [_The Unlicense_](LICENSE). This means I have no liability, but
you can do absolutely what you want with this.
