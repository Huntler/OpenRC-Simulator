"""This module defines displayed text on screen."""
from typing import Tuple

import pygame as py
from OpenRCSimulator.graphics.font import FontWrapper
from OpenRCSimulator.graphics.objects.sprite import Sprite


class Text(Sprite):
    """The text shown on screen can be modified based on arguments such as position, size, color, 
    font, content."""

    ANCHOR_TOP_LEFT = 0
    ANCHOR_CENTER = 1

    def __init__(self, surface: py.Surface, text: str, x: int, y: int, c: Tuple[int, int, int], 
                 font: FontWrapper) -> None:
        """Initialization of a Text sprite.

        Args:
            surface (py.Surface): The surface, the text is displayed on.
            text (str): The content of the sprite.
            x (int): Pixel horizontal position.
            y (int): Pixel vertical position.
            c (Tuple[int, int, int]): Color in RGB.
            font (FontWrapper): The font of the text.
        """
        super().__init__(surface)

        self._text = text
        self._c = c
        self._antialiasing = True

        self._font = font.unpack()
        self._text_surface = self._font.render(text, self._antialiasing, c)
        self.set_position((x, y))

    def set_font(self, font: FontWrapper) -> None:
        """Sets the text's font.

        Args:
            font (FontWrapper): The font object.
        """
        self._font = font.unpack()
        self._text_surface = self._font.render(
            self._text, self._antialiasing, self._c)

    def get_size(self) -> Tuple[int, int]:
        """Returns the text's size

        Returns:
            Tuple[int, int]: Width and height of the sprite.
        """
        return self._font.size(self._text)

    def set_color(self, c: Tuple[int, int, int]) -> None:
        """Changes the text color

        Args:
            c (Tuple[int, int, int]): RGB values.
        """
        self._c = c
        self._text_surface = self._font.render(
            self._text, self._antialiasing, self._c)

    def set_text(self, text: str) -> None:
        """Changes the text of this sprite.

        Args:
            text (str): The text.
        """
        self._text = text
        self._text_surface = self._font.render(
            text, self._antialiasing, self._c)
        # TODO: change psoition may be needed

    def get_text(self) -> str:
        """Returns the text.

        Returns:
            str: The text.
        """
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
        """Returns the text's position.

        Returns:
            Tuple[int, int]: The horizontal and vetical pixel position of the sprite.
        """
        return (self._x, self._y)

    def draw(self) -> None:
        """Draws the sprite, uses 1 call.
        """
        super().draw()

        self._surface.blit(self._text_surface, (self._x, self._y))

    def collidepoint(self, point: Tuple[int, int]) -> bool:
        """Returns True if the text collides with a given coordinate.

        Args:
            point (Tuple[int, int]): The point of collision to test.

        Returns:
            bool: True if collision is detected.
        """
        pass
