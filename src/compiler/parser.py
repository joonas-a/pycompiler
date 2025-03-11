import compiler.ast as ast
from compiler.errors import EmptyInputError, UnexpectedTokenError
from compiler.utils import Token

"""
TODO:: todo

"""


def raise_error(token: Token) -> None:
    if token.kind == "punctuator":
        if token.text == ")":
            raise UnexpectedTokenError(f"{token.loc}: Unexpected closing parenthesis")
    raise UnexpectedTokenError(f"{token.loc}: Unexpected token")


def parse(tokens: list[Token]) -> ast.Expression:
    pos = 0
    open_parantheses = 0

    def check_open_parantheses() -> bool:
        print("num of open parans", open_parantheses)
        return open_parantheses > 0

    def peek() -> Token:
        print("peek", pos)
        if pos < len(tokens):
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
        print("consumed", pos, token.text)
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
        if peek().kind != "int_literal":
            raise UnexpectedTokenError(f"{peek().loc}: expected an integer literal")
        token = consume()
        return ast.Literal(int(token.text))

    def parse_identifier() -> ast.Identifier:
        if peek().kind != "identifier":
            raise UnexpectedTokenError(f"{peek().loc}: expected an identifier")
        token = consume()
        return ast.Identifier(token.text)

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
            case "punctuator":
                print("Punctuator", pos)
                if peek().text == "(":
                    return parse_parenthesized()
                if peek().text == ")":
                    print("SOS SOS SOS")
                    raise UnexpectedTokenError(
                        f"{peek().loc}: Unexpected closing parenthesis"
                    )
                raise Exception(f"{peek().loc}: Unimplemented punctuator")
            case "int_literal":
                print("Int literal", pos)
                return parse_int_literal()
            case "identifier":
                print("Identifier", pos)
                return parse_identifier()

            case _:
                raise UnexpectedTokenError(f"{peek().loc}: Invalid token")

    def parse_term() -> ast.Expression:
        left = parse_factor()
        while peek().text in ["*", "/"]:
            operator_token = consume()
            operator = operator_token.text
            right = parse_factor()
            left = ast.BinaryOp(left, operator, right)
        if peek().kind not in ["operator", "end"] and not check_open_parantheses():
            print(" going to raise error")
            raise_error(peek())
        return left

    def parse_expression() -> ast.Expression:
        left = parse_term()
        while peek().text in ["+", "-"]:
            operator_token = consume()
            operator = operator_token.text
            right = parse_term()
            left = ast.BinaryOp(left, operator, right)
        if peek().kind not in ["end"] and not check_open_parantheses():
            raise_error(peek())
        return left

    return parse_expression()
