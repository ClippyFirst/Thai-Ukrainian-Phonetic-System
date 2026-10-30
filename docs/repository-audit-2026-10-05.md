# Repository audit — 2026-10-05

The repository separates authoritative Thai data, implementation, validation, documentation and derived artefacts. The 2026-10-05 finalization identified committed local debris (Python caches, bytecode and generated package metadata) and oversized deterministic generated CSVs as material technical debt; local Python caches and package metadata are now removed from the active branch, while large deterministic tables remain CI-generated artifacts.

Metadata is aligned to software version 0.5.0. The project explicitly distinguishes implemented rules, evidence-supported claims, empirical validation and normative Ukrainian standards.

The current PR #14 branch consolidates the web product layer with the research core and keeps the research/audit boundary explicit.

Empirical corpus accuracy remains not claimed because no versioned gold corpus is processed by CI. Structural exhaustive generation is not lexical attestation.

Release classification: research-ready software infrastructure; web productization remains a separate generated presentation layer.
