from compiler.tokenizer import tokenize
from compiler.utils import L, Token, Location


def test_tokenizer_basics() -> None:
    assert tokenize("if  3\nwhile \n \n else") == [
        Token("if", "identifier", Location(0, (0, 2))),
        Token("3", "int_literal", L),
        Token("while", "identifier", Location(1, (0, 5))),
        Token("else", "identifier", Location(3, (1, 5))),
    ]


def test_tokenizer_operators() -> None:
    assert tokenize("1+2-/<>\n<=>=!====*") == [
        Token("1", "int_literal", Location(0, (0, 1))),
        Token("+", "operator", L),
        Token("2", "int_literal", L),
        Token("-", "operator", L),
        Token("/", "operator", L),
        Token("<", "operator", L),
        Token(">", "operator", L),
        Token("<=", "operator", Location(1, (0, 2))),
        Token(">=", "operator", L),
        Token("!=", "operator", L),
        Token("==", "operator", L),
        Token("=", "operator", L),
        Token("*", "operator", L),
    ]


def test_tokenizer_punctuation() -> None:
    assert tokenize("()), {{}}, ; ") == [
        Token("(", "punctuation", L),
        Token(")", "punctuation", L),
        Token(")", "punctuation", L),
        Token(",", "punctuation", L),
        Token("{", "punctuation", L),
        Token("{", "punctuation", L),
        Token("}", "punctuation", L),
        Token("}", "punctuation", L),
        Token(",", "punctuation", L),
        Token(";", "punctuation", L),
    ]


def test_one_line_comment() -> None:
    assert tokenize("s# 404\n2") == [
        Token("s", "identifier", L),
        Token("2", "int_literal", L),
    ]


def test_multi_line_comment() -> None:
    assert tokenize("a/*a\nb\n#c\n//\nd*/e") == [
        Token("a", "identifier", L),
        Token("e", "identifier", L),
    ]
