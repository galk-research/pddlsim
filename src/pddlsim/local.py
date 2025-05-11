"""Utilities for local simulation, with a similar API to remote simulation."""

import os
from dataclasses import dataclass
from typing import ClassVar

from pddlsim.ast import Domain, Problem
from pddlsim.parser import parse_domain_problem_pair_from_files
from pddlsim.remote import client
from pddlsim.remote.server import _SimulationServer


@dataclass(frozen=True)
class LocalSimulator:
    """Local simulator for running multiple local agent simulation sessions.

    The main constructor is `LocalSimulator.from_domain_problem_pair`.
    """

    _server: _SimulationServer

    _HOST: ClassVar = "127.0.0.1"

    @classmethod
    async def from_domain_problem_pair(
        cls, domain: Domain, problem: Problem
    ) -> "LocalSimulator":
        """Create a `LocalSimulator` from a `pddlsim.ast.Domain` and a `pddlsim.ast.Problem`."""  # noqa: E501
        return LocalSimulator(
            await _SimulationServer.from_host_and_port(
                domain, problem, LocalSimulator._HOST
            )
        )

    @classmethod
    async def from_domain_problem_pair_files(
        cls, domain_path: str | os.PathLike, problem_path: str | os.PathLike
    ) -> "LocalSimulator":
        """Create a `LocalSimulator` from paths to a domain and problem."""
        domain, problem = parse_domain_problem_pair_from_files(
            domain_path, problem_path
        )

        return await cls.from_domain_problem_pair(domain, problem)

    async def simulate(
        self, initializer: client.AgentInitializer
    ) -> client.SessionSummary:
        """Run the provided agent on the simulation until termination.

        The returned value is an object representing how the simulation ended.
        """
        return await client.act_in_simulation(
            self._server.host, self._server.port, initializer
        )


async def simulate_domain_problem_pair(
    domain: Domain, problem: Problem, initializer: client.AgentInitializer
) -> client.SessionSummary:
    """Simulate the provided agent on a domain-problem pair.

    The returned value is an object representing how the simulation ended.
    """
    simulator = await LocalSimulator.from_domain_problem_pair(domain, problem)

    return await simulator.simulate(initializer)


async def simulate_domain_problem_pair_from_files(
    domain_path: str | os.PathLike,
    problem_path: str | os.PathLike,
    initializer: client.AgentInitializer,
) -> client.SessionSummary:
    """Simulate the provided agent on a domain-problem pair, given their paths.

    The returned value is an object representing how the simulation ended.
    """
    simulator = await LocalSimulator.from_domain_problem_pair_files(
        domain_path, problem_path
    )

    return await simulator.simulate(initializer)
