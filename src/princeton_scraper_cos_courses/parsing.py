
import copy
import typing
import urllib.parse

import bs4
import loguru

import princeton_scraper_cos_courses.helpers


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "CosCourseInstance",
    "CosCourseTerm",
    "get_all_terms",
    "parse_cs_course"
]


# COS course schedule info type + term

CosCourseTerm = typing.TypedDict(
    "CosCourseTerm", {
        "year": int,
        "period": str,
        "term": str,
        "internal": str,
        "sortkey": str,
    }, total=True)

CosCourseInstance = typing.TypedDict(
    "CosCourseInstance", {
        "course": str,
        "title": str,
        "term": CosCourseTerm,
        "people": typing.List[str],
        "hours": str,
        "room": str
    }, total=False)


# Hard-coded constants that are required to scrape the web page

PRINCETON_CS_URL_BASE = "https://www.cs.princeton.edu/"
PRINCETON_CS_SCHEDULE_BASE = "https://www.cs.princeton.edu/courses/schedule/"

PRINCETON_CS_TERMS_IN_ORDER = ["Spring", "Fall"]

CS_HTML_NAME_SCHEDULE_SELECT = "select"
CS_HTML_CLASS_SCHEDULE_SELECT = "semester-select"
CS_HTML_NAME_SCHEDULE_TABLE = "table"
CS_HTML_ID_SCHEDULE_TABLE = "course-schedules"

# These are the headers of the schedule page and their renamed field name

CS_SCHEDULE_FIELDS_RENORMALIZATION = {
    "Num": "course",
    "Name": "title",
    "Professor(s)": "people",
    "Classes": "hours",
    "Room": "room"
}


# These are computed "constants"

_course_terms = None
_course_fields_data = None
_course_fields_id_to_caption = None
_course_fields_original_to_caption = None


def _recompute_data(suffix: typing.Optional[str] = None):
    global _course_terms, _course_fields_data, _course_fields_id_to_caption, _course_fields_original_to_caption

    url = PRINCETON_CS_SCHEDULE_BASE
    if suffix is not None:
        url = urllib.parse.urljoin(url, suffix)

    schedule_soup = princeton_scraper_cos_courses.helpers.fetch_page_as_soup(
        PRINCETON_CS_SCHEDULE_BASE
    )

    if schedule_soup is None:
        loguru.logger.error("could not load schedule page; could not recompute constants")
        return
    
    # parsing semesters

    semester_select = schedule_soup.find(
        name=CS_HTML_NAME_SCHEDULE_SELECT,
        attrs={"class": CS_HTML_CLASS_SCHEDULE_SELECT},
    )

    # WARN: hardcore parsing here (assume "Spring 2021" -> 0 1)
    _course_terms = [
        CosCourseTerm(
            year=int(option_tag.text.strip().split()[1]),
            period=option_tag.text.strip().split()[0],
            term=option_tag.text.strip(),
            internal=option_tag.get("value"),
            sortkey="{}_{}".format(
                int(option_tag.text.strip().split()[1]),
                PRINCETON_CS_TERMS_IN_ORDER.index(option_tag.text.strip().split()[0])
            )
        )
        for option_tag in semester_select.find_all("option")
    ]

    # parsing field names

    schedule_table = schedule_soup.find(
        name=CS_HTML_NAME_SCHEDULE_TABLE,
        attrs={"id": CS_HTML_ID_SCHEDULE_TABLE},
    )

    _course_fields_data = [
        {
            "id": i,
            "original": tag.text.strip(),
            "renamed": CS_SCHEDULE_FIELDS_RENORMALIZATION.get(tag.text.strip()),
        }
        for i, tag in enumerate(schedule_table.find("thead").find_all("th"))
    ]

    _course_fields_id_to_caption = {
        row["id"]: row["renamed"]
        for row in _course_fields_data
    }

    _course_fields_original_to_caption = {
        row["original"]: row["renamed"]
        for row in _course_fields_data
    }

_recompute_data()


def get_all_terms(sort=True, reverse=True) -> typing.List[CosCourseTerm]:
    global _course_terms

    if _course_terms is None:
        loguru.logger.debug("terms not cached, recomputing")
        _recompute_data()
        if _course_terms is None:
            loguru.logger.debug("recomputing failed")
            return list()
        else:
            loguru.logger.debug("recomputing successful")

    # defensive copy
    _ct = copy.deepcopy(_course_terms)
    if sort:
        _ct.sort(
            key=lambda term: term.get("sortkey"),
            reverse=reverse
        )

    return _ct


def parse_cs_course(
        tag: bs4.Tag,
        term: typing.Optional[CosCourseTerm],
) -> CosCourseInstance:
    td_tags = tag.find_all("td")

    course = CosCourseInstance({
        _course_fields_id_to_caption[i]: td_tag.text
        for i, td_tag in enumerate(td_tags)
    })
    
    # post-process
    course["people"] = course["people"].split(", ")
    if term is not None:
        course["term"] = term
    
    return course
