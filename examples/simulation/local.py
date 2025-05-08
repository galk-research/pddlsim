import asyncio
import logging
import random
from collections.abc import Sequence

from pddlsim.local import simulate_domain_problem_pair_from_files
from pddlsim.remote.client import (
    GiveUpAction,
    SimulationAction,
    SimulationClient,
    with_no_initializer,
)
from pddlsim.simulation import GroundedAction


def pick_grounded_action(
    actions: Sequence[GroundedAction],
) -> GroundedAction:
    return random.choice(actions)


async def get_next_action(simulation: SimulationClient) -> SimulationAction:
    options = await simulation.get_grounded_actions()

    match len(options):
        case 0:
            return GiveUpAction.from_dead_end()
        case 1:
            return options[0]
        case _:
            return pick_grounded_action(options)


async def main() -> None:
    termination = await simulate_domain_problem_pair_from_files(
        "assets/problems/gripper/domain.pddl",
        "assets/problems/gripper/instance.pddl",
        with_no_initializer(get_next_action),
    )

    print(termination)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    asyncio.run(main())
