"""This module controls the graphics of the creator window."""
# pylint: disable=E1101

from typing import Callable, Tuple
import pygame as py
from OpenRCSimulator.graphics.objects.rectangle import Rectangle
from OpenRCSimulator.graphics.objects.text import Text
from OpenRCSimulator.graphics.window import BaseWindow
from OpenRCSimulator.gui import BACKGROUND_COLOR, MODE_TEXT_COLOR
from OpenRCSimulator.gui.sub_controller.shortcut_controller import ShortcutController


CREATOR_PLACE_WALL = "place_wall"
CREATOR_PLACE_CAR = "place_car"
STORAGE_SAVE = "save_map"
SHORTCUTS_UNTOGGLE = "untoggle"


class CreatorWindow(BaseWindow):
    """Visualization of the map creation window. The user is able to place walls, 
    the racing car, and more.

    Args:
        BaseWindow (BaseWindow): Super class.
    """
    def __init__(self, window_size: Tuple[int, int], draw_area: Tuple[int, int] = None) -> None:
        super().__init__(window_size, draw_area, "Map Creator", frame_rate=60, flags=0)

        # background object and window title (shown in background)
        background = Rectangle(self._surface, 0, 0,
                               self._width, self._height, 
                               BACKGROUND_COLOR)
        self.add_sprite("background", background, zindex=99)

        title_font = self.get_font().copy(size=120)
        center_x, center_y = window_size[0] // 2, window_size[1] // 2
        text_mode = Text(self._surface, "CREATOR", center_x,
                         center_y, MODE_TEXT_COLOR, title_font)
        self.add_sprite("text_mode", text_mode, zindex=98)

        # add shortcuts controller
        self._shortcuts = ShortcutController(self)

    def draw(self) -> None:
        pass

    def wall_callback(self, callback: Callable) -> None:
        """Sets the callback when the user starts placing a wall.

        Args:
            callback (Callable): Function to call.
        """
        self._shortcuts.add_shortcut(
            CREATOR_PLACE_WALL, callback, "'P' Start drawing a wall", py.K_p, can_toggle=True)

    def car_callback(self, callback: Callable) -> None:
        """Sets the callback when the user wants to place the car.

        Args:
            callback (Callable): The Function to call.
        """
        self._shortcuts.add_shortcut(CREATOR_PLACE_CAR, callback, "'R' Place the car", py.K_r)

    def save_callback(self, callback: Callable) -> None:
        """Sets the callback when the user wants to save.

        Args:
            callback (Callable): The save-map function.
        """
        self._shortcuts.add_shortcut(STORAGE_SAVE, callback, "'S' Save the map", py.K_s)

    def untoggle_callback(self, callback: Callable) -> None:
        """Sets the callback when all toggle-callbacks should be untoggled again.

        Args:
            callback (Callable): Untoggle all function.
        """
        self._shortcuts.untoggle_all()
        self._shortcuts.add_shortcut(SHORTCUTS_UNTOGGLE, callback, "'ESC' Stop input", py.K_ESCAPE)
