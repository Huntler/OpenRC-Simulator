import math
import pygame as py
import numpy as np
from typing import Dict, Tuple, List
from OpenRCSimulator.graphics.objects.rectangle import Rectangle
from OpenRCSimulator.graphics.objects.sprite import Sprite


class CarBase(Sprite):

    TRACK_SPACING = "track_spacing"
    WHEELBASE = "wheelbase"
    WHEEL_DIAMENTER = "tire_diameter"
    WHEEL_WIDTH = "tire_width"
    STEERING_ANGLE = "steering_angle"
    
    CHASSIS_FRONT = "chassis_front"
    CHASSIS_REAR = "chassis_rear"

    def __init__(self, surface: py.Surface, position: Tuple[int, int], size: Tuple[int, int]) -> None:
        super().__init__(surface)

        # store the original sprite's position and size
        self._x, self._y = position
        self._w, self._h = size

        # store the internal sprite's position and size as the sprite is always centered
        self.__x, self.__y = position
        self.__w, self.__h = size

        # add margins required for steering visualization
        self._steering_length = 50
        self.__x += self._steering_length
        self.__w -= self._steering_length

        # add sprites
        self._background = Rectangle(self._surface, self._x, self._y, self._w, self._h, (40, 45, 45))

        # data container for car configuration in centimeter to pixel dimension
        self._data: Dict[str, List[float, int]] = {
            CarBase.TRACK_SPACING: [0, 0],
            CarBase.WHEELBASE: [0, 0],
            CarBase.WHEEL_DIAMENTER: [0, 0],
            CarBase.WHEEL_WIDTH: [0, 0],
            CarBase.STEERING_ANGLE: [0, 0],
            CarBase.CHASSIS_FRONT: [0, 0],
            CarBase.CHASSIS_REAR: [0, 0]
        }

        # load some dummy data in pixel dimension
        self._angle = math.radians(180 - 45)
        self._angle_coordinates = None

        # transfer centimeter to pixel dimension and fit car to sprite surface
        self._update_sizes()

    def _get_car_size(self) -> Tuple[float, float]:
        # get car width and height based on track spacing and wheelbase
        car_width = self._data[CarBase.TRACK_SPACING][0] + self._data[CarBase.WHEEL_WIDTH][0]
        car_height = self._data[CarBase.WHEELBASE][0] + self._data[CarBase.WHEEL_DIAMENTER][0]
        if car_height == 0 or car_width == 0:
            return 0, 0, 1
        
        # calculate the centimeter to pixel multiplier based on preview surface size and car size
        multiplier = min((self.__h / car_height), (self.__w / car_width))        
        return car_width * multiplier, car_height * multiplier, multiplier
    
    def _center_sprite(self) -> None:
        # center align the car based on its size and the preview's position and size
        car_width, car_height, _ = self._get_car_size()
        self.__x = self._x + (self.__w - car_width) // 2 + self._steering_length
        self.__y = self._y + (self.__h - car_height) // 2
    
    def _update_sizes(self) -> None:
        # calculate the multiplier to fit dimensions to the sprite's available surface area
        _, _, multiplier = self._get_car_size()
        
        self._data[CarBase.TRACK_SPACING][1] = self._data[CarBase.TRACK_SPACING][0] * multiplier
        self._data[CarBase.WHEELBASE][1] = self._data[CarBase.WHEELBASE][0] * multiplier
        self._data[CarBase.WHEEL_DIAMENTER][1] = self._data[CarBase.WHEEL_DIAMENTER][0] * multiplier
        self._data[CarBase.WHEEL_WIDTH][1] = self._data[CarBase.WHEEL_WIDTH][0] * multiplier

        # update internal x and y position
        self._center_sprite()

        # create line sprite showing steering angle 
        self._data[CarBase.STEERING_ANGLE][1] = math.radians(180 - self._data[CarBase.STEERING_ANGLE][0])
        self._angle_coordinates = self._calculate_steering()
    
    def set_value(self, name: str, value: float) -> None:
        self._data[name] = [value, 0]
        self._update_sizes()
    
    def _get_chassis_position(self) -> Tuple:
        # get front and rear bumper position
        front = ((self.__x, self.__y - 10), (self.__x + self.__w, self.__y - 10))
        rear = ((self.__x, self._y + self.__h), (self.__x + self.__w, self._y + self.__h))
        return front, rear
    
    def _get_axis_position(self) -> Tuple:
        # calculate position of the axis
        x = self.__x + self._data[CarBase.WHEEL_WIDTH][1] / 2
        y = self.__y + self._data[CarBase.WHEEL_DIAMENTER][1] / 2
        w = x + self._data[CarBase.TRACK_SPACING][1] - self._data[CarBase.WHEEL_WIDTH][1]
        h = y + self._data[CarBase.WHEELBASE][1]

        front = (x, y, w, y)        
        rear = (x, h, w, h)        
        center = (x + (w - x) / 2, y, x + (w - x) / 2, h)

        return front, rear, center
    
    def _get_wheels(self) -> Tuple:
        # calculate positions of wheels
        x1, x2 = self.__x, self.__x + self._data[CarBase.TRACK_SPACING][1] - self._data[CarBase.WHEEL_WIDTH][1]
        y1, y2 = self.__y, self.__y + self._data[CarBase.WHEELBASE][1]
        w = self._data[CarBase.WHEEL_WIDTH][1]
        h = self._data[CarBase.WHEEL_DIAMENTER][1]

        # create wheel objects
        fl = Rectangle(self._surface, x1, y1, w, h, (255, 255, 255))
        fr = Rectangle(self._surface, x2, y1, w, h, (255, 255, 255))
        rl = Rectangle(self._surface, x1, y2, w, h, (255, 255, 255))
        rr = Rectangle(self._surface, x2, y2, w, h, (255, 255, 255))

        return fl, fr, rl, rr
    
    def _calculate_steering(self) -> Tuple:
        # define start and end of a vector [0, 1]
        start = np.array((self.__x, self.__y + self._data[CarBase.WHEEL_DIAMENTER][1] // 2))
        end = np.array((self.__x, self.__y))
        offset = np.array((self._data[CarBase.TRACK_SPACING][1] - self._data[CarBase.WHEEL_WIDTH][1], 0))
        angle = self._data[CarBase.STEERING_ANGLE][1]

        # rotate vector by angle
        vec = start - end        
        p_x = vec[0] * math.cos(angle) - vec[1] * math.sin(angle)
        p_y = vec[0] * math.sin(angle) + vec[1] * math.cos(angle)

        # norm the length of the vector
        vec = np.array([p_x, p_y])
        if vec[0] == 0 and vec[1] == 0:
            return None
        
        angeled = (vec / np.linalg.norm(vec)) * self._steering_length + start

        # draw lines
        return start, angeled, start + offset, angeled + offset

    def draw(self) -> None:       
        self._background.draw()

        # draw steering
        if self._angle_coordinates:
            s1, e1, s2, e2 = self._angle_coordinates
            py.draw.line(self._surface, (255, 255, 255), s1, e1, width = 5)
            py.draw.line(self._surface, (255, 255, 255), s2, e2, width = 5)

        # draw axis
        front_axis, rear_axis, center = self._get_axis_position()
        py.draw.line(self._surface, (255, 255, 255), front_axis[:2], front_axis[2:], width = 5)
        py.draw.line(self._surface, (255, 255, 255), rear_axis[:2], rear_axis[2:], width = 5)
        py.draw.line(self._surface, (255, 255, 255), center[:2], center[2:], width = 5)

        # draw wheels
        for wheel in self._get_wheels():
            wheel.draw()