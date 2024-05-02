import asyncio
import itertools
import sys
import threading
import time
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
        asyncio.new_event_loop()

        self.start()

    def __target(self, *args, **kwargs):
        result = None
        error = None

        log.debug(f"Task running: {self.task_func}.")
        try:
            result = self.task_func(*args, **kwargs)
        except Exception as exception:
            log.error(
                f"Error while running Task: {self.task_func}\nException: {exception}"
            )

            error = exception
            _ex_type, _ex_value, trace = sys.exc_info()
            traceback.print_tb(trace)

        self.source_id = GLib.idle_add(self.callback, result, error)

        return self.source_id

    def silly(self, callback, *args, **kwargs):
        loop = asyncio.new_event_loop()
        try:
            results = loop.run_until_complete(self.__async_callback(callback))
            return results
        finally:
            loop.close()

    async def __async_callback(self, callback):
        """
        This will run the callback function asynchronously
        """
        retry_count = itertools.count()
        while True:
            try:
                loop = asyncio.get_running_loop()

                if loop.is_running():
                    async with asyncio.TaskGroup() as tg:
                        task = tg.create_task(callback)

                    self.__for_justice = task.result()
            except RuntimeError as e:
                if next(retry_count) >= 5:
                    time.sleep(30)
                    continue
                else:
                    print("failed on max retries.")
                    raise e
            except Exception as e:
                print("unrecoverable error")
                raise e
            break
