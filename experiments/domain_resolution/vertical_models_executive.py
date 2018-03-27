import random

from pddlsim.fd_parser import FDParser
from pddlsim.parser_independent import PDDL, Literal, Conjunction
from pddlsim.services import valid_actions, perception
from pddlsim.local_simulator import LocalSimulator


class VerticalModelsExecutive():

    def __init__(self, top_domain_path, top_to_bottom_actions, bottom_to_top_state):
        self.top_domain_path = top_domain_path
        self.top_to_bottom_actions = top_to_bottom_actions
        self.bottom_to_top_state = bottom_to_top_state
        self.commited_actions = None

    def initialize(self, services):
        self.goal_tracking = services.goal_tracking
        self.bottom_pddl = services.pddl
        self.bottom_perception = services.perception
        self.bottom_valid_actions = services.valid_actions
        top_perception = perception.Perception(lambda: self.bottom_to_top_state(
            self.bottom_pddl.copy_state(services.perception.get_state())))
        top_initial_state = top_perception.get_state()
        top_problem = 'tmp_problem.pddl'
        self.bottom_pddl.generate_problem(
            top_problem, top_initial_state, self.bottom_pddl.goals[0])
        self.top_pddl = FDParser(self.top_domain_path, top_problem)
        self.top_valid_actions = valid_actions.PythonValidActions(
            self.top_pddl, top_perception)

    def next_action(self):
        if self.goal_tracking.reached_all_goals():
            return None
        if self.commited_actions:
            return self.commited_actions.pop(0)
        valid_top_actions = self.top_valid_actions.get()
        valid_bottom_actions = self.bottom_valid_actions.get()
        if valid_top_actions:
            next_top_action = random.choice(valid_top_actions)
            self.commited_actions = self.top_to_bottom_actions(
                self.bottom_perception.get_state(), next_top_action)
            if self.commited_actions:
                return self.commited_actions.pop(0)
        return random.choice(valid_bottom_actions)


class ModelConverter():

    def top_to_bottom_actions(self, bottom_state, top_action_str):
        action_name, target_tile = PDDL.parse_action(top_action_str)
        if action_name != 'move-east':
            return [top_action_str]

        for person in bottom_state['person']:
            break

        actions = []
        start_location = self.find_in_state(
            bottom_state, 'at', lambda x: x[0] == person[0])[1]
        while True:
            middle = self.east_of(bottom_state, start_location)
            if not middle:
                break
            middle = middle[1]
            actions.append(
                '(move-east {} {} {})'.format(person[0], start_location, middle))
            start_location = middle
        return actions

    def find_in_state(self, state, predicate_name, condition):
        return next((x for x in state[predicate_name] if condition(x)), None)

    def east_of(self, state, tile_name):
        return self.find_in_state(
            state, 'east', lambda x: x[0] == tile_name)

    def bottom_to_top_state(self, bottom_state):
        top_state = bottom_state
        for person in top_state['person']:
            break

        start_location = self.find_in_state(
            top_state, 'at', lambda x: x[0] == person[0])[1]
        while True:
            middle = self.east_of(top_state, start_location)
            if not middle:
                break
            middle = middle[1]
            after_middle = self.east_of(top_state, middle)

            if not after_middle:
                break
            after_middle = after_middle[1]
            # bottom state: start_location <-> middle <-> after_middle
            # top state: start_location <-> after_middle

            top_state['east'].remove((start_location, middle))
            top_state['east'].remove((middle, after_middle))
            top_state['west'].remove((middle, start_location))
            top_state['west'].remove((after_middle, middle))

            top_state['east'].add((start_location, after_middle))
            top_state['west'].add((after_middle, start_location))
            start_location = after_middle
        return top_state


if __name__ == '__main__':

    bottom_domain_path, bottom_problem_path = '../domain.pddl', 'simple_problem.pddl'
    top_domain_path = bottom_domain_path

    converter = ModelConverter()
    vme = VerticalModelsExecutive(
        top_domain_path, converter.top_to_bottom_actions, converter.bottom_to_top_state)
    LocalSimulator().run(bottom_domain_path, bottom_problem_path, vme)
