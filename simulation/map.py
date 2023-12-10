import yaml
import pickle
import matplotlib.pyplot as plt
import numpy as np
from algorithm.robot_population import RobotPopulation


class Map:
    def __init__(self, name: str) -> None:
        self.__ea = None
        self.__config_name = ""
        self.__simulation_config = name
    
    def load_training_config(self, config_name) -> None:
        # copy the robots so they match the population's size
        with open(f"configs/{config_name}.yaml", "r") as file:
            dict_file: dict = yaml.load(file, Loader=yaml.FullLoader)

        self.__ea = RobotPopulation(**dict_file)
        self.__ea.set_simulation_details(self.__simulation_config)
        self.__config_name = config_name

    def ea_train(self) -> None:
        print("Started training using EA.")
        # train
        population, history = self.__ea.run_evolution()

        # store the best robot
        
        filehandler = open(f"robot_{self.__config_name}.pkl", 'wb') 
        pickle.dump(population[0], filehandler)

        # plot the history using matplot
        font = {'family': 'serif',
            'color':  'darkred',
            'weight': 'normal',
            'size': 16,
        }

        print(history)

        best_fitnesses = history.get("best_fitness", [])
        plt.figure(1)
        plt.subplot(211)
        plt.plot(range(len(best_fitnesses)), best_fitnesses, 'k')
        plt.title('Fitness of best genome', fontdict=font)
        plt.xlabel('Generation', fontdict=font)
        plt.ylabel('Fitness', fontdict=font)

        mean_fitnesses = history.get("mean_fitness", [])
        plt.subplot(212)
        plt.plot(range(len(mean_fitnesses)), mean_fitnesses, 'k')
        plt.title('Mean fitness of population', fontdict=font)
        plt.xlabel('Generation', fontdict=font)
        plt.ylabel('Fitness', fontdict=font)

        # save the generated plots
        plt.savefig(f"plot_{self.__config_name}.png")
