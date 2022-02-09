from typing import List
from graphics.objects.text import ANCHOR_CENTER, ANCHOR_TOP_LEFT, Text
from graphics.sub_controller import BaseSubController
from simulation import CREATOR, MODE_TEXT_COLOR, SHORTCUT_TEXT_COLOR, SHORTCUT_TEXT_COLOR_ACTIVE
from simulation.window import CREATOR_SAVE_MAP, SimulationWindow
import yaml


class StorageController(BaseSubController):
    def __init__(self, window: SimulationWindow, app_mode: int) -> None:
        super().__init__()
        self._app_mode = app_mode
        self._changes = "unsaved"
        
        # window and surface information
        self._window = window
        self._ww, self._wh = window.get_window_size()
        self._surface = window.get_surface()
        
        # texts
        if app_mode == CREATOR:
            self._text_storage = Text(self._surface, "'S' Save the map", 0, 0, 30, SHORTCUT_TEXT_COLOR)
            self._text_storage.set_position((20, self._wh - 40), ANCHOR_TOP_LEFT)
            self._window.add_sprite("text_storage", self._text_storage, zindex=98)
            self._window.on_callback(CREATOR_SAVE_MAP, self.toggle)

            self._text_status = Text(self._surface, self._changes, 0, 0, 30, SHORTCUT_TEXT_COLOR)
            self._text_status.set_position((self._ww // 2, self._wh // 2 + 80), ANCHOR_CENTER)
            self._window.add_sprite("text_status", self._text_status, zindex=98)
    
    def toggle(self, call: bool = True) -> None:
        self._toggle_callback()
    
    def changes(self, value: bool) -> None:
        self._changes = "unsaved" if value else "saved"
        self._text_status.set_text(self._changes)
        self._text_status.set_color(SHORTCUT_TEXT_COLOR if value else MODE_TEXT_COLOR)

    def save(self, file_name: str, controllers: List[BaseSubController]) -> None:
        """This method stores a given list of controllers to a yaml file.

        Args:
            controllers (List[BaseSubController]): The list of controllers to save.
        """
        dict_file = {}
        dict_file["app"] = {}
        dict_file["app"]["width"] = self._ww
        dict_file["app"]["height"] = self._wh

        for controller in controllers:
            dict_file = dict_file | controller.dict()
        
        with open(f"{file_name}.yaml", "w") as file:
            documents = yaml.dump(dict_file, file)
        
        self.changes(False)
    
    def loop(self) -> None:
        pass