import math
import pygame as py
from typing import Dict, Tuple
from pygame import Surface
from graphics.objects.robot import Robot
from graphics.objects.text import ANCHOR_TOP_LEFT, Text
from graphics.objects.wall import Wall
from graphics.sub_controller import BaseSubController
from simulation import CREATOR, SHORTCUT_TEXT_COLOR, SHORTCUT_TEXT_COLOR_ACTIVE
from simulation.window import CREATOR_PLACE_WALL, MOUSE_CLICK, SimulationWindow
from threading import Lock


WALL_COLOR = (255, 120, 120)
WALL_THICKNESS = 11
SNAP_THRESHOLD = 25


class WallController(BaseSubController):
    def __init__(self, window: SimulationWindow, app_mode: int) -> None:
        super().__init__()
        self._app_mode = app_mode
        self.dict_name = "walls"
        
        # window and surface information
        self._window = window
        self._ww, self._wh = window.get_window_size()
        self._surface = window.get_surface()

        # wall sprites
        self._walls = []
        self._active_wall = None

        # wall placement shortcuts
        if app_mode == CREATOR:
            self._text_wall = Text(self._surface, "'P' Start drawing a wall", 0, 0, 30, SHORTCUT_TEXT_COLOR)
            self._text_wall.set_position((20, self._wh - 100), ANCHOR_TOP_LEFT)

            self._window.add_sprite("text_wall", self._text_wall)
            self._window.on_callback(CREATOR_PLACE_WALL, self.toggle)

    def toggle(self, call: bool = True) -> None:
        super().toggle(call)

        if self.is_toggled():
            self._window.on_callback(MOUSE_CLICK, self._on_mouse_click)
            self._text_wall.set_color(SHORTCUT_TEXT_COLOR_ACTIVE)

        else:
            self._window.remove_callback(MOUSE_CLICK)
            self._text_wall.set_color(SHORTCUT_TEXT_COLOR)

            # remove the latest wall which is never finished
            if self._active_wall:
                wall_index = len(self._walls)
                self._walls.remove(self._active_wall)
                self._window.remove_sprite(f"sprite_wall_{wall_index}")

                self._active_wall = None
            
    def _new_wall(self, pos: Tuple[int, int]) -> Wall:
        """Method adds a new wall to the set of walls.
        """
        wall = Wall(self._surface, pos, pos, WALL_COLOR, WALL_THICKNESS)
        self._walls.append(wall)
        self._window.add_sprite(f"sprite_wall_{len(self._walls)}", wall, zindex=2)

        self._active_wall = wall
        
    def _on_mouse_click(self, pos: Tuple[int, int]) -> None:
        if self.is_toggled():
            if not self._active_wall:
                self._new_wall(pos)

                # set start point of last added wall
                self._start_point_set = True
                pos = self._snap(pos)
                self._active_wall.set_start(pos)
            else:
                # set end point of last added wall
                pos = self._snap(pos)
                self._active_wall.set_end(pos)

                # create a new wall to continue
                self._new_wall(pos)
                self._active_wall.set_start(pos)

    def _snap(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """This method snaps a position to a wall's position given some threshold.

        Args:
            pos (Tuple[int, int]): The position, which can be snapped.

        Returns:
            Tuple[int, int]: The snapped or original position.
        """
        x, y = pos
        for wall in self._walls[:-1]:
            wx, wy = wall.get_start()
            distance = math.hypot(x - wx, y - wy)

            if distance <= SNAP_THRESHOLD:
                return (wx, wy)

            wx, wy = wall.get_end()
            distance = math.hypot(x - wx, y - wy)

            if distance <= SNAP_THRESHOLD:
                return (wx, wy)
        
        return pos

    def app_mode(self, mode: int) -> None:
        self._app_mode = mode
    
    def loop(self) -> None:
        # draw the latest wall from the last click position to the current
        # cursor position
        if self.is_toggled():
            mouse_pos = py.mouse.get_pos()
            snap_pos = self._snap(mouse_pos)
            if self._active_wall:
                self._active_wall.set_end(snap_pos)
    
    def to_dict(self) -> Dict:
        dict_file = {}
        
        for i, wall in enumerate(self._walls):
            sx, sy = wall.get_start()
            ex, ey = wall.get_end()
            name = f"sprite_wall_{i + 1}"
            dict_file[name] = {}
            dict_file[name]["start_x"] = sx
            dict_file[name]["start_y"] = sy
            dict_file[name]["end_x"] = ex
            dict_file[name]["end_y"] = ey
        
        final_dict = {}
        final_dict["walls"] = dict_file
        return final_dict
    
    def from_dict(self, d: Dict) -> None:
        for wall_name in d.keys():
            wall_dict = d[wall_name]
            start_pos = (wall_dict["start_x"], wall_dict["start_y"])
            end_pos = (wall_dict["end_x"], wall_dict["end_y"])

            wall = Wall(self._surface, start_pos, end_pos, WALL_COLOR, WALL_THICKNESS)
            self._walls.append(wall)
            self._window.add_sprite(wall_name, wall, zindex=2)
