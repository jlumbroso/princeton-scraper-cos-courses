
import datetime
import os
import json
import sys

import princeton_scraper_cos_courses.output
import princeton_scraper_cos_courses.parsing


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"


# noinspection PyBroadException
if __name__ == "__main__":

    is_csv = False
    has_images = False
    person_types = None
    generate_feeds = False
    feeds_output = None

    # "parse" command line parameter
    # NOTE: should be a real command line tool

    if len(sys.argv) > 0:
        argv = sys.argv[:]

        if "--csv" in argv:
            is_csv = True
            argv.remove("--csv")

        # NOTE: should use a command line parser!
        if "--feeds" in sys.argv:
            generate_feeds = True
            feed_output_index = argv.index("--feeds") + 1
            if feed_output_index != 0 and feed_output_index < len(argv):
                feeds_output = argv[feed_output_index]

            del argv[feed_output_index]
            argv.remove("--feeds")

    # generate feeds
    if generate_feeds:
        save_all = False
        
        records = princeton_scraper_cos_courses.output.json_output()
        output = json.dumps(records, indent=2)

        dirpath = os.path.join(feeds_output, "feeds")
        filepath = os.path.join(dirpath, "index.json")

        # ensure the folder exists
        try:
            os.makedirs(dirpath)
        except FileExistsError:
            pass

        with open(filepath, "w") as f:
            f.write(output)

        filepath = os.path.join(feeds_output, "feeds", "index.json")
        with open(filepath, "w") as f:
            f.write(json.dumps({
                "source": "https://github.com/jlumbroso/princeton-scraper-cos-courses/",
                "timestamp": datetime.datetime.now().isoformat(),
                "data": records,
            }, indent=2))

        sys.exit(0)

    # output selected format

    output = None
    if is_csv:
        output = princeton_scraper_cos_courses.output.csv_output()
    else:
        output = princeton_scraper_cos_courses.output.json_output()

    if output is None:
        sys.exit(1)
    else:
        print(output)
        sys.exit(0)
