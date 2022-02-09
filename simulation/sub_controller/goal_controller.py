from typing import Dict
from graphics.objects.text import ANCHOR_TOP_LEFT, Text
from graphics.sub_controller import BaseSubController
from simulation import CREATOR, SHORTCUT_TEXT_COLOR
from simulation.window import CREATOR_PLACE_GOAL, SimulationWindow


class GoalController(BaseSubController):
    def __init__(self, window: SimulationWindow, app_mode: int) -> None:
        super().__init__()
        self._app_mode = app_mode
        
        # window and surface information
        self._window = window
        self._ww, self._wh = window.get_window_size()
        self._surface = window.get_surface()

        # goal sprite
        # TODO
        
        # goal placement shortcuts
        if app_mode == CREATOR:
            self._text_goal = Text(self._surface, "'G' Place the goal", 0, 0, 30, SHORTCUT_TEXT_COLOR)
            self._text_goal.set_position((20, self._wh - 70), ANCHOR_TOP_LEFT)
            self._window.add_sprite("text_goal", self._text_goal, zindex=98)
            self._window.on_callback(CREATOR_PLACE_GOAL, self.toggle)
    
    def toggle(self, call: bool = True) -> None:
        super().toggle(call)
    
    def loop(self) -> None:
        pass

    def dict(self) -> Dict:
        return {}