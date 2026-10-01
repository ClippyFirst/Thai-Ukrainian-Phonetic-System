# Changelog

## [0.4.0] - 2026-10-01

### Adversarial hardening

- Fixed longest-match shadowing for complex Thai vowel/glide rimes.
- Prevented multi-grapheme rimes such as /iaw/ from leaking nucleus consonants into onset/coda analysis.
- Removed unsupported implicit-/a/ guessing; unresolved implicit vowels now withhold IPA until lexical/morphological evidence exists.
- Corrected the negative tone regression to use the genuinely invalid high-class + mai tri combination `ข๊า`.
- Made the syllable analysis JSON Schema strict and aligned with the runtime model.

- Added explicit word analysis with syllable positions: standalone, initial, medial, final.
- Added positional regression tests.
- Added a documented methodological boundary: automatic Thai word/syllable segmentation is not silently guessed.
- Preserved the distinction between positional metadata and position-dependent phonological rules.


## 0.3.0 — 2026-10-01

### Added

- Research-grade Thai graphemic, phonological, tone and IPA pipeline foundation.
- Feature-based Ukrainian candidate ranking layer.
- Evidence and provenance registries.
- Structural syllable-space accounting with explicit upper-bound semantics.
- JSONL corpus evaluation API and CLI.
- Machine-readable corpus-record schema.
- Deterministic generated-artifact checks in CI.
- Negative/regression tests for Thai vowel, glide, coda and ห นำ behaviour.
- `CITATION.cff` and MIT license metadata.

### Explicitly not claimed

- Exhaustive lexical segmentation of arbitrary Thai text.
- Complete special-orthography coverage (`รร`, silent letters and all morphology-dependent cases).
- Connected-speech narrow phonetics.
- Corpus-derived accuracy or calibrated probabilities.
- A single universally correct Ukrainian orthographic realization.
