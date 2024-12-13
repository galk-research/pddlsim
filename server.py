import asyncio
import logging

import pddlsim.rsp.server

logging.basicConfig(level=logging.DEBUG)


async def main() -> None:
    await pddlsim.rsp.server.start_simulator_server("domain.pddl", "instance.pddl", "127.0.0.1")


asyncio.run(main(), debug=True)
