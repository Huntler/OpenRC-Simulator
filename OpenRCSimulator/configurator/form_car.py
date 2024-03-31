"""This module defines the car configuration form."""
from typing import Callable
from OpenRCSimulator.graphics.objects.car_base import CarBase
from OpenRCSimulator.graphics.objects.text_field import TextField
from OpenRCSimulator.graphics.window import BaseWindow
from OpenRCSimulator.graphics.elements.form_controller import FormController


def create_car_form(window: BaseWindow, width: int, height: int,
                    listener: Callable) -> FormController:
    """Creates the car configuration form.

    Args:
        window (BaseWindow): The window showing this form.
        width (int): Width of the window.
        height (int): Height of the window.
        listener (Callable): Class receiving the callbacks.

    Returns:
        FormController: The controller.
    """
    form = FormController(window, "Base", (8, 8),
                                     (width // 3 - 8, height - 16),
                                     listener=listener)

    form.add_element(CarBase.WHEELBASE, "Wheelbase (cm)",
                     "0", TextField.FILTER_NUMBERS)
    form.add_element(CarBase.TRACK_SPACING, "Track Spacing (cm)",
                     "0", TextField.FILTER_NUMBERS)
    form.add_element(CarBase.WHEEL_DIAMETER, "Wheel Diameter (cm)",
                     "0", TextField.FILTER_NUMBERS)
    form.add_element(CarBase.WHEEL_WIDTH, "Wheel Width (cm)",
                     "0", TextField.FILTER_NUMBERS)
    form.add_element(CarBase.STEERING_ANGLE, "Steering Angle (°)",
                     "0", TextField.FILTER_NUMBERS)

    return form
