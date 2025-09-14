Automated Proof Generator & Verifier (P2 Axioms + MP)

This project has two parts:

Part I (Verifier): parses and checks P2 proofs using only the axioms AX1–AX3 and rule MP (Modus Ponens).

Part II (Orchestrator): uses an LLM to generate/repair a proof for given premises and a goal. If no proof is found, it produces a counterexample (truth assignment).

The implementation uses ASCII operators only:

Negation: ~

Implication: ->

Parentheses: ( )

0) Requirements

Python 3.10+

pip install -r requirements.txt (if you created one)
Minimal deps (already imported by files you have):

openai (OpenRouter-compatible)

python-dotenv

1) Project Layout (what you actually run)
LLM_assisted_proof_generation/
  axioms.py               # AX1–AX3 patterns (schema)
  p2_ast.py               # AST node types
  tokenizer.py            # tokenizer
  parser.py               # parser
  matcher.py              # axiom instance matcher
  substitution.py         # variable substitution
  proofline.py            # proof line parser ("<n>. <formula>  <rule>")
  proof_checker.py        # Part I checker
  llm_client.py           # OpenRouter client (loads key from .env)
  orchestrator.py         # Part II generate→verify→repair (+ counterexample)
  semantics.py            # truth-table evaluator/counterexample
  CLI.py                  # optional CLI for Part I only (verifier)
  benchmarks.py           # runs a suite of cases through the orchestrator
  test_orchestrator.py    # quick examples for success/failure
  .env                    # put your API key here (see below)

2) API Key (OpenRouter)

We call the LLM via OpenRouter. Put your key in a local .env file at the project root:

OPENROUTER_API_KEY= not_stated_here
3) Quick start:

Verify the LLM client is set up:

python -c "from llm_client import complete_text; print(complete_text('Reply with exactly: OK'))"


You should see OK.

4) Run the orchestrator (Part II)
A) Programmatic (simple)
from orchestrator import generate_proof

premises = ["P", "P -> Q"]
goal = "Q"

ok, proof, errors = generate_proof(premises, goal)
print("SUCCESS" if ok else "FAILED")
print(proof if ok else errors)

B) Pre-baked examples
python benchmarks.py


This runs a few success/failure cases and prints either a valid proof or a counterexample.

5) Run the verifier only (Part I)

You can still use the verifier by itself (no LLM). The expected proof file format is:

<n>. <formula>  <justification>


Two spaces before the justification

justification ∈ {Premise, AX1, AX2, AX3, MP i,j, Substitution k <mapping>}

Example:

1. P              Premise
2. P -> Q         Premise
3. Q              MP 1,2


With the provided CLI.py:

# Example (Windows PowerShell / macOS / Linux)
python CLI.py -A "P,P->Q" -G "Q"  # if CLI prints nothing, it just verified silently


The orchestrator handles proof generation; the CLI is only for manual verification of a file you’ve already written.

6) Input/Output conventions
Premises / Goal (strings)

ASCII only: ~, ->, parentheses.

Variables: letters, digits, underscores (start with a letter), e.g. P, Q1, rate_ok.

Proof text (LLM output or manual)

Each line: "<n>. <formula> <justification>"

Line numbers start at 1 and are consecutive.

Allowed rules: Premise, AX1, AX2, AX3, MP i,j
(Substitution is supported by the verifier but the orchestrator prompt avoids it.)

Counterexamples

Printed as a Python dict: e.g. {'P': False, 'Q': False}

Means: premises are true and goal is false under that assignment.

7) Axioms (schema)

AX1: A -> (B -> A)

AX2: (A -> (B -> C)) -> ((A -> B) -> (A -> C))

AX3: (~B -> ~A) -> (A -> B)

Rule: Modus Ponens (MP)
From φ and φ -> ψ, infer ψ.

8) Examples you can try

Provable:

generate_proof(["P", "P -> Q"], "Q")
generate_proof([], "P -> (Q -> P)")
generate_proof(["~Q -> ~P", "P"], "Q")
generate_proof(["P -> Q", "Q -> R"], "P -> R")


Unprovable (gets counterexample):

generate_proof(["P -> Q"], "P")
generate_proof([], "P")
generate_proof([], "(~A -> B) -> (~A -> ~A)")

9) Troubleshooting

OPENROUTER_API_KEY not set
Create .env with OPENROUTER_API_KEY=... or set the env var in your shell.

No output when running orchestrator.py
It only defines functions by default. Use test_orchestrator.py/benchmarks.py, or add a small if __name__ == "__main__": to run a case.

Unicode operators (like ¬, →)
The orchestrator normalizes them to ASCII. If you’re writing proofs by hand, use ~ and ->.

Imports fail
Run from the project root (LLM_assisted_proof_generation/). All files are in one folder, so from X import Y should work.

10) Important: Use of AI in Development

This project was built with the assistance of AI tools (ChatGPT).
AI was used to:

1. Generate example code templates (semantics, matcher, proof_checker, proofline, orchestrator).

2. Understanding LLM integration

3. To come up with benchmark cases.

4. Draft documentation and test cases.

5. All AI-generated code and text were reviewed, tested, and understood by the author