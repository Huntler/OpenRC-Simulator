import math
import pkg_resources
import pygame as py
import numpy as np
from typing import List, Tuple

from OpenRCSimulator.state import ROOT_FOLDER
from OpenRCSimulator.graphics import CENTIMETER_TO_PIXEL
from OpenRCSimulator.graphics.objects.sprite import Sprite



class Car(Sprite):

    NORMAL = 0
    CONFIG = 1

    def __init__(self, surface, x: int, y: int, chassis_size: Tuple[float, float], font, mode: int = NORMAL) -> None:
        super().__init__()

        # get the chassis size in pixels
        self._pixel_size = np.array(chassis_size) * CENTIMETER_TO_PIXEL

        # set drawing surface
        self._surface = surface

        # load the car's texture
        image_name = "car_white.png" if mode == Car.NORMAL else "car_white_config.png"
        car_resource_path = "/".join(("resources", image_name))
        self._car_surface = py.image.load(pkg_resources.resource_stream(ROOT_FOLDER, car_resource_path))
        self._car_surface = py.transform.rotate(self._car_surface, 90)
        self._car_surface = py.transform.smoothscale(self._car_surface, self._pixel_size)
        self._car_surface = self._car_surface.convert_alpha()

        self._x = x
        self._y = y
        self._sensors = []
        self._distances = []

        self.set_direction(90)

        self._font = font

    def set_direction(self, angle: float) -> None:
        """Sets direction of the car in radians.

        Args:
            angle (float): Angle in radians.
        """
        self._angle = angle

    def get_direction(self) -> float:
        """Returns the current car's direction in radians.

        Returns:
            float: Direction in radians.
        """
        return self._angle

    def set_position(self, pos: Tuple[int, int]) -> None:
        """Sets the position of the car.

        Args:
            pos (Tuple[int, int]): Position given as (x, y)
        """
        self._x, self._y = pos

    def get_position(self) -> Tuple[int, int]:
        """Returns the current car's position

        Returns:
            Tuple[int, int]: Position in (x, y)
        """
        return self._x, self._y

    def set_alpha(self, alpha: float = 1.0) -> None:
        if alpha < 0 or alpha > 1.0:
            raise RuntimeError
        
        self._car_surface.set_alpha(math.ceil(alpha * 255))

    def set_sensors(self, sensors: List[Tuple[int, int]]):
        """Position of sensor given as a point (x, y)

        Args:
            sensors (List): Expected list of sensors.
        """
        self._sensors = sensors

    def set_distances(self, distances: List[float]):
        """Sets the distance readings of each sensor.

        Args:
            distances (List): Distances given as float in a list.
        """
        self._distances = distances

    def __rotate_pivoted(self, surface: py.Surface, angle: float, pivot: Tuple):
        # rotate the leg image around the pivot
        image = py.transform.rotate(surface, angle)
        rect = image.get_rect()
        rect.center = pivot
        return image, rect

    def draw(self) -> None:
        # rotate the car
        car, car_rect = self.__rotate_pivoted(self._car_surface, -math.degrees(self._angle) - 90, (self._x, self._y))

        # calculate the correct center
        x = car_rect[0] + (car_rect[2] / 2)
        y = car_rect[1] + (car_rect[3] / 2)

        for sensor_point in self._sensors:
            py.draw.line(self._surface, (255, 255, 255), (x, y), sensor_point)
        
        # draw car, first rotate to correct direction
        self._surface.blit(car, car_rect)

        # draw sensors
        for index, sensor in enumerate(self._sensors):
            label = self._font.render(str(self._distances[index]), True, (255, 255, 255))
            self._surface.blit(label, sensor)

        super().draw()

    def collidepoint(self, point: Tuple[int, int]) -> bool:
        """Checks if the car collides with a given point.

        Args:
            point (Tuple[int, int]): The collision point to check.

        Returns:
            bool: True if collision was detected.
        """
        x, y = point
        x1, y1, x2, y2 = self._car_surface.get_rect()
        return x1 <= x and x <= x2 and y1 <= y and y <= y2

    def _clicked(self) -> None:
        pass
