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
| THAI-001 | P0 | IN_PROGRESS | Diagnose `ตรอก` failure from the actual parser path. Establish expected syllable structure and reading from a reliable Thai source; add/adjust a regression only if independently justified. Preserve rejection of genuinely impossible onsets. | Failing CI run 37929499793; test `tests/test_text_pipeline.py`; inspect parser/lexical data. |
| THAI-002 | P0 | TODO | Restore full CI gate: Python tests, generated-artifact cleanliness, master table, Node IPA→UA test and Python/browser parity must all run successfully on a new commit. | THAI-001; existing `ci.yml`. |
| THAI-003 | P0 | TODO | Verify current Pages deployment after CI passes; confirm both `index.html` and `system.html` load and browser analysis works. | THAI-002; existing Pages workflow. |
| THAI-004 | P1 | TODO | Audit onset validation against standard Thai clusters, leading consonants, false clusters and lexical `ทร`; ensure valid word-internal syllable structures are not rejected by a single-syllable validator. | THAI-001; evidence registry and claim-level sources. |
| THAI-005 | P1 | TODO | Audit `รร`, `ฤ/ฤๅ`, `ฦ/ฦๅ`, thanthakhat/silent letters and `อ นำ`; for each, record implemented behavior, source-backed rule, independent examples and unresolved cases. | Special-orthography registry; reliable lexical/official sources. |
| THAI-006 | P1 | TODO | Audit Unicode normalization, tokenization, explicit syllable boundaries, unknown input and malformed input in Python and browser implementations. | Existing Unicode, text and parity tests. |
| THAI-007 | P1 | TODO | Verify claim-level citations for tone, vowel length, consonant classes, codas, clusters and IPA; record exact page/section where available. | `docs/evidence.md`; source files and cited references. |
| THAI-008 | P1 | TODO | Build an independent, versioned gold evaluation protocol and report actual metrics only after processing a licensed/adjudicated corpus. Include stratified errors and explicit denominators. | External corpus access/licensing; `docs/corpus-validation.md`. |
| THAI-009 | P2 | TODO | Audit mobile usability, accessibility, deployment metadata and documentation consistency after functional CI is green. | THAI-002, THAI-003. |
| THAI-010 | P2 | TODO | Inspect `CITATION.cff`, release protocol and licensing/provenance; then prepare versioned release, Zenodo archive and methodology paper without unsupported accuracy claims. | THAI-004–THAI-009. |

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
