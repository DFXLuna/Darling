import uuid

class Submission:
    def __init__(self, submitter, teamNumber, problemNumber, filePath):
        self.submitter = submitter
        self.teamNumber = teamNumber
        self.filePath = filePath
        self.uuid = uuid.uuid4()

    def GetSubmitter():
        return self.submitter

    def GetTeamNumber():
        return self.teamNumber

    def GetProblemNumber():
        return self.problemNumber

    def GetFilePath():
        