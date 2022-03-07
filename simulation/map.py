from typing import Tuple
import yaml
from commander.sub_controller.robot_controller import ROBOT_SIZE
from simulation.robot import Robot
from simulation.wall import Wall


class Map:
    def __init__(self, name: str) -> None:
        # open map file
        with open(f"maps/{name}.yaml", "r") as file:
            dict_file: dict = yaml.load(file, Loader=yaml.FullLoader)

        # load robot
        robot_dict = dict_file.get(Robot.dict_name, None)
        self.__robots = [Robot(pixel_pos=(robot_dict["x"], robot_dict["y"], ROBOT_SIZE, robot_dict["direction"]))]

        # load all walls
        self.__walls = []
        walls_dict: dict = dict_file.get(Wall.dict_name, None)
        for wall in walls_dict.items():
            start_pos = (wall["start_x"], wall["start_y"])
            end_pos = (wall["end_x"], wall["end_y"])
            self.__walls.append(Wall(start_pos, end_pos))
    
    def load_training_config(self, config_name) -> None:
        # copy the robots so they match the population's size
        pass

    def ea_train(self) -> None:
        pass