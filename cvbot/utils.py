import pyautogui
import time
import cv2
import numpy as np
import pyscreenshot as ImageGrab

pyautogui.FAILSAFE = False

def match_template(img, template):

        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        threshold = .9
        return np.where(res >= threshold)



def key_press(key):
    pyautogui.keyDown(key)
    time.sleep(abs(np.random.normal(.1, .01, 1)))
    pyautogui.keyUp(key)


def screenshot():
    ImageGrab.grab_to_file('temp.bmp')
    img = cv2.imread('temp.bmp')

    return img


def click(x, y):
    pyautogui.click(x, y)
    pyautogui.moveTo(100, 100)


def crop_image(base_image, top_left_template, x_range=800, y_range=400):
    locs = match_template(base_image, top_left_template)
    print locs
    x, y = locs[1][0] + 3, locs[0][0] + 3

    return base_image[y:y+y_range, x:x+x_range]