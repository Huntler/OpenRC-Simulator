"""This module logs to the LogService."""
from threading import Thread
from multiprocessing import Lock
import socket
import time


MUTEX = Lock()


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
        self._send_queue = []

    def run(self) -> None:
        # try to connect to the server
        try:
            self._service.connect(("", 9975))
        except ConnectionRefusedError as e:
            print("Unable to connect to LogService: " + e.strerror)

        self._running = True
        while self._running:
            # check if something to log is in the queue
            if len(self._send_queue) > 0:
                self._service.send(self._send_queue[0].encode())

                # entry was send, remove from queue
                self._send_queue.pop(0)
            time.sleep(0.3)

    def add_log(self, text: str) -> None:
        """Adds a log entry to the queue, which will be logged async.

        Args:
            text (str): Text to log.
        """
        with MUTEX:
            self._send_queue.append(text)
