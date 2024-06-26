from pddlsim.utils.valid_actions import get_valid_candidates_for_action


class ValidActions:
    """
    Python implemention for valid actions
    """

    def __init__(self, parser, perception):
        self.parser = parser
        self.perception = perception

    def get(self):
        current_state = self.perception.get_state()
        possible_actions = []
        for name, action in self.parser.actions.items():
            for candidate in get_valid_candidates_for_action(current_state, action):
                possible_actions.append(action.action_string(candidate))
        return possible_actions

    def on_action(self, action_sig):
        pass
