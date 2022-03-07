import yaml
import pickle
from algorithm.robot_population import RobotPopulation


class Map:
    def __init__(self, name: str) -> None:
        self.__ea = None
        self.__config_name = ""
        self.__simulation_config = name
    
    def load_training_config(self, config_name) -> None:
        # copy the robots so they match the population's size
        with open(f"ea_configs/{config_name}.yaml", "r") as file:
            dict_file: dict = yaml.load(file, Loader=yaml.FullLoader)

        self.__ea = RobotPopulation(**dict_file)
        self.__ea.set_simulation_details(self.__simulation_config)
        self.__config_name = config_name

    def ea_train(self) -> None:
        # train
        population, history = self.__ea.run_evolution()

        # store the best robot
        filehandler = open(f"robot_{self.__config_name}.pkl", 'wb') 
        pickle.dump(population[0], filehandler)

        # plot the history using matplot
        # TODO: can be done after training is implemented

        # save the generated plots
        # TODO: can be done after training is implemented
