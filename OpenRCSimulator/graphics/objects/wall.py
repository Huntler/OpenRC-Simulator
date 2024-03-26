"""This module defines the displayed wall."""
from typing import Tuple

import pygame as py
from pygame import Surface
from OpenRCSimulator.graphics.objects.sprite import Sprite


class Wall(Sprite):
    """The wall, the user can place on a map or which can be loaded from a map-file.

    Args:
        Sprite (Sprite): The sprite super-class handles most interactions.
    """
    def __init__(self, surface: Surface, start_pos: Tuple[int, int], end_pos: Tuple[int, int], c: Tuple[int, int, int], thickness: int = 5) -> None:
        """Creates the wall object, which is defined by start, end coordinates, as well as color and thickness.

        Args:
            surface (Surface): The surface, the wall is displayed on.
            start_pos (Tuple[int, int]): The start position given as pixels (x, y).
            end_pos (Tuple[int, int]): The end position given as pixels (x, y).
            c (Tuple[int, int, int]): The color in (r, g, b) in 8-bit format.
            thickness (int, optional): The lines thickness in pixel format. Defaults to 5.
        """
        super().__init__(surface)

        self._sx, self._sy = start_pos
        self._ex, self._ey = end_pos
        self._t = thickness
        self._c = c

    def get_size(self) -> Tuple[int, int]:
        """Returns the a rectangle reflecting the space, the wall covers.

        Returns:
            Tuple[int, int]: Width, height
        """
        return (max(self._sx, self._ex) - min(self._sx, self._ex),
                max(self._sy, self._ey) - min(self._sy, self._ey))

    def set_start(self, pos: Tuple[int, int]) -> None:
        """Changes the start position of this wall.

        Args:
            pos (Tuple[int, int]): The start position in pixel-coordinates.
        """
        self._sx, self._sy = pos

    def get_start(self) -> Tuple[int, int]:
        """Returns the wall's start position.

        Returns:
            Tuple[int, int]: Returns the wall's start position.
        """
        return self._sx, self._sy

    def set_end(self, pos: Tuple[int, int]) -> None:
        """Sets the wall's end position.

        Args:
            pos (Tuple[int, int]): x and y pixel coordinate.
        """
        self._ex, self._ey = pos

    def get_end(self) -> Tuple[int, int]:
        """Returns the wall's end position.

        Returns:
            Tuple[int, int]: x and y pixel coordinate.
        """
        return self._ex, self._ey

    def set_color(self, c: Tuple[int, int, int]) -> None:
        """Set the wall's color.

        Args:
            c (Tuple[int, int, int]): Color given in RGB.
        """
        self._c = c

    def draw(self) -> None:
        """Draw the line, uses 3 calls.
        """
        super().draw()

        py.draw.line(self._surface, self._c, (self._sx, self._sy),
                     (self._ex, self._ey), self._t)
        py.draw.circle(self._surface, self._c,
                       (self._sx, self._sy), self._t // 2)
        py.draw.circle(self._surface, self._c,
                       (self._ex, self._ey), self._t // 2)

    def collidepoint(self, point: Tuple[int, int]) -> bool:
        """Returns True if the wall collides with a given coordinate.

        Args:
            point (Tuple[int, int]): The point of collision to test.

        Returns:
            bool: True if collision is detected.
        """
        pass
