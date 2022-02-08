from typing import Tuple
from graphics.controller import BaseController
from graphics.objects.rectangle import Rectangle
from graphics.objects.robot import Robot
from simulation.window import SimulationWindow
import pygame as py
import time


BACKGROUND_COLOR = (30, 35, 35)
ROBOT_COLOR = (160, 160, 200)
ROBOT_SIZE = 50


class SimulationController(BaseController):
    def __init__(self, window_size: Tuple[int, int], flags: int = 0) -> None:
        """The SimulationController manages the SimulationWindow. This is a seperate 
        thread, than the pygame one.

        Args:
            window_size (Tuple[int, int]): Width and height of the window.
            flags (int, optional): Fullscreen, hardware acceleration, ... Defaults to 0.
        """
        super().__init__()

        self._width, self._height = window_size
        self._flags = flags

        # create the window visuals
        self._window = SimulationWindow(window_size=window_size, flags=flags)
        surface = self._window.get_surface()

        # create the sprites we want to use
        background = Rectangle(surface, 0, 0, self._width, self._height, BACKGROUND_COLOR)
        self._window.add_sprite("background", background, zindex=99)

        self._robot = Robot(surface, ROBOT_SIZE * 2, self._height / 2 - ROBOT_SIZE, ROBOT_SIZE, ROBOT_COLOR)
        self._window.add_sprite("robot", self._robot)

        #keys = py.key.get_pressed()
        #print(keys)
    
    def mode(self, mode: int) -> None:
        """The applications mode (CREATOR, SIMULATION, MANUAL)

        Args:
            mode (int): The mode.
        """
        # TODO: if creator mode, then add edit bar
        pass

    def loop(self) -> None:
        pass
