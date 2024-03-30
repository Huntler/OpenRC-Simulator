"""This module handles the map creation."""
from typing import Tuple
import pygame as py
import yaml
from OpenRCSimulator.creator.creator_window import CreatorWindow
from OpenRCSimulator.state import MAPS_FOLDER, get_data_folder
from OpenRCSimulator.graphics.controller import BaseController
from OpenRCSimulator.graphics.sub_controller import BaseSubController
from OpenRCSimulator.gui import CREATOR
from OpenRCSimulator.gui.sub_controller.car_controller import CarController
from OpenRCSimulator.gui.sub_controller.wall_controller import WallController


class CreatorController(BaseController):
    """The CreatorController manages the MainWindow. This is a separate
    thread than the pygame one.

    Args:
        window_size (Tuple[int, int]): Width and height of the window.
        flags (int, optional): Fullscreen, hardware acceleration, ... Defaults to 0.
    """

    def __init__(self, window_size: Tuple[int, int], flags: int = 0) -> None:
        super().__init__()
        self._t = py.time.get_ticks()
        self._delta = 0.1
        self._file_name = None

        self._width, self._height = window_size
        self._center = (self._width // 2, self._height // 2)
        self._flags = flags
        self._is_saved = False

        # create the window visuals
        self._window = CreatorWindow(window_size=window_size)
        self._window.set_listener(self)
        self._surface = self._window.get_surface()

        self._window.set_title(self._window.get_title() + " (unsaved)")

        # create sub controllers
        self._active_sub_controller = None

        # create the car controller
        self._car = CarController(self._window, CREATOR)
        self._car.on_toggle(self._sub_controller_toggled)
        self._window.car_callback(self._car.toggle)

        # create the wall controller
        self._wall = WallController(self._window, CREATOR)
        self._wall.on_toggle(self._sub_controller_toggled)
        self._window.wall_callback(self._wall.toggle)

        # define other shortcuts
        self._window.save_callback(self._save)
        self._window.untoggle_callback(self._untoggle_all_sub_controller)

    def _sub_controller_toggled(self, sub_controller: BaseSubController) -> None:
        """This method executes if a subcontroller was toggled. In this case, this method 
        disables all other subcontrollers.
        """
        # if the active sub controller was toggled again, then just unregister it
        if self._active_sub_controller == sub_controller:
            self._active_sub_controller = None
            self._changes()
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
            self._changes()

    def _changes(self) -> None:
        """Changes the saved-status text displayed on screen.

        Args:
            value (bool): saved or not.
        """
        self._window.set_title(self._window.get_title() + " (unsaved)")

    def _save(self) -> None:
        # create the dict to store
        dict_file = {}
        dict_file["app"] = {}

        width, height = self._surface.get_size()
        dict_file["app"]["width"] = width
        dict_file["app"]["height"] = height

        # get subcontroller infos, such as car position, walls, ...
        for controller in [self._wall, self._car]:
            dict_file = dict_file | controller.to_dict()

        # save the dict
        path = f"{get_data_folder(MAPS_FOLDER)}{self._file_name}.yaml"
        with open(path, "w", encoding="UTF-8") as file:
            _ = yaml.dump(dict_file, file)

        # show saved status
        self._window.set_title(self._window.get_title())

    def load(self, name: str) -> None:
        """This method sets the name of a map.

        Args:
            name (str): The map's name.
        """
        self._file_name = name

    def loop(self) -> None:
        pass
