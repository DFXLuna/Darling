import uuid as u

class Submission:
    def __init__(self, submitter, teamNumber, problemNumber, url, userId, gradeStatus='ungraded', uuid=None):
        self.submitter = submitter
        self.teamNumber = teamNumber
        self.problemNumber = problemNumber
        self.url = url
        self.userId = userId
        self.gradeStatus = gradeStatus
        if uuid is None:
            self.uuid = str(u.uuid4())
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

    def GetUserId(self):
        return self.userId

    def GetGradeStatus(self):
        return self.gradeStatus

    def GetUuid(self):
        return self.uuid

    def Pass(self):
        self.gradeStatus = 'pass'
    
    def Fail(self):
        self.gradeStatus = 'fail'

    def Ungrade(self):
        self.gradeStatus = 'ungraded'
    
    def IsGraded(self):
        return self.gradeStatus != 'ungraded'

    def IsPass(self):
        return self.gradeStatus == 'pass'

    def IsFail(self):
        return self.gradeStatus == 'fail'