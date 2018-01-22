# echo_server.py

import SocketServer
from pddlsim.planner import make_plan
import struct
from server.socket_utils import *
import uuid
import shutil
import pickle
from pddlsim.simulator import Simulator

NEXT_ACTION, DONE = 0,1
INITILIZE_EXECUTIVE = 'init'
PERCEPTION_REQUEST = 'request_perception'

class RemoteExecutive():
    def __init__(self, socket, simulator):
        self.socket = socket
        self.simulator = simulator

    def initilize(self,services):
        self.socket.send_one_message(INITILIZE_EXECUTIVE)
        return self.wait_for_one_message_and_serve_perception()
    
    def next_action(self):
        self.socket.send_int(NEXT_ACTION)
        return self.wait_for_one_message_and_serve_perception()

    def wait_for_one_message_and_serve_perception(self):
        while True:            
            message = self.socket.recv_one_message()            
            if message == PERCEPTION_REQUEST:
                self.socket.send_one_message(pickle.dumps(self.simulator.perceive_state()))
            else:
                return message

class SimulatorHandler(SocketServer.BaseRequestHandler):
    def simulate(self,sim, problem_path, executor):
        init = lambda : executor.initilize(None)

        return sim.simulate_with_funcs(problem_path, init, executor.next_action)

    def handle(self):
        try:
            sock = BufferedSocket(self.request)
            sock.get_file(self.domain_path)
            sock.get_file(self.problem_path)

            sim = Simulator(self.domain_path)
            remote = RemoteExecutive(sock,sim)
            # sim.simulate_with_funcs(self.problem_path, lambda : remote.initilize(None), remote.next_action)
            self.simulate(sim,self.problem_path,remote)

            sock.send_int(DONE)
            sock.send_one_message(pickle.dumps(sim.report_card))
            print('Reached goal!' if sim.report_card.success else 'Failed to reach goal')
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
