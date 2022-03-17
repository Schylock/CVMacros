from cvbot import base
from cvbot.tasks.rng_tasks import RngMouseMove
from cvbot.template_task import ClickTask, HotKeyTask, StopTask, WaitTask, SequenceTask, HoverTask, HoverLoc

if __name__ == '__main__':
    item_one = 'templates/swamp_tar.bmp'
    item_two = 'templates/c_harra.bmp'
    bank = 'templates/use_bank_chest.bmp'

    bank_coords = [965, 490,]
    preset_key = '2'

    tasks = [
        HotKeyTask(preset_key, positives=['templates/bank.bmp']),
        HotKeyTask('space', positives=['templates/mix.bmp', ]),
        SequenceTask(
            [        ClickTask(bank, negatives=[item_two],
                  threshold=10, coords=(-1, -1)),
                ClickTask(item_two),
            ClickTask(item_one),],
            negatives=['templates/cancel.bmp', 'templates/mix.bmp', 'templates/bank.bmp'],
            threshold=0
        ),
        HoverLoc(bank_coords[0], bank_coords[1], negatives=[bank, item_two], ),
        # RngMouseMove(mst=6000, gst=12000),

    ]

    # tasks = [
    #     # RngMouseMove(),
    #     StopTask(positives=['templates/smelting_oom.bmp']),
    #     WaitTask(threshold=0, positives=['templates/cancel.bmp']),
    #     ClickTask(template='templates/banker.bmp', positives=['templates/c_torstol.bmp'],
    #               negatives=['templates/bank.bmp', ],
    #               threshold=2.5, coords=(-1, -1)),
    #     HotKeyTask('2', n_presses=1, positives=['templates/bank.bmp']),
    #     HotKeyTask('2', n_presses=1, positives=['templates/g_torstol.bmp']),
    #     HotKeyTask('space', n_presses=1, positives=['templates/clean_button.bmp']),
    #
    # ]

    base.Bot(tasks, cycle_delay=0, minutes=2400).main()
