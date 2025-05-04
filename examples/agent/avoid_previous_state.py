import random
from dataclasses import dataclass

from pddlsim.ast import Domain, Problem
from pddlsim.remote.client import (
    SimulationAction,
    SimulationClient,
)
from pddlsim.simulation import GroundedAction, Simulation
from pddlsim.state import SimulationState


@dataclass
class Agent:
    client: SimulationClient
    domain: Domain
    problem: Problem
    previous_state: SimulationState | None

    async def _is_action_backtracking(
        self, grounded_action: GroundedAction
    ) -> bool:
        simulation = Simulation.from_domain_and_problem(
            self.domain, self.problem, await self.client.get_state()
        )
        simulation.apply_grounded_action(grounded_action)

        return simulation.state == self.previous_state

    async def get_next_action(self) -> SimulationAction:
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

        self.previous_state = await self.client.get_state()

        return picked_action
