import numpy as np
import math

from skspatial.objects import Line, Circle


class Robot:
    def __init__(self, midpoint, l, theta):
        """
        initializes robot
        :param midpoint: midpoint of the robot (in space)
        :param l: distance between the centers of the two wheels
        """

        self.midpoint = midpoint
        self._theta = theta
        self._l = l

        self.l_wheel_pos = (midpoint[0] - l / 2, midpoint[1])
        self.r_wheel_pos = (midpoint[0] + l / 2, midpoint[1])

        pi = math.pi
        self._sensor_lenght = 100
        self.sensor_lines = [
            np.array([self.midpoint[0] + math.cos(2 * pi / 12 * x) * self._sensor_lenght, self.midpoint[1] +
                      math.sin(2 * pi / 12 * x) * self._sensor_lenght])
            for x in range(0, 12 + 1)]
        self.distances = []

    def _calc_velocities(self, omega, r):
        """
        calculates velocities for both wheels
        :param omega: rate of rotation
        :param r: signed distance form icc to the midpoint
        :return: velocities for left and right wheel
        """
        velocity_l = omega(r - self._l / 2)
        velocity_r = omega(r + self._l / 2)

        return velocity_l, velocity_r

    def _calc_r(self, velocity_l, velocity_r):
        """
        calculates the signed distance from icc to the midpoint
        :param velocity_l: velocity of left wheel
        :param velocity_r: velocity of right wheel
        :return: signed distance from icc to the midpoint
        """
        return (self._l / 2) * ((velocity_l + velocity_r) / velocity_r - velocity_l)

    def _calc_omega(self, velocity_l, velocity_r):
        """
        calculates the rate of rotation
        :param velocity_l: velocity of left wheel
        :param velocity_r: velocity of right wheel
        :return: rate of rotation
        """
        return (velocity_r - velocity_l) / self._l

    def _calc_icc(self, velocity_l, velocity_r):
        """
        calaculates the icc
        :param velocity_l: velocity of left wheel
        :param velocity_r: velocity of right wheel
        :return: icc - the point that the robot rotates about
        """
        r = self._calc_r(velocity_l, velocity_r)
        return self.midpoint + np.array([- r * math.sin(self._theta), r * math.cos(self._theta)])

    def rotate(self, t, delta, velocity_l, velocity_r):
        """
        rotates the robot
        :param t: timestep
        :param delta: timestep when robot should be at new position
        :param velocity_l: velocity of left wheel
        :param velocity_r: velocity of right wheel
        """

        omega = self._calc_omega(velocity_l, velocity_r)
        icc = self._calc_icc(velocity_l, velocity_r)

        rotation_matrix = np.array([math.cos(omega * delta * t), - math.sin(omega * delta * t)])

        # rotate robot
        self.midpoint = rotation_matrix * (self.midpoint - icc) + icc
        self._theta = self._theta + omega * delta * t

        # rotate sensor lines
        pi = math.pi
        self.sensor_lines = [
            np.array([self.midpoint[0] + math.cos(2 * pi / 12 * x) * self._sensor_lenght, self.midpoint[1] +
                      math.sin(2 * pi / 12 * x) * self._sensor_lenght])
            for x in range(0, 12 + 1)]

    def calc_distance(self, line):
        """
        calculates distance to a line for every sensor line
        :param line: the line to which the distance should be calculated
        """
        distances = []
        line = Line(point=line[0], direction=line[1])

        for s_line in self.sensor_lines:
            # transform arrays to scikit Lines
            sensor_line = Line(point=self.midpoint, direction=s_line)
            point_intersection = line.intersect_line(sensor_line)
            distance = point_intersection.distance_point(self.midpoint)

            # append distance if it is less than 200
            if distance > 200:
                distances.append(200)
            else:
                distances.append(distance)

        self.distances = distances

    def collision(self, line):
        """
        calculates collision points of robot with a line
        :param line: the line the robot collided with
        :return: the collision points
        """
        robot_body = Circle(self.midpoint, self._l / 2)
        line = Line(line[0], line[1])
        try:
            point_a, point_b = robot_body.intersect_line(line)
        except ValueError:
            return None

        return point_a, point_b


if __name__ == '__main__':
    robot = Robot(np.array([-75, 50]), 10, 0)
    # print(robot.collision([np.array([0, 0]), np.array([7, 7])]))

    # import matplotlib.pyplot as plt
    #
    # fig, ax = plt.subplots()
    #
    # ax.scatter([x[0] for x in robot.sensor_lines], [x[1] for x in robot.sensor_lines], vmin=0, vmax=100)
    # ax.plot(np.linspace(-100, 100, 10), np.linspace(-100, 100, 10))
    # plt.show()
