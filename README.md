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

<!-- Quick Intro -->
<p>
  This project has two parts:
</p>
<ul>
  <li><strong>Part I (Verifier):</strong> Parses and checks P2 proofs using only axioms AX1–AX3 and rule MP.</li>
  <li><strong>Part II (Orchestrator):</strong> Uses an LLM to generate/repair a proof for given premises and a goal. If no proof is found, it produces a counterexample (truth assignment).</li>
</ul>

<!-- TOC -->
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

<!-- 0) Requirements -->
<h2 id="requirements">0) Requirements</h2>
<ul>
  <li>Python <strong>3.10+</strong></li>
  <li>
    Optional deps:
    <code>openai</code> (OpenRouter-compatible), <code>python-dotenv</code>
    <br/>Install (if you have a requirements file):
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
</ul>

<!-- 1) Layout -->
<h2 id="layout">1) Project Layout (what you actually run)</h2>
<pre><code>LLM_assisted_proof_generation/
  axioms.py               # AX1–AX3 patterns (schema)
  p2_ast.py               # AST node types
  tokenizer.py            # tokenizer
  parser.py               # parser
  matcher.py              # axiom instance matcher
  substitution.py         # variable substitution
  proofline.py            # proof line parser ("&lt;n&gt;. &lt;formula&gt;  &lt;rule&gt;")
  proof_checker.py        # Part I checker
  llm_client.py           # OpenRouter client (loads key from .env)
  orchestrator.py         # Part II generate→verify→repair (+ counterexample)
  semantics.py            # truth-table evaluator/counterexample
  CLI.py                  # optional CLI for Part I only (verifier)
  benchmarks.py           # runs a suite of cases through the orchestrator
  test_orchestrator.py    # quick examples for success/failure
  .env                    # put your API key here (see below)
</code></pre>

<!-- 2) API Key -->
<h2 id="apikey">2) API Key (OpenRouter)</h2>
<p>
  We call the LLM via OpenRouter. Put your key in a local <code>.env</code> file at the project root:
</p>
<pre><code>OPENROUTER_API_KEY= not_stated_here
</code></pre>

<!-- 3) Quick Start -->
<h2 id="quickstart">3) Quick Start</h2>
<details>
  <summary><strong>Verify the LLM client is set up</strong></summary>
  <pre><code>python -c "from llm_client import complete_text; print(complete_text('Reply with exactly: OK'))"</code></pre>
  <p>You should see <code>OK</code>.</p>
</details>

<!-- 4) Orchestrator -->
<h2 id="orchestrator">4) Run the Orchestrator (Part II)</h2>
<h3>A) Programmatic (simple)</h3>
<pre><code>from orchestrator import generate_proof

premises = ["P", "P -&gt; Q"]
goal = "Q"

ok, proof, errors = generate_proof(premises, goal)
print("SUCCESS" if ok else "FAILED")
print(proof if ok else errors)
</code></pre>

<h3>B) Pre-baked examples</h3>
<pre><code>python benchmarks.py
</code></pre>
<p>This runs a few success/failure cases and prints either a valid proof or a counterexample.</p>

<!-- 5) Verifier -->
<h2 id="verifier">5) Run the Verifier Only (Part I)</h2>
<p>
  You can use the verifier by itself (no LLM). The expected proof file format is:
</p>
<pre><code>&lt;n&gt;. &lt;formula&gt;  &lt;justification&gt;

Two spaces before the justification
justification ∈ {Premise, AX1, AX2, AX3, MP i,j, Substitution k &lt;mapping&gt;}

Example:
1. P              Premise
2. P -&gt; Q         Premise
3. Q              MP 1,2
</code></pre>

<p>With the provided <code>CLI.py</code>:</p>
<pre><code># Example (Windows PowerShell / macOS / Linux)
python CLI.py -A "P,P-&gt;Q" -G "Q"  # if CLI prints nothing, it just verified silently
</code></pre>

<p>
  The orchestrator handles proof generation; the CLI is only for manual verification of a file you’ve already written.
</p>

<!-- 6) I/O Conventions -->
<h2 id="io">6) Input/Output Conventions</h2>
<ul>
  <li><strong>Premises / Goal (strings)</strong><br/>
    ASCII only: <code>~</code>, <code>-&gt;</code>, parentheses.<br/>
    Variables: letters, digits, underscores (start with a letter), e.g. <code>P</code>, <code>Q1</code>, <code>rate_ok</code>.
  </li>
  <li><strong>Proof text (LLM output or manual)</strong><br/>
    Each line: <code>"&lt;n&gt;. &lt;formula&gt; &lt;justification&gt;"</code><br/>
    Line numbers start at 1 and are consecutive.<br/>
    Allowed rules: <code>Premise, AX1, AX2, AX3, MP i,j</code> (<em>Substitution</em> is supported by the verifier but the orchestrator prompt avoids it.)
  </li>
  <li><strong>Counterexamples</strong><br/>
    Printed as a Python dict, e.g. <code>{'P': False, 'Q': False}</code><br/>
    Means: premises are true and goal is false under that assignment.
  </li>
</ul>

<!-- 7) Axioms -->
<h2 id="axioms">7) Axioms (Schema)</h2>
<ul>
  <li><strong>AX1</strong>: <code>A -&gt; (B -&gt; A)</code></li>
  <li><strong>AX2</strong>: <code>(A -&gt; (B -&gt; C)) -&gt; ((A -&gt; B) -&gt; (A -&gt; C))</code></li>
  <li><strong>AX3</strong>: <code>(~B -&gt; ~A) -&gt; (A -&gt; B)</code></li>
</ul>
<p><strong>Rule: Modus Ponens (MP)</strong><br/>
From <code>φ</code> and <code>φ -&gt; ψ</code>, infer <code>ψ</code>.
</p>

<!-- 8) Examples -->
<h2 id="examples">8) Examples you can try</h2>
<h3>Provable</h3>
<pre><code>generate_proof(["P", "P -&gt; Q"], "Q")
generate_proof([], "P -&gt; (Q -&gt; P)")
generate_proof(["~Q -&gt; ~P", "P"], "Q")
generate_proof(["P -&gt; Q", "Q -&gt; R"], "P -&gt; R")
</code></pre>

<h3>Unprovable (gets counterexample)</h3>
<pre><code>generate_proof(["P -&gt; Q"], "P")
generate_proof([], "P")
generate_proof([], "(~A -&gt; B) -&gt; (~A -&gt; ~A)")
</code></pre>

<!-- 9) Troubleshooting -->
<h2 id="troubleshooting">9) Troubleshooting</h2>

<details>
  <summary><strong>OPENROUTER_API_KEY not set</strong></summary>
  <p>Create <code>.env</code> with <code>OPENROUTER_API_KEY=...</code> or set the env var in your shell.</p>
</details>

<details>
  <summary><strong>No output when running orchestrator.py</strong></summary>
  <p>It only defines functions by default. Use <code>test_orchestrator.py</code>/<code>benchmarks.py</code>, or add a small <code>if __name__ == "__main__":</code> to run a case.</p>
</details>

<details>
  <summary><strong>Unicode operators (like ¬, →)</strong></summary>
  <p>The orchestrator normalizes them to ASCII. If you’re writing proofs by hand, use <code>~</code> and <code>-&gt;</code>.</p>
</details>

<details>
  <summary><strong>Imports fail</strong></summary>
  <p>Run from the project root (<code>LLM_assisted_proof_generation/</code>). All files are in one folder, so <code>from X import Y</code> should work.</p>
</details>

<!-- 10) AI Use -->
<h2 id="aiuse">10) Important: Use of AI in Development</h2>
<p>
  This project was built with the assistance of AI tools (ChatGPT).
  AI was used to:
</p>
<ol>
  <li>Generate example code templates (semantics, matcher, proof_checker, proofline, orchestrator).</li>
  <li>Understand LLM integration.</li>
  <li>Devise benchmark cases.</li>
  <li>Draft documentation and test cases.</li>
  <li>All AI-generated code and text were reviewed, tested, and understood by the author.</li>
</ol>

<hr/>

<p align="center" style="font-size:13px;color:#666;">
  <em>ASCII operators only:</em> Negation: <code>~</code> &nbsp;•&nbsp; Implication: <code>-&gt;</code> &nbsp;•&nbsp; Parentheses: <code>( )</code>
</p>
