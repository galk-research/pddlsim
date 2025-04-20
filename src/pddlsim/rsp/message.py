from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Annotated, Any

import cbor2
from pydantic import (
    Field,
    PositiveInt,
    TypeAdapter,
    field_validator,
)
from pydantic.dataclasses import dataclass as pydantic_dataclass

from pddlsim.parser import SerializablePredicate
from pddlsim.simulation import SerializableGroundedAction


@pydantic_dataclass
class Message(ABC):
    payload: Any
    type: str

    @field_validator("type", mode="after")
    @classmethod
    def matches_type(cls, value: str) -> str:
        if value != cls.type:
            raise ValueError(
                f"expected message type '{cls.type}', got '{value}'"
            )

        return value


@pydantic_dataclass
class SessionSetupRequest(Message):
    payload: PositiveInt
    type: str = "session-setup-request"


@pydantic_dataclass
class SessionSetupResponse(Message):
    payload: None = None
    type: str = "session-setup-response"


@pydantic_dataclass
class ProblemSetupRequest(Message):
    payload: None = None
    type: str = "problem-setup-request"


@pydantic_dataclass
class DomainProblemPair:
    domain: str
    problem: str


@pydantic_dataclass
class ProblemSetupResponse(Message):
    payload: DomainProblemPair
    type: str = "problem-setup-response"


@pydantic_dataclass
class PerceptionRequest(Message):
    payload: None = None
    type: str = "perception-request"


@pydantic_dataclass
class PerceptionResponse(Message):
    payload: list[SerializablePredicate]
    type: str = "perception-response"


@pydantic_dataclass
class GetGroundedActionsRequest(Message):
    payload: None = None
    type: str = "get-grounded-actions-request"


@pydantic_dataclass
class GetGroundedActionsResponse(Message):
    payload: list[SerializableGroundedAction]
    type: str = "get-grounded-actions-response"


@pydantic_dataclass
class PerformGroundedActionRequest(Message):
    payload: SerializableGroundedAction
    type: str = "perform-grounded-action-request"


@pydantic_dataclass
class PerformGroundedActionResponse(Message):
    payload: None = None
    type: str = "perform-grounded-action-response"


@pydantic_dataclass
class TerminationMessage(Message):
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError


@pydantic_dataclass
class GoalReached(TerminationMessage):
    payload: None = None
    type: str = "goal-reached"

    def description(self) -> str:
        return "goal reached"


class TerminationSource(StrEnum):
    INTERNAL = "internal"
    EXTERNAL = "external"


@pydantic_dataclass
class ErrorReason:
    source: TerminationSource
    reason: str | None


@pydantic_dataclass
class Error(TerminationMessage):
    payload: ErrorReason
    type: str = "error"

    def description(self) -> str:
        return (
            f"{self.payload.reason} ({self.payload.source} error)"
            if self.payload.reason
            else f"{self.payload.source} error"
        )


@pydantic_dataclass
class MessageTypeMismatchError(Error):
    def __init__(
        self,
        expected_message_type: type[Message],
        received_message_type: type[Message],
    ) -> None:
        super().__init__(
            ErrorReason(
                source=TerminationSource.EXTERNAL,
                reason=f"expected {expected_message_type.type}, "
                f"got {received_message_type.type}",
            )
        )


@pydantic_dataclass
class SessionUnsupported(TerminationMessage):
    payload: None = None
    type: str = "session-unsupported"

    def description(self) -> str:
        return "session unsupported"


@pydantic_dataclass
class Timeout(TerminationMessage):
    payload: None = None
    type: str = "timeout"

    def description(self) -> str:
        return "timeout"


@pydantic_dataclass
class GiveUp(TerminationMessage):
    payload: str | None
    type: str = "give-up"

    def description(self):
        return (
            f"session given up ({self.payload})"
            if self.payload
            else "session given up"
        )


@pydantic_dataclass
class Custom(TerminationMessage):
    payload: str | None
    type: str = "custom"

    def description(self) -> str:
        return self.payload if self.payload else "unknown"


class CommunicationChannelClosed(Custom):
    def __init__(self) -> None:
        super().__init__("communication channel closed")


ValidMessage = (
    SessionSetupRequest
    | SessionSetupResponse
    | ProblemSetupRequest
    | ProblemSetupResponse
    | PerceptionRequest
    | PerceptionResponse
    | GetGroundedActionsRequest
    | GetGroundedActionsResponse
    | PerformGroundedActionRequest
    | PerformGroundedActionResponse
    | GoalReached
    | Error
    | SessionUnsupported
    | Timeout
    | GiveUp
    | Custom
)


_ADAPTER = TypeAdapter[ValidMessage](
    Annotated[
        ValidMessage,
        Field(union_mode="left_to_right"),
    ]
)


def deserialize_message(message: cbor2.Any) -> Message:
    return _ADAPTER.validate_python(message, strict=True)
