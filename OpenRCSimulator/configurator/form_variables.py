"""This module defines the car configuration form."""
from typing import Callable
from OpenRCSimulator.graphics.objects.text_field import TextField
from OpenRCSimulator.graphics.window import BaseWindow
from OpenRCSimulator.graphics.elements.form_controller import FormController


WEIGHT = "weight"
GEAR_RATIO = "gear_ratio"
MOTOR_POWER = "motor_power"


def create_variables_form(window: BaseWindow, width: int, height: int,
                        listener: Callable) -> FormController:
    """Creates the car's variables configuration form.

    Args:
        window (BaseWindow): The window showing this form.
        width (int): Width of the window.
        height (int): Height of the window.
        listener (Callable): Class receiving the callbacks.

    Returns:
        FormController: The controller.
    """
    form = FormController(window, "Motor", (width // 3 + 8, height // 2),
                          (width // 3 - 8, height // 2 - 8),
                          listener=listener)
    form.add_element(WEIGHT, "Total Weight (kg)", "0",
                     TextField.FILTER_NUMBERS)
    form.add_element(MOTOR_POWER, "Motor Power (W)", "0",
                     TextField.FILTER_NUMBERS)
    form.add_element(GEAR_RATIO, "Gear Ratio (1:X)", "0",
                     TextField.FILTER_NUMBERS)

    return form
