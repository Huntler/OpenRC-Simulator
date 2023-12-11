from typing import List
import yaml

from OpenRCSimulator.simulation.map import Map


class Trainer:
    def __init__(self, config_name: str, map_name: str = None) -> None:
        self.__config_name = config_name
        self.__map_name = map_name
    
    def _load_config(self) -> None:
        with open(f"configs/{self.__config_name}.yaml", "r") as file:
            dict_file: dict = yaml.load(file, Loader=yaml.FullLoader)

    def _get_maps(self) -> List[str]:
        """
        Get map names of files located in 'maps/'
        """
        import os
        return [name.replace(".yaml", "") for name in os.listdir("maps")]

    def train_map(self, map_name: str):
        map = Map(map_name)

        # TODO: RL here

    def train(self) -> None:
        import random

        # map specified, only training specific map
        if self.__map_name:
            self.train_map(self.__map_name)
            return
    
        # get all maps to train on
        map_names = self._get_maps()

        # TODO: adjust training parameters based on number of maps (e.g. epochs to play / number of maps)

        for i in random.sample(range(0, len(map_names)), len(map_names)):
            self.train_map(map_names[i])


    
