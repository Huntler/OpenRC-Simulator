import math
import pygame as py
import numpy as np
from typing import Dict, Tuple
from OpenRCSimulator.graphics.objects.rectangle import Rectangle
from OpenRCSimulator.graphics.objects.sprite import Sprite


class CarBase(Sprite):

    TRACK_SPACING = "track_spacing"
    WHEELBASE = "wheelbase"
    WHEEL_DIAMENTER = "tire_diameter"
    WHEEL_WIDTH = "tire_width"
    STEERING_ANGLE = "steering_angle"

    def __init__(self, surface: py.Surface, position: Tuple[int, int], size: Tuple[int, int]) -> None:
        super().__init__(surface)

        self._x, self._y = position
        self._w, self._h = size

        self._steering_length = 50
        self._y += self._steering_length
        self._x += self._steering_length
        self._w -= self._steering_length
        self._h -= self._steering_length

        self._data: Dict[str, int] = {}

        self._track_spacing = 180
        self._wheelbase = 300
        self._wheel_diameter = 50
        self._wheel_width = 30
        self._angle = math.radians(180 - 45)
        self._angle_coordinates = None
        self._update_sizes()
    
    def _update_sizes(self) -> None:
        car_width = self._data.get(CarBase.TRACK_SPACING, self._track_spacing) + \
                    self._data.get(CarBase.WHEEL_WIDTH, self._wheel_width)
        car_height = self._data.get(CarBase.WHEELBASE, self._wheelbase) + \
                    self._data.get(CarBase.WHEEL_DIAMENTER, self._wheel_diameter)
        multiplier = max((self._h / car_height), (self._w / car_width))
        
        self._track_spacing = self._data.get(CarBase.TRACK_SPACING, self._track_spacing) * multiplier
        self._wheelbase = self._data.get(CarBase.WHEELBASE, self._wheelbase) * multiplier
        self._wheel_diameter = self._data.get(CarBase.WHEEL_DIAMENTER, self._wheel_diameter) * multiplier
        self._wheel_width = self._data.get(CarBase.WHEEL_WIDTH, self._wheel_width) * multiplier

        self._angle = math.radians(180 - self._data.get(CarBase.STEERING_ANGLE, 45))
        self._angle_coordinates = self._calculate_steering()
    
    def set_value(self, name: str, value: float) -> None:
        self._data[name] = value
        self._update_sizes()
    
    def _get_axis_position(self) -> Tuple:
        front = (self._x + self._wheel_width / 2, self._y + self._wheel_diameter / 2, 
                self._x + self._track_spacing - self._wheel_width / 2, self._y + self._wheel_diameter / 2)
        
        rear = (self._x + self._wheel_width / 2, self._y + self._wheel_diameter / 2 + self._wheelbase, 
                self._x + self._track_spacing - self._wheel_width / 2, self._y + self._wheel_diameter / 2 + self._wheelbase)
        
        center = (self._x + self._track_spacing / 2, self._y + self._wheel_diameter / 2,
                  self._x + self._track_spacing / 2, self._y + self._wheel_diameter / 2 + self._wheelbase)

        return front, rear, center
    
    def _get_wheels(self) -> Tuple:
        fl = Rectangle(self._surface, self._x, self._y, self._wheel_width, self._wheel_diameter, (255, 255, 255))
        fr = Rectangle(self._surface, self._x + self._track_spacing - self._wheel_width / 2, self._y, self._wheel_width, 
                       self._wheel_diameter, (255, 255, 255))
        rl = Rectangle(self._surface, self._x, self._y + self._wheelbase, self._wheel_width, self._wheel_diameter, 
                       (255, 255, 255))
        rr = Rectangle(self._surface, self._x + self._track_spacing - self._wheel_width / 2, self._y + self._wheelbase, 
                       self._wheel_width, self._wheel_diameter, (255, 255, 255))
        return fl, fr, rl, rr
    
    def _calculate_steering(self) -> Tuple:
        # calculate angle of line
        start = np.array((self._x + self._wheel_width / 2, self._y))
        end = np.array((self._x + self._wheel_width / 2, self._y - self._steering_length))
        offset = np.array((self._track_spacing - self._wheel_width / 2, 0))

        vec = start - end        
        p_x = vec[0] * math.cos(self._angle) - vec[1] * math.sin(self._angle)
        p_y = vec[0] * math.sin(self._angle) + vec[1] * math.cos(self._angle)

        vec = np.array([p_x, p_y])
        angeled = (vec / np.linalg.norm(vec)) * self._steering_length + start

        # draw lines
        return start, angeled, start + offset, angeled + offset

    def draw(self) -> None:
        # draw axis
        front_axis, rear_axis, center = self._get_axis_position()
        py.draw.line(self._surface, (255, 255, 255), front_axis[:2], front_axis[2:], width = 5)
        py.draw.line(self._surface, (255, 255, 255), rear_axis[:2], rear_axis[2:], width = 5)
        py.draw.line(self._surface, (255, 255, 255), center[:2], center[2:], width = 5)

        # draw wheels
        for wheel in self._get_wheels():
            wheel.draw()
        
        # draw steering
        if self._angle_coordinates:
            s1, e1, s2, e2 = self._angle_coordinates
            py.draw.line(self._surface, (255, 255, 255), s1, e1, width = 5)
            py.draw.line(self._surface, (255, 255, 255), s2, e2, width = 5)