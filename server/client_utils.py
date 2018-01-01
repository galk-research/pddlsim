# echo_client.py

import socket, sys, os
import struct
from socket_utils import *

INITILIZE_EXECUTIVE, NEXT_ACTION, DONE = 0,1,2

class FakeSim():
    def __init__(self, domain_path, problem_path):
        self.domain_path = domain_path
        self.problem_path = problem_path

    @property
    def domain_path(self):
        return self.domain_path

    @property
    def problem_path(self):
        return self.problem_path

class RemoteSimulator():
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.sent_domain_and_problem = False
        self.original_socket = None
        self.sock = None

    def __enter__(self):
        self.original_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.original_socket.connect((self.host, self.port))
        self.sock = BufferedSocket(self.original_socket)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.original_socket.close()

    def use_domain_and_problem(self, domain_path, problem_path):
        self.domain_path = domain_path
        self.problem_path = problem_path
        self.sock.send_file(domain_path)
        self.sock.send_file(problem_path)
        self.sent_domain_and_problem = True
        return self

    def simulate(self, executive):
        if self.sent_domain_and_problem:
            message = self.sock.recv_int()
            if message != INITILIZE_EXECUTIVE: return

            fake_sim = FakeSim(self.domain_path, self.problem_path)
            executive.initilize(fake_sim)

            self.sock.send_int(INITILIZE_EXECUTIVE)

            while True:
                message = self.sock.recv_int()
                if message == DONE: return
                next_action = executive.next_action()
                if next_action is None:
                    next_action = '(reach-goal)'
                self.sock.send_one_message(next_action)
