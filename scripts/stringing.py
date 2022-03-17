import time

from cvbot import base
from cvbot.tasks.rng_tasks import RngMouseMove
from cvbot.template_task import ClickTask, HotKeyTask, StopTask, WaitTask, SequenceTask, HoverTask, HoverLoc

class HoverBankerGE(HoverTask):
    def __init__(self, **kwargs):
        super(HoverBankerGE, self).__init__(
            [(8, 33, 145),(13, 51, 45),(178, 46, 95),(178, 14, 226)], **kwargs
        )


if __name__ == '__main__':
    #click anvil on finish, space bar in menu, click anvil if no heat bar?

    # tasks = [
    #     StopTask(positives=['templates/smelting_oom.bmp']),
    #     ClickTask('templates/use_bank_chest.bmp',
    #               negatives=['templates/bowstring.bmp'],
    #                coords=(-1, -1)),
    #     # ClickTask('templates/banker.bmp',
    #     #           negatives=['templates/bowstring.bmp'],
    #     #           coords=(-1, -1)),
    #     HotKeyTask('1', n_presses=1, positives=['templates/bank.bmp', ]),
    #     HotKeyTask('4', n_presses=1, positives=['templates/bowstring.bmp', ], negatives=['templates/cancel.bmp']),
    #     HotKeyTask('space', positives=['templates/fletch_button.bmp', ]),
    #
    #     HoverLoc(x=965, y=460, negatives=['templates/bowstring.bmp'], threshold=60),
    #     # HoverTask( [(0, 11, 238), (178, 14, 226), (0, 0, 255), (5, 15, 206), (13, 155, 143)],
    #     #           threshold=10, negatives=['templates/bowstring.bmp', 'templates/banker.bmp' ])
    # ]

    tasks = [
        # RngMouseMove(),
        # StopTask(positives=['templates/smelting_oom.bmp']),
        # WaitTask(threshold=0, positives=['templates/g_dweed.bmp', 'templates/cancel.bmp']),
        ClickTask(template=None, positives=['templates/c_dweed.bmp', 'templates/use_bank_chest.bmp'],
                  negatives=['templates/bank.bmp', 'templates/g_dweed.bmp'],
                  threshold=3, coords=(-1, -1)),
        HotKeyTask('2', n_presses=1, positives=['templates/bank.bmp']),
        HotKeyTask('2', n_presses=1, positives=['templates/g_dweed.bmp'], negatives=['templates/cancel.bmp']),
        HotKeyTask('space', n_presses=1, positives=['templates/clean_button.bmp']),
        HoverLoc(x=965, y=460, negatives=['templates/g_dweed.bmp'],
                 positives=['templates/c_dweed.bmp'],threshold=60),
    ]

    # tasks = [
    #     # RngMouseMove(),
    #     # StopTask(positives=['templates/smelting_oom.bmp']),
    #     # WaitTask(threshold=0, positives=['templates/g_dweed.bmp', 'templates/cancel.bmp']),
    #     ClickTask(template=None, positives=['templates/c_lanta.bmp', 'templates/use_bank_chest.bmp'],
    #               negatives=['templates/bank.bmp', 'templates/g_lanta.bmp'],
    #               threshold=10, coords=(-1, -1)),
    #     HotKeyTask('2', n_presses=1, positives=['templates/bank.bmp']),
    #     HotKeyTask('2', n_presses=1, positives=['templates/g_lanta.bmp'], negatives=['templates/cancel.bmp', 'templates/bank.bmp']),
    #     HotKeyTask('space', n_presses=1, positives=['templates/clean_button.bmp']),
    #     HoverLoc(x=965, y=460, negatives=['templates/g_lanta.bmp'],
    #              positives=['templates/c_lanta.bmp'],threshold=60),
    # ]


    # tasks = [
    #     StopTask(positives=['templates/smelting_oom.bmp']),
    #     ClickTask('templates/use_bank_chest.bmp',
    #               positives=['templates/magic_logs.bmp'],
    #                coords=(-1, -1)),
    #     # ClickTask('templates/banker.bmp',
    #     #           negatives=['templates/bowstring.bmp'],
    #     #           coords=(-1, -1)),
    #     HotKeyTask('2', n_presses=1, positives=['templates/bank.bmp', ]),
    #     HotKeyTask('3', n_presses=1, positives=[], negatives=['templates/cancel.bmp','templates/magic_logs.bmp', ]),
    #     HotKeyTask('space', positives=['templates/make_button.bmp', ]),
    #
    #     HoverLoc(x=965, y=460, positives=['templates/magic_logs.bmp'], threshold=60),
    #     # HoverTask( [(0, 11, 238), (178, 14, 226), (0, 0, 255), (5, 15, 206), (13, 155, 143)],
    #     #           threshold=10, negatives=['templates/bowstring.bmp', 'templates/banker.bmp' ])
    # ]

    base.Bot(tasks, cycle_delay=0, minutes=2400).main()
