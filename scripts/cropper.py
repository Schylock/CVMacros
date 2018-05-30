import cv2
import os
from cvbot.utils import match_template


def crop_image(base_image, top_left_template, x_range = 600, y_range = 600):
    locs = match_template(base_image, top_left_template)

    x, y = locs[1][0] + 3, locs[0][0] + 3

    return base_image[x:x+x_range, y:y+y_range]

if __name__ == '__main__':

    top_left_template = cv2.imread('templates/bandori/top_left.bmp')
    saved_img_dir = 'logs/'
    for filename in os.listdir(saved_img_dir):
        base_image = cv2.imread(saved_img_dir + filename)

        cv2.imwrite('test.bmp', crop_image(base_image, top_left_template))
        break

