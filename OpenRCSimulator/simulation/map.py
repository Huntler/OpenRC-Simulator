"""This module handles the loading and definition of a map."""
import yaml
import numpy as np

from OpenRCSimulator.state import get_data_folder, MAPS_FOLDER
from OpenRCSimulator.simulation.openrc import OpenRC
from OpenRCSimulator.simulation.wall import Wall


class Map:
    """A map is loaded from the app's MAP_FOLDER and contains the window's dimension,
    the wall's and the car's position.
    """
    def __init__(self, name: str) -> None:
        self.__map_name = name

        self.__car = None
        self.__walls = []

        self.__width = 0
        self.__height = 0

    def _load_map(self) -> None:
        path = f"{get_data_folder(MAPS_FOLDER)}{self.__map_name}.yaml"
        with open(path, "r", encoding="UTF-8") as file:
            dict_file: dict = yaml.load(file, Loader=yaml.FullLoader)

        # load car location/direction from map info
        robot_dict = dict_file.get(OpenRC.dict_name, None)
        self.__car = OpenRC(
            np.array([robot_dict["x"], robot_dict["y"]]), robot_dict["direction"])

        # load all walls
        self.__walls = []
        walls_dict: dict = dict_file.get(Wall.dict_name, None)
        for wall in walls_dict.items():
            wall = wall[1]
            start_pos = (wall["start_x"], wall["start_y"])
            end_pos = (wall["end_x"], wall["end_y"])
            self.__walls.append(Wall(start_pos, end_pos))

        # load width, height
        size_dict = dict_file.get("app", None)
        self.__width = size_dict["width"]
        self.__height = size_dict["height"]

    @property
    def walls(self):
        return self.__walls

    @property
    def car(self):
        return self.__car

    @property
    def map_size(self):
        return [self.__width, self.__height]
