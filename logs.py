import time
from datetime import datetime


class Logfile:
    def __init__(self, file):
        self.file = file
        self.f = None
    def __enter__(self):
        self.f = open(self.file, "w+")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()

    def entry(self, text):
        self.f.write("{} --- {}".format(datetime.now()   , text))

with Logfile("./logs/newlog.txt") as log:
    log.entry("This is a test message")

