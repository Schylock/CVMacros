import time

import cv2
import numpy as np
import logging
import sys

import pyautogui

from cvbot.utils import screenshot, get_logger, match_template, crop_array

logger = get_logger()


class Bot(object):
    def __init__(self, tasks, cycle_delay=0, minutes=None):
        self.tasks = tasks
        self.cycle_delay = cycle_delay
        self.start_time = time.time()
        self.exec_seconds = minutes * 60 if minutes else sys.maxint

        self.cycles = 0

    def main(self):
        last = time.time()
        last_task_id = 0

        while time.time() - self.start_time < self.exec_seconds:
            # logger.debug('cycle {}'.format(self.cycles))
            img = screenshot()#[:900, :]
            tasks_tried = 0
            # for task in self.tasks:
            for i in range(len(self.tasks)):
                task = self.tasks[(i+last_task_id)%len(self.tasks)]
                if task.active(img):
                    print(task)
                    last_task_id = (i+last_task_id)%len(self.tasks)
                    task.run(img)
                    break
                tasks_tried += 1
            time.sleep(self.cycle_delay)# + np.random.normal(self.cycle_delay / 2, self.cycle_delay / 4))
            current = time.time()
            logger.debug('elapsed since last {} tasks tried {} seconds remaining {}'.format(
                current - last, tasks_tried, int(self.exec_seconds - time.time() + self.start_time)))
            last = current
            self.cycles+=1

class Task(object):
    # relevant_screen = ((100, 1000), (600, 1600))
    # relevant_screen = ((0, 1040), (0, 1920))
    relevant_screen = ((400, 1270), (1200, 2600))
    # relevant_screen = ((1200, 2600), (400, 1270))
    def __init__(self, threshold=2, positives=[], negatives=[], pos_w_count = [], main_template=None):
        self.last_run = time.time() - threshold
        self.threshold = threshold
        self.times_activate = 0
        self.times_execute = 0
        self.positives = [cv2.imread(x) for x in positives]
        self.negatives = [cv2.imread(x) for x in negatives]
        self.pos_w_count = [
            (cv2.imread(x), count) for (x, count) in pos_w_count
        ]
        self.main_template = None if main_template is None else cv2.imread(main_template)

    def _active(self, img):
        return True

    def active(self, img):

        if time.time() - self.last_run < self.threshold:

            # logger.info('task ran recently, so skipping {}'.format(self.__str__()))
            return False

        if not self._active(img):
            return False

        img = crop_array(img, self.relevant_screen[0], self.relevant_screen[1])
        if len(self.negatives) > 0:
            for template in self.negatives:
                if len(match_template(img, template)[0]) > 0:
                    return False

        if len(self.positives) > 0:
            for template in self.positives:
                if len(match_template(img, template)[0]) == 0:
                    return False

        if len(self.pos_w_count) > 0:
            for (template, count) in self.pos_w_count:
                if len(match_template(img, template)[0]) < count:
                    return False

        return True

    def run(self, img):
        self.times_execute += 1
        status = self._run(img)
        self.last_run = time.time()
        logger.info('running {}'.format(self.__str__()))
        return status

    def _run(self, img):
        return True


