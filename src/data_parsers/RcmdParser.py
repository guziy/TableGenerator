from datetime import datetime
from data_parsers.activity_model import DayStartEvent, Break, Talk

__author__ = 'huziy'

import re


def _get_start_and_end_times(text):
    groups = re.findall("\\d+:\\d+", text)
    #print groups
    startTime = datetime.strptime(groups[0], "%H:%M")
    endTime = datetime.strptime(groups[1], "%H:%M")

    return startTime, endTime


def _get_title_from_one_liner(line):
    fields = line.split(":")[3:]
    return ":".join(fields)[2:].strip()


def _parse_block(block):
    """
    :param block: list of lines for parsing, corresponding to a given activity
    :return: object representing an activity
    """
    first_line = block[0]

    if first_line.startswith("new_day"):
        return DayStartEvent(title=first_line.split(":")[1].strip())
    else:

        startTime, endTime = _get_start_and_end_times(first_line)

        if first_line.startswith("break") or len(block) == 1:  # coffee break or similar ..., or one-liner event
            description = _get_title_from_one_liner(first_line)
            return Break(startTime=startTime, endTime=endTime, description=description)
        else:  # the activity corresponding to a talk
            speakerName = block[1]
            spEmail = block[2]
            spAffiliation = block[3]

            title = " ".join([line.strip() for line in block[4:]])

            talk = Talk(startTime=startTime, endTime=endTime, speakerName=speakerName)
            talk.spEmail = spEmail
            talk.spAffiliation = spAffiliation
            talk.title = title
            return talk


def get_list_of_activities(path="data/workshop_2013-05-14-data.txt"):
    """

    :param path:
    """
    f = open(path)

    lines = f.readlines()

    activities = []
    block = []
    for line in lines:
        line = line.strip()
        if line == "" and len(block) > 0:
            activities.append(_parse_block(block))
            block = []
        else:
            if not line == "":
                block.append(line)

    f.close()
    return activities

if __name__ == "__main__":
    get_list_of_activities()