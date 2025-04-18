from collections.abc import Generator, MutableMapping
from dataclasses import dataclass
from enum import StrEnum


class IDKind(StrEnum):
    VARIABLE = "variable"
    OBJECT_NAME = "object"
    PREDICATE = "predicate"
    TYPE_NAME = "type"
    RULE = "rule"
    TEMPORARY = "T"


@dataclass(frozen=True, eq=True)
class ID:
    value: int
    kind: IDKind

    def __str__(self) -> str:
        return f"{self.kind}{self.value}"

    @classmethod
    def from_str(cls, string: str) -> "ID":
        for kind in IDKind:
            if string.startswith(kind.value):
                return ID(int(string[len(kind.value) :]), kind)

        raise ValueError("id prefix not recognized")


class IDAllocator[T]:
    def __init__(self, kind: IDKind) -> None:
        self._previous_id = -1
        self._kind = kind
        self._ids: MutableMapping[T, ID] = {}
        self._values: MutableMapping[ID, T] = {}

    def next_id(self) -> ID:
        self._previous_id += 1

        return ID(self._previous_id, self._kind)

    def __iter__(self) -> Generator[tuple[T, ID]]:
        yield from self._ids.items()

    def get_id_or_insert(self, value: T) -> ID:
        if value in self._ids:
            return self._ids[value]
        else:
            id = self.next_id()

            self._ids[value] = id
            self._values[id] = value

            return id

    def get_value(self, id: ID) -> T:
        return self._values[id]
