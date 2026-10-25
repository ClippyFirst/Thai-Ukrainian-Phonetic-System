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
| THAI-005 | P1 | IN_PROGRESS | Source-backed `รร` lexical segmentation is now added for `สรรพคุณ`, `สรรพสินค้า`, and `สรรพนาม` from the Office of the Basic Education Commission learning resource (p. 29); PR #61 merged as `50e854bead2e71ecd6adb20030387fe6532be2ae`. Exact-head CI [40220350547](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40220350547) passed Python tests and the 351,780-row master-artifact job. | Continue auditing `ฤ/ฤๅ`, `ฦ/ฦๅ`, thanthakhat/silent letters and `อ นำ`; keep the three `รร` items lexical exceptions, not a productive rule or IPA gold. |
| THAI-006 | P1 | IN_PROGRESS | PR #64 established the cross-runtime Unicode contract; PR #66 adds explicit-boundary regressions in Python/browser for ASCII space/tab/CR/LF splitting and ensures VT/FF are rejected rather than silently treated as layout. PR #66 merged as `18ab41db87192dc7be69683ef85e53cb04db5517`; exact-head CI [40224809393](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40224809393) passed both test and master-artifact jobs. | Broader unknown-input and lexical word-boundary coverage remains; current Unicode/boundary tests are integrity checks, not phonetic accuracy evidence. Post-merge main CI/Pages for this merge must be checked before reporting the branch green. |
| THAI-BOUNDARY-001 | P1 | DONE_VERIFIED | Explicit layout-whitespace boundary tests now exercise Python `parse_thai` and browser `analyzeText`; VT/FF embedded in a syllable are retained as unsupported input and cannot yield IPA/Ukrainian output. PR #66 merged as `18ab41db87192dc7be69683ef85e53cb04db5517`; exact-head CI [40224809393](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40224809393) passed the Python/browser/parity and master-artifact jobs. | These checks verify input integrity and API contracts, not pronunciation accuracy. |
| THAI-UNICODE-001 | P1 | DONE_VERIFIED | Add regression coverage for NFC/trim idempotence, normalized code-point indices, C0/C1 controls, zero-width space, bidi override, U+0085 and Python/browser tokenization. PR #64 merged as `4ba2f794185b43990ee213951b2df4c8fa451586`; exact-head CI [40223490715](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40223490715) passed. | This is Unicode/input-integrity evidence, not a pronunciation benchmark. Post-merge main CI/Pages were in progress when this checkpoint was prepared. |
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


## Source-backed รร lexical segmentation — 2026-10-25

- PR [#61](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/61) merged as `50e854bead2e71ecd6adb20030387fe6532be2ae`.
- Added the Office of the Basic Education Commission learning resource, “การอ่านพยางค์ที่มี รร (รอหัน)” (p. 29), to `data/thai/sources.csv` and linked it to `SP-RR-001`. Source: https://academic.obec.go.th/images/document/1649041534_d_1.pdf
- Added curated lexical syllabifications `สรรพคุณ → สับ|พะ|คุน`, `สรรพสินค้า → สับ|พะ|สิน|ค้า`, and `สรรพนาม → สับ|พะ|นาม`. Regression tests confirm these reviewed syllable forms reach the existing IPA→Ukrainian adapter.
- Exact-head CI [40220350547](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40220350547) passed both jobs: Python tests, generated checks, browser IPA/UA, parity/UI contracts, and the 351,780-row master-artifact assertions.
- The source supplies reading/syllabification, not IPA labels. These are lexical segmentation cases, not a productive `รร` rule and not independent IPA gold. Unknown/ambiguous `รร` forms remain evidence-gated.
- Remaining THAI-005 work: `ฤ/ฤๅ`, `ฦ/ฦๅ`, thanthakhat/silent letters and `อ นำ`; THAI-008 independent adjudicated gold evaluation remains open.


## Unicode input-contract checkpoint — 2026-10-25

- PR [#64](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/64) merged as `4ba2f794185b43990ee213951b2df4c8fa451586`.
- Python and browser now use a consistent explicit ASCII layout-whitespace set for outer normalization and tokenization. The Python syllable-list API no longer uses broad `str.split()`, which had silently treated U+0085 NEXT LINE as a separator while the browser rejected it.
- Added tests for normalization idempotence and index consistency, C0/C1 controls, U+200B ZERO WIDTH SPACE, U+202E RIGHT-TO-LEFT OVERRIDE, and U+0085 across Python syllable/text APIs and browser tokenization.
- Exact-head full CI [40223490715](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40223490715) passed Python tests, generated-data drift checks, browser IPA→Ukrainian, parity/UI contracts and the master-artifact job (351,780 rows, 41 vowel records). Static validation [40223494258](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40223494258) passed.
- Post-merge main CI [40223983615](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40223983615) and Pages deployment [40223983567](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40223983567) were in progress when this checkpoint was authored; verify final state before claiming post-merge green.
- THAI-006 remains IN_PROGRESS for broader explicit-boundary and unknown-input coverage. The Unicode fix is an input-integrity improvement, not empirical pronunciation accuracy. Independent Thai lexical IPA gold remains 0.


## Explicit whitespace-boundary checkpoint — 2026-10-25

- PR [#66](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/66) merged as `18ab41db87192dc7be69683ef85e53cb04db5517`.
- Fixed the tests to exercise the correct APIs: `analyzeText` for tokenized text boundaries and `analyze` for a single-syllable input. The earlier draft incorrectly expected `analyze` to return a `syllables` list; exact-head CI exposed that test-contract error, which was corrected rather than weakening runtime validation.
- Python and browser tests now verify ASCII space/tab/CR/LF split two supplied Thai tokens; vertical tab and form feed remain unsupported symbols and must not produce IPA/Ukrainian output.
- Exact-head CI [40224809393](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40224809393) passed both the test job and the 351,780-row master-artifact job. Earlier failing runs [40224159637](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40224159637) and [40224159615](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40224159615) are retained as history, not treated as passing.
- Main CI and Pages for the merged head were in progress when this checkpoint was authored; verify those exact runs before claiming post-merge green.
- This closes one boundary-contract gap only. THAI-006 remains IN_PROGRESS; lexical segmentation coverage and independent Thai IPA gold remain open.


## Segmentation, independent gold, benchmark and parity checkpoint — 2026-10-25

### Starting state and preserved implementation

- Branch created from the current `main` ref: `research/thai-segmentation-gold-parity-20261025`. Current main's latest observed commit is `0be5fd841070e337cb5c805ef92954938abe61bb` (explicit whitespace-boundary verification documentation); the branch is intended to carry only this checkpoint's evidence and acceptance-gate updates.
- Existing code was inspected before changes: `src/thai_ukrainian/lexicon.py` already has an evidence-backed TSV lexicon loader and strict `segment_word` that raises `KeyError` for an unknown entry; `segment_text` requires explicit word tokens. The repository already has `scripts/evaluate_corpus.py`, `scripts/benchmark_ipa.py`, `tests/test_benchmark_ipa.py`, `data/benchmark/gold.tsv` and `data/benchmark/predictions.tsv`. The benchmark TSVs are header-only; there are zero adjudicated gold rows, so no accuracy score can be computed. These modules and files are reused, not duplicated.
- The current mainline also contains the 36-input external G2P smoke evidence and an external renderer registry. Prior runs are diagnostics only: 36 inputs × 3 engines gave 108 output rows, with thaiphon 36/36 non-empty, FastThaiG2P 36/36, Goruut 26/36; there were 88 pairwise comparisons and 13 exact agreements in one pinned report. Independent gold was 0 and accuracy was null. Goruut also showed unstable repeated outputs. Do not interpret engine agreement as accuracy or enable these candidates in production.

### Newly verified external resources (candidate status, not adopted gold)

- **CCOST** — Zenodo v1.0, DOI [10.5281/zenodo.17366698](https://doi.org/10.5281/zenodo.17366698), published 2025-10-16; includes audio and TextGrid annotations, about 7 hours spontaneous plus 5 hours controlled Standard Thai from 49 speakers, word-list/sentence tasks, metadata and an annotation manual. Dataset license is **CC BY-NC-SA 4.0**. It is the strongest found candidate for acoustic/phonetic adjudication, but the non-commercial/share-alike terms must be honored; it must not be bundled or mirrored in this MIT code repository. The released package is 6.2 GB, so use a local, manifest-pinned download and store only permissible metadata/hashes and derived evaluation rows. Verify each annotation layer and speaker/task split before using as phonetic gold.
- **PyThaiNLP Thai G2P Wiktionary corpus** — [upstream repository](https://github.com/PyThaiNLP/thai-g2p-wiktionary-corpus) declares CC BY-SA 3.0 and provides 2020/2022 TSV snapshots. It is a useful source-attested IPA regression candidate, but it is Wiktionary-derived and overlaps with FastThaiG2P provenance; it is **not independent gold** and must not be the sole held-out benchmark against Wiktionary-derived systems.
- **BEST / InterBEST 2010 and LST20 word-boundary resources** — the [NLP for Thai corpus index](https://nlpforthai.com/tasks/word-segmentation/) lists word-boundary corpora, including BEST I (CC BY-SA-NC 4.0; access may require registration), Blackboard Treebank (CC BY 3.0), Wisesight samples (CC0-1.0), and VISTEC-TP-TH-21 (CC BY-SA 3.0). These are segmentation resources, not pronunciation gold. Prioritize a license-compatible, held-out word-boundary test set (Wisesight-1000/CC0 for a small smoke; Blackboard Treebank/LST20 for broader evaluation after checking exact upstream files and terms). Do not redistribute restricted BEST data.
- Published segmentation comparisons report high F1 on BEST-2010 (e.g. LATTE 0.9907 in an indexed benchmark table), but those figures are external, task/split-specific and not a ClippyFirst result. Never compare them directly with the current explicit-lexicon segmentation API; first define tokenization contract, dataset split, Unicode normalization and metric.

### Task ledger

| Task | Status | Evidence / acceptance criterion |
|---|---|---|
| Explicit lexical segmentation and source-backed exceptions | PARTIAL | TSV lexicon and source-attested `รร`/`ทร`/`ศรี` entries exist; unknown words must remain unresolved. Expand coverage only from exact lexical sources; never turn a small lexicon into a claimed general Thai tokenizer. |
| Independent pronunciation gold | TODO / BLOCKED BY ADJUDICATION | CCOST is identified and licensed for non-commercial research; select and adjudicate a stratified subset with a native phonetician, exact audio/TextGrid locator, profile, annotation layer and competing analyses. No independent adjudicated rows are present yet. |
| Word segmentation benchmark | TODO | Acquire a permissible word-boundary corpus and pin version/hash/split; compute boundary precision/recall/F1 and exact segmentation; report domain coverage and unknown-word handling separately. |
| IPA benchmark and external G2P comparisons | PARTIAL | Harness exists and is fail-closed; current gold/prediction TSVs have headers only. Re-run all comparators against the same adjudicated held-out forms and retain raw output, version, status, missing predictions and source provenance. |
| Python/browser parity | PARTIAL / engineering gate | Python and browser implementations and parity fixtures/tests exist. Run exact-head CI and generated-artifact checks; add parity fixtures only from reviewed gold or clearly labelled engineering probes. CI parity is not evidence of linguistic correctness. |
| Repository-local skills audit | BLOCKED BY TOOLING VISIBILITY | The GitHub connector can fetch known file paths but its file search returned no results for `skill`/`AGENTS.md`, and no tree-listing operation was exposed in this run. Do not claim the repo-local skill inventory was fully inspected or applied; locate and review the actual skill files before marking this complete. |

### Commands / verification boundary

- Repository-defined local commands remain: `python scripts/generate_derived.py`, `python scripts/generate_syllable_space.py`, `python -m unittest discover -s tests -v`, and `python scripts/evaluate_corpus.py path/to/records.jsonl`; browser parity/UI checks are wired into CI. The connector environment does not provide a local checkout or command runner, so these commands were **not executed in this session**. No test pass is claimed for this branch until its exact-head CI finishes.
- No corpus data was downloaded or copied into the repository. No new linguistic labels or scores were fabricated. Next acceptance step: run CI on this branch, then build a non-commercial CCOST-based, independently reviewed subset and a separate license-compatible segmentation holdout; only then compute scores.


## Segmentation evaluator implementation checkpoint — 2026-10-25

- Added `scripts/evaluate_segmentation.py`, a standard-library-only evaluator that scores only adjudicated rows with source/license/split provenance, validates exact NFC token concatenation without dropping whitespace, and reports boundary precision/recall/F1, exact token-sequence rate and prediction coverage separately. Missing predictions remain in the gold denominator; an empty gold set reports `NOT_MEASURED`, not a fabricated score.
- Added `tests/test_segmentation_benchmark.py` for exact segmentation, boundary-vs-sequence differences, missing predictions, no-gold status, provenance/concatenation rejection and Unicode normalization. The current fixtures are synthetic software tests only and are not Thai accuracy data.
- Files were created on this dedicated branch; the repository's unittest discovery should pick up the new test file. **Tests were not executed locally** because this connector session has no repository checkout/command execution. Exact-head CI is the required verification gate; do not mark the implementation DONE_VERIFIED until that run passes.
- The evaluator is a first practical deliverable for the segmentation benchmark, not an automatic Thai segmenter and not a substitute for a licensed held-out corpus. No external corpus was copied into the repository.


## Exact-head verification follow-up — 2026-10-25

### Verified result

- PR #71 head `13dbac32a9ce96f52c8bc6b20e113a6af046145b` was checked against GitHub Actions run [40227311442](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40227311442). Both jobs completed successfully: `test` and `master-artifact`.
- The `test` job passed package installation, `scripts/generate_derived.py`, `scripts/generate_syllable_space.py`, generated-artifact drift check, `scripts/generate_master_table.py`, `python -m unittest discover -s tests -v`, `node web/tests/ipa-ua.test.mjs`, `node web/tests/parity.test.mjs`, and `node web/tests/ui-contract.test.mjs`.
- The `master-artifact` job passed master-table generation and asserted `rows == expected_rows == 351780` and `vowel_records == 41`, then uploaded the artifact.
- Therefore the software/evidence-gate changes in this PR are CI-verified on the exact PR head. This does **not** verify Thai lexical segmentation or phonetic accuracy. The 36-form challenge still has no adjudicated IPA/word-boundary gold; external G2P agreement is diagnostic only.
- The static lexicon audit found 23/36 exact challenge-form matches (63.9%) and 13/36 misses. This is a lookup-coverage count on a hand-picked adversarial set, not engine accuracy, not population coverage, and not a release metric. Unresolved multi-grapheme text must continue to abstain rather than invent IPA/Ukrainian output.
- Local execution remains unavailable in the current environment because resolving `github.com` from the container failed. The successful remote CI run is the test evidence; do not describe tests as locally executed.
- PR #71 remains a draft intentionally: its software acceptance checks pass, but independent adjudication and license/source review of a representative gold set are still blockers for any accuracy claim. Do not merge it automatically or mark empirical accuracy complete.

### Updated task ledger

| Task | Status | Evidence / acceptance criterion |
|---|---|---|
| Segmentation scorer, provenance gates, malformed/duplicate-ID checks | DONE_VERIFIED | Exact-head CI run 40227311442 passed Python test discovery. |
| Generated data and master artifact reproducibility | DONE_VERIFIED | Same run passed drift check and 351,780-row / 41-vowel assertions. |
| Browser IPA→Ukrainian parity and UI contract | DONE_VERIFIED | Same run passed all three Node checks. |
| Runtime diagnostics across all 36 challenge inputs | PARTIAL | External comparator smoke exists; ClippyFirst lexical lookup audit is static only. Add a reproducible engine-run report without treating it as gold accuracy. |
| Representative Thai word-boundary and IPA gold | BLOCKED | Requires independently reviewed source attestations, scope/profile metadata, licensing review, and human adjudication; acceptance requires non-empty eligible records plus reproducible scoring. |
| Full lexical segmentation and special-orthography coverage | TODO | Add only evidence-backed entries/rules with regression tests; unknown words must remain explicitly unresolved. |


## Runtime challenge diagnostic — exact-head CI verified (2026-10-25)

- PR #71 branch `research/thai-segmentation-gold-parity-verified-20261025`, exact head `8a98c30cd47a7844696211550a9c2bc2b9e5931a`.
- Full CI run [40227910891](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40227910891) completed successfully on that exact SHA. Both jobs passed: `test` and `master-artifact`.
- Test job passed editable package install; `scripts/generate_derived.py`; `scripts/generate_syllable_space.py`; generated-artifact drift check; `scripts/generate_master_table.py`; `python -m unittest discover -s tests -v`; `scripts/run_challenge_diagnostics.py --output /tmp/challenge-runtime-diagnostics.json`; the guard asserting exactly 36 inputs are accounted for, diagnostic-only evaluation kind and absence of an accuracy field; and Node checks `web/tests/ipa-ua.test.mjs`, `web/tests/parity.test.mjs`, `web/tests/ui-contract.test.mjs`.
- Master-artifact job passed generation, asserted `rows == expected_rows == 351780` and `vowel_records == 41`, and uploaded the generated artifact.
- Duplicate workflow run [40227913467](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40227913467) was still in progress at the last poll; run 40227910891 is the completed successful evidence for the same exact head. Do not infer linguistic correctness from either CI run.
- The runtime diagnostic is now executed in CI and regression-tested; it is still a runtime behavior report, not an accuracy benchmark. The 36-form static lexicon lookup count remains 23/36 (63.9%) on this deliberately selected challenge set and is not general coverage or accuracy.
- Remaining gates: independently adjudicated Thai word boundaries and IPA/tone/vowel-length labels with exact source locators and license review; broaden lexicon/segmentation only with source-backed entries; separately resolve `รร`, `ฤ/ฤๅ`, `ฦ/ฦๅ`, `ทร`, silent-letter constructions and connected speech. PR #71 remains draft because these research gates are not satisfied.


## One-pass segmentation benchmark hardening — 2026-10-25

### Branch, exact-head verification and implementation result

- Dedicated branch: `research/thai-segmentation-gold-parity-verified-20261025`, based on current `main` `0be5fd841070e337cb5c805ef92954938abe61bb`. Code-bearing commit: `b1f67a881d17a356f73712877dd71f4287b5bba3`.
- GitHub Actions run [40229701920](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40229701920): the exact-head `test` job passed. It ran generated-data regeneration and drift checks, master-table generation, **143 Python tests**, the 36-record ClippyFirst runtime diagnostic plus guards against reporting accuracy, and Node checks `web/tests/ipa-ua.test.mjs`, `web/tests/parity.test.mjs`, and `web/tests/ui-contract.test.mjs`. Python/browser parity reports 27 fixtures passed. At the time this checkpoint was written, the separate `master-artifact` job for this SHA was still running its artifact generation/upload step; do not claim that job completed until the workflow reports success. The equivalent artifact job on predecessor SHA `693caa3ca1a7ae04b0fb7259aa40e63fd3fa5e23` passed in run [40229604077](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40229604077), asserting 351,780 structural rows and 41 vowel/rime records and uploading the artifact.
- Local test execution remains unavailable: the container could not resolve `github.com` and this connector session has no local checkout/command runner. The evidence is remote GitHub Actions, not a claimed local run.

### Concrete evaluator fixes

- Segmentation predictions are scoreable only when `status=ok`. Error, abstention, partial, or other statuses cannot receive credit even if a stale token array is present; the report counts non-success status rows explicitly. This closes a real scoring-integrity defect.
- Boundary F1 now uses `2TP / (2TP + FP + FN)`: it is 0 when one side has boundaries but there are no true positives, and undefined only when both boundary sets are empty. Added a regression test for the zero-predicted-boundary case.
- The ClippyFirst challenge diagnostic now fails closed on an empty JSONL input instead of emitting a vacuous success report.
- The current 36-form runtime diagnostic reports 23 lexicon-resolved forms and 13 unresolved forms; 21 inputs emitted complete engine output and 15 abstained or lacked complete output. It counted 30 syllable analyses as `analyzed` and 3 as `analysis-dependent:special-orthography`. These are diagnostics on a hand-picked adversarial set, **not** accuracy or representative corpus coverage.

### Reconciled task ledger

| Task | Status | Evidence / remaining acceptance criterion |
|---|---|---|
| Segmentation scorer: provenance, NFC concatenation, unique IDs, missing-prediction denominator | DONE_VERIFIED | Synthetic regression tests pass in exact-head CI; no empirical corpus score is claimed. |
| Failed/partial prediction status gating and zero-boundary F1 edge case | DONE_VERIFIED | Exact-head CI run 40229701920 passed the new regression tests. |
| Empty challenge input rejection and 36-input runtime diagnostic | DONE_VERIFIED | Exact-head CI passed the diagnostic and guards; report explicitly omits accuracy. |
| Generated data, master-table generation, Python/browser IPA→Ukrainian parity and UI contract | DONE_VERIFIED for the passing `test` job | 143 Python tests; 27 parity fixtures; all three Node checks passed. The separate artifact-upload job for this exact SHA must be confirmed before claiming exact-head artifact publication. |
| Challenge lexicon lookup | PARTIAL | 23/36 on this hand-selected challenge set; 13/36 remain unresolved. This is neither population coverage nor pronunciation accuracy. Expand only with source-backed entries and tests. |
| Independent Thai IPA, tone, vowel-length and word-boundary gold | BLOCKED BY ADJUDICATION | No independently adjudicated rows exist. Requires a licensed, version-pinned source, exact locators, a declared Standard Thai profile/split, and independent expert review of competing analyses before scoring. |
| General Thai word segmentation | PARTIAL / EVIDENCE-LIMITED | Unknown multi-grapheme input abstains safely. The segmentation scorer is ready, but gold manifests are header-only and a versioned, license-compatible holdout has not been processed. |
| Special orthography (`รร`, `ฤ/ฤๅ`, `ฦ/ฦๅ`, `ทร`, silent letters) | PARTIAL | Existing rules/lexical exceptions remain conservative and word-/sense-dependent. PR #68 adds official OBEC scope evidence and has successful CI on its own head, but is a separate, non-mergeable branch and was not merged or ported blindly. It does not supply universal IPA gold. |
| Connected speech and empirical Ukrainian orthographic preference | BLOCKED BY EVIDENCE | Requires acoustic/phonetic material and separately adjudicated Ukrainian target preferences; no scores or calibrated probabilities may be inferred from current output. |
| Repository-local skills inventory | DONE_VERIFIED — none found | Recursive Git tree inspection of the 172-entry branch tree found no `skills/`, `AGENTS.md`, `SKILL.md`, or `.github/instructions` paths. Project matrices/plans and existing tests were used; do not claim repo-local skills were applied. |

### PR and branch reconciliation

- PR #71 remains open and draft; no merge was performed. Its benchmark infrastructure is software-verified, while empirical pronunciation/segmentation accuracy remains unmeasured.
- PR #68 (`research/thai-special-vowel-source-contract-20261025`, head `4e03079d48a4b05470bfbb498c22e0b39de50185`) is independently scoped to official-source evidence for special vowel letters and lexical `อ นำ`. Its exact-head CI runs [40225937524](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40225937524), [40225937608](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40225937608), and [40225932880](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40225932880) succeeded. GitHub reports it 14 commits ahead and 1 behind current `main`, with `mergeable=false`; leave it untouched until its mergeability/conflicts are explicitly reconciled.
- PRs #69 and #70 are closed, unmerged duplicate/superseded segmentation-benchmark attempts. Their branches were not deleted. No other PR was merged or altered.

### External evidence and stop condition

- CCOST v1.0 (DOI `10.5281/zenodo.17366698`) remains a candidate for non-commercial phonetic adjudication under CC BY-NC-SA 4.0; its corpus was not downloaded, mirrored, or bundled. The Wiktionary-derived G2P corpus remains source-attested regression material, not independent gold against systems with overlapping provenance.
- The segmentation-corpus index is discovery metadata only. Exact upstream version, license, annotation convention, split and hash must be verified before populating gold TSVs. Synthetic test fixtures must never be represented as Thai accuracy evidence.
- Readiness: **research software prototype with verified engineering infrastructure; not empirically validated and not release-ready for arbitrary Thai text**. The remaining blockers are evidence/adjudication and representative lexical coverage, not missing benchmark plumbing.



## 2026-10-25 follow-up — permissive segmentation evidence and source-attested IPA

### Changes prepared on `research/thai-evidence-gated-coverage-20261025`

- Five source-attested entries were added to `data/thai/text_lexicon.tsv`: `ไกล`, `ใกล้`, `เดิน`, `กรรม`, `บรรจุ`. Exact Thai Wiktionary revision URLs, source claim scopes, and CC BY-SA 4.0 attribution are recorded in `data/thai/text_lexicon_sources.csv`; the share-alike scope is explained in `data/thai/TEXT-LEXICON-DATA-LICENSE.md`.
- `เงิน` was deliberately **not** added as a normal runtime lexicon entry. Its source gives /ŋɤn˧/ with short /ɤ/, while the existing graphemic parser has a known lexical-length ambiguity. The text lexicon cannot encode a typed IPA override, so enabling it as ordinary graphemes risks wrong output.
- Added `data/benchmark/segmentation-gold.tsv` with 993 source-annotated human word-tokenization rows from Wisesight. Exact upstream commit `c1d063649abc3a6870b5fd1aae26cd1c64bdde7b`, source blob SHA-1 `279aeb2d4323fd8032306160144d33dcb5b2df84`, license CC0-1.0. All rows are test-only in this repo and status `SOURCE_ANNOTATED`; no claim of expert adjudication or inter-annotator agreement.
- Added source provenance/conversion contract at `data/benchmark/wisesight1000-source.json`; added six revision-pinned dictionary IPA records in `data/benchmark/source-attested-ipa.tsv`, all labeled `SOURCE_ATTESTED_NOT_GOLD`.
- Updated `scripts/evaluate_segmentation.py` so source-annotated and expert-adjudicated labels cannot be mixed in a single score, and whitespace-only boundaries do not inflate lexical boundary metrics. Added `scripts/run_wisesight_segmentation_diagnostic.py` and CI assertions/artifact upload.
- Tests added for source annotation grade, whitespace boundary semantics, exact 993-row data reconstruction, five lexical entries, and the source-attested IPA registry.

### Verification ledger for this batch

- **PARTIAL — CI pending at the time of this handoff.** No local tests were run; the available session has GitHub file/branch APIs but no local checkout/command runner. Wait for exact-head CI on this branch before marking new code/data gates DONE_VERIFIED.
- Expected evidence: full Python suite; generated-data drift check; master-table generation and 351,780-row/41-vowel assertion; Node IPA→UA, browser parity and UI contract; new Wisesight 993-row diagnostic artifact.
- New boundary benchmark outcome must be reported as `SOURCE_ANNOTATED`, not independent expert gold. Its baseline is a no-automatic-segmentation diagnostic; do not advertise it as a production segmenter score.

### Remaining genuine blockers

1. **BLOCKED — independent IPA/tone/vowel-length gold:** requires CCOST annotation-manual/license review, a pinned speaker-aware sample, and independent Thai phonetic adjudication with disagreements logged.
2. **TODO — typed lexical IPA override:** preserve `เงิน /ŋɤn˧/` through the typed IPA result and Ukrainian adapter with provenance and Python/browser parity; do not use a source grapheme workaround.
3. **PARTIAL — special orthography:** `รร`, `ฤ/ฤๅ`, `ฦ/ฦๅ`, `ทร` and silent-letter readings remain lexical/context-dependent.
4. **BLOCKED — connected speech and Ukrainian preferences:** requires acoustic labels and a separate Ukrainian target-preference set.


### Exact-head acceptance checklist for the new corpus batch

- [ ] `python -m unittest discover -s tests -v` passes, including the new Wisesight integrity and source-attested IPA registry tests.
- [ ] `python scripts/run_wisesight_segmentation_diagnostic.py --output /tmp/wisesight1000-segmentation-baseline.json` succeeds and reports exactly 993 `SOURCE_ANNOTATED` rows, zero `ADJUDICATED` rows, and no expert-gold claim.
- [ ] Generated-data drift check remains clean; the structural master generator still validates 351,780 rows and 41 rime records.
- [ ] Node IPA→UA, browser parity, and UI contract tests pass.
- [ ] The CI artifact `wisesight1000-segmentation-baseline` is uploaded and inspected before the task is marked DONE_VERIFIED.
- [ ] Recompute the 36-form challenge runtime diagnostic; expected static lexicon lookup count is 28/36 after five source-backed additions, but the CI report—not this expectation—defines the verified outcome.

Do not merge PR #71 or call the repository empirically validated solely because these gates pass. The source-annotated boundary benchmark is a real improvement over empty TSVs, while expert IPA/tone/length gold and the lexical IPA override for `เงิน` remain separate gates.


## Final verification checkpoint — 2026-10-25

- **Starting branch head for this follow-up:** `7e39fd4bc108386148c1e9a79d257d75babcc9aa`.
- **Code-bearing acceptance commit:** `818a378d37b248d74628243b9a8d62fb82029815`.
- **CI:** [run 40233825012](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40233825012) passed both jobs, `test` and `master-artifact`.
- **Commands verified in CI:** `python scripts/generate_derived.py`; `python scripts/generate_syllable_space.py`; generated-artifact drift check; `python scripts/generate_master_table.py`; `python -m unittest discover -s tests -v` (150 passed); `python scripts/run_challenge_diagnostics.py --output /tmp/challenge-runtime-diagnostics.json`; Node `web/tests/ipa-ua.test.mjs`, `web/tests/parity.test.mjs`, `web/tests/ui-contract.test.mjs`; `python scripts/run_wisesight_segmentation_diagnostic.py --output /tmp/wisesight1000-segmentation-baseline.json`; 993-row/status/coverage assertions; master artifact assertions for 351,780 rows and 41 vowel/rime records.
- **Challenge diagnostic:** 36 forms; 28 lexicon-resolved, 8 unresolved; 25 complete engine outputs and 11 abstentions/incomplete outputs. This is not accuracy.
- **Wisesight baseline:** 993 source-annotated rows, full prediction coverage; boundary precision 0.638319, recall 0.091858, F1 0.160604, exact sequence rate 0.031219. The source labels are not expert-adjudicated. Uploaded artifact ID `12614106636`.
- **Generated master artifact:** job passed the 351,780-row and 41 vowel/rime assertions; uploaded artifact ID `12613439376`.
- **Initial failure and repair:** run `40233445474` found a generated-audit artifact drift after adding `text_lexicon_sources.csv`; the generated JSON was regenerated into exact expected key order. Run `40233522119` then exposed a stale test fixture expecting `ไกล` to remain unresolved after it had been added to the lexicon. The fixture was corrected to use unsupported `กฉ`; final run `40233825012` passed.
- **PR #71:** remains open and draft; no merge or release was performed. PR #68 remains untouched because it is a separate conflicting branch and has its own official-source scope.
- **Final readiness:** engineering-verified research prototype with source-annotated segmentation baseline. Not release-ready for arbitrary Thai text; no independent expert/acoustic IPA, tone, or vowel-length gold exists. `เงิน` remains excluded from the runtime lexicon pending a typed lexical-IPA override. `รร`, `ฤ/ฤๅ`, `ฦ/ฦๅ`, `ทร`, silent-letter contexts, connected speech and Ukrainian preference remain evidence-gated.

The audit/matrix/handoff edits after the code-bearing commit are documentation-only. Verify the latest branch head's CI before treating the final branch state as fully green.


### Last verified docs checkpoint

- Documentation head `b3eaddde55de0474e47abe01ece7692467f1a229` passed both jobs in [CI run 40234324067](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40234324067).
- After that successful run, only the final audit JSON status wording and this matrix/handoff checkpoint were updated; no source code, test logic, or benchmark data changed. The latest docs-only head must still complete CI before this run is closed.
- Keep the readiness split explicit: engineering gates pass; independent phonetic adjudication and a safe lexical IPA override for `เงิน` do not.
