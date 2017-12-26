# echo_server.py

import SocketServer
from pddlsim.planner import make_plan
import struct
from shared.socket_utils import *
import uuid
import shutil

class PlanningHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """    
    def handle(self):
        try:            
            sock = BufferedSocket(self.request)
            while True:
                print("Waiting for command...")
                command = sock.recv_int()
                if command is  None: return
                print("Recived command: " + str(command))
                if command == SENDING_DOMAIN:
                    sock.get_file(self.domain_path)                
                if command == SENDING_PROBLEM:
                    sock.get_file(self.problem_path)
                if command == REQUEST_PLAN:
                    make_plan(self.domain_path,self.problem_path,self.plan_path)
                    sock.send_file(self.plan_path)
                # send_int(self.request,ACK)            
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
        self.plan_path = os.path.join(self.directory,'plan.ipc')        
        return SocketServer.BaseRequestHandler.setup(self)    

    def finish(self):
        #auto clean temporary directory for process
        shutil.rmtree(self.directory)
        return SocketServer.BaseRequestHandler.finish(self)

if __name__ == "__main__":
    
    HOST, PORT = "localhost", 9999

    # instantiate the server, and bind to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), PlanningHandler)
    
    print("Server starting...")
    # activate the server
    # this will keep running until Ctrl-C
    server.serve_forever()