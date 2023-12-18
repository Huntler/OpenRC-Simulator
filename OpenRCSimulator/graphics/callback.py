from typing import Tuple

from OpenRCSimulator.graphics.objects.text_field import TextField


class BaseListener:
    def __init__(self) -> None:
        pass

class MouseListener(BaseListener):
    def on_movement(self, position: Tuple[int, int], delta: Tuple[int, int]) -> None:
        pass

    def on_click(self, buttons: Tuple[bool, bool, bool], position: Tuple[int, int]) -> None:
        pass

class TextListener(BaseListener):
    def on_text_changed(self, object: TextField, text: str) -> None:
        pass

    def on_text_end(self, object: TextField) -> None:
        pass

class KeyListener(BaseListener):
    def on_key_pressed(self, key: int) -> None:
        pass

class WindowListener(BaseListener):
    def on_quit(self) -> None:
        pass