# Mininet Integration

This script was developed with the aim to integrate the built simulation with Mininet Wifi. It reads the already preprocessed data on CSV files containing buses informations (such as latitude and longitude) and send it to both Mininet Wifi and Simulation.

# Setup and Run

- Download and install [Mininet-WiFi Pre-configured Virtual Machine](https://github.com/intrig-unicamp/mininet-wifi/#pre-configured-virtual-machine).
- Open terminal and go inside this folder
  `$ cd path/to/mininet_integration`
- Run `build.sh` shell script:
 `$ sh build.sh`
  - After that, a folder named `dist` will be created.
- Copy the folder `dist` inside the virtual machine folder `/home/wifi/mininet-wifi/mn_wifi/examples` (you may want to rename it for some more convenient name after copying it. Also, a shell script named `deploy.sh` may be helpful if you link a folder from your computer with a VM folder)
  - At the end of this step you may have a folder (with a name such as `dist`) containing the python scripts (`main.py`, `build_simulation.py` and `set_vehicles_positions.py`) and the other directories (`controllers`, `data`, `gym_envs` and `utils`).
- Open the terminal and go inside the folder copied in the previous step
  `$ cd /home/wifi/mininet-wifi/mn_wifi/examples/dist`
- Run the script.
  `$ sudo python main.py`
