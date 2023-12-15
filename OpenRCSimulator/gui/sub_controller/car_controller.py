import math
from time import sleep
import numpy as np
import pygame as py
from typing import Dict, Tuple
from OpenRCSimulator.graphics.callback import MouseListener
from OpenRCSimulator.graphics.window import MUTEX
from OpenRCSimulator.simulation.openrc import OpenRC
from OpenRCSimulator.simulation import CHASSIS_SIZE
from OpenRCSimulator.graphics.objects.car import Car
from OpenRCSimulator.graphics.sub_controller import BaseSubController
from OpenRCSimulator.gui import CREATOR, GARAGE, SIMULATION
from OpenRCSimulator.gui.window import MOUSE_CLICK, MainWindow


ON, OFF = 1, 0
FORWARD, BACKWARD = 2, 3


class CarController(BaseSubController, MouseListener):
    def __init__(self, window: MainWindow, app_mode: int) -> None:
        super().__init__()
        self._app_mode = app_mode
        self.dict_name = "car"
        self._is_paused = False

        self._car = OpenRC(np.array([-CHASSIS_SIZE[0] * 2, -CHASSIS_SIZE[1] * 2]))

        # window and surface information
        self._window = window
        self._ww, self._wh = window.get_window_size()
        self._surface = window.get_surface()
        self._sensor_font = window.get_font().copy(size=12)

        # car sprite
        car_mode = Car.CONFIG if self._app_mode == GARAGE else Car.NORMAL
        self._sprite_car = Car(self._surface, -CHASSIS_SIZE[0] * 2, -CHASSIS_SIZE[1] * 2, CHASSIS_SIZE, self._sensor_font, car_mode)
        self._window.add_sprite("sprite_car", self._sprite_car)
        self._sprite_position_set = True

    def accelerate(self):
        with MUTEX:
            self._car.accelerate()
    
    def slowdown(self):
        with MUTEX:
            self._car.slowdown()

    def turn_left(self):
        with MUTEX:
            self._car.turn_left()

    def turn_right(self):
        with MUTEX:
            self._car.turn_right()
    
    def stop(self):
        with MUTEX:
            self._car.reset_acceleration()
            self._car.reset_turn()


    def set_brain(self, genome) -> None:
        # TODO
        pass

    def pause(self) -> None:
        self._is_paused = not self._is_paused

    def toggle(self, call: bool = True) -> None:
        """This method toggles a special mode for this controller. In CREATOR mode, the car's 
        position can be changed.

        Args:
            call (bool, optional): If false, then the registered callback is not executed. Defaults to True.
        """
        super().toggle(call)

        if self._toggled:
            self._window.set_listener(self)
            self._sprite_position_set = False

        else:
            self._window.remove_listener(self)

    def on_click(self, buttons: Tuple[bool, bool, bool], position: Tuple[int, int]) -> None:
        if not self._sprite_position_set:
            self._sprite_position_set = True
        else:
            self.toggle()
        sleep(0.2)
    
    def on_movement(self, position: Tuple[int, int], delta: Tuple[int, int]) -> None:
        if self.is_toggled():
            # set position
            if not self._sprite_position_set:
                self._sprite_car.set_position(position)

            # set angle to mouse
            angle = math.atan2(position[1] - self._sprite_car.get_position()[1], position[0] - self._sprite_car.get_position()[0])
            self._sprite_car.set_direction(angle)

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


        
