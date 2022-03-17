import os
import cv2
import pyautogui

from cvbot import base
from cvbot import utils
from cvbot.template_task import ClickTask, ScreenshotTask, SequenceTask, HotKeyTask, DragTask, StopTask, HoverLoc

import pyscreenshot as ImageGrab

from cvbot.utils import key_press, crop_image

import time


if __name__ == '__main__':
    #click anvil on finish, space bar in menu, click anvil if no heat bar?

    tasks = [
        StopTask(positives=['templates/smelting_oom.bmp']),

        ClickTask('templates/smelt_furnace.bmp', negatives=['templates/cancel.bmp'], coords=(-1, -1)),

        HotKeyTask( 'space', positives=['templates/begin_project_bar.bmp',], negatives=['templates/empty_bar.bmp']),

        HoverLoc(x=965, y=460, negatives=['templates/cancel.bmp']),
    ]

    base.Bot(tasks, cycle_delay=0, minutes=2400).main()
