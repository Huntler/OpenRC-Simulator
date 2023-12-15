from typing import Tuple
import pygame as py


class Sprite:
    def __init__(self) -> None:
        self._button_down = False
        self._size = None

    def set_position(self, pos: Tuple[int, int]) -> None:
        raise NotImplemented

    def get_position(self) -> Tuple[int, int]:
        raise NotImplemented

    def get_size(self) -> Tuple[int, int]:
        return self._size

    def draw(self) -> None:
        mouse_pos = py.mouse.get_pos()
        mouse_buttons = py.mouse.get_pressed()

        if self.collidepoint(mouse_pos):
            if mouse_buttons[0]:
                self._button_down = True

            if self._button_down and not mouse_buttons[0]:
                self._clicked()
                self._button_down = False

        elif self._button_down:
            self._button_down = False

    def active(self, val: bool) -> None:
        """
        Only active sprites can call the hover and click event.
        """
        self._active = val

    def callback(self, event_type, func) -> None:
        raise NotImplemented

    def collidepoint(self, point: Tuple[int, int]) -> bool:
        raise NotImplemented

    def _clicked(self) -> None:
        raise NotImplemented
