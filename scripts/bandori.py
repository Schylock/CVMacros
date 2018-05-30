import os
import cv2
import pyautogui
import pyperclip

from cvbot import base
from cvbot import utils
from cvbot.template_task import ClickTask, ScreenshotTask, SequenceTask, HotKeyTask, DragTask

import pyscreenshot as ImageGrab

from cvbot.utils import key_press, crop_image

import time


class TitledScreenshot(ScreenshotTask):
    def _run(self, img):
        filename = pyperclip.paste().replace('\n', ' ')

        if filename != '':
            ImageGrab.grab_to_file('logs/{}.bmp'.format(filename))

        key_press('home')
        time.sleep(3)

        # for i in range(3):
        #     key_press('esc')
        #     time.sleep(1)


class Transcode(ClickTask):
    def _run(self, img):
        time.sleep(.2)
        locs = utils.match_template(img, self.template)
        utils.click(locs[1][0] + 3, locs[0][0] + 3)
        time.sleep(1)

        pw = 'q1w2e3r4'
        pyautogui.typewrite(pw)


class DelFile(ClickTask):
    def _run(self, img):
        time.sleep(.2)
        locs = utils.match_template(img, self.template)
        utils.click(locs[1][0] + 3, locs[0][0] + 3)
        time.sleep(1)

        time.sleep(1)

        key_press('home')


class ClickWait(ClickTask):
    def _run(self, img):
        time.sleep(.2)
        locs = utils.match_template(img, self.template)
        utils.click(locs[1][0] + 3, locs[0][0] + 3)

        time.sleep(1)

        utils.click(locs[1][0] + 3, locs[0][0] + 3)

        time.sleep(3)



if __name__ == '__main__':

    path_prefix = 'templates/bandori/repeatable_buttons/'
    button_templates = os.listdir(path_prefix)

    priority_tasks = [
        'skip_grey_button.bmp', 'skip_pink_button.bmp',

        'ok_grey_button.bmp',
        'ok_grey_1.bmp',
        'play_button.bmp',
        'play_again.bmp',
        'ok_pink_button.bmp', 'new_story_button.bmp',
        'no_voice_button.bmp',
        'rolling.bmp',
        'skip_faded.bmp',
        'next_button.bmp'
    ]
    button_templates = priority_tasks + [
        x for x in button_templates if x not in priority_tasks
    ]

    sequence_prefix = 'templates/bandori/sequence/'

    sequence_setup = [SequenceTask(
        [
        ClickTask(sequence_prefix+'game_icon.bmp'),
         ClickTask(sequence_prefix+'check_box.bmp'), ClickTask(sequence_prefix+'agree_button.bmp'),
          ClickTask(sequence_prefix+'area_story.bmp'),
         ClickTask(sequence_prefix+'done.bmp'),

        ClickTask(path_prefix+'cancel_button.bmp'),
         ClickTask(path_prefix+'close_grey_button.bmp'),
         ClickTask(sequence_prefix+'menu_button.bmp'), ClickTask(sequence_prefix+'data_transfer_button.bmp'),
         Transcode(sequence_prefix+'password_button.bmp'),
            ClickWait(path_prefix+'ok_pink_button.bmp'),
            ClickTask(sequence_prefix+'copy_id_button.bmp'),
         ClickTask(sequence_prefix+'close.bmp'),

        ClickTask(path_prefix + 'close_grey_button.bmp'),

         ClickTask(sequence_prefix+'presents.bmp'), ClickTask(sequence_prefix+'present_accept.bmp'),
            ClickTask(path_prefix + 'ok_grey_1.bmp'),
            ClickTask(sequence_prefix + 'back.bmp'),


        ClickTask(sequence_prefix + 'mission.bmp'), ClickTask(sequence_prefix + 'mission_accept.bmp'),
            ClickTask(path_prefix + 'ok_grey_1.bmp'),
        ClickTask(sequence_prefix + 'back.bmp'),


         ClickTask(sequence_prefix+'gacha.bmp'),

         ClickTask(sequence_prefix+'1_play.bmp'),

         HotKeyTask(sequence_prefix+'more_pylons.bmp', 'esc'),

            HotKeyTask(sequence_prefix + 'back.bmp', 'esc'),

            HotKeyTask(sequence_prefix + 'back.bmp', 'esc'),

          ClickTask(sequence_prefix+'band.bmp'),
            ClickTask(sequence_prefix+'members.bmp'),

         TitledScreenshot('templates/bandori/member_list.bmp'),

            ClickTask(sequence_prefix + 'home.bmp'),

            DragTask(sequence_prefix + 'task_manager.bmp'),

            ClickTask(sequence_prefix + 'file_manager.bmp'),
            ClickTask(sequence_prefix + '6_dots.bmp'),
            ClickTask(sequence_prefix + 'refresh.bmp'),
            ClickTask(sequence_prefix + 'file_name.bmp'),
            ClickTask(sequence_prefix + '6_dots.bmp'),
            ClickTask(sequence_prefix + 'delete.bmp'),
            DelFile(sequence_prefix + 'yes.bmp')
        ]
    )]


    button_tasks = [
        ClickTask(path_prefix + file_name) for file_name in button_templates
    ]

    base.Bot(sequence_setup + button_tasks, cycle_delay=1, minutes=2400).main()



# if __name__ == '__main__':
#
#     top_left_template = cv2.imread('templates/bandori/sequence/back.bmp')
#     saved_img_dir = 'logs/'
#     for filename in os.listdir(saved_img_dir):
#         base_image = cv2.imread(saved_img_dir + filename)
#
#         cv2.imwrite(saved_img_dir + filename, crop_image(base_image, top_left_template))
#
