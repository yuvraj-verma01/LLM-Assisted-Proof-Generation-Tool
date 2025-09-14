from dataclasses import dataclass
from p2_ast import Formula, Variable, Negation, Implication

@dataclass(frozen=True)
class Meta(Formula):
    name: str
    def __str__(self) -> str:
        return f"<{self.name}>"

A = Meta("A")
B = Meta("B")
C = Meta("C")

AX1= Implication(A, Implication(B, A))
AX2= Implication(Implication(A, Implication(B, C)), Implication(Implication(A, B), Implication(A, C)))
AX3 = Implication(Implication(Negation(B), Negation(A)), Implication(A, B))

axioms = {"AX1": AX1, "AX2": AX2, "AX3": AX3}