#!/usr/bin/python

'Example of hostss being positioned using CSV data'

import time
import os

from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.telemetry import telemetry
from mn_wifi.wmediumdConnector import interference


def topology():
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    dr1 = net.addStation('dr1', mac='00:00:00:00:00:01', ip='10.0.0.1/8',
                         position='30,60,0')

    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    net.addLink(dr1, cls=adhoc, intf='dr1-wlan0',
                ssid='adhocNet', proto='batman_adv',
                mode='g', channel=5, ht_cap='HT40+')

    info("*** Starting network\n")
    net.build()

    nodes = net.stations
    telemetry(nodes=nodes, single=True, data_type='position')

    sta_drone = []
    for n in net.stations:
        sta_drone.append(n.name)
    sta_drone_send = ' '.join(map(str, sta_drone))

    # # set_socket_ip: localhost must be replaced by ip address
    # # of the network interface of your system
    # # The same must be done with socket_client.py
    info("*** Starting Socket Server\n")
    net.socketServer(ip='127.0.0.1', port=12345)

    info("*** Configure the node position\n")
    path = os.path.dirname(os.path.abspath(__file__))
    setNodePosition = 'python {}/setNodePosition.py {} &'.format(
        path, sta_drone_send)
    os.system(setNodePosition)

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    kill_process()
    net.stop()


def kill_process():
    os.system('pkill -9 -f setNodePosition.py')
    # os.system('rm examples/csv/data/*')


if __name__ == '__main__':
    setLogLevel('info')
    # Killing old processes
    kill_process()
    topology()
