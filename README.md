MIT License
Copyright (c) October 2026 Roger Cooperman; A.E. Petrunina V.V.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Updated E8 white paper validation suite

This package matches the corrected version of the newly attached updated white paper. It covers its ten numbered items (Theorems 10 and 13–20, plus Lemma 6) and eight groups of supporting mathematical results. It is self-contained and does not need the previous validation ZIP.

## Run

Python 3.10+ and NumPy are required:

```bash
python -m pip install -r requirements.txt
python validate_all.py --document corrected_paper.docx --output my_results.json
python check_t16.py
python validate_all.py --list
```

Run from the extracted folder. Do not use `python -O`, because assertions implement the checks. The suite uses no quantum hardware, credentials or network access. Optional `pip install networkx` enables an additional matching-library comparison; otherwise L6 explicitly reports NOT_RUN for that comparison and still runs an exhaustive exact small-graph oracle. Neither check proves asymptotic matching complexity or real-time hardware latency.

## Interpretation

Execution PASS means the diagnostic completed successfully. This includes checks that demonstrate why an original assertion fails. `original_verdict` applies to the submitted draft, not the corrected theorem. `scope` identifies assumptions and what remains unproved or unimplemented. Finite computations do not prove continuum theorems, a general optimization guarantee, a physical field theory or fault tolerance.

The document comparison checks the exact corrected titles, statements, equations, proofs and scope paragraphs against `claims.json`. It fails on a mismatch. This verifies synchronization, not mathematical truth. General proof arguments are in the paper; calculations and counterexamples are in the scripts. Change the shared claim record and associated diagnostic when revising a formula.

## Contents

- `corrected_paper.docx`: corrected paper, identical to the document delivered separately.
- `validate_all.py`: all diagnostic implementations and document comparison.
- `check_*.py`: individual entry points for all 18 groups.
- `claims.json`: corrected statements, equations, proofs, limitations and source mapping.
- `results.json`: executed results and corrected document SHA256.
- `coverage.md`: mapping from submitted results to checks.
- `submitted_source.txt`: paragraph-numbered text of the submitted update.
- `source_identity.json`: submitted and corrected document hashes.
- `references.json`: sources used for the corrections.

## Exact and numerical scope

Root closure, matching enumeration, code checks, distillation error-pattern counts, rational probabilities and formal series coefficients use integer or Fraction arithmetic. NumPy matrix identities use tolerance 1e-10. The distillation fixed point is numerically bracketed with rational evaluations; uniqueness of that root is not inferred from bisection. The certified iteration bound uses an exact rational majorant with p_star=0.01 and A approximately 40.7144517.

The concentration examples include a finite torus grid and an exactly enumerated binomial law. These illustrate the stated bounded-differences argument; they do not substitute for its general proof. The thermal integral is checked through the zeta(2) series and integral-test remainder bounds. Field-theory checks verify parameter algebra and integrability conditions, not a Chern–Simons path integral or hardware edge realization.

The corrected paper replaces unsupported claims with conditional results. In particular, it does not claim a 72-vertex bound for all decoding windows, that 8 Cartan matrices span all 256 diagonal operators, that a scalar braid phase is evidence of non-Abelian statistics, or that polynomial state-vector cost in N is polynomial cost in qubit count.
