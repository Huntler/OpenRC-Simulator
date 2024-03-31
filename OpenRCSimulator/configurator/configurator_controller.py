"""This module handles the car's configuration used within the simulation."""
import os
from typing import Any, Tuple
import pygame as py
import yaml
from OpenRCSimulator.configurator.configurator_window import ConfiguratorWindow
from OpenRCSimulator.graphics.objects.car_base import CarBase
from OpenRCSimulator.graphics.controller import BaseController
from OpenRCSimulator.state import get_data_folder
from OpenRCSimulator.graphics.elements.form_controller import FormListener

SAVE = "save_configuration"

WEIGHT = "weight"
GEAR_RATIO = "gear_ratio"
MOTOR_POWER = "motor_power"


class ConfiguratorController(BaseController, FormListener):
    """The ConfiguratorController manages the MainWindow. This is a separate
    thread than the pygame one.

    Args:
        window_size (Tuple[int, int]): Width and height of the window.
    """
    def __init__(self, window_size: Tuple[int, int]) -> None:
        super().__init__()
        self._t = py.time.get_ticks()
        self._file_name = None

        self._width, self._height = window_size
        self._center = (self._width // 2, self._height // 2)

        # create the window visuals
        self._window = ConfiguratorWindow(window_size=window_size, listener=self)
        self._window.set_title(self._window.get_title() + " (unsaved)")
        self._window.save_callback(self._save)

        self._surface = self._window.get_surface()
        self._title_font = self._window.get_font().copy(size=14)

        # add live preview of changes
        self._car_base = CarBase(self._surface, ((self._width // 3 + 8) * 2 - 8, 8),
                                 (self._width // 3 - 16, self._height - 16),
                                 margins=(20, 50, 20, 50))
        self._window.add_sprite("live_preview", self._car_base)
        self._log.add_log("Configurator started.")

    def on_form_change(self, name: str, value: Any, input_finished: bool) -> None:
        if value and input_finished:
            self._car_base.set_value(name, float(value))
            self._log.add_log(f"Changed value {name} to {value}.")
            self._window.set_title(self._window.get_title() + " (unsaved)")

    def _save(self) -> None:
        """Save the current configuration.
        """
        path = f"{get_data_folder('')}/car_config.yaml"
        with open(path, "w", encoding="UTF-8") as file:
            _ = yaml.dump(self._window.get_form_data(), file)

        self._window.set_title(self._window.get_title())
        self._log.add_log("Configuration saved.")

    def load(self) -> None:
        """Load the current configuration to be edited.
        """
        path = f"{get_data_folder('')}car_config.yaml"
        if not os.path.exists(path):
            return

        with open(path, "r", encoding="UTF-8") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        self._window.set_form_data(data)
        for key, value in data.items():
            self._car_base.set_value(key, value)

        self._window.set_title(self._window.get_title())
        self._log.add_log("Configuration loaded.")

    def loop(self) -> None:
        pass
