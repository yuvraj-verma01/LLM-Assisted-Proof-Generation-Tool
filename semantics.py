from typing import Dict, Iterable, Set
from p2_ast import Formula, Variable, Negation, Implication

def vars_in(f: Formula) -> Set[str]:
    if isinstance(f, Variable):
        return {f.name}
    if isinstance(f, Negation):
        return vars_in(f.value)
    if isinstance(f, Implication):
        return vars_in(f.left) | vars_in(f.right)
    return set()

def eval_f(f: Formula, val: Dict[str, bool]) -> bool:
    if isinstance(f, Variable):
        return val[f.name]
    if isinstance(f, Negation):
        return not eval_f(f.value, val)
    if isinstance(f, Implication):
        return (not eval_f(f.left, val)) or eval_f(f.right, val)
    raise TypeError(f"Unknown node: {type(f)}")

def counterexample(premises: Iterable[Formula], goal: Formula):
    names = sorted(set().union(*(vars_in(p) for p in premises), vars_in(goal)))
    m = len(names)

    for mask in range(1 << m):
        val = {names[i]: bool((mask >> i) & 1) for i in range(m)}
        if all(eval_f(p, val) for p in premises) and not eval_f(goal, val):
            return val  
    return None
