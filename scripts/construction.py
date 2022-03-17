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

        #
        # HotKeyTask('2', positives=['templates/build_menu.bmp']),
        # ClickTask('templates/remove.bmp', ),
        # ClickBuild('templates/build.bmp', coords=(-1, -1), main_template='templates/mahogany_plank.bmp'),
        # ClickTask('templates/interact.bmp', coords=(-1, -1), button='right'),
        #
        # ClickTask('templates/talk_dbutler.bmp', coords=(-1, -1), button='right', threshold=15,
        #           negatives=['templates/fetch.bmp', 'templates/fetch_menu.bmp', 'templates/mahogany_plank.bmp']),
        # ClickTask('templates/fetch.bmp', ),
        # HotKeyTask('1', positives=['templates/fetch_menu.bmp']),
        #
        # # SequenceTask([
        #
        # # ], negatives=['templates/mahogany_plank.bmp']),
        #
        # HoverBuild(x=970, y=297, main_template='templates/mahogany_plank.bmp',
        #            negatives=['templates/build.bmp', 'templates/interact.bmp', 'templates/remove.bmp']),
        # HoverTask([(0, 0, 0), (6, 215, 127), (5, 181, 135)],
        #           threshold=20, negatives=['templates/mahogany_plank.bmp',
        #                                    'templates/talk_dbutler.bmp', 'templates/fetch.bmp', 'templates/fetch_menu.bmp']),
        #
        #
        #

        HotKeyTask('1', positives=['templates/build_menu_teak.bmp']),
        ClickTask('templates/remove_teak.bmp', ),
        ClickBuild('templates/build.bmp', coords=(-1, -1), main_template='templates/teak_plank.bmp'),
        ClickTask('templates/interact_teak.bmp', coords=(-1, -1), button='right'),

        ClickTask('templates/talk_dbutler.bmp', coords=(-1, -1), button='right', threshold=15,
                  negatives=['templates/fetch.bmp', 'templates/fetch_menu.bmp', 'templates/teak_plank.bmp']),
        ClickTask('templates/fetch.bmp', ),
        HotKeyTask('1', positives=['templates/fetch_menu_teak.bmp']),

        # SequenceTask([

        # ], negatives=['templates/mahogany_plank.bmp']),

        HoverBuild(x=970, y=297, main_template='templates/teak_plank.bmp',
                   negatives=['templates/build.bmp', 'templates/interact.bmp', 'templates/remove.bmp']),
        HoverTask([(0, 0, 0), (6, 215, 127), (5, 181, 135)],
                  threshold=20, negatives=['templates/teak_plank.bmp',
                                           'templates/talk_dbutler.bmp', 'templates/fetch.bmp',
                                           'templates/fetch_menu.bmp']),

    ]


    base.Bot(tasks, cycle_delay=0, minutes=2400).main()
