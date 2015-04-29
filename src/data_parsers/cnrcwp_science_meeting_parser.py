from data_parsers import RcmdParser
from data_parsers.activity_model import DayStartEvent, Break, Talk
import re
__author__ = 'huziy'



def get_break_title(line):
    return re.split(r"\d+:\d+", line)[-1]

def parse_block(block):
    """
    :param block: list of lines for parsing, corresponding to a given activity
    :return: object representing an activity
    """
    first_line = block[0]

    if first_line.startswith("new_day"):
        return DayStartEvent(title=":".join(first_line.split(":")[1:]).strip())
    else:

        [startTime, endTime] = RcmdParser.get_start_and_end_times(first_line)

        if first_line.startswith("break") or len(block) == 1:  # coffee break or similar ..., or one-liner event
            description = get_break_title(first_line)
            print(description)
            return Break(startTime=startTime, endTime=endTime, description=description)
        else:  # the activity corresponding to a talk
            print(block)
            speakerName = block[1] if len(block) >= 3 else ""
            #spEmail = block[2]
            #spAffiliation = block[3]

            title = block[2] if len(block) >= 3 else block[1]
            #" ".join([line.strip() for line in block[4:]])

            talk = Talk(startTime=startTime, endTime=endTime, speakerName=speakerName)
            talk.title = title


            for the_line in block:
                if the_line.strip().lower().startswith("homepage"):
                    talk.speakerHomePage = the_line.split()[-1]



            return talk


