import datetime

class Registration:
    
    def __init__(self):
        self.entries = {}

    def GetEntry(self, key):
        return self.entries.get(key)

    def Register(self, name, teamNumber):
        self.entries[name] = teamNumber
    
    def Unregister(self, name):
        if name in self.entries:
            self.entries.pop(name)
    
    def Flush(self):
        dt = datetime.datetime.now()
        dtString = f'[{dt.day}-{dt.month}-T{dt.hour},{dt.minute},{dt.second}]db.csv'
        with open(dtString, 'w') as f:
            for k,v in self.entries.items():
                f.write(f'{k}, {v}\n')
