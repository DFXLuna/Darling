import datetime
import logger
import csv
import os.path

class Registration:
    
    def __init__(self, dbfile, logger):
        self.entries = {}
        self.dbfile = dbfile
        self.logger = logger

        if os.path.isfile(dbfile):
            self.logger.Log("Loading registration from " + dbfile)
            with open(dbfile, 'r') as f:
                reader = csv.DictReader(f)
                entriesLoaded = 0
                for row in reader:
                    self.entries[row['user']] = row['team']
                    entriesLoaded += 1
            self.logger.Log(f"Loaded {entriesLoaded} registration entries")
        else:
            self.logger.Log("Did not load registration")

    def GetEntry(self, key):
        return self.entries.get(key)

    def Register(self, name, teamNumber):
        self.entries[name] = teamNumber

    def Unregister(self, name):
        self.entries.pop(name)

    def Flush(self):
        self.logger.Log("Flushing registration to disk")
        with open(self.dbfile, 'w') as f:
            fieldnames = ['user', 'team']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for k,v in self.entries.items():
                writer.writerow( {'user': k, 'team': v} )
        self.logger.Log("Finished flushing")
