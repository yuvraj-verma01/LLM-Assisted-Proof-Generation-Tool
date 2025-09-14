import re
from dataclasses import dataclass
from typing import Tuple, Optional, Dict, List
from p2_ast import Formula
from parser import parse_formula
from substitution import Substitution

@dataclass(frozen=True)
class Line:
    id : int
    statement: Formula
    rule: str
    from_ids: Tuple[int, ...]
    subs: Optional[Substitution] = None

_line_re = re.compile(r"^\s*(\d+)\.\s*(.*?)\s{2,}(.+?)\s*$")

def parse_subs_blob(blob: str) -> Substitution:
    subs: Dict[str, Formula] = {}
    if not blob.strip():
        return subs
    parts = [p.strip() for p in blob.split(',')]
    for p in parts:
        if not p:
            continue
        if '=' not in p:
            raise ValueError(f"Bad substitution: {p}")
        v, f = p.split('=', 1)
        v, f = v.strip(), f.strip()
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", v):
            raise ValueError(f"Substitution variable must be a const: {v}")
        subs[v] = parse_formula(f)
    return subs

def parse_justification(just: str) -> Tuple[str, Tuple[int, ...], Optional[Substitution]]:
    just = just.strip()
    if just == "Premise":
        return "Premise", (), None
    if just in ("AX1", "AX2", "AX3"):
        return just, (), None
    if just.startswith("MP"):
        m = re.match(r"MP\s+(\d+)\s*,\s*(\d+)\s*$", just)
        if not m:
            raise ValueError(f"Bad MP justification: {just}")
        i, j = int(m.group(1)), int(m.group(2))
        return "MP", (i, j), None
    if just.startswith("Substitution"):
        m = re.match(r"Substitution\s+(\d+)\s+(.*)$", just)
        if not m:
            raise ValueError(f"Bad Substitution justification: {just}")
        k = int(m.group(1))
        subs_blob = m.group(2).strip()
        subs = parse_subs_blob(subs_blob)
        return "Substitution", (k,), subs
    raise ValueError(f"Unknown justification: {just}")

def parse_proof_text(proof_text: str) -> List[Line]:
    lines: List[Line] = []
    for raw in proof_text.strip().splitlines():
        if not raw.strip():
            continue
        m = _line_re.match(raw)
        if not m:
            raise ValueError(f"Bad proof line format: {raw}")
        ln = int(m.group(1))
        formula_str = m.group(2).strip()
        just = m.group(3).strip()
        stmt = parse_formula(formula_str)
        rule, from_ids, subs = parse_justification(just)
        lines.append(Line(ln, stmt, rule, from_ids, subs))
    ids = [ln.id for ln in lines]
    if ids != list(range(1, len(lines) + 1)):
        raise ValueError(f"Line numbers must be consecutive from 1; got {ids}")
    return lines

