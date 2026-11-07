# Contributing

This guide is for people changing ClippyFirst. The repository's canonical technical map is [docs/README.md](docs/README.md); coding-agent-specific execution rules are in [AGENTS.md](AGENTS.md). Keep those documents complementary: this file is the human contributor entry point, not a second task ledger.

## Before changing code

1. Read [README.md](README.md) for product scope and [docs/architecture.md](docs/architecture.md) for the stable pipeline.
2. Read the newest entry in [the execution handoff](docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md), then reconcile it with [the validation matrix](docs/validation-matrix.md) and [the audit](docs/final-audit.md). Historical handoff entries are not current status.
3. Read the owner document for the subsystem and trace its callers, tests, data/schema inputs and generated outputs. See [the documentation map](docs/README.md) and [script inventory](scripts/README.md).
4. For linguistic or corpus changes, read [the research protocol](docs/research-protocol.md), [evidence registry](docs/evidence.md) and [independent adjudication protocol](docs/independent-adjudication-protocol.md).

## Architecture contracts

The primary phonetic route is:

`Thai orthography → structural analysis → Thai phonology → typed IPA → Ukrainian adaptation from IPA → Ukrainian practical orthography`.

The typed IPA result is the only input contract for the phonetic Ukrainian adapter. Preserve phonemic and surface IPA as distinct layers, and retain syllable boundaries, tone, length, provenance and uncertainty.

RTGS is a separate, optional romanization route:

`Thai orthography → RTGS syllable analysis/romanization → RTGS Latin → separately labelled Ukrainian rendering`.

RTGS is not IPA, is not a phonetic transcription, and must never become an input to the primary IPA → Ukrainian adapter. It does not fully represent tone or vowel length. Unsupported or ambiguous spans must remain explicitly unavailable; do not add speculative grapheme fallbacks.

## Development workflow

- Work from current `main` on one focused branch and one focused PR. Do not merge old divergent branch histories wholesale; compare their actual changes first. Preserve historical refs unless there is an explicit, verified reason to remove them.
- For behavior changes, add a failing regression test first, reproduce the defect, fix the smallest root cause, and rerun the affected tests.
- Prefer existing modules, schemas, registries, generators and tests. Do not create parallel plans, duplicate data sources, or hand-edit generated artifacts.
- Keep source data, licensing, version pins and provenance explicit. Do not bundle external datasets or models without a verified permission basis.
- Separate spec compliance from code-quality review. Every finding should name a concrete input, path, requirement or test.
- Inspect the final diff and verify the exact commit that will be proposed for merge.

## Local checks

Set up the development environment:

```bash
python -m pip install -e ".[dev]"
```

For RTGS parity work, install the pinned comparator:

```bash
python -m pip install pythainlp==5.4.0
```

Useful focused checks:

```bash
ruff check src tests scripts
python -m pytest -q -ra
node web/tests/rtgs-reference.test.mjs
node web/tests/rtgs-romanizer.test.mjs
python scripts/test_rtgs_parity.py
```

The GitHub Actions workflows are the authoritative full verification contract. Inspect `.github/workflows/ci.yml`, `.github/workflows/web-static.yml`, Pages and compatibility workflows for the current complete command set. Run the relevant workflow checks on the final PR head; a skipped job is not a pass. Check generated-artifact drift and clean-install/wheel smoke where the change affects packaging or generated data.

## Linguistic evidence and claims

- A published whole-word romanization does not attest the internal syllable boundaries inferred by an implementation.
- PyThaiNLP parity demonstrates implementation agreement with a pinned comparator, not linguistic correctness.
- Source-annotated corpora, source-attested dictionary forms and model outputs are not independently adjudicated gold.
- Do not report accuracy without an appropriately scoped, independently reviewed gold set and a reproducible evaluation.
- Record unresolved judgments as blocked or not measured; never invent a pronunciation to make a test green.

## Pull request acceptance

A PR should explain the behavior being changed, its scope, the evidence behind linguistic decisions, the exact commands/workflows run and their results. Update the existing validation matrix, audit and handoff when the project state changes. Update `final-audit.json` alongside the Markdown audit when the audit register changes. Keep the root README user-facing and the docs index navigational; neither is a substitute for executable tests or the acceptance ledger.
