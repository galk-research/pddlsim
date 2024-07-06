from pddlsim.executors.executor import Executor
from pddlsim.utils import planner


class PlanDispatcher(Executor):
    """docstring for PlanDispatcher."""

    def __init__(self, use_local=True):
        super(PlanDispatcher, self).__init__()
        self.steps = []
        self.planner = planner.local if use_local else planner.online

    def initialize(self, services):
        self.steps = self.planner(services.pddl.domain_path, services.pddl.problem_path)

    def next_action(self):
        if len(self.steps) > 0:
            return self.steps.pop(0).lower()
        return None
