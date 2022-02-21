from random import randint, random, randrange
from typing import List, Tuple

import numpy as np


class RobotGenome:
    def __init__(self, sensor_num: int = 12, motor_num: int = 2, hidden_layer_size: int = 4) -> None:
        # randomly initialize the input layer weights
        self._input_layer_weights = np.array(
            [[random() for _ in range(hidden_layer_size)] for _ in range(sensor_num)])

        # randomly initilize the output layer weights
        self._output_layer_weights = np.array(
            [[random() for _ in range(motor_num)] for _ in range(hidden_layer_size)])

        self._sigmoid = lambda x: 1.0 / (1.0 + np.exp(-x))
        self._relu = lambda x: x * (x > 0)

    def fitness(self, benchmark_func) -> float:
        pass

    def drive(self, sensors: np.ndarray) -> Tuple[float]:
        # forward passthrough the sensors into our NN to get the motors acceleration
        x = self._input_layer_weights * sensors
        x = self._relu(self._activation_func)

        x = self._output_layer_weights * x
        x = self._sigmoid(self._activation_func)

        # 1 means accelerate, -1 breake and 0 nothing
        return np.sign(x)

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
        motor_num = a._output_layer_weights.shape[0] * \
                    a._output_layer_weights.shape[1] / hidden_layer_size

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
    print(np.sign([-123, 0.435]))
