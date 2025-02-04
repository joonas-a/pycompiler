from compiler.tokenizer import tokenize
from compiler.utils import L, Token, Location


def test_tokenizer_basics() -> None:
    assert tokenize("if  3\nwhile \n \n else") == [
        Token("if", "identifier", Location(0, (0, 2))),
        Token("3", "int_literal", L),
        Token("while", "identifier", Location(1, (0, 5))),
        Token("else", "identifier", Location(3, (1, 5))),
    ]
