"""This module handles the simulation's visualization and enables manual play,
as well as watching the AI drive."""
import os
from typing import Callable, Dict, Tuple
import pygame as py
import yaml
from OpenRCSimulator.graphics.callback import KeyListener
from OpenRCSimulator.graphics.objects.text import Text
from OpenRCSimulator.gui.sub_controller.car_controller import CarController
from OpenRCSimulator.gui.sub_controller.shortcut_controller import ShortcutController
from OpenRCSimulator.gui.sub_controller.wall_controller import WallController
from OpenRCSimulator.log.log_consumer import LogConsumer
from OpenRCSimulator.state import MAPS_FOLDER, MODELS_FOLDER, get_data_folder
from OpenRCSimulator.graphics.controller import BaseController
from OpenRCSimulator.graphics.objects.rectangle import Rectangle
from OpenRCSimulator.gui import BACKGROUND_COLOR, MANUAL, MODE_TEXT_COLOR
from OpenRCSimulator.gui.window import MainWindow


MANUAL_ACCELERATE = "accelerate_rear"
MANUAL_SLOWDOWN = "slowdown_rear"
MANUAL_TURN_LEFT = "turn_left"
MANUAL_TURN_RIGHT = "turn_right"
MANUAL_MOTOR_STOP = "motor_stop"
SIMULATION_PAUSE = "pause"


class SimulationController(BaseController, KeyListener):
    """The SimulationController manages the MainWindow. This is a separate
    thread than the pygame one.

    Args:
        window_size (Tuple[int, int]): Width and height of the window.
        flags (int, optional): Fullscreen, hardware acceleration, ... Defaults to 0.
    """
    def __init__(self, window_size: Tuple[int, int], flags: int = 0) -> None:
        super().__init__()
        self._t = py.time.get_ticks()
        self._file_name = None
        self._log = LogConsumer()

        self._width, self._height = window_size
        self._center = (self._width // 2, self._height // 2)
        self._flags = flags
        self._active_sub_controller = None
        self._callback_register: Dict[int, Callable] = {}

        # create the window visuals
        self._window = MainWindow(window_size=window_size, flags=flags)
        self._surface = self._window.get_surface()

        self._window_title = "Simulation"
        self._window.set_title(self._window_title)

        self._title_font = self._window.get_font().copy(size=120)
        self._log.add_log("Created visuals")

        # background object (just a colored box)
        background = Rectangle(self._surface, 0, 0,
                               self._width, self._height, BACKGROUND_COLOR)
        self._window.add_sprite("background", background, zindex=99)

        background = Rectangle(self._surface, 0, 0,
                               self._width, self._height, BACKGROUND_COLOR)
        self._window.add_sprite("background", background, zindex=99)
        self._text_mode = Text(
            self._surface, "MANUAL", self._center[0], self._center[1], MODE_TEXT_COLOR, self._title_font)
        self._window.add_sprite("text_mode", self._text_mode, zindex=98)

        # create simulation objects
        self._car = CarController(self._window, MANUAL)
        self._wall = WallController(self._window, MANUAL)

        # show shortcut info
        self._shortcuts = ShortcutController(self._window)
        self._shortcuts.add_shortcut(
            SIMULATION_PAUSE, self._car.pause, "'P' Pause", py.K_p)

    def on_key_pressed(self, key: int) -> None:
        if key in self._callback_register:
            self._callback_register[key]()
    
    def on_key_released(self, key: int) -> None:
        if key in self._callback_register:
            self._callback_register[key]()

    def load(self, map_name: str, car_name: str) -> None:
        """Load the the given map to control the car on. If a car name is given, then the manual control is 
        disabled and the model loaded.

        Args:
            map_name (str): Map name to load.
            car_name (str): Car to load. Defaults to None (no car loaded.)
        """
        path = f"{get_data_folder(MAPS_FOLDER)}/{map_name}.yaml"
        if not os.path.exists(path):
            return

        # load the car's position and map
        with open(path, "r", encoding="UTF-8") as file:
            dict_file = yaml.load(file, Loader=yaml.FullLoader)
            self._car.from_dict(dict_file["car"])
            self._wall.from_dict(dict_file["walls"])

        # load the agent if given [todo]
        path = f"{get_data_folder(MODELS_FOLDER)}/car_{car_name}.pkl"
        if car_name and os.path.exists(path):
            _ = open(
                f"{get_data_folder(MODELS_FOLDER)}/car_{car_name}.pkl", 'rb')

            # change the background text
            self._text_mode.set_text("SIMULATION")
            self._text_mode.set_position((0, 0), Text.ANCHOR_CENTER)
        else:
            # if no agent is present, load manual controls by enabling key listener
            self._window.set_listener(self)

            self._callback_register[py.K_w] = self._car.accelerate
            self._callback_register[py.K_s] = self._car.slowdown
            self._callback_register[py.K_a] = self._car.turn_left
            self._callback_register[py.K_d] = self._car.turn_right
            self._callback_register[py.K_x] = self._car.stop

            self._window.set_title(self._window_title + " (Manual Controls)")

    def loop(self) -> None:
        # calculate the time delta
        delta = (py.time.get_ticks() - self._t) / 1_000
        self._t = py.time.get_ticks()

        walls = self._wall.get_walls()
        self._car.loop(delta, walls)

        self._t += delta
