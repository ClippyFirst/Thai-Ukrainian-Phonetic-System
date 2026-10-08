# Changelog

## 2026-10-08 — v0.5.1 transliteration hardening

- Fixed a real false-positive class in the Thai parser: จร, สร, ศร and ซร are now evidence-gated special orthography rather than ordinary consonant clusters.
- Added regression coverage for established forms such as จริง, สร้าง, เศร้า and ไซร้; IPA and Ukrainian output are withheld until lexical evidence resolves the reading.
- Corrected the documented and tested analysis of ไกล /klaj/: ล is the second member of the true onset cluster /kl/, not a final coda.
- Added ไกล, ใกล้ and ไก่ parity probes to protect preposed-vowel onset and tone behaviour.
- Aligned the browser tone-bearing consonant selection with the Python cluster-tone rule.
- Synchronized browser false-cluster rules with the machine-readable special-orthography registry.

## 2026-10-02 — master correspondence table

- Added deterministic IPA-first generation of the full declared structural space (343,200 rows).
- Added a rich research CSV and a derived two-column `Thai | Ukrainian` presentation CSV.
- Added a generation manifest and CI artifact publication; generated tables remain reproducible rather than being maintained as a hand-written lookup list.

## 2026-10-02 — v0.4.0 completion pass

- Moved tone rules into a machine-readable registry consumed by the tone engine.
- Added explicit analysis-dependent handling for special Thai orthography.
- Added an external lexicon adapter for evidence-backed syllable segmentation.
- Added a project-defined Ukrainian orthographic candidate layer with tone kept separate.
- Added source → parser → derived consistency checks and CI enforcement.
- Added completion-layer adversarial tests.
- Final clean CI gate: run 213, 57 tests, generated artifacts synchronized.

## [0.4.0] - 2026-10-01

### Adversarial hardening

- Fixed longest-match shadowing for complex Thai vowel/glide rimes.
- Prevented multi-grapheme rimes such as /iaw/ from leaking nucleus consonants into onset/coda analysis.
- Removed unsupported implicit-/a/ guessing; unresolved implicit vowels now withhold IPA until lexical/morphological evidence exists.
- Corrected the negative tone regression to use the genuinely invalid high-class + mai tri combination `ข๊า`.
- Made the syllable analysis JSON Schema strict and aligned with the runtime model.
- Declared all parser-recognized glide/rime IDs in the machine-readable vowel registry.
- Added a separate tone-bearing consonant class for cluster tone calculation.
- Removed final-coda licensing from carrier `อ` and added a regression guard.
- Restricted complex-onset parsing to structurally licensed Thai onset patterns; arbitrary adjacent consonants are now unresolved instead of being forced into a cluster.
- Added adversarial coverage for a licensed cluster (`กล้า`) and a nonconforming sequence (`แสดง`).

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


### Post-audit CI repair

- Fixed the preposed consonant-plus-glide matcher for forms such as `เลย`, which had been shadowed by the generic `เ{C}` vowel pattern.
- GitHub Actions run 156 verifies the current HEAD with generated-artifact checks and 44 tests.
