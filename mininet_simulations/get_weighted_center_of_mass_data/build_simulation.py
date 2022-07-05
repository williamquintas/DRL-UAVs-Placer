import socket, sys, threading
sys.path.append('..')

from utils.constants import SIMULATION_SOCKET_PORT
from utils.log import log, write_to_file
from controllers.simulation import SimulationController, SimulationRendererController

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
        log("Simulation socket listening on {}:{}\n".format(host, port))
        return server

    def _process_set_position(self, hostname: str, **kwargs):
        hosts = self._simulation.get_hosts()
        host = list(filter(lambda h: h.get_id() == hostname, hosts))

        row = kwargs['timestamp']
        for h in hosts:
            row += ",{},{},{}".format(h.get_position()['x'], h.get_position()['y'], h.get_avg_data_communicated_per_second())
        write_to_file("{}\n".format(row))

        if(host):
            host[0].set_position(kwargs)
        else:
            log("No host found with id {}.".format(hostname))

    def _process_set_rx_tx(self, hostname: str, data_list: list):
        hosts = self._simulation.get_hosts()
        host = list(filter(lambda h: h.get_id() == hostname, hosts))
        if(host):
            host[0].set_data_communicated_list(data_list)
        else:
            log("No host found with id {}.".format(hostname))

    def _process_command(self, command: str, hostname: str, *args) -> None:
        if command == SET_POSITION:
            x, y = float(args[0][0]),float(args[0][1])
            timestamp = args[0][2]
            self._process_set_position(hostname, x=x, y=y, timestamp=timestamp)
        elif command == SET_RX_TX:
            data_list = args[0]
            self._process_set_rx_tx(hostname, data_list)
        else:
            log("Command {} is not known. \n Accepted commands: {}".format(
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
            threading.Thread(target=self.on_new_connection, args=(connection,)).start()

        self._server.close()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        log("No vehicles names passed in arguments. \n")
        sys.exit()
    else:
        log("*** Running Simulation\n")
        simulation_runner = SimulationRunner(sys.argv[1:])
        simulation_runner.receive_data_on_server()
