<!-- Automated Proof Generator & Verifier (P2 Axioms + MP) -->
<div align="center" style="margin-bottom:18px;">
  <h1 style="margin:0;">Automated Proof Generator & Verifier</h1>
  <p style="margin:6px 0 0 0; font-size:14px; color:#555;">
    <strong>System P2:</strong> AX1–AX3 + Modus Ponens (MP) • ASCII syntax (~, ->, ( ))
  </p>
  <p style="margin:8px 0 0 0;">
    <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-informational">
    <img alt="LLM" src="https://img.shields.io/badge/LLM-OpenRouter-blueviolet">
    <img alt="License" src="https://img.shields.io/badge/Logic-P2%20Hilbert%20style-lightgrey">
  </p>
</div>

<hr/>

<p>
  This project has two parts:
</p>
<ul>
  <li><strong>Part I (Verifier):</strong> Parses and checks P2 proofs using only axioms AX1–AX3 and rule MP.</li>
  <li><strong>Part II (Orchestrator):</strong> Uses an LLM to generate/repair a proof for given premises and a goal. If no proof is found, it produces a counterexample (truth assignment).</li>
</ul>

<h2 id="toc">Table of Contents</h2>
<ol>
  <li><a href="#requirements">Requirements</a></li>
  <li><a href="#layout">Project Layout</a></li>
  <li><a href="#apikey">API Key (OpenRouter)</a></li>
  <li><a href="#quickstart">Quick Start</a></li>
  <li><a href="#orchestrator">Run the Orchestrator (Part II)</a></li>
  <li><a href="#verifier">Run the Verifier Only (Part I)</a></li>
  <li><a href="#io">Input/Output Conventions</a></li>
  <li><a href="#axioms">Axioms (Schema) & Rule</a></li>
  <li><a href="#examples">Examples</a></li>
  <li><a href="#troubleshooting">Troubleshooting</a></li>
  <li><a href="#aiuse">Use of AI in Development</a></li>
</ol>

<hr/>

<h2 id="requirements">0) Requirements</h2>
<ul>
  <li>Python <strong>3.10+</strong></li>
  <li>No <code>requirements.txt</code> provided. You must install dependencies manually:</li>
</ul>
<pre><code>pip install openai python-dotenv</code></pre>

<h2 id="layout">1) Project Layout</h2>
<pre><code>LLM_assisted_proof_generation/
  axioms.py               # AX1–AX3 patterns (schema)
  p2_ast.py               # AST node types
  tokenizer.py            # tokenizer
  parser.py               # parser
  matcher.py              # axiom instance matcher
  substitution.py         # variable substitution
  proofline.py            # proof line parser ("<n>. <formula>  <rule>")
  proof_checker.py        # Part I checker
  llm_client.py           # OpenRouter client (reads key from .env, model configurable inside)
  orchestrator.py         # Part II generate→verify→repair (+ counterexample)
  semantics.py            # truth-table evaluator/counterexample
  CLI.py                  # CLI for Part I only (verifier)
  benchmarks.py           # runs a suite of cases, outputs to bench_results.txt
  README.md
  .env (not committed)    # you must create this with your API key
</code></pre>

<h2 id="apikey">2) API Key (OpenRouter)</h2>
<p>Create a file named <code>.env</code> in the project root:</p>
<pre><code>OPENROUTER_API_KEY=your_api_key_here
</code></pre>
<p>
You may also need to change the default <code>model</code> inside <code>llm_client.py</code> to a model available under your account.
</p>

<h2 id="quickstart">3) Quick Start</h2>
<details>
  <summary><strong>Verify the LLM client is set up</strong></summary>
  <pre><code>python -c "from llm_client import complete_text; print(complete_text('Reply with exactly: OK'))"</code></pre>
  <p>You should see <code>OK</code>.</p>
</details>

<h2 id="orchestrator">4) Run the Orchestrator (Part II)</h2>
<h3>A) Programmatic</h3>
<pre><code>from orchestrator import generate_proof

premises = ["P", "P -> Q"]
goal = "Q"

ok, proof, errors = generate_proof(premises, goal)
print("SUCCESS" if ok else "FAILED")
print(proof if ok else errors)
</code></pre>

<h3>B) Benchmarks</h3>
<pre><code>python benchmarks.py
</code></pre>
<p>This runs a few success/failure cases and saves output to <code>bench_results.txt</code>.</p>

<h2 id="verifier">5) Run the Verifier Only (Part I)</h2>
<p>Proofs must be written in a plain text file (e.g. <code>my_proof.txt</code>):</p>
<pre><code>1. P              Premise
2. P -> Q         Premise
3. Q              MP 1,2
</code></pre>

<p>Run via CLI:</p>
<pre><code># Example
python CLI.py -A "P,P->Q" -G "Q" -P my_proof.txt
</code></pre>
<ul>
  <li><code>-A</code> / <code>--assumptions</code>: comma-separated premises (leave empty if none)</li>
  <li><code>-G</code> / <code>--goal</code>: the goal formula</li>
  <li><code>-P</code> / <code>--proof</code>: path to the proof text file</li>
</ul>
<p>If the proof verifies, it prints <code>Proof verified.</code>. Otherwise, errors are listed:contentReference[oaicite:0]{index=0}.</p>

<h2 id="io">6) Input/Output Conventions</h2>
<ul>
  <li><strong>ASCII only</strong>: <code>~</code>, <code>-></code>, parentheses.</li>
  <li>Variables: letters, digits, underscores (must start with a letter).</li>
  <li>Justifications: <code>Premise</code>, <code>AX1</code>, <code>AX2</code>, <code>AX3</code>, <code>MP i,j</code>. (Substitution supported but not used in orchestrator.)</li>
  <li>Counterexamples are printed as dicts, e.g. <code>{'P': True, 'Q': False}</code>.</li>
</ul>

<h2 id="axioms">7) Axioms</h2>
<ul>
  <li><strong>AX1</strong>: <code>A -> (B -> A)</code></li>
  <li><strong>AX2</strong>: <code>(A -> (B -> C)) -> ((A -> B) -> (A -> C))</code></li>
  <li><strong>AX3</strong>: <code>(~B -> ~A) -> (A -> B)</code></li>
</ul>
<p><strong>Rule:</strong> Modus Ponens (MP): from <code>φ</code> and <code>φ -> ψ</code>, infer <code>ψ</code>.</p>

<h2 id="examples">8) Examples</h2>
<h3>Provable</h3>
<pre><code>generate_proof(["P", "P -> Q"], "Q")
generate_proof([], "P -> (Q -> P)")
generate_proof(["~Q -> ~P", "P"], "Q")
generate_proof(["P -> Q", "Q -> R"], "P -> R")
</code></pre>

<h3>Unprovable (counterexample)</h3>
<pre><code>generate_proof(["P -> Q"], "P")
generate_proof([], "P")
generate_proof([], "(~A -> B) -> (~A -> ~A)")
</code></pre>

<h2 id="troubleshooting">9) Troubleshooting</h2>
<details>
  <summary><strong>OPENROUTER_API_KEY not set</strong></summary>
  <p>Create a <code>.env</code> with <code>OPENROUTER_API_KEY=...</code>.</p>
</details>
<details>
  <summary><strong>No output from orchestrator.py</strong></summary>
  <p>Use <code>benchmarks.py</code> or add <code>if __name__ == "__main__":</code> in <code>orchestrator.py</code>.</p>
</details>
<details>
  <summary><strong>Unicode operators</strong></summary>
  <p>Use ASCII only: <code>~</code> and <code>-></code>.</p>
</details>
<details>
  <summary><strong>Imports fail</strong></summary>
  <p>Run from the project root (<code>LLM_assisted_proof_generation/</code>).</p>
</details>

<h2 id="aiuse">10) Important: Use of AI in Development</h2>
<p>
This project was built with the assistance of AI tools (ChatGPT).  
AI was used to generate code templates, integrate the LLM client, devise benchmarks, draft docs, and test cases.  
All AI-generated outputs were reviewed and understood by the author.
</p>

<hr/>
<p align="center" style="font-size:13px;color:#666;">
  <em>ASCII operators only:</em> Negation: <code>~</code> • Implication: <code>-></code> • Parentheses: <code>( )</code>
</p>
