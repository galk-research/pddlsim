import random

from pddlsim.rsp.client import DeadEndAction, SimulationClient, SimulationAction
from pddlsim.rsp.message import GroundedAction


def pick_grounded_action(actions: list[GroundedAction]) -> GroundedAction:
    return random.choice(actions)


async def get_next_action(simulation: SimulationClient) -> SimulationAction:
    options = await simulation.get_grounded_actions()

    match len(options):
        case 0:
            return DeadEndAction()
        case 1:
            return options[0]
        case _:
            return pick_grounded_action(options)
