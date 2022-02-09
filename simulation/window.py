from graphics.window import BaseWindow
import pygame as py


MOUSE_CLICK = "mouse_click"
CREATOR_TOGGLE_ROBOT = "creator_robot_toggle"
CREATOR_PLACE_WALL= "creator_place_wall"
CREATOR_SAVE_MAP = "creato_save_map"


class SimulationWindow(BaseWindow):
    def sprites(self) -> None:
        # define sprites here
        pass

    def draw(self) -> None:
        pass

    def _execute_callback(self, type: str) -> None:
        func = self._callbacks.get(type, None)
        if func:
            func()

    def event(self, event) -> None:
        super().event(event)

        mouse_pos = py.mouse.get_pos()
        mouse_buttons = py.mouse.get_pressed()

        if event.type == py.KEYDOWN:
            # events when creator mode enabled
            # roboter movement
            if event.key == py.K_r:
                self._execute_callback(CREATOR_TOGGLE_ROBOT)

            # wall placement
            if event.key == py.K_p:
                self._execute_callback(CREATOR_PLACE_WALL)

            # save map
            if event.key == py.K_s:
                self._execute_callback(CREATOR_SAVE_MAP)
        
        if mouse_buttons[0]:
            func = self._callbacks.get(MOUSE_CLICK, None)
            if func:
                func(mouse_pos)