# Thai: IPA benchmarking and external systems

**Status: benchmark harness added; empirical accuracy remains unmeasured until independently adjudicated gold rows exist.** This is not a claim that candidate engines have been installed, run, licensed for redistribution, or validated for Thai.

## Required pipeline boundary

source orthography → structural analysis → source-language phonology → typed IPA → ClippyFirst IPA-to-Ukrainian adapter → Ukrainian practical orthography

External engines are comparators or optional upstream IPA providers only. Preserve their raw output separately from any normalized IPA. Do not bypass the ClippyFirst IPA adapter, silently rewrite an engine's proprietary phoneme alphabet as IPA, or treat agreement among engines as ground truth.

## Reproducible benchmark

The standard-library-only harness is scripts/benchmark_ipa.py. It reads tab-separated files:

- Gold columns: id, text, gold_ipa, gold_status, profile, source_id.
- Prediction columns: id, engine, raw_output, ipa, status, version.

Run from the repository root:

python scripts/benchmark_ipa.py --gold data/benchmark/gold.tsv --predictions data/benchmark/predictions.tsv --output reports/ipa-benchmark.json

Only rows with gold_status=ADJUDICATED and non-empty gold IPA enter the denominator. For each engine, every eligible gold row is counted: an absent prediction row or empty IPA is a miss and remains in the denominator. The report provides strict NFC exact match, missing-prediction rate, and code-point Levenshtein CER. NFC and outer whitespace trim are the only normalizations: tone, vowel length, diacritics, and syllable separators remain significant. Code-point CER is a diagnostic, not a feature-weighted phonetic metric. A header-only gold file correctly yields NOT_MEASURED, not a fabricated zero or 100% score. An engine with no predictions for eligible gold rows is not scored; once an engine appears in the prediction file, omitted eligible IDs count as missing.

Stratify gold cases by syllable shape, consonant class/series, vowel type and length, coda, tone/prosody where applicable, morphology, lexical/loanword status, and uncertainty. Report the denominator and source/profile per row. Avoid training/test leakage and use a held-out set for any tuning.

## External candidates (not yet approved for runtime)

- thaiphon
- FastThaiG2P
- PyThaiNLP (supporting NLP
- not assumed to produce IPA)
- eSpeak NG (diagnostic candidate only)

These are research leads, not verified availability claims. Before executing a candidate, record the exact release/commit, installation command, language/voice/model identifier, raw output, runtime errors, license for code plus model/dictionary/data, and whether the output is actual IPA or a tool-specific phone alphabet. Do not install or enable a candidate by default merely because it appears here.

## Acceptance gates

1. Build a versioned gold set from cited primary sources with exact page/section/audio locator, dialect/profile, and independent adjudication; Unicode tables alone do not establish pronunciation.
2. Keep raw source output immutable; store conversion rules and normalized output separately.
3. Run the same inputs/profile through ClippyFirst and each available candidate; preserve failed/missing outputs in the denominator report.
4. Evaluate both strict IPA exact match and reviewed feature-level errors (tone, vowel length/quality, onset, coda, syllable boundaries). Do not infer a winner from exact match alone.
5. Run the existing repository test/CI suite and validate the benchmark script on a synthetic fixture; do not publish synthetic scores as language accuracy.
6. Keep candidates optional, pinned, license-reviewed, and fail-closed. A missing tool must never change the core result silently.

## Current evidence status

- Harness baseline: executed successfully in prior main CI. Additional fail-closed validation now requires every ADJUDICATED row to have non-empty IPA, source_id and profile; PR #35 adds regression tests for these gates and must pass CI on its final head.
- Adjudicated language-specific gold rows: not yet established by this document.
- Candidate engine availability, version, licenses, and language-specific output quality: unverified until recorded as run evidence.
- Release status: research prototype; no accuracy claim is authorized by this registry.

## Existing external run evidence (reconciled 2026-10-24)

- Latest smoke: [workflow 40119612565](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40119612565), `thaiphon==0.7.0` (base engine; optional VOLUBILIS lexicon absent) and FastThaiG2P 0.1.0 at commit `c4759eef7df03e11fcbb9aa83efe8cf21709fd2f`; 36 engineering inputs × 2 engines = 72 outputs, zero runtime errors, zero independently adjudicated gold labels. Artifact ZIP SHA-256 `b7232dbd508cd6244503005eb41974c090f8f5cc569fd2407f525dcda6216049`. `ไกล`: thaiphon `/kaj˧/ /la˦˥/` vs FastThaiG2P `/klaj˧/`; `จริง`: thaiphon `/tɕa˨˩/ /ri˦˥/ /ŋa˦˥/` vs FastThaiG2P `/t͡ɕiŋ˧/`. These are high-priority lexical/segmentation discrepancies, not an accuracy ranking.
- Upstream [thaiphon](https://github.com/5w0rdf15h/thaiphon) reports ~57% exact match for the base engine and ~75% with `thaiphon-data-volubilis` on its own Wiktionary-derived etalon; it reports ~73% on a PyThaiNLP G2P cross-check. These are upstream-reported figures, not reproduced here and not comparable to ClippyFirst's 36-item smoke. Engine code is Apache-2.0; the optional lexicon is separately CC-BY-SA 4.0.
- [FastThaiG2P](https://github.com/awslabs/FastThaiG2P) documents a 62,112-word IPA dictionary and rule-based OOV fallback; dictionary provenance includes manually curated, Wiktionary-derived and generated entries. Review per-source provenance and license before treating any material as gold.
- [Goruut](https://github.com/neurlang/goruut) lists Thai support upstream; no pinned Goruut run is yet recorded.
- Current acceptance: build a shared held-out gold set and map IPA conventions before comparing exact-match rates.

## Source-attested Thai spot-check (not gold, 2026-10-24)

A three-word targeted spot-check was added to `data/benchmark/runs/external-g2p-smoke-2026-10-24.json` using the standard-IPA fields in the Thai Wiktionary pronunciation sections:

- [กา](https://th.wiktionary.org/wiki/กา): `/kaː˧/`; both engines' raw strings match.
- [ไกล](https://th.wiktionary.org/wiki/ไกล): `/klaj˧/`; FastThaiG2P matches; thaiphon outputs `/kaj˧/ /la˦˥/`.
- [จริง](https://th.wiktionary.org/wiki/จริง): `/t͡ɕiŋ˧/`; FastThaiG2P matches; thaiphon outputs `/tɕa˨˩/ /ri˦˥/ /ŋa˦˥/`.

Diagnostic string-concordance is 3/3 for FastThaiG2P and 1/3 for thaiphon on these selected cases. **Do not report this as accuracy**: this is a disagreement-selected sample, Wiktionary entries are source-attested but not independently expert-adjudicated here, and both upstream systems may overlap with Wiktionary-derived resources. It is useful for prioritizing segmentation/lexical review, not selecting a winner. Preserve the raw outputs and inspect tie-bar/segmentation conventions before normalization.


Attribution/license: the spot-check records Wiktionary contributors and source URLs in the JSON report. Wiktionary content is generally available under CC BY-SA 4.0; recheck the page footer and applicable terms before redistributing any larger excerpt or dataset. No bulk Wiktionary data was copied into this repository.


## Upstream provenance, license boundaries and comparator triage (checked 2026-10-24)

| Candidate | Verified upstream fact | Evidence boundary / next step |
|---|---|---|
| [thaiphon 0.7.0](https://pypi.org/project/thaiphon/0.7.0/) | PyPI declares Apache-2.0. Upstream reports 57% exact match for the base engine and about 75% with optional thaiphon-data-volubilis; the lexicon is a separate CC-BY-SA 4.0 package. These are upstream-reported figures, not this repository's measurements. | Our smoke intentionally ran the base engine without the optional lexicon. Do not compare its output directly to the upstream 57%/75% claims without reproducing the exact upstream corpus, lexicon, version and scoring convention. |
| [FastThaiG2P](https://github.com/awslabs/FastThaiG2P) | Upstream describes a 62k-entry IPA dictionary and a rule-based fallback; its README attributes dictionary content to Wiktionary, manual overrides and generated entries, including model-generated data. | Our pinned smoke ran 36 inputs / 72 outputs, but independent gold count is zero. Its dictionary can overlap with Wiktionary-derived comparator labels, so concordance on the three selected Wiktionary spot checks is not independent accuracy. Audit the license of the code and each bundled dataset separately before redistribution. |
| [Epitran](https://github.com/dmort27/epitran) | General IPA transliteration toolkit; only use a language-script pair if its current mapping inventory explicitly supports it. | Not part of the current Thai smoke evidence; verify the exact Thai pair before adding it as a comparator. |
| [Goruut](https://github.com/neurlang/goruut) | Upstream advertises an IPA phone set and Thai support. | Support claim only; no successful Thai run recorded here. |

The source-attested spot check in data/benchmark/runs/external-g2p-smoke-2026-10-24.json is selected to investigate disagreements, not sampled to estimate accuracy. Keep raw strings, tone marks, tie bars and segmentation intact until a declared normalization protocol is reviewed.

