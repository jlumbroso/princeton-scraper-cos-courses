
import datetime
import json
import typing

import comma

import princeton_scraper_cos_courses.cos_courses
import princeton_scraper_cos_courses.parsing


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "json_output",
    "csv_output",
]


# noinspection PyBroadException
def json_output() -> typing.Optional[str]:
    try:
        data = princeton_scraper_cos_courses.cos_courses.fetch_cos_courses()

        return json.dumps({
            "source": "https://github.com/jlumbroso/princeton-scraper-cos-courses/",
            "timestamp": datetime.datetime.now().isoformat(),
            "data": data,
        }, indent=2)
    except Exception:
        raise
        return


def csv_output() -> typing.Optional[str]:
    try:
        data = princeton_scraper_cos_courses.cos_courses.fetch_cos_courses()

        # for row in data:
        #     del row["research"]
        #     row["affiliations"] = ";".join(row["affiliations"])
        return comma.dumps(data)
    except Exception:
        return
