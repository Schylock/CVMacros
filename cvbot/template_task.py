import time
import cv2
import datetime

import pyautogui
import pyscreenshot as ImageGrab

from cvbot import base
from cvbot import utils


class ClickTask(base.Task):
    def __init__(self, template):
        '''

        :param template: path of template bmp file
        '''
        super(ClickTask, self).__init__()
        self.template_path = template
        self.template = cv2.imread(template)

    def active(self, img):
        # print self.template_path
        #
        # if self.template_path == 'templates/bandori/repeatable_buttons/ok_pink_button.bmp':
        #     nani = cv2.matchTemplate(img, self.template, cv2.TM_CCOEFF_NORMED)
        #
        #     nani_max = np.max(nani)
        #     import IPython
        #     IPython.embed()

        return len(utils.match_template(img, self.template)[0]) > 0

    def _run(self, img):
        print self.template_path + ' activated'
        time.sleep(.2)
        locs = utils.match_template(img, self.template)
        utils.click(locs[1][0] + 3, locs[0][0] + 3)


class DragTask(base.Task):
    def __init__(self, template):
        '''

        :param template: path of template bmp file
        '''
        super(DragTask, self).__init__()
        self.template_path = template
        self.template = cv2.imread(template)

    def active(self, img):
        # print self.template_path
        #
        # if self.template_path == 'templates/bandori/repeatable_buttons/ok_pink_button.bmp':
        #     nani = cv2.matchTemplate(img, self.template, cv2.TM_CCOEFF_NORMED)
        #
        #     nani_max = np.max(nani)
        #     import IPython
        #     IPython.embed()

        return len(utils.match_template(img, self.template)[0]) > 0

    def _run(self, img):
        print self.template_path + ' activated'
        time.sleep(.2)
        locs = utils.match_template(img, self.template)

        pyautogui.moveTo(locs[1][0] + 3, locs[0][0] + 3)
        pyautogui.dragTo(locs[1][0] + 500, locs[0][0], 2)

        time.sleep(1)

        utils.key_press('home')


class HotKeyTask(base.Task):
    def __init__(self, template, key_str='1'):
        super(HotKeyTask, self).__init__()
        self.template = cv2.imread(template)
        self.key_str = key_str

    def active(self, img):
        return len(utils.match_template(img, self.template)[0]) > 0

    def _run(self, img):
        time.sleep(.2)
        utils.key_press(self.key_str)
        time.sleep(1)


class ScreenshotTask(base.Task):
    def __init__(self, template):
        super(ScreenshotTask, self).__init__()
        self.template = cv2.imread(template)
        self.threshold = 30

    def active(self, img):
        print 'nani sore'
        return len(utils.match_template(img, self.template)[0]) > 0

    def _run(self, img):
        filename = (datetime.datetime.now() - datetime.datetime(1, 1, 1)).total_seconds()
        ImageGrab.grab_to_file('logs/{}.bmp'.format(filename))


class SequenceTask(base.Task):
    def __init__(self, tasks):
        super(SequenceTask, self).__init__()
        self.task_sequence = tasks
        self.current_task = 0

    def active(self, img):
        return self.task_sequence[self.current_task].active(img)

    def _run(self, img):
        self.task_sequence[self.current_task]._run(img)

        self.current_task += 1
        self.current_task %= len(self.task_sequence)

