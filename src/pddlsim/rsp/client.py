import asyncio
from collections.abc import Awaitable, Callable
from typing import NoReturn

from pddlsim.rsp import (
    RSP_VERSION,
    RSPMessageBridge,
    SessionTermination,
)
from pddlsim.rsp.message import (
    GetGroundedActionsRequest,
    GetGroundedActionsResponse,
    GiveUp,
    GoalTrackingRequest,
    GoalTrackingResponse,
    GroundedAction,
    Message,
    MessageTypeMismatchError,
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


class Simulation:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        self._bridge = RSPMessageBridge(
            reader,
            writer,
        )

        self._domain_problem_pair: tuple[str, str] | None = None
        self._percepts: dict[str, list[list[str]]] | None = None
        self._grounded_actions: list[GroundedAction] | None = None
        self._reached_unreached_goals_pair: tuple[list[str], list[str]] | None = None

        self._termination: SessionTermination | None = None

    async def _receive_message[T: Message](self, expected_message_type: type[T]) -> T:
        try:
            message = await self._bridge.receive_message()

            if not isinstance(message, expected_message_type):
                await self._terminate_session(SessionTermination(MessageTypeMismatchError(expected_message_type, type(message)), TerminationSource.INTERNAL))

            return message
        except SessionTermination as termination:
            await self._terminate_session(termination.with_traceback(None))

    async def _send_message(self, message: Message) -> None:
        try:
            await self._bridge.send_message(message)
        except SessionTermination as termination:
            await self._terminate_session(termination.with_traceback(None))

    async def _terminate_session(self, termination: SessionTermination) -> NoReturn:
        if termination.source is TerminationSource.INTERNAL:
            await self._send_message(termination.message)

        self._termination = termination

        raise self._termination

    def _is_terminated(self) -> bool:
        return self._termination is not None

    def _assert_unterminated(self) -> None:
        if self._is_terminated():
            raise self._termination  # type: ignore

    async def _start_session(self) -> None:
        await self._send_message(SessionSetupRequest(RSP_VERSION))

        _message = await self._receive_message(SessionSetupResponse)

    async def _get_problem_setup(self) -> tuple[str, str]:
        self._assert_unterminated()

        if not self._domain_problem_pair:
            await self._send_message(ProblemSetupRequest())

            message = await self._receive_message(ProblemSetupResponse)

            self._domain_problem_pair = (message.domain, message.problem)

        return self._domain_problem_pair

    async def get_domain(self) -> str:
        # This is not wasteful thanks to caching
        return (await self._get_problem_setup())[0]

    async def get_problem(self) -> str:
        # This is not wasteful thanks to caching
        return (await self._get_problem_setup())[1]

    async def get_percepts(self) -> dict[str, list[list[str]]]:
        self._assert_unterminated()

        if not self._percepts:
            await self._send_message(PerceptionRequest())

            message = await self._receive_message(PerceptionResponse)

            self._percepts = message.percepts

        return self._percepts

    async def get_grounded_actions(self) -> list[GroundedAction]:
        self._assert_unterminated()

        if not self._grounded_actions:
            await self._send_message(GetGroundedActionsRequest())

            message = await self._receive_message(GetGroundedActionsResponse)

            self._grounded_actions = message.grounded_actions

        return self._grounded_actions

    async def _goal_tracking(self) -> tuple[list[str], list[str]]:
        self._assert_unterminated()

        if not self._reached_unreached_goals_pair:
            await self._send_message(GoalTrackingRequest())

            message = await self._receive_message(GoalTrackingResponse)

            self._reached_unreached_goals_pair = (message.reached_goals, message.unreached_goals)

        return self._reached_unreached_goals_pair

    async def reached_goals(self) -> list[str]:
        # This is not wasteful thanks to caching
        return (await self._goal_tracking())[0]

    async def unreached_goals(self) -> list[str]:
        # This is not wasteful thanks to caching
        return (await self._goal_tracking())[1]

    async def _perform_grounded_action(self, grounded_action: GroundedAction) -> int:
        self._assert_unterminated()

        self._percepts = None
        self._grounded_actions = None
        self._reached_unreached_goals_pair = None

        await self._send_message(PerformGroundedActionRequest(grounded_action))

        message = await self._receive_message(PerformGroundedActionResponse)

        return message.effect_index

    async def _give_up(self, reason: str | None) -> None:
        self._assert_unterminated()

        await self._terminate_session(SessionTermination(GiveUp(reason), TerminationSource.INTERNAL))


class GiveUpAction:
    def __init__(self, reason: str | None = None) -> None:
        self._reason = reason


class DeadEndAction(GiveUpAction):
    def __init__(self) -> None:
        super().__init__("dead end")


type SimulationAction = GiveUpAction | GroundedAction


async def act_in_simulation(host: str, port: int, get_next_action: Callable[[Simulation], Awaitable[SimulationAction]]) -> SessionTermination:
    reader, writer = await asyncio.open_connection(host, port)

    simulation = Simulation(reader, writer)

    try:
        await simulation._start_session()

        while not simulation._is_terminated():
            action = await get_next_action(simulation)

            match action:
                case GiveUpAction(_reason=reason):
                    await simulation._give_up(reason)
                case GroundedAction():
                    await simulation._perform_grounded_action(action)
    except SessionTermination:
        pass

    return simulation._termination  # type: ignore
