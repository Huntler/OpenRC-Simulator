from functools import partial
from random import choices, randint, randrange
from random import random
from typing import Callable, List, Tuple


genome = List[int]
population = List[genome]
FitnessFunc = Callable[[genome], int]
PopulateFunc = Callable[[], population]
SelectionFunc = Callable[[population, FitnessFunc], Tuple[genome, genome]]
CrossoverFunc = Callable[[genome, genome], Tuple[genome, genome]]
MutationFunc = Callable[[genome], genome]


def generate_genome(lenght: int) -> genome:
    return choices([0, 1], k=lenght)


def generate_population(size: int, genome_length: int) -> population:
    return [generate_genome(genome_length) for _ in range(size)]


def fitness(genome: genome, sensors: List[float], weight_limit: int) -> int:
    if len(genome) != len(sensors):
        raise ValueError("Lenght of sensors and genomes must match.")

    weight = 0
    value = 0
    # calculate the fitness of a genome based on the list of sensors
    # near to a wall -> lower distances -> lower fitness
    for i, sensor in enumerate(sensors):
        if genome[i] == 1:
            # each sensor has the same weight attached to it
            weight += 1
            value += sensor

            if weight > weight_limit:
                return 0

    return value


def selection_pair(population: population, fitness_func: FitnessFunc) -> population:
    # select two genomes based on their fitness value
    return choices(
        population=population,
        weights=[fitness_func(genome) for genome in population],
        k=2
    )


def single_point_crossover(a: genome, b: genome) -> Tuple[genome, genome]:
    if len(a) != len(b):
        raise ValueError("Dimension of genomes a and b must match.")

    # if length to short, then crossover not needed
    length = len(a)
    if length < 2:
        return a, b

    # do a random crossover
    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]


def mutation(genome: genome, num: int = 1, probability: float = 0.5) -> genome:
    # mutate the amount of values (num) in the genome with a given probability
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random(
        ) > probability else abs(genome[index] - 1)

    return genome


def run_evolution(populate_func: PopulateFunc,
                  fitness_func: FitnessFunc,
                  fitness_limit: int,
                  selection_func: SelectionFunc = selection_pair,
                  crossover_func: CrossoverFunc = single_point_crossover,
                  mutation_func: MutationFunc = mutation,
                  generation_limit: int = 100
                  ) -> Tuple[population, int]:

    population = populate_func()

    # run for (at most) as many generations as specified
    for i in range(generation_limit):
        # sort the population based on the genome's fitness
        population = sorted(
            population,
            key=lambda genome: fitness_func(genome),
            reverse=True
        )

        # if this generation includes a genome with the maximum fitness specified
        # then break -> best population found
        if fitness_func(population[0]) >= fitness_limit:
            break

        # create a new generation based on the best two genomes
        next_generation = population[:2]
        for j in range(len(population) // 2 - 1):
            # also select parents from the old population
            parents = selection_func(population, fitness_func)

            # and create childrens using the crossover function
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])

            # do not forget to mutate those children to inject the evolutionary approach
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)

            # then add those children to the new generation
            next_generation += [offspring_a, offspring_b]

        # new generation build up -> repeat process
        population = next_generation

    # the best population was found (or the limit has been reached)
    # sort the population based on the genome's fitness and return it
    # together with the amount of generations simulated
    population = sorted(
        population,
        key=lambda genome: fitness_func(genome),
        reverse=True
    )
    return population, i


if __name__ == "__main__":
    sensors = [20, 20, 20, 15, 10, 15, 20, 20, 20, 20, 20, 20]
    population, generations = run_evolution(
        populate_func=partial(
            generate_population, size=10, genome_length=12
        ),
        fitness_func=partial(
            fitness, sensors=sensors, weight_limit=20
        ),
        fitness_limit=100,
        generation_limit=100,

    )

    print("number of generations:", generations)
    print(population)
