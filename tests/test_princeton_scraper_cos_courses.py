
import requests
import bs4


#from princeton_scraper_seas_faculty import __version__


SOME_LOW_TENS_NUMBER = 14


# def test_version():
#     assert __version__ == '0.1.0'


def test_faculty_format_dom():
    r = requests.get("https://www.cs.princeton.edu/courses/schedule/")
    assert r.ok

    s = bs4.BeautifulSoup(r.content, features="html.parser")
    assert s is not None

    courses = s.find_all("td", {"class": "course-schedule-num"})
    
    assert len(courses) > SOME_LOW_TENS_NUMBER


