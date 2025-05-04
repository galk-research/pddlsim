import asyncio
import logging

import cbor2

from pddlsim.remote._message import (
    Custom,
    Error,
    GoalReached,
    Message,
    Payload,
    TerminationPayload,
    TerminationSource,
)

RSP_VERSION = 1

MAXIMUM_VALUE_BITS_BYTES = 4


class SessionTermination(Exception):
    def __init__(
        self,
        termination_payload: TerminationPayload,
        source: TerminationSource,
        *args: object,
    ) -> None:
        super().__init__(termination_payload, *args)

        self._termination_payload = termination_payload
        self.source = source

    def is_goal_reached(self) -> bool:
        return isinstance(self._termination_payload, GoalReached)

    def is_error(self) -> bool:
        return isinstance(self._termination_payload, Error)

    @property
    def payload(self) -> TerminationPayload:
        return self._termination_payload

    def __str__(self):
        description = self._termination_payload.description()

        match self.source:
            case TerminationSource.INTERNAL:
                return f"session terminated internally: {description}"
            case TerminationSource.EXTERNAL:
                return f"session terminated externally: {description}"


class _RSPMessageBridge:
    def __init__(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        self.reader = reader
        self.writer = writer

    async def send_message(self, payload: Payload) -> None:
        serialized_message = Message(payload).serialize()
        logging.info(f"sending: {serialized_message}")

        data = cbor2.dumps(serialized_message)

        try:
            self.writer.write(len(data).to_bytes(MAXIMUM_VALUE_BITS_BYTES))
            self.writer.write(data)
            await self.writer.drain()
        except ConnectionResetError as exception:
            raise SessionTermination(
                Custom.from_communication_channel_closed(),
                TerminationSource.EXTERNAL,
            ) from exception

    async def receive_payload(self) -> Payload:
        try:
            byte_size = int.from_bytes(
                await self.reader.readexactly(MAXIMUM_VALUE_BITS_BYTES)
            )
            value_bytes: bytes = await self.reader.readexactly(byte_size)
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
