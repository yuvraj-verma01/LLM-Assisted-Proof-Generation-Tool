from typing import Dict, Optional, Tuple
from p2_ast import Formula, Variable, Negation, Implication
from axioms import Meta, axioms as AXIOMS

Env = Dict[str, Formula]

def match(pattern: Formula, instance: Formula, env: Env ) -> bool:
    if isinstance(pattern, Meta):
        bound = env.get(pattern.name)
        if bound is None:
            env[pattern.name] = instance
            return True
        return bound == instance
    
    if type(pattern) != type(instance):
        return False
    
    if isinstance(pattern, Variable):
        return pattern == instance
    
    if isinstance(pattern, Negation):
        return match(pattern.value, instance.value, env)
    
    if isinstance(pattern, Implication):
        return (match(pattern.left, instance.left, env) and
                match(pattern.right, instance.right, env))
    return False

def is_instance_of(axname: str, phi: Formula) -> bool:

    env : Env = {}
    return match(AXIOMS[axname], phi, env)

def find_axiom_instance(phi: Formula) -> Optional[Tuple[str, Env]]:
    for name, schema in AXIOMS.items():
        env: Env = {}
        if match(schema, phi, env):
            return name, env
    return None
