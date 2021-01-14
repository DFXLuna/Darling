import uuid as u

class Submission:
    def __init__(self, submitter, teamNumber, problemNumber, url, uuid=None):
        self.submitter = submitter
        self.teamNumber = teamNumber
        self.problemNumber = problemNumber
        self.url = url
        if uuid is None:
            self.uuid = u.uuid4()
        else:
            self.uuid = uuid

    def GetSubmitter(self):
        return self.submitter

    def GetTeamNumber(self):
        return self.teamNumber

    def GetProblemNumber(self):
        return self.problemNumber

    def GetUrl(self):
        return self.url

    def GetUuid(self):
        return self.uuid