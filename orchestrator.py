# orchestrator.py
from proofline import parse_proof_text
from proof_checker import check_proof
from parser import parse_formula
from semantics import counterexample
from llm_client import complete_text

# Prompt templates
GEN_PROMPT = """You are a proof generator for a Hilbert-style propositional system with:
Axioms:
AX1: A -> (B -> A)
AX2: (A -> (B -> C)) -> ((A -> B) -> (A -> C))
AX3: (~B -> ~A) -> (A -> B)
Rule: MP (Modus Ponens)

TASK: Given premises and a goal, produce a complete proof that ends with the goal.

Rules:
- Use only: Premise, AX1, AX2, AX3, MP.
- ASCII only: "~" for not, "->" for implies, parentheses "()".
- Each line: "<n>. <formula>  <justification>"
- Line numbers start at 1 and are consecutive.
- The last line must equal the goal exactly.

Premises:
{premises}

Goal:
{goal}

Return ONLY the proof lines.
"""

REPAIR_PROMPT = """Fix the proof so it verifies under AX1–AX3 and MP.

Premises:
{premises}
Goal:
{goal}

Previous proof:
{proof}

Verifier errors:
{errors}

Constraints:
- Use only Premise, AX1, AX2, AX3, MP.
- Keep ASCII "~" and "->", and the exact line format "<n>. <formula>  <justification>".
- Keep numbering consecutive; make minimal edits.

Return ONLY the corrected proof lines.
"""

def _format_premises(premises: list[str]) -> str:
    return "\n".join(f"- {p}" for p in premises) if premises else "(none)"

def _normalize(raw: str) -> str:
    s = raw.replace("¬", "~").replace("→", "->").strip()
    lines, n = [], 1
    for line in s.splitlines():
        line = line.strip()
        if not line:
            continue
        if not line[:1].isdigit():
            if "  " in line:
                formula, just = line.split("  ", 1)
                lines.append(f"{n}. {formula.strip()}  {just.strip()}")
            else:
                lines.append(f"{n}. {line}")
        else:
            lines.append(line)
        n += 1
    return "\n".join(lines)

def generate_proof(premises: list[str], goal: str, attempts: int = 5) -> tuple[bool, str, list[str]]:
    """
    Returns: (ok, proof_text, errors_list)
    Tries up to `attempts`: first generate, then iterative repair with checker feedback.
    Falls back to a semantic counterexample if proof generation fails.
    """
    proof, errors_blob = "", ""
    for k in range(attempts):
        prompt = (
            GEN_PROMPT.format(premises=_format_premises(premises), goal=goal)
            if k == 0 else
            REPAIR_PROMPT.format(premises=_format_premises(premises),
                                 goal=goal, proof=proof, errors=errors_blob)
        )

        raw = complete_text(prompt)
        proof = _normalize(raw)

        try:
            parse_proof_text(proof)
        except Exception as e:
            errors_blob = str(e)
            continue

        result = check_proof(premises, goal, proof)
        if result.ok:
            return True, proof, []
        errors_blob = "\n".join(result.errors)

    #If all attempts failed then counterexample
    try:
        prem_formulas = [parse_formula(p) for p in premises]
        goal_f = parse_formula(goal)
        ce = counterexample(prem_formulas, goal_f)
        if ce:
            return False, proof, [f"Counterexample: {ce}"]
    except Exception as e:
        return False, proof, [f"Counterexample check failed: {e}"]

    return False, proof, errors_blob.splitlines() if errors_blob else []
