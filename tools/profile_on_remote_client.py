# echo_client.py
from pddlsim.executors import (plan_dispatch, random_executor,
                               executor_profiler)

HOST, PORT = "localhost", 9999


def profile(executives, log_file='reusage_log', domain_path=None, problem_path=None):
    '''
    Profile against a remote server
    The idea is to isolate what the executive is using and not include the simulation resources
    '''
    results = dict()
    for executive in executives:
        results[executive.__class__.__name__] = False
        profiled_executive = executor_profiler.ExecutorProfiler(executive)
        with RemoteSimulator(HOST, PORT) as sim:
            sim.use_domain_and_problem(domain_path, problem_path)
            results[executive.__class__.__name__] = sim.simulate(
                profiled_executive)
            profiled_executive.save_rusage_log(log_file)
    return results

if __name__ == '__main__':
    domain = 'domains/generated/domain.pddl'
    problem = 'domains/generated/problems/t_5_5_5.pddl'

    executives = [
        plan_dispatch.PlanDispatcher(), random_executor.RandomExecutor()]
    results = profile(executives, 'reusage_log', domain, problem)
    for ex, rc in results.iteritems():
        print ex
        print str(rc)
        print
