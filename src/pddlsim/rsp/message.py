from abc import ABC, abstractmethod
from collections.abc import Iterable
from enum import StrEnum
from typing import Self

import cbor2
import schema  # type: ignore
from schema import Schema

from pddlsim.parser import Identifier, ObjectName
from pddlsim.simulation import GroundedAction, SimulationState


class Message(ABC):
    @classmethod
    @abstractmethod
    def message_type(cls) -> str:
        raise NotImplementedError

    @abstractmethod
    def serialize_payload(self) -> cbor2.Any:
        raise NotImplementedError

    def serialize(self) -> cbor2.Any:
        return {
            "type": type(self).message_type(),
            "payload": self.serialize_payload(),
        }

    @classmethod
    @abstractmethod
    def schema(cls) -> Schema:
        raise NotImplementedError

    @classmethod
    def validate(cls, value: cbor2.Any):
        cls.schema().validate(value)

    @classmethod
    @abstractmethod
    def _deserialize(cls, value: cbor2.Any) -> Self:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, value: cbor2.Any) -> Self:
        cls.validate(value)

        return cls._deserialize(value)


class SessionSetupRequest(Message):
    def __init__(self, supported_protocol_version: int) -> None:
        super().__init__()

        if supported_protocol_version <= 0:
            raise ValueError("protocol version must be greater than 0")

        self.supported_protocol_version = supported_protocol_version

    @classmethod
    def message_type(cls) -> str:
        return "session-setup-request"

    def serialize_payload(self) -> cbor2.Any:
        return self.supported_protocol_version

    @classmethod
    def schema(cls) -> Schema:
        return Schema(schema.And(int, lambda version: version > 0))

    @classmethod
    def _deserialize(cls, value: cbor2.Any) -> "SessionSetupRequest":
        return SessionSetupRequest(value)


class SessionSetupResponse(Message):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def message_type(cls) -> str:
        return "session-setup-response"

    def serialize_payload(self) -> cbor2.Any:
        return None

    @classmethod
    def schema(cls) -> Schema:
        return Schema(None)

    @classmethod
    def _deserialize(cls, value: cbor2.Any) -> "SessionSetupResponse":
        return SessionSetupResponse()


class ProblemSetupRequest(Message):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def message_type(cls) -> str:
        return "problem-setup-request"

    def serialize_payload(self) -> cbor2.Any:
        return None

    @classmethod
    def schema(cls) -> Schema:
        return Schema(None)

    @classmethod
    def _deserialize(cls, value: cbor2.Any) -> "ProblemSetupRequest":
        return ProblemSetupRequest()


class ProblemSetupResponse(Message):
    def __init__(self, domain: str, problem: str) -> None:
        super().__init__()

        self.domain = domain
        self.problem = problem

    @classmethod
    def message_type(cls) -> str:
        return "problem-setup-response"

    def serialize_payload(self) -> cbor2.Any:
        return {"domain": self.domain, "problem": self.problem}

    @classmethod
    def schema(cls) -> Schema:
        return Schema({"domain": str, "problem": str})

    @classmethod
    def _deserialize(cls, value: cbor2.Any) -> "ProblemSetupResponse":
        return ProblemSetupResponse(value["domain"], value["problem"])


class PerceptionRequest(Message):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def message_type(cls) -> str:
        return "perception-request"

    def serialize_payload(self) -> cbor2.Any:
        return None

    @classmethod
    def schema(cls) -> Schema:
        return Schema(None)

    @classmethod
    def _deserialize(cls, value: cbor2.Any) -> "PerceptionRequest":
        return PerceptionRequest()


class PerceptionResponse(Message):
    def __init__(self, simulation_state: SimulationState) -> None:
        super().__init__()

        self.simulation_state = simulation_state

    @classmethod
    def message_type(cls) -> str:
        return "perception-response"

    def serialize_payload(self) -> cbor2.Any:
        return self.simulation_state.percepts()

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                str: [[str]],
            }
        )

    @classmethod
    def _deserialize(cls, value: cbor2.Any) -> "PerceptionResponse":
        return PerceptionResponse(value)


class GetGroundedActionsRequest(Message):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def message_type(cls) -> str:
        return "get-grounded-actions-request"

    def serialize_payload(self) -> cbor2.Any:
        return None

    @classmethod
    def schema(cls) -> Schema:
        return Schema(None)

    @classmethod
    def _deserialize(cls, value: cbor2.Any) -> "GetGroundedActionsRequest":
        return GetGroundedActionsRequest()


class GetGroundedActionsResponse(Message):
    def __init__(self, grounded_actions: Iterable[GroundedAction]) -> None:
        super().__init__()

        self.grounded_actions = tuple(grounded_actions)

    @classmethod
    def message_type(cls) -> str:
        return "get-grounded-actions-response"

    def serialize_payload(self) -> cbor2.Any:
        return [
            {
                "name": grounded_action.name.value,
                "grounding": [
                    object_name.value
                    for object_name in grounded_action.grounding
                ],
            }
            for grounded_action in self.grounded_actions
        ]

    @classmethod
    def schema(cls) -> Schema:
        return Schema([{"name": str, "grounding": [str]}])

    @classmethod
    def _deserialize(cls, value: cbor2.Any) -> "GetGroundedActionsResponse":
        return GetGroundedActionsResponse(
            GroundedAction(
                grounded_action["name"], grounded_action["grounding"]
            )
            for grounded_action in value
        )


class PerformGroundedActionRequest(Message):
    def __init__(self, grounded_action: GroundedAction) -> None:
        super().__init__()

        self.grounded_action = grounded_action

    @classmethod
    def message_type(cls) -> str:
        return "perform-grounded-action-request"

    def serialize_payload(self) -> cbor2.Any:
        return {
            "name": self.grounded_action.name,
            "grounding": self.grounded_action.grounding,
        }

    @classmethod
    def schema(cls) -> Schema:
        return Schema({"name": str, "grounding": [str]})

    @classmethod
    def _deserialize(cls, value: cbor2.Any) -> "PerformGroundedActionRequest":
        return PerformGroundedActionRequest(
            GroundedAction(
                Identifier(value["name"]),
                tuple(
                    ObjectName(object_name)
                    for object_name in value["grounding"]
                ),
            )
        )


class PerformGroundedActionResponse(Message):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def message_type(cls) -> str:
        return "perform-grounded-action-response"

    def serialize_payload(self) -> cbor2.Any:
        return None

    @classmethod
    def schema(cls) -> Schema:
        return Schema(None)

    @classmethod
    def _deserialize(cls, value: cbor2.Any) -> "PerformGroundedActionResponse":
        return PerformGroundedActionResponse()


class TerminationMessage(Message):
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError


class GoalReached(TerminationMessage):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def message_type(cls) -> str:
        return "goal-reached"

    def serialize_payload(self) -> cbor2.Any:
        return None

    @classmethod
    def schema(cls) -> Schema:
        return Schema(None)

    @classmethod
    def _deserialize(cls, value: cbor2.Any) -> "GoalReached":
        return GoalReached()

    def description(self):
        return "goal reached"


class TerminationSource(StrEnum):
    INTERNAL = "internal"
    EXTERNAL = "external"


class Error(TerminationMessage):
    def __init__(self, source: TerminationSource, reason: str | None) -> None:
        super().__init__()

        self.source = source
        self.reason = reason

    @classmethod
    def message_type(cls) -> str:
        return "error"

    def serialize_payload(self) -> cbor2.Any:
        return {"source": self.source, "reason": self.reason}

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                "source": schema.Use(TerminationSource),
                "reason": schema.Or(str, None),
            }
        )

    @classmethod
    def _deserialize(cls, value: cbor2.Any) -> "Error":
        return Error(value["source"], value["reason"])

    def description(self) -> str:
        return (
            f"{self.reason} ({self.source} error)"
            if self.reason
            else f"{self.source} error"
        )


class MessageTypeMismatchError(Error):
    def __init__(
        self,
        expected_message_type: type[Message],
        received_message_type: type[Message],
    ):
        super().__init__(
            TerminationSource.EXTERNAL,
            f"expected {expected_message_type.message_type()}, "
            f"got {received_message_type.message_type()}",
        )


class SessionUnsupported(TerminationMessage):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def message_type(cls) -> str:
        return "session-unsupported"

    def serialize_payload(self) -> cbor2.Any:
        return None

    @classmethod
    def schema(cls) -> Schema:
        return Schema(None)

    @classmethod
    def _deserialize(cls, value: cbor2.Any) -> "SessionUnsupported":
        return SessionUnsupported()

    def description(self) -> str:
        return "session unsupported"


class Timeout(TerminationMessage):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def message_type(cls) -> str:
        return "timeout"

    def serialize_payload(self) -> cbor2.Any:
        return None

    @classmethod
    def schema(cls) -> Schema:
        return Schema(None)

    @classmethod
    def _deserialize(cls, value: cbor2.Any) -> "Timeout":
        return Timeout()

    def description(self):
        return "timeout"


class GiveUp(TerminationMessage):
    def __init__(self, reason: str | None) -> None:
        super().__init__()

        self.reason = reason

    @classmethod
    def message_type(cls) -> str:
        return "give-up"

    def serialize_payload(self) -> cbor2.Any:
        return self.reason

    @classmethod
    def schema(cls) -> Schema:
        return Schema(schema.Or(str, None))

    @classmethod
    def _deserialize(cls, value: cbor2.Any) -> "GiveUp":
        return GiveUp(value)

    def description(self):
        return (
            f"session given up ({self.reason})"
            if self.reason
            else "session given up"
        )


class Custom(TerminationMessage):
    def __init__(self, reason: str | None) -> None:
        super().__init__()

        self.reason = reason

    @classmethod
    def message_type(cls) -> str:
        return "custom"

    def serialize_payload(self) -> cbor2.Any:
        return self.reason

    @classmethod
    def schema(cls) -> Schema:
        return Schema(str)

    @classmethod
    def _deserialize(cls, value: cbor2.Any) -> "Custom":
        return Custom(value)

    def description(self):
        return self.reason if self.reason else "unknown"


class CommunicationChannelClosed(Custom):
    def __init__(self):
        super().__init__("communication channel closed")


MESSAGE_TYPES: list[type[Message]] = [
    SessionSetupRequest,
    SessionSetupResponse,
    ProblemSetupRequest,
    ProblemSetupResponse,
    PerceptionRequest,
    PerceptionResponse,
    GetGroundedActionsRequest,
    GetGroundedActionsResponse,
    PerformGroundedActionRequest,
    PerformGroundedActionResponse,
    GoalReached,
    Error,
    SessionUnsupported,
    Timeout,
    GiveUp,
    Custom,
]


def deserialize_message(message: cbor2.Any) -> Message:
    Schema({"type": object, "payload": object}).validate(message)

    message_type_string = message["type"]
    payload = message["payload"]

    for candidate_message_type in MESSAGE_TYPES:
        if candidate_message_type.message_type() == message_type_string:
            return candidate_message_type.deserialize(payload)

    raise ValueError(f"unsupported message type {message_type_string}")
