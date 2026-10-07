# Consolidated E8 validation package

The consolidated manuscript is `merged_paper.docx`. It combines the corrected original paper and corrected update, restores the six-paragraph structure of the updated introduction with mathematical corrections, and consolidates 19 bibliography entries.

## Run

Python 3.10 or later and NumPy are required:

```sh
python -m pip install -r requirements.txt
python run_all.py --document merged_paper.docx --output merged_results.json
```

The runner executes 32 original and 18 update diagnostic groups in separate processes, checks the exact corrected statements and justifications/proofs against the consolidated manuscript, and checks its introduction and bibliography against `merged_manifest.json`. Results use namespaced identifiers such as `original/T10` and `update/T10`. These are 50 diagnostic groups, not 50 distinct theorems. Overlapping supporting results are retained and identified by their manuscript part.

A successful diagnostic is finite computational evidence, not a general mathematical proof. Conditional assumptions and limits remain in the manuscript and each suite's results. The optional NetworkX implementation comparison is explicitly marked NOT_RUN when NetworkX is absent; the exact matching oracle still runs. Install NetworkX separately to enable that comparison.

## Preserved sources

- `original/`: complete original corrected suite, its standalone manuscript, claim manifest, source identity and previous results.
- `update/`: complete updated corrected suite, its standalone manuscript, claim manifest, source identity, references and previous results.
- `merged_results.json`: execution results against the consolidated manuscript; consult this for merged-document validation. Nested `results.json` files retain their prior standalone-document provenance.
- `coverage.json`: namespaced inventory of all 50 diagnostic groups.

Both suites retain their individual `check_*.py` entry points and original filenames. The consolidated runner isolates module imports to prevent collisions. Written proofs, finite evidence, original-draft regression verdicts, and untested implementation claims remain distinguished.

The abstract was revised on 7 October 2026 to incorporate the requested spectral-estimation framing while retaining the corrected mathematical qualifications. The original suite claim manifest and its included manuscript snapshot carry the same revised abstract. Nested historical results retain their earlier provenance; merged_results.json records the current run.
