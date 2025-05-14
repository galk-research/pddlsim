import asyncio
import logging

import pddlsim.remote.server


async def main() -> None:
    await pddlsim.remote.server.start_simulation_server(
        pddlsim.remote.server.SimulatorConfiguration.from_domain_and_problem_files(
            "assets/problems/dungeon/domain.pddl",
            "assets/problems/dungeon/instance-1-reveal.pddl",
        ),
        "127.0.0.1",
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    asyncio.run(main(), debug=True)
