class ProblemGenerator():
    def __init__(self, simulator, goal_tracking, path):
        self.simulator = simulator
        self.path = path
        self.goal_tracking = goal_tracking

    def generate_problem(self, state, goal = None):
        if goal is None:
            goal = self.goal_tracking.uncompleted_goals()[0]
        self.simulator.parser.generate_problem(self.path, self.simulator.state, goal)
        return self.path
