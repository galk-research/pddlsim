SUPPORTS_LAPKT = False
try:
    from pddlsim.external.liblapkt import Planner
    SUPPORTS_LAPKT = True
except:
    pass

from pddlsim.utils.valid_actions import get_valid_candidates_for_action

class ValidActions():

    """
    ValidActions creates the provider for the actual valid action.
    It has a fallback if LAPKT isn't available to the python implementation, note that that implementation neither efficient nor stable
    """

    def __init__(self, parser, pddl, perception, force_python_version=False):
        problem = pddl.problem_path

        self.provider = None
        if SUPPORTS_LAPKT and not force_python_version:
            self.provider = TrackedSuccessorValidActions(
                pddl.domain_path, problem)
        else:
            self.provider = PythonValidActions(parser, perception)

    def get(self):
        return self.provider.get()

    def on_action(self, action_sig):
        self.provider.on_action(action_sig)


class TrackedSuccessorValidActions():

    """
    Use the TrackedSuccessor to query for valid actions at the current state
    This successor is tracked because LAPKT needs to keep track of the state
    """

    def __init__(self, domain_path, problem_path):
        self.task = Planner()
        self.task.load(domain_path, problem_path)
        self.task.setup()
        self.sig_to_index = dict()
        for i in range(0, self.task.num_actions()):
            self.sig_to_index[self.task.get_action_signature(i)] = i

    def get(self):
        return map(str.lower, self.task.next_actions_from_current())

    def on_action(self, action_signature):
        """
        This is called by the SimulatorServices to notify that an action has been selected
        It is necessary because TrackedSuccessors keeps track of it's own state
        """
        self.task.proceed_with_action(
            self.sig_to_index[action_signature.upper()])


class PythonValidActions():

    """
    Python implemention for valid actions
    This is significantly less efficient than the TrackedSuccessor version
    """

    def __init__(self, parser, perception):
        self.parser = parser
        self.perception = perception

    def get(self):
        current_state = self.perception.get_state()
        possible_actions = []
        for (name, action) in self.parser.actions.items():
            for candidate in get_valid_candidates_for_action(current_state, action):
                possible_actions.append(action.action_string(candidate))
        return possible_actions

    def on_action(self, action_sig):
        pass
