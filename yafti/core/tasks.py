import os
import sys
import threading
import traceback

from gi.repository import GLib

from yafti import log


class YaftiTasks(threading.Thread):
    """
    Task that will run in the background
    """

    def __init__(self, task_func, callback=None, *args, **kwargs):

        self.source_id = None
        super().__init__(target=self.__target, args=args, kwargs=kwargs)

        self.task_func = task_func

        self.callback = callback if callback else lambda r, e: None
        self.daemon = kwargs.pop("daemon", True)

        self.start()

    def __target(self, *args, **kwargs):
        result = None
        error = None

        log.debug(f"Task running: {self.task_func}.")

        try:
            result = self.task_func(*args, **kwargs)
        except Exception as exception:
            log.error(f"Error while running Task: {self.task_func}\nException: {exception}")

            error = exception
            _ex_type, _ex_value, trace = sys.exc_info()
            traceback.print_tb(trace)

        self.source_id = GLib.idle_add(self.callback, result, error)

        return self.source_id