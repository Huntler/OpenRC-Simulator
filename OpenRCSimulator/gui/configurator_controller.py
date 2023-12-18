import os
from typing import Any, Tuple
import pygame as py
import yaml
from OpenRCSimulator.graphics.objects.car_base import CarBase
from OpenRCSimulator.graphics.objects.text_field import TextField
from OpenRCSimulator.gui.sub_controller.form_controller import FormController, FormListener
from OpenRCSimulator.gui.sub_controller.shortcut_controller import ShortcutController
from OpenRCSimulator.state import get_data_folder
from OpenRCSimulator.graphics.controller import BaseController
from OpenRCSimulator.graphics.objects.rectangle import Rectangle
from OpenRCSimulator.gui import BACKGROUND_COLOR
from OpenRCSimulator.gui.window import MainWindow

SAVE = "save_configuration"


WEIGHT = "weight"
GEAR_RATIO = "gear_ratio"
MOTOR_POWER = "motor_power"


class ConfiguratorController(BaseController, FormListener):
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
        self._base_form = FormController(self._window, "Base", (8, 8), 
                                    (self._width // 3 - 8, self._height - 16), listener=self)
        self._base_form.add_element(CarBase.WHEELBASE, "Wheelbase (cm)", "0", TextField.FILTER_NUMBERS)
        self._base_form.add_element(CarBase.TRACK_SPACING, "Track Spacing (cm)", "0", TextField.FILTER_NUMBERS)
        self._base_form.add_element(CarBase.WHEEL_DIAMETER, "Wheel Diameter (cm)", "0", TextField.FILTER_NUMBERS)
        self._base_form.add_element(CarBase.WHEEL_WIDTH, "Wheel Width (cm)", "0", TextField.FILTER_NUMBERS)
        self._base_form.add_element(CarBase.STEERING_ANGLE, "Steering Angle (°)", "0", TextField.FILTER_NUMBERS)

        self._chassis_form = FormController(self._window, "Chassis", (self._width // 3 + 8, 8), 
                                            (self._width // 3 - 8, self._height // 2 - 16), listener=self)        
        self._chassis_form.add_element(CarBase.CHASSIS_FRONT, "Chassis Front (cm)", "0", TextField.FILTER_NUMBERS)
        self._chassis_form.add_element(CarBase.CHASSIS_REAR, "Chassis Rear (cm)", "0", TextField.FILTER_NUMBERS)

        self._motor_form = FormController(self._window, "Motor", (self._width // 3 + 8, self._height // 2),
                                          (self._width // 3 - 8, self._height // 2 - 8), listener=self)
        self._motor_form.add_element(WEIGHT, "Total Weight (kg)", "0", TextField.FILTER_NUMBERS)
        self._motor_form.add_element(MOTOR_POWER, "Motor Power (W)", "0", TextField.FILTER_NUMBERS)
        self._motor_form.add_element(GEAR_RATIO, "Gear Ratio (1:X)", "0", TextField.FILTER_NUMBERS)

        # add live preview of changes
        self._car_base = CarBase(self._surface, ((self._width // 3 + 8) * 2 - 8, 8), 
                                 (self._width // 3 - 16, self._height - 16), margins=(20, 50, 20, 50))
        self._window.add_sprite("live_preview", self._car_base)

        # show shortcut info
        self._shortcuts = ShortcutController(self._window)
        self._shortcuts.add_shortcut(SAVE, self._save, "'S' Save configuration", py.K_s)
    
    def on_form_change(self, name: str, value: Any) -> None:
        if value:
            self._car_base.set_value(name, float(value))
    
    def _save(self) -> None:
        """Save the current configuration.
        """
        data = {}
        for d in [self._base_form.get_data(), self._chassis_form.get_data(), self._motor_form.get_data()]:
            data.update(d)

        with open(f"{get_data_folder('')}/car_config.yaml", "w") as file:
            documents = yaml.dump(data, file)

    def load(self) -> None:        
        """Load the current configuration to be edited.
        """
        path = f"{get_data_folder('')}car_config.yaml"
        if not os.path.exists(path):
            return
        
        with open(path, "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        
        self._base_form.set_data(data)
        self._chassis_form.set_data(data)
        self._motor_form.set_data(data)
        for key, value in data.items():
            self._car_base.set_value(key, value)

    def loop(self) -> None:
        pass
