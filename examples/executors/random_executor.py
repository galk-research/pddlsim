import random
from pddlsim.executor import Executor


class RandomExecutor(Executor):
    """
    RandomExecutor - pick a random valid action each step
    the trick is finding out the valid actions
    Using the tracked successor is significantly faster
    """

    def initialize(self, services):
        self.services = services

    def pick_action_from_many(self, options):
        chosen_action = random.choice(options)

        return chosen_action

    def next_action(self):
        options = self.services.valid_actions.get()

        if len(options) == 0:
            return None
        elif len(options) == 1:
            return options[0]

        return self.pick_action_from_many(options)
