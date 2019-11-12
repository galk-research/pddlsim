# echo_client.py

import socket, sys, os
import struct
from planning_server import SENDING_DOMAIN, SENDING_PROBLEM, REQUEST_PLAN, SENDING_PLAN
from server.socket_utils import *

HOST, PORT = "localhost", 9999

# create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # connect to server
    sock.connect((HOST, PORT))
    mysock = BufferedSocket(sock)

    mysock.send_file( './experiments/domain.pddl')
    mysock.send_file( './experiments/problems/corridor_100.pddl')
    mysock.get_file('plan.ipc')

finally:
    # shut down
    sock.close()
