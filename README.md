# OpenRC Simulator

This repository originated from an university project within the scope of autonomous robotic systems (ARS) and was uesed to train a cleaning robot based on an evolutionary algorithm (EA). The legacy code can be found in the release section with the tag `ARS-EA`.

Now, the repository is used to simulate the OpenRC, a 3D printable racing car. The aim of this project is to equip the car with sensors to enable autonoums driving based on a trained agent. If you want to build such a car on your own, head to thingiverse: [OpenRC Print Files](https://www.thingiverse.com/thing:42198)

## Installation/Development Environment

The installation candidates can be found in the [release](https://github.com/Huntler/OpenRC-Simulator/releases) section and are installed as [Python](https://www.python.org/) package. Alternatively, follow these steps to build and install the simulator for your system.

1. Clone the repository

```
git clone https://github.com/Huntler/OpenRC-Simulator.git
```

2. Build & Install

Within the cloned repository, type:

```
pip install .
```

## Usage

The simulator delivers a map editor to create maps (editing maps is WIP), a testing environment to load a trained agent on a map (WIP), a training mode which disables the GUI for maximum efficiency, and a manual mode to test a created map. 

### Map Editor

The map editor is a handy tool to create scenarios with different levels of complexity. To start the editor, call:

```
openrc-sim --name <MAP_NAME> --create
```

Replace `<MAP_NAME>` with a name of your choice. With the window opened, press `p` to start drawing mode and add some walls to your map. If you have finished adding walls, press `p` again. Finally, press `r` to place the car at a spot of your liking. Do not forget to save your creation my pressing `s`.

### Manual 

There is an option to manually drive the car on your map. 

```
openrc-sim --name <MAP_NAME> --manual
```

### Training

The code tries to sqeeuze as much performance as possible when enabling training mode. Therefore, the GUI is disabled when training an agent.

```
openrc-sim --name <MAP_NAME> --train <CONFIG_NAME>
```

Replace `<CONFIG_NAME>` with a configuration as `yaml`-file which is read and passed as parameters to the simulated OpenRC. E.g.:

```
WIP
```

Configuration files are always stored in `$HOME/.openrc-sim/config/` on linux and `%appdata%/OpenRC-Sim/config` on windows. The config editor is WIP.

### Simulation

Trained agents can be loaded into a simulation of your liking as follows:

```
openrc-sim --agent <MODEL_NAME> --name <MAP_NAME> --simulation 
```

## Future
[ ] Train on all maps randomly
[ ] Print training progress
[ ] Convert simulation to OpenAI Gym