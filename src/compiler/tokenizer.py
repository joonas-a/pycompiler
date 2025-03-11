import re
from typing import List, Tuple
from .utils import Token, Location, Kind


OPERATORS = ["+", "-", "*", "/", "=", "==", "!=", "<=", ">=", "<", ">"]
PUNCTUATORS = ["(", ")", "{", "}", ",", ";"]

CONDITIONALS = ["if", "then", "else"]

COMMENTS = ["//", "#"]
COMMENT_START = ["/*"]
COMMENT_END = ["*/"]


## TODO: add other "kinds"
def parseKind(value: str) -> Kind:
    if value.isnumeric():
        return "int_literal"
    elif value in OPERATORS:
        return "operator"
    elif value in PUNCTUATORS:
        return "punctuator"
    elif value in COMMENTS:
        return "comment"
    elif value in COMMENT_START:
        return "comment_start"
    elif value in COMMENT_END:
        return "comment_end"
    elif value in CONDITIONALS:
        return "conditional"
    else:
        return "identifier"


def parseLoc(line: int, span: Tuple[int, int]) -> Location:
    return Location(line, (span[0], span[1]))


r = re.compile(
    r"#|\*\/|\/\*|\/\/|==|!=|<=|>=|>|<|\+|\-|\*|\/|=|\(|\)|\{|\}|,|;|[a-zA-Z_]+[a-zA-Z0-9_]*|[0-9]+"
)


def tokenize(source_code: str) -> list[Token]:
    tokens: List[Token] = []

    multi_comment = False

    for line, text in enumerate(source_code.splitlines()):
        single_comment = False
        ts = r.finditer(text)
        for t in ts:
            token = Token(
                text=t.group(),
                kind=parseKind(t.group()),
                loc=parseLoc(line, t.span()),
            )
            if token.kind == "comment":
                single_comment = True
            if token.kind == "comment_start":
                multi_comment = True

            if not multi_comment and not single_comment:
                tokens.append(token)

            if token.kind == "comment_end":
                multi_comment = False

    return tokens
