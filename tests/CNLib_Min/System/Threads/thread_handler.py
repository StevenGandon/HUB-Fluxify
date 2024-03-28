from typing import Callable
from threading import Thread
from time import time
from time import sleep
from signal import signal, SIGINT
import sys

class ThreadHandler(object):
    def __init__(self, callback: Callable, args: tuple = (), kwargs: dict = None, is_daemon: bool =  None, name: str = None) -> None:
        self.thread: Thread = Thread(None, self.callback_wrapper, name, args, kwargs, daemon=is_daemon)
        self.is_running: bool = False
        self.pid = None

        self.callback = callback

        self.is_daemon = is_daemon

        self.args = args
        self.kwargs = kwargs

        self.name = name

        self.do_stop = False

    def event_stop(self):
        return (self.do_stop)

    def run(self):
        self.is_running: bool = True
        self.thread.start()

    def callback_wrapper(self, *args, **kwargs):
        self.callback(self, *args, **kwargs)
        self.is_running: bool = False

    def wait(self, timeout: int = -1):
        start: int = time()

        while (self.is_running):
            if (timeout == -1):
                continue

            if (time() - start >= timeout):
                break

    def close(self, force: bool = False, max_wait: int = 5):
        if (not self.is_running):
            try:
                self.thread.join()
            except RuntimeError:
                pass
            return

        self.wait(max_wait)

        if (force and self.is_running):
            self.do_stop = True

        self.thread.join()

class ThreadPool(object):
    def __init__(self) -> None:
        self.threads = []

        signal(SIGINT, self.handle_signals)

    def handle_signals(self, *args):
        self.close()

        raise KeyboardInterrupt()

    def add_thread(self, callback: Callable, args: tuple = (), kwargs: dict = None, is_daemon: bool = None, name: str = None):
        self.threads.append(ThreadHandler(callback, args, kwargs, is_daemon, name))

    def debug_threads(self, end_at: int = 10):
        size_y = len(self.threads)
        start = time()
        forced = False
        
        while (not self.is_ended()):
            delta = (time() - start)

            if (delta >= end_at):
                self.close()
                forced = True

            sys.stdout.write(f"elapsed: {round(delta, 2)}s     \n")

            for i, item in enumerate(self.threads):
                if (item.is_running):
                    sys.stdout.write(f"{str(item.name)} (T{i}): running{'.' * ((int(delta * 10.0) % 3) + 1)}      \n")
                else:
                    sys.stdout.write(f"{str(item.name)} (T{i}): dead         \n")

            sys.stdout.write(f"\033[{size_y + 1}A\r")

        if (not forced):
            self.close()

        sys.stdout.write("\n" * (size_y + 1))

    def is_ended(self):
        return (all(map(lambda x: not x.is_running, self.threads)))

    def run(self, with_debug: bool = False):
        for item in self.threads:
            item.run()

        if (with_debug):
            self.debug_threads()

    def wait(self, timeout = -1):
        for item in self.threads:
            item.wait(timeout)

    def close(self):
        for item in self.threads:
            item.close(True, 1)

# def test(self: ThreadHandler):
#     while (not self.event_stop()):
#         continue

# def count(self: ThreadHandler):
#     test = 0
#     for i in range(5000000):
#         if (self.event_stop()):
#             break
#         test += i * i 

# def ez(self: ThreadHandler):
#     test = 0

# T = ThreadPool()
# T.add_thread(test, name="test1")
# T.add_thread(test, name="test2")
# T.add_thread(count, name="count")
# T.add_thread(ez, name="fast")
# T.run(True)
# T.close()
# exit()