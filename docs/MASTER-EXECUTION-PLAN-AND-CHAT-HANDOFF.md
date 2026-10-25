# Master execution plan and chat handoff — Thai → Ukrainian Phonetic System

Last audited: 2026-10-20
Repository: https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System
Branch checked: `main`
HEAD at audit start: `47ccd4d29c38a3032487c74075b569373c3d30bf`
Release declared in README/pyproject: `0.6.1`

## Operating rule

At the start of each continuation, read this file, `docs/final-audit.md`, `docs/evidence.md`, `docs/adversarial-validation.md`, `docs/corpus-validation.md`, and the current workflow definitions. Re-check HEAD and the newest CI/Pages runs before acting. Do not treat older audit prose as proof of current CI status. Keep linguistic correctness separate from parser consistency and empirical accuracy. Never convert a regression test copied from current behavior into linguistic gold evidence.

## Current verified state (2026-10-20)

- Public repository is accessible; default branch is `main`; current HEAD at audit start is `47ccd4d29c38a3032487c74075b569373c3d30bf` (commit dated 2026-10-09).
- Workflows present: `.github/workflows/ci.yml`, `pages.yml`, `web-static.yml`.
- The original code baseline failed [CI run 37929499793](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/37929499793). The docs-only handoff commit was checked by [run 738](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/39482426090), which repeated the `ตรอก` failure. The parser fix plus structural regression test were committed as `83bcdb8177d81392683864df0b4ae45aeafdfb7e` and `8fcc25d1bd3cac6d8a372319abfd0651e022687f`. CI run 741 failed before unit tests because `docs/generated-audit.json` changed only in `csv_records` key order: `Path.glob()` iteration in `src/thai_ukrainian/validator.py` was nondeterministic. Fixed by sorting CSV paths in commit `78e96814eaaf225131469bd2229d56ec8a7cf1ec` and sorting the tracked artifact in commit `0e141ea1c88c99fcad245d395748587fb809b7d9`. CI run 743 is currently in progress; artifact generation and clean-tree check have passed, and master-table generation is running. Unit and browser checks have not completed yet.
- Latest observed Pages workflow for HEAD: [run 37929499737](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/37929499737), conclusion **failure**; deploy job was skipped because regression tests failed.
- CI log: package install, derived artifact generation, structural-space generation, clean-tree check and master-table generation passed. Python unittest step ran 88 tests and failed one subtest; Node/browser checks were skipped due to fail-fast job sequencing.
- Exact failing case: `tests/test_text_pipeline.py::TextPipelineTests.test_final_velar_stop_is_preserved_in_ukrainian_output`, subtest `word='ตรอก'`. Expected status `analyzed`, actual `unresolved:nonconforming-consonant-sequence`. This is a real release blocker; do not relabel as passed or weaken the test without independent linguistic justification.
- The repository's README explicitly disclaims empirical corpus accuracy and says unknown segmentation and special orthography must remain evidence-gated. Preserve those limitations.
- `CITATION.cff` already exists. Do not recreate it blindly; inspect its metadata before release work.
- Root cause of `ตรอก` was identified in `_split_onset_coda`: it re-collected every inventory consonant from the spelling, including `อ`, even after `classify_o_role` had identified อ as a vowel component and the main parser had removed it from structural consonant candidates. This created a spurious extra consonant in the proposed onset and caused the valid `ตร` cluster to be rejected. The parser now accepts an `ignored_consonants` argument and passes `อ` when its role is `vowel_component`/`orthographic_component`; the regression test additionally asserts onset `["ต", "ร"]` and coda `"ก"` for `ตรอก`. Independent lexical evidence lists `ตรอก` syllabification as `ตฺรอก` and standard IPA /trɔːk̚˨˩/ (Wiktionary Thai entry: https://th.wiktionary.org/wiki/ตรอก; English entry: https://en.wiktionary.org/wiki/ตรอก). Do not mark THAI-001 complete until the current CI's Python and browser/parity checks pass. No tests were run locally; all test outcomes are from GitHub Actions.

## Execution backlog

| ID | Priority | Status | Task / acceptance criteria | Dependencies / evidence |
|---|---|---|---|---|
| THAI-001 | P0 | DONE_VERIFIED | Preserve final velar stop for `ตรอก`; regression asserts analyzed status, onset `ต ร`, coda `ก`, final IPA `k`, and Ukrainian final `к`. | `tests/test_text_pipeline.py::test_final_velar_stop_is_preserved_in_ukrainian_output`; current-main CI [40131709016](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131709016) passed. The old failure reference 37929499793 is historical only. |
| THAI-002 | P0 | DONE_VERIFIED | Exact PR-head workflow [40196572177](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40196572177) passed both `test` and `master-artifact` jobs after PR #46 was integrated. It ran 112 Python unittest cases, generated-data cleanliness, syllable-space/master-table generation, Node IPA→Ukrainian, Python/browser parity, and the 351,780-row / 41-vowel artifact assertions. | Existing `ci.yml`; independent gold gate remains separate. |
| THAI-003 | P0 | TODO | Verify current Pages deployment after CI passes; confirm both `index.html` and `system.html` load and browser analysis works. | THAI-002; existing Pages workflow. |
| THAI-004 | P1 | IN_PROGRESS | Existing lexical exceptions for `จริง`, `สร้าง`, `เศร้า`, and `ไซร้` remain regression-tested. PR #49 adds `ศรี → สี`, PR #50 adds source-attested `ทร` readings, and PR #53 removes the unsafe unconditional `ทราย → ซาย` override because the Royal Institute 2011 article distinguishes the sand sense (false cluster /s/) from the deer-name sense (true `ทร` cluster). PR #53 merged as `e39e1502623d0f625db1991350ea3017179f4851`; exact-head workflow [40212243319](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40212243319) passed both test and master-artifact jobs, including 117 Python tests and 351,780 master rows. | The spelling-only API now withholds IPA/UA for `ทราย` under `SP-THR-001`; source `SRC-ORST-CLUSTER-2011-THRAY-SENSE` points to p. 556. This is ambiguity handling, not IPA gold. | Continue auditing valid clusters, leading consonants and lexical `ทร`; source-located lexical IPA gold and context coverage remain open. |
| THAI-005 | P1 | TODO | Audit `รร`, `ฤ/ฤๅ`, `ฦ/ฦๅ`, thanthakhat/silent letters and `อ นำ`; for each, record implemented behavior, source-backed rule, independent examples and unresolved cases. | Special-orthography registry; reliable lexical/official sources. |
| THAI-006 | P1 | TODO | Audit Unicode normalization, tokenization, explicit syllable boundaries, unknown input and malformed input in Python and browser implementations. | Existing Unicode, text and parity tests. |
| THAI-007 | P1 | TODO | Verify claim-level citations for tone, vowel length, consonant classes, codas, clusters and IPA; record exact page/section where available. | `docs/evidence.md`; source files and cited references. |
| THAI-008 | P1 | TODO | Build an independent, versioned gold evaluation protocol and report actual metrics only after processing a licensed/adjudicated corpus. Include stratified errors and explicit denominators. | External corpus access/licensing; `docs/corpus-validation.md`. |
| THAI-009 | P2 | IN_PROGRESS | Selectively port current-main-safe UX improvements from stale PR #17 without replacing the v0.6.1 text/IPA engine: visible input guidance, Ctrl/⌘+Enter, immediate examples, active navigation, result headings, copy controls, status guide, and a truthful warning when tokenization/analysis is unresolved or no Thai token exists. Added a Node DOM-contract test wired into CI. | Exact-head CI must pass Python, IPA→Ukrainian, Python/browser parity and the new UI contract test. No screenshot/device audit is claimed; mobile and real assistive-technology checks remain open. |
| THAI-010 | P2 | TODO | Inspect `CITATION.cff`, release protocol and licensing/provenance; then prepare versioned release, Zenodo archive and methodology paper without unsupported accuracy claims. | THAI-004–THAI-009. |
| THAI-011 | P1 | DONE_VERIFIED | Merged PR #46 as `fcfe7c95858efceaa73417deaf762908529a8514`: unsupported onset segments now withhold both IPA layers, downgrade status to `unresolved:unsupported-onset`, and emit a diagnostic. Regression is a discovered `unittest.TestCase` method. Exact-head CI [40196572177](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40196572177) passed both jobs. | This closes only the unsupported-onset contract; broader unknown-input, cluster, special-orthography and independent-gold tasks remain open. |

Allowed statuses: `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE_VERIFIED`, `DEFERRED`, `NOT_APPLICABLE`. Mark `DONE_VERIFIED` only with recorded evidence and exact check result.

## Known linguistic/evidence boundaries

The existing docs explicitly mark these as analysis-dependent or not empirically closed: `รร`; `ฤ/ฤๅ` and `ฦ/ฦๅ`; lexical/morphological `ทร`; silent-letter constructions; automatic multi-syllable segmentation; connected-speech phonetics; and empirical Ukrainian orthographic preference. These must be reviewed, not assumed complete merely because a registry exists.

The 351,780-row generated table is a structural combinatorial upper bound, not a count of valid or attested Thai syllables. The project currently has no published corpus accuracy or calibrated candidate probabilities.

## Continuation update — 2026-10-20, parser diagnosis and deterministic audit fix

- Parser fix commit: `83bcdb8177d81392683864df0b4ae45aeafdfb7e`; regression test commit: `8fcc25d1bd3cac6d8a372319abfd0651e022687f`.
- `ตรอก` failure root cause is the extra `อ` reintroduced by `_split_onset_coda`; fix explicitly excludes that grapheme when it is a vowel/orthographic component. Added assertions for onset `ต, ร` and coda `ก`.
- CI run 741 failed before Python tests because `docs/generated-audit.json` key order changed between runs. `csv_counts()` used unsorted `Path.glob("*.csv")`. Fixed by sorting paths (`78e96814eaaf225131469bd2229d56ec8a7cf1ec`) and regenerated/sorted `docs/generated-audit.json` (`0e141ea1c88c99fcad245d395748587fb809b7d9`). This is an independent reproducibility bug, not a parser failure.
- CI run 743 (`39483996886`, SHA `0e141ea1c88c99fcad245d395748587fb809b7d9`) was observed in progress: artifact generation and generated-artifact cleanliness passed; master-table generation was running. Do not claim test success until run completes.

## Continuation update — 2026-10-20, after handoff commit

- Latest CI run 738 (`39482426090`, SHA `c77c2017f68822c1139de09ad61eab63dd0e3af8`) failed in `python -m unittest discover -s tests -v`; the same `ตรอก` subtest is still failing. The master-artifact job was skipped because it depends on the test job.
- Current parser source declares `ต` as a licensed complex-cluster first member and `ร` as a licensed second member. The `_split_onset_coda` branch appears intended to assign `ตร` as onset and `ก` as coda, but the actual returned state in CI is not fully explained by static inspection. Next step: add a temporary, narrowly scoped diagnostic test or reproduce in a local checkout to inspect `detect_vowel`, `_split_onset_coda`, final `onset`, `coda`, `structural_cs`, and `complex_invalid` for `ตรอก` and control `พริก`; remove diagnostic-only output before merge. Only then implement the smallest evidence-supported fix.
- No parser code was changed in this continuation; do not mark THAI-001 done.

## Handoff for next chat

1. Re-read this file and the linked current audit/evidence docs.
2. Recheck `main` HEAD and newest CI/Pages run; if HEAD changed, fetch the new logs before using this diagnosis.
3. Start with THAI-001. Inspect `src/thai_ukrainian` onset validation and any lexical/special-orthography pathways. Do not change the test expectation merely to make CI green.
4. Use independent evidence to decide whether `ตรอก` is a valid lexical exception, requires a word/syllable boundary, or should remain unresolved under the declared API contract.
5. After a justified fix, run the narrow regression and full local checks where possible, commit the evidence and update this file with commit SHA, exact commands/results, CI links, and next open IDs.


## Handoff update — external Thai G2P smoke workflow (2026-10-24)

- Branch: `ci/optional-external-g2p-smoke-2026-10-24`; PR will add a manually dispatchable and path-triggered optional workflow.
- Pins: `thaiphon==0.7.0`, `pythainlp==5.4.0`, and FastThaiG2P upstream commit `c4759eef7df03e11fcbb9aa83efe8cf21709fd2f` (source commit already recorded by the benchmark script).
- The workflow preserves raw outputs and summary in an artifact. The 30+ challenge items are not independently adjudicated gold; exact raw-string matches are diagnostic only. The optional VOLUBILIS lexicon is not installed.
- Status: IN_PROGRESS until CI and artifact inspection. No engine enabled in production; no accuracy claim. Existing TODO THAI-001 and all research gates remain unchanged.


## Handoff update — Thai external G2P smoke result (2026-10-24)

- **DONE_VERIFIED — raw-output smoke:** [workflow 40092505291](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40092505291) passed. Artifact SHA-256: `9b2776de9be93f15d16c52b0c336fd196db7b41de6513394ac4a8f9b09218a78`. Pins: thaiphon 0.7.0 (base engine; no optional VOLUBILIS lexicon), PyThaiNLP 5.4.0, FastThaiG2P commit c4759eef7df03e11fcbb9aa83efe8cf21709fd2f / package 0.1.0.
- 36 inputs × 2 engines = 72 raw outputs, 0 errors, 0 gold-labeled rows, 0 scored comparisons. Example: `ไกล` diverges (thaiphon returns `/kaj˧/ /la˦˥/`; FastThaiG2P `/klaj˧/`); `จริง` shows a large divergence consistent with a fallback/lexicalization issue. These are prioritization signals only, not accuracy results.
- No external engine enabled in production. Next research step: audit lexical source overlap and independently adjudicate the special-orthography and segmentation challenge set before any accuracy metric. Existing THAI-001 parser issue remains unresolved and must not be marked done from this benchmark.


## Final merge checkpoint — Thai external G2P smoke (2026-10-24)

- PR [#23](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/23) merged to main at `bbe9298b2e643d78c0f9f27127482cfda0c62315`.
- Full test/build/parity suite and generated master artifact passed on the code-tested head: [CI 40093256851](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40093256851). The master artifact check validated 351,780 rows and 41 vowel records. Optional raw-output smoke [40093259692](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40093259692) passed.
- Artifact SHA-256 `9b2776de9be93f15d16c52b0c336fd196db7b41de6513394ac4a8f9b09218a78`; 36 inputs × 2 engines = 72 raw outputs, zero errors. Pins: thaiphon 0.7.0, PyThaiNLP 5.4.0, FastThaiG2P commit c4759eef7df03e11fcbb9aa83efe8cf21709fd2f / package 0.1.0. Optional VOLUBILIS lexicon was not installed.
- Diagnostic divergences include `ไกล` and `จริง`; these are research leads only. No independently adjudicated gold labels exist, so no accuracy or winner is claimed. No external engine is enabled in production. Unrelated open PR #17 remains untouched.


## Post-merge main-branch smoke verification — 2026-10-24

- Main workflow [40093730177](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40093730177) passed after merge commit `bbe9298b2e643d78c0f9f27127482cfda0c62315`.
- Inspected artifact SHA-256 `9044719e206505158c9fc1c5da36a9bc8c34d60b4a829b6e98e7623e63b6374a`: 72 raw output rows (36 inputs × 2 engines), 0 runtime errors, 0 gold-labeled rows, 0 raw-string diagnostic rows. Engines: thaiphon 0.7.0 and FastThaiG2P 0.1.0 at commit c4759eef7df03e11fcbb9aa83efe8cf21709fd2f; PyThaiNLP 5.4.0. No optional VOLUBILIS lexicon.
- This confirms repeatable execution only. Accuracy is not measured and no engine is selected for production.


Authoritative readiness checkpoint — 2026-10-24 12:38 UTC

This section supersedes historical workflow-status statements above where they conflict with current evidence.

- Current main HEAD: 728fa7c539d74aa2b0495f163254a647b94bbbee.
- THAI-001: DONE_VERIFIED. Current main includes theตรอก regression and asserts analyzed status, onset [ต, ร], coda ก, and final /k/ preserved in Ukrainian output. Current-main CI passed this test.
- THAI-002: DONE_VERIFIED. Current-main CI 40094071217 passed derived-data generation, clean-tree checks, master-table generation, Python unittest suite, IPA-to-UA test and Python/browser parity test. Master artifact acceptance on prior code-equivalent commit validated 351,780 rows and 41 vowel records.
- Web deployment: latest observed Pages deployment 40091525305 succeeded on 8cf960c8dbf6101ba2a9d83a0f2c7c9b70474d9. Subsequent changes were optional benchmark/docs; no site source changed after that deploy. Exact current-head Pages redeploy was not observed.
- External G2P smoke: DONE_VERIFIED as execution only. Current-main raw-output run 40093730177 produced 72 outputs, 0 runtime errors, 0 independent gold rows. Artifact SHA-256 9044719e206505158c9fc1c5da36a9bc8c34d60b4a829b6e98e7623e63b6374a.
- Remaining TODO/BLOCKED: independently adjudicated Thai lexical/IPA gold corpus; lexicalized/special orthography and connected-speech coverage; calibrated probabilities; independent review of candidate outputs. Keep external G2P engines disabled by default and do not claim empirical accuracy.
- Readiness: engineering CI and reproducible candidate smoke are verified. The repository is a research prototype, not a scientifically accuracy-certified or release-ready general-purpose transcription engine.


## Final post-merge CI verification — 2026-10-24 12:51 UTC

This checkpoint supersedes the earlier note that the post-merge master-artifact job was still running.

- Current `main` HEAD under verification: `f7a2f75ab67b66844fbdca655ddd3600cebea4c9`.
- CI run [40095214451](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40095214451): **SUCCESS**. Both jobs completed successfully:
  - `test`: derived-data generation, syllable-space generation, generated-file cleanliness, master-table generation, Python unittest suite, Node IPA→UA test, and Python/browser parity test all passed.
  - `master-artifact`: master-table generation completed; acceptance assertion passed for `rows == expected_rows == 351780` and `vowel_records == 41`; artifact upload succeeded.
- Uploaded artifact: `thai-ukrainian-master-table`, 3,086,200 bytes, SHA-256 `91e26838ae90235c046f997474126e9ef8402cc88ba62059b6926354f0fe92ec`. Artifact ID `12560063754`; it expires 2027-01-22.
- This closes the engineering-CI and deterministic master-artifact acceptance gate for the current main head. It does **not** close the independent linguistic-evidence gate: there is still no adjudicated, independently sourced gold IPA corpus, so empirical accuracy remains unmeasured and no external G2P engine is enabled in production.
- Open PR [#17](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/17) was inspected but left untouched. Its branch is stale relative to current `main`, GitHub reports it as not mergeable, and its older web/runtime implementation differs substantially from the current main files. Do not merge blindly; if its UX changes are still desired, re-evaluate each against current main and port only demonstrably missing improvements in a fresh branch.
- Current readiness: **engineering CI verified; research prototype, not accuracy-certified or general-purpose release-ready**. Remaining acceptance work is independent gold-corpus acquisition/adjudication, claim-level linguistic evidence review, and stratified evaluation with explicit denominators.


## Fail-closed Thai text output when word segmentation is unresolved — 2026-10-24

### Finding
Both the Python text pipeline (`src/thai_ukrainian/text.py`) and browser engine (`web/src/engine.js`) marked unknown multi-grapheme words as `segmentation_status="unresolved"`, but still passed the entire word to the syllable engine and returned a syllable analysis. The UI therefore could display IPA and a Ukrainian candidate for a word whose syllable boundaries were explicitly unknown. A warning at token level did not prevent the misleading phonetic output.

### Change prepared
- Python and browser text pipelines now return no syllable analyses for unresolved multi-grapheme Thai words; no IPA or Ukrainian candidate is emitted until a lexical entry or explicit segmentation is available.
- Warnings explicitly state that IPA and Ukrainian output are withheld.
- Added Python and browser regression assertions for unknown continuous Thai strings. Curated lexical entries and explicitly segmented syllables continue through the existing phonology → IPA → Ukrainian adapter.

### Verification boundary
- PR [#27](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/27), based on main `822797042dd3f6980202c2f92e491f2a53df80b0`.
- Tests for this PR head are pending. Require Python unittest suite, generated-data drift checks, IPA → Ukrainian tests, browser/Python parity, and master-artifact generation to pass before merge.
- This is a segmentation-integrity correction. It does not claim new lexical readings or improve measured accuracy; the independent-gold corpus is still missing.


## IPA benchmark harness and external engine protocol — 2026-10-24

- Added `scripts/benchmark_ipa.py`, a standard-library-only harness with strict Unicode NFC exact match, code-point Levenshtein CER (diagnostic only), and explicit missing-prediction accounting. Every independently adjudicated gold row remains in each engine's denominator; omitted outputs cannot inflate accuracy.
- Added `data/benchmark/gold.tsv` and `data/benchmark/predictions.tsv` header templates plus `tests/test_benchmark_ipa.py` covering no-gold behavior, adjudication gating, diacritic preservation, missing rows, and mismatches.
- Added `docs/benchmarking-and-external-ipa.md`; linked the existing `data/external-ipa-renderers.json` inventory to the benchmark protocol. External candidates remain optional and disabled by default.
- PR is open; current CI is queued / not yet verified. Do not merge until hosted tests pass. Local GitHub access is unavailable from the current container due network/DNS failure.
- No adjudicated gold corpus was added and no accuracy score is claimed. Candidate engine language support, actual IPA semantics, exact versions, and model/data licensing still require verification. Registry presence and smoke execution are not evidence of accuracy.
- Required next acceptance: run the repository test suite including the new harness tests; inspect all generated-artifact checks; then populate the gold set only with source-located, independently adjudicated pronunciations and rerun all engines against the same held-out set.


## External IPA/G2P and benchmark continuation — 2026-10-24

- Registry and per-language evidence notes: `data/external-ipa-renderers.json` and `docs/benchmarking-and-external-ipa.md`.
- External outputs are diagnostics only unless compared against a versioned, independently adjudicated gold set. Engineering fixtures and source-attested dictionary entries are not automatically gold.
- Shared harness: `scripts/benchmark_ipa.py`; empty templates at `data/benchmark/gold.tsv` and `data/benchmark/predictions.tsv`; tests at `tests/test_benchmark_ipa.py`.


### Verified status as of 2026-10-24

PR #30 was closed as superseded by PR #31, merged as `73617280e6fadab74885845b899bc2314c8d5b6e`. The source-attested three-word Wiktionary spot-check remains diagnostic, not accuracy; PR #32 (text-endpoint warning clarification) and PR #34 (upstream comparator provenance) are separate open follow-ups. Latest unit/web tests and external G2P smoke passed; 100 Python tests, 27 Python/web parity fixtures and tokenizer/lexical regressions passed. Thai smoke: 36 inputs × 2 engines = 72 outputs, 0 runtime errors, independent gold=0, accuracy=null. Durable examples: `data/benchmark/runs/external-g2p-smoke-2026-10-24.json`; full artifact: https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40119997011/artifacts/12570776008.

- Keep IPA adaptation boundary: source spelling → structural parse → source phonology → typed IPA → Ukrainian adapter. Third-party candidates remain optional and disabled in production.
- Current true blocker: a source-located, independently adjudicated language-specific gold corpus with a documented dialect and IPA convention. Do not report accuracy until it exists.


## Source-attested Thai G2P disagreement spot-check — 2026-10-24

- PR [#31](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/31) merged at `73617280e6fadab74885845b899bc2314c8d5b6e` and added three source-attested standard-IPA spot-checks to `data/benchmark/runs/external-g2p-smoke-2026-10-24.json`.
- Selected Wiktionary entries: [กา](https://th.wiktionary.org/wiki/กา) `/kaː˧/`, [ไกล](https://th.wiktionary.org/wiki/ไกล) `/klaj˧/`, [จริง](https://th.wiktionary.org/wiki/จริง) `/t͡ɕiŋ˧/`. On these selected strings FastThaiG2P matches 3/3 and thaiphon 1/3; `ไกล` and `จริง` reveal major segmentation/lexicalization divergences in thaiphon.
- These are source-attested, not independently expert-adjudicated gold. The sample was selected because of known disagreements, and upstream systems may share Wiktionary-derived resources. The counts are not accuracy; no engine is selected for production.
- Preserve raw output and attribution/license notes. Wiktionary content is generally CC BY-SA 4.0; no bulk data was copied. Full caveats and URLs are in `docs/benchmarking-and-external-ipa.md` and the JSON report.
- Overall readiness unchanged: reproducible smoke is verified; empirical Thai accuracy remains NOT_MEASURED until a representative, independently adjudicated held-out gold set exists.



## Thai inter-engine tone diagnostic — verified 2026-10-24

- Latest pinned smoke [run 40123365441](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40122636062) passed: 36 inputs, 72 outputs across thaiphon and FastThaiG2P, 0 runtime errors. Exact inter-engine agreement is 13/36 (36.1%); removing only IPA tone letters in a diagnostic copy gives 14/36 (38.9%), resolving just one additional mismatch. The remaining 22 input pairs differ beyond tone-letter strings and need segmentation/segmental/format review.
- These are inter-engine diagnostics, not accuracy: independent gold count is 0, accuracy is null, and neither engine is selected for production. The source-attested Wiktionary spot-check is pinned to revisions 5734858, 5688545 and 2441036, but is not independently adjudicated and may overlap with FastThaiG2P's sources.
- Artifact ZIP SHA-256: `a4688f082f9a6307fded825b96d7cd025c39869383a4483311707b2d7c2c53ab`.


## Per-engine output accounting

The first pinned Goruut run completed the 36-input challenge and produced 108 rows, but the inter-engine diagnostic compared only 88 pairs. The updated harness therefore reports per-engine successful outputs, failed outputs, empty outputs without an exception, and representative failures. A complete three-engine smoke should have 108 pair comparisons if all three engines produce valid outputs for all 36 inputs. This is a coverage diagnostic, not an accuracy metric.


## Goruut repeatability

The endpoint readiness probe returned `kaː˧` for `กา`, while the first benchmark artifact recorded `ka` for the same form. Because these requests occurred in different contexts, this is a repeatability hypothesis rather than proof of stochastic output. The optional workflow now repeats each challenge form three times and preserves raw outputs plus Goruut's randomization counters. A stable output is not evidence of correctness; variability must be analyzed separately from accuracy.


## Goruut benchmark evidence checkpoint — 2026-10-24 (continuation)

- PR [#42](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/42) now includes the pinned Goruut comparator, per-engine accounting, fail-closed smoke-success accounting, and a repeatability probe. Production runtime remains unchanged.
- Inspected run [40128121032](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40128121032), artifact ZIP SHA-256 `83cde4269dad940ef3d2521b6aba0b8f22eda56f71ec3612bb7230f6274f5b6b`: 36 inputs/108 rows; thaiphon 36/36 non-empty, FastThaiG2P 36/36, Goruut 26/36 non-empty and 10 per-input failures. Pairwise diagnostics: 88 comparisons, 13 exact agreements, 14 tone-stripped diagnostic agreements, 1 tone-only disagreement, 74 non-tone/format disagreements.
- Raw-output caveat: `กา` was `/kaː˧/` in thaiphon/FastThaiG2P but `ka` in Goruut; several outputs lack separators and some requests return an empty `Words` array. These are format/coverage observations, not adjudicated pronunciation errors. Goruut remains optional, `verified_in_repo=false`, independent gold=0, accuracy=null.
- A repeatability probe now repeats challenge forms three times and records raw output/randomization counters. The readiness probe and first benchmark differ for `กา` (`kaː˧` vs `ka`); this is a hypothesis requiring the repeated run, not yet evidence of stochasticity.
- Current PR head: `7e235197b162a4f7a8af3f23205ee595b23c9054`. Current-head CI `40128778875` and optional smoke/repeatability workflow `40128778650` are queued. Do not mark the PR verified until those runs complete and their artifacts are inspected.
- Remaining scientific blockers: representative independently adjudicated Thai gold; documented Goruut output convention/dialect/model-data provenance; feature-level evaluation separate from raw string agreement.

The harness now emits `pairwise_engine_diagnostic` for each engine pair, including its own comparable-input denominator and raw/slash-stripped/slash+tone-stripped counts. This avoids mixing missing-output coverage across engine pairs.

## Continuation checkpoint — 2026-10-24, after current-head smoke

- Current reviewed PR #42 head at this checkpoint: `9ef3612dd54d30640f299cdb19bff0ab95fa7b29`. The optional three-engine smoke run [40129230641](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40129230641) completed successfully and produced artifact [12573981792](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40129230641/artifacts/12573981792), ZIP SHA-256 `192950f4bd426f3c274a78ab135072546225931003d59acd9ed7dd036dc4ef2a`.
- Inspected artifact `summary.json`: 36 inputs × 3 engines = 108 rows; thaiphon 36/36 and FastThaiG2P 36/36 non-empty; Goruut 26/36 non-empty and 10 explicit `Words: []` failures. 88 engine pairs, 13 exact agreement pairs; slash-stripped and slash+tone-stripped matches are diagnostic-only (30 and 31 pairs). 57 pairs still differ after those limited diagnostics. Independent gold count 0, accuracy null.
- Registry and benchmarking document refreshed to reference this current artifact. This is endpoint/coverage evidence only, not an accuracy result. Do not normalize away tone/length or treat cross-engine agreement as gold.
- Full CI [40129230638](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40129230638) was still in progress when inspected: generated artifacts were clean and master-table generation was underway; Python and Node tests had not yet completed. Re-check this exact head before merge.
- Remaining acceptance gates: inspect completion of full CI; obtain and inspect the separate repeatability-probe artifact before making claims about stochasticity; validate raw output conventions and per-language model/dictionary provenance; create an independently sourced/adjudicated Thai gold set before any accuracy score. No production runtime change is authorized by this research PR.

## CI regression / corrective checkpoint — 2026-10-24

- Inspected full CI run [40129230638](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40129230638) using its job log. Generated-data checks and master-table generation passed; Python suite ran 108 tests and failed exactly one registry test.
- Failure: `tests/test_external_ipa_registry.py::ExternalIpaRegistryTests.test_candidates_have_unique_ids_and_valid_https_links` expected controlled status vocabulary `candidate | benchmark-resource | supporting-tool | display-only`, but Goruut had `status=SMOKE_VERIFIED_PARTIAL_COVERAGE_NOT_ACCURACY`.
- Corrected registry to `status=candidate`; retained execution result separately as `execution_status=SMOKE_VERIFIED_PARTIAL_COVERAGE_NOT_ACCURACY`. This is an actual CI regression fix, not a linguistic change.
- Acceptance: inspect CI on the exact corrected branch head; require Python, Node IPA→UA and parity checks all to pass. The previous run's Node checks were skipped after the Python failure.

## Repeatability probe artifact/test correction — 2026-10-24

- Found two observability gaps in the optional workflow: the upload step omitted `goruut-repeatability.json` and `repeatability-summary.json`; fixed the artifact path list.
- Found that the CLI printed a human-readable path after its JSON summary to stdout, making the `tee` summary file invalid JSON. Moved that path notice to stderr and added a CLI regression test that parses stdout and the saved report as JSON.
- Found the two repeatability checks were bare pytest-style functions, while CI invokes `python -m unittest discover -s tests -v`; unittest discovery would not execute those functions. Converted them to `unittest.TestCase` methods and added the CLI output-contract test.
- Current source changes require fresh exact-head CI and smoke verification. Do not use earlier smoke artifacts to infer repeatability: they did not upload the repeated-call report.

## Latest repeatability evidence and exact CI checkpoint — 2026-10-24

- Current inspected optional smoke [40130130705](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40130130705), artifact [12575022202](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40130130705/artifacts/12575022202), ZIP SHA-256 `88693eb1e85b9957c86aa2e04993dd30d8749d58dd39d7074437c7d2bdc73d16`. All three JSON artifacts parsed: benchmark summary, full repeatability report and repeatability summary.
- Three-engine benchmark: 36 inputs / 108 rows; thaiphon 36/36, FastThaiG2P 36/36, Goruut 26/36 non-empty with 10 no-`Words` responses; 88 comparable engine pairs, 13 exact agreements. Slash and tone removal are diagnostic-only; no gold rows exist.
- Repeatability: 36 forms × 3 = 108 calls; 78 non-empty, 30 no-output, 0 runtime errors. Among 26 forms with at least two non-empty results, 15 varied and 11 were stable in this sample (observed repeatability 42.3%). All 15 variable forms reported `RandomizationWordsCount=1` and 2–4 `RandomizationWordsChoices`; ten forms had no non-empty output across all three calls.
- Pinned upstream selector [source](https://github.com/neurlang/goruut/blob/b224bde02151f8f86d0fe260804e4ca743bda620/repo/services/parts_of_speech_selector_service.go) documents a random dictionary-pronunciation fallback when no preferred homograph is available. This is consistent with observed variation but does not adjudicate which pronunciation is correct. Keep Goruut optional/disabled and do not use as gold.
- Fixed the registry controlled-status regression, repeatability artifact upload list, JSON-only stdout contract and test discovery by unittest. Current full CI run [40130130702](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40130130702) was still in progress before these latest evidence-documentation commits; exact final head needs a fresh CI run and all Python/Node/parity gates.

## Replication and workflow-trigger cleanup — 2026-10-24

- Second successful smoke run [40130492210](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40130492210), artifact [12574282871](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40130492210/artifacts/12574282871), ZIP SHA-256 `39b9075da2242e302ceddf62af1d75ef19bcb3cefabe98254371c954bc36cd2c`. All expected files present; all three JSON files parse. Benchmark: 36 inputs / 108 rows, Goruut 26/36 non-empty, 10 no-`Words` failures, 0 runtime exceptions; 13/88 raw pair agreements and diagnostic-only slash/tone counts 28/31.
- Repeatability sample: 78/108 non-empty calls, 30 no-output, 0 runtime errors; 14/26 inputs with at least two non-empty outputs varied (46.15% repeatability), compared with 15/26 (42.31%) in prior run 40130130705. All variable cases in both runs reported one randomized dictionary selection and 2–4 choices. Preserve both run records and raw artifacts; do not infer accuracy.
- Updated the structured registry to point to run 40130492210 while retaining the previous run's repeatability statistics. Evidence-only changes no longer trigger the optional smoke workflow: it now runs on pushes touching code/input/workflow paths or manual dispatch, not broad PR path matching. This prevents stochastic re-runs on documentation-only updates.
- CI on prior code/evidence head [40130130702](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40130130702) completed its test job successfully: generated artifact drift check, master-table generator, 108 Python tests (including repeatability tests), Node IPA→UA test and Python/browser parity passed. The separate master-artifact job was still generating/verifying the 351,780-row artifact at last check; current evidence-only head needs its own CI completion before merge.

## Post-merge checkpoint — 2026-10-24

- PR #42 (`Add optional Goruut Thai IPA comparator with repeatability evidence`) was squash-merged into main as `19cc950d84c699b2302c436e013b62f53d48233f`. It adds research/benchmark tooling only; production phonetic runtime remains unchanged, Goruut remains `enabled_by_default=false` and `verified_in_repo=false`.
- Exact pre-merge head `7303ed151df73a491150e5a3012cedf5bc73c942` CI test job [40130708512](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40130708512) passed generated-data drift checks, master-table generation, 108 Python unittest cases (including the repeatability CLI JSON test), Node IPA→UA tests, and Python/browser parity. Its separate 351,780-row master-artifact job was queued at merge time; the same generator, 351,780-row count and 41-vowel check passed on code-identical head `1bb56eb77d97e43a80c4e3e4f46ab722fdcfa9be` in [40130492215](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40130492215).
- Optional smoke [40130492210](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40130492210) passed and its artifact [12574282871](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40130492210/artifacts/12574282871) was inspected; all JSON files parse. It yielded 36 inputs/108 rows, Goruut 26/36 non-empty, 10 no-`Words` responses; repeated calls yielded 78/108 non-empty, 30 no-output, 0 runtime errors, 14/26 variable forms (46.15% observed repeatability). The prior run had 15/26 variable. All variable forms had the upstream randomization counters set.
- Post-merge main workflows [CI 40131179279](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131179279), [optional smoke 40131179238](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131179238), and Pages deployment [40131179264](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131179264) were queued when this note was prepared. Do not report those post-merge runs as passed until inspected.
- Release/research status: **research/engineering prototype, not accuracy-validated**. Independent Thai gold count is zero; no accuracy score is claimed. The primary next blocker is an independently sourced and adjudicated Thai gold set with declared dialect and IPA conventions, plus a documented audit of tone/length/segmentation and upstream language-data provenance.

## Post-merge workflow refresh — 2026-10-24

- Main optional smoke [40131179238](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131179238) completed successfully; artifact [12575525598](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131179238/artifacts/12575525598), ZIP SHA-256 `f3dbd829d59db79eb4c5b8c86395f7948355da488285f968f7dca955c9eade9a`. The four expected files are present; all JSON summaries parse. It again returned 36 inputs/108 rows, Goruut 26/36 non-empty, 10 no-`Words` failures, 88 engine pairs and 13 exact agreements. Slash/tone-stripped counts are diagnostic only.
- Post-merge repeatability: 108 calls, 78 non-empty, 30 no-output, 0 runtime errors; 13/26 forms with at least two non-empty outputs varied (50% observed repeatability). Earlier samples recorded 15/26 and 14/26 variable forms. All variable forms in these samples had randomization count=1 and 2–4 dictionary choices. Keep all run records; no accuracy is measured.
- Verified the upstream Goruut software `LICENSE` at pinned commit `b224bde02151f8f86d0fe260804e4ca743bda620` is MIT. This only establishes the upstream software license; bundled language-specific lexicon/model provenance and data rights have not been independently audited, so those remain a blocker.
- Post-merge main CI [40131179279](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131179279) and Pages deployment [40131179264](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131179264) were still running/queued at this checkpoint. The CI test job on pre-merge exact head passed, but do not report post-merge CI/deploy as passed until their own conclusions are inspected.

## Authoritative current-head checkpoint — 2026-10-25

This section supersedes earlier notes in this handoff that said post-merge main CI or Pages deployment were queued. The SHA below is the base-main commit immediately before this documentation-only checkpoint; the current PR head and its own checks are recorded in PR #44.

- Base `main` before this documentation-only checkpoint: `26dfafcd4d0b06045505f5d13bfd454bb6d873e5`.
- Post-merge CI [40131709016](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131709016): `success`. Post-merge Pages deployment [40131709018](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131709018): `success`.
- Exact documentation/registry PR #43 head [40131388837](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131388837): `success`.
- Optional Goruut smoke [40131179238](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131179238) and artifact [12575525598](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131179238/artifacts/12575525598) were inspected. 36 inputs, 108 calls across engines; Goruut yielded 26/36 non-empty outputs and 10 no-`Words` results. On repeated calls 13/26 comparable forms varied; prior samples varied on 15/26 and 14/26. This is a repeatability/coverage diagnostic only. Independent Thai gold remains 0 and accuracy remains unmeasured.
- Goruut's upstream software license at pinned commit `b224bde02151f8f86d0fe260804e4ca743bda620` is MIT. This does not establish rights/provenance for bundled language data, which remains unaudited.
- Remaining acceptance work: source-located, independently adjudicated Thai gold with declared dialect and IPA convention; review of tone/length/segmentation; language-data provenance; The former THAI-001 regression is now DONE_VERIFIED: `tests/test_text_pipeline.py::test_final_velar_stop_is_preserved_in_ukrainian_output` asserts the onset, coda, IPA final, and Ukrainian final; current-main CI [40131709016](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40131709016) passed. Do not mark research/linguistic accuracy complete based on engineering CI.


## Continuation update — 2026-10-25, public UI IPA-boundary consistency

- Rechecked current `main` engine, README, `web/system.html`, and `web/index.html`. The README and implementation describe the required path as Thai orthography → structural analysis → typed phonetic result/IPA → Ukrainian adaptation, but the service page said the Ukrainian candidate was formed directly from structured Thai analysis and contrasted that with IPA substitution. That wording obscured the actual adapter boundary and contradicted the documented contract.
- Branch: `fix/ui-ipa-boundary-copy-20261025`. Changed only the service method note, added regression assertions to the existing `web/tests/ipa-ua.test.mjs` test (which CI already executes), and recorded this finding here. The assertions verify both the new explanatory wording and consistency with the methodology page; no phonological output, mappings, benchmark rows, or gold labels were changed.
- Verification: exact-head CI run [40193767761](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40193767761) passed the full Python suite, deterministic derived-data checks, 351,780-row master-table generation, `node web/tests/ipa-ua.test.mjs`, and `node web/tests/parity.test.mjs`. Static validation [40193767793](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40193767793) also passed. PR [#45](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/45) merged to `main` at `143dd1cd437059c3a9e4580cbfe1939aa5d1b682`.
- Research boundary unchanged: this UI/documentation correction improves contract clarity only. It does not establish independent Thai IPA or Ukrainian-target accuracy; the independently adjudicated gold corpus remains a separate blocker.


## Fail-closed onset adapter correction — 2026-10-25

- Branch: `fix/withhold-unknown-thai-onset-ipa-20261025`; PR [#46](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/46).
- Defect guarded: `phonologize()` previously composed an unmapped onset as the literal `?` followed by the vowel, which could look like a partial but usable IPA string if a parser/status invariant was violated or the inventory changed.
- Fix: validate every effective onset segment against the adapter's explicit `ONSET_IPA` map before composition. If any segment is unsupported, withhold both phonemic and surface IPA, downgrade status to `unresolved:unsupported-onset`, append a diagnostic warning and record `PHON-UNSUPPORTED-ONSET-WITHHELD`. This prevents stale `analyzed` status from contradicting the withheld result.
- Regression: `tests/test_positional_correspondence.py::PositionalCorrespondenceTests.test_unknown_onset_never_becomes_question_mark_ipa` verifies status is `unresolved:unsupported-onset`, both IPA layers remain `None`, and the diagnostic is present. The regression is a `unittest.TestCase` method because CI uses `python -m unittest discover`; it is no longer a bare pytest-style function that the configured runner would skip.
- Verification: exact code-head workflow [40196214758](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40196214758) passed **112 Python unittest cases**, including `PositionalCorrespondenceTests.test_unknown_onset_never_becomes_question_mark_ipa`, generated-derived-data cleanliness, syllable-space/master-table generation, Node IPA→Ukrainian test, and Python/browser parity. Its separate master-artifact job was queued at last poll; earlier full workflow [40195243134](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40195243134) completed successfully with artifact assertions `rows == expected_rows == 351780` and `vowel_records == 41`. Latest documentation/matrix-only branch head is pending its own CI run.
- This is defensive contract verification, not a change to Thai phonology or an empirical accuracy result. The independent adjudicated IPA gold count remains 0; accuracy is not measured. The older UX PR #17 remains untouched because its engine/data files are stale relative to current main.


## Post-merge checkpoint — 2026-10-25

- PR #46 was merged to `main` as `fcfe7c95858efceaa73417deaf762908529a8514`.
- Exact PR-head workflow [40196572177](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40196572177) completed successfully: `test` and `master-artifact` jobs passed, including 112 Python tests, Python/browser parity, generated-data reproducibility, and master-artifact assertions (351,780 rows, 41 vowel records).
- The unsupported-onset adapter fix is DONE_VERIFIED. This does not close the remaining onset/cluster and special-orthography audit or establish empirical accuracy. Independent adjudicated IPA gold remains 0.


## False-cluster lexical follow-up — 2026-10-25

- PR #49 merged as `650f6e4b1cf651807357ad4f555fe4a3d9c2a543`, adding `ศรี → สี` to both Python and browser lexical-reading registries.
- The cited Royal Institute Dictionary 2011 entry, via Longdo's dictionary interface, supplies the reading `[สี]`; this supports the lexical normalization only, not an independently adjudicated IPA gold label. See https://dict.longdo.com/search/ศรี .
- Exact-head CI [40197477915](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40197477915) passed both `test` and `master-artifact` jobs; the Python suite ran 113 tests.
- THAI-004 is now IN_PROGRESS rather than TODO because one documented false-cluster case was added, but cluster generalization and independent gold remain open.


## Source-attested Thai ทร false-cluster coverage — 2026-10-25

- Added the Royal Institute of Thailand Journal article “เรื่องยุ่ง ๆ เกี่ยวกับอักษรควบ” (vol. 36 no. 4, Oct–Dec 2011) as a specific source record. The article lists selected lexical forms in which ทร is read with ซ, and distinguishes these from Sanskrit/Pali or loanword forms where /tr/ is retained.
- Added explicit lexical overrides for ทราบ → ซาบ, ทราย → ซาย, ทรง → ซง, ทรัพย์ → ซับ, and แทรก → แซก in Python and browser runtimes, with regression tests and text-segmentation entries.
- These are lexical spelling-to-reading overrides grounded in the cited source's example list; they are not independent IPA gold labels and do not justify a productive rule mapping every ทร sequence to /s/.
- The first exact-head test run caught three existing tests that incorrectly assumed `ทราย` always resolves to /s/; those tests now distinguish its lexical segmentation from its unresolved pronunciation. The replacement exact-head CI must pass Python tests, generated-data drift checks, IPA→Ukrainian tests, browser/Python parity, and master-artifact generation.


- Runtime integration follow-up: the Python text lexicon reads `data/thai/text_lexicon.tsv`, while the browser has its own explicit `TEXT_LEXICON` map. The five source-attested words are now added to both segmentation paths and the browser parity regression checks whole-word segmentation plus lexical IPA resolution.


- CI revealed that the lexical override `แทรก → แซก` exposed a deeper parser issue: the preposed-vowel branch treated any non-cluster consonant pair as onset-only and skipped coda analysis. Python and browser now fall through to positional coda assignment when the first pair is not a licensed cluster. Regression asserts `แซก` parses as onset `ซ`, coda `ก`, phonemic IPA `sɛːk`; the existing illegal multi-consonant sequence guard remains in place.


## Source-attested ทร lexical follow-up merged — 2026-10-25

- PR #50 merged as `831993cde68cbc6d40c66d44628cdbd5e96a2565`.
- Added explicit lexical readings `ทราบ → ซาบ`, `ทราย → ซาย`, `ทรง → ซง`, `ทรัพย์ → ซับ`, `แทรก → แซก` from the Royal Institute of Thailand Journal article “เรื่องยุ่ง ๆ เกี่ยวกับอักษรควบ” (vol. 36 no. 4, Oct–Dec 2011; https://www.orst.go.th/FILEROOM/CABROYINWEB/DRAWER004/GENERAL/DATA0000/00000630.FLP/html/49/).
- The parser regression found by `แทรก → แซก` was also fixed: a non-cluster pair after a preposed vowel now falls through to positional coda analysis, retaining coda `ก` and yielding the implementation's `sɛːk`.
- Exact-head CI [40209338369](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40209338369) passed the Python test suite, browser/Python parity, generated-data checks and master-artifact checks.
- These are source-attested lexical overrides, not an independent IPA gold corpus. The implementation must not generalize them into a productive rule that every `ทร` is /s/.


## Current-main Thai UX/accessibility port — 2026-10-25

- Revisited open PR #17 after comparing its old branch against current `main`. The old branch's engine/data files are stale and unsafe to merge; only still-missing presentation improvements are being ported into a fresh branch.
- Preserved the current v0.6.1 `analyzeText` pipeline and IPA → Ukrainian adapter boundary. Updated the current UI to expose input/segmentation guidance, keyboard shortcut, quick examples, status definitions, accessible result headings, copy actions and accurate unresolved/no-Thai-token notices.
- Added `web/tests/ui-contract.test.mjs` and wired it into `.github/workflows/ci.yml` so keyboard interaction, examples, empty/unsupported status and result messaging are tested rather than inferred from static markup.
- This is a code-level accessibility/integrity pass. No screenshot-based, mobile-device, screen-reader or live Pages audit is claimed. PR #17 remains open until this selective port is verified; do not merge its stale engine/runtime.


## Sense-sensitive ทร reading guard — 2026-10-25

- Found a false-confidence bug in the unconditional lexical override `ทราย → ซาย`. The official Royal Institute 2011 article (vol. 36 no. 4, p. 556) distinguishes the sand sense (false cluster, /s/) from the deer-name sense (true ทร cluster).
- Because the API receives spelling without lexical sense, the unconditional override is removed from both Python and browser runtimes. The existing `SP-THR-001` path now withholds IPA and Ukrainian output for the bare homograph.
- Added Python and Node/browser-engine regressions. This is an ambiguity/safety fix, not a new phonological rule or IPA gold label.
- The first exact-head run caught the same three stale assumptions about `ทราย`; those tests were updated to assert conservative withholding. The replacement exact-head CI must pass Python tests, generated-data checks, IPA→Ukrainian tests, Python/browser parity, UI contract and master-artifact assertions before merge.


## Post-merge checkpoint — sense-ambiguous ทราย — 2026-10-25

- PR #53 merged to `main` as `e39e1502623d0f625db1991350ea3017179f4851`.
- The official Royal Institute article, “เรื่องยุ่ง ๆ เกี่ยวกับอักษรควบ”, vol. 36 no. 4 (Oct–Dec 2011), p. 556, distinguishes the sand sense of `ทราย` (initial /s/) from the deer-name sense (true `ทร` cluster): https://www.orst.go.th/FILEROOM/CABROYINWEB/DRAWER004/GENERAL/DATA0000/00000630.FLP/html/48/ .
- Exact-head workflow [40212243319](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40212243319) passed both `test` and `master-artifact`; the master artifact asserted 351,780 rows and 41 vowel records.
- The API now withholds a deterministic reading when only the ambiguous spelling is supplied. This remains a narrow evidence-gated fix; independent IPA gold and general `ทร` context rules remain open.


## Exact-head checkpoint — 2026-10-25

- PR [#55](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/55) merged as `30eae38360367923025851654d2a01745c8fd136`.
- The PR adds regression coverage for the source-attested lexical readings `ทราบ → ซาบ`, `ทรง → ซง`, `ทรัพย์ → ซับ`, and `แทรก → แซก`. These remain lexical overrides, not a productive rule for every spelling with `ทร`, and not independent IPA gold.
- Exact-head CI run [40214453752](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40214453752) passed both jobs: the test job (Python unit tests, generated-audit/syllable-space/source-manifest drift check, IPA adapter tests, Python/browser parity and UI contract) and the master-artifact job (generated 351,780 rows, asserted expected row count and 41 vowel records, uploaded the artifact).
- This confirms engineering regression/reproducibility for the added cases only. Independent gold-corpus accuracy remains unmeasured; the repository remains a research-oriented reference implementation, not an empirically validated release.


## Typed Thai IPA surface-layer validation — 2026-10-25

- Adversarial inspection found that `PhoneticResult.from_syllable_analysis` validated phonemic IPA segments for `SUPPORTED` status but did not include unsupported symbols in the broad surface IPA in that decision. A malformed or empty surface string could therefore remain visible while the typed result was marked supported and passed the Ukrainian adapter gate.
- The typed-result builder now checks surface-IPA segment certainty as well as phonemic segments. Added regressions injecting an unsupported snowman symbol and an empty surface IPA into otherwise valid phonemic output; the typed result must be `UNSUPPORTED` and the Ukrainian adapter must withhold output.
- This is an adapter-boundary integrity fix, not evidence of improved Thai phonetic accuracy. Exact-head CI is required before merge; independent gold-corpus accuracy remains unmeasured.


## Reconciliation of stale Thai v0.5.1 UX/IPA overhaul PR — 2026-10-25

- Open PR [#17](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/17) targets the v0.5.1 browser implementation from 2026-10-08. Its web app, engine and data files materially diverge from current `main`, which now has a newer text pipeline, IPA boundary and generated-data contracts. Do not merge its code wholesale.
- The historical audit `docs/repository-audit-2026-10-05.md` is already on `main`. The unique design specification and static UX audit are being preserved under `docs/archive/` with explicit historical notices. They do not verify the current UI or imply that their historical checklists remain complete.
- PR #58 conflicted after PR #57 updated this same handoff and was closed as superseded; its branch remains untouched. The rebased archive-only PR #59 then merged as `eed20b0903b67940d82f2e60ef49aadf12528378`, and PR #17 was closed as superseded. Its original branch remains untouched.


## Post-merge typed IPA boundary checkpoint — 2026-10-25

- Thai surface-IPA validation fix merged as `433a76d3ee6c916a8e831529ae9489191ae961cf` via [PR #57](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/57).
- Exact-head CI [40216847288](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40216847288) passed both the test job (Python suite, generated-data drift, browser IPA/UA, parity and UI contract tests) and the master-artifact job (351,780-row generated artifact validation).
- The typed result now fails closed if broad surface IPA contains unsupported symbols or is an empty string while phonemic IPA exists; Ukrainian adaptation is withheld because the typed status is unsupported. This is adapter-boundary integrity, not corpus accuracy evidence.


## Final PR reconciliation checkpoint — 2026-10-25

- Current `main` after the typed IPA-boundary fix and historical-document archive is `eed20b0903b67940d82f2e60ef49aadf12528378`.
- Code PR #57 exact-head CI passed in [run 40216847288](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40216847288), including Python tests, generated-data drift, browser IPA/UA and parity/UI contracts, plus the 351,780-row master artifact job. Archive-only PR #59 merged; PR #17 was closed as superseded after preserving its unique historical documents. No branches were deleted.
- Post-merge `main` CI/Pages runs for the archive commit were queued/in progress at the last check; do not claim those post-merge runs have completed until verified. The code-bearing PR head itself is CI-verified.
