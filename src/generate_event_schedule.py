# -*- coding: utf-8 -*-
from datetime import datetime
import os
from data_parsers import RcmdParser, CnrcwpStudentWorkshopParser, cnrcwp_science_meeting_parser
from data_parsers.activity_model import Talk, Break, DayStartEvent
from pathlib import Path

__author__ = 'huziy'


def main(parser=None, data_path=""):
    import sys

    from jinja2 import Environment, FileSystemLoader

    env = Environment(loader=FileSystemLoader("templates"))

    env.filters["datetimenow"] = datetime.now

    talk_template = env.get_template('rcmd_talk.tpl.html')
    break_template = env.get_template("rcmd_break.tpl.html")
    day_start_template = env.get_template("rcmd_daystart.tpl.html")

    activities = RcmdParser.get_list_of_activities(path=data_path,
                                                   block_parser=parser.parse_block)

    print("Number of activities: {}".format(len(activities)))

    # Number of columns in the resulting table
    ncols = 3
    lines = []
    for index, act in enumerate(activities):
        print(type(act))
        if isinstance(act, Talk):
            lines.extend(talk_template.render(talk=act, index=index))
        elif isinstance(act, Break):
            lines.extend(break_template.render(act=act, ncols=ncols, index=index))
        elif isinstance(act, DayStartEvent):
            lines.extend(day_start_template.render(act=act, ncols=ncols))

    print("Num of lines = {}".format(len(lines)))

    html_dir = Path("html")
    if not html_dir.is_dir():
        html_dir.mkdir(parents=True)

    out_file_path = html_dir.joinpath(os.path.basename(data_path) + ".html")
    with out_file_path.open(mode="w") as f:
        f.write("<table class=\"workshop-schedule\">\n")
        f.writelines(lines)
        f.write("</table>")


# entry point
if __name__ == "__main__":

    # data_path = "data/workshop_2013-05-14-data.txt"
    #parser = RcmdParser

    #data_path = "data/workshop_2013-12-17.txt"

    # data_path = "data/cnrcwp_science_meeting_2014.txt"
    data_path = "data/cnrcwp_science_meeting_2015"
    #parser = CnrcwpStudentWorkshopParser
    #parser = cnrcwp_science_meeting_parser


    known_parsers = [
        cnrcwp_science_meeting_parser, CnrcwpStudentWorkshopParser, RcmdParser
    ]

    for the_parser in known_parsers:
        try:
            main(parser=the_parser, data_path=data_path)
        except Exception as e:
            print("{0} failed".format(the_parser))
            raise e

        print("Used {0} for data parsing".format(the_parser))
        break