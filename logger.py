import os
import datetime


class Logger:
    def __init__(self, path=f"log/{str(datetime.datetime.now()).replace(':', '-')}.txt"):
        self.path = path
        dirname = os.path.dirname(self.path)
        if not os.path.exists(dirname):
            os.mkdir(dirname)

    def log(self, *args, **kwargs):
        with open(self.path, "a") as logfile:
            logfile.write('; '.join([str(arg) for arg in args]) + '\n')
            logfile.write('\n'.join([f"{key} : {kwargs[key]}" for key in kwargs.keys()]) + '\n')


logger = Logger()
