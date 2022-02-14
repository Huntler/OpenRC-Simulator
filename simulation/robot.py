from dis import dis
import numpy as np
import math

from simulation import ROBOT_INITIAL_THETA, ROBOT_MOTOR_POWER, ROBOT_SENSOR_DISTANCE, ROBOT_WEIGHT, ROBOT_WHEEL_DISTANCE
from skspatial.objects import Line, Circle
from shapely.geometry import LineString, Point


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
        self.sensor_lines = np.array([np.zeros(2) for _ in range(13)])
        self._update_sensors()
        self._distances = np.array([ROBOT_SENSOR_DISTANCE for sensor in self.sensor_lines])

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
        self._velocity /= brake_const

    def _update_sensors(self):
        # the factor which is used to get the sensors end position
        factor = 2 * math.pi / 12

        # iterate of each sensor
        for i, _ in enumerate(self.sensor_lines):
            # and create its stock position
            sensor = np.array([
                self._pos[0] + math.cos(factor * i),
                self._pos[1] + math.sin(factor * i)
                ])

            # then update the sensors position afterwards
            sensor[0] += math.cos(factor * i - self._theta) * ROBOT_SENSOR_DISTANCE
            sensor[1] += math.sin(factor * i - self._theta) * ROBOT_SENSOR_DISTANCE

            self.sensor_lines[i] = sensor

    def _rotate(self):
        # calculate the current velocity
        vel_left = self._velocity[0] * self._acceleration
        vel_right = self._velocity[1] * self._acceleration
        
        # calculate the movement and rotation
        self._pos[0] += ((vel_left + vel_right) / 2) * math.cos(self._theta) * self._delta
        self._pos[1] -= ((vel_left + vel_right) / 2) * math.sin(self._theta) * self._delta
        self._theta += (vel_right - vel_left) / ROBOT_WHEEL_DISTANCE * self._delta
        self._theta = self._theta % (2 * math.pi)

        # rotate sensor lines
        self._update_sensors()

    def _calc_distances(self, lines):
        """
        calculates distances to all lines for every sensor line
        :param lines: the lines to which the distance is calculated
        """
        robot = Point(self._pos)

        # reset each sensor values
        for sensor_num, sensor_point in enumerate(self.sensor_lines):
            sensor_line = LineString([self._pos, sensor_point])
            self._distances[sensor_num] = ROBOT_SENSOR_DISTANCE

            # calulate the current sensor's value for each wall
            for wall in lines:
                wall = LineString(wall)
                hit = sensor_line.intersection(wall)

                if hit:
                    distance = robot.distance(hit)

                    # change distance if it is less than the found distance so far
                    if distance < self._distances[sensor_num]:
                        self._distances[sensor_num] = distance

    def _collision(self) -> np.ndarray:
        """
         calculates collision points of robot with all lines
         :param lines: the lines the robot collided with
         :return: the collision points
        """
        # get collisions
        collisions = np.where(self._distances < ROBOT_WHEEL_DISTANCE / 2, -self._distances, 0)

        # if any collision was found, then reset the robots position back so it is not stuck in the wall
        if collisions.any() != 0:
            sensor_num = np.argmin(collisions)

            # FIXME: this calculation may be wrong
            collision = collisions[sensor_num] / self._pixel_meter_const
            direction = self.sensor_lines[sensor_num] / np.linalg.norm(self.sensor_lines[sensor_num])

            self._pos = self._pos + direction * collision
            self.hard_stop()

        return collisions

    def drive(self, lines):
        lines = np.array(lines) / self._pixel_meter_const

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
        collisions = self._collision()

        # transfer back to pixel data
        x = int(self._pos[0] * self._pixel_meter_const)
        y = int(self._pos[1] * self._pixel_meter_const)

        # update the distance lines
        distances = list((self._distances).astype(int))
        sensor_lines = [(int(sensor[0] * self._pixel_meter_const), int(sensor[1] * self._pixel_meter_const))
                        for sensor in self.sensor_lines]

        return -self._theta, x, y, sensor_lines, distances
