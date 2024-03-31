"""This module shows stats on a separate window."""
import time
from typing import Tuple
from datetime import datetime

from OpenRCSimulator.graphics.controller import BaseController
from OpenRCSimulator.log.log_service import LogService
from OpenRCSimulator.log.log_window import LogWindow


class LogController(BaseController):
    """The LogController logs the application's data.

    Args:
        BaseController (BaseController): Super class.
    """

    def __init__(self, window_size: Tuple[int, int]) -> None:
        super().__init__(disable_logging=True)

        # set up the service
        self._log = 0
        self._service = LogService(self.add_log)

        # set up the window
        self._width, self._height = window_size
        self._window = LogWindow(window_size=window_size)

        # set up the log
        self.add_log("Started logger.")

    def add_log(self, text: str) -> None:
        """Adds a log entry to the log window. This method implicitly adds a time stamp prefix.

        Args:
            text (str): The text to log.
        """
        # make some space for the new log entry
        self._window.scroll_log(self._log)

        # create the log entry
        log_time = datetime.now()
        seconds = log_time.second if log_time.second > 9 else "0" + str(log_time.second)
        prefix = f"{log_time.hour}:{log_time.minute}:{seconds} - "
        self._window.add_text(prefix + text, self._log)
        self._log += 1

    def loop(self) -> None:
        self._service.receive()

    def stop(self) -> None:
        self.add_log("Stopping LogService.")
        self._service.stop()
        self._running = False
        print("LogService has stopped.")
