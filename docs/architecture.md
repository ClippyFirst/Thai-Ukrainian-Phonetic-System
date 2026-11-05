# Architecture

## Primary phonetic pipeline

Thai orthography → Unicode normalization and graphemic analysis → syllable structure → Thai phonology and tone → typed IPA result → Ukrainian practical adaptation → Ukrainian orthographic candidates.

The layers are intentionally non-collapsible:

1. **Orthography** — normalize Thai Unicode and inspect graphemes, vowel signs, tone marks and special constructions.
2. **Structure** — determine onset, nucleus, coda, syllable position and live/dead status. Thai written vowel order is not phonological order.
3. **Phonology and tone** — compose phonemic IPA and calculate tone from the declared rule environment. Surface phonetics is emitted only where the source/rule evidence supports it.
4. **Typed IPA boundary** — `PhoneticResult` carries phonemic IPA, optional broad surface IPA, segment records, syllable boundaries, tone, length, provenance and uncertainty. Unsupported or uncertain results must not be promoted to a supported Ukrainian output.
5. **Ukrainian practical adaptation** — `ukrainian_adaptation.py` consumes the typed IPA result only. It records applied rules and neutralized features, and withholds output for unsupported IPA.
6. **Secondary target candidates** — `ua_orthography.py` renders project-defined orthographic alternatives from supported typed IPA. `correspondence.py` separately ranks feature-space candidates using `data/ua_target_vectors.csv`; its distance is a model parameter, not a probability or the primary Ukrainian transcription path.

## External phonetic-text corpus boundary

CCOST TextGrid ingestion is a separate, text-only source adapter. It preserves the raw source label, tier, interval and CCOST tone suffixes before producing typed IPA. MAS/KAS/KAN source labels remain provisional; MAU phone-level surface labels cannot independently drive syllable-level Ukrainian adaptation. Unknown X-SAMPA is rejected. The parser reads Praat long-text TextGrid only and never opens paired WAV files. Actual CCOST archive compatibility remains blocked until a lawful TextGrid-only sample is obtained and inspected.

## Separate romanization route

The optional RTGS route is intentionally separate:

Thai orthography → pinned RTGS reference implementation → RTGS Latin sequence → Ukrainian practical rendering of that sequence.

It is not phonetic IPA, ISO 11940 transliteration, or an input to the primary IPA adapter. Tone and some vowel-length distinctions are not represented by RTGS.

## Code ownership

| Concern | Python reference | Browser implementation | Primary data / contract |
|---|---|---|---|
| Thai orthography and syllable parsing | `orthography.py`, `parser.py`, `special.py`, `orthographic_rules.py` | `engine.js`, `vowels.js` | `data/thai/*.csv` |
| Phonology and tone | `phonology.py`, `contextual.py`, `tone.py` | `engine.js` | consonant, vowel, phonotactic and tone registries |
| Typed IPA boundary | `phonetic_result.py`, `models.py` | Browser analysis result contract in `engine.js` | regression fixtures and source provenance |
| Text-only CCOST import | `adapters/ccost.py`, `adapters/xsampa.py` | — | TextGrid tier semantics, strict X-SAMPA → IPA conversion, tone/length/boundaries and source provenance |
| Ukrainian IPA adaptation | `ukrainian_adaptation.py` | `ipa-ua.js` | Explicit project mapping; parity tests |
| Text segmentation | `text.py`, `segmentation.py` | `engine.js` plus generated dictionary index | reviewed text lexicon and pinned CC0 word-boundary list |
| RTGS | Python reference/parity script | `rtgs-reference.js`, `rtgs-ukrainian.js` | pinned RTGS source and method matrices |
| Public interfaces | `api.py`, `batch.py`, `cli.py`, `server.py` | `app.js` | API and UI contract tests |
| Derived research outputs | `scripts/` | generated browser index where applicable | source registries, generators and manifests |

Python and browser modules intentionally implement equivalent logic in separate runtimes; their parity is tested. Do not collapse these modules or move source data without first proving the generated/runtime contract and clean-install behavior.

## Static dependency and test-overlap audit

CI runs `scripts/audit_repository_structure.py` and publishes the `repository-static-dependency-and-test-audit` artifact. The report inventories static Python imports, browser ES-module imports, HTML script/stylesheet references, workflow script references, dynamic-import review sites, Python test functions, browser test files/imports/assertion counts and exact/similar Python test-name candidates. It is a reproducible static graph, not a complete runtime call graph: reflection, indirect calls, generated imports, runtime data flows and dynamically selected assets still require manual tracing. Similar test names are review prompts only; no test is removed without semantic acceptance-contract and coverage evidence.

## Evidence and release boundaries

- Source-attested examples and source-annotated segmentation are not expert-adjudicated gold.
- A lexical IPA override may attest segmental IPA and tone without attesting a separate surface-phonetic transcription; absence remains explicit.
- Structural combinatorial tables are not lexical inventories.
- RTGS output and IPA-first phonetic output must remain separately labelled.
- Engineering CI verifies software contracts, not independent linguistic accuracy or WCAG conformance.


## Test overlap evidence

The static audit reports Python test function names, exact AST-body SHA-256 fingerprints and similar-name clusters. These are candidate-generation aids only: the same body may be valid in different fixtures or modules, and different bodies may still test the same behavior. Review candidates against test intent, fixtures, failure modes, branch conditions and mutation/negative coverage before considering consolidation. No automated deletion or deduplication is performed.
