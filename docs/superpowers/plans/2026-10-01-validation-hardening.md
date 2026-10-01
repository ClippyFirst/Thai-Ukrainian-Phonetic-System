# Thai → Ukrainian Research Validation Implementation Plan

Goal: Move the repository from a structural research foundation to a reproducible validation-ready release without pretending that licensed corpus accuracy has been measured.

Architecture: Keep the existing Thai orthography/phonology pipeline intact, add a small evaluation layer that consumes user-supplied corpus records, computes auditable metrics, and never bundles restricted corpora. Strengthen provenance and release auditing around the distinction between structural coverage, lexical attestation, and empirical validation.

Tech Stack: Python 3.10+, standard library, CSV/JSON/JSONL, unittest, GitHub Actions.

Spec: docs/research-protocol.md

## Global Constraints
- No giant manual Thai-character → Ukrainian-character substitution table.
- Standard Thai / Bangkok-centered contemporary standard is the primary scope.
- Tone marks and phonological tones remain separate.
- Structural combinations must not be reported as valid, lexical, or corpus-attested syllables.
- Ukrainian target inventory remains external; local vectors are a reproducible snapshot/adapter.
- Restricted corpus data must not be redistributed by the repository.
- Empirical accuracy/probability claims require actual gold data.

## Review Focus
- A corpus record with missing gold IPA must not silently count as correct.
- A multi-syllable record must not be confused with a single-syllable parser fixture.
- Empty or malformed records must be rejected deterministically.
- Metric denominators must be explicit and zero-safe.
- The release audit must distinguish validation infrastructure from completed validation.

## Task 1: Corpus evaluation contract
Files: create tests/test_evaluation.py and src/thai_ukrainian/evaluation.py.
Interfaces: load_records(path) -> list[dict]; evaluate_records(records) -> dict; evaluate_file(path) -> dict.
Steps: add failing tests; verify expected failures in CI; implement standard-library evaluator; run full suite; commit.

## Task 2: Reproducible command-line evaluation
Files: create scripts/evaluate_corpus.py; modify src/thai_ukrainian/cli.py; extend tests/test_evaluation.py.
Interface: python scripts/evaluate_corpus.py path/to/records.jsonl.
Output: deterministic JSON with records_total, records_evaluable, ipa_exact_accuracy, tone_accuracy, and explicit status.
Steps: add failing CLI contract test; verify; implement; run full suite; commit.

## Task 3: Evidence and audit hardening
Files: modify docs/corpus-validation.md, docs/final-audit.md, data/claims.csv, README.md.
Steps: document denominators, missing gold fields, source licensing and corpus version identifiers; update release language; run derivation and tests; commit.

## Task 4: Release verification
Files: modify pyproject.toml and .github/workflows/ci.yml; regenerate docs/generated-audit.json and docs/syllable-space.json.
Steps: add deterministic generated-artifact verification; run workflow; inspect every job and step; only report success when actually successful.
