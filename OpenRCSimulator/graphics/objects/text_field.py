from typing import Tuple

import pygame as py
from OpenRCSimulator.graphics.font import FontWrapper
from OpenRCSimulator.graphics.objects.text import Text


ANCHOR_TOP_LEFT = 0
ANCHOR_CENTER = 1


class TextField(Text):

    ACTIVATED_COLOR = 2
    COLOR = 1
    TEXT_COLOR = 0

    FILTER_NUMBERS = 0
    FILTER_TEXT = 1
    FILTER_NONE = -1

    def __init__(self, surface: py.Surface, x: int, y: int, text: str = "", fontwrapper: FontWrapper = None) -> None:
        # set default colors
        self._c = (0, 0, 0)
        self._bc = (200, 200, 200)
        self._ac = (255, 255, 255)

        self._active = False
        self._margin = [10, 2, 20, 4]
        self._callback = lambda _: _

        self._filter = -1
        self._box = (0, 0, 0, 0)

        # initilize
        super().__init__(surface, text, x, y, self._c, fontwrapper)
    
    def get_size(self) -> Tuple[int, int]:
        return (self._box[2], self._box[3])
    
    def set_text_filter(self, filter: int = FILTER_NONE) -> None:
        """Filters text from update method.

        Args:
            filter (int, optional): Text to filter. Defaults to FILTER_NONE.
        """
        self._filter = filter

    def on_activated(self, callback) -> None:
        self._callback = callback
    
    def set_color(self, c: Tuple[int, int, int], mode: int = TEXT_COLOR) -> None:
        """Changes the color

        Args:
            c (Tuple[int, int, int]): RGB values.
        """
        if mode == TextField.TEXT_COLOR:
            self._c = c
            self._text_surface = self._font.render(self._text, self._antialiasing, self._c)
        elif mode == TextField.ACTIVATED_COLOR:
            self._ac = c
        elif mode == TextField.COLOR:
            self._bc = c
    
    def set_text(self, text: str) -> None:
        """Changes the text of this sprite.

        Args:
            text (str): The text.
        """
        # set the text
        self._text = text
        self._text_surface = self._font.render(text, self._antialiasing, self._c)

        # calculate new box size
        w = self._text_surface.get_width()
        h = self._text_surface.get_height()
        self._box = (self._x - self._margin[0], self._y - self._margin[1], w + self._margin[2], h + self._margin[3])
    
    def is_activated(self) -> bool:
        return self._active

    def deactivate(self) -> None:
        self._active = False

    def update_text(self, text: str) -> None:
        """Sets text if field is active.

        Args:
            text (str): Text
        """
        if self._active:
            if text == "\n":
                self._active = False
                return
            
            if self._filter == TextField.FILTER_TEXT:
                text = "".join(filter(str.isalpha, text))
            elif self._filter == TextField.FILTER_NUMBERS:
                text = "".join(filter(str.isnumeric, text))

            self.set_text(text)
    
    def set_position(self, pos: Tuple[int, int], anchor: int = ANCHOR_CENTER) -> None:
        """This method sets the position of the text based on its text and anchor point.

        Args:
            pos (Tuple[int, int]): The x and y coordinate of the text object.
            anchor (int, optional): The anchor position. Defaults to ANCHOR_TOP_LEFT.

        Raises:
            RuntimeError: Occurs if the anchor point was defined incorrectly.
        """
        w = self._text_surface.get_width()
        h = self._text_surface.get_height()

        if anchor == ANCHOR_TOP_LEFT:
            self._x, self._y = pos
            self._box = (self._x - self._margin[0], self._y - self._margin[1], w + self._margin[2], h + self._margin[3])
            return

        if anchor == ANCHOR_CENTER:
            _x, _y = pos
            self._x = _x - w // 2
            self._y = _y - h // 2
            self._box = (self._x - self._margin[0], self._y - self._margin[1], w + self._margin[2], h + self._margin[3])
            return
        
        raise RuntimeError("Wrong anchor point provided.")
    
    def draw(self) -> None:
        super().draw()

        # draw the background box
        color = self._ac if self._active else self._bc
        py.draw.rect(self._surface, color, self._box)

        # draw the text
        self._surface.blit(self._text_surface, (self._x, self._y))


    def collidepoint(self, point: Tuple[int, int]) -> bool:
        x, y = point
        min_x, min_y, max_x, max_y = self._box
        max_x, max_y = min_x + max_x, min_y + max_y

        return min_x < x and x < max_x and min_y < y and y < max_y

    def _clicked(self) -> None:
        if self.collidepoint(py.mouse.get_pos()):
            self._active = True
            self._callback()