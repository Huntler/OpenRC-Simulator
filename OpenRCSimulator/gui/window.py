from typing import List
from OpenRCSimulator.graphics.window import BaseWindow
import pygame as py


MOUSE_CLICK = "mouse_click"
SHORTCUTS_UNTOGGLE = "untoggle_all"

CREATOR_PLACE_CAR = "creator_place_car"
CREATOR_PLACE_GOAL = "creator_place_goal"
CREATOR_PLACE_WALL= "creator_place_wall"
STORAGE_SAVE = "creato_save_map"

SENSORS_ACTIVATED = "sensors_activated"
TEXT_INPUT_W = "text_input_width"
TEXT_INPUT_L = "text_input_length"
TEXT_INPUT_T = "text_input_turn"


class MainWindow(BaseWindow):
    def sprites(self) -> None:
        # define sprites here
        pass

    def draw(self) -> None:
        pass

    def _execute_callback(self, type: str, param: dict = {}) -> None:
        func = self._callbacks.get(type, None)
        if func:
            func(**param)

    def _execute_callbacks(self, types: List[str], param: dict = {}) -> None:
        for CALLBACK in types:
            self._execute_callback(CALLBACK, param)

    def event(self, event) -> None:
        super().event(event)

        mouse_pos = py.mouse.get_pos()
        mouse_buttons = py.mouse.get_pressed()

        if event.type == py.KEYDOWN:
            # text input enabled, ignoring shortcuts        
            if self._text_input:
                if event.key == py.K_ESCAPE or event.key == py.K_RETURN:
                    self._text_input = False
                    self._text_cache = ""
                    self._execute_callbacks([TEXT_INPUT_W, TEXT_INPUT_L, TEXT_INPUT_T], 
                                            {"text": "\n"})

                elif event.key == py.K_BACKSPACE:
                    self._text_cache = self._text_cache[:-1]
                else:
                    self._text_cache += event.unicode
                    self._execute_callbacks([TEXT_INPUT_W, TEXT_INPUT_L, TEXT_INPUT_T],
                                            {"text": self._text_cache})
        
        if mouse_buttons[0]:
            func = self._callbacks.get(MOUSE_CLICK, None)
            if func:
                func(mouse_pos)