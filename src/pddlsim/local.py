import os
from dataclasses import dataclass

from pddlsim.ast import Domain, Problem
from pddlsim.parser import parse_domain_problem_pair_from_files
from pddlsim.remote import SessionTermination, client
from pddlsim.remote.server import _SimulationServer


@dataclass(frozen=True)
class LocalSimulator:
    _server: _SimulationServer

    HOST = "127.0.0.1"

    @classmethod
    async def from_domain_problem_pair(
        cls, domain: Domain, problem: Problem
    ) -> "LocalSimulator":
        return LocalSimulator(
            await _SimulationServer.from_host_and_port(
                domain, problem, LocalSimulator.HOST
            )
        )

    @classmethod
    async def from_domain_problem_pair_files(
        cls, domain_path: str | os.PathLike, problem_path: str | os.PathLike
    ) -> "LocalSimulator":
        domain, problem = parse_domain_problem_pair_from_files(
            domain_path, problem_path
        )

        return await cls.from_domain_problem_pair(domain, problem)

    async def simulate(
        self, initializer: client.AgentInitializer
    ) -> SessionTermination:
        return await client.act_in_simulation(
            self._server.host, self._server.port, initializer
        )


async def simulate_domain_problem_pair(
    domain: Domain, problem: Problem, initializer: client.AgentInitializer
) -> SessionTermination:
    simulator = await LocalSimulator.from_domain_problem_pair(domain, problem)

    return await simulator.simulate(initializer)


async def simulate_domain_problem_pair_from_files(
    domain_path: str | os.PathLike,
    problem_path: str | os.PathLike,
    initializer: client.AgentInitializer,
) -> SessionTermination:
    simulator = await LocalSimulator.from_domain_problem_pair_files(
        domain_path, problem_path
    )

    return await simulator.simulate(initializer)
