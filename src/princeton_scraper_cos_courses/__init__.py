
"""
Library to fetch and parse the public Princeton COS courses history as a
Python dictionary or JSON data source.
"""

__version__ = '1.0.0'

__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "CosCourseInstance",
    "CosCourseTerm",
    "fetch_cos_courses",
]


from princeton_scraper_cos_courses.parsing import CosCourseInstance
from princeton_scraper_cos_courses.parsing import CosCourseTerm
from princeton_scraper_cos_courses.cos_courses import fetch_cos_courses


version_info = tuple(int(v) if v.isdigit() else v for v in __version__.split('.'))

