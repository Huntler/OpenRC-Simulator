"""This module handles the logger window of the app"""
from typing import Tuple
from OpenRCSimulator.graphics.objects.rectangle import Rectangle
from OpenRCSimulator.graphics.objects.text import Text
from OpenRCSimulator.graphics.window import BaseWindow
from OpenRCSimulator.gui import BACKGROUND_COLOR


class LogWindow(BaseWindow):
    """The logger window of the app wraps the BaseWindow allowing for modifications.

    Args:
        BaseWindow (BaseWindow): The base window class.
    """

    def __init__(self, window_size: Tuple[int, int]) -> None:
        super().__init__(window_size, None, "Log", 30, 0)

        # create the background
        background = Rectangle(self.get_surface(), 0, 0,
                               self._width, self._height, BACKGROUND_COLOR)

        self.add_sprite("background", background, zindex=99)

        self._content_margin = (10, 60, 10, 80)
        self._max_log_entries = 20

    def add_text(self, text: str, i: int) -> None:
        """Adds a text to the log window.

        Args:
            text (str): The text to add.
            i (int): The position to add the text to.
        """
        t = Text(self.get_surface(), text, 0, 0,
                 (255, 255, 255), self.get_font())
        t.set_position((self._content_margin[0],
                        self._content_margin[1] + i * t.get_size()[1]),
                       Text.ANCHOR_TOP_LEFT)

        self._max_log_entries = (
            self._height - self._content_margin[0] - self._content_margin[3]) // t.get_size()[1]
        self.add_sprite(f"log_{i}", t)

    def scroll_log(self, n: int) -> None:
        """Shifts the text, occurs when a new text is added.

        Args:
            n (int): Number of texts.
        """
        i = max(0, n - self._max_log_entries)
        self.remove_sprite(f"log_{i-1}")
        for j in range(i, n):
            log: Text = self.get_sprite(f"log_{j}")
            log.set_position((self._content_margin[0],
                              self._content_margin[1] + (j + 1) * log.get_size()[1]),
                             Text.ANCHOR_TOP_LEFT)

    def draw(self) -> None:
        pass
