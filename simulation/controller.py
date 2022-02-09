from typing import Tuple
from graphics.controller import BaseController
from graphics.objects.rectangle import Rectangle
from graphics.objects.robot import Robot
from graphics.objects.text import ANCHOR_CENTER, ANCHOR_TOP_LEFT, Text
from graphics.sub_controller import BaseSubController
from simulation import BACKGROUND_COLOR, CREATOR, MANUAL, MODE_TEXT_COLOR, SHORTCUT_TEXT_COLOR, SHORTCUT_TEXT_COLOR_ACTIVE, SIMULATION
from simulation.sub_controller.goal_controller import GoalController
from simulation.sub_controller.robot_controller import RobotController
from simulation.sub_controller.wall_controller import WallController
from simulation.window import CREATOR_PLACE_WALL, CREATOR_SAVE_MAP, MOUSE_CLICK, SHORTCUTS_UNTOGGLE, SimulationWindow


class SimulationController(BaseController):
    def __init__(self, window_size: Tuple[int, int], mode:int, flags: int = 0) -> None:
        """The SimulationController manages the SimulationWindow. This is a seperate 
        thread, than the pygame one.

        Args:
            window_size (Tuple[int, int]): Width and height of the window.
            flags (int, optional): Fullscreen, hardware acceleration, ... Defaults to 0.
        """
        super().__init__()

        self._width, self._height = window_size
        self._center = (self._width // 2, self._height // 2)
        self._flags = flags

        # create the window visuals
        self._window = SimulationWindow(window_size=window_size, flags=flags)
        self._surface = self._window.get_surface()

        # create the sprites we want to use
        # background object (just a colored box)
        background = Rectangle(self._surface, 0, 0, self._width, self._height, BACKGROUND_COLOR)
        self._window.add_sprite("background", background, zindex=99)

        # create sub controllers
        self._active_sub_controller = None

        # create the robot controller
        self._robot = RobotController(self._window, mode)
        self._robot.on_toggle(self._sub_controller_toggled)

        # create the wall controller
        self._wall = WallController(self._window, mode)
        self._wall.on_toggle(self._sub_controller_toggled)

        # create the goal controller
        self._goal = GoalController(self._window, mode)
        self._goal.on_toggle(self._sub_controller_toggled)

        self._window.on_callback(SHORTCUTS_UNTOGGLE, self._untoggle_all_sub_controller)

        #keys = py.key.get_pressed()
        #print(keys)
        self.mode(mode)
    
    def _sub_controller_toggled(self, sub_controller: BaseSubController) -> None:
        """This method executes if a subcontroller was toggled. In this case, this method 
        disables all other subcontrollers.
        """
        # if the active sub controller was toggled again, then just unregister it
        if self._active_sub_controller == sub_controller:
            self._active_sub_controller = None
            return

        # if there was an active sub controller, then toggle it again
        if self._active_sub_controller:
            self._active_sub_controller.toggle(call=False)
            self._active_sub_controller = None
        
        if sub_controller.is_toggled():
            self._active_sub_controller = sub_controller
    
    def _untoggle_all_sub_controller(self) -> None:
        if self._active_sub_controller:
            self._active_sub_controller.toggle(call=False)
            self._active_sub_controller = None
    
    def mode(self, mode: int) -> None:
        """The applications mode (CREATOR, SIMULATION, MANUAL)

        Args:
            mode (int): The mode.
        """
        # TODO: if creator mode, then add edit bar
        cx, cy = self._center

        # show background text
        # text describing the current mode (integrated into the background)
        mode_text = ["SIMULATION", "CREATOR", "MANUAL"]
        text_mode = Text(self._surface, mode_text[mode], cx, cy, 120, MODE_TEXT_COLOR)
        self._window.add_sprite("text_mode", text_mode, zindex=98)

        # show shortcut info for CREATOR mode
        shortcuts_height = [80, 180, 80]
        text_shortcuts = Text(self._surface, "Shortcuts", 0, 0, 50, SHORTCUT_TEXT_COLOR)
        text_shortcuts.set_position((20, self._height - shortcuts_height[mode]), ANCHOR_TOP_LEFT)
        self._window.add_sprite("text_shortcuts_title", text_shortcuts, zindex=98)
    
    def loop(self) -> None:
        self._robot.loop()
        self._wall.loop()
        self._goal.loop()
