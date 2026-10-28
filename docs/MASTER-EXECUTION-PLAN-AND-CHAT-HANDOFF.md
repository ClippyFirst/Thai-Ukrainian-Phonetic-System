## 2026-10-27 — super-soft full-coverage mode (verification checkpoint)

- Branch: feat/supersoft-full-coverage-20261027. Code commit verified: 6f53ca955a2702db8e070a04c181dbb68d6d6900, based on main 9c527e46b3fa012e277c8914683ae70834165a22. Follow-up documentation-only checkpoint: 502940ea61005b8b3494d074688301d23a1aeb29.
- Draft PR #105: https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/105. Not merged or deployed.
- Added opt-in super-soft mode with approximate segmental IPA for unreviewed Thai fragments and Ukrainian output derived only through the existing IPA adapter. Continuous Thai output has regression coverage for no unresolved placeholders; non-Thai spans, punctuation, spacing and numbers remain intact.
- **DONE_VERIFIED for code commit 6f53ca955a2702db8e070a04c181dbb68d6d6900:** Web static validation run 40577745185 passed. Full CI run 40577745331 completed successfully, including the master-artifact job. The CI test job passed Python unittest discovery, IPA adapter tests, browser parity, UI contract, challenge and segmentation diagnostics, source-attested IPA diagnostics, and browser latency benchmark. The later commit 502940ea61005b8b3494d074688301d23a1aeb29 changed documentation only; its CI run 40578911871 was still in progress at its latest check.
- PR #104 (research-only morphology) remains open and overlaps web/src/app.js, web/src/engine.js, web/tests/parity.test.mjs, web/tests/ui-contract.test.mjs, README and audit/handoff documents. Keep #105 draft and do not merge blindly; reconcile/rebase after #104's disposition. PR #101 is the earlier competing morphology branch and remains untouched.
- Evidence boundary: full output coverage is an engineering contract, not evidence of correct Thai word boundaries, lexical pronunciation, tone, proper names or Ukrainian target spelling. Research status remains a partial prototype, not release-ready.

## 2026-10-27 — direct IPA adapter merged; published-site verification in progress

- **Merged to `main`:** PR [#103](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/103) added fail-closed malformed delimiter handling to PR [#102](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/102)'s branch; PR #102 was then merged to main. Main merge commit: `070687575026ebc6d5d5dabdd0bb7bf647656bfc`.
- **Exact-head verification passed before merge:** CI run [40569408788](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40569408788) completed successfully, including `test` and `master-artifact`; Web static validation [40569408783](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40569408783) also passed. The tested code head was `e9295d26f41f278848396913b19b3877c2935c01`; it is the code head integrated by the main merge.
- Direct website IPA → Ukrainian panel uses the same browser adapter as the main pipeline. Python and browser implementations are both present; the Python adapter is suitable for scripts, batch processing, and integrations. Cross-runtime tests are included in CI. This does not mean the Python module is itself running inside the browser.
- Added a Pages workflow acceptance check in commit `3a69b65de3a42f8573e6106061702230638c52cf` to verify live `ipa-input`, `ipa-adapt`, `ipa-adapter-result` and `src/ipa-ua.js`, including malformed-delimiter rejection. **The Pages deployment outcome has not yet been independently confirmed in this session**; do not state that the public website is updated until this workflow's deploy job succeeds.
- Documentation reconciliation commits: validation matrix `8cb7148a2f59d5284f9d55f3993bf52a7254e235`; audit JSON `3df07488522cc20c19c60063bc07a4ced80b2644`. These update the existing artifacts in place.
- **Remaining release blockers:** (1) verify live Pages deployment contract; (2) independent adjudication of Thai IPA and Ukrainian practical outputs on a representative gold set; (3) resolve TLTK contradictory license scope and audit any external model/dictionary provenance before importing; (4) finish broader language-coverage and arbitrary-text evaluation. Current status remains **partial research prototype, not release-ready**.
- No local tests were run in this session; GitHub Actions is the verification evidence. The merge was based on successful exact-head CI and web static validation.

---

## Continuation — malformed IPA delimiter rejection (2026-10-27)

- Working branch: `fix/ipa-normalization-audit-20261027`, based on PR #102 code head `a85452f9623b87f1d3270df9eb8f29efb0542fbd`.
- Added fail-closed validation in both Python and browser IPA adapters for unmatched or mixed outer delimiters. Previously strings such as `[kʰaː/`, `/kʰaː]`, `[kʰaː`, and `kʰaː]` could reach token parsing and be treated as merely unsupported characters rather than malformed notation; they now return `withheld` before normalization.
- Added matching regression cases to `tests/test_ukrainian_adaptation.py` and `web/tests/ipa-ua.test.mjs`.
- Implementation commits: Python `e70ddd43946cd9fe25d886da3f697a5389c8ae8e`; browser `b3d11e927a36f87646e24863fb5f65e14b9f0acc`; tests `bfe33ba25fecb0db10ca351f8d28605449c47a93` and `db6316125ca19a036740ecc55bcad720afbd0c9d`. The validation matrix, final audit JSON, and this handoff were updated in the same branch.
- Exact-head CI and static validation are pending. The connector's workflow-run lookup returned no PR-triggered runs for the new head before a PR was opened; no local checkout/test execution was available. Do not mark this fix DONE_VERIFIED until CI runs on the final branch HEAD.
- This fix validates delimiter syntax only. It does not establish expert correctness of IPA, tone interpretation, or Ukrainian target forms. PR #101 morphology remains separate and research-only.

---

# Latest continuation — direct IPA recognition and Ukrainian adapter hardening (2026-10-27)

- Dedicated branch `feat/ipa-input-adapter-robustness-20261027`; PR [#102](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/102) remains open pending exact-head verification and integration. PR #101 morphology work remains separate.
- Added a website panel for externally sourced IPA. It calls the same IPA → Ukrainian adapter as the main Thai→IPA path and displays normalized segmental IPA, the Ukrainian practical candidate, applied rules, and recognized/neutralized features.
- Both Python and browser adapters support common wrappers, Thai tone letters and selected combining tone marks, stress, length, selected phonetic modifiers, and tied `t͡ɕ` notation. Unknown segments and tone-only input are withheld.
- Quality hardening: removed U+0306 combining breve from the automatic tone-mark deletion set. A breve can mark extra-shortness, so the adapter now preserves it as an unsupported distinction and withholds the output. Python/browser regression tests cover this fail-closed case.
- Previous code head `ba3771e29b7554325c4b63cb3c39e2356e414066` passed CI [40559473200](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40559473200) and Web static validation [40559473259](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40559473259). Current code head `ff27ebdcfb3c0d45bfc82943fbfd93b4f055708b` is pending because GitHub Actions runs are queued; do not claim its tests passed until those exact-head runs finish.
- Local execution is unavailable in this session because the environment could not resolve `github.com`; CI is the available verification route.
- Evidence boundary: parser support does not certify the lexical correctness of arbitrary IPA or independently adjudicated Ukrainian spelling. Project remains a partial research prototype.

---

# Master execution plan and chat handoff — Thai → Ukrainian Phonetic System

## Latest continuation — source-attested Ukraine/Eastern Europe article forms and parser gap (2026-10-27)

- Dedicated PR [#98](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/98), branch `feat/source-attested-east-thai-lexicon-20261027`, now includes `ตะวันออก` → `ตะ|วัน|ออก`, `ยุโรป` → `ยุ|โรป`, and `ยุโรปตะวันออก` → `ยุ|โรป|ตะ|วัน|ออก`. Sources are pinned to en.wiktionary revisions 86398986, 91325849 and 87721830 (CC BY-SA 4.0).
- Exact-head CI first exposed a real engine defect: the Python text test received `None` rather than IPA for the final syllable `ออก`. The PR was not merged. A follow-up adds a source-pinned `ออก` lexical IPA override (`ʔɔːk`, long vowel, low tone), Python/browser parity fixture and typed IPA → Ukrainian assertions (`ок`); the full phrase `ตะวันออก` yields `таванок`.
- Additional regression tests assert `ยุโรป` source IPA `/ju˦˥.roːp̚˨˩/` and the five-syllable phrase `ยุโรปตะวันออก` `/ju˦˥.roːp̚˨˩.ta˨˩.wan˧.ʔɔːk̚˨˩/`, with expected project candidates `йуроп` and `йуроптаванок`. These are source-attested dictionary readings, not independent expert/acoustic gold.
- `docs/generated-audit.json` now records 11 source-registry rows. The exact-head CI and Web static validation for the latest commit must both pass before merge; do not mark DONE_VERIFIED while checks are pending or failing.
- Readiness remains a partial research prototype. The missing independent adjudicated Thai segmentation/IPA set and Ukrainian target-form review remain genuine blockers.

---

## Latest continuation — source-attested lexical coverage, article diagnostics and cluster-safe benchmark (2026-10-27)

- Checkpoint at PR #95 merge: `e6fed3689d6cec8cb8b7effaa885a20c95885678`. Follow-up PR [#96](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/96) then merged as `2d0616cf8b1837749724caa05e858764cec583dc`, adding exact expected Ukrainian output assertions for `ยูเครน` (`йу` + `крен` → `йукрен`). Exact-head CI [40513150425](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40513150425) passed both `test` and `master-artifact`; static validation [40513191551](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40513191551) passed. Post-merge CI run [40513842348](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40513842348) has passed the test job; its master-artifact job was still queued, and Pages run [40513842696](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40513842696) was still building at this checkpoint.
- PR [#94](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/94) merged as `ac81d188d9ceff9266a264e455d50d8e12281893`. Exact-head CI [40510490288](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40510490288) and Web static validation [40510490201](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40510490201) passed. The source-attested Thai proper name `ยูเครน` is segmented `ยู|เครน`; its cited IPA is `/juː˧.kʰreːn˧/` from en.wiktionary revision 88025965, CC BY-SA 4.0. This is source-attested evidence, not independent expert/acoustic gold.
- PR [#95](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/95) merged as `e6fed3689d6cec8cb8b7effaa885a20c95885678`. It carries six article-style diagnostic probes, null-gold assertions and pinned raw external G2P outputs. Full branch CI [40510716596](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40510716596) and optional external smoke [40510554606](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40510554606) passed. Post-merge main CI [40511892392](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40511892392) and Pages deployment [40511892093](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40511892093) subsequently completed successfully. The merged checkpoint is verified for build/deployment, not for general pronunciation accuracy.
- External benchmark interpretation remains limited: FastThaiG2P gives a compact candidate for `ยูเครน`, while thaiphon emits four fragments. There are 42 challenge prompts, 126 raw output rows, and zero independently adjudicated gold labels. These results diagnose coverage/convention differences; they do not establish which engine is accurate.
- Task ledger:
  - `DONE_VERIFIED`: article cleanup and deployed-page contract on the prior verified main checkpoint; PR #94 exact-head tests; PR #95 branch CI and external smoke.
  - `DONE_VERIFIED`: source-attested `ยูเครน` lexicon integration has passing exact-head tests, post-merge main CI and Pages deployment. `PARTIAL`: challenge probes are merged and validated as diagnostic inputs, but still have no gold labels.
  - `PARTIAL`: lexical segmentation; the CC0 dictionary baseline and TUD Viterbi research model have measurable but non-gold results. The TUD model is not in the production browser engine.
  - `BLOCKED / evidence-limited`: high-confidence general G2P and claims of pronunciation accuracy require an independently adjudicated Thai IPA/word-boundary set, dialect/IPA conventions, and qualified review. Do not import external outputs as truth or bypass the typed IPA → Ukrainian adapter.
- PR [#85](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/85) merged as `553456432be092d99f35e385c5b56eafe60099f0`. It fixes the latency benchmark to append complete Thai lexical units instead of slicing arbitrary code points. Its main CI test job passed in run [40513578523](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40513578523), and the generated latency artifact `12739570652` reports Node v22.23.3, 5 warmups / 30 samples: target 100 → actual 113 code points, median/p95 2.102/3.294 ms; target 250 → actual 261, 5.636/8.600 ms; target 500 → actual 500, 7.386/11.115 ms. This remains a runtime diagnostic, not an accuracy score or speedup claim.
- Do not label the repository release-ready based on CI alone. The implementation is a research-oriented prototype; the next genuine quality gate is same-row, independently adjudicated evaluation for segmentation, tones, vowel length, IPA and Ukrainian target adaptation.

---

## Continuation — article-style G2P probes and cleanup regression (2026-10-27)

- Default-branch checkpoint before the probe continuation: `463e81b5ec5b90dedb84eaeb2ec5f27330be3ec2` (PR #91 cleanup fix merged). The earlier Pages run [40505659010](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40505659010) exposed nested IPA link debris. PR #91 fixed it; PR #93 then corrected the live-contract checker to look for `softSyllabify` in `/src/engine.js` rather than `/src/app.js`. Current post-merge Pages run [40509900075](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40509900075) passed deployment and the published-page contract; main CI [40509900074](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40509900074) passed. Cleanup/deployment gate is now DONE_VERIFIED.
- **Engine evidence:** the pinned TUD unigram Viterbi segmenter has held-out TUD test boundary F1 0.872932 and Wisesight source-annotated test-only boundary F1 0.792101 (precision 0.659221, recall 0.992072; 993 rows, zero expert-adjudicated). The pinned CC0 dictionary maximum-match baseline on the same 993 source-annotated rows reports boundary F1 0.839471, precision 0.822287, recall 0.857390, exact-sequence rate 0.193354. These are descriptive measurements on source annotations, not expert-gold accuracy, and the TUD and dictionary reports use different group filtering; do not compare aggregate scores as if the evaluations were identical. Neither number proves production-quality segmentation.
- Added six unscored article-style diagnostic probes to `data/benchmark/thai_g2p_challenge.jsonl`: `ยูเครน`, `ประเทศยูเครน`, `ยูเครนเป็นประเทศหนึ่ง`, `เป็นประเทศหนึ่ง`, `ยุโรปตะวันออก`, and `ประเทศในยุโรปตะวันออก`. CI challenge count is now 42, and a regression test ensures these rows remain null-gold and `not_adjudicated`. This gives the optional external G2P smoke workflow target-relevant inputs but does not create gold or claim accuracy.
- **Observed external smoke:** run [40507249579](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40507249579), artifact [12734699648](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40507249579/artifacts/12734699648), artifact digest `sha256:772aac743eb3ac03e1b4ae8dc11ec3102e4d17bc59461e770acd73a694835371`. All 42 prompts produced raw output from thaiphon 0.7.0 and FastThaiG2P 0.1.0; Goruut returned no words for 16/42, including all six article-style probes. On `ยูเครน`, FastThaiG2P returns `/juː˧.kʰreːn˧/`, while thaiphon returns four slash-separated fragments `/juː˧/ /kʰeː˧/ /ra˦˥/ /na˦˥/`. This discrepancy is now durably recorded in `data/benchmark/runs/article-style-external-g2p-2026-10-27.json`; without independently adjudicated gold, neither output is declared correct.
- Task ledger:
  - `DONE_VERIFIED`: cleanup fix and deployed-page contract; article-style probes added with null gold; challenge-count guard and data-contract tests updated; external smoke run completed and raw outputs preserved.
  - `DONE_VERIFIED (pre-merge)` / `PARTIAL (post-merge gate pending)`: PR #94 merged as `ac81d188d9ceff9266a264e455d50d8e12281893`. Exact-head CI and Web static validation passed; it adds source-attested `ยูเครน` → `ยู|เครน` with pinned en.wiktionary oldid 88025965 and keeps the IPA → Ukrainian adapter boundary. Post-merge main CI/deployment verification is tracked below.
  - `PARTIAL`: external comparator infrastructure exists (thaiphon 0.7.0, FastThaiG2P pinned commit, Goruut pinned commit); 42 probes / 126 raw outputs, zero independent gold. Compare outputs only as diagnostics until expert gold exists.
  - `BLOCKED / evidence-limited`: high-confidence pronunciation and broad coverage require a source-attested, independently adjudicated Thai IPA/word-boundary set and expert review. The Viterbi model remains research-only; it should not replace the dictionary segmenter without same-row comparison and cluster-boundary safety.
- No external pronunciation model or dictionary data was imported; no runtime architecture was changed. The IPA → Ukrainian adapter boundary remains mandatory.



## Continuation — strict and soft engine modes (2026-10-27)

- Starting default-branch commit: `b66d83c7f2d58ca979201aefff88a357ed71b0be`. Implementation PR [#87](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/87) merged as `3074bb7f58b36a217cedfaf5e4d8e40de5d27579`; Pages-contract diagnostic follow-up PR [#88](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/88) merged as `cc00c2f11ec2f6ee170c7fb282ee6b0a62b899c7`.
- **Implemented:** strict remains the default and preserves fail-closed behavior for unknown spans. Soft mode greedily tries structurally analyzable syllable spans inside unknown Thai tokens. Resolved Ukrainian output still comes only from the IPA → Ukrainian adapter; unresolved subspans remain explicitly marked. The selector and provisional-status notice are present in the code.
- **Exact-head verification:** PR-head CI [40485018684](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40485018684) passed both `test` and `master-artifact`; Web static validation [40485018701](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40485018701) passed. Post-merge main CI [40485685242](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40485685242) and Web static validation [40485685122](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40485685122) also passed.
- **Deployment is not yet DONE_VERIFIED:** Pages deployment run [40485685042](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40485685042) reported that the deployment itself succeeded, but its published-page contract check failed after 12 attempts. That first checker did not identify which marker was missing. PR #88 adds per-marker diagnostics; post-follow-up Pages run [40486647739](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40486647739) and CI [40486647745](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40486647745) were still `queued` at the time of this checkpoint.
- Task ledger:
  - `DONE_VERIFIED`: strict/soft implementation, IPA-first adaptation path, UI contract tests, exact PR-head CI, main CI, and static validation.
  - `PARTIAL`: live UI deployment; the deploy action succeeded but the actual published-page marker contract has not passed.
  - `BLOCKED`: determine the exact missing live marker from the diagnostic Pages run, repair the cause, and rerun until the published homepage exposes `id="engine-mode"`, `value="soft"`, and the served app contains `softSyllabify` plus the provisional-mode notice.
  - `BLOCKED / evidence-limited`: soft structural syllabification does not establish lexical word boundaries or verified pronunciation. Independent Thai phonetic review and a licensed/adjudicated gold corpus remain necessary before any accuracy claim.
- PR [#85](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/85), an unrelated latency-benchmark fix, was left untouched. No release was published.

Last audited: 2026-10-27
Repository: https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System
Branch checked: `research/thai-segmentation-gold-parity-verified-20261025`
Starting checkpoint for this continuation: `0be5fd841070e337cb5c805ef92954938abe61bb`
Release declared in README/pyproject: `0.6.1`

## Latest verified checkpoint — 2026-10-26

- Default-branch starting commit for this continuation: `0be5fd841070e337cb5c805ef92954938abe61bb` (`main`). Work branch: `research/thai-segmentation-gold-parity-verified-20261025`.
- **Latest fully verified code/data head:** `cb775d6156f62392fa2d0f4bcf8d1aa30d219530`. Exact-head CI [40315032771](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40315032771) passed both `test` and `master-artifact`; Web static validation [40315032788](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40315032788) passed.
- CI ran **180 Python tests**, generated-derived and syllable-space checks, clean generated-artifact drift, the **351,780-row / 41-rime** master table, challenge diagnostics, Node IPA→Ukrainian, **28 Python/browser parity fixtures**, UI contract, Wisesight diagnostics, target-candidate registry check, source-attested IPA diagnostic, TUD train/dev/test evaluation, and artifact uploads. These are engineering/reproducibility checks, not pronunciation accuracy.
- The 12 failures in earlier CI run [40313439910](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40313439910) were traced to four malformed rows in `data/thai/special_orthography.csv`: the `pattern` value was omitted, shifting the CSV columns so candidate IPA appeared in `analysis_status` and the parser could not match the isolated letters. Fixed in `a0bd6f598c5117154db1c78f02ae25b6d6fbf1bc`; schema/provenance regression coverage was added in `1282dad1d8703cc4cb0d321206a1d3406a4f2533`.
- Added Python adapter-boundary mutation/fail-closed coverage in `5720ef2a23f49bb85286bfa0d6366d88473c3031`, browser end-to-end IPA mutation coverage in `85448d632aa503b537803993fbe3d8335cc9f150`, and explicit tone/length/boundary/provenance/uncertainty preservation assertions in `cb775d6156f62392fa2d0f4bcf8d1aa30d219530`. Isolated `ฤ`, `ฤๅ`, `ฦ`, `ฦๅ` remain analysis-dependent and emit no confident IPA/Ukrainian output without lexical context.
- The TUD unigram-Viterbi segmenter remains research-only: held-out TUD boundary F1 `0.872932`, Wisesight test-only boundary F1 `0.792101`, absolute cross-domain drop `0.080831`; Wisesight has 993 source-annotated rows and zero expert-adjudicated rows. No production-default integration is justified.
- PR [#71](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/71) remains open as Draft. PR [#68](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/68) remains open and untouched; its special-orthography source changes are represented in #71, which is based directly on current `main`. No PR was merged or closed and no release was published.
- **Readiness:** engineering-verified research prototype, **not release-ready**. Independent Thai IPA/acoustic gold, independently adjudicated Ukrainian target forms, context/transcription-level adjudication of `บรรจุ`, and independent segmentation quality review remain open blockers.

## Operating rule

At the start of each continuation, read this file, `docs/final-audit.md`, `docs/evidence.md`, `docs/adversarial-validation.md`, `docs/corpus-validation.md`, and the current workflow definitions. Re-check HEAD and the newest CI/Pages runs before acting. Do not treat older audit prose as proof of current CI status. Keep linguistic correctness separate from parser consistency and empirical accuracy. Never convert a regression test copied from current behavior into linguistic gold evidence.

## Historical verified state (2026-10-20; retained for audit trail)

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
| THAI-005 | P1 | IN_PROGRESS | Source-backed `รร` lexical segmentation is now added for `สรรพคุณ`, `สรรพสินค้า`, and `สรรพนาม` from the Office of the Basic Education Commission learning resource (p. 29); PR #61 merged as `50e854bead2e71ecd6adb20030387fe6532be2ae`. The official OBEC/IPST guide (`SRC-OBEC-SPECIAL-VOWELS-2022`, p. 5) supports the conservative syllabic/lexical classification of `ฤ/ฤๅ`, `ฦ/ฦๅ`; a separate OBEC teaching guide (`SRC-OBEC-O-NAM-2022`, printed p. 275) supports the scope of the `อ นำ ย` family; added Python and browser fail-closed regressions, without assigning isolated-letter IPA. Exact-head CI for this port is pending. | Continue auditing thanthakhat/silent letters and word-level special orthography; retain analysis-dependent status where lexical evidence is missing. The educational source is not independent IPA gold. |
| THAI-006 | P1 | IN_PROGRESS | PR #64 established the cross-runtime Unicode contract; PR #66 adds explicit-boundary regressions in Python/browser for ASCII space/tab/CR/LF splitting and ensures VT/FF are rejected rather than silently treated as layout. PR #66 merged as `18ab41db87192dc7be69683ef85e53cb04db5517`; exact-head CI [40224809393](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40224809393) passed both test and master-artifact jobs. | Broader unknown-input and lexical word-boundary coverage remains; current Unicode/boundary tests are integrity checks, not phonetic accuracy evidence. Post-merge main CI/Pages for this merge must be checked before reporting the branch green. |
| THAI-BOUNDARY-001 | P1 | DONE_VERIFIED | Explicit layout-whitespace boundary tests now exercise Python `parse_thai` and browser `analyzeText`; VT/FF embedded in a syllable are retained as unsupported input and cannot yield IPA/Ukrainian output. PR #66 merged as `18ab41db87192dc7be69683ef85e53cb04db5517`; exact-head CI [40224809393](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40224809393) passed the Python/browser/parity and master-artifact jobs. | These checks verify input integrity and API contracts, not pronunciation accuracy. |
| THAI-UNICODE-001 | P1 | DONE_VERIFIED | Add regression coverage for NFC/trim idempotence, normalized code-point indices, C0/C1 controls, zero-width space, bidi override, U+0085 and Python/browser tokenization. PR #64 merged as `4ba2f794185b43990ee213951b2df4c8fa451586`; exact-head CI [40223490715](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40223490715) passed. | This is Unicode/input-integrity evidence, not a pronunciation benchmark. Post-merge main CI/Pages were in progress when this checkpoint was prepared. |
| THAI-007 | P1 | IN_PROGRESS | Claim-level citation work is expanded for special vowel letters and `อ นำ` using the official OBEC/IPST teaching guide (pp. 5, 7), registered in `data/thai/sources.csv`, `data/claims.csv`, and `data/thai/special_orthography.csv`; regression tests assert the source scope and preserve unresolved output for isolated `ฤ/ฤๅ/ฦ/ฦๅ`. | Still audit exact claim-level page/section anchors for tone, vowel length, consonant classes, codas, clusters and IPA; current change is not enough to close the whole task. Exact-head CI for this port is pending. |
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


## Current continuation checkpoint — 2026-10-25

- Continuation started from branch checkpoint `cc7c0276c11df39c55edc4df8da4c82b988bd4ab`.
- Current code/data/test head at this audit refresh: `43687b2753379b1d617b1c925f87358f8aad13bd`; branch: `research/thai-segmentation-gold-parity-verified-20261025`; PR #71 remains open and draft.
- Latest fully successful code/data CI checkpoint: `59890a0bfcf7b84d19408310f690d41244a482d1`, run [40237347247](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40237347247): 158 Python tests passed; generated-data drift and master artifact guards passed; existing Node IPA/UA, parity and UI tests passed at that checkpoint; Wisesight and source-attested IPA diagnostics passed.
- The current head adds the browser-side lexical IPA override and parity fixture for `เงิน`. Its exact-head CI run [40238198251](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40238198251) and Web static validation [40238198334](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40238198334) are queued at this audit refresh. Do not mark them passed until the workflow reports success.
- Current challenge diagnostic on the verified Python checkpoint: 36 inputs; 28 ordinary lexicon-resolved + 1 lexical IPA override; 7 unresolved; 26 complete outputs; 10 abstentions/incomplete. Not an accuracy benchmark.
- Text IPA diagnostic: 6 source-attested dictionary rows; 5 complete engine outputs; 4 segmental agreements; 5 tone-category agreements; 1 withheld. `บรรจุ` has a source/engine difference on final `/ʔ/`; preserve as a review item because stress/transcription level may explain it.
- Wisesight remains 993-row `SOURCE_ANNOTATED`, test-only, not independent expert gold and not training data. Current baseline: boundary P .638319, R .091858, F1 .160604, exact sequence .031219.
- Active lexical override: Thai Wiktionary revision 5759179 for `เงิน`, short `/ɤ/`, mid tone, CC BY-SA 4.0; result passes through `PhoneticResult` and the browser IPA→Ukrainian adapter.
- Corpus register now records LST20 and VISTEC as candidates requiring license/annotation review. CCOST is CC BY-NC-SA 4.0; TextGrid annotations are in a 6.2 GB archive and are not bundled.
- Remaining: production automatic segmentation; independent IPA/tone/length gold; acoustic/connected-speech validation; independent Ukrainian target-form adjudication. The repository remains a research-ready engineering prototype, not release-ready.

## Continuation handoff — 2026-10-26 (current work; exact-head CI pending)

Working branch: `research/thai-segmentation-gold-parity-verified-20261025` (existing draft PR #71). The current implementation batch has been ported onto the latest PR branch head `b2611172117c79c5e7e79044a59927b02e606a24`, preserving the intervening seven commits that added the pinned CC0 dictionary segmenter and Ukrainian target-candidate registry. Do not replace those changes with the earlier `cfd6c56` checkpoint.

### New implementation

- `scripts/train_tud_word_segmenter.py`: downloads pinned TUD files at commit `67413969add552b7030184f16f24fa9f630913bc`, validates each Git blob SHA-1, pools snapshots and derives source-document-disjoint 80/10/10 splits by normalized filename. A unigram-frequency Viterbi model is trained on the derived train split, token penalty is selected on dev, and test/Wisesight metrics are reported separately. The model/report are CI artifacts; this is a research model, not yet the public API default.
- TUD license is CC BY-SA 4.0; model metadata carries attribution/share-alike context. Wisesight remains 993-row CC0-1.0 test-only and is never used for fitting/tuning.
- `เดิน` now has a pinned source-attested lexical IPA override from Thai Wiktionary oldid 1908803 (/dɤːn˧/, long /ɤː/), routed through the same typed IPA→Ukrainian adapter in Python and browser code. The structural parser's grapheme-only ambiguity contract remains intact. The IPA diagnostic marks this source-derived output as circular and excludes it from source agreement counts.
- Added `data/benchmark/ipa-adjudication-template.tsv`, `data/benchmark/ukrainian-target-adjudication.tsv`, and `docs/independent-adjudication-protocol.md`. These are blank evidence-collection templates, not completed gold labels.
- Existing `բรรจุ`/final /ʔ/ discrepancy remains evidence-limited; do not introduce a universal rule without agreeing on broad phonemic vs surface transcription and context/stress.

### Exact-head verification required

CI was updated to run the TUD trainer, verify source-split reports and circular-override accounting, and upload the model/report artifacts. **Do not report these new checks as passed until the workflow for the current branch head completes successfully.** The GitHub Actions workflow must download the pinned TUD files; if network access fails, record it as a blocker rather than skipping or fabricating metrics.

### Remaining ledger

| ID | Status | Acceptance / blocker |
|---|---|---|
| SEG-TRAIN-001 | PARTIAL | Review exact-head TUD dev/test and Wisesight metrics; production integration is contingent on acceptable held-out results and explicit CC BY-SA 4.0 attribution/share-alike compliance |
| IPA-GOLD-001 | BLOCKED | Independent Thai phonetician plus authorized CCOST audio/TextGrid access; agree transcription layer; collect dual labels and disagreement log |
| WALK-LEX-001 | PARTIAL | Exact lexical override implemented; exact-head Python/browser CI pending; still not independent IPA gold |
| BANCHU-IPA-001 | PARTIAL / EVIDENCE-LIMITED | Resolve /ʔ/ transcription level and stress/context independently; no global rule |
| UA-TARGET-001 | BLOCKED | Two independent Ukrainian-native reviewers, predefined criteria, blinded preferences and adjudication log |

The repository remains a research prototype, not release-ready. Do not merge PR #71 or publish a release as part of this handoff.

Latest code-bearing commit after adding a deterministic source-disjoint split regression: `088b4e6649fde09f2c9d1232091e2e3c8091d9bd`. Exact-head CI remains pending; the audit JSON will be refreshed last after this handoff update. Do not claim the trainer or new IPA override tests passed until a matching run completes.


## Continuation checkpoint — 2026-10-26 (after CI failure review)

Current continuation branch: `research/thai-segmentation-gold-parity-verified-20261025`. Latest code/test correction commit: `4656a557a74405f64455219e1a6fece6be575915`.

### Current evidence and task ledger

- **DONE_VERIFIED (earlier checkpoints only):** generated-data drift and master-table generation passed in CI run `40286374324` before unit tests; Web static validation passed in `40286374333` for the then-current PR head. These results do not validate the newer correction commit.
- **PARTIAL:** opt-in dictionary maximum-match segmenter, pinned dictionary provenance, Wisesight source-annotated test-only benchmark, typed IPA override loader, Python/browser IPA→Ukrainian path, TUD source-document-disjoint research trainer, independent adjudication templates.
- **PARTIAL / CI pending:** updated four regression expectations for the newly activated `เดิน` override. They now expect the two source-pinned overrides (`เงิน`, `เดิน`), retain grapheme-only parser ambiguity, and assert `เดิน` goes through the typed IPA result and IPA→Ukrainian adapter. Changes are in `8369edd141ad83c451b0395a57ba25f7a1c57006`, `2337dcf69ff6d59cde1862d486f50031fe9a815e`, `4964d3970c6f14cedd07f04138b99b95c57ef506`, `4656a557a74405f64455219e1a6fece6be575915`.
- **BLOCKED:** no independent expert-adjudicated IPA/acoustic gold, no independent Ukrainian target-form adjudication, and no final resolution of `บรรจุ` final `/ʔ/` across transcription levels.
- **TODO:** observe full CI for the exact latest head. Previous CI `40286374324` failed 4 unit tests after the `เดิน` override; later steps were skipped, so no segmentation/TUD/Node/parity result is available for that run. Do not infer new-head success from earlier green jobs.

### Next action

Poll the latest commit's CI and Web static validation. If CI fails, inspect exact failed tests/logs and repair only evidence-backed mismatches; rerun on the new exact head. After all available engineering gates pass, keep the repository classified as a research prototype until independent linguistic/phonetic and Ukrainian target adjudication criteria are met.


### Final audit-register synchronization — 2026-10-26

- The machine-readable audit was subsequently corrected in commit `c498cd8e9d56146f7dcafd2884bf860ae80af866`; this is the latest documentation head, superseding the `96b474bd15c139f70bfc432de848c7ca2d614537` checkpoint above.
- Exact-head CI run `40292666463` is still in progress at `scripts/generate_master_table.py`; Web static validation `40292666543` passed. The generator has not yet completed, so later tests, Wisesight diagnostics, TUD model training, and artifact upload have not yet reported results on this head.


## Continuation quality review — 2026-10-26

### Final documentation-head checks

- Exact docs head `cb8832ca99e4ccce53b6fb2b6988b5945acaad71`: CI [40297155713](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40297155713) completed successfully for both `test` and `master-artifact`; Web static validation [40297155831](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40297155831) passed.
- Code/data head `4c3d01d9b726b410c98048878441082d8d5c8299`: full CI [40296520186](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40296520186) passed 176 Python tests and all configured parity, data, diagnostic, TUD-training and artifact checks.

### TUD unigram-Viterbi quality review and integration decision

**Decision: keep research-only; do not integrate as the production default.**

- Held-out TUD: precision 0.788598, recall 0.977464, F1 0.872932, exact-group rate 0.432 (375 filtered Thai-only multi-token groups).
- Wisesight test-only: precision 0.659221, recall 0.992072, F1 0.792101, exact-group rate 0.385 (2,848 filtered groups).
- Cross-domain boundary F1 drop: 0.080831. The much higher recall than precision and modest exact-group rates indicate that boundary metrics alone overstate practical segmentation usefulness; Wisesight precision is materially weaker. These are not full-text metrics, and neither source is independent expert adjudication.
- Acceptance before reconsideration: (1) manually inspect a stratified sample of false splits/merges; (2) set explicit minimum precision/F1/exact-sequence and coverage thresholds before tuning; (3) evaluate on an independently sourced, untouched domain with provenance/license and split integrity documented; (4) confirm runtime/abstention behavior and preserve CC BY-SA 4.0 attribution/share-alike; (5) record an explicit integration decision. Do not tune against Wisesight, which remains test-only.

### Remaining genuine blockers

- **IPA/acoustic gold — BLOCKED:** qualified independent Thai phonetician, agreed broad-vs-surface transcription protocol, and authorized recording/TextGrid access. Acceptance: independent labels, speaker-aware sample, disagreement log, and acoustic evidence for any acoustic claim.
- **Ukrainian target forms — BLOCKED:** independent Ukrainian-native reviewers, blinded judgments and agreed criteria. Acceptance: versioned criteria, judgments, disagreement log, adjudicated target set.
- **`บรรจุ` final /ʔ/ — PARTIAL / evidence-limited:** require context/transcription-level expert review; do not apply a global rule.
- **Release readiness:** not release-ready. Engineering CI is green, but independent pronunciation gold, Ukrainian target adjudication, and production segmentation quality remain unestablished.


## Mandatory architecture clarification and exact-head CI review — 2026-10-26

The owner has explicitly reaffirmed that the system's purpose is Thai-to-Ukrainian transcription **through an actual IPA intermediate**. Treat this as a non-negotiable architecture invariant:

`Thai orthography → structural analysis → Thai phonology → typed/inspectable IPA → Ukrainian adaptation from IPA → Ukrainian practical orthography`.

IPA must be the actual data-flow boundary, not a parallel audit display. No independent Thai-grapheme → Ukrainian output path is acceptable. The Ukrainian adapter must consume the typed IPA result and documented metadata only; source graphemes, vowel IDs, or Thai coda fields must not independently determine the final target string. Preserve phonemic/broad surface IPA, tone, length, segment/syllable boundaries, provenance and uncertainty. If IPA is unsupported or unresolved, withhold the dependent Ukrainian result rather than guessing.

### Acceptance and verification

- Review/update architecture and research docs against this invariant; README and `docs/research-protocol.md` now state it explicitly.
- Verify the adapter boundary and end-to-end data flow in both Python and browser implementations; tests must establish that Ukrainian output is derived from the IPA result actually exposed by the source stage.
- Run the complete test suite, generated-artifact checks, browser IPA→UA/parity/UI tests and available diagnostics on the exact resulting branch head. Prior passing runs do not validate newer commits.
- Continue to distinguish software conformance from linguistic accuracy. Independent Thai IPA/acoustic adjudication and independent Ukrainian-native target-form adjudication remain separate evidence gates.

### Latest exact-head failure — do not mark CI green

CI run [40305933260](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40305933260) on the current PR head completed with failure: generated-data drift checks and master-table generation (351,780 rows) passed, but Python unit tests ran 179 tests and reported 12 failures. The failures are in three assertions groups:
1. `tests/test_completion_layers.py`: isolated `ฤ`, `ฤๅ`, `ฦ`, `ฦๅ` return `unresolved:unsupported-symbol`, not the expected analysis-dependent status;
2. `tests/test_text_pipeline.py`: the same four isolated spellings return `unresolved:unsupported-symbol`;
3. `tests/test_special_orthography_evidence.py`: four registry assertions compare `analysis_status` to `analysis-dependent`, but the current field contains IPA candidate strings (`rɯ|ri|rɤ`, `rɯː`, `lɯ`, `lɯː`). Inspect the schema and intended uncertainty contract before changing either implementation or assertions. Do not coerce uncertain standalone letters to one IPA value to satisfy a test.

Web static validation [40305933181](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40305933181) passed for this head, but that does not override the failed Python suite. The current branch is **not exact-head CI-verified**. Next acceptance step: repair the schema/test mismatch without introducing unsupported IPA, then rerun full CI and web static validation on the new exact head.


## Exact-head continuation update — 2026-10-26 (post-audit verification refresh)

- Verified documentation checkpoint: `4c61866d98312e8cf08f78bc8ab0f213bc8dc8c0`.
- Exact-head CI [40316202183](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40316202183) passed both `test` and `master-artifact`; Web static validation [40316202145](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40316202145) passed.
- The CI job ran 180 Python tests; generated-data drift and syllable-space checks; master-table generation (351,780 rows, 41 vowel/rime records); Node IPA→Ukrainian; 28 Python/browser parity fixtures; UI contract; challenge, Wisesight and source-attested IPA diagnostics; Ukrainian target-candidate registry check; pinned TUD train/dev/test evaluation; and artifact uploads.
- The artifact inventory confirms a TUD research model/report, Wisesight baseline and dictionary diagnostics, source-attested IPA diagnostic, and master table were uploaded. These are reproducible engineering artifacts, not independent pronunciation gold.
- The TUD segmenter remains research-only. Held-out TUD boundary F1 is 0.872932 with exact-group rate 0.432; Wisesight source-annotated test-only boundary F1 is 0.792101 with exact-group rate 0.385. The 0.080831 F1 drop, high recall relative to precision, and low exact-group rates do not support production-default integration. No manual false-split/false-merge audit or independent untouched-domain adjudication has been completed.
- Open evidence gates remain: (1) independent Thai phonetic/acoustic adjudication with agreed broad/surface/narrow transcription layer and lawful asset access; (2) two independent Ukrainian-native target-form judgments plus adjudication log; (3) context/transcription-level adjudication of `บรรจุ` final `/ʔ/`; and (4) representative segmentation error review, predefined deployment thresholds and independent-domain evaluation. Do not fabricate labels or claim these gates passed.
- PR [#71](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/71) remains Draft because evidence gates are open; PR [#68](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/68) remains open and unmerged. Do not merge either blindly or publish a release.
- The machine-readable audit was refreshed in commit `2ab132647323a253b4a4147d4951b9b26d32eff1`. This handoff/matrix synchronization itself changes documentation and therefore requires exact-head CI plus Web static validation before this new docs head can be marked `DONE_VERIFIED`. No local test execution is claimed.


## Segmentation error-review implementation batch — 2026-10-26

- Added `scripts/analyze_segmentation_errors.py` to produce deterministic, row-level false-split and false-merge review examples for the pinned 993-row CC0-1.0 Wisesight source-annotated test set. It reports boundary precision/recall/F1, exact-sequence rate, source/license/split metadata, stable example ordering and explicit caveats.
- Added `tests/test_segmentation_error_analysis.py` for whitespace-boundary semantics, report provenance/evidence grade, and presence of both error classes.
- Wired the report into `.github/workflows/ci.yml` with assertions that all 993 rows remain source-annotated (zero expert-adjudicated rows), the test-only split and CC0-1.0 provenance are intact, both false-split and false-merge examples exist, and the report cannot be mistaken for adjudicated gold. CI uploads artifact `thai-segmentation-error-review`.
- Implementation commit: `e80606e641d631966b566999027ee9d2b4d00bb`; audit-register update: `6e34f66498b5bf474fe59af054940b93f5380e9a`. Exact-head CI and Web static validation for the resulting documentation head must pass before this batch is marked `DONE_VERIFIED`; do not claim the report ran locally.
- This batch advances the segmentation error-analysis acceptance criterion but does not complete expert review. Source-annotated differences are triage candidates, not proof that each prediction is linguistically wrong. Production segmentation remains blocked pending human review, predefined thresholds and independent-domain evaluation.


### Error-review metric parity correction — 2026-10-26

- The first generated report correctly matched boundary precision/recall/F1 against the existing dictionary diagnostic, but reported zero exact sequences because `segment_text_preserving` returns a tuple while JSON gold tokenization is a list. The comparison was therefore always false despite equivalent token sequences.
- Corrected the diagnostic to normalize predicted tokens to a list before equality checks. Added a pinned regression expecting 192 exact token-array matches out of 993, and CI now asserts this count alongside both error classes and the source-grade gate.
- Fix commit: `bec1b7027f34a4f70f0b6f9fdc415ef43343eab9`; test commit: `aba6832eb97cb4b84f2e62fa058fa963cfb34803`; CI assertion commit: `c189cdb9209d85780c3baeb1df23800101840b16`. Audit JSON was synchronized in `0b39f427da68be645d3479b0aa05ef0d7de76193`.
- The earlier artifact from CI run [40319308274](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40319308274) is superseded for exact-sequence counts; its boundary metrics and false-split/false-merge samples remain useful, but do not cite its zero exact-sequence count. The corrected final-head run must pass before this metric repair is verified.


### Exact-head verification of segmentation error review — 2026-10-26

- Corrected implementation head: `4b1592cd72298d1ca92e0b99ab330975764a078a`.
- Full CI [40320450844](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40320450844) passed both `test` and `master-artifact`; Web static validation [40320450587](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40320450587) passed.
- CI ran **182 Python tests**, including the new report tests; the evidence-grade/error-review assertions passed; generated-data drift passed; master artifact passed with 351,780 rows and 41 vowel/rime records; Node IPA→Ukrainian, 28 Python/browser parity fixtures, UI contract, Wisesight diagnostics, source-attested IPA diagnostics, candidate-registry check, TUD research evaluation and artifact uploads passed.
- Verified report artifact: `thai-segmentation-error-review`, artifact ID `12648833301`, SHA-256 `005c18ba366fc692193db7f6557b052ff7f940dea3274ec168f6a93f0df7e66b`. On 993 CC0-1.0 source-annotated test rows (zero expert-adjudicated rows), the dictionary baseline has 13,891 gold boundaries, 14,484 predicted boundaries, 11,910 true positives, 2,574 false splits and 1,981 false merges; precision 0.822287, recall 0.857390, F1 0.839471, and 192/993 exact token arrays (0.193353). These are descriptive against source annotations, not independent expert accuracy.
- A previous CI run [40320041521](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40320041521) failed because an escaped newline accidentally commented out the prediction assignment. The source was corrected in commit `4b1592cd72298d1ca92e0b99ab330975764a078a`; the exact-head full run above passed. Do not treat the earlier artifact's zero exact-match count as valid.
- This verifies the error-reporting software, not human adjudication. Production segmentation remains PARTIAL pending manual false-split/false-merge categorization, predeclared thresholds and independent-domain evaluation.


## Comparative segmentation review — 2026-10-26 (new verification pending)

- Added `scripts/compare_segmentation_error_review.py` to compare the dictionary max-match segmenter and the TUD unigram-Viterbi research model against the **same exact 993 pinned Wisesight rows**, with the same lexical-boundary policy. It reports boundary precision/recall/F1, exact token-array matches, false-split/false-merge examples and left/right source-text context at each disputed code-point offset.
- The TUD model is consumed from the current CI run's generated `/tmp/thai-tud-word-model.json`; it is not copied into the repository and Wisesight remains excluded from model training/tuning. Mixed-script, URL, number, punctuation and whitespace runs are preserved unchanged while only Thai runs are segmented.
- Added `tests/test_comparative_segmentation_error_review.py` for lossless mixed-text handling, same-row comparison, provenance/evidence grade and both error classes. Added a CI step after TUD training and a dedicated `thai-segmentation-comparative-error-review` artifact. Workflow asserts 993 source-annotated rows, zero expert-adjudicated rows, shared rows, both error classes and explicit caveats.
- The already verified dictionary-only report on run [40321293906](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40321293906) has 2,574 false splits, 1,981 false merges, boundary F1 0.839471 and 192/993 exact sequences. These are against source annotation, not expert gold. Representative report excerpts expose review strata such as numeric/punctuation fragmentation, Latin/URL/brand handling and token granularity differences. These are **preliminary non-expert triage observations**, not adjudicated linguistic categories.
- The comparative implementation/test/workflow commits are `7590a32ed652eb7fc2eb5b5897fc6a8591a31c09`, `c2d946e11690a517fb958b768733da4c864a49c1`, `54e1db86cf3882f025f00ede86d86e7efb3909e2`, and `b6dbec7928b106f0ab52e06af33a26635df75412`; validation matrix update is `dfaffb6c07b063a85f3a955556a8d95526d39c60`. CI/static validation for this new branch head must be observed before this batch is marked DONE_VERIFIED. No local test execution is claimed.
- Production remains blocked pending representative human review, predeclared precision/recall/exact-sequence/abstention thresholds, and independent licensed-domain evaluation. Wisesight labels remain source-annotated, not independent expert gold. Independent Thai IPA/acoustic gold, two independent Ukrainian-native judgments, and contextual transcription-level adjudication of `บรรจุ` remain evidence-gated.


## Comparative review exact-head verification — 2026-10-26

- Code/workflow checkpoint `b6dbec7928b106f0ab52e06af33a26635df75412`: CI [40322960615](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40322960615) passed, including the comparative report, evidence-grade checks and artifact uploads. Web static validation [40322959844](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40322959844) passed.
- Documentation checkpoint `e4ab3fd46e9c48c4220afb1f73ae5c6127b328ff`: full CI [40323209539](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40323209539) passed both `test` and `master-artifact`; Web static validation [40323209471](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40323209471) passed.
- Comparative artifact `thai-segmentation-comparative-error-review`, ID `12649094231`, SHA-256 `8005cc91939ea06b852c1717fee9fb72d370709e74267b8f99636a6476d30775`. Same 993 pinned Wisesight rows, CC0-1.0, source-annotated, zero expert-adjudicated:
  - Dictionary max-match: precision 0.822287, recall 0.857390, F1 0.839471, 2,574 false splits, 1,981 false merges, 192/993 exact sequences (19.34%).
  - TUD unigram-Viterbi: precision 0.608000, recall 0.973868, F1 0.748623, 8,722 false splits, 363 false merges, 119/993 exact sequences (11.98%).
- These are same-row full-text metrics with non-Thai runs preserved. They differ from the earlier TUD report's filtered Thai-only-span metrics and should not be conflated. The TUD model has high boundary recall but severe over-segmentation and worse exact-sequence rate on the common full-text evaluation; keep it research-only. Neither system's disagreement against source annotation is automatically a linguistic error.
- PR reconciliation: PR [#68](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/68) was closed as superseded after comparing all eight changed paths with PR #71 and confirming that the OBEC special-vowel/อ นำ source, claims, registry, tests and generated-audit changes are represented in #71. A supersession comment was added; the #68 branch was not deleted or modified. PR [#71](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/71) remains open Draft, mergeable; no merge or release was performed.
- Remaining blockers are unchanged: independent Thai IPA/acoustic gold; two independent Ukrainian-native target-form judgments; contextual/transcription-level adjudication for `บรรจุ`; human review of representative segmentation cases, predeclared acceptance thresholds and an independent licensed domain. Engineering CI cannot substitute for these.
- The matrix, handoff, audit register and PR #71 description now record the comparison. The documentation commits after checkpoint `e4ab3fd46e9c48c4220afb1f73ae5c6127b328ff` must themselves pass exact-head CI and Web static validation before the final branch head is called green.


## Human-review sample generator and exact-head verification — 2026-10-26

- Added `scripts/build_segmentation_manual_review.py` and `tests/test_segmentation_manual_review.py`. The generator joins real comparative-report error examples to full source rows in the pinned 993-row Wisesight TSV, keeps only IDs for which both systems have a recorded prediction, verifies exact source reconstruction for gold and both predictions, and emits full text, gold/dictionary/TUD token arrays, triage provenance, sampling strata, and blank reviewer decision fields.
- Sampling strata (numeric/date, URL/email, mixed Latin–Thai, Latin/brand, punctuation/quoting, long Thai, and engine disagreement) are explicitly heuristic candidate labels only. Every row stays `SOURCE_ANNOTATED`, `adjudicated=NO`; no error is automatically called linguistically wrong.
- CI now builds and validates the manual-review TSV and uploads it with the comparative JSON artifact. Acceptance requires both model predictions, exact lossless reconstruction, non-empty sample, and empty human decision fields.
- Comparative artifact independently downloaded and inspected: artifact ID `12649094231`, run `40322960615`, head `b6dbec7928b106f0ab52e06af33a26635df75412`; ZIP size 83,500 bytes; SHA-256 `8005cc91939ea06b852c1717fee9fb72d370709e74267b8f99636a6476d30775`. JSON has 993 source-annotated rows, 0 expert-adjudicated rows, same rows and boundary policy for both engines, Unicode-code-point offsets, and lossless mixed-text policy.
- Exact metrics from the artifact: dictionary P=0.822287, R=0.857390, F1=0.839471, 2,574 false splits, 1,981 false merges, 192/993 exact sequences; TUD P=0.608000, R=0.973868, F1=0.748623, 8,722 false splits, 363 false merges, 119/993 exact sequences. TUD remains research-only; these source-annotation comparisons are not expert gold.
- Latest pre-review-sampler exact-head CI for `4115326490bc8189660838f51bfe47a382ada203`: run `40324015433` passed both `test` and `master-artifact`; Web static validation `40324015445` passed. The review-sampler code/workflow changes are newer and require their own exact-head CI and static validation before being marked verified.
- External gates remain: independent Thai IPA/acoustic gold, two independent Ukrainian target-form reviewers, context-specific `บรรจุ` final /ʔ/ adjudication, another licensed evaluation domain, and full official OBEC PDF review (direct PDF access previously returned HTTP 403; only scoped claims from accessible evidence are made). No release-readiness claim is made.


## One-pass continuation — stratified review sampling and external-source audit (2026-10-26)

### Task ledger at this checkpoint

| Task | Status | Outcome / acceptance criterion |
|---|---|---|
| IPA-first adapter, fail-closed behavior, Python/browser parity | DONE_VERIFIED on prior exact-head CI | Preserve the existing implementation. Do not treat older passing CI as proof for newer commits. |
| Dictionary/TUD segmentation comparison | DONE_VERIFIED as a diagnostic artifact | Same 993 Wisesight rows; dictionary F1 0.839471 and 192 exact token sequences; TUD F1 0.748623 and 119 exact sequences. Labels are source-annotated, not independent gold. TUD stays research-only. |
| Stratified human-review sample | PARTIAL; exact-head verification pending | Replaced top-error-only sampling with deterministic heuristic strata plus a uniform control sample; computes both predictions across all source rows; verifies exact reconstruction; keeps all human decision fields blank. CI must pass on final HEAD and artifact must be inspected. |
| Independent Thai IPA/acoustic gold | BLOCKED by external specialist and authorized audio | CCOST v1.0 is listed publicly under CC BY-NC-SA 4.0 (https://zenodo.org/records/17366698; DOI 10.5281/zenodo.17366698). Archive/manual not downloaded and inspected in this session; no expert annotations were fabricated. |
| Independent Ukrainian target forms | BLOCKED by two independent reviewers | Existing TSV and protocol are ready for annotation; no judgments are invented. |
| บรรจุ final /ʔ/ | PARTIAL / context-limited | Pinned Wiktionary revision records /ban˧.t͡ɕuʔ˨˩/. This is source attestation, not independent gold. No lossy one-syllable override added for a multisyllabic word. |
| Independent segmentation domain | BLOCKED by licensed data/access and protocol | Need a second lawful corpus, immutable snapshot/hash, predeclared split, and untouched evaluation. Wisesight must remain test-only. |
| Full official OBEC PDF review | BLOCKED — HTTP 403 | The exact cited URL still returns 403. Do not claim full inspection or broaden claims beyond already scoped accessible evidence. |
| Exact-head CI + Web static validation | PARTIAL / pending | Current batch has new workflow runs; only a successful run tied to the final commit can close this task. |
| Release readiness | BLOCKED | Keep repository classified as an engineering-oriented research prototype until both engineering and external evidence gates close. |

### Changes in this batch

- scripts/build_segmentation_manual_review.py: deterministic stratified sampling plus uniform controls across the pinned source set; full dictionary/TUD predictions are recomputed; provenance, model license and lossless reconstruction are enforced.
- tests/test_segmentation_manual_review.py: deterministic output, control sample, blank adjudication fields, wrong model provenance and reconstruction failures are tested.
- .github/workflows/ci.yml: pass the current CI-generated TUD model into the sampler and assert control rows, exact reconstruction and no automatic adjudication.
- docs/independent-adjudication-protocol.md: sampling protocol and restrictions on population-level claims are documented.
- docs/evidence.md: public CCOST metadata/license and official OBEC 403 blocker recorded.
- docs/validation-matrix.md, docs/final-audit.md, and docs/final-audit.json: status and evidence gates synchronized.

### Verification status and next blocker

- No local Python tests are claimed as run: local clone/test execution remains unavailable because the container could not resolve github.com.
- Prior exact-head CI for comparative segmentation analysis passed at b6dbec7928b106f0ab52e06af33a26635df75412; it does not verify this newer sampler.
- Latest pre-handoff documentation/audit commit: 175658510101082ccc91e3179f71e47f4945d648. The handoff update itself creates the next commit; inspect the branch head after this write and wait for both CI and Web static validation to finish for that exact SHA.
- No PR was merged and no release was published. PR #71 remains Draft; PR #68 remains closed unmerged and its branch is preserved.


## External-domain evaluation and scalable review — continuation checkpoint 2026-10-26

### Work completed in this batch

- Replaced top-error-only manual segmentation review with deterministic sampling across all source rows: up to 8 per heuristic stratum plus 12 uniform controls. The packet recomputes both model predictions for every row, enforces lossless reconstruction, records sampling reasons, and leaves human decisions blank.
- Added tests for stable sampling, control inclusion, provenance, wrong model license, source reconstruction and blank adjudication fields.
- Verified VISTEC-TP-TH-2021's dataset-specific upstream README at commit 215a7dc3d384f20eb56af1cbc41fb32b7f8df57c. It declares CC-BY-SA 3.0, describes 49,997 manually annotated samples and uses pipe-delimited word tokenization in submissionText. Pinned CSV Git blob SHA-1: edfcb85907a604c5e30643065ac4975862a0fe90.
- Added a VISTEC adapter and tests. It strips only documented NER/misspelling tags, builds the existing benchmark format, and requires exact reconstruction. It explicitly uses annotated submissionText rather than the separate raw questionText field.
- Added an opt-in GitHub Actions workflow that checks out the exact external commit, validates the CSV blob hash and license declaration, evaluates dictionary and TUD systems, and uploads only the report. VISTEC is never used for training/tuning and its metrics will remain source-annotation diagnostics, not expert gold.
- Optimized scripts/evaluate_segmentation.py to index gold rows once. This removes quadratic repeated row scans when scoring ~50k rows against two models.
- Updated the existing README, corpus/evidence registry, adjudication protocol, validation matrix, final audit, machine-readable audit and this handoff in place. No duplicate master plan was created.

### Current ledger

| Task | Status | Exact acceptance criterion |
|---|---|---|
| IPA-first architecture, adapter boundary and parity | DONE_VERIFIED on prior exact-head CI | Keep the typed IPA contract and fail-closed uncertainty; do not equate earlier CI with validation of new changes. |
| Wisesight comparative metrics | DONE_VERIFIED as source-annotation diagnostic | Same 993 rows; dictionary F1 0.839471 / 192 exact sequences; TUD F1 0.748623 / 119 exact sequences. No independent expert labels. |
| Stratified human-review packet | PARTIAL | Exact-head CI must pass; inspect artifact; human reviewers must fill it under the protocol before claiming adjudicated boundaries. |
| VISTEC independent-domain source metadata | DONE_VERIFIED (metadata) | Pinned upstream commit/blob and dataset-specific CC-BY-SA 3.0 declaration recorded. |
| VISTEC evaluation adapter/workflow | PARTIAL | New workflow and tests are queued; require a successful run, 50,000 CSV rows, 100% prediction coverage, exact reconstruction and artifact inspection. |
| Independent Thai IPA/acoustic gold | BLOCKED | CCOST v1.0 is public under CC BY-NC-SA 4.0, but the archive/manual must be reviewed and qualified Thai phonetic reviewers must annotate a speaker-aware sample. |
| Independent Ukrainian target forms | BLOCKED | Two Ukrainian-native reviewers must independently annotate the existing template and record criteria, agreement and adjudication. |
| บรรจุ final /ʔ/ | PARTIAL / context-limited | Pinned dictionary IPA records /ban˧.t͡ɕuʔ˨˩/; do not turn one lexical citation into a universal rule. Define transcription level and context. |
| Full official OBEC PDF | BLOCKED — HTTP 403 | Requires lawful authoritative access; no full-document review is claimed. |
| Exact-head CI and Web static validation | PARTIAL / queued | Current final branch head must pass both workflows; new test files are not called passed until their run succeeds. |
| Release readiness | BLOCKED | External linguistic evidence and engineering checks remain incomplete; keep research-prototype status. |

### Verification checkpoint

- Starting main SHA: 0be5fd841070e337cb5c805ef92954938abe61bb.
- Branch: research/thai-segmentation-gold-parity-verified-20261025.
- Latest pre-handoff audit commit: 8123ca324622b5c34a7715964346cfc176cc3bcf. The handoff update itself creates the next commit; check the branch ref and exact-head workflows after this write.
- New CI, Web static validation and VISTEC workflow runs were queued when last checked. No result from those runs is claimed as passed.
- Local tests remain unexecuted because the environment previously could not resolve github.com. GitHub Actions is the available verification path.
- PR #71 remains open Draft. PR #68 remains closed unmerged as superseded; its branch is preserved. No PR was merged and no release was published.


### Final handoff synchronization — 2026-10-26

- The VISTEC workflow sparse-checkout configuration was corrected to non-cone mode so the pinned nested CSV/license/README file paths are selected explicitly. Code/workflow checkpoint: a56fc37b11e74a1a52b8b80736eeb4724746ba2b.
- Machine-readable audit synchronization checkpoint: c6dac498ec8c7939c6f2bfbcea04c8d1fdeab96a.
- The branch head immediately before this final handoff update was c6dac498ec8c7939c6f2bfbcea04c8d1fdeab96a. This handoff update creates the final commit; inspect the branch ref for its resulting SHA.
- Exact-head CI, Web static validation and External VISTEC segmentation evaluation remain queued in the latest observed workflow state. No current-batch tests are claimed as passed and no VISTEC metric is claimed. The next genuine blocker is execution of these queued workflows, followed by actual human/specialist adjudication and the OBEC access issue.


### Source-integrity hardening and final status — 2026-10-26

- The VISTEC adapter now independently computes the Git blob SHA-1 of the supplied CSV and rejects any file that does not match the pinned upstream blob. The external workflow also checks out the exact upstream commit and checks the Git blob/license before evaluation. Regression coverage was added for an unpinned CSV.
- Latest implementation/test checkpoint: 43fb1416e6d103de4999a84a1dbaefd663507cb6. Latest machine-audit checkpoint before this handoff update: bc16f7b70481bb88cd30bb4d9589203da819f4f1.
- The branch head immediately before this handoff update is bc16f7b70481bb88cd30bb4d9589203da819f4f1. This update creates the next commit; read the branch ref for the final SHA.
- Latest exact-head CI, Web static validation and VISTEC evaluation were still queued at the last status read. No new tests are marked PASS, and no VISTEC metrics are reported. If the queue remains blocked, record that as a CI service/runner blocker rather than treating tests as successful.
- External evidence gates remain: actual independent Thai phonetic/acoustic review, two Ukrainian-native target-form reviews, human segmentation adjudication, contextual decision for บรรจุ final /ʔ/, and full official OBEC PDF inspection (HTTP 403). These require human/specialist or lawful-source access and cannot be honestly synthesized by code.


## VISTEC annotation parser hardening — 2026-10-26

- Reviewed the external VISTEC adapter and found that empty pipe-delimited token fields were silently discarded after annotation-tag removal. This could conceal malformed source annotations even when the remaining tokens reconstructed some text.
- Changed `scripts/evaluate_vistec_segmentation.py` to fail closed if any token field becomes empty after documented `<ne>`/`<msp>` markup removal. Added regressions for repeated separators, an empty markup-only token, a leading separator, and the existing all-empty input case.
- Code commits: `a02e3c6ed57fc927e880863c49563d69032f62df`, `fd37959129c74285148f07fff5844a7593d5d037`, and `1cbf97036ec931266f4a6ed5eb747a00e5b7ad29` (the last aligns the prior empty-input test with the stricter contract).
- Verification status: source and test edits were re-fetched from GitHub and inspected; local repository execution is unavailable in this session. No CI/workflow run or combined status was yet returned for the new head `1cbf97036ec931266f4a6ed5eb747a00e5b7ad29`; do not mark the regression tests as passed until exact-head CI completes.
- Acceptance: exact-head Python CI and VISTEC evaluation workflow pass; inspect the generated 49,997-row report and confirm the stricter parser accepts the pinned upstream snapshot without unexpected empty fields. If it rejects the pinned source, inspect the precise offending row before relaxing the gate; do not restore silent token dropping.


## Latest validation status refresh — 2026-10-26

- Latest code-bearing commit for the VISTEC parser guard is `550f26fdbf6fd66a0d1c2cb1caa9bd6bd10de196`. Three workflow runs are now visible for that code-bearing head: CI [40346688497](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40346688497), Web static validation [40346688520](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40346688520), and external VISTEC evaluation [40346688621](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40346688621). The latest poll shows all three `queued`; no result or metric is claimed.
- Follow-on commits `920bdc8b1e9aec80e49d3df866fa26e2dc1aca46`, `7521fd76242a93eb2db8a7bd64771f164f38eee9`, and `835139e4003cdf3df2452cf9e729d2cdb0c55234` update only audit JSON, audit markdown, and the validation matrix to reflect this newly visible queue state. They do not change executable code. Refresh the PR head and CI before merge; if GitHub does not run docs-only commits, retain the distinction between the code-bearing tested SHA and the final documentation SHA.


### Failed workflow diagnosis and fixes — 2026-10-26

- Freshly inspected run logs: CI 40346688497 failed exactly one test due to stale expected license wording; Web static validation 40346688520 passed; external VISTEC run 40346688621 failed after immutable source commit/blob verification and model training because the pinned CSV contains 50,000 data rows while the prior expected count was 49,997.
- Corrected the stale license assertion, changed evaluator/workflow expected rows to 50,000, and clarified the corpus registry that upstream README describes 49,997 samples while the pinned CSV actually has 50,000 data rows. The CSV hash remains the immutable snapshot identity; the discrepancy is explicitly documented, not hidden.
- Fix commits: 357d83c10ee2647b0debe5c7efe52b489c37f4bd, ea27324a044e7d9c3298285e09bc7959b15681f5, 55306fda1af8c9652854e6d504ff56ff0358fdeb, 906e1293203635dcf481dbc164712403d088231c, e05d5644f94b5d9c8707c3da981182822d272fa0.
- Acceptance remains pending: exact-head CI must pass; corrected VISTEC run must process all 50,000 rows and produce an inspected artifact; no independent-gold accuracy claim is justified.


### Corrected-head CI handoff — 2026-10-26

- Corrected the stale corpus license assertion and aligned the evaluator plus all three workflow row-count checks to the 50,000 data rows actually present in the pinned CSV blob. The upstream README's separate 49,997-sample statement remains documented as a metadata discrepancy.
- Current code-bearing workflow commit: `ccee129d509c95f95c2f455fd769bcbcd9ae71e0`. Latest runs: CI 40353097806, Web static validation 40353097480, external VISTEC evaluation 40353097539. All were queued at the last poll; no tests or metrics are marked passed on this head.
- Do not merge or release until exact-head CI/static validation pass, VISTEC processes all 50,000 rows and its report artifact is inspected. Independent linguistic adjudication and official OBEC PDF access remain genuine evidence blockers.


### Follow-up CI diagnosis and repair — 2026-10-26

- The exact-head CI run [40354836807](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40354836807) completed with one failure among 194 Python tests: `test_segmentation_sources_preserve_license_and_usage_gates` still required the obsolete substring `verify upstream terms` for VISTEC, while the registry now correctly records the pinned README's explicit CC-BY-SA-3.0 declaration and attribution/share-alike obligation.
- Updated that assertion to check `attribution/share-alike required` instead. Fix commit: `0e60b2d277facee573839335b7e1681d5520a224`. This is a test-expectation correction to match the verified source registry; it does not weaken the license gate.
- For the prior head `2f049649b0c4c2524b1cd9fbca243e8c650e72ae`, Web static validation [40354836884](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40354836884) and external VISTEC evaluation [40354836797](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40354836797) passed. VISTEC processing ran against the pinned 50,000-row CSV; its labels remain source-annotated, not expert-adjudicated.
- The CI run above used GitHub's PR merge ref and failed before downstream diagnostics could run. Fresh exact-head checks for the test fix are required; do not infer that CI is green from the two passing workflows.
- Remaining blockers unchanged: independent Thai IPA/acoustic review, independent Ukrainian target judgments, human segmentation adjudication, contextual review of บรรจุ final /ʔ/, and lawful full-PDF access for the cited OBEC source (prior HTTP 403). No release or merge was performed.


### VISTEC source-annotation results read from successful workflow report — 2026-10-26

- External run [40354836797](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40354836797) succeeded and emitted the full JSON report in the workflow log; artifact ZIP metadata is also available (artifact ID 12667445022, SHA-256 a02e3c8fe769a9b0998fdf2e66a49d6d0bec1c0b7191e08854d2dd81cc50132c). The archive itself has not been downloaded/opened, so acceptance still includes artifact-level inspection.
- On all 50,000 source-annotated rows (zero expert-adjudicated rows), dictionary maximum matching: boundary precision 0.76880, recall 0.89788, F1 0.82834, exact token sequences 76/50,000 (0.152%). Research-only TUD unigram Viterbi: precision 0.60640, recall 0.99316, F1 0.75302, exact token sequences 16/50,000 (0.032%). Both report 100% output coverage; this does not mean accurate segmentation.
- These are descriptive agreement metrics against upstream source annotations, not expert accuracy. The extremely low exact-sequence rates and differing precision/recall profiles make clear that neither model is production-ready. Do not tune on this external evaluation set or present these metrics as independently adjudicated gold.
- The fresh checks triggered by the test assertion fix and subsequent audit updates are queued: CI [40360861858], Web static validation [40360861799], VISTEC [40360861912]. No result is claimed for those runs.


### Artifact archive inspected — 2026-10-26

- Downloaded and opened artifact ZIP 12667445022 from successful VISTEC run 40354836797. Archive contains only `vistec-segmentation-report.json` (3,803 bytes). Parsed the JSON and independently confirmed schema 1.0, 50,000 source-annotated rows, 0 adjudicated rows, and metrics recorded above; report status remains `MEASURED_ON_SOURCE_ANNOTATED_ROWS_NOT_EXPERT_ADJUDICATED`. ZIP digest matches GitHub artifact metadata: `a02e3c8fe769a9b0998fdf2e66a49d6d0bec1c0b7191e08854d2dd81cc50132c`.
- Artifact acceptance is now DONE_VERIFIED for reproducible source-annotation diagnostic output. This does not satisfy independent linguistic adjudication or release gates. Fresh exact-head CI/Web/VISTEC runs remain queued at the latest poll.

## Public beta-site continuation — 2026-10-26

### UI changes in this batch
- `web/index.html`: added a visible Ukrainian research-beta notice before the input area, explicitly warning that outputs are candidates rather than an official norm or guaranteed pronunciation; links to the evidence/limitations section.
- `web/system.html`: added the same beta notice and a public evidence section reporting the pinned VISTEC/Wisesight segmentation diagnostics and zero independently expert-reviewed rows.
- `web/src/styles.css`: added responsive styling for the beta notice.
- `web/tests/ui-contract.test.mjs`: added regression assertions for the beta label, evidence anchor, metric denominators, and mobile styling.
- `docs/validation-matrix.md` and `docs/final-audit.md`: updated in place with beta status, deployment boundary, and outstanding external evidence gates.

### Evidence published to the site
- VISTEC (50,000 source-annotated rows): dictionary F1 0.82834 / 76 exact sequences (0.152%); TUD Viterbi F1 0.75302 / 16 exact sequences (0.032%).
- Wisesight (993 source-annotated rows): dictionary F1 0.83947 / 192 exact sequences (19.34%); TUD Viterbi F1 0.74862 / 119 exact sequences (11.98%).
- Neither set is independent expert gold. Zero rows have independent expert adjudication. These metrics are agreement diagnostics only and do not establish Thai pronunciation accuracy. Neither segmenter is production-ready.

### Verification and deployment boundary
- Latest successful verification before the beta UI edits: commit `17eac785a00ce1e8a95ac904db348ddf8c286040`; CI 40372261539, Web static validation 40372261553, and external VISTEC evaluation 40372261718 all succeeded.
- The beta UI and new UI assertions were committed after that verified checkpoint. Exact-head CI/static checks for the new UI are pending; do not mark them PASS until the actual runs succeed.
- Pages workflow deploys only on pushes to `main` (or manual dispatch). PR #71 is still draft. The 304-commit research PR was not merged, and its branch was not deployed over the existing public site. Public publication is therefore not yet verified; next acceptance criterion is successful exact-head CI/static checks, review of the PR diff, then deliberate merge/deploy or a separate preview host.
- Current research prototype remains not release-ready for arbitrary Thai text. Remaining external blockers: independent Thai IPA/acoustic review; two independent Ukrainian target-form reviews; human segmentation adjudication; context-level review of บรรจุ final /ʔ/; and lawful access to the full official OBEC PDF (prior URL returned HTTP 403).

## Final beta-site handoff — 2026-10-26

### Implementation and verification
- Research-beta banner added to `web/index.html` and `web/system.html`; evidence/limitations anchor and source-annotation segmentation metrics are visible on the system page.
- Responsive styles added in `web/src/styles.css`.
- `web/tests/ui-contract.test.mjs` now checks beta disclosure, evidence anchor, full metric denominators, and responsive styling.
- `.github/workflows/pages.yml` includes the UI-contract test in the Pages build. A temporary branch deployment trigger was tested, then removed; the workflow again deploys only on `main`.

### Actual results
- Pages build run [40377552366](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40377552366): build job PASS — Python regression tests, browser parity, UI contract and Pages artifact upload all succeeded. Deploy job FAILED immediately before executing steps; no logs or pending approval details were exposed.
- Web static validation [40377552367](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40377552367): PASS.
- VISTEC evaluation [40377560151](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40377560151): PASS; source-annotation diagnostic only, not independent gold.
- The latest successful public Pages deployment remains main commit `18ab41db87192dc7be69683ef85e53cb04db5517`, run [40225366216](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40225366216). Public URL: https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/. The beta changes are **not live yet**.
- Exact cause of the branch deployment failure is unknown because the deploy job had no steps/logs; no external settings were changed. Pages is restored to main-only deployment to prevent repeated attempts from the draft branch.

### Current branch and next genuine blocker
- Latest branch head before this handoff synchronization: `048b89d9234ac91e3d592c0bca7d816f4a5ae5b5`; PR #71 remains open Draft, 304 commits / 68 changed files. Latest push/PR CI runs were still in progress when checked; do not mark exact-head CI fully green until the master-artifact job completes.
- Do not merge the large draft PR blindly. To publish this exact engine, the owner must either review and merge PR #71 to `main` while accepting the documented evidence limitations, or authorize a separate preview host. No PR was merged and no release was published.
- Independent Thai IPA/acoustic gold, two independent Ukrainian target-form reviews, human segmentation adjudication, context-level review of บรรจุ final /ʔ/, and lawful full official OBEC PDF access remain evidence blockers. The site must continue to call itself a research beta and must not claim empirical pronunciation accuracy.

## Post-merge handoff correction — 2026-10-26 20:51 EET

The pre-merge statements earlier in this handoff are historical and are superseded by this section.

- PR #71 is merged to `main` as `b4ae9e9f88a79d6f55cb1207363ac6877df080ba`.
- Pages run [40378981918](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981918): build job passed, including Python regression tests, generated fixture parity, browser parity, UI-contract/beta-disclosure checks, and artifact upload. The deploy job `121775188761` remained queued without a runner or steps for over two hours. Pending-deployment approvals were empty; the exact queue cause is unknown.
- Web static validation [40378982254](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378982254) passed. CI [40378981710](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981710) test job passed, but its master-artifact job was still queued at last check.
- The public Pages URL is https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/. The last confirmed successful deployment is still run [40225366216](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40225366216), commit `18ab41db87192dc7be69683ef85e53cb04db5517`. The new beta is merged, but not yet confirmed live; don't tell users it is deployed until run 40378981918's deploy job succeeds and the live page is checked.
- The connected Firecrawl account reported insufficient credits; the direct web fetch was inaccessible. No repeated scrape was attempted. No external settings were changed, no alternate hosting project was created, and no release was published.
- Canonical records were updated on `main`: `docs/validation-matrix.md`, `docs/final-audit.md`, and `docs/final-audit.json`. Most recent audit-record commit at the time of this handoff is `c953bf174139f2f1091ff1b6b1cae040f3774993`; the handoff itself is being updated in this commit sequence.

### Next action
Inspect GitHub Actions runner/queue availability, then retry or wait for the queued Pages deploy without weakening branch or environment restrictions. After successful deployment, verify the served index and system page show the beta notice and evidence/limitations section, then update these same canonical records with the actual deployed commit and check. The independent Thai IPA/acoustic gold, human segmentation adjudication, independent Ukrainian target-form reviews, contextual review of บรรจุ final /ʔ/, and lawful full official OBEC PDF access remain research blockers. This remains a **research beta candidate, not a release-ready general-purpose Thai transcription system**.

## Final correction — successful Pages deployment — 2026-10-26 22:08 EET

This section supersedes the earlier queue-blocker status in this handoff.

- **GitHub Pages deployment succeeded.** Run [40378981918](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981918) completed with build job 121769734639 PASS and deploy job 121775188761 PASS.
- **Main CI succeeded.** Run [40378981710](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981710) passed both the test and master-artifact jobs.
- **Static validation succeeded.** Run [40378982254](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378982254) PASS.
- Public URL: https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/. Beta source is merged via `b4ae9e9f88a79d6f55cb1207363ac6877df080ba`.
- Direct inspection of the served HTML could not be completed because the available web fetch could not access the Pages URL. This is a verification limitation, not a failed Actions deployment. If convenient, open the public URL in a normal browser to confirm the visible beta notice and evidence panel.
- Canonical records updated in `docs/final-audit.json`, `docs/final-audit.md`, and `docs/validation-matrix.md`. Latest main CI checked before this doc update: [40381878163](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40381878163), PASS.

**Readiness:** deployed research beta, not release-ready for arbitrary Thai text. Still unresolved: independent Thai IPA/acoustic gold, human segmentation adjudication, two independent Ukrainian target-form reviews, context review of บรรจุ final /ʔ/, and lawful full official OBEC PDF access. Keep all beta and evidence caveats visible; do not claim expert-validated accuracy.


## Continuation update — whole-text web input — 2026-10-26

The web endpoint previously treated each uninterrupted Thai-script run as one dictionary key. Any absent full-run key became unresolved, so adjacent known words could not emit IPA. This was a real execution gap, not merely a homepage-example problem.

On branch `fix/examples-ipa-coverage-20261026`, the web engine now applies conservative longest-match segmentation against its reviewed text lexicon and source-attested IPA override keys. It emits known entries separately and retains contiguous unmatched material as unresolved spans, allowing known neighboring words to produce IPA without inventing pronunciation for unknown material. UI-contract tests cover adjacent known entries (`กาไฟมา`), an unknown span followed by known entries (`ทดสอบกาไฟ`), and punctuation/whitespace (`กาไฟ มา!`). The quick examples were aligned to entries that currently produce phonological IPA.

**Scope warning:** this is a deterministic dictionary-max-match baseline, not a complete Thai word segmenter. It can make wrong boundary choices when a known entry occurs inside an unknown word or when multiple analyses are possible. Do not advertise arbitrary Thai text as fully recognized. Existing source-annotated segmentation scores are diagnostics, not independent expert gold.

**Verification state at handoff (checked 2026-10-26):** latest branch head before this handoff correction was `d7d7acf268e3f1e46abc302d5a0b1eb0b4aad530`; the engine, UI tests, homepage hint/examples, validation matrix, audit, and handoff updates are present. Exact-head GitHub CI run [40397682426](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40397682426) (`test`) and web static validation [40397682437](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40397682437) (`validate`) were still **queued** at last check, so this implementation is not yet `DONE_VERIFIED`. Recheck their conclusions on the new head after this documentation-only correction. If either fails, inspect logs, fix, and rerun. Next real work after green CI: evaluate the browser segmenter on pinned, held-out Thai boundary data; add adversarial ambiguity and unknown-word fixtures; compare precision/recall with the existing Python segmentation baseline; improve segmentation only where evidence supports it. Keep independent IPA/UA review and all other research blockers open.


### Follow-up regression coverage — 2026-10-26

After the prior handoff note, UI-contract coverage was extended to the reviewed full-sentence entry `กินข้าวกับไข่และผลไม้` (expecting seven syllable-level phonological IPA outputs) and punctuation-separated runs `กา,ไฟ!มา`. The matrix now lists these cases. Latest code/test head at this update is `f872eaf84d73c86c9dba00d2cc2e5ea4c0b3a70e`; the subsequent matrix-only docs commit is `1b1ecc8a64b963adc4aef0e2801deda077ac4e3b`. CI and static validation were queued for the latest head at the time of checking; do not infer pass from queued or in-progress older runs. Recheck the latest SHA's workflows before changing status.


### Verification closeout — whole-text input — 2026-10-26

**Verified code checkpoint:** `1b1553876ef24bf18f692d7aa512634bdceeee70`. CI run [40400809948](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40400809948) completed successfully for both `test` and `master-artifact`; the latter validated the generated master table at 351,780 rows and 41 vowel records. Web static validation [40400809797](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40400809797) passed. The UI-contract and parity tests passed after correcting their assertions: unknown-span abstention now uses the truly unknown `ทดสอบ`, IPA counts target visible field labels rather than copy-button accessible labels, and punctuation expectations match the app's preserved-token rendering.

The documentation-only follow-up commits update the matrix and audit; the code-bearing checkpoint above remains unchanged. PR #73 was subsequently merged as `e49b5f2b54d42e577f732b4308080e11e410d557`. The code checkpoint passed CI test + master-artifact and web static validation. The Pages workflow is configured to deploy on relevant pushes to `main`, but the live deployment is still unverified because the available tools could not retrieve push-triggered workflow runs or fetch the served HTML. Do not mark general Thai segmentation or linguistic accuracy as complete: the greedy dictionary baseline remains partial, and independent segmentation adjudication, Thai IPA/acoustic gold, and Ukrainian target-form reviews remain blockers.


### Final follow-up — lexical override UI status — 2026-10-26

The latest code-bearing head is `3ccf84f564add02c189524c3b9ca794154d35c8b`. A final review found that `lexical_ipa_override` tokens rendered valid IPA but the summary counter treated them as unresolved because it accepted only `lexicon`; the UI now treats both statuses as resolved, and the UI-contract test covers adjacent source-attested override entries `เงินเดิน`. For this code head, CI `test` and `master-artifact` both passed in [run 40402504410](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504410), and web static validation passed in [run 40402504394](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504394). PR #73 is merged as `e49b5f2b54d42e577f732b4308080e11e410d557`. The Pages deployment remains **unverified**, not failed: GitHub Pages is configured to deploy on relevant `main` pushes, but push-triggered run listing and live HTML retrieval were unavailable through the connected tools. Next genuine blocker is deployment confirmation, followed by independent Thai word-boundary adjudication and IPA/UA review.


## Current continuation checkpoint — 2026-10-27

- Main merge commit at the start of this documentation refresh: `581231596a0df6b3ab58964dacedeec7a8fd8908` (PR #75, documentation reconciliation).
- PR #75 CI [40406992550](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40406992550) is complete and green: `test` + `master-artifact`. This includes generated-data drift, Python tests, 351,780-row / 41-vowel master artifact, Node IPA→Ukrainian, Python/browser parity, UI contract, and segmentation/IPA diagnostic gates.
- Runtime code checkpoint remains `3ccf84f564add02c189524c3b9ca794154d35c8b`; its CI [40402504410](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504410) and static validation [40402504394](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504394) passed.
- Current statuses: whole-text input = DONE_VERIFIED; known-entry greedy segmentation = PARTIAL; general Thai segmentation = TODO / evidence-limited; complete IPA for arbitrary text = BLOCKED by coverage and linguistic evidence; live Pages publication/served markup = UNVERIFIED.
- Do not confuse successful CI with a complete transcription engine. Greedy longest-match may choose a known substring inside an unknown word; unresolved spans must not receive guessed IPA. The next engineering improvement should target adversarial false-split/false-merge cases and be evaluated against pinned held-out boundaries, not add unsupported word guesses.
- Pages acceptance criterion: confirm a successful Pages build/deploy run after the relevant main change and inspect served HTML. Previous known deployment run [40378981918](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981918) predates the whole-text UI change.
- Research blockers remain: human-adjudicated Thai boundaries, independent Thai IPA/acoustic gold, two Ukrainian target-form reviews, contextual `บรรจุ` final /ʔ/ review, lawful full official OBEC PDF, and per-resource license/attribution audit.
- Readiness: partial research prototype, not release-ready for arbitrary Thai text.


## Continuation checkpoint — CC0 browser segmentation fallback — 2026-10-27

- Main merge commit: `96c2af3c2a24d0ea95455b5d6af4c079e5609d29` (PR #77).
- Added `scripts/generate_web_word_dictionary.py`, which validates the pinned CC0 word-list Git blob SHA, license declaration, 60,963 unique Thai-block entries, and required regression word `กาแฟ`; it generates ignored `web/src/word-dictionary.generated.js` (1,615,714 bytes, 51 initial-character buckets).
- Browser segmentation now considers both the curated pronunciation lexicon and the CC0 word dictionary, prefers the longer match, and prefers curated entries on ties. A longer dictionary match prevents partial IPA for a known substring. Dictionary segmentation remains boundary evidence only; non-curated words remain unresolved with no guessed IPA/UA.
- Regression `กาแฟ` prevents partial output for `กา`; regression `เงินเดิน` exposed a preposed-vowel boundary bug, fixed by excluding preposed vowels from the combining-mark set.
- Web static validation passed on pre-merge head `7b2c9572feb542fb3ee81558b9758bb4fa5f2bef` ([40411659863](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40411659863)). Full CI test job passed on code head `3eb1155631da158b7e04436f608711680750e475` ([40411558761](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40411558761)); exact-head full CI and master-artifact remained queued, so they are not marked passed.
- Post-merge Pages run `40412224812`, main CI `40412224673`, and web-static push run `40412224629` were queued at last inspection. The Pages workflow now retries until it verifies the served homepage contract. Check these runs before claiming deployment verified.
- Next: confirm post-merge Pages check; inspect whether the 60k dictionary bucket scan has acceptable browser latency on representative 100–500-character text; then improve coverage only with source-attested syllabification/pronunciation. General Thai segmentation, independent IPA gold, UA target review, `บรรจุ` contextual adjudication, OBEC PDF access, and per-resource license audit remain open.
- Readiness: partial research prototype, not release-ready for arbitrary Thai text.


## Continuation update — browser dictionary lookup cost — 2026-10-27

The post-merge CI and Pages workflow were rechecked: main CI run [40412393544](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40412393544) passed both `test` and `master-artifact`; Pages run [40412224812](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40412224812) passed build, deploy, and the post-deployment HTML contract check. The deployed site therefore includes the whole-text UI contract on the deployment associated with the merged browser-dictionary change.

A follow-up performance audit found that dictionary lookup selected candidates by first Thai code point, potentially scanning a large candidate bucket at every unmatched position. Branch `perf/browser-dictionary-prefix-index-20261027` changes the generated index to two-code-point prefixes, validates that every word is stored under the correct key, and reports the largest bucket in generator output. The matching policy is unchanged: longest match, curated lexicon wins ties, and dictionary-only matches never authorize IPA/UA.

Do not call this optimization complete until the branch's exact-head CI and web validation pass. The remaining major blocker is still evidence, not code structure: no independently adjudicated Thai boundary/IPA gold or two independent Ukrainian target-form reviews are available. The engine remains a partial research prototype for arbitrary Thai text.

## Continuation — prefix-index implementation under verification (2026-10-27)

Branch `perf/browser-dictionary-prefix-index-20261027` is based on main `91e5b8daef8b610e75aef52a087d7ffbed983ac6`. It changes the browser's generated CC0 word dictionary to two-code-point prefix buckets, checks the one-character bucket as a fallback, and adds parity-test assertions for all 60,963 entries, key correctness and longest-first ordering. This narrows the candidate set scanned at each offset without changing lexical precedence or treating dictionary matches as pronunciation evidence.

**Do not merge until verified:** branch-head CI must pass the Python tests and generated master artifact job; Web static validation must pass the generated dictionary and browser parity tests. A measured runtime benchmark is still desirable before claiming a quantitative speedup. Unknown text must continue to abstain from IPA/Ukrainian output. The independent Thai boundary/IPA gold and two independent Ukrainian target-form reviews remain genuine research blockers; the repository is still a partial research prototype, not release-ready for arbitrary Thai text.

## Final status — browser prefix-index optimization (2026-10-27)

PR [#79](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/79) was merged to main as `c799dbed4247ac9743845acc0fd4131922cfbb74`. The code-bearing branch head `e17a7f96fef9989f6375d36331f30ce0246e378a` passed full CI including `test` and `master-artifact` ([40466046264](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466046264)) and Web static validation ([40466046237](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466046237)). After merge, main Pages deployment and its served-HTML check passed ([40466830868](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466830868)); main Web static validation passed ([40466830820](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466830820)). The main CI `test` job passed in [40466830808](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466830808); its redundant `master-artifact` packaging job was still running when this note was written, although that job had passed on the code-bearing commit.

Generator output observed in CI: 60,963 entries, 1,085 two-code-point buckets, largest bucket 1,521 entries, 1,629,301 bytes (13,587 bytes / ~0.84% larger than the old uncompressed index). This demonstrates a narrower lookup index, not a measured latency gain. The UI contract, unresolved-span behavior and IPA-first safety boundary remain intact.

Remaining genuine blockers: independently adjudicated Thai segmentation boundaries, independent Thai IPA/acoustic gold, two independent Ukrainian target-form reviews, contextual review of `บรรจุ` final /ʔ/, lawful access to the complete official OBEC PDF, and per-resource license/attribution review. General arbitrary-text IPA coverage remains partial; release status remains research prototype, not release-ready.

## Continuation — browser segmentation latency measurement (2026-10-27)

Branch `perf/browser-segmentation-latency-benchmark-20261027` adds a non-gating, reproducible Node diagnostic at `scripts/benchmark_web_segmentation.mjs`. CI runs five warmups and 30 measurements for 100-, 250- and 500-code-point Thai inputs, reports median/p95/min/max plus output counts, and uploads `thai-browser-segmentation-latency-diagnostic`. This is deliberately not an accuracy score or latency-threshold gate. Do not claim a quantitative speedup without a comparable baseline on the same runner and runtime. Verify exact-head CI and inspect the artifact before treating the measurement task as done. Linguistic evidence blockers and the partial-research-prototype readiness classification are unchanged.


## Continuation — TLTK license evidence and post-merge verification (2026-10-27)

- PR [#98](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/98) was merged after exact-head CI runs [40521291699](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40521291699) and [40521282321](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40521282321) passed, along with Web static validation [40521292201](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40521292201). Squash merge commit: `c944a2b07c7d0af9aa1adb16e27bd77d4fdae32e`. This merges source-attested lexical forms and the shared Python/browser fixture-generator fix. Those tests establish engineering regression coverage, not independent phonetic accuracy.
- New main-head CI [40554024740](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40554024740), Web static validation [40554025097](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40554025097), and Pages deployment [40554024831](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40554024831) were queued at this snapshot; do not claim post-merge validation or deployment until completed.
- PR [#99](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/99) at head `c7a828d348476ca2937d3c1e9f4a49edbaca1686` had successful CI runs [40523750151](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40523750151) and [40523739234](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40523739234), but GitHub reports it is not mergeable against the newly advanced main. The documentation-only changes are being reconciled on this branch from the current main base rather than force-merging a conflicting PR.
- TLTK upstream artifacts remain contradictory: README.rst/setup.py claim BSD-3-Clause while the inspected repository tree also contains an LGPL v3 root LICENSE and a BSD-style LICENSE.txt. Do not reuse TLTK code until an authoritative maintainer/release clarification establishes the applicable license by version/file.
- FastThaiG2P remains benchmark-only: repo-level Apache-2.0 metadata does not by itself clear its bundled IPA dictionary, TLTK-derived fallback, or all resource-level provenance. No third-party code, model, or dictionary has been imported.
- Task ledger: PR #98 lexical fixture regression = DONE_VERIFIED for exact-head CI/static checks, post-merge main CI and Pages = PARTIAL pending current main workflows; TLTK license correction = PARTIAL pending reconciled docs PR and authoritative scope clarification; FastThaiG2P asset reuse = BLOCKED pending resource-level provenance; independent expert/acoustic IPA gold and Ukrainian adaptation review = EVIDENCE_LIMITED; arbitrary-text readiness = PARTIAL PROTOTYPE.
- Verification source: GitHub Actions API job/run records and repository file inspection. No local checkout or local test run was performed in this continuation.


## 2026-10-27 — Thai → Ukrainian methodology table

- Branch: `docs/thai-ukrainian-method-table-20261027`, based on main at `c7e686d4665c978577f771e62947545ddbc67cfe`.
- Added `docs/ukrainian-transcription-methodology.md`: context-aware initial/coda consonant table, vowel/rime orientations, Ukrainian IPA adapter conventions, tone/length preservation, contextual rules, evidence statuses, and comparison references to Thai–Russian practical transcription.
- README and validation matrix updated. No engine behavior changed. Method document is PARTIAL, not a verified standard; examples are illustrative and not independent phonetic gold.
- Remaining acceptance criteria: review the exact primary 2025 Russian reference edition if using its rules comparatively; independently adjudicate Thai IPA and Ukrainian target forms; encode approved rules in a versioned machine-readable registry only after evidence review; add regression tests and held-out evaluation. Keep lexical ambiguity fail-closed.

- Follow-up after the completeness question: added section 11 to the method document enumerating the 44-consonant inventory, conventional 32-vowel-form set, tone marks, diacritics, special signs, digits, and mixed-script policy. Added NECTEC/W3C/Thai Orthography Notes references. This closes a documentation inventory gap, not the engine-coverage gate.
- Still required: automated inventory/Unicode tests against actual runtime, exact per-character/context rule registry, independent IPA and Ukrainian target review. Do not describe all-letter support as verified until those checks run.


## 2026-10-27 — українські особливості тайської практичної транскрипції

- Branch: `docs/thai-ukrainian-method-table-20261027`; new research document: `docs/ukrainian-vs-russian-thai-transcription.md`.
- Compared the Thai–Russian practical table against the official Ukrainian orthography standard and Ukrainian scholarship on practical transcription of foreign proper names.
- Candidate issues recorded: Thai /ɯ/ → Ukrainian «и» as an approximation; project policy /h/ → «г» with IPA /h/ preserved; one-letter Ukrainian practical forms for aspirates; contextual /j/ and Ukrainian йотated letters; /w/; /ɛ/~/e/ neutralization; Thai /tɕ, tɕʰ/ → «ч», not «дж».
- **PARTIAL / EVIDENCE-LIMITED.** Documentation now records the chosen project policy: /h/ → «г»; /kʰ pʰ tʰ tɕʰ/ → one Ukrainian letter each (к/п/т/ч); Thai /tɕ/ and /tɕʰ/ both → «ч», not «дж» because they are voiceless and differ by aspiration, whereas Ukrainian «дж» is voiced /d͡ʒ/. IPA must preserve /h/, aspiration, and the affricate distinction. No runtime rules changed in this documentation batch. Code inspection confirms the browser and Python IPA→Ukrainian adapters already implement these mappings, and their existing test files assert them. Next acceptance: obtain passing CI evidence on the current PR head, then validate source-attested Ukrainian names and independent IPA/editorial adjudication.


### Follow-up — Thai Ukrainian IPA adaptation implementation (2026-10-27)

This note supersedes the preceding documentation-only status. The branch now changes `src/thai_ukrainian/ukrainian_adaptation.py` and `web/src/ipa-ua.js` so IPA /h/ maps to Ukrainian «г»; aspirated /kʰ pʰ tʰ tɕʰ/ render as one practical Ukrainian letter each; /tɕ/ and /tɕʰ/ both render as «ч», never «дж». Regression cases were added to `tests/test_ukrainian_adaptation.py` and `web/tests/ipa-ua.test.mjs`, and `data/derived/thai_consonant_correspondence.csv` was aligned with the candidate generator. Status: PARTIAL pending exact-head CI, parity, and generated-artifact validation. This is a project adaptation decision, not an official standard or an accuracy benchmark; IPA retains /h/ and aspiration distinctions.


## 2026-10-27 — continuation: verified IPA policy merge and benchmark evidence gate

- Branch for this audit/handoff update: `audit/thai-ipa-benchmark-gates-20261027`, created from the then-current `main` after PR #106 was merged. Starting main before merge: `c7e686d4665c978577f771e62947545ddbc67cfe`; PR #106 head: `7e4ccb8aa789f97144ee46a9b5927402cb58e05c`; merge commit: `e3052ff9bede79ed8b4f19e746ce545912cfd7d5`.
- PR #106 was not merged blindly: exact-head CI run [40586665956](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40586665956) passed; Web static validation [40586665936](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40586665936) passed. The PR contains Python/browser IPA-adapter mappings and regression tests for /h/ → г, aspiration neutralization only at the Ukrainian practical layer, /tɕ/ and /tɕʰ/ → ч, and rejection of unsupported /d͡ʒ/ as a Thai correspondence. This is a verified implementation/policy change, not evidence of general end-to-end accuracy.
- **Benchmark data-quality gate:** `data/benchmark/gold.tsv` contains only its header (0 gold rows). `data/benchmark/source-attested-ipa.tsv` contains 6 source-attested dictionary entries, all explicitly labelled `SOURCE_ATTESTED_NOT_GOLD`. `data/benchmark/thai_g2p_challenge.jsonl` has 42 challenge candidates, with 0 adjudicated gold IPA labels; these are probes, not scored test cases. `data/benchmark/segmentation-predictions.tsv` is header-only (0 prediction rows), so the 606,026-byte segmentation-gold file cannot yield a current prediction score. Target-adjudication entries are candidates pending independent adjudication, not preference gold. No accuracy percentage or before/after accuracy claim is valid from these datasets.
- Existing external-engine evidence remains smoke/diagnostic only: `data/external-ipa-renderers.json` documents Goruut with partial coverage and variable output; prior smoke results for ThaiPhon and FastThaiG2P are execution/inter-engine comparisons without independent gold. No external engine is promoted to a production dependency and no external IPA output is treated as gold. Resource-level provenance/licensing and output conventions remain unresolved for potential reuse.
- PR #104 morphology branch has exact-head CI [40574979967](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40574979967) and [40574969370](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40574969370) successful and Web static validation [40574979983](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40574979983) successful on head `9fbdb5d9a73fe36fc3c6d42e6800304a46c06d1b`. It remains open and is not merged here: it was based on older `main`, overlaps browser/README/audit/handoff files, and needs reconciliation against merged PR #105 and now-merged PR #106 before integration. Earlier PR #101 remains untouched.
- Task ledger: IPA adaptation policy implementation + Python/browser regression CI = `DONE_VERIFIED`; main integration of #106 = `DONE_VERIFIED`; source-attested IPA inventory = `PARTIAL`; end-to-end G2P accuracy evaluation = `BLOCKED` by absent adjudicated gold; segmentation accuracy evaluation = `BLOCKED` by header-only predictions; Ukrainian target-form accuracy = `BLOCKED` by pending independent adjudication; external engine production integration = `DEFERRED` pending reproducible interface, provenance/license review, deterministic candidate contract, and IPA validation; PR #104 = `PARTIAL` pending rebase/reconciliation and exact post-rebase verification.
- Environment limitation: a local shallow clone was attempted but failed because this runtime could not resolve `github.com` (`Could not resolve host: github.com`). Therefore no local Python, browser, build, or generator commands are claimed as executed in this session. Verification cited above is GitHub Actions evidence only. This audit branch documents evidence and does not claim local reproducibility.
- Acceptance criteria for a real accuracy benchmark: (1) independently reviewed and source-cited IPA gold with status and license per row; (2) nonempty, reproducible predictions generated by the exact tested commit; (3) separate metrics for structure/segmentation, IPA, target adapter on adjudicated IPA, end-to-end output, strict refusal quality, approximate coverage, and regressions; (4) versioned run metadata and held-out split. Do not populate gold with guesses merely to make metrics available.

## 2026-10-27 — source-attested lexical tone-pair coverage

- Branch: `feat/source-attested-lexical-ipa-coverage-20261027`, based on `main` at `8c082ea530ef0c4c8e67b25837b05273316c0b84`.
- Added exact-form lexical IPA records for `ไกล` (/klaj/, mid tone; Wiktionary revision 5688545) and `ใกล้` (/klaj/, falling tone; revision 5721860). Both records retain CC-BY-SA-4.0 provenance and `ACTIVE_SOURCE_ATTESTED_NOT_GOLD` status. They flow through the existing typed IPA → Ukrainian adapter; they are not promoted to adjudicated gold.
- Added regression tests for source revision, IPA segment string, tone contour, diphthong classification, Ukrainian adapter output, and visible non-gold warning. Updated the source registry test to validate the new records.
- This is a narrow, evidence-backed coverage improvement for a lexical tone pair, not a general G2P accuracy claim. Source-attested dictionary entries can be wrong or reflect a particular transcription convention; independent review remains required.
- **Verification status:** code/data/tests committed to the branch; exact-head CI and web static validation must pass before DONE_VERIFIED. No local tests are claimed because local GitHub DNS access was previously unavailable.
- **Remaining benchmark blocker:** `data/benchmark/gold.tsv` still has zero independently adjudicated rows; no overall accuracy or before/after score can be reported. Do not copy these two source records into gold as if independently adjudicated.


## 2026-10-27 — source-attested diagnostic assertion reconciliation

- Exact-head CI run [40591565959](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40591565959) passed master-table generation and all 203 Python tests. It then failed at the source-attested IPA diagnostic guard because the workflow still expected the old split (2 circular / 4 independently comparable) after the `ไกล` and `ใกล้` overrides were added.
- Actual diagnostic output is still 6 source records and 6 complete outputs, but now 4 records are circular and 2 remain independently comparable; segmental agreements = 1 and tone agreements = 2. No accuracy is claimed.
- Updated the workflow guard and current audit summary to match the observed diagnostic, preserving circularity checks against the actual records. A new exact-head CI run must pass before merge; do not mark DONE_VERIFIED yet.
- The independent IPA gold fixture remains empty, so end-to-end pronunciation accuracy is still BLOCKED by independent adjudication rather than by missing implementation alone.


## 2026-10-28 — verified merge and live Pages deployment

- PR [#108](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/108) was squash-merged into `main` as `c6ba73b77766b0169d70619383b6efe27564d774`. This is the single active release path; no user branches were deleted.
- Exact-head CI [40592380586](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40592380586) passed both `test` and `master-artifact`. Web static validation [40592380619](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40592380619) passed, including browser JavaScript syntax, Python/browser parity fixtures, and IPA→Ukrainian/UI contracts.
- GitHub Pages deployment [40592864388](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40592864388) passed its build and deploy jobs. The post-deploy workflow verified the live whole-text interface, strict/soft/super-soft modes, and IPA adapter contract at https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/.
- The Python/browser lexical IPA adapters now both handle the source-pinned pair `ไกล` and `ใกล้` as phonemic /klaj/, preserve mid vs falling tone, return the same Ukrainian candidate `клай`, and withhold surface IPA because the dictionary source does not provide an independently verified surface-phonetic form. Both entries remain `SOURCE_ATTESTED_NOT_GOLD`.
- The source-attested diagnostic reports 6 records, 4 circular source overrides, 2 independently comparable records, 1 segmental agreement and 2 tone agreements. This is source-comparison evidence, not an accuracy score. `data/benchmark/gold.tsv` remains without independently adjudicated IPA gold; overall G2P/IPA/end-to-end accuracy is still NOT_MEASURED.
- Post-merge CI run [40592864584](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40592864584) had its `test` job pass; its separate `master-artifact` job was still running at audit time. The exact-head PR CI above passed both jobs, and the Pages build independently generated the master table and passed its Python/browser checks.
- PR #101 was closed as a duplicate of #104; PR #104 was closed/deferred because its separate research-only morphology overlay was based on an older main and had not been reconciled against the deployed head. Both source branches are preserved. Reopen/port that feature only after rebasing, exact-head CI and browser parity, and keeping morphology outside practical phonetic output.
- Readiness: engineering and deployment checks are verified; the project remains a research prototype, not release-ready for accuracy claims, pending independent IPA gold and Ukrainian target-form adjudication.


## 2026-10-28 — Thai phonology completeness and ambiguous readings

- Working branch: `audit/thai-phonology-ambiguity-coverage-20261028`, based on current `main` at `c1d19996b027822d6e079ba33cabee52587da592`.
- Added `docs/phonology-ambiguity-coverage.md`, a source-backed audit matrix for tone/live-dead rules, onset clusters, codas, `ห นำ`/`อ นำ`, `ทร`, false clusters (`จร/สร/ศร/ซร`), `รร`, `ฤ/ฤๅ/ฦ/ฦๅ`, thanthakhat, lexical segmentation, and connected speech.
- Added regression tests requiring unlisted special-orthography forms to remain analysis-dependent and verifying that the exact lexical reading `ทราบ` does not make `ทร` a productive global /s/ rule. The Royal Institute source explicitly distinguishes `ทราย` “sand” (non-cluster /s/) from `ทราย` in the deer-name family (true cluster reading); the engine must not guess the sense from spelling alone.
- This is a coverage audit and fail-closed regression hardening, not a broad phonology expansion. No unsupported IPA labels or accuracy claims were added. Independent IPA gold remains blocked on expert adjudication.
- Status pending: exact-head CI, generated master artifact, browser/Python parity and static web validation on the PR head. Do not mark the new tests DONE_VERIFIED until CI completes.


### Follow-up — productive tone-table completeness test

- Added `tests/test_tone_rule_coverage.py`: exact expected matrix for all 15 conventional tone rules, duplicate-condition detection, runtime lookup verification for every row, and rejection of mai-tri/mai-chattawa with high/low-class initials.
- This validates completeness of the declared orthographic rule table, not the parser's segmentation or acoustic tone accuracy. CI remains in progress at `generate_master_table.py`; no pass is claimed until downstream test jobs execute.


### Follow-up — context-scoped resolution for ทราย (2026-10-28)

- Source-pinned English Wiktionary revision 87239667 records the exact sand compound `ทะเลทราย` as `ทะ-เล-ซาย`, IPA `/tʰa˦˥.leː˧.saːj˧/`, CC BY-SA 4.0. Added this exact compound to the Python text lexicon and browser lexical map; its Ukrainian candidate is produced syllable-by-syllable through the existing IPA adapter.
- The isolated homograph `ทราย` remains analysis-dependent because the Royal Institute 2011 article distinguishes sand from the deer-name sense, which has a true cluster. No context-free override was added.
- Added Python and browser regression tests for the exact compound, IPA/tone sequence and Ukrainian adapter result, while retaining the isolated-homograph abstention test. CI still needs to complete before marking the code/data change DONE_VERIFIED.


### CI generator performance fix — special-orthography registry cache

- Added `functools.lru_cache(maxsize=1)` to `load_special_rules()`. The exhaustive master-table generator re-parses 351,780 structural combinations; the uncached loader reopened `data/thai/special_orthography.csv` for each parse, making a registry lookup an avoidable per-row file I/O operation.
- This is semantics-preserving: the registry is static during a run, callers do not mutate it, and the returned rules remain identical. The latest exact-head CI must verify that generation completes and all Python/browser tests pass.


### Test correction after first executable run

- The generator completed after caching the special-orthography registry. The first Python suite then ran 209 tests and reported one failure in the newly added exact-`ทราบ` regression: the test called the structural-only `parse_syllable()` API but asserted that it had already composed IPA. The production path is `api.analyze_syllable()`; the regression now exercises that end-to-end API. The source-attested desert compound and all three new tone-table tests passed in that run. Latest-head CI must rerun after this test correction.


## 2026-10-28 — ambiguity audit verification result

- Exact code/documentation head tested: `7a47e1f86862f33bb8eadfb34de75aeba5fd3809`.
- **CI run 40645028725: PASS** — all 209 Python unit tests; challenge diagnostics; web word-dictionary generation; IPA adapter, Python/browser parity and UI-contract tests; browser latency benchmark; Wisesight and TUD segmentation diagnostics; source-attested IPA diagnostic; target-candidate registry check; and the generated master artifact. The separate `master-artifact` job verified exactly 351,780 rows and 41 vowel records.
- **Web static validation run 40645028587: PASS**.
- The first new regression attempt exposed a test-harness mistake (structural-only parser asserted final IPA); it was corrected to use `api.analyze_syllable()` and the full suite then passed. The registry cache eliminated the long-running master-generator bottleneck.
- Remaining state is intentionally PARTIAL for linguistic completeness: isolated sense-ambiguous `ทราย`, the broader lexical exception space, connected speech, and independent IPA/Ukrainian target adjudication remain unresolved. Source-attested dictionary entries are not gold labels.
- Verified code/test head above is the parent of the final audit-register-only commit. The final documentation commit SHA is reported in the handoff's Git history / final report.
