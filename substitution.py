from __future__ import annotations
from typing import Mapping, Dict
from p2_ast import Formula, Variable, Negation, Implication
Substitution = Mapping[str, Formula]

def substitute(f: Formula, subs: Substitution) -> Formula:
    if isinstance(f, Variable):
        return subs.get(f.name, f)
    if isinstance(f, Negation):
        return Negation(substitute(f.value, subs))
    if isinstance(f, Implication):
        return Implication(substitute(f.left, subs), substitute(f.right, subs))
    raise ValueError(f"Unknown formula type: {f}")

