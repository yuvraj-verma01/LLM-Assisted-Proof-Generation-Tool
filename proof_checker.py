from typing import List, Dict
from p2_ast import Formula, Implication
from parser import parse_formula
from proofline import Line, parse_proof_text
from matcher import is_instance_of
from substitution import substitute

class CheckResult:
    def __init__(self, ok: bool, errors: List[str]):
        self.ok = ok
        self.errors = errors

def mp_correct(target: Formula, f1: Formula, f2: Formula) -> bool: #defining modus ponens
    if isinstance(f2, Implication) and f2.left == f1 and f2.right == target:
        return True
    if isinstance(f1, Implication) and f1.left == f2 and f1.right == target:
        return True
    return False

def check_proof(assumptions: List[str], goal: str, proof_text: str) -> CheckResult: 
    sigma_formulas = [parse_formula(s) for s in assumptions]
    goal_f = parse_formula(goal)

    lines: List[Line] = parse_proof_text(proof_text)

    by_id: Dict[int, Formula] = {}   
    errors: List[str] = []

    for ln in lines:
        if any(fid >= ln.id for fid in ln.from_ids):
            errors.append(f"Line {ln.id}: cites non-earlier line(s) {ln.from_ids}.")
            continue

        statement = ln.statement

        if ln.rule == "Premise":
            if statement not in sigma_formulas:
                errors.append(f"Line {ln.id}: premise not in assumptions.")
            else:
                by_id[ln.id] = statement
        
        elif ln.rule == "MP":
            if len(ln.from_ids) != 2:
                errors.append(f"Line {ln.id}: MP needs exactly 2 references i, j.")
            else:
                a = by_id.get(ln.from_ids[0])
                b = by_id.get(ln.from_ids[1])
                if a is None or b is None:
                    errors.append(f"Line {ln.id}: MP references unknown line(s) {ln.from_ids}.")
                elif not mp_correct(statement, a, b):
                    errors.append(f"Line {ln.id}: MP invalid; need x and (x -> {statement}).")
                else:
                    by_id[ln.id] = statement

        elif ln.rule in ("AX1", "AX2", "AX3"):
            if not is_instance_of(ln.rule, statement):
                errors.append(f"Line {ln.id}: not an instance of {ln.rule}.")
            else:
                by_id[ln.id] = statement

        elif ln.rule == "Substitution":
            if len(ln.from_ids) != 1:
                errors.append(f"Line {ln.id}: Substitution cites exactly one line.")
            elif ln.subs is None or len(ln.subs) == 0:
                errors.append(f"Line {ln.id}: Substitution needs a non-empty mapping.")
            else:
                base = by_id.get(ln.from_ids[0])
                if base is None:
                    errors.append(f"Line {ln.id}: Substitution references unknown line {ln.from_ids[0]}.")
                else:
                    expected = substitute(base, ln.subs)
                    if expected != statement:
                        errors.append(
                            f"Line {ln.id}: Substitution mismatch.\n"
                            f"  expected: {expected}\n"
                            f"  found:    {statement}"
                        )
                    else:
                        by_id[ln.id] = statement

        else:
            errors.append(f"Line {ln.id}: unknown rule {ln.rule!r}.")

    if not lines:
        errors.append("Empty proof.")
    else:
        if lines[-1].statement != goal_f:
            errors.append(
                "Last line is not the goal.\n"
                f"  got:  {lines[-1].statement}\n"
                f"  need: {goal_f}"
            )

    return CheckResult(len(errors) == 0, errors)
