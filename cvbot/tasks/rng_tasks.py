import time
import pyautogui

import numpy as np

from cvbot import base
from cvbot import utils

logger = utils.get_logger()

class RngTask(base.Task):
    relevant_screen = ((0, 1080), (0, 1920))
    def __init__(self, mst = 3600, gst = 1000000, **kwargs):
        super(RngTask, self).__init__(**kwargs)
        self.mst = mst
        self.gst = gst


    def _active(self, img):
        elapsed = int(time.time() - self.last_run)

        if elapsed > self.gst:
            return True

        randnum = np.random.randint(0, self.mst)
        logger.debug(msg='elapsed {} randnum {} gst {}'.format(elapsed, randnum, self.gst))
        return  randnum <= elapsed

class RngMouseMove(RngTask):
    def __init__(self, mst = 1080, gst = 1000000, centroid=(980, 540), **kwargs):
        super(RngMouseMove, self).__init__(**kwargs)
        self.mst = mst
        self.gst = gst
        self.centroid = centroid


    def _run(self, img):
        pyautogui.moveTo(
            np.random.randint(self.centroid[0] - 250,
                              self.centroid[0] + 250),
            np.random.randint(self.centroid[1] - 250,
                              self.centroid[1] + 250))
        time.sleep(3)
        return True

class RngBreak(RngTask):
    def _run(self, img):
        time.sleep(np.random.randint(0, 300))
        return True


class RngKey(RngTask):

    def __init__(self, key, mst = 3600, **kwargs):
        super(RngKey, self).__init__(**kwargs)
        self.mst = mst
        self.key_str = key

    def _run(self, img):
        utils.key_press(self.key_str)
        time.sleep(.33 + np.random.random() / 3)

        return True