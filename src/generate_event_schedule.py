# -*- coding: utf-8 -*-
from datetime import datetime
from data_parsers.RcmdParser import get_list_of_activities
from data_parsers.activity_model import Talk, Break, DayStartEvent

__author__ = 'huziy'


def main():
    import sys

    reload(sys)
    sys.setdefaultencoding("utf8")

    data_path = "data/workshop_2013-05-14-data.txt"
    from jinja2 import Environment, FileSystemLoader

    env = Environment(loader=FileSystemLoader("templates"))

    env.filters["datetimenow"] = datetime.now

    talk_template = env.get_template('rcmd_talk.tpl.html')
    break_template = env.get_template("rcmd_break.tpl.html")
    day_start_template = env.get_template("rcmd_daystart.tpl.html")

    activities = get_list_of_activities(path=data_path)



    #Number of columns in the resulting table
    ncols = 3
    lines = []
    for index, act in enumerate(activities):
        if isinstance(act, Talk):
            lines.extend(talk_template.render(talk=act, index=index))
        elif isinstance(act, Break):
            lines.extend(break_template.render(act=act, ncols=ncols, index=index))
        elif isinstance(act, DayStartEvent):
            lines.extend(day_start_template.render(act=act, ncols=ncols))


    f = open("html/rcmd_2013.html", mode="w")
    f.write("<table class=\"workshop-schedule\">\n")
    f.writelines(lines)
    f.write("</table>")
    f.close()


#entry point
if __name__ == "__main__":
    main()
