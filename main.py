import argparse
import pygame as py
import commander
from commander.controller import SimulationController


# add program arguments for configuring the run
parser = argparse.ArgumentParser()

parser.add_argument("--create", help="Starts Creation tool. Make sure to provide a name to store the map.", action="store_true")
parser.add_argument("--manual", help="Loads the manual control mode. Make sure to provide a name to load a map", action="store_true")
parser.add_argument("--simulation", help="Loads the simulation mode. Make sure to provide a name to load a map", action="store_true")
parser.add_argument("--name", help="The name of a map (needed to create or load a map).")

args = parser.parse_args()

if not args.name:
    print("Provide a map. Exit.")
    quit()

mode = commander.SIMULATION
if args.create:
    mode = commander.CREATOR

if args.manual:
    mode = commander.MANUAL

# create the visuals
application = SimulationController(window_size=(1200, 900), mode=mode, flags=py.HWSURFACE)
application.file(args.name)
application.boot()

# TODO: manual
# TODO: simulation