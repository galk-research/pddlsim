"""Interface for interacting with simulations, and code to connect to them."""

import asyncio
import time
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass, field
from typing import NoReturn, override

from pddlsim.ast import Domain, GroundedAction, Problem
from pddlsim.remote import (
    _RSP_VERSION,
    _RSPMessageBridge,
    _SessionTerminationError,
)
from pddlsim.remote._message import (
    Error,
    GetGroundedActionsRequest,
    GetGroundedActionsResponse,
    GiveUp,
    GoalsReached,
    GoalTrackingRequest,
    GoalTrackingResponse,
    Payload,
    PerceptionRequest,
    PerceptionResponse,
    PerformGroundedActionRequest,
    PerformGroundedActionResponse,
    ProblemSetupRequest,
    ProblemSetupResponse,
    SessionSetupRequest,
    SessionSetupResponse,
    TerminationSource,
)
from pddlsim.simulation import SimulationState


@dataclass(frozen=True)
class ErrorResult:
    """Represents a session prematurely terminated due to an error."""

    reason: str | None

    @override
    def __str__(self) -> str:
        return f"error: {self.reason if self.reason else ''}"


@dataclass(frozen=True)
class FailureResult:
    """Represents a session where not all problem goals were reached."""

    reason: str | None

    @override
    def __str__(self) -> str:
        return f"failure: {self.reason if self.reason else ''}"


@dataclass(frozen=True)
class SuccessResult:
    """Represents a session ended by achieving all problem goals."""

    @override
    def __str__(self) -> str:
        return "success"


type SessionResult = SuccessResult | FailureResult | ErrorResult
"""Represents the end results of a session, i.e., what caused it to stop."""


@dataclass
class SessionStatistics:
    """Statistics on the behavior of the agent during the session."""

    actions_attempted: int = 0
    failed_actions: int = 0
    perception_requests: int = 0
    goal_tracking_requests: int = 0
    get_grounded_actions_requests: int = 0


@dataclass(frozen=True)
class SessionSummary:
    """A summary of the behavior of the agent in a simulation session."""

    result: SessionResult
    statistics: SessionStatistics
    time_elapsed: float

    def is_success(self) -> bool:
        """Check if the result of the session is a success."""
        return isinstance(self.result, SuccessResult)

    @override
    def __str__(self) -> str:
        return str(self.result)


@dataclass
class SimulationClient:
    """Interface with a remote simulation."""

    _bridge: _RSPMessageBridge

    _state: SimulationState | None = None
    _domain_problem_pair: tuple[Domain, Problem] | None = None
    _grounded_actions: list[GroundedAction] | None = None
    _reached_and_unreached_goal_indices: tuple[list[int], list[int]] | None = (
        None
    )

    _statistics: SessionStatistics = field(default_factory=SessionStatistics)

    @classmethod
    def _from_reader_and_writer(
        cls, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> "SimulationClient":
        return SimulationClient(
            _RSPMessageBridge(
                reader,
                writer,
            )
        )

    async def _receive_payload[P: Payload](
        self, expected_payload_type: type[P]
    ) -> P:
        try:
            payload = await self._bridge.receive_payload()

            if not isinstance(payload, expected_payload_type):
                await self._terminate_session(
                    _SessionTerminationError(
                        Error.from_type_mismatch(
                            expected_payload_type, type(payload)
                        ),
                        TerminationSource.INTERNAL,
                    )
                )

            return payload
        except _SessionTerminationError as termination:
            await self._terminate_session(termination.with_traceback(None))

    async def _send_payload(self, payload: Payload) -> None:
        try:
            await self._bridge.send_message(payload)
        except _SessionTerminationError as termination:
            await self._terminate_session(termination.with_traceback(None))

    async def _terminate_session(
        self, termination: _SessionTerminationError
    ) -> NoReturn:
        if termination.source is TerminationSource.INTERNAL:
            await self._send_payload(termination._termination_payload)

        raise termination

    async def _start_session(self) -> None:
        await self._send_payload(SessionSetupRequest(_RSP_VERSION))

        _payload = await self._receive_payload(SessionSetupResponse)

    async def _get_problem_setup(self) -> tuple[Domain, Problem]:
        if not self._domain_problem_pair:
            await self._send_payload(ProblemSetupRequest())

            payload = await self._receive_payload(ProblemSetupResponse)

            self._domain_problem_pair = (
                payload.domain,
                payload.problem,
            )

        return self._domain_problem_pair

    async def get_domain(self) -> Domain:
        """Get the domain used in the simulation."""
        # This is not wasteful thanks to caching
        return (await self._get_problem_setup())[0]

    async def get_problem(self) -> Problem:
        """Get the problem used in the simulation.

        "Hidden information", in particular revealables
        and action fallibilities, are redacted.
        """
        # This is not wasteful thanks to caching
        return (await self._get_problem_setup())[1]

    async def _get_reached_and_unreached_goals(
        self,
    ) -> tuple[list[int], list[int]]:
        if not self._reached_and_unreached_goal_indices:
            self._statistics.goal_tracking_requests += 1
            await self._send_payload(GoalTrackingRequest())

            payload = await self._receive_payload(GoalTrackingResponse)

            self._reached_and_unreached_goal_indices = (
                payload.reached_goal_indices,
                payload.unreached_goal_indices,
            )

        return self._reached_and_unreached_goal_indices

    async def get_reached_goal_indices(self) -> Sequence[int]:
        """Get the indices of the problem goals that have been reached.

        By using `pddlsim.ast.GoalList.get_goal` on the problem's
        `pddlsim.ast.Problem.goals` one can see the condition corresponding to
        the index.
        """
        return (await self._get_reached_and_unreached_goals())[0]

    async def get_unreached_goal_indices(self) -> Sequence[int]:
        """Get the indices of the problem goals that have yet to be reached.

        By using `pddlsim.ast.GoalList.get_goal` on the problem's
        `pddlsim.ast.Problem.goals` one can see the condition corresponding to
        the index.
        """
        return (await self._get_reached_and_unreached_goals())[1]

    async def get_perceived_state(self) -> SimulationState:
        """Get the current state, as perceived by the agent.

        > [!NOTE]
        > This state can differ than the one obtained by using
        > `SimulationClient.get_domain` and `SimulationClient.get_problem`
        > and simulating changes to the state manually, as the problem
        > has its action fallibilities and revealables removed, as these
        > are considered hidden information.
        """
        if not self._state:
            self._statistics.perception_requests += 1
            await self._send_payload(PerceptionRequest())

            payload = await self._receive_payload(PerceptionResponse)

            self._state = SimulationState(set(payload.true_predicates))

        return self._state

    async def get_grounded_actions(self) -> Sequence[GroundedAction]:
        """Get all grounded actions  for the agent in the current state.

        > [!NOTE]
        > These actions can differ from those obtained by using
        > `SimulationClient.get_domain` and `SimulationClient.get_problem`
        > and simulating the problem manually, as the problem has its action
        > fallibilities and revealables removed, as these are considered hidden
        > information.
        """
        if not self._grounded_actions:
            self._statistics.get_grounded_actions_requests += 1
            await self._send_payload(GetGroundedActionsRequest())

            payload = await self._receive_payload(GetGroundedActionsResponse)

            self._grounded_actions = payload.grounded_actions

        return self._grounded_actions

    async def _perform_grounded_action(
        self, grounded_action: GroundedAction
    ) -> None:
        self._state = None
        self._grounded_actions = None
        self._reached_and_unreached_goal_indices = None

        self._statistics.actions_attempted += 1
        await self._send_payload(PerformGroundedActionRequest(grounded_action))
        response = await self._receive_payload(PerformGroundedActionResponse)
        self._statistics.failed_actions += not response.success

    async def _give_up(self, reason: str | None) -> None:
        await self._terminate_session(
            _SessionTerminationError(GiveUp(reason), TerminationSource.INTERNAL)
        )


@dataclass(frozen=True)
class GiveUpAction:
    """`SimulationAction` representing that the agent has given up.

    After making this action. the simulation will terminate.
    """

    reason: str | None = None

    @classmethod
    def from_dead_end(cls) -> "GiveUpAction":
        """Construct a `GiveUpAction` which is due to a dead end."""
        return GiveUpAction("dead end")


type SimulationAction = GiveUpAction | GroundedAction
"""An interaction of the agent with a simulation.

This can be a `pddlsim.simulation.GroundedAction`, which will affect the
state of the simulation, an indication by the agent that it is giving up
on the simulation, etc.
"""

type NextActionGetter = Callable[[], Awaitable[SimulationAction]]
"""A simple model of an agent, sequentially returning `SimulationAction`s.

The callable is async as the agent may need to use the `SimulationClient`,
which may involve communication with the simulation server.
"""
type AgentInitializer = Callable[
    [SimulationClient], Awaitable[NextActionGetter]
]
"""An agent initializer, allowing the agent to setup, and then returning it.

This acts as an "agent constructor", in such a way that the agent is expected
to store the `SimulationClient` handle it receives. Finally, assuming
initialization involves using the `SimulationClient`, the callable is
async.
"""


def with_no_initializer(
    get_next_action: Callable[[SimulationClient], Awaitable[SimulationAction]],
) -> AgentInitializer:
    """Wrap stateless agents into initializers.

    Most of PDDLSIM's API expects `AgentInitializer`s, so this function is
    useful for quickly making "dummy initializers" for stateless agents,
    while avoiding boilerplate.
    """

    async def no_op_initializer(client: SimulationClient) -> NextActionGetter:
        return lambda: get_next_action(client)

    return no_op_initializer


async def act_in_simulation(
    host: str,
    port: int,
    initializer: AgentInitializer,
) -> SessionSummary:
    """Connect to the remote simulation and run the agent on it.

    The remote simulation to connect to is specified as a `host` and
    `port` pair, where `host` is generally an IP address.

    The returned object (`SessionTermination`) represents how the simulation
    session ended.
    """
    reader, writer = await asyncio.open_connection(host, port)

    client = SimulationClient._from_reader_and_writer(reader, writer)

    start = time.monotonic()

    try:
        await client._start_session()

        get_next_action = await initializer(client)

        while True:
            action = await get_next_action()

            match action:
                case GiveUpAction(reason):
                    await client._give_up(reason)
                case GroundedAction():
                    await client._perform_grounded_action(action)
    except _SessionTerminationError as termination:
        match termination.payload:
            case GoalsReached():
                result: SessionResult = SuccessResult()
            case Error(reason):
                result = ErrorResult(reason)
            case other_payload:
                result = FailureResult(other_payload.description())

        return SessionSummary(
            result, client._statistics, time.monotonic() - start
        )
    except Exception as exception:
        exception_reason = str(exception)

        await client._bridge.send_message(
            Error(
                TerminationSource.INTERNAL,
                exception_reason
                if exception_reason
                else type(exception).__name__,
            )
        )

        raise exception
