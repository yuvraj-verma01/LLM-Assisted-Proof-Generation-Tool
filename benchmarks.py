import argparse
from orchestrator import generate_proof

LOG_FILE = "bench_results.txt"

def log(msg: str, file):
    print(msg)               
    file.write(msg + "\n")   


def run_case(premises, goal, desc, attempts: int, file):
    log("=" * 72, file)
    log(f"CASE: {desc}", file)
    log(f"Premises: {premises if premises else '(none)'}", file)
    log(f"Goal    : {goal}", file)

    ok, proof, errors = generate_proof(premises, goal, attempts=attempts)

    if ok:
        log("Final outcome: Valid", file)
        log("--- Proof ---", file)
        log(proof, file)
    else:
        log("Final outcome: Failed", file)
        if errors:
            log("--- Reason ---", file)
            for e in errors:
                log(f" - {e}", file)
        if proof.strip():
            log("\n(Generated but invalid proof attempt)", file)
            log(proof, file)

    log("", file)


# (premises, goal, description)
BENCHMARKS = [
    ([],"P -> (Q -> P)", "1"),
    (["P", "P -> Q"], "Q", "2"),
    (["~Q -> ~P", "P"], "Q", "3"),
    (["P -> Q", "Q -> R"], "P -> R", "4"),
    (["P -> Q"], "P", "5"),
]


def main():
    ap = argparse.ArgumentParser(description="Run LLM-assisted proof benchmarks.")
    ap.add_argument("--attempts", type=int, default=5,
                    help="Max LLM repair attempts per case (default: 5)")
    args = ap.parse_args()

    with open(LOG_FILE, "w", encoding="utf-8") as file:
        for premises, goal, desc in BENCHMARKS:
            run_case(premises, goal, desc, attempts=args.attempts, file=file)

        log("=" * 72, file)
        log("Done.", file)


if __name__ == "__main__":
    main()
