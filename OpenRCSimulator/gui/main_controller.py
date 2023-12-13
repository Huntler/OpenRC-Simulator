import time
from typing import Tuple
import pickle
import pygame as py
from OpenRCSimulator.gui.sub_controller.shortcut_controller import ShortcutController
from OpenRCSimulator.state import MAPS_FOLDER, get_data_folder, MODELS_FOLDER
from OpenRCSimulator.graphics.controller import BaseController
from OpenRCSimulator.graphics.objects.rectangle import Rectangle
from OpenRCSimulator.graphics.objects.text import ANCHOR_TOP_LEFT, Text
from OpenRCSimulator.graphics.sub_controller import BaseSubController
from OpenRCSimulator.gui import BACKGROUND_COLOR, CREATOR, MANUAL, MODE_TEXT_COLOR, SHORTCUT_TEXT_COLOR
from OpenRCSimulator.gui.sub_controller.car_controller import CarController
from OpenRCSimulator.gui.sub_controller.storage_controller import StorageController
from OpenRCSimulator.gui.sub_controller.wall_controller import WallController
from OpenRCSimulator.gui.window import CREATOR_PLACE_CAR, CREATOR_PLACE_WALL, MANUAL_ACCELERATE, MANUAL_MOTOR_STOP, MANUAL_SLOWDOWN, MANUAL_TURN_LEFT, MANUAL_TURN_RIGHT, SHORTCUTS_UNTOGGLE, SIMULATION_PAUSE, MainWindow


class MainController(BaseController):
    def __init__(self, window_size: Tuple[int, int], mode: int, flags: int = 0) -> None:
        """The SimulationController manages the SimulationWindow. This is a separate
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

        # create the car controller
        self._car = CarController(self._window, mode)
        self._car.on_toggle(self._sub_controller_toggled)

        # create the wall controller
        self._wall = WallController(self._window, mode)
        self._wall.on_toggle(self._sub_controller_toggled)

        # create the storage controller
        self._storage = StorageController(self._window, mode)
        self._storage.on_toggle(self._save)

        # create shortcuts
        self._shortcuts = ShortcutController(self._window)
        if mode == CREATOR:
            self._shortcuts.add_shortcut(CREATOR_PLACE_WALL, self._wall.toggle, "'P' Start drawing a wall", py.K_p, can_toggle=True)
            self._shortcuts.add_shortcut(CREATOR_PLACE_CAR, self._car.toggle, "'R' Place the car", py.K_r)
        
        if mode == MANUAL:
            # driving shortcuts are defined in 'CarController'
            self._shortcuts.add_shortcut(SIMULATION_PAUSE, self._car.pause, "'P' Pause simulation", py.K_p, can_toggle=True)

        self.mode(mode)
    
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
    
    def mode(self, mode: int) -> None:
        """The applications mode (CREATOR, SIMULATION, MANUAL)

        Args:
            mode (int): The mode.
        """
        self._mode = mode
        cx, cy = self._center

        # show background text
        # text describing the current mode (integrated into the background)
        mode_text = ["SIMULATION", "CREATOR", "MANUAL", "TRAINING"]
        text_mode = Text(self._surface, mode_text[mode], cx, cy, MODE_TEXT_COLOR, self._title_font)
        self._window.add_sprite("text_mode", text_mode, zindex=98)

        # show shortcut info for CREATOR mode
        shortcuts_height = [80, 180, 110, 80]
        text_shortcuts = Text(self._surface, "Shortcuts", 0, 0, SHORTCUT_TEXT_COLOR, self._shortcuts_font)
        text_shortcuts.set_position((20, self._height - shortcuts_height[mode]), ANCHOR_TOP_LEFT)
        self._window.add_sprite("text_shortcuts_title", text_shortcuts)
    
    def _save(self) -> None:
        self._storage.save(self._file_name, {
            CREATOR: [self._car, self._wall]
        })

    def file(self, name: str, car_name: str = None) -> None:        
        self._file_name = name
        if self._mode != CREATOR:
            self._storage.load(get_data_folder(MAPS_FOLDER), name, [self._car, self._wall])

        if car_name:
            # load the car's brain from file
            filehandler = open(f"{get_data_folder(MODELS_FOLDER)}/car_{car_name}.pkl", 'rb') 
            genome = pickle.load(filehandler)
            self._car.set_brain(genome)

            print("Loaded trained car into simulation.")

    def loop(self) -> None:
        # calculate the time delta
        delta = (py.time.get_ticks() - self._t) / 1_000
        self._t = py.time.get_ticks()

        self._wall.loop()
        walls = self._wall.get_walls()
        self._car.loop(delta, walls)

        self._t += delta
