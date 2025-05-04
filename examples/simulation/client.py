import asyncio
import logging
import random
from dataclasses import dataclass

from pddlsim.remote.client import (
    GiveUpAction,
    NextActionGetter,
    SimulationAction,
    SimulationClient,
    act_in_simulation,
)

logging.basicConfig(level=logging.DEBUG)


@dataclass
class Agent:
    configuration: "AgentConfiguration"
    client: SimulationClient
    steps: int = 0

    async def get_next_action(self) -> SimulationAction:
        if self.steps >= self.configuration.max_steps:
            return GiveUpAction("max steps reached")

        self.steps += 1

        _state = await self.client.get_state()

        grounded_actions = await self.client.get_grounded_actions()

        return random.choice(grounded_actions)


@dataclass
class AgentConfiguration:
    max_steps: int

    async def initialize(self, client: SimulationClient) -> NextActionGetter:
        _domain = await client.get_domain()
        _problem = await client.get_problem()

        return Agent(self, client).get_next_action


async def main() -> None:
    port = int(input("What port to connect to? (0-65535): "))
    termination = await act_in_simulation(
        "127.0.0.1",
        port,
        AgentConfiguration(300).initialize,
    )

    print(f"Finished with: {termination}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    asyncio.run(main())
