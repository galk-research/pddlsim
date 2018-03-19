# echo_server.py

import SocketServer
from pddlsim.services.planner import make_plan
import struct
from server.socket_utils import *
import uuid
import shutil

SENDING_DOMAIN, SENDING_PROBLEM, REQUEST_PLAN, SENDING_PLAN = 0, 1, 2, 3


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
            sock.get_file(self.domain_path)
            sock.get_file(self.problem_path)
            make_plan(self.domain_path, self.problem_path, self.plan_path)
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
        self.directory = os.path.join('.tmp', uuid.uuid4().hex)
        os.makedirs(self.directory)
        self.domain_path = os.path.join(self.directory, 'domain.pddl')
        self.problem_path = os.path.join(self.directory, 'problem.pddl')
        self.plan_path = os.path.join(self.directory, 'plan.ipc')
        return SocketServer.BaseRequestHandler.setup(self)

    def finish(self):
        # auto clean temporary directory for process
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
