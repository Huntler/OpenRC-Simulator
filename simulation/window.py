from graphics.window import BaseWindow
from graphics.objects.rectangle import Rectangle
from graphics.objects.robot import Robot
import pygame as py


class SimulationWindow(BaseWindow):
    def sprites(self) -> None:
        # define sprites here
        pass

    def draw(self) -> None:
        pass

    def event(self, event) -> None:
        super().event(event)