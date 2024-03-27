"""This module communicates between the car's simulation and the car's 
visualization."""
import math
from time import sleep
from typing import Dict, Tuple
import numpy as np
from OpenRCSimulator.graphics.callback import MouseListener
from OpenRCSimulator.graphics.window import MUTEX
from OpenRCSimulator.simulation.openrc import OpenRC
from OpenRCSimulator.simulation import CHASSIS_SIZE
from OpenRCSimulator.graphics.objects.car import Car
from OpenRCSimulator.graphics.sub_controller import BaseSubController
from OpenRCSimulator.gui import CREATOR, GARAGE, SIMULATION
from OpenRCSimulator.gui.window import MainWindow


ON, OFF = 1, 0
FORWARD, BACKWARD = 2, 3


class CarController(BaseSubController, MouseListener):
    """This controller class connects the car's simulation and visualization. Also,
    it enables manual control over the car, if the app_mode is 'MANUAL' (int = 2).

    Args:
        BaseSubController (BaseSubController): Base class.
        MouseListener (MouseListener): The controller reacts on mouse events.
    """
    def __init__(self, window: MainWindow, app_mode: int) -> None:
        super().__init__()
        self._app_mode = app_mode
        self.dict_name = "car"
        self._is_paused = False

        self._car = OpenRC(np.array([-CHASSIS_SIZE[0] * 2, -CHASSIS_SIZE[1] * 2]))
        # accelerate, backwards, break, left, right
        self._controls = np.array([False, False, False, False, False])

        # window and surface information
        self._window = window
        self._ww, self._wh = window.get_window_size()
        self._surface = window.get_surface()
        self._sensor_font = window.get_font().copy(size=12)

        # car sprite
        car_mode = Car.CONFIG if self._app_mode == GARAGE else Car.NORMAL
        self._sprite_car = Car(
            self._surface, -CHASSIS_SIZE[0] * 2, -CHASSIS_SIZE[1] * 2, CHASSIS_SIZE,
            self._sensor_font, car_mode)
        self._window.add_sprite("sprite_car", self._sprite_car)
        self._sprite_position_set = True

    def accelerate(self):
        """This method calls the simulation to accelerate the car.
        """
        self._controls[0] = not self._controls[0]

    def slowdown(self):
        """This method calls the simulation to slowdown the car.
        """
        self._controls[1] = not self._controls[1]

    def turn_left(self):
        """This method calls the simulation to turn the car left.
        """
        self._controls[3] = not self._controls[3]

    def turn_right(self):
        """This method calls the simulation to trun the car right.
        """
        self._controls[4] = not self._controls[4]

    def stop(self):
        """This method calls the simulation to stop the car.
        """
        self._controls[2] = not self._controls[2]

    def pause(self) -> None:
        """This method pauses the simulation.
        """
        self._is_paused = not self._is_paused

    def toggle(self, call: bool = True) -> None:
        """This method toggles a special mode for this controller. In CREATOR mode, the car's 
        position can be changed.

        Args:
            call (bool, optional): If false, then the registered callback is not 
            executed. Defaults to True.
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
            angle = math.atan2(position[1] - self._sprite_car.get_position()[
                               1], position[0] - self._sprite_car.get_position()[0])
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
        position = (d["x"], d["y"])
        direction = d["direction"]

        self._sprite_car.set_position(position)
        self._sprite_car.set_direction(direction)

        self._car = OpenRC(np.array([d["x"], d["y"]], dtype=float))

    def loop(self, delta, lines) -> None:
        """
        This loop is always executed by the main controller.
        """

        if self._app_mode != CREATOR:
            # get the simulations info about the car and update the sprite
            if self._is_paused:
                delta = 0
            
            # run the simulation
            self._car.set_time_delta(delta)
            walls = [[line.get_start(), line.get_end()] for line in lines]
            angle, x, y, sensor_lines, distances = self._car.drive(walls, self._controls)

            # update the car's position
            self._sprite_car.set_position((x, y))
            self._sprite_car.set_direction(angle)
            self._sprite_car.set_sensors(sensor_lines)
            self._sprite_car.set_distances(distances)

        if self._app_mode == SIMULATION:
            # pass through the sensors to the trained robocart and use its decision
            # to controll the car
            print("Simulation not implemented. WIP")
