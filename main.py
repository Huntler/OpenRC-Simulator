import argparse
import pygame as py
import commander
from commander.controller import SimulationController
from simulation.map import Map


# add program arguments for configuring the run
parser = argparse.ArgumentParser()

parser.add_argument("--create", help="Starts Creation tool. Make sure to provide a name to store the map.", action="store_true")
parser.add_argument("--manual", help="Loads the manual control mode. Make sure to provide a name to load a map", action="store_true")
parser.add_argument("--simulation", help="Loads the simulation mode. Make sure to provide a name to load a map", action="store_true")
parser.add_argument("--train", help="Starts training a robot using EA on the provided map. Provded a config file!")
parser.add_argument("--name", help="The name of a map (needed to create or load a map).")
parser.add_argument("--robot", help="The trained robot, this contains the NN for controlling the robot.")

args = parser.parse_args()

if not args.name:
    print("Provide a map. Exit.")
    quit()

mode = commander.SIMULATION
if args.create:
    mode = commander.CREATOR

if args.manual:
    mode = commander.MANUAL

if args.train:
    mode = commander.TRAIN

# create the visuals
if mode != commander.TRAIN:
    application = SimulationController(window_size=(1200, 900), mode=mode, flags=py.HWSURFACE)
    application.file(args.name, args.robot)
    application.boot()

else:
    map = Map(args.name)
    map.load_training_config(args.train)
    map.ea_train()

# TODAY'S TODOS
# DONE: simulation - when startet, then load a trained robot
# DONE: walls should be loaded as UI independent object, so we can access them without having the UI active
# DONE: training - start the program without a UI and execute the training process
# TODO: fitness function based on 1. map covered (unique, so driving on spot is not rewarded) [optional 2. time (less time is better)]
# DONE: current neural network is feed forward, we need to have a recurrent neural network
# DONE: add metric measurements to the training loop and TODO: plot/save them in the end
# DONE: we need to store the best robot (using pickle?) so we can load it later on into the simulation
# TODO: add some kind of progress report while training (into the console should be sufficient)
# DONE: add a yaml configuration file to specify population, random mutation, aso.

# MIDNIGHT'S TODOS
# TODO: start a training to check everything works -> debug :(

# TOMORROW'S TODOS
# TODO: start a few trainings with different parameters
# TODO: analyze those results and create a video from it
# TODO: then upload the video and code, don't forget to add credentials