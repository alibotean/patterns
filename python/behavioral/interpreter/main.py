"""
Interpreter Pattern

Intent: Given a language, define a representation for its grammar along with an
interpreter that uses the representation to interpret sentences in the language.

Use when: You have a simple, well-defined grammar that is evaluated repeatedly.

Example: a tiny boolean rule engine that evaluates expressions like
  "age >= 18 AND country == 'US'"
Each node in the AST is an Expression that knows how to evaluate itself.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


# ── Context ────────────────────────────────────────────────────────────────────

Context = dict[str, object]  # e.g. {"age": 25, "country": "US"}


# ── Abstract Expression ────────────────────────────────────────────────────────

class Expression(ABC):
    @abstractmethod
    def interpret(self, ctx: Context) -> bool: ...


# ── Terminal Expressions ───────────────────────────────────────────────────────

class VariableComparison(Expression):
    """
    Compares a named variable from the context against a literal value.
    Supports operators: ==, !=, <, <=, >, >=
    """
    _OPS = {
        "==": lambda a, b: a == b,
        "!=": lambda a, b: a != b,
        "<":  lambda a, b: a <  b,
        "<=": lambda a, b: a <= b,
        ">":  lambda a, b: a >  b,
        ">=": lambda a, b: a >= b,
    }

    def __init__(self, variable: str, operator: str, value: object) -> None:
        if operator not in self._OPS:
            raise ValueError(f"Unknown operator: {operator}")
        self._variable = variable
        self._operator = operator
        self._value    = value

    def interpret(self, ctx: Context) -> bool:
        if self._variable not in ctx:
            raise KeyError(f"Variable '{self._variable}' not in context")
        return self._OPS[self._operator](ctx[self._variable], self._value)

    def __str__(self) -> str:
        return f"{self._variable} {self._operator} {self._value!r}"


# ── Non-Terminal Expressions ───────────────────────────────────────────────────

class AndExpression(Expression):
    """Both left AND right must be true."""
    def __init__(self, left: Expression, right: Expression) -> None:
        self._left  = left
        self._right = right

    def interpret(self, ctx: Context) -> bool:
        # Short-circuit: if left is False, right is never evaluated
        return self._left.interpret(ctx) and self._right.interpret(ctx)

    def __str__(self) -> str:
        return f"({self._left} AND {self._right})"


class OrExpression(Expression):
    """Either left OR right must be true."""
    def __init__(self, left: Expression, right: Expression) -> None:
        self._left  = left
        self._right = right

    def interpret(self, ctx: Context) -> bool:
        return self._left.interpret(ctx) or self._right.interpret(ctx)

    def __str__(self) -> str:
        return f"({self._left} OR {self._right})"


class NotExpression(Expression):
    """Negates an expression."""
    def __init__(self, operand: Expression) -> None:
        self._operand = operand

    def interpret(self, ctx: Context) -> bool:
        return not self._operand.interpret(ctx)

    def __str__(self) -> str:
        return f"NOT({self._operand})"


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Build the AST for:
    #   (age >= 18 AND country == 'US') OR (age >= 21 AND country == 'CA')
    us_adult = AndExpression(
        VariableComparison("age",     ">=", 18),
        VariableComparison("country", "==", "US"),
    )
    ca_adult = AndExpression(
        VariableComparison("age",     ">=", 21),
        VariableComparison("country", "==", "CA"),
    )
    rule = OrExpression(us_adult, ca_adult)

    print(f"Rule: {rule}\n")

    test_cases: list[Context] = [
        {"age": 25, "country": "US"},  # True  — US adult
        {"age": 16, "country": "US"},  # False — US but too young
        {"age": 22, "country": "CA"},  # True  — CA adult
        {"age": 19, "country": "CA"},  # False — CA but under 21
        {"age": 30, "country": "UK"},  # False — neither condition
    ]

    for ctx in test_cases:
        result = rule.interpret(ctx)
        print(f"  age={ctx['age']:>2}, country={ctx['country']}  →  {result}")
