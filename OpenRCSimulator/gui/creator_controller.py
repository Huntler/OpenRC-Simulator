from typing import Tuple
import pygame as py
import yaml
from OpenRCSimulator.gui.sub_controller.shortcut_controller import ShortcutController
from OpenRCSimulator.state import MAPS_FOLDER, get_data_folder
from OpenRCSimulator.graphics.controller import BaseController
from OpenRCSimulator.graphics.objects.rectangle import Rectangle
from OpenRCSimulator.graphics.objects.text import Text
from OpenRCSimulator.graphics.sub_controller import BaseSubController
from OpenRCSimulator.gui import BACKGROUND_COLOR, CREATOR, MODE_TEXT_COLOR, SHORTCUT_TEXT_COLOR
from OpenRCSimulator.gui.sub_controller.car_controller import CarController
from OpenRCSimulator.gui.sub_controller.wall_controller import WallController
from OpenRCSimulator.gui.window import CREATOR_PLACE_CAR, CREATOR_PLACE_WALL, SHORTCUTS_UNTOGGLE, STORAGE_SAVE, MainWindow


class CreatorController(BaseController):
    def __init__(self, window_size: Tuple[int, int], flags: int = 0) -> None:
        """The CreatorController manages the MainWindow. This is a separate
        thread than the pygame one.

        Args:
            window_size (Tuple[int, int]): Width and height of the window.
            flags (int, optional): Fullscreen, hardware acceleration, ... Defaults to 0.
        """
        super().__init__()
        self._t = py.time.get_ticks()
        self._delta = 0.1
        self._file_name = None

        self._width, self._height = window_size
        self._center = (self._width // 2, self._height // 2)
        self._flags = flags
        self._saved_status = "unsaved"

        # create the window visuals
        self._window = MainWindow(window_size=window_size, flags=flags)
        self._window.set_listener(self)
        self._surface = self._window.get_surface()
        self._title_font = self._window.get_font().copy(size=120)

        # background object (just a colored box)
        background = Rectangle(self._surface, 0, 0, self._width, self._height, BACKGROUND_COLOR)
        self._window.add_sprite("background", background, zindex=99)
        text_mode = Text(self._surface, "CREATOR", self._center[0], self._center[1], MODE_TEXT_COLOR, self._title_font)
        self._window.add_sprite("text_mode", text_mode, zindex=98)
        
        self._font_saved_status = self._window.get_font().copy(size=30)
        self._text_status = Text(self._surface, self._saved_status, 0, 0, SHORTCUT_TEXT_COLOR, self._font_saved_status)
        self._text_status.set_position((self._width // 2, self._height // 2 + 80), Text.ANCHOR_CENTER)
        self._window.add_sprite("text_status", self._text_status, zindex=98)

        # create sub controllers
        self._active_sub_controller = None

        # create the car controller
        self._car = CarController(self._window, CREATOR)
        self._car.on_toggle(self._sub_controller_toggled)

        # create the wall controller
        self._wall = WallController(self._window, CREATOR)
        self._wall.on_toggle(self._sub_controller_toggled)

        # create shortcuts
        self._shortcuts = ShortcutController(self._window)
        self._shortcuts.add_shortcut(CREATOR_PLACE_WALL, self._wall.toggle, "'P' Start drawing a wall", py.K_p, can_toggle=True)
        self._shortcuts.add_shortcut(CREATOR_PLACE_CAR, self._car.toggle, "'R' Place the car", py.K_r)
        self._shortcuts.add_shortcut(STORAGE_SAVE, self._save, "'S' Save the map", py.K_s)
        self._shortcuts.add_shortcut(SHORTCUTS_UNTOGGLE, self._untoggle_all_sub_controller, "'ESC' Stop input", py.K_ESCAPE)
    
    def _sub_controller_toggled(self, sub_controller: BaseSubController) -> None:
        """This method executes if a subcontroller was toggled. In this case, this method 
        disables all other subcontrollers.
        """
        # if the active sub controller was toggled again, then just unregister it
        if self._active_sub_controller == sub_controller:
            self._active_sub_controller = None
            self._changes(True)
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
            self._changes(True)
            self._shortcuts.untoggle_all()
    
    def _changes(self, value: bool) -> None:
        """Changes the saved-status text displayed on screen.

        Args:
            value (bool): saved or not.
        """
        self._saved_status = "unsaved" if value else "saved"
        self._text_status.set_text(self._saved_status)
        self._text_status.set_color(SHORTCUT_TEXT_COLOR if value else MODE_TEXT_COLOR)
    
    def _save(self) -> None:
        dict_file = {}
        dict_file["app"] = {}
        dict_file["app"]["width"] = self._ww
        dict_file["app"]["height"] = self._wh

        for controller in [self._wall, self._car]:
            dict_file = dict_file | controller.to_dict()
        
        with open(f"{get_data_folder(MAPS_FOLDER)}{self._file_name}.yaml", "w") as file:
            documents = yaml.dump(dict_file, file)

    def load(self, name: str) -> None:        
        self._file_name = name

    def loop(self) -> None:
        pass
