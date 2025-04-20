import asyncio
import logging
from dataclasses import asdict

import cbor2

from pddlsim.rsp.message import (
    CommunicationChannelClosed,
    Error,
    ErrorReason,
    Message,
    TerminationMessage,
    TerminationSource,
    deserialize_message,
)

RSP_VERSION = 1

MAXIMUM_VALUE_BITS_BYTES = 4


class SessionTermination(Exception):
    def __init__(
        self,
        termination_message: TerminationMessage,
        source: TerminationSource,
        *args: object,
    ) -> None:
        super().__init__(termination_message, *args)

        self.message = termination_message
        self.source = source

    def __str__(self):
        description = self.message.description()

        match self.source:
            case TerminationSource.INTERNAL:
                return f"session terminated internally: {description}"
            case TerminationSource.EXTERNAL:
                return f"session terminated externally: {description}"


class RSPMessageBridge:
    def __init__(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        self.reader = reader
        self.writer = writer

    async def send_message(self, message: Message) -> None:
        serialized_message = asdict(message)
        logging.info(f"sending: {serialized_message}")

        data = cbor2.dumps(serialized_message)

        try:
            self.writer.write(len(data).to_bytes(MAXIMUM_VALUE_BITS_BYTES))
            self.writer.write(data)
            await self.writer.drain()
        except ConnectionResetError as exception:
            raise SessionTermination(
                CommunicationChannelClosed(), TerminationSource.EXTERNAL
            ) from exception

    async def receive_message(self) -> Message:
        try:
            byte_size = int.from_bytes(
                await self.reader.readexactly(MAXIMUM_VALUE_BITS_BYTES)
            )
            value_bytes: bytes = await self.reader.readexactly(byte_size)
        except (asyncio.IncompleteReadError, ConnectionResetError) as exception:
            raise SessionTermination(
                CommunicationChannelClosed(), TerminationSource.EXTERNAL
            ) from exception

        serialized_message = cbor2.loads(value_bytes)
        logging.info(f"receiving: {serialized_message}")

        message = deserialize_message(serialized_message)

        if isinstance(message, TerminationMessage):
            raise SessionTermination(message, TerminationSource.EXTERNAL)

        return message

    async def error(
        self, source: TerminationSource, reason: str | None
    ) -> SessionTermination:
        error_message = Error(ErrorReason(source, reason))

        await self.send_message(error_message)

        return SessionTermination(error_message, TerminationSource.INTERNAL)
