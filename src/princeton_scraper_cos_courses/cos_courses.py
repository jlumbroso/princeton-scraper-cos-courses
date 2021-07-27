
import typing
import urllib.parse

import bs4
import requests

import princeton_scraper_cos_courses.parsing
import princeton_scraper_cos_courses.helpers


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "fetch_cos_people_directory",
]


#  URL to retrieve the COS course schedule

PRINCETON_CS_URL_BASE = "https://www.cs.princeton.edu/"
PRINCETON_CS_SCHEDULE_BASE = "https://www.cs.princeton.edu/courses/schedule/"


def _build_schedule_url(
        term: str,
) -> str:
    url = urllib.parse.urljoin(PRINCETON_CS_SCHEDULE_BASE, term)
    return url


def fetch_cos_courses() -> typing.Dict[str, typing.List[princeton_scraper_cos_courses.parsing.CosCourseInstance]]:
    data = {}

    for term in princeton_scraper_cos_courses.parsing.get_all_terms():
        url = _build_schedule_url(term["internal"])
        soup = princeton_scraper_cos_courses.helpers.fetch_page_as_soup(url=url)
        
        schedule_table = soup.find(
            name="table",
            attrs={"id": "course-schedules"}
        )
        courses = [
            princeton_scraper_cos_courses.parsing.parse_cs_course(
                tag=tr_tag,
                term=term,
            )
            for tr_tag in schedule_table.find("tbody").find_all("tr")
        ]
        data[term["internal"]] = courses

    return data  
