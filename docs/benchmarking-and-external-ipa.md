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

- [กา](https://th.wiktionary.org/w/index.php?title=กา&oldid=5734858): `/kaː˧/`; both engines' raw strings match.
- [ไกล](https://th.wiktionary.org/w/index.php?title=ไกล&oldid=5688545): `/klaj˧/`; FastThaiG2P matches; thaiphon outputs `/kaj˧/ /la˦˥/`.
- [จริง](https://th.wiktionary.org/w/index.php?title=จริง&oldid=2441036): `/t͡ɕiŋ˧/`; FastThaiG2P matches; thaiphon outputs `/tɕa˨˩/ /ri˦˥/ /ŋa˦˥/`.

Diagnostic string-concordance is 3/3 for FastThaiG2P and 1/3 for thaiphon on these selected cases. **Do not report this as accuracy**: this is a disagreement-selected sample, Wiktionary entries are source-attested but not independently expert-adjudicated here, and both upstream systems may overlap with Wiktionary-derived resources. It is useful for prioritizing segmentation/lexical review, not selecting a winner. Preserve the raw outputs and inspect tie-bar/segmentation conventions before normalization.


Attribution/license: the spot-check records Wiktionary contributors and source URLs in the JSON report. Wiktionary content is generally available under CC BY-SA 4.0; recheck the page footer and applicable terms before redistributing any larger excerpt or dataset. No bulk Wiktionary data was copied into this repository.


## Upstream provenance, license boundaries and comparator triage (checked 2026-10-24)

| Candidate | Verified upstream fact | Evidence boundary / next step |
|---|---|---|
| [thaiphon 0.7.0](https://pypi.org/project/thaiphon/0.7.0/) | PyPI declares Apache-2.0. Upstream reports 57% exact match for the base engine and about 75% with optional thaiphon-data-volubilis; the lexicon is a separate CC-BY-SA 4.0 package. These are upstream-reported figures, not this repository's measurements. | Our smoke intentionally ran the base engine without the optional lexicon. Do not compare its output directly to the upstream 57%/75% claims without reproducing the exact upstream corpus, lexicon, version and scoring convention. |
| [FastThaiG2P](https://github.com/awslabs/FastThaiG2P) | Upstream describes a 62k-entry IPA dictionary and a rule-based fallback; its README attributes dictionary content to Wiktionary, manual overrides and generated entries, including model-generated data. | Our pinned smoke ran 36 inputs / 72 outputs, but independent gold count is zero. Its dictionary can overlap with Wiktionary-derived comparator labels, so concordance on the three selected Wiktionary spot checks is not independent accuracy. Audit the license of the code and each bundled dataset separately before redistribution. |
| [Epitran](https://github.com/dmort27/epitran) | General IPA transliteration toolkit; only use a language-script pair if its current mapping inventory explicitly supports it. | Not part of the current Thai smoke evidence; verify the exact Thai pair before adding it as a comparator. |
| [Goruut](https://github.com/neurlang/goruut) | Upstream advertises an IPA phone set and Thai support; pinned commit `b224bde02151f8f86d0fe260804e4ca743bda620` ran successfully in the optional smoke workflow. | Execution is verified, but output-format/coverage suitability is not: 26/36 non-empty outputs, 10 per-input failures, and raw strings differ materially from the other engines. No independent gold exists. |

The source-attested spot check in data/benchmark/runs/external-g2p-smoke-2026-10-24.json is selected to investigate disagreements, not sampled to estimate accuracy. Keep raw strings, tone marks, tie bars and segmentation intact until a declared normalization protocol is reviewed.



## Diagnostic decomposition of inter-engine disagreement (2026-10-24)

The optional smoke report now compares engines per shared input and reports raw exact agreement alongside a separate tone-letter-stripped diagnostic. The diagnostic removes only `˥ ˦ ˧ ˨ ˩`; it does not alter raw outputs, scoreable output strings, syllable separators, vowel length or tie bars. It classifies tone-only disagreement separately from segmental/format disagreement requiring review. These are **inter-engine diagnostics, not accuracy**: neither engine is gold and the 36-case challenge has no independently adjudicated gold labels.




## Benchmark metric semantics — 2026-10-24

- `exact_match_rate` is strict string equality after the declared Unicode normalization and is comparable only when the same IPA profile/conventions are used. Tone, length, stress, syllable boundaries, tie bars and other IPA distinctions are not silently removed.
- `character_error_rate` is Levenshtein distance over Unicode code points, not a phoneme/segment error rate. IPA affricates, combining diacritics, length marks and tone symbols can occupy multiple code points; interpret this field as a string-distance diagnostic only.
- A valid score still requires a non-empty independently adjudicated gold set with source locator and profile. Smoke output, engineering fixtures, source-attested but unadjudicated entries, and inter-engine agreement are not accuracy.


## Goruut: pinned third-engine diagnostic

The optional external-G2P workflow builds Goruut from pinned upstream commit `b224bde02151f8f86d0fe260804e4ca743bda620` and queries the Thai endpoint alongside `thaiphon` and FastThaiG2P. The pinned smoke completed, but output-convention and coverage suitability remain unverified: see the latest inspected run below. The upstream repository reports MIT, but per-language dictionary/model data provenance and licenses are not independently audited. Goruut is not a product-runtime dependency. Preserve raw outputs; engine agreement is not accuracy, and tone-stripped agreement remains diagnostic only.



## Latest inspected Goruut smoke — 2026-10-24

Pinned run [40128121032](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40128121032) built and started Goruut successfully and processed all 36 challenge inputs. The artifact contains 108 rows: thaiphon 36/36 non-empty outputs, FastThaiG2P 36/36, and Goruut 26/36 non-empty outputs with 10 per-input errors. The pairwise diagnostic reports 88 comparable engine pairs, 13 exact-agreement pairs, 14 tone-stripped agreement pairs (diagnostic only), 1 tone-only disagreement, and 74 non-tone/format disagreements. Artifact ZIP SHA-256: `83cde4269dad940ef3d2521b6aba0b8f22eda56f71ec3612bb7230f6274f5b6b`.

Inspecting the raw output revealed convention/coverage concerns: for กา, thaiphon and FastThaiG2P emit `/kaː˧/`, while Goruut emits `ka`; several multi-syllable strings have no explicit separators, and some responses return an empty `Words` array. These are output-format and coverage observations, not adjudicated phonological errors. The output should not be assumed to be directly comparable standardized IPA without a documented convention adapter. The engine remains optional and disabled by default; `verified_in_repo` remains false, `independent_gold_count` remains 0, and `accuracy` remains null.

The benchmark harness was also tightened so an empty string is not counted as a successful smoke output, per-input failures are included in the summary's error list, and a run exits non-zero if all recorded outputs are unusable. Current-head CI and smoke verification are pending for the latest code changes.


## Goruut repeatability

The endpoint readiness probe returned `kaː˧` for `กา`, while the first benchmark artifact recorded `ka` for the same form. Because these requests occurred in different contexts, this is a repeatability hypothesis rather than proof of stochastic output. The optional workflow now repeats each challenge form three times and preserves raw outputs plus Goruut's randomization counters. A stable output is not evidence of correctness; variability must be analyzed separately from accuracy.


## First pinned three-engine run: coverage and disagreement decomposition

The first pinned run [40128121032](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40128121032) processed 36 inputs across `thaiphon`, FastThaiG2P and Goruut. `thaiphon` and FastThaiG2P each returned 36/36 non-empty outputs; Goruut returned 26/36 and 10 responses with an empty `Words` array. This is partial coverage, not an accuracy score.

Across the 88 valid engine pairs, raw exact agreement was 13/88 (14.8%). Removing only IPA `/` transcription delimiters raises diagnostic agreement to 21/88 (23.9%); removing those delimiters and IPA tone-letter symbols raises it to 24/88 (27.3%). The latter decomposes as 8 wrapper-format-only additional matches and 3 additional tone-only matches; 64 pairs still differ after these limited diagnostics. Pairwise: `thaiphon` vs FastThaiG2P 13/36 raw and 14/36 after tone-letter stripping; `thaiphon` vs Goruut 0/26 raw, 2/26 after delimiter removal, 3/26 after delimiter+tone removal; FastThaiG2P vs Goruut 0/26 raw, 6/26 after delimiter removal, 7/26 after delimiter+tone removal. These are convention/disagreement diagnostics only, never accuracy.

The workflow now reports per-engine failures and repeats each input three times to investigate possible Goruut output variability. The readiness request returned `kaː˧` for `กา`, whereas the first benchmark row recorded `ka`; this cross-request difference is a repeatability hypothesis pending the repeated-call report.

The harness now emits `pairwise_engine_diagnostic` for each engine pair, including its own comparable-input denominator and raw/slash-stripped/slash+tone-stripped counts. This avoids mixing missing-output coverage across engine pairs.

## CI regression found and corrected — 2026-10-24

Full CI run [40129230638](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40129230638) reached the Python suite and failed one of 108 tests: `test_candidates_have_unique_ids_and_valid_https_links` rejected Goruut's custom `status` value `SMOKE_VERIFIED_PARTIAL_COVERAGE_NOT_ACCURACY`. The repository schema deliberately restricts `status` to `candidate`, `benchmark-resource`, `supporting-tool`, or `display-only`. Corrected the registry to use `status: candidate` and moved the execution classification to `execution_status`; this preserves the evidence distinction while respecting the existing schema. The exact corrected head must pass CI before the PR can be merged. The failure was a registry-schema regression, not a pronunciation or engine runtime failure.

## Repeatability artifact and test-runner contract — 2026-10-24

The optional workflow's artifact manifest now includes both the full repeated-call report (`goruut-repeatability.json`) and its CLI summary (`repeatability-summary.json`). The CLI now writes the report-path notice to stderr so stdout captured by `tee` remains valid JSON. Regression tests also use `unittest.TestCase`: this repository's CI runs `python -m unittest discover -s tests -v`, which does not execute bare pytest-style test functions. The test now checks that the CLI stdout and saved report parse as JSON and that repeated outputs/errors are summarized without an accuracy claim. These changes require a fresh exact-head CI and smoke artifact inspection; previous smoke artifacts do not contain the repeated-call files.

## Latest verified three-engine and repeatability artifact — 2026-10-24

Current inspected optional smoke run [40130130705](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40130130705), artifact [12575022202](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40130130705/artifacts/12575022202), ZIP SHA-256 `88693eb1e85b9957c86aa2e04993dd30d8749d58dd39d7074437c7d2bdc73d16`. The archive includes `external-g2p-latest.jsonl`, `summary.json`, `goruut-repeatability.json`, and `repeatability-summary.json`; all three JSON files parse successfully in this run. The benchmark has 36 inputs / 108 rows: thaiphon 36/36 non-empty, FastThaiG2P 36/36, Goruut 26/36 with 10 no-`Words` responses. Pairwise comparison reports 88 pairs, 13 exact agreements, 28 slash-stripped and 31 slash+tone-stripped diagnostic agreements, and 57 remaining mismatches. These are not accuracy scores; independent gold remains zero.

The repeatability probe made 108 requests (36 forms × 3). It observed 78 non-empty calls, 30 no-output calls and zero transport/runtime exceptions. For 26 forms with at least two non-empty outputs, 15 varied across the three attempts and 11 were stable in this small sample; observed repeatability is therefore 11/26 = 42.3% under this probe's definition. Ten inputs yielded no non-empty output in all three attempts. Every one of the 15 variable forms had `RandomizationWordsCount=1` and `RandomizationWordsChoices` from 2 to 4. Examples include `กา` → `kaː˥` / `kaː˧`, `ไกล` → `flaj˧` / `klaj˧`, `จริง` → `tɕiŋ˧` / `ʈʐiŋ˧`, and `กรรม` with three distinct outputs. The earlier run showed 14/26 variable; the changed count across runs itself demonstrates why single-run engine comparisons are not stable evidence.

The pinned upstream selector source [`parts_of_speech_selector_service.go`](https://github.com/neurlang/goruut/blob/b224bde02151f8f86d0fe260804e4ca743bda620/repo/services/parts_of_speech_selector_service.go) increments its randomization counters when multiple dictionary pronunciations are present and comments that, absent a preferred homograph result, the fallback selects a random dictionary pronunciation. This source behavior is consistent with the observed variation: all 15 variable forms had the counters set. It does not tell us which candidate is linguistically correct. Treat Goruut's current output as non-deterministic candidate evidence; do not use it as gold or rely on one call for production output.

The full CI run [40130130702](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40130130702) was still running at this checkpoint; generated artifacts were clean and master-table generation was underway. Re-check the exact final head after the latest evidence-documentation commit. The previous run's registry status failure was fixed, and repeatability tests were converted to `unittest.TestCase` so the configured CI discovery actually executes them.

## Replication run after trigger cleanup — 2026-10-24

A second successful smoke on the workflow-trigger cleanup commit is [run 40130492210](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40130492210), artifact [12574282871](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40130492210/artifacts/12574282871), ZIP SHA-256 `39b9075da2242e302ceddf62af1d75ef19bcb3cefabe98254371c954bc36cd2c`. It contains all four expected files, and `summary.json`, `goruut-repeatability.json` and `repeatability-summary.json` all parse as JSON. Three-engine coverage and pairwise counts matched the prior run: 36 inputs, 108 rows; 26/36 Goruut outputs, 10 no-`Words` responses; 88 comparable engine pairs, 13 exact matches, 28 slash-only and 31 slash+tone diagnostic matches, 57 remaining mismatches.

The new repeated-call sample again yielded 78 non-empty calls, 30 no-output calls and zero runtime exceptions. Of 26 forms with at least two non-empty outputs, 14 varied (46.15% observed repeatability); the preceding sample had 15 variable forms (42.31% observed repeatability). All variable forms in both samples reported `RandomizationWordsCount=1` and 2–4 choices. This is evidence of unstable candidate output, not an accuracy estimate. The different per-run variation count is itself a reason to preserve run-specific raw artifacts rather than collapse results into one supposedly canonical output.

The optional workflow now runs on `push` when its code/input/workflow files change, or through `workflow_dispatch`; the broad `pull_request` path trigger was removed so documentation/evidence-only commits do not repeatedly launch the stochastic probe. Record run IDs and hashes instead of triggering another random sample merely to update prose.

## Merge and post-merge verification checkpoint — 2026-10-24

PR #42 was squash-merged as `19cc950d84c699b2302c436e013b62f53d48233f`. The change is optional research tooling; it does not alter the runtime phonetic pipeline and Goruut remains disabled by default/unverified in repo. Exact pre-merge CI test job [40130708512](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40130708512) passed generated-data checks, the master-table generator, 108 Python tests, Node IPA→UA and parity tests. Its separate master-artifact job was queued at merge time; a code-identical prior run [40130492215](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40130492215) passed the 351,780-row / 41-vowel artifact assertion. Optional smoke [40130492210](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40130492210) succeeded and its four-file artifact was inspected; all JSON summaries parse.

Post-merge main CI [40131179279](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131179279), smoke [40131179238](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131179238), and Pages deployment [40131179264](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131179264) were queued when this note was written. Their conclusions must be checked before final release-readiness claims. Accuracy remains unmeasured: independent gold = 0.

## Post-merge smoke and upstream license scope — 2026-10-24

Main-branch optional smoke [40131179238](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131179238) passed and artifact [12575525598](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131179238/artifacts/12575525598) was inspected; ZIP SHA-256 `f3dbd829d59db79eb4c5b8c86395f7948355da488285f968f7dca955c9eade9a`. All expected files are present and all JSON parses. The 3-engine diagnostic remains 36 inputs/108 rows, Goruut 26/36 non-empty and 10 no-`Words` responses; 13/88 raw pair agreements. Repeated calls again produced 78 non-empty, 30 no-output, zero runtime exceptions; 13/26 comparable forms varied. Prior runs varied on 15/26 and 14/26. All variable forms carried the upstream randomization counters; this is strong evidence of unstable candidate output, not accuracy.

The upstream software `LICENSE` at pinned commit `b224bde02151f8f86d0fe260804e4ca743bda620` is MIT. This is not a blanket license finding for the bundled language-specific lexicon/model: its provenance and any separate data rights remain unaudited. Registry wording now distinguishes software licensing from unresolved data provenance.

Post-merge CI [40131179279](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131179279) and Pages deployment [40131179264](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131179264) were still pending when this update was prepared. Inspect before release-readiness claims.
