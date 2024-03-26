"""This module handles the state of the app, e.g. it receives the disk location 
to store and load files."""

import os
import platform

ROOT_FOLDER = __name__[:-6]
MAPS_FOLDER = "maps/"
CONFIGS_FOLDER = "configs/"
MODELS_FOLDER = "models/"


def get_data_folder(folder_type: str) -> str:
    """Finds the app's data folder specific of an OS.

    Args:
        folder_type (str): The folder type to receive (ROOT_FOLDER, MAPS_FOLDER, 
        CONFIGS_FOLDER, MODELS_FOLDER).

    Returns:
        str: Returns the full path to one of the app's folder.
    """
    # get data folder based on OS
    path = os.path.expanduser("~") + "/.openrc-simulator"
    if platform.system() == "Windows":
        path = os.getenv("LOCALAPPDATA") + "/OpenRCSimulator"

    path = f"{path}/{folder_type}"
    if not os.path.exists(path):
        os.makedirs(path)

    return path
