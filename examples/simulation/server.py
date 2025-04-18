import asyncio
import logging

import pddlsim.rsp.server
from pddlsim.parser import (
    parse_domain_from_file,
    parse_problem_from_file,
)

logging.basicConfig(level=logging.DEBUG)


async def main() -> None:
    await pddlsim.rsp.server.start_simulation_server(
        parse_domain_from_file("assets/problems/gripper/domain.pddl"),
        parse_problem_from_file("assets/problems/gripper/instance.pddl"),
        "127.0.0.1",
    )


asyncio.run(main(), debug=True)
