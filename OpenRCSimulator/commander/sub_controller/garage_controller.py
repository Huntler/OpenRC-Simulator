import math
from time import sleep
import numpy as np
import pygame as py
from typing import Dict, Tuple
from OpenRCSimulator.commander import SHORTCUT_TEXT_COLOR, SHORTCUT_TEXT_COLOR_ACTIVE

from OpenRCSimulator.commander.window import MOUSE_CLICK, SENSORS_ACTIVATED, TEXT_INPUT_W, TEXT_INPUT_L, TEXT_INPUT_T, SimulationWindow
from OpenRCSimulator.graphics.objects.text_field import TextField
from OpenRCSimulator.graphics.window import MUTEX
from OpenRCSimulator.simulation.openrc import OpenRC
from OpenRCSimulator.simulation import CHASSIS_SIZE
from OpenRCSimulator.graphics.objects.car import Car
from OpenRCSimulator.graphics.objects.text import ANCHOR_TOP_LEFT, Text
from OpenRCSimulator.graphics.sub_controller import BaseSubController


CENTIMETER_TO_PIXEL = 20
PIXEL_TO_CENTIMETER = 1. / CENTIMETER_TO_PIXEL


class GarageController(BaseSubController):
    def __init__(self, window: SimulationWindow, app_mode: int, font) -> None:
        super().__init__()
        self._app_mode = app_mode
        self.dict_name = "car"
        self._is_paused = False

        # window and surface information
        self._window = window
        self._ww, self._wh = window.get_window_size()
        self._surface = window.get_surface()
        self._font = font

        # car position and size (1cm = 10px)
        center_x, center_y = self._ww / 2, self._wh / 2
        car_size = [CHASSIS_SIZE[0] * CENTIMETER_TO_PIXEL, CHASSIS_SIZE[1] * CENTIMETER_TO_PIXEL]

        # car sprite
        self._sprite_car = Car(self._surface, center_x, center_y, car_size, font, Car.CONFIG)
        self._sprite_car.set_direction(0)
        self._window.add_sprite("sprite_car", self._sprite_car, zindex=90)

        ###############
        # input texts #
        ###############
        # car width
        self._text_car_width = Text(self._surface, "Width (cm)", center_x - car_size[1] / 2 - 70, center_y - 10, 30, (255, 255, 255))
        self._window.add_sprite("text_width", self._text_car_width)

        self._field_car_width = TextField(self._surface, center_x - car_size[1] / 2 - 70, center_y + 20, 30, "18")
        self._field_car_width.set_text_filter(TextField.FILTER_NUMBERS)
        self._field_car_width.on_activated(self._window.toggle_text_capture)
        self._window.add_sprite("field_width", self._field_car_width)
        self._window.on_callback(TEXT_INPUT_W, self._field_car_width.update_text)

        # car length
        self._text_car_length = Text(self._surface, "Length (cm)", center_x, center_y - car_size[0] / 2 - 80, 30, (255, 255, 255))
        self._window.add_sprite("text_length", self._text_car_length)

        self._field_car_length = TextField(self._surface, center_x, center_y - car_size[0] / 2 - 50, 30, "18")
        self._field_car_length.set_text_filter(TextField.FILTER_NUMBERS)
        self._field_car_length.on_activated(self._window.toggle_text_capture)
        self._window.add_sprite("field_length", self._field_car_length)
        self._window.on_callback(TEXT_INPUT_L, self._field_car_length.update_text)

        # car max turn
        self._text_car_angle = Text(self._surface, "Angle (°)", center_x + car_size[1] / 2 + 80, center_y - 10, 30, (255, 255, 255))
        self._window.add_sprite("text_angle", self._text_car_angle)

        self._field_car_angle = TextField(self._surface, center_x + car_size[1] / 2 + 80, center_y + 20, 30, "18")
        self._field_car_angle.set_text_filter(TextField.FILTER_NUMBERS)
        self._field_car_angle.on_activated(self._window.toggle_text_capture)
        self._window.add_sprite("field_angle", self._field_car_angle)
        self._window.on_callback(TEXT_INPUT_T, self._field_car_angle.update_text)

        # shortcuts
        self._sensors_activated = False
        self._text_sensors = Text(self._surface, "'A' Activate sensors", 0, 0, 30, SHORTCUT_TEXT_COLOR)
        self._text_sensors.set_position((20, self._wh - 70), ANCHOR_TOP_LEFT)
        self._window.add_sprite("text_car", self._text_sensors)
        self._window.on_callback(SENSORS_ACTIVATED, self.toggle)

    def toggle(self, call: bool = True) -> None:
        """This method toggles a special mode for this controller. In CREATOR mode, the car's 
        position can be changed.

        Args:
            call (bool, optional): If false, then the registered callback is not executed. Defaults to True.
        """
        super().toggle(call)

        if self._toggled:
            self._text_sensors.set_color(SHORTCUT_TEXT_COLOR_ACTIVE)
            self._sensors_activated = True

        else:
            self._text_sensors.set_color(SHORTCUT_TEXT_COLOR)
            self._sensors_activated = False

    def _on_mouse_click(self, pos: Tuple[int, int]) -> None:
        """This method is executed, if the event was registered from inside this controller.

        Args:
            pos (Tuple[int, int]): The mouse position.
        """
        if not self._sprite_position_set:
            self._sprite_position_set = True
        else:
            self.toggle()
        sleep(0.2)

    def to_dict(self) -> Dict:
        """Used to pickle data from this class. The data configures the car's configuration 
        and simulation behaviour.

        Returns:
            Dict: Car's configuration.
        """
        x, y = self._sprite_car.get_position()
        dict_file = {}
        dict_file["car"] = {}
        dict_file["car"]["rear_dist"] = self._field_car_width.get_text()
        dict_file["car"]["front_rear_dist"] = self._field_car_length.get_text()
        dict_file["car"]["max_turn_angle"] = self._field_car_angle.get_text()
        return dict_file

    def from_dict(self, d: Dict) -> None:
        """Unpickles class from given dict to adjust car's configuration.

        Args:
            d (Dict): Corresponding dict.
        """
        self._field_car_width.set_text(d["rear_dist"])
        self._field_car_length.set_text(d["front_rear_dist"])
        self._field_car_angle.set_text(d["max_turn_angle"])

    def loop(self) -> None:
        """
        This loop is always executed by the main controller.
        """
        pass


        
