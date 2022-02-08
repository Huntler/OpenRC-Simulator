from multiprocessing.spawn import freeze_support
from threading import Thread

from graphics.window import BaseWindow


class BaseController(Thread):
    def __init__(self) -> None:
        """
        This class represents a controller that connects the game logic to the GUI object.
        This runs in a separate thread so it is next to the GUI one.
        """
        super(BaseController, self).__init__(group=None, target=None, name="ControllerThread")
        
        self._running = False
        self._window = None
    
    def boot(self) -> None:
        """
        This method is important, because with this, the controller and GUI will be started.
        """
        self.start()

        self._window.on_callback(BaseWindow.QUIT, self.stop)
        self._window.start()
    
    def is_alive(self) -> bool:
        """
        This method checks if the controller thread is still alive.
        """
        return self._running

    def run(self) -> None:
        """
        This is the main loop which is started by the thread parent class.
        """
        self._running = True
        while self._running:
            self.loop()
        
        print("Controller has stopped.")
    
    def loop(self) -> None:
        """
        In here the logic can be implemented. This will be executed in a while 
        thread alive loop.
        """
        pass
    
    def stop(self) -> None:
        """
        This method gently stops the thread by ending its loop.
        """
        self._running = False


if __name__ == '__main__':
    freeze_support()