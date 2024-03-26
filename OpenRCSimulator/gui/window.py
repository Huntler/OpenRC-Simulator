"""This module handles the main window of the app"""
from OpenRCSimulator.graphics.window import BaseWindow


class MainWindow(BaseWindow):
    """The main window of the app wraps the BaseWindow allowing for modifications.

    Args:
        BaseWindow (BaseWindow): The base window class.
    """

    def draw(self) -> None:
        pass
