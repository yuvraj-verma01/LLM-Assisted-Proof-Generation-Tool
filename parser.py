from typing import List
from tokenizer import tokenize, Token
from p2_ast import Formula, Variable, Negation, Implication

class Parser:
    def __init__(self, string: str):
        self.tokens: List[Token] = tokenize(string)
        self.i: int = 0

    def peek(self) -> Token:
        return self.tokens[self.i]

    def consume(self, kind: str) -> Token:
        t = self.peek()
        if t.kind != kind:
            raise ValueError(
                f"Expected {kind}, got {t.kind} at token {self.i} (text={t.text!r})"
            )
        self.i += 1
        return t

    def parse(self) -> Formula:
        f = self.parse_implication()
        if self.peek().kind != "EOF":
            t = self.peek()
            raise ValueError(
                f"Trailing tokens after formula starting at {t.kind}:{t.text!r}"
            )
        return f

    def parse_implication(self) -> Formula:
        left = self.parse_negation()
        if self.peek().kind == "Implication":
            self.consume("Implication")
            right = self.parse_implication()   
            return Implication(left, right)
        return left

    def parse_negation(self) -> Formula:
        if self.peek().kind == "Negation":
            self.consume("Negation")
            return Negation(self.parse_negation())   
        return self.parse_atom()

    def parse_atom(self) -> Formula:
        t = self.peek()
        if t.kind == "Variable":
            self.consume("Variable")
            return Variable(t.text)
        if t.kind == "(":
            self.consume("(")
            f = self.parse_implication()
            self.consume(")")
            return f
        raise ValueError(f"Unexpected token {t.kind}:{t.text!r} at token {self.i}")

def parse_formula(s: str) -> Formula:
    return Parser(s).parse()
