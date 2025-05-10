import inspect
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, ClassVar, Self, TypedDict

from koda_validate import (
    AlwaysValid,
    IntValidator,
    ListValidator,
    Min,
    NoneValidator,
    OptionalValidator,
    StringValidator,
    TypedDictValidator,
    Validator,
)

from pddlsim._serde import (
    Serdeable,
    SerdeableEnum,
)
from pddlsim.ast import Domain, Object, Predicate, Problem
from pddlsim.parser import parse_domain_problem_pair
from pddlsim.simulation import GroundedAction


class Payload[T](Serdeable[T]):
    payloads: ClassVar[dict[str, type["Payload"]]] = {}

    def __init_subclass__(cls) -> None:
        if not inspect.isabstract(cls):
            cls.payloads[cls.type()] = cls

        super().__init_subclass__()

    @classmethod
    @abstractmethod
    def type(cls) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class SessionSetupRequest(Payload[int]):
    supported_rsp_version: int

    def serialize(self) -> int:
        return self.supported_rsp_version

    @classmethod
    def _validator(cls) -> Validator[int]:
        return IntValidator(Min(1))

    @classmethod
    def _create(cls, value: int) -> "SessionSetupRequest":
        return SessionSetupRequest(value)

    @classmethod
    def type(cls) -> str:
        return "session-setup-request"


@dataclass(frozen=True)
class EmptyPayload(Payload[None]):
    def serialize(self) -> None:
        return None

    @classmethod
    def _validator(cls) -> Validator[None]:
        return NoneValidator()

    @classmethod
    def _create(cls, _value: None) -> Self:
        return cls()


class SessionSetupResponse(EmptyPayload):
    @classmethod
    def type(cls) -> str:
        return "session-setup-response"


class ProblemSetupRequest(EmptyPayload):
    @classmethod
    def type(cls) -> str:
        return "problem-setup-request"


class SerializedProblemSetupResponse(TypedDict):
    domain: str
    problem: str


@dataclass(frozen=True)
class ProblemSetupResponse(Payload[SerializedProblemSetupResponse]):
    domain: Domain
    problem: Problem

    def serialize(self) -> SerializedProblemSetupResponse:
        return SerializedProblemSetupResponse(
            domain=repr(self.domain),
            problem=repr(self.problem),
        )

    @classmethod
    def _validator(cls) -> Validator[SerializedProblemSetupResponse]:
        return TypedDictValidator(SerializedProblemSetupResponse)

    @classmethod
    def _create(
        cls, value: SerializedProblemSetupResponse
    ) -> "ProblemSetupResponse":
        domain, problem = parse_domain_problem_pair(
            value["domain"], value["problem"]
        )

        return ProblemSetupResponse(domain, problem)

    @classmethod
    def type(cls) -> str:
        return "problem-setup-response"


class PerceptionRequest(EmptyPayload):
    @classmethod
    def type(cls) -> str:
        return "perception-request"


@dataclass(frozen=True)
class PerceptionResponse(Payload[list[Any]]):
    true_predicates: list[Predicate[Object]]

    def serialize(self) -> list[Any]:
        return [predicate.serialize() for predicate in self.true_predicates]

    @classmethod
    def _validator(cls) -> Validator[list[Any]]:
        return ListValidator(AlwaysValid())

    @classmethod
    def _create(cls, value: list[Any]) -> "PerceptionResponse":
        return PerceptionResponse(
            [Predicate[Object].deserialize(item) for item in value]
        )

    @classmethod
    def type(cls) -> str:
        return "perception-response"


class GoalTrackingRequest(EmptyPayload):
    @classmethod
    def type(cls) -> str:
        return "goal-tracking-request"


class SerializedGoalTrackingResponse(TypedDict):
    reached: list[int]
    unreached: list[int]


@dataclass(frozen=True)
class GoalTrackingResponse(Payload[SerializedGoalTrackingResponse]):
    reached_goal_indices: list[int]
    unreached_goal_indices: list[int]

    def serialize(self) -> SerializedGoalTrackingResponse:
        return SerializedGoalTrackingResponse(
            reached=self.reached_goal_indices,
            unreached=self.unreached_goal_indices,
        )

    @classmethod
    def _validator(cls) -> Validator[SerializedGoalTrackingResponse]:
        return TypedDictValidator(SerializedGoalTrackingResponse)

    @classmethod
    def _create(
        cls, value: SerializedGoalTrackingResponse
    ) -> "GoalTrackingResponse":
        return GoalTrackingResponse(value["reached"], value["unreached"])

    @classmethod
    def type(cls) -> str:
        return "goal-tracking-response"


class GetGroundedActionsRequest(EmptyPayload):
    @classmethod
    def type(cls) -> str:
        return "get-grounded-actions-request"


@dataclass(frozen=True)
class GetGroundedActionsResponse(Payload[list[Any]]):
    grounded_actions: list[GroundedAction]

    def serialize(self) -> list[Any]:
        return [
            grounded_action.serialize()
            for grounded_action in self.grounded_actions
        ]

    @classmethod
    def _validator(cls) -> Validator[list[Any]]:
        return ListValidator(AlwaysValid())

    @classmethod
    def _create(cls, value: list[Any]) -> "GetGroundedActionsResponse":
        return GetGroundedActionsResponse(
            [GroundedAction.deserialize(item) for item in value]
        )

    @classmethod
    def type(cls) -> str:
        return "get-grounded-actions-response"


@dataclass(frozen=True)
class PerformGroundedActionRequest(Payload[Any]):
    grounded_action: GroundedAction

    def serialize(self) -> Any:
        return self.grounded_action.serialize()

    @classmethod
    def _validator(cls) -> Validator[Any]:
        return AlwaysValid()

    @classmethod
    def _create(cls, value: Any) -> "PerformGroundedActionRequest":
        return PerformGroundedActionRequest(GroundedAction.deserialize(value))

    @classmethod
    def type(cls) -> str:
        return "perform-grounded-action-request"


class PerformGroundedActionResponse(EmptyPayload):
    @classmethod
    def type(cls) -> str:
        return "perform-grounded-action-response"


class TerminationPayload[T](Payload[T]):
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError


class GoalsReached(EmptyPayload, TerminationPayload):
    @classmethod
    def type(cls) -> str:
        return "goals-reached"

    def description(self) -> str:
        return "goals reached"


class TerminationSource(SerdeableEnum):
    INTERNAL = "internal"
    EXTERNAL = "external"


class ErrorReason(TypedDict):
    source: Any
    reason: str | None


@dataclass(frozen=True)
class Error(TerminationPayload[ErrorReason]):
    source: TerminationSource
    reason: str | None

    @classmethod
    def from_type_mismatch(
        cls,
        expected_payload_type: type[Payload],
        received_payload_type: type[Payload],
    ) -> "Error":
        return Error(
            TerminationSource.EXTERNAL,
            f"expected {expected_payload_type.type()}, got {received_payload_type.type()}",  # noqa: E501
        )

    def serialize(self) -> ErrorReason:
        return ErrorReason(source=self.source.serialize(), reason=self.reason)

    @classmethod
    def _validator(cls) -> Validator[ErrorReason]:
        return TypedDictValidator(ErrorReason)

    @classmethod
    def _create(cls, value: ErrorReason) -> "Error":
        return Error(
            TerminationSource.deserialize(value["source"]), value["reason"]
        )

    @classmethod
    def type(cls) -> str:
        return "error"

    def description(self) -> str:
        return (
            f"{self.reason} ({self.source} error)"
            if self.reason
            else f"{self.source} error"
        )


class SessionUnsupported(EmptyPayload, TerminationPayload):
    @classmethod
    def type(cls) -> str:
        return "session-unsupported"

    def description(self) -> str:
        return "session unsupported"


class Timeout(EmptyPayload, TerminationPayload):
    @classmethod
    def type(cls) -> str:
        return "timeout"

    def description(self) -> str:
        return "timeout"


@dataclass(frozen=True)
class GiveUp(TerminationPayload[str | None]):
    reason: str | None

    def serialize(self) -> str | None:
        return self.reason

    @classmethod
    def _validator(cls) -> Validator[str | None]:
        return OptionalValidator(StringValidator())

    @classmethod
    def _create(cls, value: str | None) -> "GiveUp":
        return GiveUp(value)

    @classmethod
    def type(cls) -> str:
        return "give-up"

    def description(self) -> str:
        return (
            f"session given up ({self.reason})"
            if self.reason
            else "session given up"
        )


@dataclass(frozen=True)
class Custom(TerminationPayload[str | None]):
    reason: str | None

    @classmethod
    def from_communication_channel_closed(cls) -> "Custom":
        return Custom("communication channel closed")

    def serialize(self) -> str | None:
        return self.reason

    @classmethod
    def _validator(cls) -> Validator[str | None]:
        return OptionalValidator(StringValidator())

    @classmethod
    def _create(cls, value: str | None) -> "Custom":
        return Custom(value)

    @classmethod
    def type(cls) -> str:
        return "custom"

    def description(self) -> str:
        return self.reason if self.reason else "unknown"


class SerializedMessage(TypedDict):
    type: str
    payload: Any


@dataclass(frozen=True)
class Message(Serdeable[SerializedMessage]):
    payload: Payload

    def serialize(self) -> SerializedMessage:
        return SerializedMessage(
            type=self.payload.type(), payload=self.payload.serialize()
        )

    @classmethod
    def _validator(cls) -> Validator[SerializedMessage]:
        return TypedDictValidator(SerializedMessage)

    @classmethod
    def _create(cls, value: SerializedMessage) -> "Message":
        return Message(
            Payload.payloads[value["type"]].deserialize(value["payload"])
        )
