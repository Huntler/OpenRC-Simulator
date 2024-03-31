"""This module handles the log service."""
import socket


class LogService:
    """The LogService opens a connection, others can connect and log to.
    """
    def __init__(self, receive_callback) -> None:
        """Initializes the socket and thread.

        Args:
            receive_callback (Callable): Executes when a clients has send a log.
        """

        self._consumer = None
        self._alive = True
        self._callback = receive_callback

        # set up the service
        # socket.setdefaulttimeout(3)
        self._service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._service.bind(("", 9975))
        self._service.listen(1)
    
    def is_alive(self) -> bool:
        """Returns state of the log service.

        Returns:
            bool: Log service alive?
        """
        return self._alive

    def receive(self) -> None:
        """This function waits for a consumer to connect and then waits
        to receive a message."""
        if not self._consumer:
            result = self._service.accept()
            if result:
                self._consumer = result[0]
        else:
            # wait for the consumer to send something to log
            text = self._consumer.recv(1024).decode()
            if text == "kys":
                self._alive = False
                self.stop()
                return
            
            self._callback(text)

    def stop(self) -> None:
        """
        This method gently stops the thread by ending its loop.
        """
        if self._consumer:
            self._consumer.close()
