# Final audit

## Release

**v0.4.0 — research-ready positional model.**

The repository is designed as a coherent research software foundation: source tables are separated from derived artifacts, the transformation layers are explicit, and validation is deterministic. A fresh CI run is required for the latest HEAD.

## Gate A — structural reproducibility

**PASS**

- 44 Thai consonant graphemes are represented explicitly.
- Vowel parsing handles interleaved Thai orthographic sequences and glide-bearing nuclei.
- Tone marks are separated from phonological tones.
- Live/dead classification is explicit.
- Generated audit and syllable-space artifacts are checked by CI.
- Unicode and malformed-input regression tests exist.
- The repository has a regression suite including adversarial probes; the latest post-audit commits still require a fresh GitHub Actions run before CI-passed status can be asserted.

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
- vowel/rime records: 40;
- structural coda grapheme options: 38;
- tone-mark states: 5;
- open-syllable structural upper bound: 8,800;
- closed-syllable structural upper bound: 334,400;
- combined structural upper bound: 343,200.

These are **combinatorial upper bounds over declared records**, not counts of valid Thai syllables, lexical forms or corpus-attested forms.

## Reproducibility criterion

A clean checkout is release-ready when:

1. package installation succeeds;
2. derived artifacts regenerate without a diff;
3. the complete test suite passes;
4. schemas and documentation agree with the implementation;
5. no empirical claim exceeds the evidence actually processed.

A previous CI run completed successfully before the latest adversarial hardening. The current release must not claim that older run as validation of the newer commits.

## What would change the status

The next status transition is **empirically validated**, not merely “more complete”. It requires an actually processed, named/versioned gold corpus and published error analysis. After that, special orthography, lexical segmentation, connected speech and expert-adjudicated Ukrainian realizations can be evaluated as separate coverage expansions.


## Positional completion — 2026-10-01

The release now includes an explicit word model with syllable index, total count, and standalone/initial/medial/final position metadata. Automatic Thai segmentation is intentionally not inferred without lexical or corpus evidence. Positional metadata is kept separate from phonological rules.


## Adversarial audit — 2026-10-01

The review found and repaired three material parser hazards: generic preposed-vowel rules could shadow longer glide/rime patterns; terminal glides could be counted again as codas after a contextual vowel match; and unsupported implicit vowels were previously defaulted to /a/. The current model instead withholds IPA for unresolved implicit-vowel cases. Invalid tone combinations are surfaced as structured invalid input rather than crashing the general analysis API.

Regression probes now cover `กา`, `กาน`, `กรา`, `ก`, `คน`, `เกะ`, `เก`, `เกีย`, `เกา`, `เกียว`, `แล้ว`, `เร็ว`, `เลย`, `ขาย`, `หงา`, and invalid `ข๊า`, plus correspondence-table coverage and word-position tests.

Special orthography (`รร`, silent letters, `ฤ/ฦ` and related morphology-dependent cases), automatic lexical segmentation, connected speech, and empirical corpus accuracy remain explicitly unclaimed.


## Adversarial audit extension — cluster tone and source-model consistency

The second audit pass found and repaired two additional consistency hazards: the parser recognized 14 glide/rime IDs that were absent from `data/thai/vowels.csv`, and the first written onset class was being reused as the tone-bearing class for every multi-consonant onset. The source registry now declares all parser-recognized glide/rime IDs, and `SyllableAnalysis` carries a separate `tone_class`. For multi-consonant onsets, the current rule uses the first consonant when the second is sonorant and the second consonant when it is non-sonorant; leading-`ห` behaviour remains explicitly represented. This follows the documented Thai cluster-tone distinction in the reference literature. 

The carrier `อ` is no longer licensed as a final coda in the core consonant inventory; its onset role remains the glottal-stop/carrier role. A regression test now prevents it from silently passing as a legal coda.


## Adversarial audit extension — complex-onset licensing

A further parser audit identified a higher-risk false-positive class: treating every adjacent consonant sequence before a vowel as a complex onset. Standard Thai descriptions restrict the second member of complex onsets; the implementation now licenses the declared core cluster structure and otherwise returns an unresolved segmentation status rather than inventing a cluster. The adversarial suite now includes `กล้า` as a licensed cluster and `แสดง` as a deliberately unresolved nonconforming sequence when supplied as a single syllable. This change is a precision/safety improvement, not an empirical accuracy claim.
