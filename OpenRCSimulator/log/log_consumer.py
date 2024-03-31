"""This module logs to the LogService."""
import queue
from threading import Thread
from multiprocessing import Lock
import socket
import time


class LogConsumer(Thread):
    """The LogConsumer logs to the LogService.

    Args:
        Thread (Thread): Runs in background.
    """
    def __init__(self) -> None:
        super().__init__(group=None, target=None, name="LogConsumer")
        self._running = False
        self._connected = False

        # connect to the server on local computer
        self._service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._send_queue = queue.SimpleQueue()

    def run(self) -> None:
        # try to connect to the server
        try:
            self._service.connect(("", 9975))
        except ConnectionRefusedError as e:
            print("Unable to connect to LogService: " + e.strerror)

        self._running = True
        while self._running:
            # check if something to log is in the queue
            text = self._send_queue.get()
            self._service.send(text.encode())

    def add_log(self, text: str) -> None:
        """Adds a log entry to the queue, which will be logged async.

        Args:
            text (str): Text to log.
        """
        self._send_queue.put_nowait(text)

    def stop(self) -> None:
        """Gently stops the LogConsumer thread.
        """
        self._running = False
