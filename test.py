# python - <<'PY'
from tokenizer import tokenize
from parser import parse_formula
from axioms import axioms as AXIOMS
from matcher import is_instance_of, find_axiom_instance


'''print(AXIOMS["AX1"])  # <A> -> (<B> -> <A>)
print(AXIOMS["AX2"])  # (<A> -> (<B> -> <C>)) -> ((<A> -> <B>) -> (<A> -> <C>))
print(AXIOMS["AX3"])  # (~<B> -> ~<A>) -> (<A> -> <B>)'''

# Example instances you can try later with a matcher:
# "P -> (Q -> P)"     matches AX1
# "(A -> (B -> C)) -> ((A -> B) -> (A -> C))"  matches AX2
# "(~Q -> ~P) -> (P -> Q)"                      matches AX3

'''print(tokenize("P -> (~Q -> P)"))
# PY

# python - <<'PY'
print(parse_formula("P -> (Q -> P)"))
# PY

print(parse_formula("P"))                    # Variable("P")
print(parse_formula("~P"))                   # Negation(Variable("P"))
print(parse_formula("P -> Q"))               # Implication(Variable("P"), Variable("Q"))
print(parse_formula("P -> Q -> R"))          # Implication(Variable("P"), Implication(Variable("Q"), Variable("R")))
print(parse_formula("~(P -> Q)"))            # Negation(Implication(Variable("P"), Variable("Q")))
print(parse_formula("(P -> (~Q -> P))"))     # Implication(Variable("P"), Implication(Negation(Variable("Q")), Variable("P")))


f = parse_formula("P -> (Q -> P)")
print(is_instance_of("AX1", f))                  # True
print(find_axiom_instance(f))                   # ('AX1', {'A': Variable('P'), 'B': Variable('Q')})

g = parse_formula("(~Q -> ~P) -> (P -> Q)")
print(is_instance_of("AX3", g))                  # True
print(find_axiom_instance(g))                   # ('AX3', {'A': Variable('P'), 'B': Variable('Q')})'''

