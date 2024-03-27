"""This module displays a rectangle sprite on a surface."""
from typing import Tuple
from OpenRCSimulator.graphics.objects.sprite import Sprite
import pygame as py


class Rectangle(Sprite):
    """A basic rectangle based on the sprite super class.

    Args:
        Sprite (Sprite): The super class.
    """
    def __init__(self, surface: py.Surface, x: int, y: int, w: int, h: int, c: Tuple[int, int, int]) -> None:
        """Initialization of the rectangle.

        Args:
            surface (py.Surface): The surface to be displayed on.
            x (int): Horizontal position.
            y (int): Vertical position.
            w (int): Width.
            h (int): Height.
            c (Tuple[int, int, int]): Colors in RGB.
        """
        super().__init__(surface)

        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._c = c

        self._clicked_c = c
        self._activated = False

    def get_size(self) -> Tuple[int, int]:
        """Returns the size of the rectangle.

        Returns:
            Tuple[int, int]: Width, height.
        """
        return (self._w, self._h)

    def set_position(self, pos: Tuple[int, int]) -> None:
        """Sets the rectangle's position.

        Args:
            pos (Tuple[int, int]): X and y pixel coordinate.
        """
        self._x, self._y = pos

    def get_position(self) -> Tuple[int, int]:
        """Returns the rectangle's position.

        Returns:
            Tuple[int, int]: X and y position.
        """
        return (self._x, self._y)

    def draw(self) -> None:
        """Draws the rectangle, 1 call needed.
        """
        super().draw()

        c = self._c if not self._activated else self._clicked_c
        py.draw.rect(self._surface, c, rect=(self._x, self._y, 
                                             self._w, self._h))

    def collidepoint(self, point: Tuple[int, int]) -> bool:
        """Calculates the collision of a point with this rectangle.

        Args:
            point (Tuple[int, int]): The point to check for collision.

        Returns:
            bool: True if collision is detected.
        """
        x, y = point
        if self._x < x and self._x + self._w > x:
            if self._y < y and self._y + self._h > y:
                return True
        return False

    def set_clicked_color(self, c: Tuple[int, int, int]) -> None:
        """Sets changed color when clicked.

        Args:
            c (Tuple[int, int, int]): The clicked color in RGB.
        """
        self._clicked_c = c

    def _clicked(self) -> None:
        """Sets the rectangle to clicked state or removes this state.
        """
        self._activated = not self._activated
