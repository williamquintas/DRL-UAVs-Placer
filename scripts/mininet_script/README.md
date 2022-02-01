# Mininet Script

This script was developed with the aim to read the already preprocessed data on CSV files containing buses informations (such as latitude and longitude). These data will be used on this script to position Mininet Wifi network nodes.

# Setup and Run

- Download and install [Mininet-WiFi Pre-configured Virtual Machine](https://github.com/intrig-unicamp/mininet-wifi/#pre-configured-virtual-machine).
- Copy this folder (mininet_script) inside the virtual machine folder `/home/wifi/mininet-wifi/mn_wifi/examples` (you may want to rename it for some more convenient name after copying it, e.g. **mn_wifi/examples/csv**)
  - At the end of this step you may have a folder (with a name such as `csv`) containing the python scripts (`place_hosts_from_csv.py` and `setNodePosition.py`) and the `data` directory (that contains the CSV file.
- Open the terminal and go inside the folder copied in the previous step
  `$ cd /home/wifi/mininet-wifi/mn_wifi/examples/csv`
- Run the script.
  `$ sudo python place_hosts_from_csv.py`
