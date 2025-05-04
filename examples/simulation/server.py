import asyncio
import logging

import pddlsim.remote.server


async def main() -> None:
    await pddlsim.remote.server.start_simulation_server_from_files(
        "assets/problems/gripper/domain.pddl",
        "assets/problems/gripper/instance.pddl",
        "127.0.0.1",
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    asyncio.run(main(), debug=True)
