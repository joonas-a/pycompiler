from dataclasses import dataclass
from typing import Literal, Tuple

Kind = Literal[
    "comment",
    "comment_start",
    "comment_end",
    "conditional",
    "end",
    "int_literal",
    "identifier",
    "operator",
    "other",
    "punctuator",
]


@dataclass
class Location:
    line: int
    column: Tuple[int, int]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Location):
            return NotImplemented
        if other.line == -1 and other.column == (-1, -1):
            return True
        if self.line == other.line and self.column == other.column:
            return True
        return False


@dataclass
class Token:
    text: str
    kind: Kind
    loc: Location


L = Location(-1, (-1, -1))
