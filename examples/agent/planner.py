# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pddlsim @ file://${PROJECT_ROOT}/",
#     "unified-planning[fast-downward]>=1.2.0",
# ]
# ///
from collections import deque
from dataclasses import dataclass

import unified_planning.shortcuts as ups
from unified_planning.io import PDDLReader

from pddlsim.ast import Identifier, Object, Requirement
from pddlsim.remote.client import (
    GiveUpAction,
    NextActionGetter,
    SimulationAction,
    SimulationClient,
)
from pddlsim.simulation import GroundedAction


@dataclass
class Agent:
    client: SimulationClient
    plan_steps: deque[GroundedAction]

    @classmethod
    async def from_client(cls, client: SimulationClient) -> NextActionGetter:
        domain = await client.get_domain()

        if Requirement.PROBABILISTIC_EFFECTS in domain.requirements:
            raise ValueError("probabilistic effects are not supported")

        problem = await client.get_problem()

        up_problem: ups.Problem = PDDLReader().parse_problem_string(
            repr(domain), repr(problem)
        )

        ups.get_environment().credits_stream = None  # Disable credits

        with ups.OneshotPlanner(problem_kind=up_problem.kind) as planner:
            plan_steps = deque(
                GroundedAction(
                    Identifier(action_instance.action.name),
                    tuple(
                        Object(parameter.object().name)
                        for parameter in action_instance.actual_parameters
                    ),
                )
                for action_instance in planner.solve(up_problem).plan.actions
            )

        return Agent(client, plan_steps).get_next_action

    async def get_next_action(self) -> SimulationAction:
        if not self.plan_steps:
            return GiveUpAction("plan has ended, but problem unsolved")

        return self.plan_steps.popleft()
