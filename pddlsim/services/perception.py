class Perception():
    def __init__(self, perception_func):
        self.perception_func = perception_func
        self.state = None
        self.dirty = True

    def get_state(self):
        if self.dirty:
            self.state = self.perception_func()
            self.dirty = False
        return {name: set(entries) for name, entries in self.state.items()}

    def on_action(self, action):
        self.dirty = True
