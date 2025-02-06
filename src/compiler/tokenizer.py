import re
from typing import List, Tuple
from .utils import Token, Location, Kind


OPERATORS = ["+", "-", "*", "/", "=", "==", "!=", "<=", ">=", "<", ">"]
PUNCTUATORS = ["(", ")", "{", "}", ",", ";"]


## TODO: add other "kinds"
def parseKind(value: str) -> Kind:
    if value.isnumeric():
        return "int_literal"
    elif value in OPERATORS:
        return "operator"
    elif value in PUNCTUATORS:
        return "punctuation"
    else:
        return "identifier"


def parseLoc(line: int, span: Tuple[int, int]) -> Location:
    return Location(line, (span[0], span[1]))


r = re.compile(
    r"==|!=|<=|>=|>|<|\+|\-|\*|\/|=|\(|\)|\{|\}|,|;|[a-zA-Z_]+[a-zA-Z0-9_]*|[0-9]+"
)


def tokenize(source_code: str) -> list[Token]:
    tokens: List[Token] = []

    for line, text in enumerate(source_code.splitlines()):
        ts = r.finditer(text)
        tokens.extend(
            map(
                lambda t: Token(
                    text=t.group(),
                    kind=parseKind(t.group()),
                    loc=parseLoc(line, t.span()),
                ),
                ts,
            )
        )

    return tokens
