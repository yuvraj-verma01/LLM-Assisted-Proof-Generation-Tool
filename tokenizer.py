from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Token:
    kind: str #could be "Variable", "Negation", "Implication", "(" ")", "EOF"
    text: str # the token text

def tokenize(s: str)-> list[Token]:
    i= 0
    n= len(s)
    output = []
    while i<n:
        char = s[i]
        if char.isspace():
            i+=1
            continue
        if char in '()':
            output.append(Token(kind = char, text = char))
            i+= 1
            continue
        if char == '~':
            output.append(Token(kind = "Negation", text = char)) 
            i+= 1
            continue
        if char == '-' and i+1 < n and s[i+1] == '>':
            output.append(Token(kind = "Implication", text = "->"))
            i+= 2
            continue
        if char.isalpha(): #Variables start with an alphabet but also can contain digits and underscores
            j = i+1
            while j < n and (s[j].isalnum() or s[j] == '_'):
                j+= 1
            output.append(Token(kind = "Variable", text = s[i:j]))
            i = j
            continue
        raise ValueError(f"Unexpected character: {char}")
    output.append(Token(kind = "EOF", text = ""))
    return output
