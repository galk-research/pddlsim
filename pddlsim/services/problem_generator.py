class ProblemGenerator():
    def __init__(self, perception, parser, path):
        self.perception = perception
        self.parser = parser
        self.path = path        
    
    def generate_problem(self, goal, state = None):
        if state is None:
            state = self.perception.get_state()        
        self.parser.generate_problem(self.path, state, goal)
        return self.path
