from dis import dis, disco

import numpy as np
import math

from simulation import CHASSIS_SIZE, INITIAL_THETA, MOTOR_POWER, SENSOR_DISTANCE, WEIGHT, WHEEL_DISTANCE
from shapely.geometry import LineString, Point


class OpenRC:
    dict_name = "open-rc"
    def __init__(self, pixel_pos: np.array, delta: float = 0.1):
        # handling coordinate system in pixel diemnsion
        # calculation:
        #  - pixel-radius * 2 to get car's size in pixel
        #  - then divided by the distance of the car's wheels (given in cm)
        #  - results in amount of pixels per meter
        self._size = CHASSIS_SIZE
        self._pixel_meter_const = CHASSIS_SIZE * 2 / WHEEL_DISTANCE
        self._pos = pixel_pos / self._pixel_meter_const

        # acceleration is calculated based on weight and motor power
        # value in meter per second (already calculated with time)
        self._acceleration = math.sqrt(MOTOR_POWER / WEIGHT) / 2 * delta
        self._velocity = np.array([0, 0], dtype=float)

        # angle to coordinate system's x-axis
        self._theta = INITIAL_THETA

        # simulation related measuremnets
        self._delta = delta

        # create distance sensors
        self.sensor_lines = np.array([np.zeros(2) for _ in range(12)])
        self._update_sensors()
        self._distances = np.array([SENSOR_DISTANCE for sensor in self.sensor_lines])

        self._stop = False
    
    @staticmethod
    def copy(car: "OpenRC") -> "OpenRC":
        pos = car._pos
        delta = car._delta
        size = car._size
        car = OpenRC([0, 0], size, delta)
        car._pos = pos
        return car

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
        self._acceleration = math.sqrt(MOTOR_POWER / WEIGHT) / 2

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
            sensor[0] += math.cos(factor * i - self._theta) * SENSOR_DISTANCE
            sensor[1] += math.sin(factor * i - self._theta) * SENSOR_DISTANCE

            self.sensor_lines[i] = sensor

    def _rotate(self, lines):
        # calculate the current velocity
        vel_left = self._velocity[0] * self._acceleration
        vel_right = self._velocity[1] * self._acceleration
        
        # calculate the movement and rotation
        update_pos = np.zeros_like(self._pos)
        update_pos[0] = +((vel_left + vel_right) / 2) * math.cos(self._theta) * self._delta
        update_pos[1] = -((vel_left + vel_right) / 2) * math.sin(self._theta) * self._delta
        self._pos += update_pos

        # stop if a collision was detected
        collision_detected = self._collision(lines, update_pos)
        if collision_detected:
            # rotate sensor lines
            self._update_sensors()
            return

        self._theta += (vel_right - vel_left) / WHEEL_DISTANCE * self._delta
        self._theta = self._theta % (2 * math.pi)

        # rotate sensor lines
        self._update_sensors()

    def _calc_distances(self, lines):
        """
        calculates distances to all lines for every sensor line
        :param lines: the lines to which the distance is calculated
        """
        car = Point(self._pos)

        # reset each sensor values
        for sensor_num, sensor_point in enumerate(self.sensor_lines):
            sensor_line = LineString([self._pos, sensor_point])
            self._distances[sensor_num] = SENSOR_DISTANCE

            # calulate the current sensor's value for each wall
            for wall in lines:
                wall = LineString(wall)
                hit = sensor_line.intersection(wall)

                if hit:
                    distance = car.distance(hit)

                    # change distance if it is less than the found distance so far
                    if distance < self._distances[sensor_num]:
                        self._distances[sensor_num] = distance

    def _collision(self, lines, update_pos) -> bool:
        """
         calculates collision points of car with all lines
         :param lines: the lines the car collided with
         :return: the true if a collision was detected
        """
        collision = False

        # check if the car hits a wall without a sensor detecting it
        # may occur at corners
        velocity = np.sum(self._velocity * self._acceleration) / 2 * self._delta

        # calculating the car's direction (as a vector)
        dir = np.sign(velocity)
        vect = np.array([math.cos(self._theta), -math.sin(self._theta)])
        vect = vect / np.linalg.norm(vect)

        # calc points in sensor directions for second shapely line
        car = Point(self._pos)
        sensor_points = [Point(sensor) for sensor in self.sensor_lines]
        sensor_lines = [LineString((car, sensor_point)) for sensor_point in sensor_points]

        for wall in lines:
            line = LineString(wall)
            wall = np.asarray(wall)

            # check if the car has collided with a wall
            distance = line.distance(car)
            if distance < WHEEL_DISTANCE / 2:
                # set the car back to the pre-collision point
                self._pos -= update_pos

                # calculate the lines direction vector
                line_vect = [wall[1][0] - wall[0][0], wall[1][1] - wall[0][1]]
                if line_vect[0] == 0 and line_vect[1] == 0:
                    continue
                    
                line_vect = line_vect / np.linalg.norm(line_vect)
                line_vect = line_vect * np.dot(vect * velocity, line_vect) / np.dot(line_vect, line_vect)
                
                # move car along side the wall
                self._pos[0] += line_vect[0]
                self._pos[1] += line_vect[1]
                
                collision = True
        return collision

    def drive(self, lines):
        # transferr walls into the simulations coordinate system
        lines = np.array(lines) / self._pixel_meter_const

        if self._stop:
            self._brake()

            # if the kinetic energy is 0 (or lower) then the car has stopped
            energy = (np.sum(self._velocity) / 2) * WEIGHT
            if energy <= 1:
                self.hard_stop()
                self._stop = False

        # calculate the rotation and movement
        self._rotate(lines)
        self._calc_distances(lines)

        # stop if there was a colision
        # self._collision(lines)

        # transfer back to pixel data
        x = int(self._pos[0] * self._pixel_meter_const)
        y = int(self._pos[1] * self._pixel_meter_const)

        # update the distance lines
        distances = list((self._distances).astype(int))
        sensor_lines = [(int(sensor[0] * self._pixel_meter_const), int(sensor[1] * self._pixel_meter_const))
                        for sensor in self.sensor_lines]

        return -self._theta, x, y, sensor_lines, distances
