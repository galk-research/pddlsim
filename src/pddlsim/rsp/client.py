import asyncio
from collections.abc import Awaitable, Callable, Sequence
from typing import NoReturn

from pddlsim.parser import Identifier, Object, Predicate
from pddlsim.rsp import (
    RSP_VERSION,
    RSPMessageBridge,
    SessionTermination,
)
from pddlsim.rsp.message import (
    Error,
    ErrorReason,
    GetGroundedActionsRequest,
    GetGroundedActionsResponse,
    GiveUp,
    Payload,
    PerceptionRequest,
    PerceptionResponse,
    PerformGroundedActionRequest,
    PerformGroundedActionResponse,
    ProblemSetupRequest,
    ProblemSetupResponse,
    ReasonString,
    SessionSetupRequest,
    SessionSetupResponse,
    TerminationSource,
)
from pddlsim.simulation import GroundedAction, SimulationState


class SimulationClient:
    def __init__(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        self._bridge = RSPMessageBridge(
            reader,
            writer,
        )

        self._domain_problem_pair: tuple[str, str] | None = None
        self._state: SimulationState | None = None
        self._grounded_actions: list[GroundedAction] | None = None

        self._termination: SessionTermination | None = None

    async def _receive_message[P: Payload](
        self, expected_message_type: type[P]
    ) -> P:
        try:
            message = await self._bridge.receive_message()

            if not isinstance(message, expected_message_type):
                await self._terminate_session(
                    SessionTermination(
                        Error.from_type_mismatch(
                            expected_message_type, type(message)
                        ),
                        TerminationSource.INTERNAL,
                    )
                )

            return message
        except SessionTermination as termination:
            await self._terminate_session(termination.with_traceback(None))

    async def _send_message(self, message: Payload) -> None:
        try:
            await self._bridge.send_message(message)
        except SessionTermination as termination:
            await self._terminate_session(termination.with_traceback(None))

    async def _terminate_session(
        self, termination: SessionTermination
    ) -> NoReturn:
        if termination.source is TerminationSource.INTERNAL:
            await self._send_message(termination.termination_payload)

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

            self._domain_problem_pair = (
                message.payload.domain,
                message.payload.problem,
            )

        return self._domain_problem_pair

    async def get_domain(self) -> str:
        # This is not wasteful thanks to caching
        return (await self._get_problem_setup())[0]

    async def get_problem(self) -> str:
        # This is not wasteful thanks to caching
        return (await self._get_problem_setup())[1]

    async def get_state(self) -> SimulationState:
        self._assert_unterminated()

        if not self._state:
            await self._send_message(PerceptionRequest())

            message = await self._receive_message(PerceptionResponse)

            self._state = SimulationState(
                {
                    Predicate(
                        Identifier(predicate.name),
                        tuple(
                            Object(object_name)
                            for object_name in predicate.assignment
                        ),
                    )
                    for predicate in message.payload
                }
            )

        return self._state

    async def get_grounded_actions(self) -> Sequence[GroundedAction]:
        self._assert_unterminated()

        if not self._grounded_actions:
            await self._send_message(GetGroundedActionsRequest())

            message = await self._receive_message(GetGroundedActionsResponse)

            self._grounded_actions = message.payload
        return self._grounded_actions

    async def _perform_grounded_action(
        self, grounded_action: GroundedAction
    ) -> None:
        self._assert_unterminated()

        self._state = None
        self._grounded_actions = None

        await self._send_message(PerformGroundedActionRequest(grounded_action))
        await self._receive_message(PerformGroundedActionResponse)

    async def _give_up(self, reason: ReasonString | None) -> None:
        self._assert_unterminated()

        await self._terminate_session(
            SessionTermination(GiveUp(reason), TerminationSource.INTERNAL)
        )


class GiveUpAction:
    def __init__(self, reason: str | None = None) -> None:
        self._reason = ReasonString(reason) if reason else None


class DeadEndAction(GiveUpAction):
    def __init__(self) -> None:
        super().__init__("dead end")


type SimulationAction = GiveUpAction | GroundedAction


async def act_in_simulation(
    host: str,
    port: int,
    get_next_action: Callable[[SimulationClient], Awaitable[SimulationAction]],
) -> SessionTermination:
    reader, writer = await asyncio.open_connection(host, port)

    simulation = SimulationClient(reader, writer)

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
    except Exception as exception:
        exception_reason = str(exception)

        await simulation._bridge.send_message(
            Error(
                ErrorReason(
                    TerminationSource.INTERNAL,
                    ReasonString(
                        exception_reason
                        if exception_reason
                        else type(exception).__name__
                    ),
                ),
            )
        )

        raise exception

    if not simulation._termination:
        raise AssertionError("simulation cannot end without termination")

    return simulation._termination
