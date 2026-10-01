# Final audit

## Release

**v0.4.0 — research-ready positional model.**

The repository is internally coherent as a research software foundation: source tables are separated from derived artifacts, the transformation layers are explicit, validation is deterministic, and CI verifies generated state.

## Gate A — structural reproducibility

**PASS**

- 44 Thai consonant graphemes are represented explicitly.
- Vowel parsing handles interleaved Thai orthographic sequences and glide-bearing nuclei.
- Tone marks are separated from phonological tones.
- Live/dead classification is explicit.
- Generated audit and syllable-space artifacts are checked by CI.
- Unicode and malformed-input regression tests exist.
- The test suite passes in GitHub Actions.

## Gate B — linguistic transparency

**PASS for the declared scope; not an exhaustive Thai grammar.**

The system explicitly distinguishes graphemic structure, phonology, tone and IPA. ห นำ is represented as an orthographic dependency rather than incorrectly treating the leading ห as an ordinary onset segment.

The following remain outside the exhaustive-grammar claim:

- all รร constructions;
- all silent-letter conventions;
- all morphology-dependent spelling;
- exhaustive multi-syllable lexical segmentation;
- connected-speech phonetics.

## Gate C — empirical validation

**INFRASTRUCTURE PASS; EMPIRICAL BENCHMARK NOT YET CLAIMED.**

The JSONL evaluator, record schema and CLI are implemented. Metrics have explicit denominators and missing gold labels are excluded from the corresponding metric.

No third-party corpus is bundled or processed by CI. Therefore the project currently publishes **no empirical accuracy percentage**, lexical-coverage percentage or calibrated Ukrainian candidate probability.

This is intentional: a structural upper bound or a hand-selected example set must not be presented as corpus performance.

## Gate D — Ukrainian target layer

**PASS as a candidate-generation layer.**

The system uses a reproducible feature-space target snapshot rather than duplicating the canonical Ukrainian inventory. Candidate ranking is heuristic/feature-based and is not represented as probability.

A final Ukrainian orthographic rendering remains a separate research decision and is not assumed to be uniquely determined by phonetic similarity.

## Quantitative audit

The generated structural syllable-space report currently gives:

- initial grapheme options: 44;
- vowel records: 26;
- structural coda options: 44;
- tone-mark states: 5;
- open-syllable structural upper bound: 5,720;
- closed-syllable structural upper bound: 251,680;
- combined structural upper bound: 257,400.

These are **combinatorial upper bounds over declared records**, not counts of valid Thai syllables, lexical forms or corpus-attested forms.

## Reproducibility criterion

A clean checkout is release-ready when:

1. package installation succeeds;
2. derived artifacts regenerate without a diff;
3. the complete test suite passes;
4. schemas and documentation agree with the implementation;
5. no empirical claim exceeds the evidence actually processed.

The current CI run for commit 3e2617418e8b4423700866d4c675ec24f0fe5e27 completed successfully; the repository test suite reported 26 passing tests.

## What would change the status

The next status transition is **empirically validated**, not merely “more complete”. It requires an actually processed, named/versioned gold corpus and published error analysis. After that, special orthography, lexical segmentation, connected speech and expert-adjudicated Ukrainian realizations can be evaluated as separate coverage expansions.


## Positional completion — 2026-10-01

The release now includes an explicit word model with syllable index, total count, and standalone/initial/medial/final position metadata. Automatic Thai segmentation is intentionally not inferred without lexical or corpus evidence. Positional metadata is kept separate from phonological rules.
