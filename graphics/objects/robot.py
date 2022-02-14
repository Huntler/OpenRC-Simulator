import math
from typing import List, Tuple
from graphics.objects.sprite import Sprite
import pygame as py


class Robot(Sprite):
    def __init__(self, surface, x: int, y: int, radius: int, c: Tuple[int, int, int], font) -> None:
        super().__init__()

        self._surface = surface

        self._x = x
        self._y = y
        self._radius = radius
        self._sensors = []
        self._distances = []
        self._border = int(radius // math.pi) // 2

        self.set_direction(90)

        self._c = c
        self._clicked_c = c

        self._font = font

    def set_direction(self, angle: float) -> None:
        self._angle = angle
        self._line_end_x = int(math.cos(self._angle) * (self._radius - 1) + self._x)
        self._line_end_y = int(math.sin(self._angle) * (self._radius - 1) + self._y)

    def get_direction(self) -> float:
        return self._angle

    def set_position(self, pos: Tuple[int, int]) -> None:
        self._x, self._y = pos
        self._line_end_x = int(math.cos(self._angle) * (self._radius - 1) + self._x)
        self._line_end_y = int(math.sin(self._angle) * (self._radius - 1) + self._y)

    def get_position(self) -> Tuple[int, int]:
        return self._x, self._y

    def set_sensors(self, sensors: List):
        self._sensors = sensors

    def set_distances(self, distances: List):
        self._distances = distances

    def draw(self) -> None:
        for sensor_point in self._sensors:
            py.draw.line(self._surface, (255, 255, 255), (self._x, self._y), sensor_point)
        py.draw.circle(self._surface, self._c, (self._x, self._y), self._radius)
        py.draw.circle(self._surface, (0, 0, 0), (self._x, self._y), self._radius, self._border)
        py.draw.line(self._surface, (0, 0, 0), (self._x, self._y), (self._line_end_x, self._line_end_y), self._border)

        for index, sensor in enumerate(self._sensors):
            label = self._font.render(str(self._distances[index]), True, (255, 255, 255))
            self._surface.blit(label, sensor)

        super().draw()

    def collidepoint(self, point: Tuple[int, int]) -> bool:
        x1, y1 = point
        x2, y2 = self._x, self._y
        distance = math.hypot(x1 - x2, y1 - y2)
        return distance <= self._radius

    def set_clicked_color(self, c: Tuple[int, int, int]) -> None:
        self._clicked_c = c

    def _clicked(self) -> None:
        py.draw.circle(self._surface, self._c, (self._x, self._y), self._radius)
        py.draw.circle(self._surface, (0, 0, 0), (self._x, self._y), self._radius, self._border)
