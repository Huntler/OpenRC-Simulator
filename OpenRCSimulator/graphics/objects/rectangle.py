from typing import Tuple
from OpenRCSimulator.graphics.objects.sprite import Sprite
import pygame as py


class Rectangle(Sprite):
    def __init__(self, surface: py.Surface, x: int, y: int, w: int, h: int, c: Tuple[int, int, int]) -> None:
        super().__init__(surface)

        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._c = c
        self._clicked_c = c
    
    def get_size(self) -> Tuple[int, int]:
        return (self._w, self._h)
    
    def set_position(self, pos: Tuple[int, int]) -> None:
        self._x, self._y = pos
    
    def get_position(self) -> Tuple[int, int]:
        return (self._x, self._y)
    
    def draw(self) -> None:
        py.draw.rect(self._surface, self._c, rect=(self._x, self._y, self._w, self._h))
        super().draw()
    
    def collidepoint(self, point: Tuple[int, int]) -> bool:
        x, y = point
        if self._x < x and self._x + self._w > x:
            if self._y < y and self._y + self._h > y:
                return True
        return False

    def set_clicked_color(self, c: Tuple[int, int, int]) -> None:
        self._clicked_c = c

    def _clicked(self) -> None:
        py.draw.rect(self._surface, self._clicked_c, rect=(self._x, self._y, self._w, self._h))

