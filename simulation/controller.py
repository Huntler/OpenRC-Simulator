from typing import Tuple
from graphics.controller import BaseController
from graphics.objects.rectangle import Rectangle
from graphics.objects.robot import Robot
from graphics.objects.text import ANCHOR_CENTER, ANCHOR_TOP_LEFT, Text
from simulation import CREATOR, MANUAL, SIMULATION
from simulation.window import SimulationWindow
import pygame as py
import time


BACKGROUND_COLOR = (30, 35, 35)
MODE_TEXT_COLOR = (40, 45, 45)
SHORTCUT_TEXT_COLOR = (70, 75, 75)
ROBOT_COLOR = (160, 160, 200)
ROBOT_SIZE = 50


class SimulationController(BaseController):
    def __init__(self, window_size: Tuple[int, int], mode:int, flags: int = 0) -> None:
        """The SimulationController manages the SimulationWindow. This is a seperate 
        thread, than the pygame one.

        Args:
            window_size (Tuple[int, int]): Width and height of the window.
            flags (int, optional): Fullscreen, hardware acceleration, ... Defaults to 0.
        """
        super().__init__()

        self._width, self._height = window_size
        self._center = (self._width // 2, self._height // 2)
        self._flags = flags

        # create the window visuals
        self._window = SimulationWindow(window_size=window_size, flags=flags)
        self._surface = self._window.get_surface()

        # create the sprites we want to use
        # background object (just a colored box)
        background = Rectangle(self._surface, 0, 0, self._width, self._height, BACKGROUND_COLOR)
        self._window.add_sprite("background", background, zindex=99)

        self._robot = Robot(self._surface, ROBOT_SIZE * 2, self._height / 2 - ROBOT_SIZE, ROBOT_SIZE, ROBOT_COLOR)
        self._window.add_sprite("robot", self._robot)

        #keys = py.key.get_pressed()
        #print(keys)
        self.mode(mode)
    
    def mode(self, mode: int) -> None:
        """The applications mode (CREATOR, SIMULATION, MANUAL)

        Args:
            mode (int): The mode.
        """
        # TODO: if creator mode, then add edit bar
        cx, cy = self._center

        # show background text
        # text describing the current mode (integrated into the background)
        mode_text = ["SIMULATION", "CREATOR", "MANUAL"]
        text_mode = Text(self._surface, mode_text[mode], cx, cy, 120, MODE_TEXT_COLOR)
        self._window.add_sprite("text_mode", text_mode, zindex=98)

        if mode == CREATOR:
            # show shortcut info for CREATOR mode
            text_shortcuts = Text(self._surface, "Shortcuts", 0, 0, 50, SHORTCUT_TEXT_COLOR)
            text_shortcuts.set_position((20, self._height - 150), ANCHOR_TOP_LEFT)
            self._window.add_sprite("text_shortcuts_title", text_shortcuts, zindex=98)

            # robot movement
            text_robot = Text(self._surface, "'R' Move the Robot", 0, 0, 30, SHORTCUT_TEXT_COLOR)
            text_robot.set_position((20, self._height - 100), ANCHOR_TOP_LEFT)
            self._window.add_sprite("text_robot", text_robot, zindex=98)

            # wall placement
            text_robot = Text(self._surface, "'P' Start drawing a wall", 0, 0, 30, SHORTCUT_TEXT_COLOR)
            text_robot.set_position((20, self._height - 70), ANCHOR_TOP_LEFT)
            self._window.add_sprite("text_wall", text_robot, zindex=98)

            # save the current creation
            text_robot = Text(self._surface, "'S' Save the map", 0, 0, 30, SHORTCUT_TEXT_COLOR)
            text_robot.set_position((20, self._height - 40), ANCHOR_TOP_LEFT)
            self._window.add_sprite("text_save", text_robot, zindex=98)

        if mode == MANUAL:
            pass

        if mode == SIMULATION:
            pass

    def loop(self) -> None:
        pass
