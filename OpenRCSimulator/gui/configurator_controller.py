from typing import Tuple
import pygame as py
from OpenRCSimulator.gui.sub_controller.garage_controller import GarageController
from OpenRCSimulator.gui.sub_controller.shortcut_controller import ShortcutController
from OpenRCSimulator.state import get_data_folder
from OpenRCSimulator.graphics.controller import BaseController
from OpenRCSimulator.graphics.objects.rectangle import Rectangle
from OpenRCSimulator.graphics.objects.text import ANCHOR_TOP_LEFT, Text
from OpenRCSimulator.graphics.sub_controller import BaseSubController
from OpenRCSimulator.gui import BACKGROUND_COLOR, GARAGE, SHORTCUT_TEXT_COLOR
from OpenRCSimulator.gui.sub_controller.storage_controller import StorageController
from OpenRCSimulator.gui.window import MOUSE_CLICK, SENSORS_ACTIVATED, SHORTCUTS_UNTOGGLE, STORAGE_SAVE, MainWindow


class ConfiguratorController(BaseController):
    def __init__(self, window_size: Tuple[int, int], flags: int = 0) -> None:
        """The ConfiguratorController manages the SimulationWindow. This is a separate
        thread than the pygame one.

        Args:
            window_size (Tuple[int, int]): Width and height of the window.
            flags (int, optional): Fullscreen, hardware acceleration, ... Defaults to 0.
        """
        super().__init__()
        self._t = py.time.get_ticks()
        self._file_name = None

        self._width, self._height = window_size
        self._center = (self._width // 2, self._height // 2)
        self._flags = flags

        # create the window visuals
        self._window = MainWindow(window_size=window_size, flags=flags)
        self._surface = self._window.get_surface()
        self._title_font = self._window.get_font().copy(size=120)
        self._shortcuts_font = self._window.get_font().copy(size=50)

        # create the sprites we want to use
        # background object (just a colored box)
        background = Rectangle(self._surface, 0, 0, self._width, self._height, BACKGROUND_COLOR)
        self._window.add_sprite("background", background, zindex=99)

        # show shortcut info
        self._shortcuts = ShortcutController(self._window)
        self._shortcuts.add_shortcut(STORAGE_SAVE, self._save, "'S' Save configuration", py.K_s)
    
    def _save(self) -> None:
        """Save the current configuration.
        """
        print("Save works")

    def load(self) -> None:        
        """Load the current configuration to be edited.
        """
        pass

    def loop(self) -> None:
        pass
