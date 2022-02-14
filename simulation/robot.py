import numpy as np
import math

from simulation import ROBOT_INITIAL_THETA, ROBOT_MOTOR_POWER, ROBOT_WEIGHT, ROBOT_WHEEL_DISTANCE
from skspatial.objects import Line, Circle


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
        self._sensor_lenght = 20
        self.sensor_lines = [
            np.array([self._pos[0] + math.cos(2 * pi / 12 * x) * self._sensor_lenght, self._pos[1] +
                      math.sin(2 * pi / 12 * x) * self._sensor_lenght])
            for x in range(0, 12 + 1)]
        self._distances = np.array([200 for sensor in self.sensor_lines])

        #
        self._stop = False

    def hard_stop(self):
        self._velocity = np.array([0, 0], dtype=float)

    def stop(self):
        self._stop = True

    def accelerate_left(self):
        self._velocity[0] += 100

    def slowdown_left(self):
        self._velocity[0] -= 100

    def accelerate_right(self):
        self._velocity[1] += 100

    def slowdown_right(self):
        self._velocity[1] -= 100

    def set_time_delta(self, delta: float):
        self._delta = delta

        # update the acceleration for the frame which has been drawn in delta time
        self._acceleration = math.sqrt(ROBOT_MOTOR_POWER / ROBOT_WEIGHT) / 2

    def _brake(self, brake_const: float = 2):
        """
        This method uses energy to reverse the motors in order to break.
        """
        self._velocity /= brake_const

    def _rotate(self):
        # calculate the current velocity
        vel_left = self._velocity[0] * self._acceleration
        vel_right = self._velocity[1] * self._acceleration
        
        # calculate the movement and rotation
        self._pos[0] += ((vel_left + vel_right) / 2) * math.cos(self._theta) * self._delta
        self._pos[1] -= ((vel_left + vel_right) / 2) * math.sin(self._theta) * self._delta
        self._theta += (vel_right - vel_left) / ROBOT_WHEEL_DISTANCE * self._delta

        # rotate sensor lines
        self.sensor_lines = [
            np.array([self._pos[0] + math.cos(2 * math.pi / 12 * (x - self._theta)) * self._sensor_lenght,
                      self._pos[1] + math.sin(2 * math.pi / 12 * (x - self._theta)) * self._sensor_lenght])
            for x in range(0, 12 + 1)]

    def _calc_distances(self, lines):
        """
         calculates distances to all lines for every sensor line
         :param lines: the lines to which the distance is calculated
         """
        for line in lines:
            line = Line(point=line[0], direction=line[1])

            for index, s_line in enumerate(self.sensor_lines):
                # transform arrays to scikit Lines
                sensor_line = Line(point=self._pos, direction=s_line)
                try:
                    point_intersection = line.intersect_line(sensor_line)
                    distance = point_intersection.distance_point(self._pos)
                except ValueError:
                    distance = 200

                # change distance if it is less than 200
                if distance < self._distances[index]:
                    self._distances[index] = distance

    def _collision(self, lines):
        """
         calculates collision points of robot with all lines
         :param lines: the lines the robot collided with
         :return: the collision points
         """
        robot_body = Circle(self._pos, ROBOT_WHEEL_DISTANCE / 2)
        for line in lines:
            line = Line(line[0], line[1])
            try:
                point_a, point_b = robot_body.intersect_line(line)
            except ValueError:
                return None, None

            return point_a, point_b

    def drive(self, lines):
        if self._stop:
            self._brake()

            # if the kinetic energy is 0 (or lower) then the robot has stopped
            energy = (np.sum(self._velocity) / 2) * ROBOT_WEIGHT
            if energy <= 1:
                self.hard_stop()
                self._stop = False

        # calculate the rotation and movement
        self._rotate()
        self._calc_distances(lines)

        # stop if there was a colision
        collision_point_a, collision_point_b = self._collision(lines)
        if collision_point_a or collision_point_b:
            self.hard_stop()

        # transfer back to pixel data
        x = int(self._pos[0] * self._pixel_meter_const)
        y = int(self._pos[1] * self._pixel_meter_const)

        # update the distance lines
        distances = list((self._pixel_meter_const * self._distances).astype(int))
        sensor_lines = [(int(sensor[0] * self._pixel_meter_const), int(sensor[1] * self._pixel_meter_const))
                        for sensor in self.sensor_lines]

        return -self._theta, x, y, sensor_lines, distances
