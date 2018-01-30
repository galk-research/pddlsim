class ActionSimulator():
    def __init__(self, parser, perception):
        self.parser = parser
        self.perception = perception

    def next_state(self, action):
        next_state = self.perception.get_state()
        self.parser.apply_action_to_state(action, next_state, False)
        return next_state