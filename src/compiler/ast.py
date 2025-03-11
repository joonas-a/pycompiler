from dataclasses import dataclass


@dataclass
class Expression:
    """Base class for AST nodes representing expressions."""


@dataclass
class Literal(Expression):
    value: int | bool


@dataclass
class Identifier(Expression):
    name: str


@dataclass
class IfThenElse(Expression):
    """AST node for an if-then-else statement like `if A then B else C`"""

    condition: Expression
    then_branch: Expression
    else_branch: Expression


@dataclass
class IfThen(Expression):
    """AST node for an if-then statement like `if A then B`"""

    condition: Expression
    then_branch: Expression


@dataclass
class BinaryOp(Expression):
    """AST node for a binary operation like `A + B`"""

    left: Expression
    op: str
    right: Expression
