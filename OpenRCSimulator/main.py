import argparse
import pygame as py
import OpenRCSimulator.gui as gui
from OpenRCSimulator.gui.configurator_controller import ConfiguratorController
from OpenRCSimulator.gui.main_controller import MainController
from OpenRCSimulator.simulation.trainer import Trainer


def main():
    # add program arguments for configuring the run
    parser = argparse.ArgumentParser()

    parser.add_argument("--create", help="Starts Creation tool. Make sure to provide a name to store the map.", action="store_true")
    parser.add_argument("--manual", help="Loads the manual control mode. Make sure to provide a name to load a map", action="store_true")
    parser.add_argument("--simulation", help="Loads the simulation mode. Make sure to provide a name to load a map", action="store_true")
    parser.add_argument("--train", help="Starts training a agent using EA on the provided map. Provded a config file!")
    parser.add_argument("--name", help="The name of a map (needed to create or load a map).")
    parser.add_argument("--model", help="The trained agent, this contains the NN for controlling the agent.")
    parser.add_argument("--garage", help="Editor to adjust the car measurments and sensors.", action="store_true")

    args = parser.parse_args()

    mode = gui.SIMULATION
    if args.create:
        mode = gui.CREATOR

    if args.manual:
        mode = gui.MANUAL

    if args.train:
        mode = gui.TRAIN

    if args.garage:
        application = ConfiguratorController(window_size=(1200, 900))
        application.load()
        application.boot()
        quit()
        
    if not args.name and mode != gui.TRAIN and mode != gui.GARAGE:
        print("Provide a map. Exit.")
        quit()

    # create the visuals
    if mode != gui.TRAIN:
        application = MainController(window_size=(1200, 900), mode=mode)
        application.file(args.name, args.model)
        application.boot()

    else:
        trainer = Trainer(args.train, args.name)
        trainer.train()


if __name__ == "__main__":
    main()