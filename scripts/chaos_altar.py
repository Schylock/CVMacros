import os
import cv2
import pyautogui

from cvbot import base
from cvbot import utils
from cvbot.template_task import ClickTask, ScreenshotTask, SequenceTask, HotKeyTask, DragTask, StopTask, HoverTask, \
    HoverLoc

import pyscreenshot as ImageGrab

from cvbot.utils import key_press, crop_image

import time

class HoverBuild(HoverLoc):
    def _active(self, img):
        if len(utils.match_template(img, self.main_template)[0]) < 8 * 2:
            return False
        return super()._active(img)

class ClickBuild(ClickTask):
    def _active(self, img):
        # print(len(utils.match_template(img, self.main_template)[0]))
        if len(utils.match_template(img, self.main_template)[0]) < 8 * 2:
            return False
        return super()._active(img)

if __name__ == '__main__':
    #stand next to wall, build above, zoom in angle up

    tasks = [
        ClickTask('templates/talk_simon.bmp', coords=(-1, -1), button='right',
                  negatives=['templates/dragon_bones.bmp']),
        ClickTask('templates/pray_chaos_altar.bmp', coords=(-1, -1), button='right',
                  positives=['templates/dragon_bones.bmp'], negatives=['templates/prayer.bmp']),



        ClickTask('templates/bank_simon.bmp', ),


        ClickTask('templates/offer_chaos_altar.bmp', ),

        HotKeyTask('1', positives=['templates/bank.bmp']),

        HoverTask([(162, 65, 51),
                   (160, 66, 85),
                   (102, 21, 209),
                   (164, 71, 47),
                   (107, 70, 165)],
                  threshold=5,
                  negatives=['templates/prayer.bmp', 'templates/offer_chaos_altar.bmp', 'templates/bank.bmp'],
                  positives=['templates/dragon_bones.bmp']),
        HoverTask([(36, 75, 159), (38, 98, 68)],
                  threshold=2,
                  negatives=['templates/dragon_bones.bmp', 'templates/talk_simon.bmp', 'templates/bank_simon.bmp']),

    ]


    base.Bot(tasks, cycle_delay=0, minutes=2400).main()
