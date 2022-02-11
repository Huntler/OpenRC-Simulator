import numpy as np
import math

from simulation import ROBOT_INITIAL_THETA, ROBOT_MOTOR_POWER, ROBOT_WEIGHT, ROBOT_WHEEL_DISTANCE


class Robot:
    def __init__(self, pixel_pos: np.array, robot_size: int, delta: float = 0.1):
        """
        initializes robot
        :param midpoint: midpoint of the robot (in space)
        """
        # handling coordinate system in pixel diemnsion
        # calculation:
        #  - pixel-radius * 2 to get robot's size in pixel
        #  - then divided by the distance of the robot's wheels (given in cm)
        #  - results in amount of pixels per meter
        self._pixel_meter_const = robot_size * 2 / ROBOT_WHEEL_DISTANCE
        self._pos = pixel_pos / self._pixel_meter_const

        # acceleration is calculated based on weight and motor power
        # value in meter per second (already calculated with time)
        self._acceleration = math.sqrt(ROBOT_MOTOR_POWER / ROBOT_WEIGHT) / 2 * delta
        self._velocity = np.array([0, 0], dtype=float)

        # angle to coordinate system's x-axis
        self._theta = ROBOT_INITIAL_THETA

        # simulation related measuremnets
        self._delta = delta

        # create distance sensors
        pi = math.pi
        self._sensor_lenght = 100
        self.sensor_lines = [
            np.array([self._pos[0] + math.cos(2 * pi / 12 * x) * self._sensor_lenght, self._pos[1] +
                      math.sin(2 * pi / 12 * x) * self._sensor_lenght])
            for x in range(0, 12 + 1)]
        self.distances = []
    
    def hard_stop(self):
        self._velocity = np.array([0, 0], dtype=float)

    def accelerate_left(self):
        self._velocity[0] += self._acceleration

    def slowdown_left(self):
        self._velocity[0] -= self._acceleration

    def accelerate_right(self):
        self._velocity[1] += self._acceleration

    def slowdown_right(self):
        self._velocity[1] -= self._acceleration

    def set_time_delta(self, delta: float):
        self._delta = delta
        self._acceleration = math.sqrt(ROBOT_MOTOR_POWER / ROBOT_WEIGHT) / 2 * self._delta

    def _rotate(self):
        # calculate the movement and rotation
        self._pos[0] += ((self._velocity[0] + self._velocity[1]) / 2) * math.cos(self._theta) * self._delta
        self._pos[1] -= ((self._velocity[0] + self._velocity[1]) / 2) * math.sin(self._theta) * self._delta
        self._theta += (self._velocity[1] - self._velocity[0]) / ROBOT_WHEEL_DISTANCE * self._delta

        # rotate sensor lines
        pi = math.pi
        self.sensor_lines = [
            np.array([self._pos[0] + math.cos(2 * pi / 12 * x) * self._sensor_lenght, self._pos[1] +
                      math.sin(2 * pi / 12 * x) * self._sensor_lenght])
            for x in range(0, 12 + 1)]

    def drive(self):
        # calculate the rotation and movement
        self._rotate()

        # transfer back to pixel data
        x = int(self._pos[0] * self._pixel_meter_const)
        y = int(self._pos[1] * self._pixel_meter_const)

        return -self._theta, x, y
