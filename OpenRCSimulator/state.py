import os
import platform

ROOT_FOLDER = __name__[:-6]
MAPS_FOLDER = "maps/"
CONFIGS_FOLDER = "configs/"
MODELS_FOLDER = "models/"

def get_data_folder(folder_type: str) -> str:
    # get data folder based on OS
    path = os.path.expanduser("~") + "/.openrc-simulator"
    if platform.system() == "Windows":
        path = os.getenv("LOCALAPPDATA") + "/OpenRCSimulator"
    
    path = f"{path}/{folder_type}"
    if not os.path.exists(path):
        os.makedirs(path)
    
    return path