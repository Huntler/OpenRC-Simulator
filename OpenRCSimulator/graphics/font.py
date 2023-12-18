import pygame as py


class FontWrapper:
    def __init__(self, name: str = None, size: int = 10) -> None:
        self._name = name
        self._size = size

        if not py.font.get_init():
            py.font.init()

        if not self.name:
            self._name = py.font.get_default_font()

        elif self._name not in py.font.get_fonts():
            print(f"Could not find font {self._name}, fallback to system default.")
            self._name = py.font.get_default_font()
        
        self.__font = py.font.SysFont(self._name, self._size)

    def copy(self, name: str = None, size: int = None) -> "FontWrapper":
        if not name:
            name = self.name
        
        if not size:
            size = self.size
        
        return FontWrapper(name, size)
    
    def unpack(self) -> py.font.Font:
        return self.__font

    @property
    def name(self) -> str:
        return self._name

    @property
    def size(self) -> int:
        return self._size