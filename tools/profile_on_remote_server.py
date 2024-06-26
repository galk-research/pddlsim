from pddlsim.remote import SimulatorForkedTCPServer
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='run a simulator server, no arguments will run without a domain and proble')
    parser.add_argument('--domain', help='')
    parser.add_argument('--problem',
                        default='',
                        help='')

    parser.add_argument('-u', '--use_defaults', action='store_true',
                        default=False,
                        help='')

    args = parser.parse_args()
    print args
    domain, problem = args.domain, args.problem
    server = SimulatorForkedTCPServer.default()
    if domain is not None and problem is not None and args.use_defaults:
        domain = 'domains/generated/domain.pddl'
        problem = 'domains/generated/problems/t_5_5_5.pddl'
    if domain is not None and problem is not None:
        server.provide_pddls(domain, problem)
    server.serve_forever()
