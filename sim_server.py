# echo_server.py

import SocketServer
from pddlsim.planner import make_plan
import struct
from server.socket_utils import *
import uuid
import shutil
import pickle
from pddlsim.simulator import Simulator

INITILIZE_EXECUTIVE, NEXT_ACTION, DONE = 0,1,2

class RemoteExecutive():
    def __init__(self, socket):
        self.socket = socket

    def initilize(self, simulator):
        self.socket.send_int(INITILIZE_EXECUTIVE)
        self.socket.recv_int()

    def next_action(self):
        self.socket.send_int(NEXT_ACTION)
        return self.socket.recv_one_message()

class SimulatorHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            sock = BufferedSocket(self.request)
            sock.get_file(self.domain_path)
            sock.get_file(self.problem_path)

            sim = Simulator(self.domain_path)
            remote = RemoteExecutive(sock)
            sim.simulate(self.problem_path, remote)

            sock.send_int(DONE)
            sock.send_one_message(pickle.dumps(sim.report_card))
            print('Reached goal!' if sim.reached_all_goals else 'Failed to reach goal')
        except socket.error, e:
            if e.errno == errno.ECONNRESET:
                # Handle disconnection -- close & reopen socket etc.
                print('disconnected')
            else:
                # Other error, re-raise
                raise

    def setup(self):
        self.directory = os.path.join('.tmp',uuid.uuid4().hex)
        os.makedirs(self.directory)
        self.domain_path = os.path.join(self.directory,'domain.pddl')
        self.problem_path = os.path.join(self.directory,'problem.pddl')
        return SocketServer.BaseRequestHandler.setup(self)

    def finish(self):
        #auto clean temporary directory for process
        shutil.rmtree(self.directory)
        return SocketServer.BaseRequestHandler.finish(self)

if __name__ == "__main__":

    HOST, PORT = "localhost", 9999

    # instantiate the server, and bind to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), SimulatorHandler)

    print("Server starting...")
    # activate the server
    # this will keep running until Ctrl-C
    server.serve_forever()
