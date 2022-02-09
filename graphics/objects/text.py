import random
from typing import Tuple

import pygame as py
from graphics.objects.sprite import Sprite


ANCHOR_TOP_LEFT = 0
ANCHOR_CENTER = 1


class Text(Sprite):
    def __init__(self, surface: py.Surface, text: str, x: int, y: int, size: int, c: Tuple[int, int, int]) -> None:
        super().__init__()
        self._surface = surface

        self._text = text
        self._size = size
        
        try:
            self._font = py.font.SysFont("ptsansnarrow", size)
        except:
            self._font = py.font.SysFont(py.font.get_default_font(), size)
            
        self._text_surface = self._font.render(text, False, c)

        self.set_position((x, y))

        self._c = c
    
    def set_text(self, text: str) -> None:
        self._text = text
        self._text_surface = self._font.render(text, False, self._c)

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
        if anchor == ANCHOR_TOP_LEFT:
            self._x, self._y = pos
            return

        if anchor == ANCHOR_CENTER:
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