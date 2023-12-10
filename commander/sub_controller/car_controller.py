import math
from time import sleep
import numpy as np
import pygame as py
from typing import Dict, Tuple
from pygame import Surface
from graphics.window import MUTEX
from simulation.openrc import OpenRC
from simulation import CHASSIS_SIZE
from graphics.objects.car import Car
from graphics.objects.text import ANCHOR_TOP_LEFT, Text
from graphics.sub_controller import BaseSubController
from commander import CREATOR, MANUAL, SHORTCUT_TEXT_COLOR, SHORTCUT_TEXT_COLOR_ACTIVE, SIMULATION
from commander.window import CREATOR_PLACE_CAR, MANUAL_BOTH_DECREASE, MANUAL_BOTH_INCREASE, MANUAL_BOTH_ZERO, \
    MANUAL_LEFT_DECREASE, MANUAL_LEFT_INCREASE, MANUAL_RIGHT_DECREASE, MANUAL_RIGHT_INCREASE, MOUSE_CLICK, \
    SIMULATION_PAUSE, SimulationWindow



class CarController(BaseSubController):
    def __init__(self, window: SimulationWindow, app_mode: int, font) -> None:
        super().__init__()
        self._app_mode = app_mode
        self.dict_name = "car"
        self._is_paused = False

        self._car = OpenRC(np.array([-CHASSIS_SIZE[0] * 2, -CHASSIS_SIZE[1] * 2]))

        # window and surface information
        self._window = window
        self._ww, self._wh = window.get_window_size()
        self._surface = window.get_surface()
        self._font = font

        # car sprite
        self._sprite_car = Car(self._surface, -CHASSIS_SIZE[0] * 2, -CHASSIS_SIZE[1] * 2, CHASSIS_SIZE, font)
        self._window.add_sprite("sprite_car", self._sprite_car)
        self._sprite_position_set = True

        # car placement shortcuts
        if app_mode == CREATOR:
            self._text_car = Text(self._surface, "'R' Place the car", 0, 0, 30, SHORTCUT_TEXT_COLOR)
            self._text_car.set_position((20, self._wh - 130), ANCHOR_TOP_LEFT)
            self._window.add_sprite("text_car", self._text_car)
            self._window.on_callback(CREATOR_PLACE_CAR, self.toggle)

        if app_mode == MANUAL:
            self._is_paused = False
            self._text_car = Text(self._surface, "'P' Pause simulation", 0, 0, 30, SHORTCUT_TEXT_COLOR)
            self._text_car.set_position((20, self._wh - 50), ANCHOR_TOP_LEFT)
            self._window.add_sprite("text_car", self._text_car)
            self._window.on_callback(SIMULATION_PAUSE, self._pause)

            self._window.on_callback(MANUAL_LEFT_INCREASE, self._motor_left(1))
            self._window.on_callback(MANUAL_LEFT_DECREASE, self._motor_left(-1))
            self._window.on_callback(MANUAL_RIGHT_INCREASE, self._motor_right(1))
            self._window.on_callback(MANUAL_RIGHT_DECREASE, self._motor_right(-1))
            self._window.on_callback(MANUAL_BOTH_INCREASE, self._motors_both(1, 1))
            self._window.on_callback(MANUAL_BOTH_DECREASE, self._motors_both(-1, -1))
            self._window.on_callback(MANUAL_BOTH_ZERO, self._motors_both(0, 0))

    def set_brain(self, genome) -> None:
        # TODO
        pass

    def _motor_left(self, left: int):
        def fire():
            with MUTEX:
                if left == -1:
                    self._car.slowdown_left()
                if left == 1:
                    self._car.accelerate_left()

        return fire

    def _motor_right(self, right: int):
        def fire():
            with MUTEX:
                if right == -1:
                    self._car.slowdown_right()
                if right == 1:
                    self._car.accelerate_right()

        return fire

    def _motors_both(self, left: int, right: int):
        def fire():
            if left == right and left == 0:
                self._car.stop()
                return

            self._motor_left(left)()
            self._motor_right(right)()

        return fire

    def _pause(self) -> None:
        self._is_paused = not self._is_paused

    def toggle(self, call: bool = True) -> None:
        """This method toggles a special mode for this controller. In CREATOR mode, the car's 
        position can be changed.

        Args:
            call (bool, optional): If false, then the registered callback is not executed. Defaults to True.
        """
        super().toggle(call)

        if self._toggled:
            self._window.on_callback(MOUSE_CLICK, self._on_mouse_click)
            self._text_car.set_color(SHORTCUT_TEXT_COLOR_ACTIVE)
            self._sprite_position_set = False

        else:
            self._window.remove_callback(MOUSE_CLICK)
            self._text_car.set_color(SHORTCUT_TEXT_COLOR)

    def _on_mouse_click(self, pos: Tuple[int, int]) -> None:
        """This method is executed, if the event was registered from inside this controller.

        Args:
            pos (Tuple[int, int]): The mouse position.
        """
        if not self._sprite_position_set:
            self._sprite_position_set = True
        else:
            self.toggle()
        sleep(0.2)

    def to_dict(self) -> Dict:
        x, y = self._sprite_car.get_position()
        dict_file = {}
        dict_file["car"] = {}
        dict_file["car"]["x"] = x
        dict_file["car"]["y"] = y
        dict_file["car"]["direction"] = self._sprite_car.get_direction()
        return dict_file

    def from_dict(self, d: Dict) -> None:
        pos = (d["x"], d["y"])
        dir = d["direction"]

        self._sprite_car.set_position(pos)
        self._sprite_car.set_direction(dir)

        self._car = OpenRC(np.array([d["x"], d["y"]], dtype=float))

    def loop(self, delta, lines) -> None:
        """
        This loop is always executed by the main controller.
        """
        if self.is_toggled():
            mouse_pos = py.mouse.get_pos()

            # set position
            if not self._sprite_position_set:
                self._sprite_car.set_position(mouse_pos)

            # set angle to mouse
            angle = math.atan2(mouse_pos[1] - self._sprite_car.get_position()[1], mouse_pos[0] - self._sprite_car.get_position()[0])
            self._sprite_car.set_direction(angle)
        
        if self._app_mode != CREATOR:
            # get the simulations info about the car and update the sprite
            if self._is_paused:
                delta = 0

            self._car.set_time_delta(delta)
            walls = [[line.get_start(), line.get_end()] for line in lines]
            angle, x, y, sensor_lines, distances = self._car.drive(walls)

            self._sprite_car.set_position((x, y))
            self._sprite_car.set_direction(angle)
            self._sprite_car.set_sensors(sensor_lines)
            self._sprite_car.set_distances(distances)
            
        if self._app_mode == SIMULATION:
            # pass through the sensors to the trained robocart and use its decision to controll the car
            pass


        
