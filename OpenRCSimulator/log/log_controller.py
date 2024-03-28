"""This module shows stats on a separate window."""
import socket
from typing import Tuple
from datetime import datetime

from OpenRCSimulator.graphics.controller import BaseController
from OpenRCSimulator.log.log_window import LogWindow


class LogController(BaseController):
    """The LogController logs the application's data.

    Args:
        BaseController (BaseController): Super class.
    """
    def __init__(self, window_size: Tuple[int, int]) -> None:
        super().__init__()

        # set up the service
        self._service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._service.bind((socket.gethostname(), 9975))

        self._consumer = None

        # set up the window
        self._width, self._height = window_size
        self._window = LogWindow(window_size=window_size)

        # set up the log
        self._log = 0
        self.add_log("Started logger.")
        
        self._service.listen(1)

    def add_log(self, text: str) -> None:
        """Adds a log entry to the log window. This method implicitly adds a time stamp prefix.

        Args:
            text (str): The text to log.
        """
        # make some space for the new log entry
        self._window.scroll_log(self._log)

        # create the log entry
        log_time = datetime.now()
        prefix = f"{log_time.hour}:{log_time.minute}:{log_time.second} - "
        self._window.add_text(prefix + text, self._log)
        self._log += 1

    def loop(self) -> None:
        # let the consumer connect to the logger
        if not self._consumer:
            result = self._service.accept()
            if result:
                self._consumer = result[0]
        else:
            # wait for the consumer to send something to log
            text = self._consumer.recv(1024).decode()
            self.add_log(text)

    def stop(self) -> None:
        super().stop()

        # close the connection to the consumer
        if self._consumer:
            self._consumer.close()
