import asyncio
import logging
import random
from dataclasses import dataclass

from pddlsim.ast import Domain, GroundedAction, Problem
from pddlsim.remote.client import (
    GiveUpAction,
    NextActionGetter,
    SimulationAction,
    SimulationClient,
    act_in_simulation,
)
from pddlsim.simulation import Simulation
from pddlsim.state import SimulationState


@dataclass
class Agent:
    configuration: "AgentConfiguration"
    client: SimulationClient
    domain: Domain
    problem: Problem
    previous_state: SimulationState | None
    steps: int = 0

    async def _is_action_backtracking(
        self, grounded_action: GroundedAction
    ) -> bool:
        simulation = Simulation.from_domain_and_problem(
            self.domain, self.problem, await self.client.get_perceived_state()
        )
        simulation.apply_grounded_action(grounded_action)

        return simulation.state == self.previous_state

    async def get_next_action(self) -> SimulationAction:
        if self.steps >= self.configuration.max_steps:
            return GiveUpAction("max steps reached")

        grounded_actions = await self.client.get_grounded_actions()
        non_backtracking_actions = [
            grounded_action
            for grounded_action in grounded_actions
            if not await self._is_action_backtracking(grounded_action)
        ]

        possibilities = (
            non_backtracking_actions
            if non_backtracking_actions
            else grounded_actions
        )

        picked_action = random.choice(possibilities)

        self.steps += 1
        self.previous_state = await self.client.get_perceived_state()

        return picked_action


@dataclass(frozen=True)
class AgentConfiguration:
    max_steps: int

    async def initialize(self, client: SimulationClient) -> NextActionGetter:
        domain = await client.get_domain()
        problem = await client.get_problem()

        return Agent(self, client, domain, problem, None).get_next_action


async def main() -> None:
    port = int(input("What port to connect to? (0-65535): "))
    summary = await act_in_simulation(
        "127.0.0.1",
        port,
        AgentConfiguration(300).initialize,
    )

    print(f"Finished with: {summary}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    asyncio.run(main())
