import os
from typing import Tuple
import pygame as py
import yaml
from OpenRCSimulator.gui.sub_controller.shortcut_controller import ShortcutController
from OpenRCSimulator.state import get_data_folder
from OpenRCSimulator.graphics.controller import BaseController
from OpenRCSimulator.graphics.objects.rectangle import Rectangle
from OpenRCSimulator.gui import BACKGROUND_COLOR
from OpenRCSimulator.gui.window import STORAGE_SAVE, MainWindow


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

        # create the configuration parameter dict
        self._param = {}

        # create the window visuals
        self._window = MainWindow(window_size=window_size, flags=flags)
        self._surface = self._window.get_surface()
        self._title_font = self._window.get_font().copy(size=120)

        # create the sprites we want to use
        # background object (just a colored box)
        background = Rectangle(self._surface, 0, 0, self._width, self._height, BACKGROUND_COLOR)
        self._window.add_sprite("background", background, zindex=99)

        # TODO: create form

        # show shortcut info
        self._shortcuts = ShortcutController(self._window)
        self._shortcuts.add_shortcut(STORAGE_SAVE, self._save, "'S' Save configuration", py.K_s)
    
    def _save(self) -> None:
        """Save the current configuration.
        """
        with open(f"{get_data_folder('')}/car_config.yaml", "w") as file:
            documents = yaml.dump(self._param, file)

    def load(self) -> None:        
        """Load the current configuration to be edited.
        """
        path = f"{get_data_folder('')}car_config.yaml"
        if not os.path.exists(path):
            return
        
        with open(path, "r") as file:
            self._param = yaml.load(file, Loader=yaml.FullLoader)
        
        # TODO: self._param -> form

    def loop(self) -> None:
        pass
