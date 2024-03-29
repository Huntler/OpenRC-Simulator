"""This module contains the simulation's required attributes. To be removed 
in the future [todo]"""
import math

# in centimeters
WHEEL_DISTANCE = 12
CHASSIS_SIZE = [18, 32]

# in kilogram
WEIGHT = 1_000

# in Watt
MOTOR_POWER = 30

# coefficient of friction
FRICTION = 1.15

# angle to coordinate system's x-axis in degree
INITIAL_THETA = math.radians(0)
TURNING_BOUNDARIES = [-30, 30]

SENSOR_DISTANCE = 500
SENSOR_POINTS = 350
