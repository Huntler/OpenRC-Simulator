"""This module controls the graphics of the configurator window."""
# pylint: disable=E1101
from typing import Callable, Dict, Tuple
import pygame as py
from OpenRCSimulator.configurator.form_car import create_car_form
from OpenRCSimulator.configurator.form_chassis import create_chassis_form
from OpenRCSimulator.configurator.form_variables import create_variables_form
from OpenRCSimulator.graphics.elements.shortcut_controller import ShortcutController
from OpenRCSimulator.graphics.objects.rectangle import Rectangle
from OpenRCSimulator.graphics.window import BaseWindow
from OpenRCSimulator.gui import BACKGROUND_COLOR, SHORTCUT_ENTRY_SEPARATION, SHORTCUT_TEXT_COLOR, \
    SHORTCUT_TEXT_COLOR_ACTIVE


SAVE = "save_configuration"


class ConfiguratorWindow(BaseWindow):
    """Visualization of the configurator window. The user is able to configure the car.

    Args:
        BaseWindow (BaseWindow): Super class.
    """

    def __init__(self, window_size: Tuple[int, int], draw_area: Tuple[int, int] = None,
                 listener: Callable = None) -> None:
        super().__init__(window_size, draw_area, "Car Configurator", frame_rate=60, flags=0)

        # background object (just a colored box)
        background = Rectangle(self._surface, 0, 0,
                               self._width, self._height, BACKGROUND_COLOR)
        self.add_sprite("background", background, zindex=99)

        # create the forms
        self._form_car = create_car_form(
            self, self._width, self._height, listener)
        self._form_chassis = create_chassis_form(
            self, self._width, self._height, listener)
        self._form_variables = create_variables_form(
            self, self._width, self._height, listener)

        # show shortcut info
        self._shortcuts = ShortcutController(self, text_color=SHORTCUT_TEXT_COLOR,
                                             active_text_color=SHORTCUT_TEXT_COLOR_ACTIVE,
                                             entry_separation=SHORTCUT_ENTRY_SEPARATION)

    def draw(self) -> None:
        pass

    def get_form_data(self) -> Dict:
        """Returns the user input of all forms.

        Returns:
            Dict: Dictionary including all data.
        """
        data = self._form_car.to_dict()
        data = data | self._form_chassis.to_dict()
        data = data | self._form_variables.to_dict()

        return data

    def set_form_data(self, data: Dict) -> None:
        """Sets the data to all forms of the UI.

        Args:
            data (Dict): Data to set.
        """
        self._form_car.from_dict(data)
        self._form_chassis.from_dict(data)
        self._form_variables.from_dict(data)

    def save_callback(self, callback: Callable) -> None:
        """Sets the callback when the user wants to save.

        Args:
            callback (Callable): The save-configuration function.
        """
        self._shortcuts.add_shortcut(
            SAVE, callback, "'S' Save the configuration", py.K_s)
