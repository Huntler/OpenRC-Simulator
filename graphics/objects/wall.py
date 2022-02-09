from typing import Tuple

import pygame as py
from pygame import Surface
from graphics.objects.sprite import Sprite


class Wall(Sprite):
    def __init__(self, surface: Surface, start_pos: Tuple[int, int], end_pos: Tuple[int, int], c: Tuple[int, int ,int], thickness: int = 5) -> None:
        super().__init__()

        self._surface = surface
        self._sx, self._sy = start_pos
        self._ex, self._ey = end_pos
        self._t = thickness
        self._c = c
    
    def set_start(self, pos: Tuple[int, int]) -> None:
        self._sx, self._sy = pos
    
    def get_start(self) -> Tuple[int, int]:
        return (self._sx, self._sy)

    def set_end(self, pos: Tuple[int, int]) -> None:
        self._ex, self._ey = pos

    def get_end(self) -> Tuple[int, int]:
        return (self._ex, self._ey)

    def set_color(self, c: Tuple[int, int, int]) -> None:
        self._c = c

    def draw(self) -> None:
        super().draw()

        py.draw.line(self._surface, self._c, (self._sx, self._sy), (self._ex, self._ey), self._t)
        py.draw.circle(self._surface, self._c, (self._sx, self._sy), self._t // 2)
        py.draw.circle(self._surface, self._c, (self._ex, self._ey), self._t // 2)
    
    def collidepoint(self, point: Tuple[int, int]) -> bool:
        pass