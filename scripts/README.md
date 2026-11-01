# Script inventory and ownership

This directory contains project tooling, not production runtime modules. Scripts are grouped by the artifact or research question they own. Keep generators, diagnostics, evaluators and release checks separate: similar-looking inputs do not imply interchangeable evidence or output contracts.

## Registry and artifact builders

| Script | Responsibility | Inputs → outputs / contract |
|---|---|---|
| `generate_derived.py` | Run structural repository validation and build the source-final manifest | Thai registries → `docs/generated-audit.json`, `docs/source-final-manifest.json`; generated files must be refreshed through this script |
| `generate_syllable_space.py` | Count the structural combinatorial space | Consonant, vowel and tone registries → `docs/syllable-space.json`; explicitly not a lexical inventory |
| `generate_master_table.py` | Build exhaustive derived correspondence tables | Thai registries and parser/IPA adapter → rich and two-column CSV plus JSON report under `data/derived/`; generated research artifact, not a runtime lexicon |
| `generate_web_word_dictionary.py` | Build the browser's compact word-boundary prefix index | Pinned CC0 word list and source manifest → ignored/generated `web/src/word-dictionary.generated.js`; boundary data only, no IPA or Ukrainian output |
| `generate_web_fixtures.py` | Refresh Python-produced browser parity fixtures | Curated Thai probes through Python API → `web/tests/fixtures.python.json`; use when intentionally refreshing parity fixtures |
| `build_word_segmentation_dictionary.py` | Reconstruct the pinned Thai word list | Exact upstream source snapshot with expected Git blob hash → `data/thai/words_th_cc0.txt`; refuses unpinned source data |
| `build_ukrainian_target_candidates.py` | Build or check the source-attested IPA → Ukrainian candidate registry | `data/benchmark/source-attested-ipa.tsv` → `data/benchmark/ukrainian-target-candidates.tsv`; candidates are adapter outputs, not native-speaker gold |

## Evaluation and external engine research

| Script | Responsibility | Evidence boundary |
|---|---|---|
| `benchmark_ipa.py` | Compare submitted IPA predictions with a supplied TSV | `ADJUDICATED` rows require two distinct reviewers, both raw IPA labels, adjudicator/outcome/record, transcription layer and source/license provenance; mixed phonemic/surface runs are rejected and metrics are stratified by profile |
| `evaluate_corpus.py` | CLI wrapper around the package's generic corpus evaluator | Uses the record schema accepted by `thai_ukrainian.evaluation` |
| `evaluate_segmentation.py` | Word- or syllable-boundary scorer | `ADJUDICATED` rows require two independent tokenizations, adjudicator/outcome/record and source/license provenance; WORD and SYLLABLE layers cannot be mixed; source-annotated rows remain separately labelled |
| `evaluate_vistec_segmentation.py` | Adapt the pinned VISTEC-TP-TH-2021 annotation format | Source-annotated segmentation, not independently re-adjudicated gold; pinned source commit, blob and license are checked |
| `run_external_g2p_benchmark.py` | Query optional external Thai G2P engines and capture raw outputs | Research-only comparator; score only independently adjudicated gold IPA rows; engine/network availability is external |
| `probe_goruut_repeatability.py` | Repeat remote Goruut requests to inspect output stability | Repeatability diagnostic, not accuracy; requires an explicitly supplied service URL |
| `validate_adjudication_packet.py` | Validate blank, single-reviewer and paired Thai phonetic review packets | Exact challenge coverage, candidate-blind fields, reviewer qualification/date, syllable-aligned tone/length/glottal labels, explicit abstention and audio intervals |
| `validate_ukrainian_preference_packet.py` | Validate blind and paired Ukrainian-native preference reviews | Source-bound IPA references, no engine candidate, fixed criteria version, reviewer qualification, rationale and explicit abstention; judgments remain conditional, not gold |

## Runtime and segmentation diagnostics

| Script | Responsibility | Output / evidence boundary |
|---|---|---|
| `run_challenge_diagnostics.py` | Run the authored text engine on the challenge set | Runtime coverage and abstention diagnostics; no accuracy score because challenge inputs lack adjudicated gold |
| `run_source_attested_ipa_diagnostic.py` | Compare source-attested dictionary IPA with the current text pipeline | Discrepancy/abstention report; source-attested is not expert gold |
| `run_wisesight_segmentation_diagnostic.py` | Establish a no-automatic-word-segmentation baseline | Diagnostic against source-annotated Wisesight rows; not expert-adjudicated gold |
| `run_dictionary_segmentation_diagnostic.py` | Evaluate the pinned dictionary max-match segmenter on Wisesight | Same source-annotated evidence grade; not phonetic accuracy |
| `analyze_segmentation_errors.py` | Produce deterministic false-split/false-merge triage | Error review on pinned CC0 source-annotated rows; triage, not adjudication |
| `train_tud_word_segmenter.py` | Train and evaluate a reproducible unigram/Viterbi research segmenter | Pinned UD Thai TUD train/dev/test sources; Wisesight is evaluation-only and must not be used for fitting/tuning |
| `compare_segmentation_error_review.py` | Compare dictionary and TUD errors on identical rows | Comparative triage on source-annotated Wisesight rows; not release-quality accuracy |
| `build_segmentation_manual_review.py` | Create a deterministic stratified human-review sample | Comparative report + TUD model → TSV sample; rows remain unadjudicated until human decisions are recorded |
| `benchmark_web_segmentation.mjs` | Measure browser Thai segmentation latency | Non-gating, environment-specific timing diagnostic; not accuracy or a release claim |

## Parity and packaging checks

| Script | Responsibility | Required environment / result |
|---|---|---|
| `test_rtgs_parity.py` | Compare browser RTGS implementation with pinned PyThaiNLP 5.4.0 | Python + Node; per-token implementation parity, not tokenizer parity or linguistic correctness |
| `wheel_install_smoke.py` | Exercise runtime registries and CLI from an installed wheel outside the checkout | Must run in the isolated wheel environment; verifies packaged data, API and console entry point |

## Workflow and change rules

- The authoritative default CI commands are in [`.github/workflows/ci.yml`](../.github/workflows/ci.yml). A script not invoked there is not implicitly verified by the default CI.
- Pages and optional research workflows may invoke additional scripts; inspect the owning workflow before changing their arguments or outputs.
- Before changing a generator, identify its canonical input, output paths, tests and downstream consumers. Never hand-edit its generated artifacts.
- Before changing an evaluator, preserve its evidence-grade and denominator rules. Source-annotated, source-attested and adjudicated records must not be silently mixed.
- Keep optional network-dependent probes out of the production runtime and default release path unless a separate decision explicitly changes that boundary.
- Current inventory: **26 scripts**. Scripts are not interchangeable merely because they consume the same corpus: baseline, dictionary, TUD, and error-triage runs answer different questions.
