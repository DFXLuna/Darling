import datetime
import logger
import csv
import submission as s
import os.path
import asyncio

class submissionDatabase:
    
    def __init__(self, dbfile, logger):
        # TODO:
        #  - Check for existing db
        self.entries = {}
        self.dbfile = dbfile
        self.logger = logger
        self.mutex = asyncio.Lock()

        if os.path.isfile(dbfile):
            self.logger.Log("Loading submission db from " + dbfile)
            with open(dbfile, 'r') as f:
                reader = csv.DictReader(f)
                entriesLoaded = 0
                for row in reader:
                    self.entries[row['uuid']] = s.Submission(row['submitter'], row['teamNumber'],
                                                row['problemNumber'], row['url'], row['uuid'])
                    entriesLoaded += 1
            self.logger.Log(f"Loaded {entriesLoaded} submission entries")
        else:
            self.logger.Log("Did not load submission db")

    async def GetSubmission(self, key):
        async with self.mutex:
            self.logger.Log(f"GetSubmission {key}")
            return self.entries.get(key)

    async def GetAllSubmissions(self):
        async with self.mutex:
            self.logger.Log(f"GetAllSubmissions")
            return List(self.entries.values())

    async def AddSubmission(self, submitter, teamNumber, problemNumber, url):
        async with self.mutex:
            toAdd = s.Submission(submitter, teamNumber, problemNumber, url)
            self.entries[toAdd.uuid] = toAdd
            self.logger.Log(f"AddSubmission {toAdd.GetUuid()}, {submitter}, {teamNumber}, {problemNumber}")

    def Flush(self):
        self.logger.Log("Flushing submissiond db to disk")
        with open(self.dbfile, 'w') as f:
            fieldnames = ['uuid', 'submitter', 'teamNumber', 'problemNumber', 'url']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for k, v in self.entries.items():
                writer.writerow( {'uuid': k, 'submitter': v.GetSubmitter(), 
                                'teamNumber': v.GetTeamNumber(), 'problemNumber': v.GetProblemNumber(),
                                'url': v.GetUrl() } )
        self.logger.Log("Finished flushing")

