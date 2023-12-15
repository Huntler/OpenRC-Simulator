from OpenRCSimulator.graphics.window import BaseWindow


MOUSE_CLICK = "mouse_click"
SHORTCUTS_UNTOGGLE = "untoggle_all"

CREATOR_PLACE_CAR = "creator_place_car"
CREATOR_PLACE_GOAL = "creator_place_goal"
CREATOR_PLACE_WALL= "creator_place_wall"
STORAGE_SAVE = "creato_save_map"

SENSORS_ACTIVATED = "sensors_activated"
TEXT_INPUT_W = "text_input_width"
TEXT_INPUT_L = "text_input_length"
TEXT_INPUT_T = "text_input_turn"


class MainWindow(BaseWindow):
    def sprites(self) -> None:
        # define sprites here
        pass

    def draw(self) -> None:
        pass

    def event(self, event) -> None:
        super().event(event)