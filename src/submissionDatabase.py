import datetime
import numProblems
import logger
import csv
import submission as s
import os.path
import asyncio

class submissionDatabase:
    
    def __init__(self, dbfile, logger):
        self.num_problems = numProblems.num_problems
        self.entries = {}
        self.dbfile = dbfile
        self.logger = logger
        self.mutex = asyncio.Lock()
        self.callbacks = []
        self.passes = [0] * self.num_problems
        self.fails = [0] * self.num_problems

        if os.path.isfile(dbfile):
            self.logger.Log("Loading submission db from " + dbfile)
            with open(dbfile, 'r') as f:
                reader = csv.DictReader(f)
                entriesLoaded = 0
                for row in reader:
                    self.entries[row['uuid']] = s.Submission(row['submitter'], int(row['teamNumber']),
                                                int(row['problemNumber']), row['url'],  int(row['userId']),
                                                row['gradeStatus'], row['uuid'])
                    entriesLoaded += 1
                for entry in self.entries.values():
                    if entry.IsPass():
                        self.passes[entry.GetProblemNumber()] += 1
                    else:
                        self.fails[entry.GetProblemNumber()] += 1
            self.logger.Log(f'Loaded {entriesLoaded} submission entries')
        else:
            self.logger.Log('Did not load submission db')

    async def GetSubmission(self, key):
        async with self.mutex:
            self.logger.Log(f'GetSubmission {key}')
            return self.entries.get(key)

    async def GetAllSubmissions(self):
        async with self.mutex:
            self.logger.Log('GetAllSubmissions')
            return list(self.entries.values())

    #returns the userID, teamnumber and problem number of the passed submission
    async def PassSubmission(self, uuid):
        userId = None
        teamNumber = None
        problemNumber = None
        async with self.mutex:
            self.logger.Log(f'Pass {uuid}')
            entry = self.entries[uuid]
            self.passes[entry.GetProblemNumber()] += 1
            entry.Pass()
            userId = entry.GetUserId()
            teamNumber = entry.GetTeamNumber()
            problemNumber = entry.GetProblemNumber()
        await self.AsyncFlush()
        #increment team's score
        return (userId, teamNumber, problemNumber)

    #returns the userID, teamnumber and problem number of the failed submission
    async def FailSubmission(self, uuid):
        userId = None
        teamNumber = None
        problemNumber = None
        async with self.mutex:
            self.logger.Log(f'fail {uuid}')
            entry = self.entries[uuid]
            self.fails[entry.GetProblemNumber()] += 1
            entry.Fail()
            userId = entry.GetUserId()
            teamNumber = entry.GetTeamNumber()
            problemNumber = entry.GetProblemNumber()
        await self.AsyncFlush()
        #increment team's score
        return (userId, teamNumber, problemNumber)

    async def AddSubmission(self, submitter, teamNumber, problemNumber, url, userId):
        async with self.mutex:
            toAdd = s.Submission(submitter, teamNumber, problemNumber, url, userId)
            self.entries[toAdd.uuid] = toAdd
            self.logger.Log(f'AddSubmission {toAdd.GetUuid()}, {submitter}, {teamNumber}, {problemNumber}, {userId}')
            await self.AddSubmissionCallbacks(toAdd)

    async def AddSubmissionCallbacks(self, submission):
        preparedFunctions = []
        for callback in self.callbacks:
            preparedFunctions.append(callback(submission))
        await asyncio.gather(*preparedFunctions)

    async def SubmissionAlreadyInProgress(self, teamNumber, problemNumber):
        async with self.mutex:
            self.logger.Log(f'SubmissionAlreadyInProgress {teamNumber}, {problemNumber}')
            for submission in self.entries.values():
                if submission.GetTeamNumber() == teamNumber and submission.GetProblemNumber() == problemNumber and not submission.IsFail():
                    return True
            return False

    async def RegisterAddSubmissionCallback(self, callback):
        self.callbacks.append(callback)

    def SyncFlush(self):
        with open(self.dbfile, 'w') as f:
            fieldnames = ['uuid', 'submitter', 'teamNumber', 'problemNumber', 'url', 'userId', 'gradeStatus' ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            count = 0
            for k, v in self.entries.items():
                writer.writerow( {'uuid': k, 'submitter': v.GetSubmitter(), 
                                'teamNumber': v.GetTeamNumber(), 'problemNumber': v.GetProblemNumber(),
                                'url': v.GetUrl(), 'userId': v.GetUserId(), 'gradeStatus': v.GetGradeStatus() } )
                count += 1
        self.logger.Log(f'Flushed {count} submissions to disk on exit')

    async def AsyncFlush(self):
        async with self.mutex:
            with open(self.dbfile, 'w') as f:
                fieldnames = ['uuid', 'submitter', 'teamNumber', 'problemNumber', 'url', 'userId', 'gradeStatus' ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                count = 0
                for k, v in self.entries.items():
                    writer.writerow( {'uuid': k, 'submitter': v.GetSubmitter(), 
                                    'teamNumber': v.GetTeamNumber(), 'problemNumber': v.GetProblemNumber(),
                                    'url': v.GetUrl(), 'userId': v.GetUserId(), 'gradeStatus': v.GetGradeStatus() } )
                    count += 1
        self.logger.Log(f'Flushed {count} submissions')

    async def NumUngradedEntries(self):
        self.logger.Log('NumUngradedEntries')
        return len(await self.GetUngradedSubmissionUuids())

    async def GetUngradedSubmissionUuids(self):
        uuids = []
        self.logger.Log('GetUngradedSubmissionUuids')
        async with self.mutex:
            for entry in self.entries.values():
                if not entry.IsGraded():
                    uuids.append(entry.GetUuid())
            return uuids

    async def GetUngradedSubmissions(self):
        submissions = []
        self.logger.Log('GetUngradedSubmission')
        async with self.mutex:
            for entry in self.entries.values():
                if not entry.IsGraded():
                    submissions.append(entry)
            return submissions

    async def GetTeamSubmissions(self, teamNumber):
        self.logger.Log('GetTeamSubmissions')
        submissions = []
        async with self.mutex:
            for entry in self.entries.values():
                if entry.GetTeamNumber() == teamNumber:
                    submissions.append(entry)
            return submissions

    async def GetPasses(self):
        return self.passes

    async def GetFails(self):
        return self.fails

    async def DeleteSubmission(self, uuid):
        async with self.mutex:
            if uuid in self.entries.keys():
                del self.entries[uuid]
                return True
        return False

