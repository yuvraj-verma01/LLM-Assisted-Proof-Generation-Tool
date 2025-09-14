import argparse
import sys
from proof_checker import check_proof   

def main():
    ap = argparse.ArgumentParser(description="Verify a proof from a text file.")
    ap.add_argument(
        "-A", "--assumptions",
        default="",
        help='Comma-separated assumptions, e.g. "P->Q,P". Leave empty if none.'
    )
    ap.add_argument(
        "-G", "--goal",
        required=True,
        help='Goal formula, e.g. "Q" or "R -> (S -> R)".'
    )
    ap.add_argument(
        "-P", "--proof",
        required=True,
        help="Path to the .txt proof file."
    )
    args = ap.parse_args()

    # Parse assumptions into a list of strings
    assumptions = [s.strip() for s in args.assumptions.split(",") if s.strip()] if args.assumptions.strip() else []

    with open(args.proof, "r", encoding="utf-8") as f:
        proof_text = f.read()

    result = check_proof(assumptions, args.goal, proof_text)
    if result.ok:
        print("Proof verified.")
        sys.exit(0)
    else:
        print("Proof failed:")
        for e in result.errors:
            print(" -", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
