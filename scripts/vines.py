import cv2
import time
import logging
import numpy as np
from cvbot import base
from cvbot import utils

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


class WaitChop(base.Task):
    lower_green = np.array([45, 100, 70])
    higher_green = np.array([55, 120, 120])

    x_offset = 400
    y_offset = 400

    def __init__(self):
        super(WaitChop, self).__init__()

    def _find_vines(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return cv2.medianBlur(cv2.inRange(hsv, self.lower_green, self.higher_green), 5)

    def active(self, img):
        vines = self._find_vines(img)
        in_front = vines[425:550, 925:975]

        if np.max(vines) == 0:
            logging.info('nothing found this loop')
            return False

        if time.time() - self.last_run > max(np.random.normal(200, 30), 280) or np.max(in_front) == 0:
            logging.info('task active')
            return True

    def _run(self, img):
        vines = self._find_vines(img)[450:500, 650:1350]
        indexs = np.nonzero(vines)

        if len(indexs) == 0:
            logging.info('something most have covered the game screen')
            return

        for i in range(10):
            sample = np.random.randint(0, len(indexs[0]))
            x, y = indexs[1][sample] + 650, indexs[0][sample] + 450

            if np.sum(vines[min(0, y - 25):max(y + 25, 700), min(0, x - 25):max(x + 25, 50)]) > 200000:
                utils.click(x, y)
                logging.info('clicking ' + str(x) + ' ' + str(y))
                break
            logging.info('sampling failed... this time')


if __name__ == '__main__':
    base.Bot([WaitChop()], cycle_delay=5, minutes=2400).main()
