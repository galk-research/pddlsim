from dataclasses import dataclass
from enum import StrEnum
from typing import Any, NewType

import cbor2
from apischema import deserialize, discriminator, schema, serialize, type_name

from pddlsim.ast import Object, Predicate
from pddlsim.simulation import GroundedAction


@dataclass
@discriminator("type")
class Payload:
    payload: Any

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    def serialize(self) -> cbor2.Any:
        return serialize(Payload, self)


@dataclass(frozen=True)
class RSPName:
    name: str

    def __call__[P: Payload](self, type: type[P]) -> type[P]:
        type.name = lambda: self.name  # type: ignore[method-assign]

        return type_name(self.name)(type)


def rsp_name(name: str) -> RSPName:
    return RSPName(name)


RSPVersion = NewType("RSPVersion", int)
schema(min=1)(RSPVersion)


@dataclass
@rsp_name("session-setup-request")
class SessionSetupRequest(Payload):
    payload: RSPVersion


@dataclass
@rsp_name("session-setup-response")
class SessionSetupResponse(Payload):
    payload: None = None


@dataclass
@rsp_name("problem-setup-request")
class ProblemSetupRequest(Payload):
    payload: None = None


@dataclass
class DomainProblemPair:
    domain: str
    problem: str


@dataclass
@rsp_name("problem-setup-response")
class ProblemSetupResponse(Payload):
    payload: DomainProblemPair


@dataclass
@rsp_name("perception-request")
class PerceptionRequest(Payload):
    payload: None = None


@dataclass
@rsp_name("perception-response")
class PerceptionResponse(Payload):
    payload: list[Predicate[Object]]


@dataclass
@rsp_name("get-grounded-actions-request")
class GetGroundedActionsRequest(Payload):
    payload: None = None


@dataclass
@rsp_name("get-grounded-actions-response")
class GetGroundedActionsResponse(Payload):
    payload: list[GroundedAction]


@dataclass
@rsp_name("perform-grounded-action-request")
class PerformGroundedActionRequest(Payload):
    payload: GroundedAction


@dataclass
@rsp_name("perform-grounded-action-response")
class PerformGroundedActionResponse(Payload):
    payload: None = None


@dataclass
@rsp_name("goal-reached")
class GoalReached(Payload):
    payload: None = None

    def __str__(self) -> str:
        return "goal reached"


class TerminationSource(StrEnum):
    INTERNAL = "internal"
    EXTERNAL = "external"


ReasonString = NewType("ReasonString", str)
schema(min_len=1)(ReasonString)


@dataclass
class ErrorReason:
    source: TerminationSource
    reason: ReasonString | None


@dataclass
@rsp_name("error")
class Error(Payload):
    payload: ErrorReason

    def __str__(self) -> str:
        return (
            f"{self.payload.reason} ({self.payload.source} error)"
            if self.payload.reason
            else f"{self.payload.source} error"
        )

    @classmethod
    def from_type_mismatch(
        cls,
        expected_message_type: type[Payload],
        received_message_type: type[Payload],
    ) -> "Error":
        return Error(
            ErrorReason(
                source=TerminationSource.EXTERNAL,
                reason=ReasonString(
                    f"expected {expected_message_type.name()}, "
                    f"got {received_message_type.name()}"
                ),
            )
        )


@dataclass
@rsp_name("session-unsupported")
class SessionUnsupported(Payload):
    payload: None = None

    def __str__(self) -> str:
        return "session unsupported"


@dataclass
@rsp_name("timeout")
class Timeout(Payload):
    payload: None = None

    def __str__(self) -> str:
        return "timeout"


@dataclass
@rsp_name("give-up")
class GiveUp(Payload):
    payload: ReasonString | None

    def __str__(self) -> str:
        return (
            f"session given up ({self.payload})"
            if self.payload
            else "session given up"
        )


@dataclass
@rsp_name("custom")
class Custom(Payload):
    payload: ReasonString | None

    def __str__(self) -> str:
        return self.payload if self.payload else "unknown"

    @classmethod
    def from_communication_channel_closed(cls) -> "Custom":
        return Custom(ReasonString("communication channel closed"))


TerminationPayload = (
    GoalReached | Error | SessionUnsupported | Timeout | GiveUp | Custom
)


def deserialize_message(message: cbor2.Any) -> Payload:
    return deserialize(Payload, message)
