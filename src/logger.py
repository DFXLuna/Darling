import datetime

class Logger:

    def __init__(self, useStdOut):
        self.useStdOut = useStdOut

        if not self.useStdOut:
            dt = datetime.now()
            dtString = f'[{dt.date.day}-{dt.date.month}-T{dt.time.hour},{dt.time.minute},{dt.time.second}]LOG.txt'
            self.file = open(dtString, 'a')

    def __del__(self):
        if not self.useStdOut:
            self.file.close()

    def Log(self, message):
        ts = datetime.datetime.now()
        self.OutputWrapper(f'[{ts}]: {message}')

    def OutputWrapper(self, message):
        if self.useStdOut:
            print(message)
        else:
            self.file.write(message)
