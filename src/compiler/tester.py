from compiler.parser import parse
from compiler.utils import Token, L, Location

"""
Use this function for local testing
Run with ./main.sh in root
"""

x = [
    Token("if", "punctuator", Location(0, (0, 1))),
    Token("a", "int_literal", Location(0, (1, 2))),
    Token("then", "punctuator", Location(0, (2, 3))),
    Token("b", "punctuator", Location(0, (3, 4))),
    Token("+", "punctuator", Location(0, (4, 5))),
    Token("c", "punctuator", Location(0, (5, 6))),
]


def main() -> None:
    print(parse(x))
