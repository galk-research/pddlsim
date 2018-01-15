class ActionSimulator():
    def __init__(self, simulator):
        self.simulator = simulator

    def next_state(self, action):
        next_state = self.simulator.clone_state()
        self.simulator.act(action, next_state)
        return next_state