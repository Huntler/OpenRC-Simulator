import pickle
from random import choices
import numpy as np
import yaml
import copy
import threading
from typing import Tuple, List, Any
from algorithm.robot_genome import RobotGenome
from commander.sub_controller.robot_controller import ROBOT_SIZE
from simulation.robot import Robot
from simulation.wall import Wall


class RobotPopulation:
    def __init__(self, population, mutation, fitness_limit, generation_limit, simulation_steps, particle_dist) -> None:
        self._mutation_parameter = mutation
        self._fitness_limit = fitness_limit
        self._generation_limit = generation_limit
        self._steps = simulation_steps
        self._particle_dist = particle_dist
        self._population = [RobotGenome() for _ in range(population)]
        self._hist = {}

    def set_simulation_details(self, name: str) -> None:
        # open map file
        with open(f"maps/{name}.yaml", "r") as file:
            dict_file: dict = yaml.load(file, Loader=yaml.FullLoader)

        # load robot
        robot_dict = dict_file.get(Robot.dict_name, None)
        self.__robot = Robot(np.array([robot_dict["x"], robot_dict["y"]]), ROBOT_SIZE, robot_dict["direction"])

        # load all walls
        self.__walls = []
        walls_dict: dict = dict_file.get(Wall.dict_name, None)
        for wall in walls_dict.items():
            wall = wall[1]
            start_pos = (wall["start_x"], wall["start_y"])
            end_pos = (wall["end_x"], wall["end_y"])
            self.__walls.append(Wall(start_pos, end_pos))

        # load width, height
        size_dict = dict_file.get("app", None)
        self._width = size_dict["width"]
        self._height = size_dict["height"]

        for genome in self._population:
            self._set_genome_simulation(genome)

    def _set_genome_simulation(self, genome: RobotGenome) -> None:
        genome.set_simulation_details(copy.copy(self.__robot), self.__walls, self._steps, self._width, self._height, self._particle_dist)

    def _select_pair(self) -> Tuple[RobotGenome, RobotGenome]:
        # select two genomes based on their fitness value
        return choices(
            population=self._population,
            weights=[genome.fitness() for genome in self._population],
            k=2
        )

    def _run_simulation(self) -> None:
        sim_threads = []
        for genome in self._population:
            t = threading.Thread(target=genome.run_simulation)
            sim_threads.append(t)
            # genome.run_simulation()

        # start all simulations simultaneously and wait for all to finish
        for t in sim_threads:
            t.start()
        for t in sim_threads:
            t.join()

    def run_evolution(self) -> tuple[list[Any], int]:
        fitness_limit_reached = False
        for i in range(self._generation_limit):
            # run simulation for each robot to get generate its fitness
            self._run_simulation()

            # sort the population based on the genome's fitness
            self._population = sorted(
                self._population,
                key=lambda genome: genome.fitness(),
                reverse=True
            )

            # save some statistics
            hist = self._hist.get("best_fitness", [])
            best_fitness = self._population[0].fitness()
            hist.append(best_fitness)
            self._hist["best_fitness"] = hist

            hist = self._hist.get("mean_fitness", [])
            mean_fitness = np.mean(np.array([g.fitness() for g in self._population]))
            hist.append(mean_fitness)
            self._hist["mean_fitness"] = hist

            # if this generation includes a genome with the maximum fitness specified
            # then break -> best population found
            if self._population[0].fitness() >= self._fitness_limit:
                fitness_limit_reached = True
                break

            # create a new generation based on the best two genomes
            next_generation = self._population[:2]
            for j in range(len(self._population) // 2 - 1):
                # also select parents from the old population
                parents = self._select_pair()

                # and create children using the crossover function
                offspring_a, offspring_b = RobotGenome.crossover(
                    parents[0], parents[1])
                self._set_genome_simulation(offspring_a)
                self._set_genome_simulation(offspring_b)

                # do not forget to mutate those children to inject the evolutionary approach
                offspring_a.mutate(probability=self._mutation_parameter)
                offspring_b.mutate(probability=self._mutation_parameter)

                # then add those children to the new generation
                next_generation += [offspring_a, offspring_b]

            # new generation build up -> repeat process
            self._population = next_generation

            print(f"In generation {i} with best fitness {best_fitness} and population mean {mean_fitness}.")

        if not fitness_limit_reached:
            self._run_simulation()

        # the best population was found (or the limit has been reached)
        # sort the population based on the genome's fitness and return it
        # together with the amount of generations simulated
        population = sorted(
            self._population,
            key=lambda genome: genome.fitness(),
            reverse=True
        )

        return population, self._hist
