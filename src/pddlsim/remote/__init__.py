"""Items for creating simulators and interacting with them over the internet.

This module contains two main submodules:

- `remote.client` contains items related to interfacing with simulations
and creating agents
- `remote.server` contains items related to create a simulator server
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import override

import cbor2

from pddlsim.remote._message import (
    Custom,
    Error,
    GoalsReached,
    Message,
    Payload,
    TerminationPayload,
    TerminationSource,
)

_RSP_VERSION = 1

_FRAME_LENGTH_BYTES = 4


class SessionTermination(Exception):  # noqa: N818
    """Represents the way in which a simulation session terminated."""

    def __init__(
        self,
        termination_payload: TerminationPayload,
        source: TerminationSource,
        *args: object,
    ) -> None:
        """Construct a `SessionTermination` from a payload and a source."""
        super().__init__(termination_payload, *args)

        self._termination_payload = termination_payload
        self.source = source

    def is_goals_reached(self) -> bool:
        """Check if the session terminated as all goals have been reached."""
        return isinstance(self._termination_payload, GoalsReached)

    def is_error(self) -> bool:
        """Check if the session has been terminated due to an error."""
        return isinstance(self._termination_payload, Error)

    @override
    def __str__(self):
        description = self._termination_payload.description()

        match self.source:
            case TerminationSource.INTERNAL:
                return f"session terminated internally: {description}"
            case TerminationSource.EXTERNAL:
                return f"session terminated externally: {description}"


@dataclass
class _RSPMessageBridge:
    _reader: asyncio.StreamReader
    _writer: asyncio.StreamWriter

    async def send_message(self, payload: Payload) -> None:
        serialized_message = Message(payload).serialize()
        logging.info(f"sending: {serialized_message}")

        data = cbor2.dumps(serialized_message)

        try:
            # If the amount of bytes doesn't fit in the 32-bit unsigned integer,
            # an overflow error is raised, so an invalid message is never sent
            self._writer.write(len(data).to_bytes(_FRAME_LENGTH_BYTES))
            self._writer.write(data)
            await self._writer.drain()
        except ConnectionResetError as exception:
            raise SessionTermination(
                Custom.from_communication_channel_closed(),
                TerminationSource.EXTERNAL,
            ) from exception

    async def receive_payload(self) -> Payload:
        try:
            byte_size = int.from_bytes(
                await self._reader.readexactly(_FRAME_LENGTH_BYTES)
            )
            value_bytes: bytes = await self._reader.readexactly(byte_size)
        except (asyncio.IncompleteReadError, ConnectionResetError) as exception:
            raise SessionTermination(
                Custom.from_communication_channel_closed(),
                TerminationSource.EXTERNAL,
            ) from exception

        serialized_message = cbor2.loads(value_bytes)
        logging.info(f"receiving: {serialized_message}")

        message = Message.deserialize(serialized_message).payload

        if isinstance(message, TerminationPayload):
            raise SessionTermination(message, TerminationSource.EXTERNAL)

        return message

    async def error(
        self, source: TerminationSource, reason: str | None
    ) -> SessionTermination:
        error_message = Error(source, reason)

        await self.send_message(error_message)

        return SessionTermination(error_message, TerminationSource.INTERNAL)
