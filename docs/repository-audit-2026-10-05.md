# Repository audit — 2026-10-05

The repository separates authoritative Thai data, implementation, validation, documentation and derived artefacts. The 2026-10-05 finalization identified committed local debris (Python caches, bytecode and generated package metadata) and oversized deterministic generated CSVs as material technical debt; local Python caches and package metadata are now removed from the active branch, while large deterministic tables remain CI-generated artifacts.

The current release metadata is aligned to **v0.5.1**. The project explicitly distinguishes implemented rules, evidence-supported claims, empirical validation and normative Ukrainian standards.

The web product layer is a presentation/runtime implementation of the research core. Browser/reference parity is enforced by fixtures and CI; the web interface must not become an independent linguistic source of truth.

Empirical corpus accuracy remains not claimed because no versioned gold corpus is processed by CI. Structural exhaustive generation is not lexical attestation.

Release classification: **research-ready software infrastructure + publication-ready static service UI**, with GitHub Pages activation remaining an operational repository setting rather than a code defect.

## 2026-10-08 final product-polish pass

The Service page now makes the input contract explicit, supports keyboard analysis with Ctrl/⌘ + Enter, gives quick examples immediate feedback, exposes result headings for assistive technology, and distinguishes deterministic results from analysis-dependent/unresolved/invalid states without presenting a warning as a successful transcription.

The System page now includes a compact status guide so a reader can understand why IPA/Ukrainian output may intentionally be absent. The visual system remains deliberately editorial and functional: deep blue structure, restrained red for attention/uncertainty, white field, strong typography and no third-party runtime dependencies.

A full screenshot-based Product Design browser audit is still not claimed in this record because the required browser capture surface was unavailable. Static HTML/CSS/JS and accessibility-contract review remain the supported evidence for the web layer.
