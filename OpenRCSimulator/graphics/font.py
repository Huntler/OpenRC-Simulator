"""This module handles the font system."""
import pygame as py


class FontWrapper:
    """The FontWrapper wraps a pygame.font for easier access and error handling.
    """
    def __init__(self, name: str = None, size: int = 10) -> None:
        self._name = name
        self._size = size

        if not py.font.get_init():
            py.font.init()

        if not self.name:
            self._name = py.font.get_default_font()

        elif self._name not in py.font.get_fonts():
            print(
                f"Could not find font {self._name}, fallback to system default.")
            self._name = py.font.get_default_font()

        self.__font = py.font.SysFont(self._name, self._size)

    def copy(self, name: str = None, size: int = None) -> "FontWrapper":
        """this method copies the current object to a new object.

        Args:
            name (str, optional): Change the font name of the new object. Defaults to None.
            size (int, optional): Change the font size of the new object. Defaults to None.

        Returns:
            FontWrapper: The newly created object.
        """
        if not name:
            name = self.name

        if not size:
            size = self.size

        return FontWrapper(name, size)

    def unpack(self) -> py.font.Font:
        """This method unpacks the pygame.font from this wrapper.

        Returns:
            py.font.Font: The font object.
        """
        return self.__font

    @property
    def name(self) -> str:
        """The font's name

        Returns:
            str: Name
        """
        return self._name

    @property
    def size(self) -> int:
        """The font's size

        Returns:
            int: Size
        """
        return self._size
