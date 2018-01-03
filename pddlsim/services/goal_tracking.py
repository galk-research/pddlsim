class GoalTracking():
    def __init__(self, simulator):
        self.simulator = simulator

    def has_multiple_goals(self):
        return len(self.simulator.uncompleted_goals) > 1

    def reached_all_goals(self):
        return self.simulator.reached_all_goals

    def uncompleted_goals(self):
        return self.simulator.uncompleted_goals
