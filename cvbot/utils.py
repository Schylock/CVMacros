import pyautogui
import time
import cv2
import numpy as np
import logging
# from hashlib import sha256
from mss import mss
from functools import reduce
# import pyscreenshot as ImageGrabcon

pyautogui.FAILSAFE = False

logger = logging.getLogger('tasks')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class TemplateCache(object):
    matches = {}


def _match_template(img, template):
    # now = time.time()

    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = .99
    res = np.where(res > threshold)

    return res

def match_template(img, template, caching=True):

    template_hash = hash(template.data.tobytes())
    template_cache = TemplateCache().matches

    if template_hash not in template_cache or not caching:
        template_cache[template_hash] = _match_template(img, template)

    return template_cache[template_hash]

def gen_hsv(img, target_colors, color_range=5, med_blur_range=21, color_blur_range=51):
# def gen_hsv(img, target_colors, color_range=3, med_blur_range=11, color_blur_range=51):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    range_caps = []

    for target_color in target_colors:
        lower = np.array(target_color).astype(int) - color_range
        upper = np.array(target_color).astype(int) + color_range
        range_caps.append(cv2.blur(cv2.inRange(hsv, lower, upper), (color_blur_range, color_blur_range)))
    ret = reduce(lambda x, y: x * y, range_caps)
    ret = cv2.medianBlur(ret, med_blur_range)

    return ret



def key_press(key, hold=0):
    pyautogui.keyDown(key)
    if hold:
        time.sleep(hold)
    #time.sleep(abs(np.random.normal(.1, .01, .5)))
    pyautogui.keyUp(key)


def screenshot():
    now = time.time()

    with mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)

        rgb = np.frombuffer(sct_img.rgb, np.uint8)
        rgb = rgb.reshape(sct_img.height, sct_img.width, 3)

        res =  np.flip(rgb, axis=2)
    tc = TemplateCache()
    tc.matches = {}
    return res

# def screenshot():
#     ImageGrab.grab_to_file('temp.bmp')
#     img = cv2.imread('temp.bmp')
#
#     return img


def click(x, y, button='left'):
    pyautogui.moveTo(x, y)
    pyautogui.click(button=button)
    # pyautogui.moveTo(1, 1)


def crop_image(base_image, top_left_template, x_range=800, y_range=400):
    locs = match_template(base_image, top_left_template)
    logging.debug(locs)
    x, y = locs[1][0] + 3, locs[0][0] + 3

    return base_image[y:y+y_range, x:x+x_range]



def get_logger():

    return logger

def crop_array(arr, h, w):
    return arr[h[0]:h[1], w[0]:w[1]]

def crop_array_v2(arr, h, w):
    arr_x, arr_y, _ = arr.shape
    y0, y1 = int(h[0] * arr_y), int(h[1] * arr_y)
    x0, x1 = int(w[0] * arr_x), int(w[1] * arr_x)
    return arr[x0:x1, y0:y1], y0, x0 

def str_to_int(s):
    return int(''.join([c for c in s if c.isnumeric()]))

def click_template(img, template, button='left', 
    base_x_offset=0, base_y_offset=0, 
    template_x_offset=0, template_y_offset=0,
    raise_if_missing=False
):
    locs = match_template(img, template)

    if len(locs[0]) == 0:
        if raise_if_missing:
            raise Exception('Tryin to click something that dne')
        else:
            return False

    x = locs[0][0] + base_x_offset + template_x_offset
    y = locs[1][0] + base_y_offset + template_y_offset

    pyautogui.moveTo(y, x)
    pyautogui.click(button=button, duration=.2)
    # pyautogui.click(y, x, button=button, duration=.5)
    pyautogui.moveTo(5, 5)

    return True