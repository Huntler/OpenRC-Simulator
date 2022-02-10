import numpy as np
import math


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

        self.midpoint = rotation_matrix * (self.midpoint - icc) + icc
        self._theta = self._theta + omega * delta * t
