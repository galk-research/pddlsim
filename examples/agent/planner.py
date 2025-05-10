from collections import deque
from dataclasses import dataclass
from typing import ClassVar

import unified_planning.shortcuts as ups  # type: ignore
from unified_planning.io import PDDLReader  # type: ignore

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

    UNSUPPORTED_DOMAIN_REQUIREMENTS: ClassVar = {
        Requirement.PROBABILISTIC_EFFECTS
    }
    UNSUPPORTED_PROBLEM_REQUIREMENTS: ClassVar = {
        Requirement.FALLIBLE_ACTIONS,
        Requirement.MULTIPLE_GOALS,
        Requirement.REVEALABLES,
    }

    @classmethod
    async def from_client(cls, client: SimulationClient) -> NextActionGetter:
        domain = await client.get_domain()
        problem = await client.get_problem()

        for requirement in cls.UNSUPPORTED_DOMAIN_REQUIREMENTS:
            if requirement in domain.requirements_section:
                raise ValueError(
                    f"`{requirement}` requirement is not supported"
                )

        for requirement in cls.UNSUPPORTED_PROBLEM_REQUIREMENTS:
            if requirement in problem.requirements_section:
                raise ValueError(
                    f"`{requirement}` requirement are not supported"
                )

        up_problem: ups.Problem = PDDLReader().parse_problem_string(
            repr(domain), repr(problem)
        )

        ups.get_environment().credits_stream = None  # Disable credits

        with ups.OneshotPlanner(problem_kind=up_problem.kind) as planner:
            plan_steps = deque(
                GroundedAction(
                    Identifier(action_instance.action.name),
                    list(
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
