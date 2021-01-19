import datetime
import logger
import csv
import submission as s
import os.path
import asyncio

class submissionDatabase:
    
    def __init__(self, dbfile, logger):
        self.entries = {}
        self.dbfile = dbfile
        self.logger = logger
        self.mutex = asyncio.Lock()
        self.callbacks = []

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
                if submission.GetTeamNumber() == teamNumber and submission.GetProblemNumber() == problemNumber and not submission.IsGraded():
                    return True
            return False

    async def RegisterAddSubmissionCallback(self, callback):
        self.callbacks.append(callback)

    def Flush(self):
        self.logger.Log('Flushing submission db to disk')
        with open(self.dbfile, 'w') as f:
            fieldnames = ['uuid', 'submitter', 'teamNumber', 'problemNumber', 'url', 'userId', 'gradeStatus' ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for k, v in self.entries.items():
                writer.writerow( {'uuid': k, 'submitter': v.GetSubmitter(), 
                                'teamNumber': v.GetTeamNumber(), 'problemNumber': v.GetProblemNumber(),
                                'url': v.GetUrl(), 'userId': v.GetUserId(), 'gradeStatus': v.GetGradeStatus() } )
        self.logger.Log('Finished flushing')

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



