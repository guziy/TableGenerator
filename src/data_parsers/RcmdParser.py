from datetime import datetime
from data_parsers.activity_model import DayStartEvent, Break, Talk

__author__ = 'huziy'

import re


def _get_start_and_end_times(text):
    groups = re.findall("\\d+:\\d+", text)
    #print groups
    print text
    startTime = datetime.strptime(groups[0], "%H:%M")
    endTime = datetime.strptime(groups[1], "%H:%M")

    return startTime, endTime


def _get_title_from_one_liner(line):

    field_index = 3 if line.startswith("break") else 2

    fields = line.split(":")[field_index:]
    return ":".join(fields)[2:].strip()


def parse_block(block):
    """
    :param block: list of lines for parsing, corresponding to a given activity
    :return: object representing an activity
    """
    first_line = block[0]

    if first_line.startswith("new_day"):
        return DayStartEvent(title=":".join(first_line.split(":")[1:]).strip())
    else:

        startTime, endTime = _get_start_and_end_times(first_line)

        if first_line.startswith("break") or len(block) == 1:  # coffee break or similar ..., or one-liner event
            description = _get_title_from_one_liner(first_line)
            print(description)
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


def get_list_of_activities(path="data/workshop_2013-05-14-data.txt", block_parser = parse_block):
    """
    :param path:
    """
    activities = []
    with open(path) as f:

        lines = f.readlines()

        print(lines[-1])

        activities = []
        block = []
        for i, line in enumerate(lines):
            line = line.strip()
            print line
            if line == "" and len(block) > 0:
                activities.append(block_parser(block))
                block = []
            elif i == len(lines) - 1 and line != "":
                activities.append(block_parser([line]))
            else:
                if not line == "":
                    block.append(line)

    return activities


if __name__ == "__main__":
    get_list_of_activities()