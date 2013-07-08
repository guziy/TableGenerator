__author__ = 'huziy'


class Activity(object):
    def __init__(self, startTime=None, endTime=None):
        self.startTime = startTime
        self.endTime = endTime


class Break(Activity):
    def __init__(self, startTime=None, endTime=None, description=""):
        super(self.__class__, self).__init__(startTime=startTime, endTime=endTime)
        self.description = description


class Talk(Activity):
    def __init__(self, startTime=None, endTime=None, speakerName=""):
        super(self.__class__, self).__init__(startTime=startTime, endTime=endTime)
        self.speakerName = speakerName
        self.spAffiliation = ""
        self.spEmail = ""
        self.title = ""

    def __str__(self):
        return "'{0}' by {1}({2}) from {3}".format(self.title, self.speakerName, self.spEmail, self.spAffiliation)


class DayStartEvent(object):
    def __init__(self, title=""):
        """
        Used to mark start of a workshop day
        :param title:
        """
        self.title = title

    def __str__(self):
        return self.title