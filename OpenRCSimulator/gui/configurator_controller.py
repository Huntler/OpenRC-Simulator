import os
from typing import Tuple
import pygame as py
import yaml
from OpenRCSimulator.graphics.objects.text_field import TextField
from OpenRCSimulator.gui.sub_controller.form_controller import FormController
from OpenRCSimulator.gui.sub_controller.shortcut_controller import ShortcutController
from OpenRCSimulator.state import get_data_folder
from OpenRCSimulator.graphics.controller import BaseController
from OpenRCSimulator.graphics.objects.rectangle import Rectangle
from OpenRCSimulator.gui import BACKGROUND_COLOR
from OpenRCSimulator.gui.window import MainWindow

SAVE = "save_configuration"

WHEELBASE = "wheelbase"
TRACK_SPACING = "track_spacing"
STEERING_ANGLE = "steering_angle"
WEIGTH = "weight"
GEAR_RATIO = "gear_ratio"
MOTOR_POWER = "motor_power"
WHEEL_SIZE = "tire_size"


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

        # create the sprites we want to use
        # background object (just a colored box)
        background = Rectangle(self._surface, 0, 0, self._width, self._height, BACKGROUND_COLOR)
        self._window.add_sprite("background", background, zindex=99)

        # create form
        self._form = FormController(self._window, "Dimensions", (8, 8), (self._width // 2 - 16, self._height - 16))

        self._form.add_element(WHEELBASE, "Wheelbase (cm)", "0", TextField.FILTER_NUMBERS)
        self._form.add_element(WHEEL_SIZE, "Wheel Size (cm)", "0", TextField.FILTER_NUMBERS)
        self._form.add_element(TRACK_SPACING, "Track Spacing (cm)", "0", TextField.FILTER_NUMBERS)
        self._form.add_element(STEERING_ANGLE, "Steering Angle (°)", "0", TextField.FILTER_NUMBERS)
        self._form.add_element(WEIGTH, "Total Weight (kg)", "0", TextField.FILTER_NUMBERS)
        self._form.add_element(MOTOR_POWER, "Motor Power (W)", "0", TextField.FILTER_NUMBERS)
        self._form.add_element(GEAR_RATIO, "Gear Ratio (1:X)", "0", TextField.FILTER_NUMBERS)

        # show shortcut info
        self._shortcuts = ShortcutController(self._window)
        self._shortcuts.add_shortcut(SAVE, self._save, "'S' Save configuration", py.K_s)
    
    def _save(self) -> None:
        """Save the current configuration.
        """
        with open(f"{get_data_folder('')}/car_config.yaml", "w") as file:
            documents = yaml.dump(self._form.get_data(), file)

    def load(self) -> None:        
        """Load the current configuration to be edited.
        """
        path = f"{get_data_folder('')}car_config.yaml"
        if not os.path.exists(path):
            return
        
        with open(path, "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        
        self._form.set_data(data)

    def loop(self) -> None:
        pass
