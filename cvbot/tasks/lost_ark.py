from random import randint
from re import U
from ..base import Task
from .. import utils
import pytesseract 
import logging
import cv2
import time

class BuyScreenTask(Task):

    def __init__(self, item, price, max_buy_stack,
        buy_screen_title,
        item_number_entry,
        buy_button,
        refresh_button,
        min_gold=1696, log_level=logging.INFO,
        threshold=2):
        super().__init__(threshold=threshold, positives=[buy_screen_title])

        self.item = item 
        self.price = price 
        self.max_buy_stack = max_buy_stack
        self.min_gold = min_gold
        self.buy_screen_title = cv2.imread(buy_screen_title)
        self.item_number_entry = cv2.imread(item_number_entry)
        self.buy_button = cv2.imread(buy_button)
        self.refresh_button = cv2.imread(refresh_button)

        self.logger = logging.getLogger('BuyScreenTask')
        self.logger.setLevel(log_level)
        self.refresh_wait = 1

        self.x_crop = [.138, .7]
        self.y_crop = [.4, .575]

        self.quant_x_crop = [.3472, .4445]
        self.quant_y_crop = [.4166, .5704]

    def _active(self, img):

        # img, _, _ = utils.crop_array_v2(img, self.y_crop, self.x_crop)

        return len(utils.match_template(img, self.buy_screen_title)[0]) > 0

    def _get_avail_count(self, img):
        img_cropped, y0, x0 = utils.crop_array_v2(img, self.quant_y_crop, self.quant_x_crop)

        img_str_og = pytesseract.image_to_string(img_cropped)
        img_str = [x.strip() for x in img_str_og.split()]
        img_str = [x for x in img_str if x]

        self.logger.debug("Quantities " +  ' '.join(img_str))

        avail_count = None
        

        for i, x in enumerate(img_str):
            if ('@' in x or '®' in x) and utils.str_to_int(x) <= self.price:
                while ('@' in img_str[i] or '®' in img_str[i]):
                    i+=1
                avail_count = img_str[i]
                break
        self.logger.debug(f"Price {self.price} Count {avail_count}")
        return avail_count if avail_count else 0

    def _run(self, img):
        img_cropped, y0, x0 = utils.crop_array_v2(img, self.y_crop, self.x_crop)

        img_str_og = pytesseract.image_to_string(img_cropped)
        img_str = [x.strip() for x in img_str_og.split()]
        img_str = [x for x in img_str if x]

        self.logger.debug("Post processed img_str " + ' '.join(img_str))

        if self.item not in img_str_og:
            raise Exception(f"Item name {self.item} not found in ocr string")

        balance_idx = img_str.index('Balance')
        self.logger.debug("Balance " + ' '.join(img_str[balance_idx+1:balance_idx+5]))
        if utils.str_to_int(img_str[balance_idx+1]) < self.min_gold:
            self.logger.info(f'Less money than {self.min_gold}, exiting')
            exit()

        avail_count = self._get_avail_count(img)

        # if 'Number' in img_str:
        #     start_idx = img_str.index('Number')
        #     stop_idx = start_idx + img_str[start_idx+1:].index('Number') + 1
        # elif 'Remaining' in img_str: 
        #     start_idx = img_str.index('Remaining')
        #     stop_idx = start_idx + img_str[start_idx + 1:].index('Quantity') + 1
        # else:
        #     self.logger.debug('Anchor words not found')
        #     utils.key_press('esc')
        #     return False
        # avail_count = 0

        # for i, x in enumerate(img_str[start_idx:stop_idx]):
        #     if ('@' in x or '®' in x) and utils.str_to_int(x) <= self.price:
        #         avail_count = img_str[start_idx + i + 1]
        #         break
        # self.logger.debug(f"Price {self.price} Count {avail_count}")

        if avail_count == 0:
            self.logger.debug('Nothing to buy, ')
            time.sleep(self.refresh_wait)
            utils.click_template(img, self.refresh_button, template_x_offset=5, template_y_offset=5)
            # utils.click_template(img_cropped, self.refresh_button, base_x_offset=x0, base_y_offset=y0,
            #     template_x_offset=5, template_y_offset=5
            # )
            return False 
        
        fresh_entry = utils.click_template(img_cropped, self.item_number_entry, base_x_offset=x0, base_y_offset=y0, 
            template_x_offset=10, template_y_offset=10
        )
        if fresh_entry:
            try:
                if int(avail_count) >= self.max_buy_stack:
                    utils.key_press(str(randint(1, 9)), hold=1)
                else:
                    utils.key_press('backspace')
                    for n in str(avail_count):
                        utils.key_press(n, hold=.1)
            except:
                utils.key_press('esc')
        utils.click_template(img, self.buy_button,
            template_x_offset=5, template_y_offset=5
        )

        self.logger.debug(f"Tryna buy {avail_count} of {self.item}")
        return True
