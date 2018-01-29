import struct
import uuid
import shutil
import pickle
import SocketServer
import errno

from pddlsim.simulator import Simulator
from remote_executive import RemoteExecutive
from socket_utils import *
from messages import *

class SimulatorHandler(SocketServer.BaseRequestHandler):
    TMP_DIR = '.tmp'
    DEFAULT_TIMEOUT = 60
    
    def simulate(self,sim, problem_path, executor):
        init = lambda : executor.initilize(None)
        return sim.simulate_with_funcs(problem_path, init, executor.next_action)

    def handle(self):
        self.request.settimeout(self.DEFAULT_TIMEOUT)
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
            elif e.errno == errno.ETIMEDOUT:
                print('timedout')
            else:
                # Other error, re-raise
                raise

    def setup(self):
        self.directory = os.path.join(self.TMP_DIR,uuid.uuid4().hex)
        os.makedirs(self.directory)
        self.domain_path = os.path.join(self.directory,'domain.pddl')
        self.problem_path = os.path.join(self.directory,'problem.pddl')
        return SocketServer.BaseRequestHandler.setup(self)

    def finish(self):
        #auto clean temporary directory after serving request
        shutil.rmtree(self.directory)
        
        # remove root directory if empty
        files = os.listdir(self.TMP_DIR)
        if len(files) == 0:
            os.rmdir(self.TMP_DIR)
        return SocketServer.BaseRequestHandler.finish(self)

def start(host="localhost", port=9999, requests_to_serve=-1):
    """
    Start a remote simulator server with host and port
    requests_to_serve will serve the specified amount
    default is -1 which will server forever
    """
    SocketServer.TCPServer.allow_reuse_address = True

    server = SocketServer.TCPServer((host, port), SimulatorHandler)
    

    print("Server starting...")
    if requests_to_serve == -1:    
        # this will keep running until Ctrl-C    
        server.serve_forever()
    else:
        for _ in xrange(requests_to_serve):
            server.handle_request()

if __name__ == "__main__":
    start()
