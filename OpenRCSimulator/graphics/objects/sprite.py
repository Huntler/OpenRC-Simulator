"""This module is a base for other sprites used within this project."""
from typing import Tuple
import pygame as py


class Sprite:
    """The base class for other elements.
    """
    def __init__(self, surface: py.Surface) -> None:
        """Initializes a sprite with basic arguments.

        Args:
            surface (py.Surface): The surface a sprite is displayed on.
        """
        self._surface = surface
        self._active = False
        self._button_down = False
        self._size = None

    def set_position(self, pos: Tuple[int, int]) -> None:
        """Sets the sprite's position

        Args:
            pos (Tuple[int, int]): x and y position.

        Raises:
            NotImplemented: This is a template for child classes.
        """
        raise NotImplemented

    def get_position(self) -> Tuple[int, int]:
        """Returns the sprite's position

        Returns:
            Tuple[int, int]: x and y position.

        Raises:
            NotImplemented: This is a template for child classes.
        """
        raise NotImplemented

    def get_size(self) -> Tuple[int, int]:
        """Returns the sprite's size

        Args:
            Tuple[int, int]: Width and height.
        """
        return self._size

    def draw(self) -> None:
        """Draws this sprite and handles mouse inputs. 0 draw calls needed.
        """
        mouse_pos = py.mouse.get_pos()
        mouse_buttons = py.mouse.get_pressed()

        if self.collidepoint(mouse_pos):
            if mouse_buttons[0]:
                self._button_down = True

            if self._button_down and not mouse_buttons[0]:
                self._clicked()
                self._button_down = False

        elif self._button_down:
            self._button_down = False

    def active(self, val: bool) -> None:
        """
        Only active sprites can call the hover and click event.
        """
        self._active = val

    def callback(self, event_type, func) -> None:
        """Execute a function matching to a registered event.

        Args:
            Any: Event type.
            Any: Callback function.

        Raises:
            NotImplemented: This is a template for child classes.
        """
        raise NotImplemented

    def collidepoint(self, point: Tuple[int, int]) -> bool:
        """Checks collision of the sprite with an intersection point.

        Args:
            point (Tuple[int, int]): The point to check for a collision 

        Raises:
            NotImplemented: This is a template for child classes.

        Returns:
            bool: True if collision is detected.
        """
        raise NotImplemented

    def _clicked(self) -> None:
        """Internal callable when a user clicked on the sprite.

        Raises:
            NotImplemented: This is a template for child classes
        """
        raise NotImplemented
