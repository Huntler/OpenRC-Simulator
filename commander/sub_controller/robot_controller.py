import numpy as np
import pygame as py
from typing import Dict, Tuple
from pygame import Surface
from algorithm.robot_genome import RobotGenome
from graphics.window import MUTEX
from simulation.robot import Robot as SimRobot
from graphics.objects.robot import Robot
from graphics.objects.text import ANCHOR_TOP_LEFT, Text
from graphics.sub_controller import BaseSubController
from commander import CREATOR, MANUAL, SHORTCUT_TEXT_COLOR, SHORTCUT_TEXT_COLOR_ACTIVE, SIMULATION
from commander.window import CREATOR_PLACE_ROBOT, MANUAL_BOTH_DECREASE, MANUAL_BOTH_INCREASE, MANUAL_BOTH_ZERO, \
    MANUAL_LEFT_DECREASE, MANUAL_LEFT_INCREASE, MANUAL_RIGHT_DECREASE, MANUAL_RIGHT_INCREASE, MOUSE_CLICK, \
    SIMULATION_PAUSE, SimulationWindow

ROBOT_COLOR = (160, 160, 200)
ROBOT_SIZE = 50


class RobotController(BaseSubController):
    def __init__(self, window: SimulationWindow, app_mode: int, font) -> None:
        super().__init__()
        self._app_mode = app_mode
        self.dict_name = "robot"
        self._is_paused = True

        self._robot = SimRobot(np.array([-ROBOT_SIZE * 2, -ROBOT_SIZE * 2], dtype=float), ROBOT_SIZE)

        # window and surface information
        self._window = window
        self._ww, self._wh = window.get_window_size()
        self._surface = window.get_surface()
        self._font = font

        # robot sprite
        self._sprite_robot = Robot(self._surface, -ROBOT_SIZE * 2, -ROBOT_SIZE * 2, ROBOT_SIZE, ROBOT_COLOR, font)
        self._window.add_sprite("sprite_robot", self._sprite_robot)

        # robot placement shortcuts
        if app_mode == CREATOR:
            self._text_robot = Text(self._surface, "'R' Place the robot", 0, 0, 30, SHORTCUT_TEXT_COLOR)
            self._text_robot.set_position((20, self._wh - 130), ANCHOR_TOP_LEFT)
            self._window.add_sprite("text_robot", self._text_robot)
            self._window.on_callback(CREATOR_PLACE_ROBOT, self.toggle)

        if app_mode == MANUAL:
            self._is_paused = False
            self._text_robot = Text(self._surface, "'P' Pause simulation", 0, 0, 30, SHORTCUT_TEXT_COLOR)
            self._text_robot.set_position((20, self._wh - 50), ANCHOR_TOP_LEFT)
            self._window.add_sprite("text_robot", self._text_robot)
            self._window.on_callback(SIMULATION_PAUSE, self._pause)

            self._window.on_callback(MANUAL_LEFT_INCREASE, self._motor_left(1))
            self._window.on_callback(MANUAL_LEFT_DECREASE, self._motor_left(-1))
            self._window.on_callback(MANUAL_RIGHT_INCREASE, self._motor_right(1))
            self._window.on_callback(MANUAL_RIGHT_DECREASE, self._motor_right(-1))
            self._window.on_callback(MANUAL_BOTH_INCREASE, self._motors_both(1, 1))
            self._window.on_callback(MANUAL_BOTH_DECREASE, self._motors_both(-1, -1))
            self._window.on_callback(MANUAL_BOTH_ZERO, self._motors_both(0, 0))

    def set_brain(self, genome: RobotGenome) -> None:
        self._genome = genome

    def _motor_left(self, left: int):
        def fire():
            with MUTEX:
                if left == -1:
                    self._robot.slowdown_left()
                if left == 1:
                    self._robot.accelerate_left()

        return fire

    def _motor_right(self, right: int):
        def fire():
            with MUTEX:
                if right == -1:
                    self._robot.slowdown_right()
                if right == 1:
                    self._robot.accelerate_right()

        return fire

    def _motors_both(self, left: int, right: int):
        def fire():
            if left == right and left == 0:
                self._robot.stop()
                return

            self._motor_left(left)()
            self._motor_right(right)()

        return fire

    def _pause(self) -> None:
        self._is_paused = not self._is_paused

    def toggle(self, call: bool = True) -> None:
        """This method toggles a special mode for this controller. In CREATOR mode, the robot's 
        position can be changed.

        Args:
            call (bool, optional): If false, then the registered callback is not executed. Defaults to True.
        """
        super().toggle(call)

        if self._toggled:
            self._window.on_callback(MOUSE_CLICK, self._on_mouse_click)
            self._text_robot.set_color(SHORTCUT_TEXT_COLOR_ACTIVE)

        else:
            self._window.remove_callback(MOUSE_CLICK)
            self._text_robot.set_color(SHORTCUT_TEXT_COLOR)

    def _on_mouse_click(self, pos: Tuple[int, int]) -> None:
        """This method is executed, if the event was registered from inside this controller.

        Args:
            pos (Tuple[int, int]): The mouse position.
        """
        self._sprite_robot.set_position(pos)
        self.toggle()

    def to_dict(self) -> Dict:
        x, y = self._sprite_robot.get_position()
        dict_file = {}
        dict_file["robot"] = {}
        dict_file["robot"]["x"] = x
        dict_file["robot"]["y"] = y
        dict_file["robot"]["direction"] = self._sprite_robot.get_direction()
        return dict_file

    def from_dict(self, d: Dict) -> None:
        pos = (d["x"], d["y"])
        dir = d["direction"]

        self._sprite_robot.set_position(pos)
        self._sprite_robot.set_direction(dir)

        self._robot = SimRobot(np.array([d["x"], d["y"]], dtype=float), ROBOT_SIZE)

    def loop(self, delta, lines) -> None:
        """
        This loop is always executed by the main controller.
        """
        if self.is_toggled():
            mouse_pos = py.mouse.get_pos()
            self._sprite_robot.set_position(mouse_pos)
        
        if self._app_mode == SIMULATION:
            # pass through the sensors to the trained robot and use its decision to controll the robot
            left_wheel, right_wheel = self._genome.drive(sensor_lines)
            self._motors_both(left_wheel, right_wheel)

        if self._app_mode != CREATOR:
            # get the simulations info about the robot and update the sprite
            if self._is_paused:
                delta = 0

            self._robot.set_time_delta(delta)
            walls = [[line.get_start(), line.get_end()] for line in lines]
            angle, x, y, sensor_lines, distances = self._robot.drive(walls)

            self._sprite_robot.set_position((x, y))
            self._sprite_robot.set_direction(angle)
            self._sprite_robot.set_sensors(sensor_lines)
            self._sprite_robot.set_distances(distances)
        
