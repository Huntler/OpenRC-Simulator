import pickle
from random import randint, random, randrange
from typing import List, Tuple

import numpy as np
from shapely.geometry import LineString, Point
from simulation import ROBOT_SENSOR_DISTANCE

from simulation.robot import Robot
from simulation.wall import Wall


class RobotGenome:
    def __init__(self, sensor_num: int = 12, motor_num: int = 2, hidden_layer_size: int = 4) -> None:
        self._motor_num = motor_num

        # randomly initialize the input layer weights
        self._input_layer_weights = np.random.uniform(0, 1, (hidden_layer_size, sensor_num))

        # randomly initialize the output layer weights
        self._output_layer_weights = np.random.uniform(0, 1, (motor_num, hidden_layer_size))

        # randomly initialize shared weights in RNN hidden layer
        self.shared_weights = np.random.uniform(0, 1, (hidden_layer_size, hidden_layer_size))

        # previous activation of hidden layer, initialized with 0s
        self.prevs = np.zeros((hidden_layer_size, 1))

        self._max_particles = 0
        self._fitness_value = 0

    def set_simulation_details(self, robot: Robot, walls: List[Wall], simulation_steps: int, width: int, height: int, particle_dist: int):
        # set simulation details aka robot, walls and simulation steps
        self._robot = robot
        self._walls = walls
        self._simulation_steps = simulation_steps
        self._width = width
        self._height = height
        self._particle_dist = particle_dist

    def run_simulation(self) -> None:
        robot_point = Point(self._robot._pos)
        walls = [LineString([wall._start_pos, wall._end_pos]) for wall in self._walls]
        particles = []

        # generate particles everywhere on the map except "in" the walls
        for x in range(0, self._height, self._particle_dist):
            for y in range(0, self._width, self._particle_dist):
                particle = Point((x, y))
                for wall in walls:
                    if not wall.distance(particle) < 1e-8:  # this might be too small
                        particles.append(particle)

        self._max_particles = len(particles)
        print(f"simulation holds {self._max_particles} particles")

        # drive simulations steps times
        for i in range(self._simulation_steps):
            output_wheels = self.drive()
            if output_wheels[0] < 0:
                self._robot.slowdown_left()
            elif output_wheels[0] > 0:
                self._robot.accelerate_left()

            if output_wheels[1] < 0:
                self._robot.slowdown_right()
            elif output_wheels[1] > 0:
                self._robot.accelerate_right()

            # update particles and fitness value
            new_particles = []
            for particle in particles:
                particle_distance = robot_point.distance(particle)
                if not particle_distance < self._robot._size:
                    new_particles.append(particle)
                else:
                    self._fitness_value += 1
            particles = new_particles

    def _sigmoid(self, x: float) -> float:
        return 1.0 / (1.0 + np.exp(-x))

    def _relu(self, x: float) -> float:
        return x * (x > 0)

    def fitness(self) -> float:
        return self._fitness_value / self._max_particles

    def drive(self) -> Tuple[float]:
        # calc distances from sensors to walls
        self._robot._calc_distances([[wall._start_pos, wall._end_pos] for wall in self._walls])

        # forward passthrough the sensors into our NN to get the motors acceleration
        x = np.dot(self._input_layer_weights, self._robot._distances / ROBOT_SENSOR_DISTANCE)
        w = np.dot(self.shared_weights, self.prevs)
        x = self._relu(x + np.transpose(w))
        self.prevs = np.transpose(x)
        # self._relu(self._activation_func) ?

        x = np.dot(self._output_layer_weights, np.transpose(x))
        print("output layer", x[:, 0])
        left, right = self._sigmoid(x[0]), self._sigmoid(x[1])  # weights are too large -> norm distances ?
        # self._sigmoid(self._activation_func) ?

        # 1 means accelerate, -1 break and 0 nothing
        return np.sign(left), np.sign(right)

    def mutate(self, num: int = 1, probability: float = 0.5) -> None:
        for _ in range(num):
            # chose a layer randomly
            layer = random()
            if layer > 0.5:
                # select a random weight
                index = randrange(len(self._input_layer_weights))

                # change it with a chance of the given probability
                value = self._input_layer_weights[index]
                if random() > probability:
                    value = random()
                self._input_layer_weights[index] = value
            else:
                # select a random weight
                index = randrange(len(self._output_layer_weights))

                # change it with a chance of the given probability
                value = self._output_layer_weights[index]
                if random() > probability:
                    value = random()
                self._output_layer_weights[index] = value

    @staticmethod
    def crossover(a: "RobotGenome", b: "RobotGenome") -> Tuple["RobotGenome", "RobotGenome"]:
        # get the genomes parameter
        sensor_num = len(a._input_layer_weights)
        hidden_layer_size = len(a._output_layer_weights)
        motor_num = a._motor_num

        # and create new ones
        new_a = RobotGenome(sensor_num, motor_num, hidden_layer_size)
        new_b = RobotGenome(sensor_num, motor_num, hidden_layer_size)

        # chose random weights from the provided genomes a and b
        p_1 = randint(1, sensor_num - 1)
        p_2 = randint(1, hidden_layer_size - 1)
        p_3 = randint(1, motor_num - 1)

        # perform crossover for the first layer
        a_crossover = a._input_layer_weights[0:p_1,
                      0:p_2] + b._input_layer_weights[p_1:, p_2:]
        new_a._input_layer_weights = a_crossover

        b_crossover = b._input_layer_weights[0:p_1,
                      0:p_2] + a._input_layer_weights[p_1:, p_2:]
        new_b._input_layer_weights = b_crossover

        # perform crossover for the second layer
        a_crossover = a._output_layer_weights[0:p_2,
                      0:p_3] + b._output_layer_weights[p_2:, p_3:]
        new_a._output_layer_weights = a_crossover

        b_crossover = b._output_layer_weights[0:p_2,
                      0:p_3] + a._output_layer_weights[p_2:, p_3:]
        new_b._output_layer_weights = b_crossover

        return new_a, new_b


if __name__ == "__main__":
    # test save a genome
    genome = RobotGenome()
    filehandler = open(f"robot_training_conf_1.pkl", 'wb')
    pickle.dump(genome, filehandler)
