"""This module handles the log service."""
from threading import Thread
import socket


class LogService(Thread):
    """The LogService opens a connection, others can connect and log to.

    Args:
        Thread (Thread): Super class makes this service a thread.
    """
    def __init__(self, receive_callback) -> None:
        """Initializes the socket and thread.

        Args:
            receive_callback (Callable): Executes when a clients has send a log.
        """
        super().__init__(group=None, target=None, name="LogService")

        self._running = False
        self._consumer = None
        self._callback = receive_callback

        # set up the service
        socket.setdefaulttimeout(3)
        self._service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._service.bind((socket.gethostname(), 9975))
        self._service.listen(1)

    def is_alive(self) -> bool:
        """
        This method checks if the service thread is still alive.
        """
        return self._running

    def run(self) -> None:
        """
        This is the main loop which is started by the thread parent class.
        """
        self._running = True
        while self._running:
            if not self._consumer:
                result = self._service.accept()
                if result:
                    self._consumer = result[0]
            else:
                # wait for the consumer to send something to log
                text = self._consumer.recv(1024).decode()
                self._callback(text)

        print("Service has stopped.")

    def stop(self) -> None:
        """
        This method gently stops the thread by ending its loop.
        """
        self._running = False
        if self._consumer:
            self._consumer.close()
