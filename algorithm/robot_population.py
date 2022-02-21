from random import choices
from typing import Tuple, List, Any
from algorithm.robot_genome import RobotGenome


class RobotPopulation:
    def __init__(self, robot_num) -> None:
        self._population = [RobotGenome() for _ in range(robot_num)]

    def _select_pair(self) -> [RobotGenome, RobotGenome]:
        # select two genomes based on their fitness value
        return choices(
            population=self._population,
            weights=[genome.fitness() for genome in self._population],
            k=2
        )

    def run_evolution(self, generation_limit: int = 100, fitness_limit: int = 100) -> tuple[list[Any], int]:
        for i in range(generation_limit):
            # sort the population based on the genome's fitness
            self._population = sorted(
                self._population,
                key=lambda genome: genome.fitness(),
                reverse=True
            )

            # if this generation includes a genome with the maximum fitness specified
            # then break -> best population found
            if self._population[0].fitness() >= fitness_limit:
                break

            # create a new generation based on the best two genomes
            next_generation = self._population[:2]
            for j in range(len(self._population) // 2 - 1):
                # also select parents from the old population
                parents = self._select_pair()

                # and create children using the crossover function
                offspring_a, offspring_b = RobotGenome.crossover(
                    parents[0], parents[1])

                # do not forget to mutate those children to inject the evolutionary approach
                offspring_a.mutate()
                offspring_b.mutate()

                # then add those children to the new generation
                next_generation += [offspring_a, offspring_b]

            # new generation build up -> repeat process
            self._population = next_generation

        # the best population was found (or the limit has been reached)
        # sort the population based on the genome's fitness and return it
        # together with the amount of generations simulated
        population = sorted(
            self._population,
            key=lambda genome: genome.fitness(),
            reverse=True
        )

        return population, i
