import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import NoReturn

from pddlsim.fd_parser import FDParser
from pddlsim.parser_independent import PDDL
from pddlsim.rsp import (
    RSP_VERSION,
    RSPMessageBridge,
    SessionTermination,
)
from pddlsim.rsp.message import (
    Error,
    GetGroundedActionsRequest,
    GetGroundedActionsResponse,
    GoalReached,
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
    SessionUnsupported,
    TerminationSource,
)
from pddlsim.services.simulator_services import SimulatorServices
from pddlsim.simulator import Simulator


async def _receive_message[T: Message](expected_message_type: type[T], bridge: RSPMessageBridge) -> T:
    message = await bridge.receive_message()

    if not isinstance(message, expected_message_type):
        raise SessionTermination(MessageTypeMismatchError(expected_message_type, type(message)), TerminationSource.INTERNAL)

    return message


async def _start_session(bridge: RSPMessageBridge) -> None:
    message = await _receive_message(SessionSetupRequest, bridge)

    if message.supported_protocol_version != RSP_VERSION:
        session_unsupported = SessionUnsupported()

        await bridge.send_message(session_unsupported)

        raise SessionTermination(session_unsupported, TerminationSource.INTERNAL)
    else:
        await bridge.send_message(SessionSetupResponse())


async def _problem_setup(domain: str, problem: str, bridge: RSPMessageBridge) -> None:
    await bridge.send_message(ProblemSetupResponse(domain, problem))


async def _perception(simulation: Simulator, bridge: RSPMessageBridge) -> None:
    await bridge.send_message(PerceptionResponse(simulation.perceive_state()))


async def _get_grounded_actions(services: SimulatorServices, bridge: RSPMessageBridge) -> None:
    await bridge.send_message(GetGroundedActionsResponse([PDDL.parse_action(valid_action) for valid_action in services.valid_actions.get()]))


async def _goal_tracking(services: SimulatorServices, bridge: RSPMessageBridge) -> None:
    await bridge.send_message(GoalTrackingResponse(services.goal_tracking.completed_goals, services.goal_tracking.uncompleted_goals))


async def _perform_grounded_action(grounded_action: GroundedAction, simulation: Simulator, services: SimulatorServices, bridge: RSPMessageBridge) -> None:
    grounded_action_string = f"({grounded_action._action_name} {" ".join(grounded_action._grounding)})"

    effect_index = simulation.apply_action(grounded_action_string)
    services.on_action(grounded_action_string)

    if not simulation.goal_tracking.reached_all_goals():
        await bridge.send_message(PerformGroundedActionResponse(effect_index))


async def _handle_requests(domain: str, problem: str, simulation: Simulator, services: SimulatorServices, bridge: RSPMessageBridge) -> NoReturn:
    while not simulation.goal_tracking.reached_all_goals():
        request = await bridge.receive_message()

        match request:
            case ProblemSetupRequest():
                await _problem_setup(domain, problem, bridge)
            case PerceptionRequest():
                await _perception(simulation, bridge)
            case GetGroundedActionsRequest():
                await _get_grounded_actions(services, bridge)
            case GoalTrackingRequest():
                await _goal_tracking(services, bridge)
            case PerformGroundedActionRequest(grounded_action=grounded_action):
                await _perform_grounded_action(grounded_action, simulation, services, bridge)
            case _:
                raise SessionTermination(Error(TerminationSource.EXTERNAL, f"expected request message, got {request.message_type()}"), TerminationSource.INTERNAL)

    raise SessionTermination(GoalReached(), TerminationSource.INTERNAL)


async def _operate_session(domain_path: str, problem_path: str, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> SessionTermination:
    bridge = RSPMessageBridge(reader, writer)

    try:
        simulation = Simulator(FDParser(domain_path, problem_path))
        services = SimulatorServices(
            simulation.parser,
            simulation.perceive_state,
        )

        with open(domain_path) as domain_file, open(problem_path) as problem_file:
            domain = domain_file.read()
            problem = problem_file.read()

        await _start_session(bridge)
        await _handle_requests(domain, problem, simulation, services, bridge)
    except SessionTermination as termination:
        logging.info(str(termination))

        if termination.source is TerminationSource.INTERNAL:
            await bridge.send_message(termination.message)

        return termination
    except Exception as termination:
        raise termination


def _server_constructor(domain_path: str, problem_path: str) -> Callable[[asyncio.StreamReader, asyncio.StreamWriter], Awaitable[None]]:
    async def _serve(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        await _operate_session(domain_path, problem_path, reader, writer)

    return _serve


async def start_simulator_server(domain_path: str, problem_path: str, host: str, port: int | None = None) -> None:
    server = await asyncio.start_server(_server_constructor(domain_path, problem_path), host, port)

    async with server:
        await server.serve_forever()
