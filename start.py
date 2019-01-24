#!/usr/bin/python3
from os.path import join
from subprocess import Popen
from time import sleep


TEMPLATE_NAME = 'haproxy.cfg.template'
CONFIG_NAME = 'haproxy.cfg'
CONFIG_FOLDER = '/usr/local/etc/'
TEMPLATE_PATH = join(CONFIG_FOLDER, TEMPLATE_NAME)
CONFIG_PATH = join(CONFIG_FOLDER, CONFIG_NAME)
TOR_CONTROL_PORT = 5566
HAPROXY_PID_FILE = '/var/run/haproxy/{}.pid'.format(TOR_CONTROL_PORT)
DATA_DIR = '/var/lib/tor'
ACCEPTABLE_PORT_RANGE = range(40000, 50000)
CONTROL_PORT_RANGE = range(30000, 39999)
TOR_PATH = 'tor'
HAPROXY_PATH = 'haproxy'
PID_FILE_TEMPLATE = '/var/run/{}/{}.pid'
TOR_PROXY_COUNT = 25


def start_tor_server(control_port, port):
    data_dir = join(DATA_DIR, str(port))
    pid_file = PID_FILE_TEMPLATE.format('tor', port)

    args = [
        TOR_PATH,
        "--SocksPort", "{}".format(port),
        "--ControlPort", "{}".format(control_port),
        "--ExitRelay", "0",
        "--RefuseUnknownExits", "0",
        "--ClientOnly", "1",
        "--DataDirectory", "{}".format(data_dir),
        "--PidFile", "{}".format(pid_file),
    ]
    Popen(args)


def compile_config(control_port, pid_file, ports):
    data = open(TEMPLATE_PATH).read()
    backend_template = "  server tor{port} 127.0.0.1:{port}"
    backends = '\n'.join([backend_template.format(port=p) for p in ports])

    with open(CONFIG_PATH, 'w') as f:
        f.write(data.format(control_port=control_port, backends=backends,
                            pid_file=pid_file))

    return CONFIG_PATH


def start_haproxy(control_port, tor_ports, config_template_path, config_path):
    pid_file = PID_FILE_TEMPLATE.format('haproxy', control_port)
    config_path = compile_config(control_port, pid_file, tor_ports)

    args = [
        HAPROXY_PATH,
        '-f',
        '{}'.format(config_path)
    ]

    Popen(args)


def start():
    ports = [ACCEPTABLE_PORT_RANGE[i] for i in range(TOR_PROXY_COUNT)]
    control_ports = [CONTROL_PORT_RANGE[i] for i in range(TOR_PROXY_COUNT)]

    for port, control_port in zip(ports, control_ports):
        start_tor_server(control_port, port)

    start_haproxy(TOR_CONTROL_PORT, ports, TEMPLATE_PATH, CONFIG_PATH)


if __name__ == '__main__':
    start()

    while 1:
        sleep(1)
