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
