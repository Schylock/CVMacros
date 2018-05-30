import time
import numpy as np
import logging
import sys

from cvbot.utils import screenshot


class Bot(object):
    def __init__(self, tasks, cycle_delay=0, minutes=None):
        self.tasks = tasks
        self.cycle_delay = cycle_delay
        self.start_time = time.time()
        self.exec_seconds = minutes * 60 if minutes else sys.maxint

    def main(self):
        while time.time() - self.start_time < self.exec_seconds:
            print 'looping'
            img = screenshot()[:900, :]
            for task in self.tasks:
                if task.active(img):
                    task.run(img)
                    break
            time.sleep(self.cycle_delay)# + np.random.normal(self.cycle_delay / 2, self.cycle_delay / 4))


class Task(object):
    def __init__(self):
        self.last_run = -1
        self.threshold = 1

    def active(self, img):
        return False

    def run(self, img):
        if time.time() - self.last_run < self.threshold:
            logging.info('task ran recently, so skipping')
            return
        self._run(img)
        self.last_run = time.time()


