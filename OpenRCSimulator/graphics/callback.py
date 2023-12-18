"""This module create all event listeners throughout this project."""
from typing import Tuple

from OpenRCSimulator.graphics.objects.text_field import TextField


class BaseListener:
    """The base listener groups all event listeners.
    """
    def __init__(self) -> None:
        pass


class MouseListener(BaseListener):
    """The MouseListener reacts on movement or on clicks.

    Args:
        BaseListener (BaseListener): Base class.
    """
    def on_movement(self, position: Tuple[int, int], delta: Tuple[int, int]) -> None:
        """Mouse movement event.

        Args:
            position (Tuple[int, int]): Current mouse position.
            delta (Tuple[int, int]): Delta to previous position.
        """
        raise NotImplementedError

    def on_click(self, buttons: Tuple[bool, bool, bool], position: Tuple[int, int]) -> None:
        """Mouse click event.

        Args:
            buttons (Tuple[bool, bool, bool]): Buttons pressed (left, middle, right)
            position (Tuple[int, int]): Mouse position on click occurence.
        """
        raise NotImplementedError


class TextListener(BaseListener):
    """The TextListener reacts text inputs, such as text change or text input
    event ended.

    Args:
        BaseListener (BaseListener): Base class.
    """
    def on_text_changed(self, ui_element: TextField, text: str) -> None:
        """Text changed event.

        Args:
            ui_element (TextField): Active text input element.
            text (str): The typed text.
        """
        raise NotImplementedError

    def on_text_end(self, ui_element: TextField) -> None:
        """Text input has ended

        Args:
            ui_element (TextField): The active text input element.
        """
        raise NotImplementedError


class KeyListener(BaseListener):
    """The KeyListener reacts on key presses.

    Args:
        BaseListener (BaseListener): Base class.
    """
    def on_key_pressed(self, key: int) -> None:
        """Key pressed event.

        Args:
            key (int): The key pressed, compare to py.K_*.
        """
        raise NotImplementedError


class WindowListener(BaseListener):
    """The WindowListener reacts on window events such as close..

    Args:
        BaseListener (BaseListener): Base class.
    """
    def on_quit(self) -> None:
        """Window quit event.
        """
        raise NotImplementedError
