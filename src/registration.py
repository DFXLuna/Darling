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