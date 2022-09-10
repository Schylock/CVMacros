import logging
import pytesseract
from cv2 import threshold
from cvbot import base
from cvbot import utils
from cvbot.tasks.lost_ark import BuyScreenTask
from cvbot.template_task import ClickTask, HotKeyTask, SequenceTask
from cvbot.utils import gen_hsv, crop_array


if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"
    base_directory = "scripts/templates/lost_ark_market"
    buy_screen_title = f"{base_directory}/buy_screen_title.bmp"
    outer_buy_button = f"{base_directory}/outer_buy_button.bmp"

    logging.basicConfig(level=logging.DEBUG)

    tasks = [
        #select item row click task: not selected, no buy menu
        #click outer buy button: row selected, no buy menu
        ClickTask(f"{base_directory}/ok.bmp"),
        # ClickTask(f"{base_directory}/armor_book.bmp", negatives=[buy_screen_title]),
        ClickTask(f"{base_directory}/blue_stone.bmp", negatives=[buy_screen_title]),
        ClickTask(outer_buy_button, negatives=[buy_screen_title]),
        BuyScreenTask(
            'Crystallized Guardian', 1, 999,
            # 'Tailoring: Applied Mending', 15, 99,
            buy_screen_title,
            f"{base_directory}/item_number_entry.bmp",
            f"{base_directory}/buy_button.bmp",
            f"{base_directory}/refresh_button.bmp", 
            log_level=logging.DEBUG,
            threshold=.1
        )
        # ClickTask(f"{base_directory}/refresh_button.bmp")
    ]

    base.Bot(tasks, cycle_delay=.1, minutes=60).main()