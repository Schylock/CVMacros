import time

from cvbot import base
from cvbot.tasks.rng_tasks import RngMouseMove
from cvbot.template_task import ClickTask, HotKeyTask, StopTask, WaitTask, SequenceTask, HoverTask, HoverLoc

class HoverBankerGE(HoverTask):
    def __init__(self, **kwargs):
        super(HoverBankerGE, self).__init__(
            [(8, 33, 145),(13, 51, 45),(178, 46, 95),(178, 14, 226)], **kwargs
        )

class HotKeyTask(HotKeyTask):
    relevant_screen = ((0, 1080), (600, 1700))

class ClickTask(ClickTask):
    relevant_screen = ((0, 1080), (600, 1700))

class HoverLoc(HoverLoc):
    relevant_screen = ((0, 1080), (600, 1700))

if __name__ == '__main__':
    herb = 'dweed'
    bank_preset = '2'
    taskbar_slot = '2'

    clean_template = 'templates/c_{}.bmp'.format(herb)
    grimy_template = 'templates/g_{}.bmp'.format(herb)


    tasks = [
        ClickTask(template=None, positives=[clean_template, 'templates/use_bank_chest.bmp'],
                  negatives=['templates/bank.bmp', grimy_template, 'templates/cancel.bmp'],
                  threshold=3, coords=(-1, -1)),
        HotKeyTask(bank_preset, n_presses=1, positives=['templates/bank.bmp']),

        HotKeyTask(taskbar_slot, n_presses=1,
                   positives=[grimy_template], negatives=['templates/cancel.bmp', 'templates/bank.bmp'], threshold=3),

        HotKeyTask('space', n_presses=1, positives=['templates/clean_button.bmp']),
        HoverLoc(x=965, y=460, negatives=[grimy_template],
                 positives=[clean_template],threshold=60),
    ]


    base.Bot(tasks, cycle_delay=0, minutes=2400).main()
