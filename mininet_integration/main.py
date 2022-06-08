import time
import os

from mininet.log import setLogLevel
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from utils.constants import MININET_SOCKET_PORT


def kill_command(filename: str) -> None:
    path = os.path.dirname(os.path.abspath(__file__))
    os.system('pkill -9 -f {}/{}.py'.format(path, filename))


def run_command(filename: str, args: str = None) -> None:
    path = os.path.dirname(os.path.abspath(__file__))
    command = "python {}/{}.py".format(path, filename)
    if args:
        command += (" " + args)
    os.system("{} &".format(command))


def create_topology() -> Mininet_wifi:
    "Create simulation topology."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    print("*** Creating nodes\n")
    uav1 = net.addAccessPoint('uav1', ssid='uav1', mode='g', channel='5',
                             position='5,5,0')
    vehicle1 = net.addStation('vehicle1', mac='00:00:00:00:00:01', ip='10.0.0.1/8',
                              position='0,0,0')
    vehicle2 = net.addStation('vehicle2', mac='00:00:00:00:00:02', ip='10.0.0.2/8',
                              position='10,10,0')
    h1 = net.addHost('h1', mac='00:00:00:00:00:03', ip='10.0.0.3/8')

    net.setPropagationModel(model="logDistance", exp=1.5)

    print("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    print("*** Associating Stations\n")
    net.addLink(vehicle1, uav1)
    net.addLink(vehicle2, uav1)
    net.addLink(h1, uav1)

    print("*** Starting network\n")
    net.build()
    uav1.start([])

    print("*** Starting Socket Server\n")
    net.socketServer(ip='127.0.0.1', port=MININET_SOCKET_PORT)

    print("*** Starting CSV reader\n")
    stations_names_list = map(lambda station: station.name, net.stations)
    stations_names_str = ' '.join(map(str, stations_names_list))
    kill_command("build_simulation")
    kill_command("set_vehicles_positions")
    run_command("build_simulation", stations_names_str)
    time.sleep(1) # Required to wait simulation run before receiving commands
    run_command("set_vehicles_positions", stations_names_str)

    return net


if __name__ == '__main__':
    setLogLevel('info')

    # Starting simulation
    net = create_topology()

    print("*** Running CLI\n")
    CLI(net)

    print("*** Stopping network\n")
    kill_command("set_vehicles_positions")
    kill_command("build_simulation")
    net.stop()
