import time
import cv2
import datetime
import logging

import pyautogui
# import pyscreenshot as ImageGrab

import numpy as np

from cvbot import base
from cvbot import utils
from cvbot.utils import gen_hsv, crop_array

logger = utils.get_logger()



class ClickTask(base.Task):
    relevant_screen = ((0, 1400), (0, 3000))
    # relevant_screen = ((400, 1270), (1200, 2600))
    def __init__(self, template, coords=(0, 0), button='left',  **kwargs):
        '''

        :param template: path of template bmp file
        '''
        super(ClickTask, self).__init__(**kwargs)
        self.template = None
        if template is not None:
            self.template = cv2.imread(template)
        self.coords = coords
        self.button = button


    def _active(self, img):

        if self.template is None:
            return True

        img = crop_array(img, self.relevant_screen[0], self.relevant_screen[1])
        return len(utils.match_template(img, self.template)[0]) > 0

    def _run(self, img):
        logger.info(' activated {}'.format(self.times_execute))

        if self.coords == (0, 0):
            locs = utils.match_template(img, self.template)
            pyautogui.moveTo(locs[1][0] + np.random.randint(1, 3), locs[0][0] + np.random.randint(1, 3), )
            utils.click(locs[1][0] + np.random.randint(1, 3), locs[0][0] + np.random.randint(1, 3),
                        button=self.button)
        elif self.coords == (-1, -1):
            # print('nani the fuck')
            pyautogui.click(button=self.button)
        else:
            pyautogui.click(self.coords[0] + np.random.randint(-10, 10),
                            self.coords[1] + np.random.randint(-10, 10),
                            button=self.button)
        # pyautogui.moveTo(69, 69)
        return True


class DragTask(base.Task):
    def __init__(self, template):
        '''

        :param template: path of template bmp file
        '''
        super(DragTask, self).__init__()
        self.template_path = template
        self.template = cv2.imread(template)

    def _active(self, img):
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
        logger.debug(self.template_path + ' activated')
        time.sleep(.2)
        locs = utils.match_template(img, self.template)

        pyautogui.moveTo(locs[1][0] + 3, locs[0][0] + 3)
        pyautogui.dragTo(locs[1][0] + 500, locs[0][0], 2)

        time.sleep(1)

        utils.key_press('home')

        time.sleep(1)


class HotKeyTask(base.Task):
    def __init__(self, key_str='1', n_presses=1, sleep_time=0, **kwargs):
        super(HotKeyTask, self).__init__(**kwargs)

        self.key_str = key_str
        self.n_presses = n_presses
        self.sleep_time=sleep_time

    def _run(self, img):

        for i in range(self.n_presses):
            utils.key_press(self.key_str)
            time.sleep(self.sleep_time)

        return True

class HoverLoc(base.Task):
    def __init__(self, x, y, **kwargs):
        super(HoverLoc, self).__init__(**kwargs)
        self.x, self.y = x, y

    def _run(self, img):
        pyautogui.moveTo(self.x + np.random.randint(-15, 15), self.y + np.random.randint(-15, 15))

        return True

class HoverTask(base.Task):
    def __init__(self, target_colors, choice='random', **kwargs):
        super(HoverTask, self).__init__(**kwargs)
        self.target_colors = target_colors
        assert choice in ('random', 'close', 'far', 'center')
        self.choice = choice


    def _active(self, img):

        if not super()._active(img):
            return False

        locs = gen_hsv(img, self.target_colors)

        # self.locs = np.where(locs > 0)
        # import IPython
        # IPython.embed()


        if len(np.where(locs > 0)[0]) == 0:
            return False
        # import IPython
        # IPython.embed()
        above_mean = locs[locs >= locs[locs > 0].mean()]
        cutoff = sorted(above_mean)[int(.9 * len(above_mean))]
        self.locs = np.where(locs >= cutoff)
        # import IPython
        # IPython.embed()
        # if len(self.locs[0]) == 0:
        #     return False
        return True

    def _run(self, img):
        # locs = gen_hsv(img, self.target_colors)
        # locs = np.where(locs > 0)
        locs = self.locs

        if len(locs[0]) == 0:
            return False

        if self.choice in ('close', 'far'):
            y_max, x_max, _ = img.shape
            y_mid, x_mid = y_max // 2, x_max // 2
            f = min if self.choice == 'close' else max


            index = f(range(len(locs[1])),
                      key=lambda i: (locs[1][i] - x_mid)**2 + (locs[0][i] - y_mid)**2
                      )
            # ntf = [(locs[1][i], locs[0][i]) for i in index]
            # import IPython
            # IPython.embed()

        elif self.choice == 'random':
            index = np.random.choice(range(len(locs[0])))
        elif self.choice == 'center':
            i1, i2  = np.mean(locs, axis=1)
            locs = ([i1], [i2])
            index=0

        # index=0

        x, y = locs[1][index] + np.random.randint(0, 5), locs[0][index] + np.random.randint(0, 5)



        pyautogui.moveTo(x, y)

        # index = (np.mean(locs, axis=1) + np.random.normal(0, 10)).astype(int)
        # pyautogui.moveTo(index[1], index[0])

        # index = np.random.randint(0, len(locs[0]))
        # pyautogui.moveTo(locs[1][index], locs[0][index])

        return True

# class ScreenshotTask(base.Task):
#     def __init__(self, template):
#         super(ScreenshotTask, self).__init__()
#         self.template = cv2.imread(template)
#         self.threshold = 30

#     def active(self, img):
#         logging.debug('nani sore')
#         return len(utils.match_template(img, self.template)[0]) > 0

#     def _run(self, img):
#         filename = (datetime.datetime.now() - datetime.datetime(1, 1, 1)).total_seconds()
#         ImageGrab.grab_to_file('logs/{}.bmp'.format(filename))


class SequenceTask(base.Task):
    def __init__(self, tasks, **kwargs):
        super(SequenceTask, self).__init__(**kwargs)
        self.task_sequence = tasks
        self.current_task = 0
        self.threshold=0

    def _active(self, img):
        logger.info('current task {}'.format(self.current_task))
        return self.task_sequence[self.current_task].active(img)

    def _run(self, img):
        success = self.task_sequence[self.current_task].run(img)

        if success:
            self.current_task += 1
            self.current_task %= len(self.task_sequence)

class StopTask(HotKeyTask):
    # relevant_screen = ((100, 800), (600, 1200))
    def _run(self, img):
        exit()


class WaitTask(base.Task):
    wait_time = .6
    relevant_screen = ((100, 900), (600, 1620))

    def __init__(self, **kwargs):
        super(WaitTask, self).__init__(**kwargs)

    def _run(self, img):
        time.sleep(self.wait_time + int(np.random.random() * .3))



