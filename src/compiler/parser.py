import compiler.ast as ast
from compiler.errors import EmptyInputError, UnexpectedTokenError, MissingTokenError
from compiler.utils import Token

"""
TODO:: todo

"""

RIGHT_ASSOCIATIVE_OPS = [
    ["="],
]

LEFT_ACCOSIATIVE_OPS = [
    ["or"],
    ["and"],
    ["==", "!="],
    ["<", "<=", ">", ">="],
    ["+", "-"],
    ["*", "/", "%"],
]
MAX_PRECEDENCE = len(LEFT_ACCOSIATIVE_OPS) - 1


def raise_error(token: Token) -> None:
    if token.kind == "punctuator":
        if token.text == ")":
            raise UnexpectedTokenError(f"{token.loc}: Unexpected closing parenthesis")
    if token.kind == "conditional":
        if token.text == "if":
            raise UnexpectedTokenError(f"{token.loc}: Unexpected if")
        if token.text == "then":
            raise UnexpectedTokenError(f"{token.loc}: Unexpected then")
        if token.text == "else":
            raise UnexpectedTokenError(f"{token.loc}: Unexpected else")
    raise UnexpectedTokenError(f"{token.loc}: Unexpected token")


def parse(tokens: list[Token]) -> ast.Expression:
    pos = 0
    open_parantheses = 0
    open_ifs = 0

    def peek() -> Token:
        if pos < len(tokens):
            print("peeking at:", pos, tokens[pos].text)
            return tokens[pos]
        elif pos == 0:
            raise EmptyInputError("Input string is empty")
        else:
            return Token(
                text="",
                kind="end",
                loc=tokens[-1].loc,
            )

    def consume(expected: str | list[str] | None = None) -> Token:
        nonlocal pos
        token = peek()
        print("consumed at:", pos, token.text)
        if isinstance(expected, str) and token.text != expected:
            raise UnexpectedTokenError(f'{token.loc}: expected "{expected}"')
        if isinstance(expected, list) and token.text not in expected:
            comma_separated = ", ".join([f'"{e}"' for e in expected])
            raise UnexpectedTokenError(
                f"{token.loc}: expected one of: {comma_separated}"
            )
        pos += 1
        return token

    def parse_int_literal() -> ast.Literal:
        token = consume()
        if token.kind != "int_literal":
            raise UnexpectedTokenError(f"{token.loc}: expected an integer literal")
        return ast.Literal(int(token.text))

    def parse_identifier() -> ast.Identifier:
        token = consume()
        if token.kind != "identifier":
            raise UnexpectedTokenError(f"{token.loc}: expected an identifier")
        return ast.Identifier(token.text)

    def parse_conditional() -> ast.Expression:
        nonlocal open_ifs

        then_branch = None
        else_branch = None

        if peek().text == "if":
            consume("if")
            open_ifs += 1
            condition = parse_expression()

        if peek().text == "then":
            consume("then")
            then_branch = parse_expression()
        if peek().text == "else":
            consume("else")
            else_branch = parse_expression()

        open_ifs -= 1

        if then_branch is None:
            raise MissingTokenError(f"{peek().loc}: Missing then branch")

        elif else_branch is None:
            return ast.IfThen(condition, then_branch)
        else:
            return ast.IfThenElse(condition, then_branch, else_branch)

    def parse_parenthesized() -> ast.Expression:
        nonlocal open_parantheses
        consume("(")
        open_parantheses += 1
        expr = parse_expression()
        consume(")")
        open_parantheses -= 1
        return expr

    def parse_factor() -> ast.Expression:
        match peek().kind:
            case "conditional":
                print("CONDITIONAL")
                return parse_conditional()
            case "punctuator":
                print("PUNCTUATOR", pos)
                if peek().text == "(":
                    return parse_parenthesized()
                if peek().text == ")":
                    print("ERROR")
                    raise UnexpectedTokenError(
                        f"{peek().loc}: Unexpected closing parenthesis"
                    )
                raise Exception(f"{peek().loc}: Unimplemented punctuator")
            case "int_literal":
                print("INT LITERAL")
                return parse_int_literal()
            case "identifier":
                print("IDENTIFIER")
                return parse_identifier()

            case _:
                raise UnexpectedTokenError(f"{peek().loc}: Invalid token")

    def parse_term(level: int) -> ast.Expression:
        if level is MAX_PRECEDENCE:
            left = parse_factor()
        else:
            left = parse_term(level + 1)

        while peek().text in LEFT_ACCOSIATIVE_OPS[level]:
            print("curr ops: ", LEFT_ACCOSIATIVE_OPS[level])
            operator_token = consume()
            operator = operator_token.text

            print("RIGHT")
            if level is MAX_PRECEDENCE:
                right = parse_factor()
            else:
                right = parse_term(level + 1)

            left = ast.BinaryOp(left, operator, right)

        if (
            peek().kind not in ["operator", "end"]
            and not open_parantheses
            and not open_ifs
        ):
            print("Raising error at parse_term()")
            raise_error(peek())

        return left

    def parse_expression() -> ast.Expression:
        result = parse_term(level=0)

        if peek().kind not in ["end"] and not open_parantheses and not open_ifs:
            print("Raising error at parse_expression()")
            raise_error(peek())
        return result

    return parse_expression()
