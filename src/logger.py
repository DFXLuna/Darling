import datetime

class Logger:

    def __init__(self, useStdOut):
        self.useStdOut = useStdOut
        self.file = None

        if not self.useStdOut:
            dt = datetime.datetime.now()
            dtString = f'[{dt.day}-{dt.month}-T{dt.hour},{dt.minute},{dt.second}]LOG.txt'
            self.file = open(dtString, 'a')

    def Log(self, message):
        ts = datetime.datetime.now()
        self.OutputWrapper(f'[{ts}]: {message}')

    def OutputWrapper(self, message):
        if self.useStdOut:
            print(message)
        else:
            self.file.write(message)
