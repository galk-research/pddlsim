class Memorizer():
    def __init__(self, perception):
        self.previous_state = None
        self.perception = perception

    def save_state(self):
        self.previous_state = self.perception.get_state()

    def load_state(self):
        return self.previous_state

    def has_state(self):
        return self.previous_state is not None
