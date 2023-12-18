"""This module controlls the wall's visualization."""
import math
from typing import Dict, Tuple, List
from OpenRCSimulator.graphics.callback import MouseListener
from OpenRCSimulator.graphics.objects.wall import Wall
from OpenRCSimulator.graphics.sub_controller import BaseSubController
from OpenRCSimulator.gui.window import MainWindow


WALL_COLOR = (255, 120, 120)
WALL_THICKNESS = 11
SNAP_THRESHOLD = 25


class WallController(BaseSubController, MouseListener):
    """The wall controller manages wall placement and beahviour.

    Args:
        BaseSubController (BaseSubController): the base controller calls.
        MouseListener (MouseListener): The class reacts to mouse events.
    """

    def __init__(self, window: MainWindow, app_mode: int) -> None:
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

    def get_walls(self) -> List:
        """This method returns the walls as a List to be further processed.

        Returns:
            walls (List): The list of walls.
        """
        return self._walls

    def toggle(self, call: bool = True) -> None:
        super().toggle(call)

        if self.is_toggled():
            self._window.set_listener(self)
        else:
            self._window.remove_listener(self)

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
        self._window.add_sprite(
            f"sprite_wall_{len(self._walls)}", wall, zindex=2)

        self._active_wall = wall

    def on_click(self, buttons: Tuple[bool, bool, bool], position: Tuple[int, int]) -> None:
        if self.is_toggled() and buttons[0]:
            if not self._active_wall:
                self._new_wall(position)

                # set start point of last added wall
                pos = self._snap(position)
                self._active_wall.set_start(pos)
            else:
                # set end point of last added wall
                pos = self._snap(position)
                self._active_wall.set_end(pos)

                # create a new wall to continue
                self._new_wall(pos)
                self._active_wall.set_start(pos)

    def on_movement(self, position: Tuple[int, int], delta: Tuple[int, int]) -> None:
        # draw the latest wall from the last click position to the current
        # cursor position
        if self.is_toggled():
            snap_pos = self._snap(position)
            if self._active_wall:
                self._active_wall.set_end(snap_pos)

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
        """Defines the controller mode.

        Args:
            mode (int): Mode (CREATOR = 1) the walls can be placed, (SIMULATION = 0) 
            the walls are oonly displayed.
        """
        self._app_mode = mode

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

            wall = Wall(self._surface, start_pos, end_pos,
                        WALL_COLOR, WALL_THICKNESS)
            self._walls.append(wall)
            self._window.add_sprite(wall_name, wall, zindex=2)
