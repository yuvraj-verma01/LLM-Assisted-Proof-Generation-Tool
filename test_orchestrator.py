from orchestrator import generate_proof

def run_case(premises, goal, description):
    print(f"=== {description} ===")
    ok, proof, errors = generate_proof(premises, goal)
    if ok:
        print("Result: SUCCESS")
        print("----- Proof -----")
        print(proof)
    else:
        print("Result: FAILED")
        if errors:
            for e in errors:
                print(" -", e)
        if proof.strip():
            print("\n(Generated but invalid proof attempt:)")
            print(proof)
    print("\n" + "=" * 40 + "\n")

def main():
    
    run_case(["P", "P -> Q"], "Q", "Simple MP")
    run_case([], "P -> (Q -> P)", "AX1 Instance")
    run_case(["~Q -> ~P", "P"], "Q", "AX3 Usage")
    run_case(["P -> Q", "Q -> R"], "P -> R", "Transitivity via AX2")
    run_case(["P -> Q"], "P", "Unprovable: Need P, but only have P -> Q")
    run_case([], "P", "Unprovable: P without premises")

if __name__ == "__main__":
    main()
