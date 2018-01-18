class Perception():
    def __init__(self, simulator):
        self.simulator = simulator
    
    def get_state(self):
        return self.simulator.perceive_state()