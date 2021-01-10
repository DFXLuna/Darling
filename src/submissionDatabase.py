import datetime
import logger
import csv
import os.path

class submissionDatabase:
    
    def __init__(self, dbfile, logger):
        # TODO:
        #  - Check for existing db
        #  - Create a folder for submission files
        #  - Create a csv file to correlate between files and teams
        self.entries = {}
        self.dbfile = dbfile
        self.logger = logger
        self.dbDisplayName = dbDisplayName

        if os.path.isfile(dbfile):
            self.logger.Log("Loading submission db from " + dbfile)
            with open(dbfile, 'r') as f:
                reader = csv.DictReader(f)
                entriesLoaded = 0
                for row in reader:
                    self.entries[row['user']] = row['team']
                    entriesLoaded += 1
            self.logger.Log(f"Loaded {entriesLoaded} submission entries")
        else:
            self.logger.Log("Did not load submission db")

    def GetEntry(self, key):
        return self.entries.get(key)

    def Register(self, name, teamNumber):
        self.entries[name] = teamNumber

    def Unregister(self, name):
        self.entries.pop(name)

    def Flush(self):
        self.logger.Log("Flushing submissiond db to disk")
        with open(self.dbfile, 'w') as f:
            fieldnames = ['user', 'team']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for k,v in self.entries.items():
                writer.writerow( {'user': k, 'team': v} )
        self.logger.Log("Finished flushing")

