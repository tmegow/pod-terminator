import os
import re
from threading import Timer

"""
(Borrowed from https://stackoverflow.com/a/13151299/9458555)
Creates Timer threads for the purpose of executing functions every interval of n
https://docs.python.org/3/library/threading.html#timer-objects
"""


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False

        multipliers = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        if re.search("[\D]", interval):
            try:
                unit = interval[-1:]
                self.interval = multipliers[unit] * int(interval[:-1])
            except KeyError:
                print('Unsupported interval "%s"!' % unit)
                os._exit(1)
        else:
            self.interval = int(interval)

        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
