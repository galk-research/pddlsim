import asyncio
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from typing import NoReturn

from pddlsim.rsp import (
    RSP_VERSION,
    RSPMessageBridge,
    SessionTermination,
)
from pddlsim.rsp.message import (
    Error,
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

    async def _receive_payload[P: Payload](
        self, expected_payload_type: type[P]
    ) -> P:
        try:
            payload = await self._bridge.receive_payload()

            if not isinstance(payload, expected_payload_type):
                await self._terminate_session(
                    SessionTermination(
                        Error.from_type_mismatch(
                            expected_payload_type, type(payload)
                        ),
                        TerminationSource.INTERNAL,
                    )
                )

            return payload
        except SessionTermination as termination:
            await self._terminate_session(termination.with_traceback(None))

    async def _send_message(self, payload: Payload) -> None:
        try:
            await self._bridge.send_message(payload)
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

        _message = await self._receive_payload(SessionSetupResponse)

    async def _get_problem_setup(self) -> tuple[str, str]:
        self._assert_unterminated()

        if not self._domain_problem_pair:
            await self._send_message(ProblemSetupRequest())

            payload = await self._receive_payload(ProblemSetupResponse)

            self._domain_problem_pair = (
                payload.domain,
                payload.problem,
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

            payload = await self._receive_payload(PerceptionResponse)

            self._state = SimulationState(set(payload.true_predicates))

        return self._state

    async def get_grounded_actions(self) -> Sequence[GroundedAction]:
        self._assert_unterminated()

        if not self._grounded_actions:
            await self._send_message(GetGroundedActionsRequest())

            payload = await self._receive_payload(GetGroundedActionsResponse)

            self._grounded_actions = payload.grounded_actions

        return self._grounded_actions

    async def _perform_grounded_action(
        self, grounded_action: GroundedAction
    ) -> None:
        self._assert_unterminated()

        self._state = None
        self._grounded_actions = None

        await self._send_message(PerformGroundedActionRequest(grounded_action))
        await self._receive_payload(PerformGroundedActionResponse)

    async def _give_up(self, reason: str | None) -> None:
        self._assert_unterminated()

        await self._terminate_session(
            SessionTermination(GiveUp(reason), TerminationSource.INTERNAL)
        )


@dataclass(frozen=True)
class GiveUpAction:
    reason: str | None = None


class DeadEndAction(GiveUpAction):
    def __init__(self) -> None:
        super().__init__("dead end")


type SimulationAction = GiveUpAction | GroundedAction


type NextActionGetter = Callable[[], Awaitable[SimulationAction]]
type AgentInitializer = Callable[
    [SimulationClient], Awaitable[NextActionGetter]
]


def with_no_initializer(
    get_next_action: Callable[[SimulationClient], Awaitable[SimulationAction]],
) -> AgentInitializer:
    async def no_op_initializer(client: SimulationClient) -> NextActionGetter:
        return lambda: get_next_action(client)

    return no_op_initializer


async def act_in_simulation(
    host: str,
    port: int,
    initializer: AgentInitializer,
) -> SessionTermination:
    reader, writer = await asyncio.open_connection(host, port)

    client = SimulationClient(reader, writer)

    try:
        await client._start_session()

        get_next_action = await initializer(client)

        while not client._is_terminated():
            action = await get_next_action()

            match action:
                case GiveUpAction(reason):
                    await client._give_up(reason)
                case GroundedAction():
                    await client._perform_grounded_action(action)
    except SessionTermination:
        pass
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

    if not client._termination:
        raise AssertionError("simulation cannot end without termination")

    return client._termination
