from collections import deque
from dataclasses import dataclass
from typing import ClassVar

import unified_planning.shortcuts as ups  # type: ignore
from unified_planning.io import PDDLReader  # type: ignore

from pddlsim.ast import (
    ActionFallibilitiesSection,
    GoalsSection,
    GroundedAction,
    Identifier,
    InitializationSection,
    Object,
    Problem,
    RawProblem,
    Requirement,
    RequirementsSection,
    RevealablesSection,
)
from pddlsim.remote.client import (
    NextActionGetter,
    SimulationAction,
    SimulationClient,
)


@dataclass
class Agent:
    client: SimulationClient
    plan_steps: deque[GroundedAction]

    UNSUPPORTED_DOMAIN_REQUIREMENTS: ClassVar = {
        Requirement.PROBABILISTIC_EFFECTS
    }
    UNSUPPORTED_PROBLEM_REQUIREMENTS: ClassVar = {
        Requirement.FALLIBLE_ACTIONS,
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

        return Agent(client, deque()).get_next_action

    async def set_plan_for_goal(self, goal_index: int) -> None:
        domain = await self.client.get_domain()
        problem = await self.client.get_problem()

        current_state = await self.client.get_perceived_state()

        goal_condition = problem.goals_section[goal_index]

        new_problem = Problem(
            RawProblem(
                problem.name,
                problem.used_domain_name,
                RequirementsSection(
                    {
                        requirement
                        for requirement in problem.requirements_section
                        if requirement is not Requirement.MULTIPLE_GOALS
                    }
                ),
                problem.objects_section,
                ActionFallibilitiesSection(),
                RevealablesSection(),
                InitializationSection(set(current_state)),
                GoalsSection([goal_condition]),
            ),
            domain,
        )

        up_problem: ups.Problem = PDDLReader().parse_problem_string(
            repr(domain), repr(new_problem)
        )

        ups.get_environment().credits_stream = None  # Disable credits

        with ups.OneshotPlanner(problem_kind=up_problem.kind) as planner:
            self.plan_steps = deque(
                GroundedAction(
                    Identifier(action_instance.action.name),
                    list(
                        Object(parameter.object().name)
                        for parameter in action_instance.actual_parameters
                    ),
                )
                for action_instance in planner.solve(up_problem).plan.actions
            )

    async def get_next_action(self) -> SimulationAction:
        if not self.plan_steps:
            uncompleted_goal_indices = (
                await self.client.get_unreached_goal_indices()
            )
            chosen_index = uncompleted_goal_indices[0]

            await self.set_plan_for_goal(chosen_index)

        return self.plan_steps.popleft()
