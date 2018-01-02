class GoalTracking():
    def __init__(self, has_multiple_goals, reached_all_goals_func):
        self.has_multiple_goals = has_multiple_goals
        self.reached_all_goals = reached_all_goals_func
