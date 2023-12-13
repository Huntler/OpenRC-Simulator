from typing import Tuple
import pygame as py
from OpenRCSimulator.gui.sub_controller.garage_controller import GarageController
from OpenRCSimulator.state import get_data_folder
from OpenRCSimulator.graphics.controller import BaseController
from OpenRCSimulator.graphics.objects.rectangle import Rectangle
from OpenRCSimulator.graphics.objects.text import ANCHOR_TOP_LEFT, Text
from OpenRCSimulator.graphics.sub_controller import BaseSubController
from OpenRCSimulator.gui import BACKGROUND_COLOR, GARAGE, SHORTCUT_TEXT_COLOR
from OpenRCSimulator.gui.sub_controller.storage_controller import StorageController
from OpenRCSimulator.gui.window import SHORTCUTS_UNTOGGLE, MainWindow


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
        self._window.on_callback(SHORTCUTS_UNTOGGLE, self._untoggle_all_sub_controller)
        self._surface = self._window.get_surface()
        self._title_font = self._window.get_font().copy(size=120)
        self._shortcuts_font = self._window.get_font().copy(size=50)

        # create the sprites we want to use
        # background object (just a colored box)
        background = Rectangle(self._surface, 0, 0, self._width, self._height, BACKGROUND_COLOR)
        self._window.add_sprite("background", background, zindex=99)

        # create sub controllers
        self._active_sub_controller = None

        # create the storage controller
        self._storage = StorageController(self._window, GARAGE)
        self._storage.on_toggle(self._save)

        # create garage controller
        self._garage = GarageController(self._window)
        self._garage.on_toggle(self._sub_controller_toggled)

        # show shortcut info
        text_shortcuts = Text(self._surface, "Shortcuts", 0, 0, SHORTCUT_TEXT_COLOR, self._shortcuts_font)
        text_shortcuts.set_position((20, self._height - 110), ANCHOR_TOP_LEFT)
        self._window.add_sprite("text_shortcuts_title", text_shortcuts)
    
    def _sub_controller_toggled(self, sub_controller: BaseSubController) -> None:
        """This method executes if a subcontroller was toggled. In this case, this method 
        disables all other subcontrollers.
        """
        # if the active sub controller was toggled again, then just unregister it
        if self._active_sub_controller == sub_controller:
            self._active_sub_controller = None
            self._storage.changes(True)
            return

        # if there was an active sub controller, then toggle it again
        if self._active_sub_controller:
            self._active_sub_controller.toggle(call=False)
            self._active_sub_controller = None
        
        if sub_controller.is_toggled():
            self._active_sub_controller = sub_controller
    
    def _untoggle_all_sub_controller(self) -> None:
        """This method untoggles all controller.
        """
        if self._active_sub_controller:
            self._active_sub_controller.toggle(call=False)
            self._active_sub_controller = None
            self._storage.changes(True)
    
    def _save(self) -> None:
        """Save the current configuration.
        """
        self._storage.save("car_config", {GARAGE: self._garage})

    def load(self) -> None:        
        """Load the current configuration to be edited.
        """
        self._storage.load(get_data_folder(""), "car_config", [self._garage])

    def loop(self) -> None:
        pass
