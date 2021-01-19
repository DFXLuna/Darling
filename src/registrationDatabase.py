import datetime
import logger
import csv
import os.path
import asyncio

class RegistrationDatabase:
    
    def __init__(self, dbfile, logger):
        self.entries = {}
        self.dbfile = dbfile
        self.logger = logger
        self.mutex = asyncio.Lock()

        if os.path.isfile(dbfile):
            self.logger.Log("Loading registration from " + dbfile)
            with open(dbfile, 'r') as f:
                reader = csv.DictReader(f)
                entriesLoaded = 0
                for row in reader:
                    self.entries[row['user']] = int(row['team'])
                    entriesLoaded += 1
            self.logger.Log(f"Loaded {entriesLoaded} registration entries")
        else:
            self.logger.Log("Did not load registration")

    async def GetEntry(self, key):
        async with self.mutex:
            return self.entries.get(key)

    async def Register(self, name, teamNumber):
        async with self.mutex:
            self.entries[name] = teamNumber

    async def Unregister(self, name):
        async with self.mutex:
            self.entries.pop(name)

    def Flush(self):
        with open(self.dbfile, 'w') as f:
            fieldnames = ['user', 'team']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            count = 0
            for k,v in self.entries.items():
                writer.writerow( {'user': k, 'team': v} )
                count += 1
        self.logger.Log(f'Flushed {count} registrations to disk')
