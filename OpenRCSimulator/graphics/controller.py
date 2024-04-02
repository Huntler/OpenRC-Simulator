"""This module defines the base controller. """
from multiprocessing.spawn import freeze_support
from threading import Thread
from threading import Lock
import sys

from OpenRCSimulator.graphics.callback import WindowListener
from OpenRCSimulator.log.log_consumer import LogConsumer


MUTEX = Lock()


class DummyListener(WindowListener):
    """The dummy listener is required to intialize the base controller before the
      MainWindow is defined.

    Args:
        WindowListener (_type_): _description_
    """
    def on_quit(self) -> None:
        sys.exit(0)


class BaseController(Thread):
    """
    This class represents a controller that connects the game logic to the GUI object.
    This runs in a separate thread, so it is next to the GUI one.
    """

    QUIT = "quit_app"

    def __init__(self, disable_logging: bool = False) -> None:
        super(BaseController, self).__init__(
            group=None, target=None, name="ControllerThread")

        self.__running = False
        self._window = None
        self._listener = DummyListener()
        self._listener.on_quit = self.stop

        self._logging = not disable_logging
        if self._logging:
            self._log = LogConsumer()

    def boot(self) -> None:
        """
        This method is important, because with this, the controller and GUI will be started.
        """
        if self._logging:
            self._log.start()

        self.start()
        self._window.set_listener(self._listener)
        self._window.start()

    def is_alive(self) -> bool:
        """
        This method checks if the controller thread is still alive.
        """
        return self.__running

    def run(self) -> None:
        """
        This is the main loop which is started by the thread parent class.
        """
        self.__running = True
        while self.__running:
            self.loop()

        print("Controller has stopped.")

    def loop(self) -> None:
        """
        In here the logic can be implemented. This will be executed in a while 
        thread alive loop.
        """
        raise NotImplementedError

    def stop(self) -> None:
        """
        This method gently stops the thread by ending its loop.
        """
        with MUTEX:
            self.__running = False

        if self._logging:
            self._log.stop()


if __name__ == '__main__':
    freeze_support()
