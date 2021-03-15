import threading
import logging

class Counter(object):
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.value = start
    def increment(self):
        #logging.warning('Waiting for lock')
        self.lock.acquire()
        try:
            #logging.warning('Acquired lock')
            self.value = self.value + 1
        finally:
            self.lock.release()
