# Repository audit — 2026-10-05

## Scope

This audit reconstructs the research architecture of the current main branch before finalization. It follows the project's cleanup protocol: distinguish authoritative research inputs, implementation, validation, documentation, derived artifacts and historical material rather than treating every committed file as equally authoritative.

## Current repository identity

- Project: Thai → Ukrainian Phonetic-Graphemic Correspondence System
- Default branch: main
- Package version: 0.5.0
- License: MIT
- Primary language: Python
- Research scope: contemporary Standard Thai, with a Bangkok/central-standard reference where the evidence permits
- Target: Ukrainian phonetic/phonological and practical orthographic candidates
- Empirical benchmark: not yet claimed

## Findings

### 1. Core architecture is coherent

The repository already separates Thai source registries in data/thai, derived audit artifacts in data/derived, implementation in src/thai_ukrainian, schemas in schemas, tests in tests, and methodology/validation documentation in docs.

The central pipeline is consistently documented as:

Thai orthography → graphemic analysis → syllable structure → phonology → tone → contextual/surface phonetics → IPA → Ukrainian target → Ukrainian orthography.

### 2. Major technical debt identified

The repository contained committed local/generated debris:

- Python __pycache__ trees;
- compiled .pyc files;
- committed src/*.egg-info packaging metadata;
- a 103 MB generated master CSV;
- a 7 MB generated two-column master CSV.

These are not authoritative research inputs. The master CSVs are deterministic outputs of scripts/generate_master_table.py and are already published by CI as workflow artifacts. They therefore should not remain in the active repository tree.

A repository-level .gitignore is required to prevent recurrence.

### 3. Metadata inconsistency

Before finalization, versions were inconsistent:

- pyproject.toml: 0.5.0
- src/thai_ukrainian/__init__.py: 0.5.0
- README: 0.5.0
- CITATION.cff: 0.4.0
- docs/final-audit.json: 0.2.0
- docs/final-audit.md: 0.4.0

The cleanup aligns machine-readable citation/audit metadata with the declared 0.5.0 software version.

### 4. CI regression found on current main

The latest main-branch CI run before this audit failed in the generated-artifact integrity step.

The failure was not a parser/test failure. The generator produced the same docs/generated-audit.json data with a different dictionary-key order. Because CI uses git diff --exit-code, this serialization-order difference failed the build.

The canonical generated JSON has been synchronized in this cleanup.

### 5. Open work

Two draft PRs were open at audit time:

- PR #10 — orthographic rule engine;
- PR #11 — full orthographic and syllable audit.

The current main branch already contains substantial completion-layer functionality, so these PRs should be reviewed for overlap before further merging. They should not be treated as independent sources of truth.

### 6. Empirical boundary

The repository correctly refuses to claim corpus accuracy. Its validation infrastructure is present, but no declared/versioned gold corpus is processed by CI.

This distinction must remain explicit:

implemented ≠ evidence-supported ≠ empirically validated ≠ normative Ukrainian standard.

## Classification

| Category | Current assessment |
|---|---|
| Core research inputs | data/thai/ and declared evidence/claims |
| Supporting data | Ukrainian target snapshot, corpus-source registry, schemas |
| Implementation | src/, scripts/ |
| Validation | tests/, validation docs, CI |
| Documentation | README.md, docs/ |
| Derived | generated audits, syllable-space report, master tables |
| Historical | docs/superpowers/plans/ and audit history |
| Obsolete/local debris | caches, bytecode, egg-info, oversized generated CSVs |
| Foreign project material | none detected in the active architecture |

## Release gate

The repository should not be labelled publication-ready until:

1. cleanup changes pass CI;
2. the detailed final audit is synchronized with the actual release commit;
3. the two draft PRs are either merged after review or explicitly closed as superseded;
4. the practical Ukrainian rendering layer is represented in machine-readable data rather than only prose;
5. a versioned evaluation corpus is processed if an empirical validation claim is desired.

The current state after this cleanup should therefore be assessed as 🟡 usable but needs finalization, not as empirically validated.
