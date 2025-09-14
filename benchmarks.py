import argparse
from orchestrator import generate_proof

def run_case(premises, goal, desc, attempts: int):
    print("=" * 72)
    print(f"CASE: {desc}")
    print(f"Premises: {premises if premises else '(none)'}")
    print(f"Goal    : {goal}")
    ok, proof, errors = generate_proof(premises, goal, attempts=attempts)
    if ok:
        print("Final outcome: Valid")
        print("--- Proof ---")
        print(proof)
    else:
        print("Final outcome: Failed")
        if errors:
            print("--- Reason ---")
            for e in errors:
                print(" -", e)
        if proof.strip():
            print("\n(Generated but invalid proof attempt)")
            print(proof)
    print()

# (premises, goal, description)
BENCHMARKS = [
    ([],"P -> (Q -> P)", "1")
    (["P", "P -> Q"], "Q", "2"),
    (["~Q -> ~P", "P"], "Q", "3"),
    (["P -> Q", "Q -> R"], "P -> R", "4"),
    (["P -> Q"], "P", "5"),
]


def main():
    ap = argparse.ArgumentParser(description="Run LLM-assisted proof benchmarks.")
    ap.add_argument("--attempts", type=int, default=5, help="Max LLM repair attempts per case (default: 5)")
    args = ap.parse_args()

    for premises, goal, desc in BENCHMARKS:
        run_case(premises, goal, desc, attempts=args.attempts)

    print("=" * 72)
    print("Done.")

if __name__ == "__main__":
    main()
