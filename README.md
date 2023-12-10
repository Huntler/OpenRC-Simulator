# OpenRC Simulator

This repository originated from an university project within the scope of autonomous robotic systems (ARS) and was uesed to train a cleaning robot based on an evolutionary algorithm (EA). The legacy code can be found in the release section with the tag `ARS-EA`.

Now, the repository is used to simulate the OpenRC, a 3D printable racing car. The aim of this project is to equip the car with sensors to enable autonoums driving based on a trained agent. If you want to build such a car on your own, head to thingiverse: [OpenRC Print Files](https://www.thingiverse.com/thing:42198)

## Installation/Development Environment

Currently, there is no distinct installation. To execute the simulation, download the code and install [Python](https://www.python.org/) with [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html). 

1. Install Miniconda

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh Miniconda3-latest-Linux-x86_64.sh
rm Miniconda3-latest-Linux-x86_64.sh
```

2. Clone the repository / get requirements

```
git clone https://github.com/Huntler/OpenRC-Simulator.git
conda create env -f OpenRC-Simulator/conda-env/env.yml
```

## Usage

Always make sure to activate the conda environment before executing any code. Also, each command assumes that you are in the root directory of the code `OpenRC-Simulator`.

```
conda activate openrc-sim
```

### Map Editor

The map editor is a handy tool to create scenarios with different levels of complexity. To start the editor, call:

```
python main.py --name <MAP_NAME> --create
```

Replace `<MAP_NAME>` with a name of your choice. With the window opened, press `p` to start drawing mode and add some walls to your map. If you have finished adding walls, press `p` again. Finally, press `r` to place the car at a spot of your liking. Do not forget to save your creation my pressing `s`. The maps are stored in `maps/` as `yaml`-files. 

### Testing 

There is an option to manually drive the car on your map. 

```
python main.py --name <MAP_NAME> --manual
```

### Training

The code tries to sqeeuze as much performance as possible when enabling training mode. Therefore, the GUI is disabled when training an agent.

```
python main.py --name <MAP_NAME> --train <CONFIG_NAME>
```

Replace `<CONFIG_NAME>` with a configuration as `yaml`-file which is read and passed as parameters to the simulated OpenRC. E.g.:

```
WIP
```

Configuration files are always stored in `config/`.

### Loading a Trained Model

Trained agents are stored in `models` and can be loaded into a simulation of your liking as follows:

```
python main.py --agent <MODEL_NAME> --name <MAP_NAME> --simulation 
```

## Future
[ ] Train on all maps randomly
[ ] Print training progress
[ ] Convert simulation to OpenAI Gym