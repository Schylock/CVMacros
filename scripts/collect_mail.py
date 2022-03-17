from cvbot import base
from cvbot import utils
from cvbot.template_task import ClickTask, HotKeyTask, SequenceTask
from cvbot.utils import gen_hsv, crop_array

logger = utils.get_logger()

if __name__ == "__main__":
    base_directory = "templates/lost_ark_market"
    select_all = f"{base_directory}/select_all.bmp"
    take_button = f"{base_directory}/take_button.bmp"
    remove_button = f"{base_directory}/remove_button.bmp"
    chest = f"{base_directory}/chest.bmp"
    envelop = f"{base_directory}/envelop.bmp"
    yes_button = f"{base_directory}/yes_button.bmp"

    tasks = [   
        ClickTask(yes_button),     
        ClickTask(select_all, threshold=1.5),
        ClickTask(take_button, positives=[chest]),
        ClickTask(remove_button, positives=[envelop], negatives=[chest]),
        
    ]

    base.Bot(tasks, cycle_delay=.25, minutes=60).main()