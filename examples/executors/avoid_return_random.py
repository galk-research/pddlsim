from pddlsim.executor import Executor
import random


class AvoidReturn(Executor):

    def __init__(self):
        pass

    def initialize(self, services):
        self.services = services
        self.previous_state = None
        self.last_different_state = None

    def next_action(self):
        """
        save previous state after choosing next action
        """

        current_state = self.services.perception.get_state()

        if current_state != self.previous_state:
            self.last_different_state = self.previous_state

        self.previous_state = current_state

        options = self.services.valid_actions.get()

        if len(options) == 0:
            return None
        elif len(options) == 1:
            return options[0]

        return self.pick_from_many(options)

    def is_next_state_same_as_previous(self, option):
        next_state = self.services.perception.get_state()

        self.services.parser.apply_action_to_state(option, next_state, False)

        return next_state != (
            self.last_different_state
            if self.previous_state == self.services.perception.get_state()
            else self.previous_state
        )

    def remove_return_actions(self, options):
        if self.previous_state:
            return filter(self.is_next_state_same_as_previous, options)

        return options

    def pick_from_many(self, options):
        options = list(self.remove_return_actions(options))
        return random.choice(options)
