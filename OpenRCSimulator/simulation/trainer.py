"""This module handles the training of an agent"""
from typing import List
import os
import random
import yaml

from OpenRCSimulator.state import get_data_folder, CONFIGS_FOLDER, MAPS_FOLDER
from OpenRCSimulator.simulation.map import Map


class Trainer:
    """The Trainer class trains an agent on a specific map or randomly on a set of maps.
    """

    def __init__(self, config_name: str, map_name: str = None) -> None:
        self.__config_name = config_name
        self.__map_name = map_name

    def _load_config(self) -> None:
        path = f"{get_data_folder(CONFIGS_FOLDER)}{self.__config_name}.yaml"
        with open(path, "r", encoding="UTF-8") as file:
            # Configure this class [todo]
            _ = yaml.load(file, Loader=yaml.FullLoader)

    def _get_maps(self) -> List[str]:
        """
        Get map names of files located in 'maps/'
        """
        return [name.replace(".yaml", "") for name in os.listdir(get_data_folder(MAPS_FOLDER))]

    def train_map(self, map_name: str):
        """This method trains the agent on a given map.

        Args:
            map_name (str): The map to train on.
        """
        # Train an agent on this map [todo]
        _ = Map(map_name)

    def train(self) -> None:
        """This method trains the agent on a set of maps randomly. The set includes all
        maps available in the app's MAP_FOLDER.
        """
        # map specified, only training specific map
        if self.__map_name:
            self.train_map(self.__map_name)
            return

        # get all maps to train on
        map_names = self._get_maps()

        # adjust training parameters based on number of maps
        # (e.g. epochs to play / number of maps) [todo]

        for i in random.sample(range(0, len(map_names)), len(map_names)):
            self.train_map(map_names[i])
