from data_parsers.activity_model import DayStartEvent, Break, Talk

__author__ = 'huziy'

import RcmdParser



def parse_block(block):
    """
    :param block: list of lines for parsing, corresponding to a given activity
    :return: object representing an activity
    """
    first_line = block[0]

    if first_line.startswith("new_day"):
        return DayStartEvent(title=":".join(first_line.split(":")[1:]).strip())
    else:

        startTime, endTime = RcmdParser.get_start_and_end_times(first_line)

        if first_line.startswith("break") or len(block) == 1:  # coffee break or similar ..., or one-liner event
            description = RcmdParser._get_title_from_one_liner(first_line)
            print(description)
            return Break(startTime=startTime, endTime=endTime, description=description)
        else:  # the activity corresponding to a talk
            print block
            speakerName = block[2] if len(block) >= 3 else ""
            assert len(block) >= 3
            #spEmail = block[2]
            #spAffiliation = block[3]

            title = block[1]
            #" ".join([line.strip() for line in block[4:]])

            talk = Talk(startTime=startTime, endTime=endTime, speakerName=speakerName)
            talk.title = title
            return talk


