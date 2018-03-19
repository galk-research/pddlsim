from pddlsim.executors.executor import Executor
from experiments import reduce_domain


class MazeReducerExecutor(Executor):

    def __init__(self):
        super(MazeReducerExecutor, self).__init__()
        self.steps = []

    def initialize(self, services):
        temp_path = 'temp_reduced.pddl'

        self.services = services

        self.graph, self.original_graph = reduce_domain.reduce_problem(
            services.pddl.domain_path, services.pddl.problem_path, temp_path)
        self.big_steps = services.planner.make_plan(
            services.pddl.domain_path)

        # self.expanded_steps = [ for step in big_steps]

    def next_action(self):
        if len(self.steps) == 0:
            if len(self.big_steps) > 0:
                self.steps = self.expand_step(self.big_steps.pop(0))
            else:
                return None
        return self.steps.pop(0).lower()

    def expand_step(self, big_step):
        direction, person, source, destination = big_step.strip(
            '()').lower().split()
        direction = direction[5:]
        loc = source
        steps = []
        while loc != destination:
            next_tile = self.original_graph[loc][direction][0]
            next_direction = self.other_direction(next_tile, direction)
            step = "(move-{} {} {} {})".format(
                direction, person, loc, next_tile)
            steps.append(step)
            loc = next_tile
            direction = next_direction
        return steps

    def other_direction(self, tile, incoming_direction):
        for dir in self.original_graph[tile]:
            if dir != reduce_domain.directions[incoming_direction]:
                return dir
