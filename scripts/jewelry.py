import os
import cv2
import pyautogui

from cvbot import base
from cvbot import utils
from cvbot.template_task import ClickTask, ScreenshotTask, SequenceTask, HotKeyTask, DragTask, StopTask, HoverTask

import pyscreenshot as ImageGrab

from cvbot.utils import key_press, crop_image

import time


if __name__ == '__main__':
    #click anvil on finish, space bar in menu, click anvil if no heat bar?

    tasks = [
        StopTask(positives=['templates/smelting_oom.bmp']),
        SequenceTask([
            #ClickTask('templates/banker.bmp', coords=(-1, -1)),
            ClickTask('templates/use_bank_chest.bmp', coords=(-1, -1)),
            HotKeyTask('2', positives=['templates/bank.bmp']),
            ClickTask('templates/smelt_furnace.bmp', coords=(-1, -1)),
            HotKeyTask('space', positives=['templates/begin_project_bar.bmp']),
        ]),
        HoverTask([(12, 180, 249),(24, 78, 121)], threshold=10,
                  positives=['templates/diamond.bmp', ], negatives=['templates/cancel.bmp',]),
        HoverTask( [(25, 170, 129), (22, 119, 92), (22, 123, 87),],
                  threshold=10, negatives=['templates/diamond.bmp',  ])
    ]


    base.Bot(tasks, cycle_delay=0, minutes=2400).main()
