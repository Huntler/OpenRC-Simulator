from typing import Tuple
import yaml
import pickle
import numpy as np
from algorithm.robot_population import RobotPopulation
from commander.sub_controller.robot_controller import ROBOT_SIZE
from simulation.robot import Robot
from simulation.wall import Wall


class Map:
    def __init__(self, name: str) -> None:
        self.__ea = None
        self.__config_name = ""

        # open map file
        with open(f"maps/{name}.yaml", "r") as file:
            dict_file: dict = yaml.load(file, Loader=yaml.FullLoader)

        # load robot
        robot_dict = dict_file.get(Robot.dict_name, None)
        self.__robots = [Robot(np.array([robot_dict["x"], robot_dict["y"]]), ROBOT_SIZE, robot_dict["direction"])]

        # load all walls
        self.__walls = []
        walls_dict: dict = dict_file.get(Wall.dict_name, None)
        for wall in walls_dict.items():
            wall = wall[1]
            start_pos = (wall["start_x"], wall["start_y"])
            end_pos = (wall["end_x"], wall["end_y"])
            self.__walls.append(Wall(start_pos, end_pos))
    
    def load_training_config(self, config_name) -> None:
        # copy the robots so they match the population's size
        with open(f"ea_configs/{config_name}.yaml", "r") as file:
            dict_file: dict = yaml.load(file, Loader=yaml.FullLoader)

        self.__ea = RobotPopulation(**dict_file)
        self.__config_name = config_name

    def ea_train(self) -> None:
        # train
        population, generation = self.__ea.run_evolution()

        # store the best robot
        filehandler = open(f"robot_{self.__config_name}.pkl", 'w') 
        pickle.dump(population[0], filehandler)
