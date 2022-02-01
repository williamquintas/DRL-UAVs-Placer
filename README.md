# DRL UAVs Placer

This repository contains material related to a project that uses Deep Reinforcement Learning (DRL) to determine the Unmanned Aerial Vehicles (UAV) position in order to improve the fairness and efficiency of network resource allocation.
It is being developed as a Scientific Initiation and Final Work for the Undergraduation of William Quintas, oriented by [Prof. Dr. Christian Rothenberg](https://www.dca.fee.unicamp.br/~chesteve/).

# Dependencies

- [Pipenv 2021.5.29](https://pipenv.pypa.io/en/latest/)
- [Python 3.9](https://www.python.org/downloads/release/python-390/)
- [Matplotlib 3.5.1](https://matplotlib.org/)
- [Numpy 1.21.4](https://numpy.org/)
- [Open AI Gym 0.21.0](https://gym.openai.com/)

# Setup

- Download and install **Python** from [here](https://www.python.org/downloads/).
  - You might make sure you have Python and that it’s available from your command line. You can check this by simply running:
    `$ python --version`
  - Additionally, you’ll need to make sure you have pip available. You can check this by running:
    `$ pip --version`
- Install **Pipenv** following the instructions from [here](https://pipenv.pypa.io/en/latest/install/#pragmatic-installation-of-pipenv).
  `$ pip install --user pipenv`
  - You can check if the installation was successful by running:
    `$ pipenv --version`
- Clone this repository.
  `$ git clone https://github.com/williamquintas/DRL-UAVs-Placer.git /path/to/repo`
- Install the dependencies.

```
cd /path/to/repo
pipenv install
```

# Files

This repository files are structured as follows:

```
|── controllers
|   |── host.py
|   |── simulation.py
|   |── uav.py
|── gym_envs
|   |── envs
|   |   |── uav_placer_env.py
|── utils
|   |── constants.py
|   |── location.py
|── main.py
|── simple_simulation.py
```

- `controllers`: folder containing the controllers. For now, only **host**, **uav** and **simulation** controllers were created.
- `gym_envs`: folder used to group settings files used in Open AI Gym custom environment.
- `utils`: folder containing utils files. It is a good practice to group functions of different entities in different utils files.
- `main.py`: main file of the repository, contains the Open AI Gym environment declaration and runs simulation (see in the section above how to run it using scripts).
- `simple_simulation.py`: file that creates a simulation without running Open AI Gym, can be used to simply see Hosts and UAVs properties (see in the section above how to run it using scripts).

# Scripts

Two scripts were declared in `Pipfile`:

- `[main]`: runs the full simulation in `main.py`. Can be called using
  `$ pipenv run main`
- `[simple]`: runs the simple simulation in `simple_simulation.py`. Can be called using
  `$ pipenv run simple`

# Integration with Mininet-WiFi

An integration with [Mininet-WiFi](https://github.com/intrig-unicamp/mininet-wifi) is being developed.
For now, an example script was developed to place network nodes reading data from a CSV. More info can be found [here](./scripts/mininet_script)

In the future, we aim to fully integrate the Deep Reinforcement Learning model developed with the Mininet-WiFi emulator and CoppeliaSim.

# External References

_TODO: reference article_
