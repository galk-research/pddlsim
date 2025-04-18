import asyncio
import logging
import random
from collections.abc import Awaitable, Callable

import pddlsim.rsp.client
from pddlsim.rsp.client import SimulationAction

logging.basicConfig(level=logging.DEBUG)


def create_get_next_action(
    max_steps: int | None = None,
) -> Callable[
    [pddlsim.rsp.client.SimulationClient], Awaitable[SimulationAction]
]:
    steps = 0

    async def get_next_action(
        simulation: pddlsim.rsp.client.SimulationClient,
    ) -> SimulationAction:
        nonlocal steps

        if max_steps and steps >= max_steps:
            return pddlsim.rsp.client.GiveUpAction("max steps reached")

        steps += 1

        grounded_actions = await simulation.get_grounded_actions()

        return random.choice(grounded_actions)

    return get_next_action


async def main() -> None:
    port = int(input("What port to connect to? (0-65535): "))
    termination = await pddlsim.rsp.client.act_in_simulation(
        "127.0.0.1", port, create_get_next_action()
    )

    print(f"Finished with: {termination}")


asyncio.run(main())
