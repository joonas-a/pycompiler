from pytest import fail

from compiler.ast import BinaryOp, Identifier, IfThenElse, Literal, IfThen
from compiler.errors import EmptyInputError, UnexpectedTokenError, MissingTokenError
from compiler.parser import parse
from compiler.utils import L, Location, Token
from compiler.tokenizer import tokenize


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


def test_basic_if_then() -> None:
    assert parse(tokenize("if true then 2")) == IfThen(
        condition=Identifier("true"),
        then_branch=Literal(2),
    )


def test_if_else() -> None:
    assert parse(tokenize("if true then 2 else 3")) == IfThenElse(
        condition=Identifier("true"),
        then_branch=Literal(2),
        else_branch=Literal(3),
    )


def test_if_then_else() -> None:
    assert parse(tokenize("if a + b then 2 * 3 else false")) == IfThenElse(
        condition=BinaryOp(Identifier("a"), "+", Identifier("b")),
        then_branch=BinaryOp(Literal(2), "*", Literal(3)),
        else_branch=Identifier("false"),
    )


def test_nested_if_else() -> None:
    assert parse(tokenize("if a then if b then 2 else 3 else 4")) == IfThenElse(
        condition=Identifier("a"),
        then_branch=IfThenElse(
            condition=Identifier("b"),
            then_branch=Literal(2),
            else_branch=Literal(3),
        ),
        else_branch=Literal(4),
    )


def test_big_nest_if_then() -> None:
    assert parse(
        tokenize("if a then if b then if c then 1 else 2 else 3 else 4")
    ) == IfThenElse(
        condition=Identifier("a"),
        then_branch=IfThenElse(
            condition=Identifier("b"),
            then_branch=IfThenElse(
                condition=Identifier("c"),
                then_branch=Literal(1),
                else_branch=Literal(2),
            ),
            else_branch=Literal(3),
        ),
        else_branch=Literal(4),
    )


def test_fail_if_else_no_then_statement() -> None:
    try:
        parse(tokenize("if a else 3"))
        fail("Parser did not catch the missing then statement")
    except MissingTokenError as e:
        assert str(e) == "Location(line=0, column=(10, 11)): Missing then branch"


def test_remainder_operator() -> None:
    assert parse(tokenize("1 % 2")) == BinaryOp(Literal(1), "%", Literal(2))
