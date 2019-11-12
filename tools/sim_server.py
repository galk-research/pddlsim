from pddlsim.remote import simulator_server
from pddlsim.remote.simulator_server import SimulatorForkedTCPServer

if __name__ == "__main__":    
    # simulator_server.start("localhost",9999)
    SimulatorForkedTCPServer.default() \
    .provide_pddls('experiments/domain.pddl','experiments/problems/t_5_5_5.pddl')\
    .serve_forever()
