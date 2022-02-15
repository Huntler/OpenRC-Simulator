from graphics.window import BaseWindow
import pygame as py


MOUSE_CLICK = "mouse_click"
SHORTCUTS_UNTOGGLE = "untoggle_all"

CREATOR_PLACE_ROBOT = "creator_place_robot"
CREATOR_PLACE_GOAL = "creator_place_goal"
CREATOR_PLACE_WALL= "creator_place_wall"
CREATOR_SAVE_MAP = "creato_save_map"

MANUAL_LEFT_INCREASE = "left_increase"
MANUAL_LEFT_DECREASE = "left_decrease"
MANUAL_RIGHT_INCREASE = "right_increase"
MANUAL_RIGHT_DECREASE = "right_decrease"
MANUAL_BOTH_INCREASE = "both_increase"
MANUAL_BOTH_DECREASE = "both_decrease"
MANUAL_BOTH_ZERO = "both_zero"

SIMULATION_PAUSE = "pause"


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
                self._execute_callback(CREATOR_PLACE_ROBOT)

            # wall placement
            if event.key == py.K_p:
                self._execute_callback(CREATOR_PLACE_WALL)
                self._execute_callback(SIMULATION_PAUSE)

            # save map
            if event.key == py.K_s:
                self._execute_callback(MANUAL_LEFT_DECREASE)
                self._execute_callback(CREATOR_SAVE_MAP)
            
            # untoggle all
            if event.key == py.K_ESCAPE:
                self._execute_callback(SHORTCUTS_UNTOGGLE)
            
            if event.key == py.K_o:
                self._execute_callback(MANUAL_RIGHT_INCREASE)
            
            if event.key == py.K_l:
                self._execute_callback(MANUAL_RIGHT_DECREASE)

            if event.key == py.K_w:
                self._execute_callback(MANUAL_LEFT_INCREASE)
            
            if event.key == py.K_t:
                self._execute_callback(MANUAL_BOTH_INCREASE)
            
            if event.key == py.K_g:
                self._execute_callback(MANUAL_BOTH_DECREASE)

            if event.key == py.K_x:
                self._execute_callback(MANUAL_BOTH_ZERO)
        
        if mouse_buttons[0]:
            func = self._callbacks.get(MOUSE_CLICK, None)
            if func:
                func(mouse_pos)