#!/usr/bin/python
from utils.constants import SIMULATION_SOCKET_PORT
from controllers.simulation import SimulationController, SimulationRendererController
import socket
import sys
import threading

sys.path.append('.')

SET_POSITION = "set_position"
SET_RX_TX = "set_rx_tx"
COMMANDS = [SET_POSITION, SET_RX_TX]


class SimulationRunner:
    def __init__(self, vehicles_names: list):
        self._simulation = SimulationController(hosts_names=vehicles_names, host_quantity=2, uav_quantity=1)
        self._renderer = SimulationRendererController(self._simulation, title="Integration with Mininet")
        self._server = self._build_server('127.0.0.1', SIMULATION_SOCKET_PORT)

    def _build_server(self, host: str, port: int):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)
        print("Simulation socket listening on {}:{}\n".format(host, port))
        return server

    def _process_set_position(self, hostname: str, **kwargs):
        hosts = self._simulation.get_hosts()
        host = list(filter(lambda h: h.get_id() == hostname, hosts))
        if(host):
            host[0].set_position(kwargs)
        else:
            print("No host found with id {}.".format(hostname))
        self._renderer.render()

    def _process_set_rx_tx(self, hostname: str, data_list: list):
        hosts = self._simulation.get_hosts()
        host = list(filter(lambda h: h.get_id() == hostname, hosts))
        if(host):
            host[0].set_data_communicated_list(data_list)
        else:
            print("No host found with id {}.".format(hostname))
        self._renderer.render()

    def _process_command(self, command: str, hostname: str, *args) -> None:
        if command == SET_POSITION:
            coordinates = list(map(float, args[0]))
            self._process_set_position(hostname, x=coordinates[0], y=coordinates[1])
        elif command == SET_RX_TX:
            data_list = args[0]
            self._process_set_rx_tx(hostname, data_list)
        else:
            print("Command {} is not known. \n Accepted commands: {}".format(
                command,
                ", ".join(COMMANDS)
            ))

    def on_new_connection(self, connection: socket) -> None:
        while True:
            data = connection.recv(1024).decode('utf-8')
            if data != '':
                hostname, command, *arguments = data.split(' ')
                self._process_command(command, hostname, arguments)
        connection.close()

    def receive_data_on_server(self) -> None:

        while True:
            connection, _ = self._server.accept()

            connection_thread = threading.Thread(target=self.on_new_connection, args=(connection,))
            connection_thread.setDaemon(True)
            connection_thread.start()

        self._server.close()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("No vehicles names passed in arguments. \n")
        sys.exit()
    else:
        print("*** Running Simulation\n")
        simulation_runner = SimulationRunner(sys.argv[1:])
        simulation_runner.receive_data_on_server()
