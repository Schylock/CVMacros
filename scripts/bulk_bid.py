from cv2 import threshold
from cvbot import base
from cvbot import utils
from cvbot.template_task import ClickTask, HotKeyTask, SequenceTask
from cvbot.utils import gen_hsv, crop_array

logger = utils.get_logger()

if __name__ == "__main__":
    base_directory = "templates/lost_ark_market"
    bid_buy_button = f"{base_directory}/bid_buy_button.bmp"
    bid_now_button = f"{base_directory}/bid_now_button.bmp"
    min_bid_1 = f"{base_directory}/min_bid_1.bmp"
    ok_button = f"{base_directory}/ok_button.bmp"
    select_row = f"{base_directory}/select_row.bmp"
    next_page_button = f"{base_directory}/next_page_button.bmp"

    # have trade menu open and filtered and sorted 
    tasks = [
        HotKeyTask('escape', negatives=[min_bid_1], positives=[bid_now_button]),
        ClickTask(bid_now_button, positives=[min_bid_1]),
        HotKeyTask('enter', positives=[ok_button]),
        SequenceTask([
            ClickTask(select_row, negatives=[bid_now_button], threshold=3),
            ClickTask(bid_buy_button, positives=[select_row], threshold=3),
        ], positives=[select_row], threshold=2),
        
        ClickTask(next_page_button, negatives=[select_row])
    ]

    # tasks = [        
        
        
        
    #     ClickTask(next_page_button, negatives=[select_row], threshold=1),

    #     SequenceTask([
    #         ClickTask(select_row, negatives=[bid_now_button]),
    #         ClickTask(bid_buy_button, positives=[select_row], negatives=[bid_now_button]),
    #         ClickTask(bid_now_button, positives=[min_bid_1]),
    #         HotKeyTask('enter', positives=[ok_button]),
    #         HotKeyTask('escape', negatives=[min_bid_1, ok_button], positives=[bid_now_button]),
    #     ], 
    #     # positives=[select_row], 
    #     # negatives=[bid_now_button]
    #     ),
        
    # ]

    base.Bot(tasks, cycle_delay=.35, minutes=60).main()