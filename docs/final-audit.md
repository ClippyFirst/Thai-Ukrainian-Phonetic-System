# Final audit

## Release

**v0.4.0 — research-ready positional model.**

The repository is designed as a coherent research software foundation: source tables are separated from derived artifacts, the transformation layers are explicit, and validation is deterministic. The current HEAD has a successful GitHub Actions CI run.

## Gate A — structural reproducibility

**PASS**

- 44 Thai consonant graphemes are represented explicitly.
- Vowel parsing handles interleaved Thai orthographic sequences and glide-bearing nuclei.
- Tone marks are separated from phonological tones.
- Live/dead classification is explicit.
- Generated audit and syllable-space artifacts are checked by CI.
- Unicode and malformed-input regression tests exist.
- The repository has a regression suite including adversarial probes; the current HEAD is CI-verified.

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

A previous CI run completed successfully before the latest adversarial hardening. The current HEAD is CI-verified by GitHub Actions run 170. The successful run regenerated derived artifacts cleanly and completed 50 tests, including the malformed-surface and preposed-vowel leading-cluster probes.

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


## Completion pass — 2026-10-02

The completion pass closes the remaining **software architecture layers** without pretending that unavailable empirical evidence is already measured.

### Closed in implementation

- tone rules are now machine-readable in `data/thai/tone_rules.csv` and loaded by the tone engine rather than being the sole source of truth in Python;
- special orthography has an explicit registry covering `รร`, `ฤ/ฤๅ`, `ฦ/ฦๅ`, thanthakhat `์`, lexical `ทร`, and `อ นำ`; these cases produce explicit analysis-dependent candidates rather than silent forced IPA;
- lexical segmentation has an explicit external-lexicon adapter; the system still refuses to invent word boundaries when no lexical evidence is supplied;
- the Ukrainian layer now reaches a project-defined orthographic candidate output, while keeping tone separate and marking the output as a research candidate rather than an official Ukrainian standard;
- a generated source→parser→derived manifest checks the 44 consonants, 40 vowel/rime records, parser vowel IDs, four tone marks/five tone states, 38 licensed coda graphemes and the 343,200 structural upper bound;
- CI now checks that the generated source-final manifest and existing derived artifacts remain synchronized.

### Initial-set vs final-set audit

The authoritative inputs remain the machine-readable Thai inventories. The final layer is now checked against those inputs rather than only documenting aggregate counts. In particular, the 40 source vowel IDs must equal the IDs declared by the parser registry; the 44 consonant graphemes and 38 coda-capable graphemes are counted directly from the source table; and the structural syllable-space formula is independently asserted.

### What is still deliberately empirical, not merely architectural

The following cannot honestly be marked as empirically closed without gold data:

- corpus accuracy and lexical coverage;
- calibration of Ukrainian candidate probabilities;
- adjudicated Ukrainian orthographic preference;
- exhaustive connected-speech phonetics;
- universal lexical/morphological coverage of every Thai spelling.

These are now explicit **evidence gates**, not missing software interfaces.

## CI verification — current HEAD

Current HEAD: `56e98433f16e5d267cd0e357f9d572b78256535f`.
GitHub Actions run **170** completed successfully. The workflow regenerated the derived artifacts without diff and completed the full test suite (**50 tests**).


## Adversarial audit extension — malformed syllable surfaces

The parser audit identified another false-positive class: a detector could select one vowel/rime pattern and silently ignore additional vowel signs, additional syllabic material, repeated tone marks, or unsupported symbols. The parser now requires the detected vowel/rime match to consume all vowel-sign material in the supplied syllable surface, rejects multiple tone marks, and rejects unsupported symbols instead of silently discarding them. Regression probes cover repeated vowel signs, concatenated syllable-like material such as `กาเก` and `กากา`, repeated tone marks, ASCII punctuation and Thai repetition mark `ๆ`. These cases are treated as unresolved input rather than assigned invented phonology.


## Adversarial audit extension — preposed-vowel leading clusters

The parser audit exposed a visual-order trap in syllables such as `ไหม` and `ไหว้`: the preposed vowel sign appears before the consonant sequence, so a simple character-index test can incorrectly demote the second onset consonant to coda. The parser now evaluates declared complex-onset licensing in preposed-vowel syllables before the generic coda fallback. The suite verifies `ไหม` as a ห นำ onset and `ไหว้` as a ห นำ onset with a tone mark. The model remains conservative for unsupported lexical leading constructions such as อ นำ.
