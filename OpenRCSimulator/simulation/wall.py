"""This module represents a wall used within the backend simulation."""
from typing import Tuple


class Wall:
    """A wall starts at a position and ends at a different position.
    """

    def __init__(self, start_pos: Tuple, end_pos: Tuple) -> None:
        self._dict_name = "walls"

        self._start_pos = start_pos
        self._end_pos = end_pos

    @property
    def dict_name(self) -> str:
        """The dict name is handy to pickle this object.

        Returns:
            str: The name of this class.
        """
        return self._dict_name
