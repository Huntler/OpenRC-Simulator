from graphics.window import BaseWindow
from graphics.objects.rectangle import Rectangle
from graphics.objects.robot import Robot
import pygame as py


class SimulationWindow(BaseWindow):
    def sprites(self) -> None:
        # define sprites here
        self._background = Rectangle(self._screen, 0, 0, self._width, self._height, (120, 120, 120))
        self._robot = Robot(self._screen, 100, 100, 50, (200, 50, 50))
        self._robot_velocity = [0, 0]
        self._robot_rotation = 0

    def draw(self) -> None:
        # draw sprites here
        self._background.draw()
        self._robot.draw()

        # move the robot
        x_robot, y_robot = self._robot.get_position()
        new_robot_pos = (x_robot + self._robot_velocity[0], y_robot + self._robot_velocity[1])
        self._robot.set_position(new_robot_pos)

        angle = self._robot.get_direction() + self._robot_rotation
        self._robot.set_direction(angle)

        self.key_pressed()
    
    def key_pressed(self) -> None:
        keys = py.key.get_pressed()

        # key pressed events
        if keys[py.K_UP]:
            self._robot_velocity[0] += 0.1
        else:
            if self._robot_velocity[0] >= 0:
                self._robot_velocity[0] -= 0.1

        if keys[py.K_DOWN]:
            self._robot_velocity[0] -= 0.1
        else:
            if self._robot_velocity[0] <= 0:
                self._robot_velocity[0] += 0.1
        
        if keys[py.K_LEFT]:
            self._robot_rotation -= 0.1
        else:
            if self._robot_rotation <= 0:
                self._robot_rotation += 0.1

        if keys[py.K_RIGHT]:
            self._robot_rotation += 0.1
        else:
            if self._robot_rotation >= 0:
                self._robot_rotation -= 0.1

    def event(self, event) -> None:
        super().event(event)