# GitHub repository: https://github.com/Huntler/ARS-Simulator
# start Creator:    python main.py --create --name MAP_NAME
# start Manual:     python main.py --manual --name MAP_NAME
# start Training:   python main.py --train CONFIG_NAME --name MAP_NAME
# start Simulation: python main.py --simulation --robot ROBOT_NAME --name MAP_NAME

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
