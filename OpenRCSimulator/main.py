"""This module handles the app's startup and starting configuration."""
import argparse
import sys
from OpenRCSimulator.gui.configurator_controller import ConfiguratorController
from OpenRCSimulator.gui.creator_controller import CreatorController
from OpenRCSimulator.gui.simulation_controller import SimulationController
from OpenRCSimulator.log.main import start_logging_process


def main():
    """Main method to start the app.
    """
    # add program arguments for configuring the run
    parser = argparse.ArgumentParser()

    parser.add_argument("--create", help="Starts Creation tool. Make sure to provide a name " +
                        "to store the map.", action="store_true")
    parser.add_argument("--manual", help="Loads the manual control mode. Make sure to provide " +
                        "a name to load a map", action="store_true")
    parser.add_argument("--simulation", help="Loads the simulation mode. Make sure to provide " +
                        "a name to load a map", action="store_true")
    parser.add_argument("--train", help="Starts training a agent using EA on the provided map. " +
                        "Provded a config file!")
    parser.add_argument(
        "--name", help="The name of a map (needed to create or load a map).")
    parser.add_argument("--model", help="The trained agent, this contains the NN for " +
                        "controlling the agent.")
    parser.add_argument("--garage", help="Editor to adjust the car measurments and sensors.",
                        action="store_true")
    parser.add_argument("--no-log", help="Start without logging.",
                        action="store_true")

    args = parser.parse_args()

    if not args.no_log:
        start_logging_process()

    # configure car
    if args.garage:
        application = ConfiguratorController(window_size=(1600, 900))
        application.load()
        application.boot()
        sys.exit(0)

    # train an agent
    if args.train:
        # Training module WIP # [todo]
        pass

    # all other modes depend on a map name
    if not args.name:
        print("Provide a map. Exit.")
        sys.exit(1)

    # create a new map
    if args.create:
        application = CreatorController(window_size=(1200, 900))
        application.load(args.name)
        application.boot()
        sys.exit(0)

    # test an agent on a map, or test drive manually
    application = SimulationController(window_size=(1200, 900))
    application.load(args.name, args.model)
    application.boot()
    sys.exit(0)


if __name__ == "__main__":
    main()
