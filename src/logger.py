import datetime
import time

class Logger:

    def __init__(self, useStdOut):
        self.useStdOut = useStdOut
        self.file = None
        self.lastFlush = time.time()

        if not self.useStdOut:
            dt = datetime.datetime.now()
            dtString = f'[{dt.month}-{dt.day}-T{dt.hour},{dt.minute},{dt.second}]LOG.txt'
            self.file = open(dtString, 'a')

    def Log(self, message):
        ts = datetime.datetime.now()
        self.OutputWrapper(f'[{ts}]: {message}')

    def LogToConsole(self, message):
        ts = datetime.datetime.now()
        print(f'[{ts}]: {message}')

    def OutputWrapper(self, message):
        if self.useStdOut:
            print(message)
        else:
            message += '\n'
            self.file.write(message)
            if time.time() - self.lastFlush > 10:
                self.file.flush()
                self.lastFlush = time.time()
