"""This module handles the sub controller base class."""
from typing import Callable, Dict


class BaseSubController:
    """The base sub controller handles basic uses, e.g. toggling a 
    controller.
    """
    def __init__(self) -> None:
        self.dict_name = None

        self._toggle_callback = False
        self._toggled = False

    def is_toggled(self) -> bool:
        """This method checks if the current controller is toggled.

        Returns:
            bool: True if toggled, else False.
        """
        return self._toggled

    def on_toggle(self, func: Callable) -> None:
        """This method executes a function on toggle.

        Args:
            func (Callable): The function to execute.
        """
        self._toggle_callback = func

    def toggle(self, call: bool = True) -> None:
        """This method toggles the current controller and executes the 
        registered callback funtion. This can be disabled by defining call=False.

        Args:
            call (bool, optional): Disables the callback execution. Defaults to True.
        """
        self._toggled = not self._toggled

        if self._toggle_callback and call:
            self._toggle_callback(self)

    def to_dict(self) -> Dict:
        """This method transfers the controllers information to a dictionary.

        Raises:
            NotImplementedError: Needs to be implemented by a child class.

        Returns:
            Dict: The information of this object.
        """
        raise NotImplementedError

    def from_dict(self, d: Dict) -> None:
        """This method loads the information of a dict to this controller.

        Args:
            d (Dict): The information, correct format required.

        Raises:
            NotImplementedError: Needs to be implemented by a child class.
        """
        raise NotImplementedError
