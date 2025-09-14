from __future__ import annotations
from dataclasses import dataclass

class Formula:
    pass

@dataclass(frozen=True)
class Variable(Formula):
    name: str
    def __str__(self) -> str:
        return self.name
    
def parenthesis(f: Formula, need: bool = False) -> str:
    if isinstance(f, Variable):
        return str(f)
    if need or isinstance(f, Implication):
        return f"({f})"
    return str(f)

@dataclass
class Negation(Formula):
    value: Formula
    def __str__(self) -> str:
        return f"~{parenthesis(self.value, need = True)}"

@dataclass
class Implication(Formula):
    left: Formula
    right: Formula
    def __str__(self) -> str:
        return f"({parenthesis(self.left)} -> {parenthesis(self.right)})"

