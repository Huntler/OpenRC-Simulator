import numpy as np
import math

from motion_model import ROBOT_INITIAL_THETA, ROBOT_MOTOR_POWER, ROBOT_WEIGHT, ROBOT_WHEEL_DISTANCE


class Robot:
    def __init__(self, pixel_pos: np.array, robot_size: int):
        """
        initializes robot
        :param midpoint: midpoint of the robot (in space)
        """
        # handling coordinate system in pixel diemnsion
        self._pixel_meter_const = robot_size * 2 / ROBOT_WHEEL_DISTANCE
        self._pixel_pos = pixel_pos

        # simulation related measuremnets
        self._x = self._y = 0
        self._delta = 0

        # angle to coordinate system's x-axis
        self._theta = ROBOT_INITIAL_THETA

        self._acceleration = math.sqrt(ROBOT_MOTOR_POWER / ROBOT_WEIGHT) / 2
        print(f"Acceleration: {round(self._acceleration * 100)} cm/s^2")
        self._acc_l = self._acc_r = 0

    def accelerate_left(self):
        self._acc_l += self._acceleration

    def slowdown_left(self):
        self._acc_l -= self._acceleration

    def accelerate_right(self):
        self._acc_r += self._acceleration

    def slowdown_right(self):
        self._acc_r -= self._acceleration

    def set_time_delta(self, delta: float):
        self._delta = delta

    def _rotation(self, vl, vr):
        # calculate metrics
        R = (ROBOT_WHEEL_DISTANCE / 2) * ((vl + vr) / (vr - vl))
        omega = (vr - vl) / ROBOT_WHEEL_DISTANCE

        # calculate ICC and extend it with w*dt
        icc = [self._x - R * math.sin(omega),
               self._y + R * math.cos(omega), 
               omega * self._delta]
        matrix = np.array([
            [math.cos(omega * self._delta), -math.sin(omega * self._delta), 0],
            [math.sin(omega * self._delta), math.cos(omega * self._delta), 0],
            [0, 0, 1]], dtype=float)
        result = np.matmul(matrix, np.array([self._x - icc[0], self._y - icc[1], self._theta])) + icc

        # update coordinates and angle
        self._x = result[0]
        self._y = result[1]
        self._theta = result[2] % (math.pi * 2)

        # update velocity of wheels
        vr = omega * (R + ROBOT_WHEEL_DISTANCE / 2)
        vl = omega * (R - ROBOT_WHEEL_DISTANCE / 2)
        return vl, vr

    def _forward(self, vl, vr):
        # calculate the distance, the roboter made after delta of time
        speed = (vl + vr) / 2
        dir_vector = np.array([math.cos(self._theta), math.sin(self._theta)])
        print(dir_vector, [vl, vr])
        distance = dir_vector * speed * self._delta * self._pixel_meter_const
        self._pixel_pos += distance

    def drive(self):
        # acceleration * times -> velocity
        velocity_l = self._acc_l * self._delta
        velocity_r = self._acc_r * self._delta

        # spin the wheels
        if velocity_l != velocity_r:
            velocity_l, velocity_r = self._rotation(velocity_l, velocity_r)
            self._forward(velocity_l, velocity_r)
        else:
            self._forward(velocity_l, velocity_r)

        # update position
        pos = self._pixel_pos + self._pixel_meter_const * np.array([self._x, -self._y])
        return self._theta, int(pos[0]), int(pos[1])
