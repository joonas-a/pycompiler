from pytest import fail
from compiler.ast import BinaryOp, Literal, Identifier
from compiler.errors import EmptyInputError, UnexpectedTokenError
from compiler.parser import parse
from compiler.utils import Token, L, Location


def test_empty() -> None:
    try:
        parse([])
        fail("Parser did not fail with empty input")
    except EmptyInputError as e:
        assert str(e) == "Input string is empty"


def test_literal() -> None:
    assert parse([Token("1", "int_literal", L)]) == Literal(1)


def test_identifier() -> None:
    assert parse([Token("a", "identifier", L)]) == Identifier("a")


def test_literal_in_parentheses() -> None:
    assert parse(
        [
            Token("(", "punctuator", L),
            Token("1", "int_literal", L),
            Token(")", "punctuator", L),
        ]
    ) == Literal(1)


def test_fail_on_unexpected_token() -> None:
    loc = Location(1, (0, 1))
    try:
        parse([Token(")", "punctuator", loc)])
        fail("Parser did not catch standalone closing parenthesis")
    except UnexpectedTokenError as e:
        assert str(e) == f"{loc}: Unexpected closing parenthesis"


def test_fail_on_unexpected_token2() -> None:
    loc = Location(1, (0, 1))
    try:
        parse([Token("(", "punctuator", loc)])
        fail("Parser did not catch standalone opening parenthesis")
    except UnexpectedTokenError as e:
        assert str(e) == f"{loc}: Invalid token"


def test_binary_op() -> None:
    assert parse(
        [
            Token("1", "int_literal", L),
            Token("+", "operator", L),
            Token("2", "int_literal", L),
        ]
    ) == BinaryOp(Literal(1), "+", Literal(2))


def test_binary_op_nested() -> None:
    assert parse(
        [
            Token("1", "int_literal", L),
            Token("+", "operator", L),
            Token("2", "int_literal", L),
            Token("*", "operator", L),
            Token("3", "int_literal", L),
        ]
    ) == BinaryOp(Literal(1), "+", BinaryOp(Literal(2), "*", Literal(3)))


def test_binary_op_identifiers() -> None:
    assert parse(
        [
            Token("a", "identifier", L),
            Token("/", "operator", L),
            Token("3", "int_literal", L),
            Token("-", "operator", L),
            Token("b", "identifier", L),
        ]
    ) == BinaryOp(BinaryOp(Identifier("a"), "/", Literal(3)), "-", Identifier("b"))


def test_binary_op_parenthesised() -> None:
    assert parse(
        [
            Token("(", "punctuator", L),
            Token("1", "int_literal", L),
            Token("+", "operator", L),
            Token("2", "int_literal", L),
            Token(")", "punctuator", L),
            Token("*", "operator", L),
            Token("3", "int_literal", L),
        ]
    ) == BinaryOp(BinaryOp(Literal(1), "+", Literal(2)), "*", Literal(3))


def test_fail_missing_parenthesis_closure() -> None:
    loc = Location(10, (0, 1))
    try:
        parse(
            [
                Token("(", "punctuator", L),
                Token("1", "int_literal", L),
                Token("+", "operator", L),
                Token("2", "int_literal", L),
                Token("*", "operator", L),
                Token("3", "int_literal", loc),
            ]
        )
        fail("Parser did not catch the closing paranthesis missing")
    except UnexpectedTokenError as e:
        assert str(e) == f'{loc}: expected ")"'


def test_fail_garbage_at_the_end() -> None:
    loc = Location(0, (2, 3))
    try:
        parse(
            [
                Token("a", "identifier", L),
                Token("+", "operator", L),
                Token("b", "identifier", L),
                Token("c", "punctuator", loc),
            ]
        )
        fail("Parser did not fail with garbage at the end")
    except UnexpectedTokenError as e:
        assert str(e) == f"{loc}: Unexpected token"


def test_fail_too_many_parenthesis_closures() -> None:
    loc = Location(10, (10, 11))
    try:
        parse(
            [
                Token("1", "int_literal", L),
                Token("+", "operator", L),
                Token("(", "punctuator", L),
                Token("2", "int_literal", L),
                Token("-", "operator", L),
                Token("3", "int_literal", L),
                Token(")", "punctuator", L),
                Token(")", "punctuator", loc),
            ]
        )
        fail("Parser did not catch the duplicate closing parenthesis")
    except UnexpectedTokenError as e:
        assert str(e) == f"{loc}: Unexpected closing parenthesis"


def test_fail_closing_paranthesis_before_opening() -> None:
    loc = Location(3, (2, 3))
    try:
        parse(
            [
                Token("1", "int_literal", L),
                Token(")", "punctuator", loc),
                Token("+", "operator", L),
                Token("(", "punctuator", L),
                Token("2", "int_literal", L),
                Token("*", "operator", L),
                Token("3", "int_literal", L),
                Token(")", "punctuator", L),
            ]
        )
        fail("Did not catch closing parenthesis appearing before opening one")
    except UnexpectedTokenError as e:
        assert str(e) == f"{loc}: Unexpected closing parenthesis"


def test_fail_closing_paranthesis_after_operator() -> None:
    loc = Location(3, (2, 3))
    try:
        parse(
            [
                Token("1", "int_literal", L),
                Token("+", "operator", L),
                Token(")", "punctuator", loc),
                Token("(", "punctuator", L),
                Token("2", "int_literal", L),
                Token("*", "operator", L),
                Token("3", "int_literal", L),
                Token(")", "punctuator", L),
            ]
        )
        fail("Did not catch closing parenthesis appearing before opening one")
    except UnexpectedTokenError as e:
        assert str(e) == f"{loc}: Unexpected closing parenthesis"


def test_fail_missing_operator() -> None:
    loc = Location(0, (1, 2))
    try:
        parse(
            [
                Token("1", "int_literal", L),
                Token("2", "int_literal", loc),
            ]
        )
        fail("Parser did not catch the missing operator")
    except UnexpectedTokenError as e:
        assert str(e) == f"{loc}: Unexpected token"
