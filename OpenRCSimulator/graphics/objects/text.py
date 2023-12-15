from typing import Tuple

import pygame as py
from OpenRCSimulator.graphics.font import FontWrapper
from OpenRCSimulator.graphics.objects.sprite import Sprite


class Text(Sprite):

    ANCHOR_TOP_LEFT = 0
    ANCHOR_CENTER = 1

    def __init__(self, surface: py.Surface, text: str, x: int, y: int, c: Tuple[int, int, int], font: FontWrapper) -> None:
        super().__init__()
        
        self._surface = surface
        self._text = text
        self._c = c
        self._antialiasing = True

        self._font = font.unpack()
        self._text_surface = self._font.render(text, self._antialiasing, c)
        self.set_position((x, y))
    
    def set_font(self, font: FontWrapper) -> None:
        self._font = font.unpack()
        self._text_surface = self._font.render(self._text, self._antialiasing, self._c)

    def get_size(self) -> Tuple[int, int]:
        return self._font.size(self._text)
    
    def set_color(self, c: Tuple[int, int, int]) -> None:
        """Changes the text color

        Args:
            c (Tuple[int, int, int]): RGB values.
        """
        self._c = c
        self._text_surface = self._font.render(self._text, self._antialiasing, self._c)
    
    def set_text(self, text: str) -> None:
        """Changes the text of this sprite.

        Args:
            text (str): The text.
        """
        self._text = text
        self._text_surface = self._font.render(text, self._antialiasing, self._c)
        # TODO: change psoition may be needed

    def get_text(self) -> str:
        return self._text
    
    def set_position(self, pos: Tuple[int, int], anchor: int = ANCHOR_CENTER) -> None:
        """This method sets the position of the text based on its text and anchor point.

        Args:
            pos (Tuple[int, int]): The x and y coordinate of the text object.
            anchor (int, optional): The anchor position. Defaults to ANCHOR_TOP_LEFT.

        Raises:
            RuntimeError: Occurs if the anchor point was defined incorrectly.
        """
        if anchor == Text.ANCHOR_TOP_LEFT:
            self._x, self._y = pos
            return

        if anchor == Text.ANCHOR_CENTER:
            w = self._text_surface.get_width()
            h = self._text_surface.get_height()
            _x, _y = pos
            self._x = _x - w // 2
            self._y = _y - h // 2
            return
        
        raise RuntimeError("Wrong anchor point provided.")
    
    def get_position(self) -> Tuple[int, int]:
        return (self._x, self._y)
    
    def draw(self) -> None:
        super().draw()

        self._surface.blit(self._text_surface, (self._x, self._y))

    def collidepoint(self, point: Tuple[int, int]) -> bool:
        pass