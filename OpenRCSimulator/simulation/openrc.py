"""This module represents the car used within the backend simulation, including the physics."""
from typing import List, Tuple
import math

from shapely.geometry import LineString, Point
import numpy as np

from OpenRCSimulator.graphics import CENTIMETER_TO_PIXEL, PIXEL_TO_CENTIMETER
from OpenRCSimulator.simulation import CHASSIS_SIZE, INITIAL_THETA, MOTOR_POWER, \
    SENSOR_DISTANCE, SENSOR_POINTS, TURNING_BOUNDARIES, WEIGHT


class OpenRC:
    """This class simulates the racing car based on the car's configuration such as size and weight.
    The car is able to drive forwards, backwards, steer to both sides, and it can break.
    """

    def __init__(self, pixel_pos: np.array, delta: float = 0.1):
        self._dict_name = "open-rc"
        # handling coordinate system in pixel diemnsion
        # calculation:
        #  - pixel-radius * 2 to get car's size in pixel
        #  - then divided by the distance of the car's wheels (given in cm)
        #  - results in amount of pixels per meter
        self._size = CHASSIS_SIZE
        self._pos = pixel_pos * PIXEL_TO_CENTIMETER

        # acceleration is calculated based on weight and motor power
        # value in meter per second (already calculated with time)
        self._acceleration = math.sqrt(MOTOR_POWER / WEIGHT) / 2 * delta
        self._velocity = 0
        self._turn_angle = 0

        # angle to coordinate system's x-axis
        self._theta = INITIAL_THETA

        # simulation related measuremnets
        self._delta = delta

        # create distance sensorsa
        self.sensor_lines = np.array([np.zeros(2)
                                     for _ in range(SENSOR_POINTS)])
        self._distances = np.array(
            [SENSOR_DISTANCE for sensor in self.sensor_lines])

        self._stop = False

    @property
    def dict_name(self) -> str:
        """The dict name is handy to pickle this object.

        Returns:
            str: The name of this class.
        """
        return self._dict_name

    def set_position(self, position: Tuple[float, float], pixel: bool = False) -> None:
        """This method places the car to a specified (real-world/pixel) coordinate.

        Args:
            position (Tuple[float, float]): The coordinate.
            pixel (bool, optional): If true, the given coordinates are pixels, otherwise 
            centimeter coordinates. Defaults to False.
        """
        if pixel:
            self._pos = position
        else:
            self._pos = position * CENTIMETER_TO_PIXEL

    def copy(self) -> "OpenRC":
        """Copies this object.

        Returns:
            OpenRC: The copied object.
        """
        delta = self._delta
        car = OpenRC([0, 0], delta)
        car.set_position(self._pos)

        return car

    def hard_stop(self):
        """This method instantly stops the car, ignoring physics.
        """
        self._velocity = 0

    def reset_acceleration(self):
        """This method simulates motors turned off.
        """
        self._stop = True

    def reset_turn(self):
        """This method simulates leaving the steering wheel.
        """
        self._turn_angle = 0

    def accelerate(self):
        """This method accelerates the car by a fixed amount.
        """
        self._velocity += 1
    
    def accelerate_backwards(self):
        """Drives the car backwards
        """
        self._velocity -= 1

    def slowdown(self, road_resistance: float = 1.005):
        """This method slows down the car by a fixed amount.
        """
        self._velocity /= road_resistance

    def turn_left(self):
        """This method turns the car left.
        """
        # TODO: add acceleration
        self._turn_angle = min(TURNING_BOUNDARIES[1], self._turn_angle + 1)

    def turn_right(self):
        """This method turns the car right.
        """
        # TODO: add acceleration
        self._turn_angle = max(TURNING_BOUNDARIES[0], self._turn_angle - 1)

    def set_time_delta(self, delta: float):
        """This method sets the delta time between each frame, which is needed to decouple
        simulation and visualization. A smaller delta means more frequent simulation calls.

        Args:
            delta (float): Should be low if the simulation is executed frequently.
        """
        self._delta = delta

        # update the acceleration for the frame which has been drawn in delta time
        self._acceleration = math.sqrt(MOTOR_POWER / WEIGHT) / 2

    def brake(self, brake_const: float = 2):
        self._velocity /= brake_const

    def _update_sensors(self, lines):
        # the factor which is used to get the sensors end position
        factor = 2 * math.pi / SENSOR_POINTS

        # iterate of each sensor
        for i, _ in enumerate(self.sensor_lines):
            # and create its stock position
            sensor = np.array([
                self._pos[0] + math.cos(factor * i),
                self._pos[1] + math.sin(factor * i)
            ])

            # create a temporary sensor
            temp_sensor = sensor.copy()
            temp_sensor[0] += math.cos(factor * i -
                                       self._theta) * SENSOR_DISTANCE
            temp_sensor[1] += math.sin(factor * i -
                                       self._theta) * SENSOR_DISTANCE

            # calculate distances
            distance = self._calc_distance(lines, temp_sensor)
            self._distances[i] = distance

            # update the sensor
            sensor[0] += math.cos(factor * i - self._theta) * distance
            sensor[1] += math.sin(factor * i - self._theta) * distance

            self.sensor_lines[i] = sensor

    def _update_state(self, lines) -> bool:
        # calculate Pro-Ackerman condition of car turning
        turning_angle = math.radians(180 - 90 - (90 - self._turn_angle))
        rear_radius = CHASSIS_SIZE[1] / math.tan(
            turning_angle) - 0.5 * CHASSIS_SIZE[0] if turning_angle != 0 else 0

        # calculate the current velocity
        velocity = self._velocity * self._acceleration
        print("velocity (internal):", self._velocity)
        print("velocity (calculated in km/h):", velocity * 0.036)
        print("acceleration:", self._acceleration)
        print("turn:", self._turn_angle)

        # calculate the vehicles angle emplyoing the distance traveled: distance = velocity * time
        theta = self._theta + \
            math.tanh(velocity * self._delta) / \
            rear_radius if rear_radius != 0 else self._theta
        theta = theta % (2 * math.pi)
        self._theta = theta

        # calculate the movement and rotation
        update_pos = np.zeros_like(self._pos)
        update_pos[0] = velocity * math.cos(theta) * self._delta
        update_pos[1] = -velocity * math.sin(theta) * self._delta

        # stop if a collision was detected
        collision_detected = self._collision(lines, theta, update_pos)
        if collision_detected:
            return False, np.zeros_like(self._pos)

        # update position and agle
        self._pos += update_pos

        return True

    def _calc_distance(self, lines, sensor_point: List[float]):
        """
        calculates distances to all lines for every sensor line
        :param lines: the lines to which the distance is calculated
        """
        car = Point(self._pos)

        # reset each sensor values
        sensor_line = LineString([self._pos, sensor_point])

        # calulate the current sensor's value for each wall
        min_distance = SENSOR_DISTANCE
        for wall in lines:
            wall = LineString(wall)
            hit = sensor_line.intersection(wall)

            if hit:
                # change distance if it is less than the found distance so far
                min_distance = min(min_distance, car.distance(hit))

        return min_distance

    def _collision(self, lines, theta, update_pos) -> bool:
        """Calculates the collision of the car with walls,.

        Args:
            lines (np.array): Array of walls.
            theta (float): Current angle of the car.
            update_pos (np.array): Update to the car's position.

        Returns:
            bool: True if collision is detected.
        """
        # check if the car hits a wall without a sensor detecting it
        # may occur at corners
        velocity = self._velocity * self._acceleration * self._delta

        # calculating the car's direction (as a vector)
        vect = np.array([math.cos(theta), -math.sin(theta)])
        vect = vect / np.linalg.norm(vect)

        # calc points in sensor directions for second shapely line
        future_position = Point(self._pos + update_pos)
        sliding_position = Point(self._pos)
        collisions = 0
        for wall in lines:
            line = LineString(wall)
            wall = np.asarray(wall)

            # check if the car has collided with a wall
            distance = line.distance(future_position)
            if distance < CHASSIS_SIZE[1] / 2:
                collisions += 1

                # calculate the lines direction vector
                line_vect = [wall[1][0] - wall[0][0], wall[1][1] - wall[0][1]]
                if line_vect[0] == 0 and line_vect[1] == 0:
                    continue

                # calculate the car's new direction (sliding along a wall)
                line_vect = line_vect / np.linalg.norm(line_vect)
                line_vect = line_vect * \
                    np.dot(vect * velocity, line_vect) / \
                    np.dot(line_vect, line_vect)
                
                sliding_position = Point(sliding_position.x + line_vect[0], 
                                         sliding_position.y + line_vect[1])

        if collisions == 0:
            return False

        # only one collision, the car slides along a wall
        if collisions == 1:
            self._pos = [sliding_position.x, sliding_position.y]
            return True

        # if the car collides with more than one wall, stop it
        return True

    def drive(self, lines: List, controls: np.array):
        """This method simulates one simulation tick. To be accurate with the real time,
        a tick should happen every self.delta seconds. Use the set_time_delta() method.

        Args:
            lines (List): A list of points representing the walls on the map.   
            controls (np.array): The control input of the car (accelerate, backwards, left, right)

        Returns:
            Tuple: Current orientation, x, y, sensors, measured distances
        """
        # transferr walls into the simulations coordinate system
        lines = np.array(lines) * PIXEL_TO_CENTIMETER

        # apply the controls
        if controls.any():
            if controls[0]:
                self.accelerate()
            
            if controls[1]:
                self.accelerate_backwards()
            
            if controls[2]:
                self.brake()

            if controls[3]:
                self.turn_left()
            
            if controls[4]:
                self.turn_right()

        if not controls[0] and not controls[1] and not controls[2]:
            self.slowdown()
        
        if not controls[3] and not controls[4]:
            self._turn_angle = self._turn_angle / 2
            if self._turn_angle < 0.5:
                self.reset_turn()

        # if the kinetic energy is 0 (or lower) then the car has stopped
        energy = (np.sum(self._velocity) / 2) * WEIGHT
        if energy <= 1:
            self.hard_stop()

        # calculate the rotation and movement
        self._update_sensors(lines)
        if not self._update_state(lines):
            self.hard_stop()

        # transfer back to pixel data
        x = int(self._pos[0] * CENTIMETER_TO_PIXEL)
        y = int(self._pos[1] * CENTIMETER_TO_PIXEL)

        # update the distance lines
        distances = list((self._distances).astype(int))
        sensor_lines = [(int(sensor[0] * CENTIMETER_TO_PIXEL), int(sensor[1] * CENTIMETER_TO_PIXEL))
                        for sensor in self.sensor_lines]

        return -self._theta, x, y, sensor_lines, distances
