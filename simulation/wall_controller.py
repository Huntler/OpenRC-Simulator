
from typing import Tuple
from pygame import Surface
from graphics.objects.robot import Robot
from graphics.objects.text import ANCHOR_TOP_LEFT, Text
from graphics.sub_controller import BaseSubController
from simulation import CREATOR, SHORTCUT_TEXT_COLOR, SHORTCUT_TEXT_COLOR_ACTIVE
from simulation.window import CREATOR_PLACE_WALL, MOUSE_CLICK, SimulationWindow


WALL_COLOR = (200, 160, 160)
WALL_THICKNESS = 10


class WallController(BaseSubController):
    def __init__(self, window: SimulationWindow, app_mode: int) -> None:
        super().__init__()
        self._app_mode = app_mode
        
        # window and surface information
        self._window = window
        self._ww, self._wh = window.get_window_size()
        self._surface = window.get_surface()

        # wall sprites
        self._walls = []

        # wall placement shortcuts
        if app_mode == CREATOR:
            self._text_wall = Text(self._surface, "'P' Start drawing a wall", 0, 0, 30, SHORTCUT_TEXT_COLOR)
            self._text_wall.set_position((20, self._wh - 70), ANCHOR_TOP_LEFT)

            self._window.add_sprite("text_wall", self._text_wall, zindex=98)
            self._window.on_callback(CREATOR_PLACE_WALL, self.toggle)    

    def toggle(self, call: bool = True) -> None:
        super().toggle(call)

        if self._toggled:
            self._window.on_callback(MOUSE_CLICK, self._on_mouse_click)
            self._text_wall.set_color(SHORTCUT_TEXT_COLOR_ACTIVE)

        else:
            self._window.remove_callback(MOUSE_CLICK)
            self._text_wall.set_color(SHORTCUT_TEXT_COLOR)
        
    def _on_mouse_click(self, pos: Tuple[int, int]) -> None:
        self.toggle()

    def app_mode(self, mode: int) -> None:
        self._app_mode = mode
    
    def loop(self) -> None:
        pass