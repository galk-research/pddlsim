"""Code for opening a simulation server accessible by the internet."""

import asyncio
import logging
import os
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import NoReturn

from pddlsim.ast import Domain, Problem
from pddlsim.parser import parse_domain_problem_pair_from_files
from pddlsim.remote import (
    _RSP_VERSION,
    SessionTermination,
    _RSPMessageBridge,
)
from pddlsim.remote._message import (
    Error,
    GetGroundedActionsRequest,
    GetGroundedActionsResponse,
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
    SessionUnsupported,
    TerminationSource,
)
from pddlsim.simulation import GroundedAction, Simulation


async def _receive_message[T: Payload](
    expected_message_type: type[T], bridge: _RSPMessageBridge
) -> T:
    message = await bridge.receive_payload()

    if not isinstance(message, expected_message_type):
        raise SessionTermination(
            Error.from_type_mismatch(expected_message_type, type(message)),
            TerminationSource.INTERNAL,
        )

    return message


async def _start_session(bridge: _RSPMessageBridge) -> None:
    message = await _receive_message(SessionSetupRequest, bridge)

    if message.supported_rsp_version != _RSP_VERSION:
        session_unsupported = SessionUnsupported()

        await bridge.send_message(session_unsupported)

        raise SessionTermination(
            session_unsupported, TerminationSource.INTERNAL
        )
    else:
        await bridge.send_message(SessionSetupResponse())


async def _problem_setup(
    simulation: Simulation, bridge: _RSPMessageBridge
) -> None:
    await bridge.send_message(
        ProblemSetupResponse(simulation.domain, simulation.problem)
    )


async def _perception(
    simulation: Simulation, bridge: _RSPMessageBridge
) -> None:
    await bridge.send_message(PerceptionResponse(list(simulation.state)))


async def _goal_tracking(
    simulation: Simulation, bridge: _RSPMessageBridge
) -> None:
    await bridge.send_message(
        GoalTrackingResponse(
            simulation.reached_goal_indices, simulation.unreached_goal_indices
        )
    )


async def _get_grounded_actions(
    simulation: Simulation, bridge: _RSPMessageBridge
) -> None:
    await bridge.send_message(
        GetGroundedActionsResponse(list(simulation.get_grounded_actions()))
    )


async def _perform_grounded_action(
    grounded_action: GroundedAction,
    simulation: Simulation,
    bridge: _RSPMessageBridge,
) -> None:
    simulation.apply_grounded_action(grounded_action)

    if not simulation.is_solved():
        await bridge.send_message(PerformGroundedActionResponse())


async def _handle_requests(
    simulation: Simulation,
    bridge: _RSPMessageBridge,
) -> NoReturn:
    while not simulation.is_solved():
        request = await bridge.receive_payload()

        match request:
            case ProblemSetupRequest():
                await _problem_setup(simulation, bridge)
            case PerceptionRequest():
                await _perception(simulation, bridge)
            case GoalTrackingRequest():
                await _goal_tracking(simulation, bridge)
            case GetGroundedActionsRequest():
                await _get_grounded_actions(simulation, bridge)
            case PerformGroundedActionRequest(grounded_action):
                await _perform_grounded_action(
                    grounded_action,
                    simulation,
                    bridge,
                )
            case _:
                raise SessionTermination(
                    Error(
                        TerminationSource.EXTERNAL,
                        f"expected request, got {request.type()}",
                    ),
                    TerminationSource.INTERNAL,
                )

    raise SessionTermination(GoalsReached(), TerminationSource.INTERNAL)


async def _operate_session(
    domain: Domain,
    problem: Problem,
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
) -> SessionTermination:
    bridge = _RSPMessageBridge(reader, writer)

    try:
        simulation = Simulation.from_domain_and_problem(domain, problem)

        await _start_session(bridge)
        await _handle_requests(simulation, bridge)
    except SessionTermination as termination:
        logging.info(str(termination))

        if termination.source is TerminationSource.INTERNAL:
            await bridge.send_message(termination._termination_payload)

        return termination
    except Exception as exception:
        exception_reason = str(exception)

        await bridge.send_message(
            Error(
                TerminationSource.INTERNAL,
                exception_reason
                if exception_reason
                else str(type(exception).__name__),
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


@dataclass(frozen=True)
class _SimulationServer:
    domain: Domain
    problem: Problem
    _server: asyncio.Server

    @classmethod
    async def from_host_and_port(
        cls,
        domain: Domain,
        problem: Problem,
        host: str,
        port: int | None = None,
    ) -> "_SimulationServer":
        server = await asyncio.start_server(
            _server_constructor(domain, problem), host, port
        )

        return _SimulationServer(domain, problem, server)

    @property
    def host(self) -> str:
        return self._server.sockets[0].getsockname()[0]

    @property
    def port(self) -> int:
        return self._server.sockets[0].getsockname()[1]

    async def serve(self) -> NoReturn:
        async with self._server:
            await self._server.serve_forever()

        raise AssertionError("serve must never end normally")


async def start_simulation_server(
    domain: Domain, problem: Problem, host: str, port: int | None = None
) -> None:
    """Open a simulation server for a domain and problem.

    `host` and `port` form a pair, specifying the network interface
    to open the server on. If the port is unspecified, it is chosen by the OS.
    """
    server = await _SimulationServer.from_host_and_port(
        domain, problem, host, port
    )

    await server.serve()


async def start_simulation_server_from_files(
    domain_path: str | os.PathLike,
    problem_path: str | os.PathLike,
    host: str,
    port: int | None = None,
) -> None:
    """Open a simulation server for a domain and problem, specified by path.

    `host` and `port` form a pair, specifying the network interface
    to open the server on. If the port is unspecified, it is chosen by the OS.
    """
    domain, problem = parse_domain_problem_pair_from_files(
        domain_path, problem_path
    )

    server = await _SimulationServer.from_host_and_port(
        domain, problem, host, port
    )

    await server.serve()
