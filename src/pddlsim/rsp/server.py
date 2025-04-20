import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import NoReturn

from pddlsim.parser import Domain, Problem
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
    GoalReached,
    Message,
    MessageTypeMismatchError,
    PerceptionRequest,
    PerceptionResponse,
    PerformGroundedActionRequest,
    PerformGroundedActionResponse,
    ProblemSetupRequest,
    SerializableGroundedAction,
    SerializablePredicate,
    SessionSetupRequest,
    SessionSetupResponse,
    SessionUnsupported,
    TerminationSource,
)
from pddlsim.simulation import GroundedAction, Simulation


async def _receive_message[T: Message](
    expected_message_type: type[T], bridge: RSPMessageBridge
) -> T:
    message = await bridge.receive_message()

    if not isinstance(message, expected_message_type):
        raise SessionTermination(
            MessageTypeMismatchError(expected_message_type, type(message)),
            TerminationSource.INTERNAL,
        )

    return message


async def _start_session(bridge: RSPMessageBridge) -> None:
    message = await _receive_message(SessionSetupRequest, bridge)

    if message.payload != RSP_VERSION:
        session_unsupported = SessionUnsupported()

        await bridge.send_message(session_unsupported)

        raise SessionTermination(
            session_unsupported, TerminationSource.INTERNAL
        )
    else:
        await bridge.send_message(SessionSetupResponse())


async def _problem_setup(
    simulation: Simulation, bridge: RSPMessageBridge
) -> None:
    # TODO: Figure out exactly how this is going to be done
    raise NotImplementedError


async def _perception(simulation: Simulation, bridge: RSPMessageBridge) -> None:
    await bridge.send_message(
        PerceptionResponse(
            [
                SerializablePredicate.from_predicate(predicate)
                for predicate in simulation.state.true_predicates()
            ]
        )
    )


async def _get_grounded_actions(
    simulation: Simulation, bridge: RSPMessageBridge
) -> None:
    await bridge.send_message(
        GetGroundedActionsResponse(
            [
                SerializableGroundedAction.from_grounded_action(grounded_action)
                for grounded_action in simulation.get_grounded_actions()
            ]
        )
    )


async def _perform_grounded_action(
    grounded_action: GroundedAction,
    simulation: Simulation,
    bridge: RSPMessageBridge,
) -> None:
    simulation.apply_grounded_action(grounded_action)

    if not simulation.is_solved():
        await bridge.send_message(PerformGroundedActionResponse())


async def _handle_requests(
    simulation: Simulation,
    bridge: RSPMessageBridge,
) -> NoReturn:
    while not simulation.is_solved():
        request = await bridge.receive_message()

        match request:
            case ProblemSetupRequest():
                await _problem_setup(simulation, bridge)
            case PerceptionRequest():
                await _perception(simulation, bridge)
            case GetGroundedActionsRequest():
                await _get_grounded_actions(simulation, bridge)
            case PerformGroundedActionRequest(payload=payload):
                await _perform_grounded_action(
                    GroundedAction.from_serializable_grounded_action(payload),
                    simulation,
                    bridge,
                )
            case _:
                raise SessionTermination(
                    Error(
                        ErrorReason(
                            TerminationSource.EXTERNAL,
                            f"expected request, got {request.type}",
                        )
                    ),
                    TerminationSource.INTERNAL,
                )

    raise SessionTermination(GoalReached(), TerminationSource.INTERNAL)


async def _operate_session(
    domain: Domain,
    problem: Problem,
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
) -> SessionTermination:
    bridge = RSPMessageBridge(reader, writer)

    try:
        simulation = Simulation.from_domain_and_problem(domain, problem)

        await _start_session(bridge)
        await _handle_requests(simulation, bridge)
    except SessionTermination as termination:
        logging.info(str(termination))

        if termination.source is TerminationSource.INTERNAL:
            await bridge.send_message(termination.message)

        return termination
    except Exception as exception:
        reason = str(exception)
        await bridge.send_message(
            Error(
                ErrorReason(
                    TerminationSource.INTERNAL,
                    reason if reason else str(type(exception).__name__),
                )
            )
        )

        raise exception


def _server_constructor(
    domain: Domain, problem: Problem
) -> Callable[[asyncio.StreamReader, asyncio.StreamWriter], Awaitable[None]]:
    async def _serve(
        reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        await _operate_session(domain, problem, reader, writer)

    return _serve


async def start_simulation_server(
    domain: Domain, problem: Problem, host: str, port: int | None = None
) -> None:
    server = await asyncio.start_server(
        _server_constructor(domain, problem), host, port
    )

    async with server:
        await server.serve_forever()
