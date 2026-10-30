## 2026-10-30 — post-PR #150 maintenance closeout

| Task | State | Evidence / next acceptance |
|---|---|---|
| PR #148 canonical audit closeout | DONE_VERIFIED | Squash-merged as `85182af4af5a69970e8cb9506b4283056e7c65d6`; refreshed the previous mainline record and task register. Post-merge CI run [41132476418](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41132476418) passed test and master-artifact jobs. |
| PR #149 wheel packaging portability | DONE_VERIFIED | Squash-merged as `2fbf3d35a7050ae60afc7426e561503c91983446`; issue #147 closed. Runtime loaders use canonical checkout data in source/editable installs and packaged `_data/` in wheels. Source distribution → wheel → isolated install passed; installed CLI, API, all core runtime registries, Ukrainian target vectors and license notices were smoke-tested outside the checkout. Exact-head CI [41132834082](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41132834082): 214 Python tests, generated-data drift and master artifact (351,780 rows; 41 vowel records) passed. External VISTEC evaluation [41132834077](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41132834077) passed. Post-merge Pages [41133469238](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41133469238) and main CI [41133469438](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41133469438) passed. |
| PR #150 Python static-analysis gate | DONE_VERIFIED | Squash-merged as `e8282dfb85f53ae18cbed5fcdc676b1b6049c313`. Added pinned `ruff==0.17.3` dev extra and correctness-only `F` checks for `src tests scripts`. Initial Ruff red run [41133551142](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41133551142) found 16 unused-import findings; 15 stale imports were removed and `__version__` was explicitly added to `__all__`. Exact-head push CI [41133766851](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41133766851) passed Ruff, 214 Python tests, browser parity/UI tests, diagnostics, wheel smoke and master-artifact (351,780 rows; 41 vowel records). VISTEC [41133770393](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41133770393) passed. |
| Post-PR #150 mainline verification | DONE_VERIFIED | Main SHA `e8282dfb85f53ae18cbed5fcdc676b1b6049c313`; post-merge CI [41134406351](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41134406351) passed test, wheel-install smoke and master-artifact; Pages [41134406540](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41134406540) passed build and deploy. |
| Wheel packaging issue #147 | DONE_VERIFIED / CLOSED | Acceptance met by PR #149 and exact-head isolated distribution smoke; no runtime research corpora bundled. |
| Python development tooling | DONE_VERIFIED | Pinned dev extra, CI Ruff gate, 16 initial lint findings resolved; formatter/type-checker intentionally not introduced because the current task was a correctness-only baseline. |
| Historical branch retention | PARTIAL | 163 refs across two API pages: docs 46, feat 26, fix 24, research 24, chore 5, audit 8, ux 7; other prefixes and exact counts are recorded in `final-audit.json`. No mass deletion or force-rebase; retention policy remains unapproved. |
| Linguistic/UI evidence gates | BLOCKED / evidence-limited | Issue #114 remains open for independent expert-adjudicated Thai segmentation/IPA/Ukrainian target gold, manual browser/device visual review and WCAG 2.2 AA review. Software parity and source-attested forms are not linguistic gold. |
| Local checkout | BLOCKED | Container DNS cannot resolve `github.com`; no local test run is claimed. Verification is from GitHub Actions. |

**Current main:** `e8282dfb85f53ae18cbed5fcdc676b1b6049c313`.
**Readiness:** engineering-verified research prototype; not release-ready for independent linguistic-accuracy claims.

---

## 2026-10-30 — verified mainline closeout after PR #146

| Task | State | Evidence / next acceptance |
|---|---|---|
| PR #141 repository hygiene | DONE_VERIFIED | Integrated into main; single package-version source, TSV delimiter correction, regression tests and core/Pages action upgrades retained. |
| PR #144 lexical evidence forward-port | DONE_VERIFIED_FOR_IMPLEMENTATION | Squash-merged as `cb7ff2a49731d3c02ddba400a4ddbc166395d493`. Exact-head checks 5/5 successful. Adds bounded `ทราม → ซาม` mapping and ten enumerated Python/browser regression forms; no productive `ทร → ซ` rule. Evidence grade SOURCE_ATTESTED_NOT_GOLD. Superseded PRs #111 and #143 were closed with their historical branches preserved. Post-merge Pages deployment [41128531547](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41128531547) succeeded. |
| PR #145 optional workflow action refresh | DONE_VERIFIED | Squash-merged as `009060cdf12908d27d399419952bdcb50828bfd6`. Core CI, master-artifact, optional G2P smoke and VISTEC external evaluation all passed. Updated checkout/setup-python/setup-go/upload-artifact pins to v7 in the optional research workflows. Post-merge main CI [41129543349](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41129543349) and optional G2P [41129543570](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41129543570) succeeded. |
| PR #146 JSON API request contract | DONE_VERIFIED | Squash-merged as `1f53eef6522d437de546d6540ebc6c7d40ecdd82`. Non-object JSON bodies (array, null, string) now return 400 `invalid_request`, not 500. Exact-head CI passed on both push and PR runs [41129878010](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41129878010) and [41129841355](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41129841355): 214 Python tests; master artifact 351,780 rows and 41 vowel records. Red-stage run [41128931305](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41128931305) showed all three new payload cases returning 500 instead of expected 400 before the fix. |
| Mainline post-merge verification after PR #146 | PARTIAL / RUNNING at handoff | Main SHA `1f53eef6522d437de546d6540ebc6c7d40ecdd82`; CI [41130536672](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41130536672) and Pages [41130536830](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41130536830) were still in progress at last check. |
| Historical PR #111 | DONE — superseded | Closed after its bounded 13-file change was forward-ported through PR #144. Original branch/history preserved. |
| Duplicate issue #113 | DONE — duplicate closed | Closed as duplicate of issue #114 after the RTGS implementation and its later evidence-gated follow-ups were already tracked there. |
| Branch inventory | PARTIAL | 159 branch refs observed across two API pages. No mass deletion or force-rebase; preserve provenance and review unique commits before any destructive pruning. |
| Wheel packaging portability | TODO — tracked as issue #147 | Runtime loaders resolve repository-root `data/` via `Path(__file__).parents[2]`, while `pyproject.toml` does not declare/package those data files. Editable installs work; a regular wheel install may not find required registries. Acceptance: build a wheel, install into an isolated environment, run CLI/API/data-loader smoke tests outside the checkout, and verify dataset licensing/provenance. This is a verified structural risk, not yet an isolated wheel reproduction. |
| Development tooling gate | TODO | No declared dev extra or lint/type-check gate. Inventory imports/style and choose minimal tooling before adding dependencies. |
| Remaining research/UI acceptance | BLOCKED / evidence-limited | Issue #114 remains open for manual browser/device review, independent expert-adjudicated Thai segmentation/IPA/Ukrainian target gold, and separate tokenizer compatibility/licensing decisions. Automated parity and source-attested dictionary entries do not prove linguistic accuracy. |

**Current main:** `1f53eef6522d437de546d6540ebc6c7d40ecdd82`.
**Branch inventory:** 159 refs; no historical branch deletion or history rewriting.
**Open pull requests:** none at last inventory.
**Tracked open issues:** #114 (research/UI evidence gates), #147 (wheel packaging portability).
**Public service:** https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/

---

## 2026-10-30 — current mainline and API contract closeout

| Task | State | Evidence / next acceptance |
|---|---|---|
| PR #141 repository hygiene | DONE_VERIFIED | Merged to main; single package-version source, TSV delimiter correction, regression tests and core/Pages action upgrades retained. |
| PR #144 lexical evidence forward-port | DONE_VERIFIED_FOR_IMPLEMENTATION | Squash-merged as `cb7ff2a49731d3c02ddba400a4ddbc166395d493`. Exact-head checks 5/5 successful. Adds bounded `ทราม → ซาม` mapping and ten enumerated Python/browser regression forms; no productive `ทร → ซ` rule. Evidence grade SOURCE_ATTESTED_NOT_GOLD. |
| PR #145 optional workflow action refresh | DONE_VERIFIED_FOR_PR_HEAD | Squash-merged as `009060cdf12908d27d399419952bdcb50828bfd6`. Core CI and master-artifact checks passed; optional G2P smoke and VISTEC external evaluation both passed. Updated checkout/setup-python/setup-go/upload-artifact to v7 in the optional research workflows. Post-merge main CI and G2P workflow were still running at last check. |
| Historical PR #111 | DONE — superseded | Closed after its bounded 13-file change was forward-ported through PR #144. Original branch/history preserved. |
| JSON API request contract | DONE_VERIFIED | Non-object JSON bodies (array, null, string) now return 400 `invalid_request`, not an accidental 500. Test-first run [41128931305](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41128931305) failed in the unittest job after the regression was added; implementation head `16a58185cd42b687a982bb59dabbf1a49d161fed` passed test and master-artifact in [41129088376](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41129088376). |
| Mainline post-merge verification | PARTIAL / RUNNING at handoff | Main SHA `009060cdf12908d27d399419952bdcb50828bfd6`; CI run [41129543349](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41129543349) and optional G2P run [41129543570](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41129543570) were still in progress. Pages deployment after PR #144 had succeeded in [41128531547](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41128531547). |
| Branch inventory | PARTIAL | 156 branch refs observed across two API pages. No mass deletion or force-rebase; preserve provenance and review unique commits before any destructive pruning. |
| Wheel packaging portability | TODO — verified structural risk | Runtime data loaders resolve repository-root `data/` via `Path(__file__).parents[2]`, while `pyproject.toml` does not declare/package these data files. Editable installs work; a regular wheel install may not find required registries. Acceptance: build a wheel, install into an isolated environment, run CLI/API smoke tests, and verify all required datasets are present without repository checkout. |
| Development tooling gate | TODO | No declared dev extra or lint/type-check gate. First inventory actual imports/style and select minimal tooling; do not add dependencies without an executable baseline. |
| Linguistic accuracy / release readiness | BLOCKED / evidence-limited | Independent expert-adjudicated Thai segmentation, IPA and Ukrainian target-form gold is still absent. Source-attested dictionary forms and parity tests are not accuracy gold. Manual browser/device and WCAG 2.2 AA review also remain outstanding. |

**Current main:** `009060cdf12908d27d399419952bdcb50828bfd6`.
**Working branch:** `chore/closeout-docs-and-debt-register-20261030` (maintenance/API contract follow-up).
**Public service:** https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/

---

## 2026-10-30 — current mainline closeout after PR #144

- PR #141 repository hygiene is integrated in main. The package version has one source of truth; TSV batch ingestion uses a tab delimiter; core CI, web-static and Pages action pins were upgraded.
- PR #144 forward-ported the bounded lexical work from historical PR #111 and was squash-merged as `cb7ff2a49731d3c02ddba400a4ddbc166395d493`.
- Exact PR #144 head `72a0e147fbbcd6d21fefc40a4219f9fb7c0bfc0b` has five successful check runs. The change adds source-attested `ทราม → ซาม` handling in Python/browser paths and ten enumerated cross-runtime regression cases; it does not add a productive `ทร → ซ` rule. Evidence grade remains SOURCE_ATTESTED_NOT_GOLD.
- Historical PR #111 is now closed as superseded. Its branch/history remains preserved.
- Post-merge main CI [41128531462](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41128531462) and Pages [41128531547](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41128531547) were still in progress at the last status read; Web Static [41128531495](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41128531495) passed.
- Branch inventory now totals 156 refs across two API pages. No destructive branch deletion or history rewriting was performed.
- Remaining engineering debt: optional external G2P/VISTEC workflow action pins are old; no declared development extra/linter/formatter/type-checker gate; stale historical branches need a reviewed retention/pruning policy.
- Evidence blockers: independent expert-adjudicated Thai segmentation, IPA and Ukrainian target-form gold remains unavailable. Automated parity and source-attested dictionary entries do not prove linguistic accuracy. Manual browser/device and WCAG 2.2 AA review remain outstanding.
- Classification: engineering-verified research prototype, not release-ready for linguistic-accuracy claims.

---

## 2026-10-30 — Thai lexical exception forward-port

- Historical PR #111 was 452 commits behind main; its bounded change was ported onto a fresh branch based on the latest main after PR #142, without force-rebasing or rewriting the historical ref.
- Added exact `ทราม → ซาม` handling in Python/browser maps, text lexicon and source registries, plus ten enumerated false-cluster/lexical regression cases through the typed IPA → Ukrainian adapter.
- No productive `ทร → ซ` rule was added. Generic ambiguity sentinels, including isolated `ทราย`, remain fail-closed.
- Evidence: Royal Institute Journal 36(4), 2011, p. 557 discusses `ทราม` among historical /s/-reading forms; English Wiktionary records `/saːm˧/`. Evidence is source-attested, not independent IPA gold.
- TDD red evidence: browser parity run `41124129117` and Python run `41124128896` failed on the expected missing lexical mapping/source-registry row before implementation. Exact-head full CI remains the acceptance gate.

## 2026-10-30 — PR #141 integrated; citation metadata follow-up

- PR [#141](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/141) was squash-merged into `main` as `4d087e66778854503a0e6d355d605d83a50354f8`.
- Exact-head PR checks passed: CI `41121318912` and Web Static Validation `41121319014`. Post-merge main CI `41122595309` and Web Static Validation `41122595149` completed successfully; Pages build/deploy and published-content verification `41122595375` completed successfully.
- The post-merge CI generated the master artifact and its assertions passed: 351,780 rows and 41 vowel records. The test job passed.
- Follow-up hygiene finding: `CITATION.cff` still identified the software as `0.5.1`, while `pyproject.toml` and the single package-version source declare `0.6.1`. A regression test was added first; CI on the test-only commit failed on this exact mismatch. The implementation now aligns the CFF version to `0.6.1` and removes the stale `date-released` field rather than inventing a release date.
- PR #142 merged into `main` as `81123ef50fbfc0335e22e6f16f4a5b02d967bb14`. Exact-head CI `41123979097` passed (212 Python tests and master-artifact job); post-merge main CI `41125905331` and Pages deployment `41125905186` passed. `CITATION.cff` now matches package version 0.6.1; no release date is asserted without evidence.
- Historical PR #111 is closed as superseded on its stale base, but its bounded `ทราม → ซาม` change is forward-ported in PR #144. Close #111 as superseded after #144 merges; retain its historical branch. No historical branch was deleted or force-rebased.
- Local checkout remains unavailable because the execution container cannot resolve `github.com`; verification is via GitHub Actions. Research/linguistic readiness remains limited by the absence of independent expert-adjudicated IPA and Ukrainian target gold.

---

## 2026-10-30 — repository hygiene and CLI contract

- **DONE_VERIFIED on branch `chore/repository-hygiene-20261030`:** package version drift is removed. `_version.py` is the single source used by setuptools metadata, the Python package and the HTTP server banner.
- **DONE_VERIFIED:** TSV input now uses a tab delimiter. The new regression test exercises an actual two-column TSV file; CSV behavior remains unchanged.
- **TDD:** test-only head `e770511cae4d2e0ddf85a66b3eb785cda1453c5b` failed in [CI 41118188899](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41118188899) on the two expected defects. Implementation head `9f488a983b77393c161afa0bfe01f0550d7c2cf3` passed [full CI 41118657251](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41118657251): 211 Python tests, browser tests/parity/UI contract, diagnostics and generated-artifact checks; master-artifact passed at 351,780 rows / 41 vowel records.
- **CI runtime maintenance:** upgraded core CI/web-static actions to v7 and Pages actions to current v6/v5 releases. Web static [41120184197](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41120184197) passed; PR-head CI [41120192415](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41120192415) completed both test and master-artifact jobs successfully. The test job passed 211 Python tests and no longer emitted the Node.js 20 deprecation warning. Pages deployment is not triggered from a feature branch; verify after merge. Optional G2P/VISTEC workflows retain old pins and are deferred because editing them triggers long external evaluation jobs.
- **Open cleanup PR:** [#141](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/141), verified implementation/workflow head `caab0adfd5b22fd07702e0aa0f86635aa46d5406`, based on main `37a2b5be62896a758ddc59b9b91184e448b4d963`; exact-head CI was queued after the final documentation checkpoint.
- **Main reconciliation:** PR #140 (documentation-only closeout for already merged UI work) was merged as `37a2b5be62896a758ddc59b9b91184e448b4d963`.
- **Branch inventory:** 151 refs are present. 44 are under `docs/`, 24 under `research/`, 22 under `feat/`, and 22 under `fix/`. PR #111 is closed as superseded, 12 ahead / 30 behind main and not mergeable. Its exact lexical evidence change was left untouched pending a clean rebase and renewed evidence/CI review. No historical branch was force-rebased or deleted.
- **Environment limitation:** local clone failed because the container could not resolve `github.com`; all test claims above refer to GitHub Actions, not local execution.
- **Readiness:** the code changes are engineering-verified, but the overall system remains a research prototype, not release-ready for claims of independently validated Thai IPA or Ukrainian target forms. Manual device/browser accessibility review also remains outstanding.

## 2026-10-30 — strictness scale and responsive layout merged; publication verified

- PR [#138](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/138) merged to `main` as `398a25e7f884f11bee85e0888026a6b2875bdf8f`. It introduced the three-position range control over the existing engine policies: 1/3 heuristic (`super-soft`), 2/3 structural (`soft`), 3/3 conservative (`strict`, default). Lower strictness increases coverage, not accuracy; the scale is not calibrated confidence.
- PR [#139](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/139) merged to `main` as `720b528e0f6560912d87750158c510fc746a3044`. It consolidated responsive CSS, preserved the scale, raised the slider and relevant controls to 44px minimum targets, added visible focus treatment, and updated asset cache keys.
- README, `docs/validation-matrix.md`, this audit and the execution handoff now describe the same three-level policy and current repository state.
- PR #139 exact-head CI passed on `8558efd9f7690938be629c3d659d6701f4597898`: test and master-artifact jobs passed in [41109778299](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41109778299) and [41109785725](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41109785725); Web static validation passed in [41109778408](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41109778408) and [41109786238](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41109786238).
- Post-merge main CI [41110504231](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41110504231) passed both `test` and `master-artifact`; master table assertions confirmed 351,780 rows and 41 vowel records. Web static validation [41110501009](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41110501009) passed.
- Pages run [41110501072](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41110501072) passed build, deploy and the published-content contract. The post-deployment gate fetched the versioned stylesheet and verified both `.strictness-scale` and the slider's 44px minimum target.
- No Thai parser, phonological rule, segmentation algorithm, IPA generation or Ukrainian adaptation behavior changed in PRs #138 or #139.
- Manual real-browser/device visual QA and WCAG 2.2 AA review have not been performed. Automated checks do not establish full visual quality or accessibility conformance.
- Independent expert-adjudicated Thai segmentation, IPA and Ukrainian target-form gold remain absent. Overall project remains a research prototype, not release-ready for linguistic-accuracy claims.
- PR #111 is closed as superseded and separate; it was not merged or modified as part of this UI work.

## 2026-10-30 — Thai service copy and methodology closeout

- Applied the editorial distinction established in the Korean service revision [2a16bae](https://github.com/ClippyFirst/Korean-Ukrainian-Phonetic-System/commit/2a16bae3bb6d4297225d358180adcefa0f301de8): homepage for ordinary users; methodology for researchers and developers.
- Homepage copy now leads with the user task, explains RTGS as a Latin reference, IPA as the phonetic representation, and Ukrainian output as the practical candidate; it explains strict/soft/super-soft trade-offs without implying that broader coverage improves accuracy.
- Methodology page title, navigation and introduction explicitly identify its audience and scope; existing technical details and evidence caveats remain intact.
- The Korean reference is a reviewed editorial revision, not a standalone formatter executable. No Thai-local formatter was invoked or claimed. Automated safeguards are the static validation and UI-contract tests.
- PR [#129](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/129) merged to `main` as `2bb0e264ed74e4d10c1a0c59ecf1d1990bcb9241`.
- **PASS:** exact PR-head full CI [41070939453](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41070939453): `test` and `master-artifact` both succeeded. Master artifact generation verified 351,780 rows and 41 vowel records. Web static validation [41070939558](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41070939558) succeeded.
- No runtime/linguistic behavior changed. No local tests are claimed.
- **PARTIAL — publication:** post-merge Pages deployment and live-content verification were not confirmed in this session.
- **BLOCKED / evidence-limited — linguistic readiness:** independent expert-adjudicated Thai segmentation, IPA and Ukrainian target-form gold remain absent. Repository remains a research prototype, not release-ready for accuracy claims.

## 2026-10-30 — copy-contract regression and correction

- The first CI run failed at the homepage copy assertion because `web/tests/ui-contract.test.mjs` still expected the old text `Можна вставити довший текст`.
- This was a stale test expectation caused by the deliberate user-facing rewrite; no production behavior failed. The assertion now checks `Можна вставити й ціле речення`.
- Web static validation run [41070448695](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41070448695) passed on head `49f7c4924ca851bfe2e7dfe46653cbd9965338ac`. Full CI run [41070448275](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41070448275) had not completed master-table generation at the last check. Full exact-head CI remains required.
- Status: PARTIAL; no merge or deployment.

## 2026-10-30 — separation of service copy and research methodology

- PR [#129](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/129), branch `docs/thai-user-copy-methodology-20261030`.
- The homepage was edited for ordinary users: plain-language task description, explanation of RTGS/IPA/Ukrainian output forms, and clearer descriptions of strict, soft and super-soft modes. The researcher page was explicitly framed as methodology for researchers/developers; its technical content and evidence caveats were retained.
- No engine, pronunciation, segmentation, IPA adaptation or RTGS behavior changed.
- A dedicated copy-corrector/formatter was not found in the tracked source tree or declared dependencies; no run of such a tool is claimed.
- Web static validation run [41070023201](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41070023201) passed on the initial PR head. Full CI run [41070023108](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41070023108) was still processing the generated master table; exact-head CI remains the acceptance gate. No local tests or live publication are claimed.
- Classification: PARTIAL pending full CI and PR review; the repository's wider linguistic-evidence limitations remain unchanged.

## 2026-10-28 — UX/UI refresh merged; published-contract follow-up

- PR #120 merged as `ad2f899978b66d3bbcb92124688b62261bb5225d`; branch exact-head CI and static validation passed. Post-merge CI's test job passed; generated master-artifact validation was still running when this entry was written.
- GitHub Pages deploy step completed for [run 40712965523](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40712965523), but the live-content contract failed because it expected the old privacy-copy phrase `Аналіз виконується локально у браузері`; the updated homepage correctly says `Текст аналізується локально у браузері`.
- Follow-up branch: `fix/pages-contract-and-ux-handoff-20261028`. It updates the live contract marker and replaces stale fixed-run references on the methodology page with stable workflow links.
- Status: PARTIAL until the follow-up branch passes checks and the next Pages deployment's published-content contract succeeds. Browser screenshot/manual device review remains unavailable in this connector-only run; no WCAG or linguistic-accuracy claim is made.


## 2026-10-28 — integrate IPA adaptation guidance into the primary workflow

- Removed the standalone homepage IPA → Ukrainian input panel because it duplicated the adapter already used by the Thai-text pipeline and implied a second core workflow.
- Kept the IPA adapter itself, Python/browser implementations, and adapter regression tests. The main flow still shows intermediate IPA, Ukrainian candidates, applied adaptation rules, and neutralized features.
- Added an explanatory method note describing IPA as the mandatory boundary, segment matching, aspirated-stop apostrophe policy, /h/ → «г», fail-closed unknown segments, and loss of tone/length/stress in practical Ukrainian spelling.
- Status: PARTIAL until exact-head CI and live Pages contract verify the updated UI. This is a UX/documentation correction, not a phonological algorithm change and not an accuracy claim.

## 2026-10-27 — direct IPA input and notation normalization

- Added a separate website IPA → Ukrainian panel for externally sourced Thai IPA. It calls the same `adaptIpaToUkrainian` adapter used by the Thai→IPA pipeline; no direct Thai-grapheme-to-Ukrainian path was added.
- Python and browser adapters normalize common presentation conventions: outer brackets/slashes, Thai tone letters, selected combining tone marks, stress, length, selected phonetic modifiers, and tied notation for the Thai alveolo-palatal affricate. Unknown segments and tone-only input are withheld.
- Regression coverage includes notation variants, direct UI adaptation, visible fail-closed behavior, and ambiguous combining breve U+0306 (which can mark extra-shortness and therefore must not be silently deleted).
- **DONE_VERIFIED at `ba3771e29b7554325c4b63cb3c39e2356e414066`:** CI [40559473200](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40559473200) and Web static validation [40559473259](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40559473259) passed. The newer conservative breve fix is **PENDING exact-head verification** at `ff27ebdcfb3c0d45bfc82943fbfd93b4f055708b` because the current GitHub Actions runs remain queued.
- **Not claimed:** successful parsing does not certify lexical IPA correctness or an official Ukrainian spelling. Independent IPA and Ukrainian-form adjudication remain open.

## 2026-10-27 source-attested lexical coverage continuation

- Added the source-attested three-syllable entry `ตะวันออก` → `ตะ|วัน|ออก`, pinned to en.wiktionary revision 86398986, which records standard IPA `/ta˨˩.wan˧.ʔɔːk̚˨˩/`. The implementation uses the existing Thai structural/phonological parser and IPA → Ukrainian adapter; it does not import external G2P output.
- Added Python/browser regressions for segmentation, IPA segments, tones and exact downstream candidate `таванок`; the source is recorded as CC BY-SA 4.0 and explicitly not independent expert/acoustic gold.
- This is a narrow lexical coverage improvement, not a general accuracy claim. The dedicated branch's latest CI and web static validation must pass before this entry is marked `DONE_VERIFIED`; independent Thai word-boundary/IPA adjudication and Ukrainian target-form review remain open.

---

## 2026-10-08 transliteration hardening

A second adversarial pass found a material false-cluster hazard that was not covered by the earlier generic cluster safeguards. Established Thai sequences **จร, สร, ศร, ซร** can contain a written ร that is not pronounced; lexical **ทร** is similarly reading-dependent. The parser now routes these constructions through the machine-readable special-orthography registry and returns **analysis-dependent:special-orthography** rather than fabricating an /r/ onset.

The pass also corrected a documentation/test boundary around **ไกล**: the /l/ is the second member of the true initial cluster /kl/, so the syllable has no coda and is /klaj/, with **ใกล้** differing by tone rather than coda structure.

Browser parity was strengthened with the same false-cluster and preposed-cluster probes, and browser tone-class selection now mirrors the Python reference for multi-consonant onsets.

Scientific status remains evidence-gated: lexical special-orthography resolution and Ukrainian practical preference still require a versioned gold corpus/adjudication layer.

# Final audit — current branch status

> **2026-10-03 branch override:** the historical release snapshots below describe earlier 40-rime / 343,200-row states. The current branch declares **41 rime records**, including reduced `-ว-` /uaː/, giving a **351,780-row** structural upper bound (44 × 41 × (1 + 38 coda options) × 5 tone-mark states). The current branch has passed the exhaustive generator and CI gates. Historical sections remain audit history, not current quantitative authority.

## 2026-10-03 full orthographic audit

### Closed by the same methodology used for `อ`

- `-อ` after a real onset is modeled as the /ɔː/ vowel construction.
- `-ือ` is modeled as the /ɯː/ construction with `อ` as a structural length carrier.
- reduced `-ว-` /uaː/ is modeled as a vowel component rather than an ordinary `ว` consonant.
- deterministic closed-syllable inherent /o/ is resolved when the supplied surface supports onset + coda analysis.
- preposed `ไ/ใ` preserves valid onset/leading-consonant structure, including `ไหม`, `ไหว้`, and `ไกล`.
- `ไ/ใ` is short in the vowel registry but live for tone calculation because it ends in /j/.
- Historical implementation note — this statement describes the earlier implementation and is superseded by the current IPA-first adapter contract documented in README.md: Ukrainian adaptation consumes the typed phonetic result/IPA boundary rather than independently re-parsing Thai graphemes.
- `ง` is represented as Ukrainian orthographic sequence `нг` in the structured adaptation layer and correspondence table.

### Still explicitly analysis-dependent

- `รร`
- `ฤ/ฤๅ`, `ฦ/ฦๅ`
- lexical/morphological `ทร`
- silent-letter constructions
- automatic multi-syllable lexical segmentation
- connected-speech phonetics
- empirical Ukrainian orthographic preference

### Verification gate

This branch must not be called CI-green until:
1. the complete test suite passes;
2. the exhaustive generator completes;
3. generated artifacts are synchronized;
4. the source/parser/derived manifest is regenerated and passes;
5. the 41-rime registry and 351,780-row structural bound are verified.

---

## Release

**v0.4.0 — research-ready phonetic-grahemic model with completed software layers.**

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
- vowel/rime records: 41;
- structural coda grapheme options: 38;
- tone-mark states: 5;
- open-syllable structural upper bound: 9,020;
- closed-syllable structural upper bound: 342,760;
- combined structural upper bound: 351,780.

These are **combinatorial upper bounds over declared records**, not counts of valid Thai syllables, lexical forms or corpus-attested forms.

## Reproducibility criterion

A clean checkout is release-ready when:

1. package installation succeeds;
2. derived artifacts regenerate without a diff;
3. the complete test suite passes;
4. schemas and documentation agree with the implementation;
5. no empirical claim exceeds the evidence actually processed.

The clean completion branch was verified by GitHub Actions run 213. The run regenerated derived artifacts cleanly, passed the source→parser→derived integrity gate, and completed **57 tests**, including the completion-layer special-orthography, lexicon-interface and Ukrainian-output probes. The documentation-only synchronization was separately verified by run 219 before the final merge into `main`. The resulting main merge HEAD is `075b009a07b129260f77d598503719bef0aee366`.

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
- a generated source→parser→derived manifest checks the 44 consonants, 41 vowel/rime records, parser vowel IDs, four tone marks/five tone states, 38 licensed coda graphemes and the 351,780 structural upper bound;
- CI now checks that the generated source-final manifest and existing derived artifacts remain synchronized.

### Initial-set vs final-set audit

The authoritative inputs remain the machine-readable Thai inventories. The final layer is now checked against those inputs rather than only documenting aggregate counts. In particular, the 41 source vowel/rime IDs must equal the IDs declared by the parser registry; the 44 consonant graphemes and 38 coda-capable graphemes are counted directly from the source table; and the structural syllable-space formula is independently asserted.

### What is still deliberately empirical, not merely architectural

The following cannot honestly be marked as empirically closed without gold data:

- corpus accuracy and lexical coverage;
- calibration of Ukrainian candidate probabilities;
- adjudicated Ukrainian orthographic preference;
- exhaustive connected-speech phonetics;
- universal lexical/morphological coverage of every Thai spelling.

These are now explicit **evidence gates**, not missing software interfaces.

## CI verification — current HEAD

The final release is tracked by the `main` branch; the clean completion content is CI-verified immediately before merge, and the audit intentionally does not embed a self-referential `main` SHA.
The final completion content was verified by GitHub Actions run **213** on the clean completion branch immediately before merge; generated artifacts were synchronized and the full test suite completed with **57 tests**.


## Adversarial audit extension — malformed syllable surfaces

The parser audit identified another false-positive class: a detector could select one vowel/rime pattern and silently ignore additional vowel signs, additional syllabic material, repeated tone marks, or unsupported symbols. The parser now requires the detected vowel/rime match to consume all vowel-sign material in the supplied syllable surface, rejects multiple tone marks, and rejects unsupported symbols instead of silently discarding them. Regression probes cover repeated vowel signs, concatenated syllable-like material such as `กาเก` and `กากา`, repeated tone marks, ASCII punctuation and Thai repetition mark `ๆ`. These cases are treated as unresolved input rather than assigned invented phonology.


## Adversarial audit extension — preposed-vowel leading clusters

The parser audit exposed a visual-order trap in syllables such as `ไหม` and `ไหว้`: the preposed vowel sign appears before the consonant sequence, so a simple character-index test can incorrectly demote the second onset consonant to coda. The parser now evaluates declared complex-onset licensing in preposed-vowel syllables before the generic coda fallback. The suite verifies `ไหม` as a ห นำ onset and `ไหว้` as a ห นำ onset with a tone mark. The model remains conservative for unsupported lexical leading constructions such as อ นำ.


## 2026-10-21 continuation — current-main reconciliation

### Source-of-truth and pipeline status

The current `main` snapshot inspected for this continuation is `d34fe54086d0295278b342d56804bcc5a409c37b` (2026-10-20). The current README defines the required pipeline as Thai orthography → structural analysis → syllable structure → Thai phonology → typed phonetic result (phonemic IPA + conservative broad surface IPA) → Ukrainian adaptation. It explicitly states that the Python Ukrainian adapter consumes the typed result and does not inspect Thai graphemes, vowel IDs, or Thai coda fields. The browser implementation imports its dedicated IPA-to-Ukrainian adapter. Accordingly, older audit wording that described direct structured-Thai-to-Ukrainian rendering is historical, not the current architecture.

### Current verification evidence

- The latest-main commit lookup returned no associated workflow runs and its combined-status endpoint returned no status checks. This is **not evidence of a passing CI run** for the inspected main HEAD.
- PR #17 (`polish/v0.5.1-research-service`, head `80680c57418574566f1b651800ec618c4681212b`) has successful workflow runs 627 (CI) and 161 (web static validation). Its CI run completed Python package installation, derived-artifact generation/drift checks, master-table generation, Python unittest discovery, and the 351,780-row / 41-rime artifact assertions. Its web run completed JavaScript syntax, required-page, static accessibility-contract, and no-remote-runtime-dependency checks.
- PR #17 is nevertheless divergent and 119 commits behind current `main`; its passing checks apply to its own old head only. Do not merge it wholesale. Reuse only changes proven absent from current `main`, after a fresh comparison and verification.
- Recent main commits add a pinned external G2P candidate-runner procedure and harden its evaluation harness, including rejection of empty challenge corpora, all-candidates-failed smoke runs, and raw IPA equality being misreported as accuracy. These are benchmark-infrastructure safeguards, not evidence of empirical accuracy by themselves.

### Acceptance ledger

| Workstream | Status | Evidence / acceptance criterion |
|---|---|---|
| IPA-first adapter boundary | PARTIAL — implementation documented; current-main executable suite not independently rerun in this session | README contract and browser adapter import support the intended boundary. Accept only after current-main CI passes and Python/browser parity remains green. |
| Structural generation and registry consistency | PARTIAL — prior branch verified, current HEAD not verified | PR #17 CI asserted 41 rime records and 351,780 structural rows; require a successful run on the current main commit or its exact successor. Structural rows are not a valid-syllable or lexical-coverage count. |
| Web polish in PR #17 | PARTIAL — stale divergent branch | Compare its nine commits with current main; retain only changes not already present and re-run web checks. No merge performed. |
| External G2P benchmark harness | PARTIAL — infrastructure present | Challenge input must be non-empty, package versions and raw outputs recorded, and scoring limited to independently adjudicated gold IPA. A successful smoke run is not corpus accuracy. |
| Licensed/adjudicated Thai IPA gold corpus | BLOCKED — corpus/evidence not established in this session | Record source, version, access date, license/redistribution terms, preprocessing and independent adjudication; then run stratified segmentation, segment, vowel-length, tone and IPA evaluation. |
| Empirical Ukrainian target preference/calibration | BLOCKED — no adjudicated target corpus | Build and license an adjudicated Ukrainian candidate/target set before reporting preference, calibration, or accuracy. |
| Local clean-install/test reproduction | BLOCKED — checkout/network unavailable | Clone the exact main SHA in a network-enabled environment; run the workflow commands and generated-artifact drift checks, then attach exact logs/results. |

### Historical audit snapshot — superseded by the 2026-10-24 continuation

The following command log records an earlier continuation and should not be read as the current merge status.

### Commands and operations executed in that earlier snapshot

- GitHub API: inspect current commit history, compare `main` with PR #17, inspect the PR patch and changed-file summary, fetch README / pyproject / audit / research-protocol / corpus-validation / browser parity test / benchmark runner, and inspect available workflow runs and combined status.
- `git clone --depth 1 https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System.git /tmp/thai-ua-audit` — BLOCKED: DNS/network error (`Could not resolve host: github.com`); no local test, generator, build, or corpus evaluation was run.
- No PR was merged, no external settings were changed, and no empirical accuracy claim was added.

### Release assessment

**Research infrastructure: substantial; release readiness: not independently verified for current main; empirical accuracy: unmeasured.** The next decisive acceptance gate is a successful workflow run on the exact current-main commit (or its exact successor), followed by independent gold-corpus evaluation.

### Current external IPA and benchmark audit — 2026-10-24

- The fail-closed unknown-token fix is merged and has passed subsequent main-equivalent CI/master-artifact checks.
- `thaiphon 0.7.0` and FastThaiG2P 0.1.0 have reproducible optional smoke evidence (36 inputs each; 72 raw outputs total; 0 runtime errors). Exact inter-engine agreement is 13/36; tone-letter-stripped diagnostic agreement is 14/36. Neither is accuracy.
- The three source-attested Thai spot-checks are pinned to exact Wiktionary revisions, but are selected diagnostics, not independently expert-adjudicated gold. Upstream source overlap is plausible.
- The durable report/registry and comparator provenance update is PR #41, which remains subject to current-head CI and smoke verification. Independent gold count is still 0; accuracy remains null.
- Release status: research infrastructure verified; phonological accuracy and full release readiness remain unverified pending independent held-out gold and source-specific adjudication.


## Current acceptance snapshot — 2026-10-25

The latest code-bearing checkpoint is `b1f67a881d17a356f73712877dd71f4287b5bba3`; exact-head CI run [40229701920](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40229701920) passed the test job: generated-data drift, master-table generation, 143 Python tests, the 36-input runtime diagnostic, 27 Python/browser parity fixtures, and all three Node adapter/parity/UI checks. The separate artifact-publication job was still running at the time of the handoff; an equivalent predecessor run [40229604077](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40229604077) successfully asserted 351,780 structural rows / 41 vowel-rime records and uploaded the artifact.

The segmentation evaluator now refuses to score prediction rows unless `status=ok`, treats error/abstention/partial outputs as abstentions, and correctly reports zero F1 when reference boundaries exist but no true positives do. The runtime diagnostic refuses an empty challenge set. These are software-quality fixes, not Thai accuracy evidence.

The 36-form challenge diagnostic yields 23 lexicon lookups, 13 unresolved inputs, 21 complete engine outputs and 15 abstentions/incomplete outputs. Independent adjudicated IPA and word-boundary gold remain absent; no empirical accuracy is published. Unknown words and analysis-dependent special orthography remain fail-closed.

**Readiness:** research infrastructure is CI-verified; linguistic accuracy, representative lexical coverage, connected speech and Ukrainian target preference remain unvalidated. This supersedes earlier historical release snapshots in this audit file.


## 2026-10-25 — source-backed evidence and segmentation baseline

- Added five challenge lexicon entries (`ไกล`, `ใกล้`, `เดิน`, `กรรม`, `บรรจุ`) with per-entry revision-pinned Thai Wiktionary locators and explicit CC BY-SA 4.0 attribution/share-alike notes. This is source-attested coverage, not a representative vocabulary claim.
- Added the 993-record Wisesight word-tokenization annotation file from upstream commit `c1d063649abc3a6870b5fd1aae26cd1c64bdde7b`, blob SHA-1 `279aeb2d4323fd8032306160144d33dcb5b2df84`, CC0-1.0. Converted records preserve exact text reconstruction and are labeled `SOURCE_ANNOTATED`, not expert-adjudicated.
- Hardened the segmentation evaluator to distinguish `ADJUDICATED` from `SOURCE_ANNOTATED`, reject mixed evidence grades in one report, preserve all gold rows in denominators, and exclude boundaries touching whitespace-only tokens from lexical boundary metrics.
- Added six pinned dictionary IPA/tone/vowel-length records, including the source-attested short-vowel `เงิน /ŋɤn˧/` vs long-vowel `เดิน /dɤːn˧/` contrast. They are explicitly not gold and are not scored as accuracy.
- Added CI tests for source-file reconstruction, evidence-grade isolation, whitespace semantics, lexicon source records, and the Wisesight baseline report.
- At code-bearing commit `818a378d37b248d74628243b9a8d62fb82029815`, exact-head GitHub Actions run [40233825012](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40233825012) passed the new Python tests, dataset checks, diagnostics, generated-data drift check, browser parity and master-artifact gates. The documentation-only reconciliation commit is being prepared separately and still requires its own CI confirmation.

### Still open after this batch

- Independent expert/acoustic IPA and tone/length gold: CCOST v1.0 remains a candidate; license/manual review and independent Thai phonetic adjudication are still required.
- Typed lexical pronunciation override for `เงิน`: source evidence exists, but the runtime adapter cannot yet safely pass this lexical short-vowel reading as a provenance-bearing typed IPA result.
- Automatic segmentation: this batch establishes a source-annotated held-out baseline, but it does not implement an automatic segmenter. The baseline report must make that limitation visible.
- Context-dependent `รร`, `ฤ/ฤๅ`, `ฦ/ฦๅ`, `ทร`, silent letters, connected speech and Ukrainian preference remain evidence-gated.


## Verified outcome — run 40233825012

**Code-bearing commit:** `818a378d37b248d74628243b9a8d62fb82029815` on `research/thai-segmentation-gold-parity-verified-20261025`.

- Both CI jobs passed: `test` and `master-artifact`.
- 150 Python tests passed; generated data regeneration/drift check passed; master artifact guard passed for 351,780 structural rows and 41 vowel/rime records; Node IPA→UA, parity and UI contract tests passed.
- Runtime challenge diagnostics: 36 forms; lexicon segmentation 28, unresolved 8; complete engine output 25, abstained/incomplete 11. Syllable analysis statuses: 35 analyzed, 3 special-orthography-dependent, 1 vowel-length-dependent; these are syllable-level counts and therefore do not sum to the 36 input forms. These are runtime diagnostics, not accuracy.
- Wisesight: 993/993 source-annotated records; 993 predictions; boundary precision 0.638319, recall 0.091858, F1 0.160604; exact sequence rate 0.031219. Gold status is `SOURCE_ANNOTATED`; zero rows are expert-adjudicated. Artifact [wisesight1000-segmentation-baseline](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40233825012) uploaded as artifact ID `12614106636`.
- The initial CI run on the expanded lexicon exposed a stale test fixture that expected `ไกล` to remain unresolved. The fixture was corrected to use unsupported `กฉ`; the final code-bearing run above passed.

**Readiness:** engineering-verified research prototype with a usable source-annotated segmentation benchmark; not release-ready for arbitrary Thai text and not empirically validated for phonetic accuracy. Independent IPA/tone/length adjudication, lexical override for `เงิน`, and context-dependent special orthography remain open.


## Text-only continuation audit — 2026-10-25

### Verified implementation state

- Added a typed, pinned lexical IPA override for `เงิน` from Thai Wiktionary revision 5759179. It preserves segmental IPA `ŋɤn`, mid tone, short-vowel metadata, source ID, revision, URL, license, and an explicit `SOURCE_ATTESTED_NOT_GOLD` status.
- Routed the override through the Python text pipeline and the browser text pipeline. Both adapters continue to produce Ukrainian output from typed IPA, not directly from Thai graphemes.
- Added a six-record source-attested IPA discrepancy/abstention diagnostic, including segmental comparison, tone-category comparison, and engine vowel-length metadata. It does not claim accuracy.
- Added a corpus-source register for Wisesight, LST20, VISTEC-TP-TH-2021, and CCOST, recording which sources are usable, candidates only, or blocked by license/access.
- Updated source registry and license notes; Wisesight remains a held-out source-annotated baseline and is not used for training.

### Evidence and limitations

- On fully successful code/data checkpoint `59890a0bfcf7b84d19408310f690d41244a482d1`, GitHub Actions run [40237347247](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40237347247) passed 158 Python tests, generated-data drift checks, existing Node IPA/UA and UI/parity tests, the Wisesight diagnostic, and the six-record IPA diagnostic. The master artifact guard checks 351,780 structural rows and 41 vowel/rime records.
- The challenge diagnostic on that checkpoint: 36 inputs; 28 ordinary lexicon resolutions + 1 lexical IPA override; 7 unresolved; 26 complete outputs; 10 abstentions/incomplete. This is not an accuracy benchmark.
- The six-record IPA diagnostic: 5 complete engine outputs; 4 segmental agreements; 5 tone-category agreements; one withheld/incomplete output. The `บรรจุ` discrepancy (source includes final `/ʔ/`, engine segmental output omits it) is intentionally not auto-corrected: source transcription level and stress-conditioned realization need review.
- The browser parity code head `43687b2753379b1d617b1c925f87358f8aad13bd` passed [CI 40238202167](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40238202167) and [Web static validation 40238202181](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40238202181). The final documentation-only head `6a153e26e17c4929fdc166b3dbeb73444668f2b1` also passed [CI 40238672074](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40238672074) and [Web static validation 40238671983](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40238671983). Earlier browser failures were stale fixture expectation/order issues, corrected before the passing head.
- Automatic word segmentation remains TODO. The 993-row Wisesight set is test-only; LST20 and VISTEC remain candidates pending license/annotation review. CCOST is CC BY-NC-SA 4.0 and its TextGrid annotations are in a 6.2 GB archive; it is not bundled.
- Independent IPA/tone/length gold, acoustic validation, connected-speech validation, and independently adjudicated Ukrainian target forms remain blocked by evidence/permission/expert-review requirements.

### Readiness

**Research-ready engineering prototype; not release-ready.** The browser parity head and final documentation head have passed CI and Web static validation. The repository still lacks independent phonetic gold, a production automatic segmenter, acoustic validation, and independently adjudicated Ukrainian target forms.

## 2026-10-26 continuation — segmentation training and adjudication gates

### Implemented in this batch; exact-head CI pending

- Added a research-only unigram-frequency Viterbi segmenter trainer in `scripts/train_tud_word_segmenter.py`. It downloads three source-pinned UD Thai TUD files from upstream commit `67413969add552b7030184f16f24fa9f630913bc`, verifies Git blob SHA-1, pools the snapshots, and creates deterministic source-document-disjoint 80/10/10 train/dev/test splits. The token penalty is selected on dev only; the test split is never used for tuning.
- Wisesight's 993 CC0-1.0 rows remain external test-only data and are not used in training or tuning. The CI uploads the trained model and report as artifacts. This model is a research experiment, not the production default; exact-head CI and the actual held-out metrics must be reviewed before claims of quality.
- Activated a source-pinned exact lexical IPA override for `เดิน` (/dɤːn˧/, Thai Wiktionary oldid 1908803) through the typed IPA→Ukrainian adapter in both Python and browser code. The grapheme-only parser's ambiguity remains unchanged. Because this override uses the same source being compared, the source-attested IPA diagnostic now excludes this row from agreement counts as circular rather than claiming independent agreement.
- Added independent IPA and Ukrainian target-form adjudication templates plus a protocol. All expert-label fields are blank; no human adjudication or audio access is claimed.

### Task ledger

| ID | Status | Current result | Acceptance criterion / blocker |
|---|---|---|---|
| SEG-TRAIN-001 | PARTIAL | TUD-trained frequency-Viterbi experiment; source-pinned, source-document-disjoint split; held-out TUD and Wisesight diagnostics configured in CI | Exact-head CI must pass and metrics must be reviewed; production integration requires acceptable held-out results and share-alike attribution |
| IPA-GOLD-001 | BLOCKED | Adjudication template and protocol prepared; CCOST audio/TextGrid not accessed | Independent Thai phonetician, authorized recording/annotation access, agreed broad-vs-surface target, dual labels and disagreement log |
| WALK-LEX-001 | PARTIAL | `เดิน` resolves through exact source-attested lexical IPA; source override excluded from independent agreement scoring | Exact-head Python/browser CI; remains source-attested, not IPA gold |
| BANCHU-IPA-001 | PARTIAL / EVIDENCE-LIMITED | `บรรจุ` final /ʔ/ mismatch retained; no universal rule added | Agree on transcription level, stress/context, and independent phonetic adjudication |
| UA-TARGET-001 | BLOCKED | Six-row Ukrainian target-form template and blinded-review protocol prepared | Two independent Ukrainian-native reviews, predefined criteria, retained disagreements and adjudicated forms |

No release or merge is performed by this continuation. The project remains an engineering-verified research prototype, not release-ready for arbitrary Thai text. The exact-head workflow is the authority for the current branch; prior CI success does not imply these new changes passed.



## Exact-head continuation update — 2026-10-26

- PR #71 latest observed CI run `40286374324` failed in `python -m unittest discover -s tests -v` (174 tests ran; 4 failures). Generated-data drift and master-table generation passed before the test step; downstream browser, segmentation diagnostics, TUD training and artifact jobs were skipped by fail-fast sequencing. Web static validation run `40286374333` passed for the then-current PR head, but does not substitute for the Python/segmentation workflow.
- Root cause: a source-pinned lexical IPA override for `เดิน` had been activated, but four older tests still asserted the pre-override state (only `เงิน` active; `เดิน` unresolved in the public analyzer; and `เดิน` classified as ordinary lexicon segmentation). The parser-only structural ambiguity assertions remain valid and must remain separate from the lexical override path.
- Updated tests on the continuation branch to assert both source-pinned overrides, verify `เดิน` metadata (`/dɤːn˧/`, long vowel, mid tone, Wiktionary oldid `1908803`, CC BY-SA 4.0, not gold), preserve parser-layer ambiguity, and expect the text pipeline status `lexical_ipa_override` for `เดิน`. Commits: `8369edd141ad83c451b0395a57ba25f7a1c57006`, `2337dcf69ff6d59cde1862d486f50031fe9a815e`, `4964d3970c6f14cedd07f04138b99b95c57ef506`, `4656a557a74405f64455219e1a6fece6be575915`.
- Latest code commit is `4656a557a74405f64455219e1a6fece6be575915`. Exact-head CI is not yet observed; do not mark this correction as verified until the new workflow run finishes. No local execution is claimed through the GitHub connector.
- Remaining blockers: independent IPA/acoustic adjudication, independent Ukrainian target-form adjudication, and review of `บรรจุ` final `/ʔ/`; TUD-trained segmenter evaluation and all post-failure CI gates must run on the latest head. Wisesight remains source-annotated test-only and is not training/tuning data.


## Exact-head continuation update — 2026-10-26 (code/data commit `4c3d01d9b726b410c98048878441082d8d5c8299`)

- **CI PASS:** [run 40296520186](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40296520186). The 176-test Python suite, generated-data clean-tree check, 351,780-row master-table generation, 36-input runtime diagnostic, Node IPA→Ukrainian tests, Python/browser parity and UI contract checks, both Wisesight diagnostics, candidate-registry `--check`, source-attested IPA diagnostic, TUD research training/evaluation and all artifact uploads passed.
- **Web static validation PASS:** [run 40296520175](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40296520175). Candidate registry TSV quoting drift was corrected in `7879fbe37f73754359a5b354284be713d45331e6`; the generator now prints a unified diff on drift (`cedb4319c9a821b83d20fd0fd1239c299957f68d`). A second stale CI assertion was corrected in `4c3d01d9b726b410c98048878441082d8d5c8299` to expect two circular source overrides and four independently comparable records, with consistency assertions against the report rows.
- **Runtime challenge diagnostic (not accuracy):** 36 inputs; 27 complete outputs; 9 abstentions/incomplete; 2 lexical IPA overrides; 7 unresolved segmentation cases. The diagnostic explicitly does not claim accuracy.
- **Wisesight-1000 (993 source-annotated rows, zero expert-adjudicated rows):** text-tokenizer baseline boundary F1 `0.160604`, precision `0.638319`, recall `0.091858`, exact-sequence rate `0.031219`; dictionary max-match boundary F1 `0.839471`, precision `0.822287`, recall `0.857390`, exact-sequence rate `0.193353`. These are descriptive source-annotation comparisons, not independent gold accuracy. Wisesight was not used to train or tune the TUD model.
- **TUD research segmenter:** pinned source commit `67413969add552b7030184f16f24fa9f630913bc`, CC BY-SA 4.0; 3,041 training sentences and 5,319-word vocabulary. Dev: 1,142 groups, boundary F1 `0.889023`, exact-group rate `0.327496`. Held-out TUD test: 375 groups, boundary F1 `0.872932`, exact-group rate `0.432000`. Wisesight test-only: 2,848 filtered groups, boundary F1 `0.792101`, exact-group rate `0.385183`. These scores apply only to contiguous Thai-only runs with at least two tokens; TUD inherits treebank tokenization and the model remains research-only, not the production default.
- **Source-attested IPA (six rows, not gold):** 3 segmental agreements, 4 tone agreements, 2 circular override rows excluded, 4 independently comparable rows; no accuracy claim. The `บรรจุ` final `/ʔ/` discrepancy remains unresolved; no global rule was introduced.
- **Still BLOCKED / PARTIAL:** independent IPA/acoustic gold needs qualified Thai phonetic adjudication and authorized audio/TextGrid access; Ukrainian target forms need independent Ukrainian-native adjudication; `บรรจุ` needs agreed transcription-level/context review. TUD segmenter remains PARTIAL pending independent quality review and a decision about integration. Repository remains a research prototype, not release-ready.
- Documentation follow-up commits will trigger their own workflows; verify the final documentation head before calling the whole continuation complete.


## TUD segmenter quality decision — 2026-10-26

**Decision: do not integrate the TUD unigram-Viterbi segmenter as the production default.** The model remains a reproducible research experiment. On filtered held-out TUD groups, boundary recall is 0.9775 but precision is 0.7886 and exact-group rate is 0.432. On filtered source-annotated Wisesight test-only groups, recall is 0.9921 but precision is 0.6592 and exact-group rate is 0.3852. Boundary F1 drops by 0.080831 between these evaluations. This pattern is consistent with a recall-heavy predictor that still makes many boundary/sequence errors and has weaker cross-domain precision; it does not establish independent accuracy because TUD inherits source tokenization and Wisesight is not expert-adjudicated.

The next acceptance gate is a documented false-split/false-merge review, explicit deployment thresholds, and an independent untouched-domain evaluation. Keep CC BY-SA 4.0 attribution/share-alike obligations. Do not change the production default on the strength of these metrics alone.

## Exact final documentation-head verification — 2026-10-26

- Branch: `research/thai-segmentation-gold-parity-verified-20261025`; final documentation head before this follow-up: `cb8832ca99e4ccce53b6fb2b6988b5945acaad71`.
- CI [40297155713](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40297155713) passed both `test` and `master-artifact` jobs. Web static validation [40297155831](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40297155831) passed.
- The code/data head `4c3d01d9b726b410c98048878441082d8d5c8299` remains the exact head with the 176-Python-test full engineering run [40296520186](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40296520186); the docs-only head check independently verifies generated master artifact and repository test workflow after documentation synchronization.
- Remaining evidence gates: independent IPA/acoustic gold with authorized recordings/TextGrid, independently adjudicated Ukrainian target forms, and context/transcription-level adjudication of `บรรจุ` final `/ʔ/`. Research prototype; not release-ready.


## Exact-head special-orthography and IPA-boundary repair — 2026-10-26

- Starting default-branch commit: `0be5fd841070e337cb5c805ef92954938abe61bb`; verified code head: `cb775d6156f62392fa2d0f4bcf8d1aa30d219530` on `research/thai-segmentation-gold-parity-verified-20261025`.
- Earlier CI [40313439910](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40313439910) reported 12 failures. Root cause was four malformed rows in `data/thai/special_orthography.csv` missing the `pattern` field, which shifted CSV columns. Corrected in `a0bd6f598c5117154db1c78f02ae25b6d6fbf1bc`; added column/schema assertions in `1282dad1d8703cc4cb0d321206a1d3406a4f2533`.
- Added Python typed-IPA mutation/fail-closed test (`5720ef2a23f49bb85286bfa0d6366d88473c3031)), browser end-to-end IPA-mutation test (`85448d632aa503b537803993fbe3d8335cc9f150)), and metadata/uncertainty preservation assertions (`cb775d6156f62392fa2d0f4bcf8d1aa30d219530`). The adapter consumes typed IPA, and unsupported/absent/uncertain IPA withholds Ukrainian output.
- Exact-head CI [40315032771](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40315032771) passed `test` and `master-artifact`: 180 Python tests, generated-data drift, 351,780-row / 41-rime master artifact, Node IPA→Ukrainian, 28 parity fixtures, UI contract, challenge/Wisesight/source-attested IPA diagnostics, target-candidate check, TUD training/evaluation and artifact uploads. Web static validation [40315032788](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40315032788) passed.
- Special-letter readings remain context/lexical dependent. The official teaching PDF supports orthographic scope, not universal word-level IPA; independent Thai phonetic/acoustic gold and Ukrainian target-form adjudication remain blocked. `บรรจุ` final `/ʔ/` remains evidence-limited. Readiness remains a research prototype, not release-ready.


## Current execution checkpoint — 2026-10-26 (comparative segmentation review)

- Previous verified code checkpoint: `4b1592cd72298d1ca92e0b99ab330975764a078a`; full CI [40320450844](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40320450844) and Web static validation [40320450587](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40320450587) passed.
- Added same-row comparative error triage for the dictionary max-match and TUD Viterbi segmenters in `scripts/compare_segmentation_error_review.py`, tests in `tests/test_comparative_segmentation_error_review.py`, and a dedicated CI artifact. Both engines are scored on the same 993 pinned CC0-1.0 Wisesight source-annotated rows; the report includes boundary context and lossless mixed-text handling. This is not independent adjudication.
- Code/workflow checkpoint `b6dbec7928b106f0ab52e06af33a26635df75412` has CI run [40322960615](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40322960615) in progress and Web static validation [40322959844](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40322959844) passed. The current documentation HEAD is newer; verify its own exact-head checks before claiming the repository head is fully green.
- Preliminary inspection of the already-generated dictionary report suggests review strata including numeric/punctuation tokenization, Latin/URL/brand spans, and token granularity for longer Thai sequences. These are non-expert hypotheses for sampling, not adjudicated error categories. Do not patch tokenization to match these labels without source/protocol review.
- Release status remains **not release-ready**. Zero independent Thai IPA/acoustic gold rows and zero independently adjudicated Ukrainian target forms remain. Production segmentation still requires human review, explicit thresholds and an independent licensed domain. The `บรรจุ` final `/ʔ/` case remains context/transcription-level evidence-limited.


## Verified comparative segmentation results and PR reconciliation — 2026-10-26

- Same-row comparative report passed CI and was uploaded in [run 40322960615](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40322960615); Web static validation [40322959844](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40322959844) passed. Artifact `thai-segmentation-comparative-error-review`, ID `12649094231`, SHA-256 `8005cc91939ea06b852c1717fee9fb72d370709e74267b8f99636a6476d30775`.
- Full-text comparison on the same 993 pinned Wisesight rows: dictionary max-match precision 0.822287, recall 0.857390, F1 0.839471, false splits 2,574, false merges 1,981, exact sequences 192/993 (19.34%); TUD Viterbi precision 0.608000, recall 0.973868, F1 0.748623, false splits 8,722, false merges 363, exact sequences 119/993 (11.98%). This same-row full-text protocol preserves non-Thai runs and differs from the earlier TUD filtered Thai-only-span diagnostic.
- Decision: **do not integrate the TUD segmenter as production default**. On this full-text evaluation it is highly recall-heavy and produces substantially more false splits, with lower F1 and exact-sequence rate than the dictionary baseline. This is a research comparison against source annotations, not independently adjudicated linguistic accuracy.
- PR [#68](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/68) is closed as superseded after confirming its eight changed paths contain no unique files and its OBEC special-orthography evidence/tests are represented in PR #71. A supersession comment is recorded; the source branch was preserved. PR [#71](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/71) remains open Draft.
- Full CI and Web static validation passed on documentation checkpoint `e4ab3fd46e9c48c4220afb1f73ae5c6127b328ff` (runs [40323209539](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40323209539) and [40323209471](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40323209471)). The later audit/matrix/handoff commits must themselves pass exact-head checks; until then, cite `e4ab3fd` as the last verified documentation checkpoint, not as the latest branch HEAD.


## Human-review sample generator and exact-head verification — 2026-10-26

- Added `scripts/build_segmentation_manual_review.py` and `tests/test_segmentation_manual_review.py`. The generator joins real comparative-report error examples to full source rows in the pinned 993-row Wisesight TSV, keeps only IDs for which both systems have a recorded prediction, verifies exact source reconstruction for gold and both predictions, and emits full text, gold/dictionary/TUD token arrays, triage provenance, sampling strata, and blank reviewer decision fields.
- Sampling strata (numeric/date, URL/email, mixed Latin–Thai, Latin/brand, punctuation/quoting, long Thai, and engine disagreement) are explicitly heuristic candidate labels only. Every row stays `SOURCE_ANNOTATED`, `adjudicated=NO`; no error is automatically called linguistically wrong.
- CI now builds and validates the manual-review TSV and uploads it with the comparative JSON artifact. Acceptance requires both model predictions, exact lossless reconstruction, non-empty sample, and empty human decision fields.
- Comparative artifact independently downloaded and inspected: artifact ID `12649094231`, run `40322960615`, head `b6dbec7928b106f0ab52e06af33a26635df75412`; ZIP size 83,500 bytes; SHA-256 `8005cc91939ea06b852c1717fee9fb72d370709e74267b8f99636a6476d30775`. JSON has 993 source-annotated rows, 0 expert-adjudicated rows, same rows and boundary policy for both engines, Unicode-code-point offsets, and lossless mixed-text policy.
- Exact metrics from the artifact: dictionary P=0.822287, R=0.857390, F1=0.839471, 2,574 false splits, 1,981 false merges, 192/993 exact sequences; TUD P=0.608000, R=0.973868, F1=0.748623, 8,722 false splits, 363 false merges, 119/993 exact sequences. TUD remains research-only; these source-annotation comparisons are not expert gold.
- Latest pre-review-sampler exact-head CI for `4115326490bc8189660838f51bfe47a382ada203`: run `40324015433` passed both `test` and `master-artifact`; Web static validation `40324015445` passed. The review-sampler code/workflow changes are newer and require their own exact-head CI and static validation before being marked verified.
- External gates remain: independent Thai IPA/acoustic gold, two independent Ukrainian target-form reviewers, context-specific `บรรจุ` final /ʔ/ adjudication, another licensed evaluation domain, and full official OBEC PDF review (direct PDF access previously returned HTTP 403; only scoped claims from accessible evidence are made). No release-readiness claim is made.


## Current continuation — 2026-10-26: stratified review packet and source re-check

- Starting default-branch SHA: `0be5fd841070e337cb5c805ef92954938abe61bb`. Work branch: `research/thai-segmentation-gold-parity-verified-20261025`. PR #71 remains open Draft; PR #68 is closed unmerged as superseded, and its branch is preserved.
- Implemented a stronger manual segmentation-review packet. The generator now computes dictionary and TUD predictions for all pinned source rows, verifies exact reconstruction for each prediction, and deterministically selects a stratified set plus uniform controls. The sample is not restricted to top-ranked model/source disagreements. The CI guard checks for control rows and blank human adjudication fields.
- Added regression tests for deterministic sampling, controls, source provenance, reconstruction, wrong-model provenance and fail-closed behavior. These tests are authored but are **not yet claimed as passed** until the exact-head CI run completes.
- External source check: Zenodo CCOST v1.0 DOI 10.5281/zenodo.17366698 explicitly records CC BY-NC-SA 4.0 and lists audio/TextGrid archive plus annotation manual. The ACL Anthology paper record describes manual correction by trained native Thai phoneticians. This makes CCOST a viable candidate for licensed non-commercial adjudication, but this project has not downloaded or reviewed the full archive/manual and has not produced expert gold. Source: https://zenodo.org/records/17366698 and https://aclanthology.org/2026.lrec-1.247/.
- The official Royal Institute dictionary site is reachable at https://dictionary.orst.go.th/. The cited OBEC PDF https://academic.obec.go.th/images/document/1649040986_d_1.pdf still returns HTTP 403; full-document inspection remains blocked. Existing claims must remain limited to page-scoped evidence already accessible.
- `บรรจุ` has a pinned Thai Wiktionary source record whose IPA is `/ban˧.t͡ɕuʔ˨˩/`; this confirms what that dictionary records, not a universal rule for all contexts. The current one-syllable lexical-override schema cannot safely encode this multisyllabic word as a single record, so no lossy override was added. Adjudication must define broad phonemic vs surface transcription and stress/context first.
- **Current readiness:** engineering-oriented research prototype, not release-ready. Independent Thai IPA/acoustic adjudication, two independent Ukrainian-native target judgments, human review of the segmentation packet, a separately licensed evaluation domain and full OBEC source inspection remain open.


## VISTEC external-domain evaluation added — 2026-10-26 (run pending)

- Verified the dataset-specific upstream README at immutable commit 215a7dc3d384f20eb56af1cbc41fb32b7f8df57c. It describes 49,997 manually annotated Thai social-media samples, identifies word-segmentation markup in submissionText, and declares CC-BY-SA 3.0. CSV Git blob SHA-1: edfcb85907a604c5e30643065ac4975862a0fe90. The third-party CSV is not bundled.
- Added scripts/evaluate_vistec_segmentation.py and tests/test_vistec_segmentation_adapter.py. The adapter strips only documented <ne>/<msp> markup, converts pipe-delimited tokenization to the existing scorer's schema, checks exact reconstruction, and compares dictionary max-match with the research-only TUD model. It explicitly evaluates annotated submissionText rather than raw questionText.
- Optimized scripts/evaluate_segmentation.py by indexing gold IDs/text once, avoiding repeated linear scans for every prediction; this is required for 50,000 CSV rows and two engine predictions per row.
- Added .github/workflows/vistec-segmentation-evaluation.yml. It checks out the pinned external commit, verifies the CSV Git blob hash and license declaration, trains the pinned TUD research model, evaluates both systems, and uploads only the report artifact.
- **Verification state:** implementation and tests are authored; no VISTEC metric is claimed until the external workflow succeeds and the artifact is inspected. This is a separate source-annotation domain, not independent expert re-adjudication.
- Source metadata is recorded in data/corpus_sources.csv, docs/evidence.md, docs/corpus-validation.md and README.md. Release readiness remains blocked by exact-head CI, independent Thai IPA/acoustic adjudication, independent Ukrainian target judgments, human segmentation review, and the still-unavailable full OBEC PDF.


## VISTEC annotation parser fail-closed repair — 2026-10-26

A review of the pinned VISTEC adapter found that empty pipe-delimited fields were silently removed after markup stripping. The adapter now raises an error for any empty token field, with regressions for repeated separators, empty markup-only tokens and a leading separator. This preserves the source-evidence gate rather than hiding malformed annotation rows. Code head: `1cbf97036ec931266f4a6ed5eb747a00e5b7ad29`.

**Verification is pending:** repository tests could not be run locally, and no workflow run/combined status was surfaced for this exact head at the last check. Do not claim the new tests or the 49,997-row VISTEC evaluation passed until exact-head CI completes and the report artifact is inspected.


## Exact-head validation refresh — 2026-10-26

A fresh GitHub Actions check now exposes three runs for branch head `550f26fdbf6fd66a0d1c2cb1caa9bd6bd10de196`: CI [40346688497](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40346688497), Web static validation [40346688520](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40346688520), and external VISTEC evaluation [40346688621](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40346688621). All three are **queued**, not passed or failed. The previous paragraph's “no workflow run surfaced” wording is historical and superseded by this refresh. Local tests remain `NOT_RUN`; no VISTEC metric is claimed. Acceptance still requires exact-head CI and static validation to pass, the VISTEC workflow to pass, and inspection of its report artifact.


## Failed exact-head runs diagnosed and repaired — 2026-10-26

- CI run [40346688497](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40346688497) failed one test because `tests/test_corpus_source_registry.py` still expected the obsolete phrase `CC BY-SA 3.0 reported`, while the registry records the pinned README's declaration `CC-BY-SA-3.0 declared in pinned upstream dataset README; attribution/share-alike required`. Updated the test to match the evidence record.
- VISTEC run [40346688621](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40346688621) verified the pinned upstream commit and CSV blob hash and trained the research-only TUD model, then failed because the immutable CSV has **50,000 data rows**, not the stale 49,997 expected by the evaluator. The upstream README describes 49,997 samples; the metadata/CSV discrepancy is recorded explicitly. Updated evaluator and workflow assertions to use 50,000 rows and updated the corpus registry to distinguish README metadata from actual CSV row count.
- Web static validation [40346688520](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40346688520) passed for the prior code-bearing head.
- Fix commits: `357d83c10ee2647b0debe5c7efe52b489c37f4bd`, `ea27324a044e7d9c3298285e09bc7959b15681f5`, `55306fda1af8c9652854e6d504ff56ff0358fdeb`, `906e1293203635dcf481dbc164712403d088231c`, `e05d5644f94b5d9c8707c3da981182822d272fa0`. Exact-head CI/VISTEC revalidation has not yet been observed. No benchmark metric is claimed.


## Corrected-head workflow refresh — 2026-10-26

After the row-count assertion was corrected in workflow commit `ccee129d509c95f95c2f455fd769bcbcd9ae71e0`, GitHub Actions reported fresh runs: CI [40353097806](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40353097806), Web static validation [40353097480](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40353097480), and VISTEC evaluation [40353097539](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40353097539). At the last poll all three were queued; this is not a pass. The corrected workflow now asserts 50,000 rows for the corpus, source-annotated gold rows, and each engine's predictions. Local tests remain unrun in this session; no VISTEC metric is claimed.


## Latest exact-head workflow diagnosis — 2026-10-26

- CI [40354836807](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40354836807) failed exactly one of 194 Python tests: the VISTEC source registry test expected the obsolete phrase `verify upstream terms`. The registry accurately records `CC-BY-SA-3.0 declared in pinned upstream dataset README; attribution/share-alike required`. Corrected the assertion to check the declared attribution/share-alike requirement, commit `0e60b2d277facee573839335b7e1681d5520a224`.
- On that tested PR merge ref, Web static validation [40354836884](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40354836884) passed and external VISTEC evaluation [40354836797](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40354836797) passed. The latter processed the pinned CSV with 50,000 data rows; upstream README's 49,997-sample description remains a documented metadata discrepancy. Do not claim expert accuracy: source annotations are not independently adjudicated.
- Exact-head CI after the assertion repair is pending. Local tests were not run in this session. Readiness remains research prototype / not release-ready; independent Thai IPA/acoustic review, Ukrainian-native target judgments, human segmentation adjudication, contextual review of บรรจุ final /ʔ/, and full official OBEC PDF inspection remain evidence-limited.


## VISTEC report values and interpretation — 2026-10-26

Successful external run [40354836797](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40354836797) emitted a 50,000-row JSON diagnostic (all labels SOURCE_ANNOTATED, zero expert-adjudicated rows). Dictionary max-match: boundary precision 0.7687958, recall 0.8978785, F1 0.8283385, exact sequences 76/50,000 (0.152%). Research-only TUD unigram Viterbi: precision 0.6064011, recall 0.9931576, F1 0.7530226, exact sequences 16/50,000 (0.032%). Coverage is 1.0 for both, but coverage is not accuracy. These are agreement diagnostics against upstream source labels, not independently adjudicated gold; the low exact-sequence rates preclude a production-quality claim. Artifact ZIP ID 12667445022 was uploaded with SHA-256 a02e3c8fe769a9b0998fdf2e66a49d6d0bec1c0b7191e08854d2dd81cc50132c; the archive itself has not been opened in this session.


Artifact ZIP 12667445022 was downloaded and inspected. It contains only `vistec-segmentation-report.json` (3,803 bytes); the parsed JSON schema is 1.0 and its row counts, evidence grade, and engine metrics match the successful workflow log. The SHA-256 digest matches the workflow artifact metadata. This closes the artifact-inspection acceptance criterion for the source-annotation diagnostic, but does not create expert-adjudicated gold or change the research-prototype readiness classification.

## Beta-site disclosure update — 2026-10-26

The service page now visibly labels the tool as a research beta and directs users to the evidence/limitations page. The system page presents the latest source-annotated segmentation diagnostics:

- VISTEC, 50,000 rows: dictionary boundary F1 0.82834, 76/50,000 exact sequences (0.152%); research-only TUD Viterbi F1 0.75302, 16/50,000 exact sequences (0.032%).
- Wisesight, 993 rows: dictionary boundary F1 0.83947, 192/993 exact sequences (19.34%); research-only TUD Viterbi F1 0.74862, 119/993 exact sequences (11.98%).
- Both datasets are source-annotated; zero rows have independent expert adjudication. These are agreement diagnostics, not an accuracy claim. Neither segmenter is presented as production-ready.

A UI-contract regression now checks the beta notice, evidence anchor, reported denominators, and responsive CSS. These changes are newer than the latest successful CI/static/VISTEC checkpoint and remain pending exact-head reruns.

The Pages workflow is configured to deploy on pushes to `main`; PR #71 is still draft. I did not merge the 304-commit research PR or deploy its branch over the existing public Pages site. Public deployment remains BLOCKED until the changes are reviewed and merged, or a separate preview host is deliberately configured.

Research readiness remains partial: independent Thai IPA/acoustic adjudication, two independent Ukrainian target-form reviews, human segmentation adjudication, contextual review of บรรจุ final /ʔ/, and lawful full official OBEC PDF access remain open.

## Beta publication attempt and actual deployment status — 2026-10-26

The beta UI implementation is present on the research branch. Pages build run [40377552366](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40377552366) completed its build job successfully: Python regression suite, browser parity and the UI-contract/beta-disclosure checks all passed, and the Pages artifact was uploaded. Static validation [40377552367](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40377552367) and external VISTEC evaluation [40377560151](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40377560151) also passed for the beta UI code checkpoint.

The Pages `deploy` job in run 40377552366 failed immediately before executing any steps; GitHub exposed no job steps/logs and no pending deployment approval details. The exact cause is not observable from the available run data. A successful Pages deployment on main, run [40225366216](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40225366216), published commit `18ab41db87192dc7be69683ef85e53cb04db5517` at https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/. The new research-branch content must not be described as live.

The temporary branch-specific Pages trigger was removed. `.github/workflows/pages.yml` again deploys only on pushes to `main`, while retaining the UI-contract check in the build. This avoids repeatedly attempting a deployment from the draft research branch. No environment settings were changed, no PR was merged, and no release was published.

The beta UI commit `274371594cc8a0b65677bb126242d90acc17caf5` passed the Pages build, static validation, and VISTEC evaluation. Latest branch head after restoring the main-only deployment trigger is `048b89d9234ac91e3d592c0bca7d816f4a5ae5b5`; its push/PR CI runs were still in progress at the time of this update. The main research PR #71 remains draft and has 304 commits / 68 changed files; it must not be merged blindly merely to bypass the Pages deployment gate.

Remaining publication choices: review and merge PR #71 to main after accepting the documented evidence gates, or explicitly authorize a separate preview host. Independent Thai IPA/acoustic gold, two independent Ukrainian target-form reviews, human segmentation adjudication, contextual review of บรรจุ final /ʔ/, and lawful full official OBEC PDF access remain unresolved.

## Correction after merge and Pages queue inspection — 2026-10-26 20:51 EET

The earlier pre-merge statements in this audit are superseded by this update. PR [#71](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/71) is now merged. Merge commit: `b4ae9e9f88a79d6f55cb1207363ac6877df080ba`.

The merged Pages workflow run [40378981918](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981918) has a successful build job. The Python regression tests, generated fixture parity, browser parity, UI-contract and beta-disclosure tests, and Pages artifact upload completed successfully. However, the separate `deploy` job (ID `121775188761`) remained queued with no runner assigned and no steps after more than two hours. The run's pending-deployment endpoint returned an empty list, so there is no evidence of an environment approval gate. The exact cause of the queue delay cannot be established with the available GitHub connector.

Web static validation [40378982254](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378982254) passed. CI [40378981710](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981710) had the test job pass, while the master-artifact job was still queued at the last check. The beta code checkpoint's VISTEC diagnostic [40377560151](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40377560151) passed, but its source annotations are not independent expert gold.

**Public deployment is not yet verified.** The last known successful Pages deployment is run [40225366216](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40225366216), commit `18ab41db87192dc7be69683ef85e53cb04db5517`. The Pages URL is https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/. The beta source is merged to `main`, but do not claim that the live URL serves the new banner until run 40378981918's deploy job completes and the served pages are checked. A direct live fetch could not be verified in this session. The connected Firecrawl service reported that its account has insufficient credits; no repeated scrape attempts were made.

No environment protection or repository deployment settings were changed, no alternate hosting project was created, and no release was published. If the deploy job remains queued, the next action is to inspect GitHub Actions runner/service availability or have the repository owner retry/inspect the queued deploy job through GitHub. Do not weaken the workflow's environment or branch restrictions to bypass the queue.

Remaining linguistic evidence gates are unchanged: independently adjudicated Thai IPA/acoustic gold, human segmentation adjudication, two independent Ukrainian target-form reviews, contextual review of บรรจุ final /ʔ/, and lawful full official OBEC PDF access. Status remains **research beta candidate, not release-ready for arbitrary Thai text**.

## Verification update — Pages deployment completed — 2026-10-26 22:08 EET

This section supersedes the earlier queued-deployment status above.

- GitHub Pages workflow [40378981918](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981918) is now **completed / success**. Build job [121769734639] passed all Python regression tests, generated-fixture checks, browser parity, UI-contract/beta-disclosure checks, and artifact upload. Deploy job [121775188761] also completed successfully.
- Main CI [40378981710](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981710) is **success**, including both the test job and master-artifact job.
- Web static validation [40378982254](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378982254) is **success**.
- Public site URL: https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/. The deployment workflow is green and the beta source was merged in commit `b4ae9e9f88a79d6f55cb1207363ac6877df080ba`. A direct fetch of the live HTML was unavailable in the connected web tool, so the precise served markup has not been independently inspected; do not confuse that limitation with a failed deployment.
- Latest separately checked main CI run [40381878163](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40381878163) also passed for docs commit `7bcc7e21c98bde8f55a7c56a1c1a97fe3486b72e`. Audit JSON synchronized in commit `6466573838c4aa18a405c510a9b5e56f0ea453b3`.

**Status:** research beta deployment is operational according to GitHub Pages workflow; not a release-ready general-purpose Thai transcription system. The independent Thai IPA/acoustic gold, human segmentation adjudication, two independent Ukrainian target-form reviews, contextual review of บรรจุ final /ʔ/, and lawful full official OBEC PDF access remain research evidence blockers. Source-annotated VISTEC/Wisesight diagnostics are not expert-adjudicated gold.


## Whole-text input follow-up — 2026-10-26

The browser engine's prior whole-run lookup failed closed whenever an uninterrupted Thai-script span was not an exact lexicon key. This prevented IPA for known words adjacent to unknown text and did not meet the expected whole-text workflow. A conservative dictionary-max-match implementation and UI regression cases have now been added on branch `fix/examples-ipa-coverage-20261026`.

This is **PARTIAL**, not a claim of full Thai text recognition: known lexicon entries may produce IPA, unknown spans remain explicitly unresolved, and greedy matches can be wrong in ambiguous contexts. CI/static validation for the latest branch head is required before this change is DONE_VERIFIED. Independent word-boundary adjudication and IPA/UA evaluation remain outstanding.


## Whole-text Thai input — verification update — 2026-10-26

- Code-bearing head `1b1553876ef24bf18f692d7aa512634bdceeee70` passed the CI `test` job and `master-artifact` job in [run 40400809948](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40400809948); the generated master table assertion passed. Web static validation passed in [run 40400809797](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40400809797).
- The first test runs exposed two test-contract defects, not a hidden pass: a parity probe treated a string containing known lexicon substrings as wholly unknown, and UI assertions counted copy-button accessible labels as additional IPA field labels. The parity probe now uses the genuinely unknown span `ทดสอบ`; the UI test counts visible IPA field labels and matches the actual punctuation-token markup. The final CI run passed the corrected parity and UI-contract tests.
- Whole-text browser segmentation remains **PARTIAL**, because greedy dictionary max-match is not a complete or context-aware Thai segmenter. Unknown spans abstain from guessed IPA/Ukrainian output. PR #73 has since been merged as `e49b5f2b54d42e577f732b4308080e11e410d557`. The Pages workflow is configured to deploy on a push to `main`, but live publication was not independently confirmed.
- Independent word-boundary adjudication, independent Thai IPA/acoustic gold, and independent Ukrainian target-form review remain outstanding. Source-annotated Wisesight diagnostics are not expert-adjudicated gold and must not be presented as accuracy proof.


### Lexical IPA override status correction — 2026-10-26

A final UI review found and fixed a summary-status bug: entries with `segmentationStatus: lexical_ipa_override` already rendered source-attested IPA but were counted as unresolved because the summary accepted only `lexicon`. The summary now accepts both known statuses; the UI-contract test verifies `เงินเดิน` produces two IPA field labels without an unresolved notice. Code checkpoint `3ccf84f564add02c189524c3b9ca794154d35c8b` passed CI's `test` job and web static validation (runs [40402504410](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504410) and [40402504394](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504394)); the `master-artifact` job subsequently completed successfully in run [40402504410](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504410). This does not change the research-readiness conclusion: dictionary max-match remains partial and linguistic gold/adjudication blockers remain open.


### Post-merge deployment status — 2026-10-26

PR #73 is merged at `e49b5f2b54d42e577f732b4308080e11e410d557`. The merged `main` branch contains the new whole-text hint, corrected label, and lexical override status handling. The code-bearing checkpoint `3ccf84f564add02c189524c3b9ca794154d35c8b` passed CI test + master-artifact and web static validation. The Pages workflow is configured to run on relevant pushes to `main`; however, live-site verification remains **BLOCKED by available tooling**: the GitHub connector exposes PR-triggered runs but not push-triggered Pages runs, direct web fetching was disabled, the container fetch failed, and the connected Firecrawl account reported insufficient credits. Do not claim the live deployment is confirmed until the Pages workflow is checked and the served HTML is inspected.


## Authoritative status refresh — 2026-10-27

Documentation PR #75 was merged into `main` at `581231596a0df6b3ab58964dacedeec7a8fd8908`. Its CI run [40406992550](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40406992550) completed successfully: `test` and `master-artifact` both passed. The checks include Python tests, generated-artifact drift, the 351,780-row / 41-vowel master artifact, IPA→Ukrainian, Python/browser parity, UI contract, and segmentation/IPA diagnostics.

This is an engineering verification result, **not** evidence that every arbitrary Thai text receives complete IPA. Whole-text input is implemented; greedy matching over known entries is partial. Ambiguous or unknown spans remain unresolved, and greedy matching can mistake a known substring inside a larger unknown word. The live Pages state for the new UI remains unverified: acceptance requires a successful post-change Pages build/deploy and inspection of the served HTML.

The repository remains a **partial research prototype, not release-ready for arbitrary Thai text**. Independent word-boundary adjudication, Thai IPA/acoustic gold, two Ukrainian target-form reviews, contextual review of `บรรจุ` final /ʔ/, lawful full OBEC PDF access, and per-resource license/attribution review remain open.


## Browser CC0 segmentation and deployment gate — 2026-10-27

PR #77 merged at `96c2af3c2a24d0ea95455b5d6af4c079e5609d29`. The browser now uses the existing pinned 60,963-entry CC0 Thai word list as boundary evidence, generated reproducibly by `scripts/generate_web_word_dictionary.py`. The generated JS index is 1,615,714 bytes and is created before browser tests and Pages packaging rather than committed as a large generated file.

The longer-match regression for `กาแฟ` prevents the known substring `กา` from producing a false partial pronunciation. The existing `เงินเดิน` UI regression exposed a cluster-boundary bug in the first implementation; it was corrected by excluding preposed vowels from the combining-mark set. Web static validation passed on head `7b2c9572feb542fb3ee81558b9758bb4fa5f2bef` ([run 40411659863](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40411659863)); the full CI test job passed on runtime code head `3eb1155631da158b7e04436f608711680750e475` ([run 40411558761](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40411558761)). Exact-head CI and the master-artifact job were not confirmed green; those runs remained queued.

The Pages workflow now includes a post-deployment HTTP contract check for the whole-text hint, examples, and beta notice. Its post-merge run `40412224812` was queued at the last check. Until it completes successfully, live deployment remains unverified. Dictionary boundaries still do not imply pronunciation: non-curated words remain unresolved. This is a partial research prototype, not release-ready for arbitrary Thai text.

## Audit refresh — browser dictionary prefix index verified (2026-10-27)

- PR #79 merged at `c799dbed4247ac9743845acc0fd4131922cfbb74`; the verified code-bearing head `e17a7f96fef9989f6375d36331f30ce0246e378a` passed CI run [40466046264](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466046264) (`test` and `master-artifact`) and Web static validation [40466046237](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466046237).
- Post-merge Pages run [40466830868](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466830868) passed build, deploy and served-homepage contract. Main Web static validation [40466830820](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466830820) and main CI [40466830808](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466830808) passed.
- Generator output: 60,963 entries, 1,085 two-code-point prefix buckets, largest bucket 1,521, generated JavaScript 1,629,301 bytes (13,587 bytes / ~0.84% larger than the previous index). This is not a measured runtime speedup.
- PR #80 merged the matrix/handoff evidence at `dd2260356f7de17d56d25b06c7c6b2c5999c0709`. The exact documentation-head CI run [40467565451](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40467565451) was still in progress at this audit refresh; the runtime code is unchanged from the verified code-bearing commit.
- The product remains a partial research prototype. Independent Thai segmentation adjudication, Thai IPA/acoustic gold, two independent Ukrainian target-form reviews, contextual review of `บรรจุ` final /ʔ/, lawful official OBEC PDF access, and per-resource licensing/attribution remain blockers.

## 2026-10-27 — methodology matrix outcome

- Added `docs/ukrainian-transcription-methodology.md` and linked it from README; validation matrix and master handoff record the continuation.
- Classification: PARTIAL. This is a documented first-pass method table, not a runtime rule registry and not a linguistically validated standard. It distinguishes onset/coda, IPA layers, vowel/rime patterns, tone/length, context rules and lexical uncertainty.
- Evidence limits: the Thai–Russian practical table is a comparison reference, not an authority for Ukrainian output. The exact 2025 edition mentioned by the reference page was not independently checked against the book itself. No independent IPA gold, Ukrainian-form adjudication, or held-out accuracy result was added by this documentation change.

- Completeness follow-up: added explicit Thai script inventory checklist (44 consonants incl. obsolete ฃ/ฅ, conventional 32 vowel forms, four tone marks, diacritics/special signs, ten Thai digits, mixed text) and primary technical references (NECTEC, W3C, Thai Orthography Notes). This corrects the earlier implication that the initial correspondence tables themselves covered the full inventory.
- Audit status remains PARTIAL: documentation enumerates the inventory, but no executable proof of actual runtime handling for every symbol or context has been produced in this update.


### Thai → Ukrainian adaptation follow-up — 2026-10-27

The current PR branch now implements the selected IPA-adapter policy: Thai /h/ → Ukrainian «г»; /kʰ pʰ tʰ/ → «к/п/т»; /tɕ/ and /tɕʰ/ → «ч». The latter pair is voiceless and differs by aspiration, whereas Ukrainian «дж» /d͡ʒ/ is voiced and would add a non-source feature. Python/browser regression cases and the derived consonant table were updated. Exact-head CI and generated-artifact verification are still queued; no accuracy improvement or official standard is claimed. This note supersedes older provisional /h/ → «х» statements for this branch's selected policy. The repository remains a partial research prototype pending linguistic adjudication.


## 2026-10-27 — continuation: verified IPA policy merge and benchmark evidence gate

- Branch for this audit/handoff update: `audit/thai-ipa-benchmark-gates-20261027`, created from the then-current `main` after PR #106 was merged. Starting main before merge: `c7e686d4665c978577f771e62947545ddbc67cfe`; PR #106 head: `7e4ccb8aa789f97144ee46a9b5927402cb58e05c`; merge commit: `e3052ff9bede79ed8b4f19e746ce545912cfd7d5`.
- PR #106 was not merged blindly: exact-head CI run [40586665956](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40586665956) passed; Web static validation [40586665936](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40586665936) passed. The PR contains Python/browser IPA-adapter mappings and regression tests for /h/ → г, aspiration neutralization only at the Ukrainian practical layer, /tɕ/ and /tɕʰ/ → ч, and rejection of unsupported /d͡ʒ/ as a Thai correspondence. This is a verified implementation/policy change, not evidence of general end-to-end accuracy.
- **Benchmark data-quality gate:** `data/benchmark/gold.tsv` contains only its header (0 gold rows). `data/benchmark/source-attested-ipa.tsv` contains 6 source-attested dictionary entries, all explicitly labelled `SOURCE_ATTESTED_NOT_GOLD`. `data/benchmark/thai_g2p_challenge.jsonl` has 42 challenge candidates, with 0 adjudicated gold IPA labels; these are probes, not scored test cases. `data/benchmark/segmentation-predictions.tsv` is header-only (0 prediction rows), so the 606,026-byte segmentation-gold file cannot yield a current prediction score. Target-adjudication entries are candidates pending independent adjudication, not preference gold. No accuracy percentage or before/after accuracy claim is valid from these datasets.
- Existing external-engine evidence remains smoke/diagnostic only: `data/external-ipa-renderers.json` documents Goruut with partial coverage and variable output; prior smoke results for ThaiPhon and FastThaiG2P are execution/inter-engine comparisons without independent gold. No external engine is promoted to a production dependency and no external IPA output is treated as gold. Resource-level provenance/licensing and output conventions remain unresolved for potential reuse.
- PR #104 morphology branch has exact-head CI [40574979967](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40574979967) and [40574969370](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40574969370) successful and Web static validation [40574979983](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40574979983) successful on head `9fbdb5d9a73fe36fc3c6d42e6800304a46c06d1b`. It remains open and is not merged here: it was based on older `main`, overlaps browser/README/audit/handoff files, and needs reconciliation against merged PR #105 and now-merged PR #106 before integration. Earlier PR #101 remains untouched.
- Task ledger: IPA adaptation policy implementation + Python/browser regression CI = `DONE_VERIFIED`; main integration of #106 = `DONE_VERIFIED`; source-attested IPA inventory = `PARTIAL`; end-to-end G2P accuracy evaluation = `BLOCKED` by absent adjudicated gold; segmentation accuracy evaluation = `BLOCKED` by header-only predictions; Ukrainian target-form accuracy = `BLOCKED` by pending independent adjudication; external engine production integration = `DEFERRED` pending reproducible interface, provenance/license review, deterministic candidate contract, and IPA validation; PR #104 = `PARTIAL` pending rebase/reconciliation and exact post-rebase verification.
- Environment limitation: a local shallow clone was attempted but failed because this runtime could not resolve `github.com` (`Could not resolve host: github.com`). Therefore no local Python, browser, build, or generator commands are claimed as executed in this session. Verification cited above is GitHub Actions evidence only. This audit branch documents evidence and does not claim local reproducibility.
- Acceptance criteria for a real accuracy benchmark: (1) independently reviewed and source-cited IPA gold with status and license per row; (2) nonempty, reproducible predictions generated by the exact tested commit; (3) separate metrics for structure/segmentation, IPA, target adapter on adjudicated IPA, end-to-end output, strict refusal quality, approximate coverage, and regressions; (4) versioned run metadata and held-out split. Do not populate gold with guesses merely to make metrics available.


## 2026-10-27 — source-attested lexical tone-pair addition

- Added `ไกล` and `ใกล้` lexical IPA overrides from pinned Wiktionary revisions 5688545 and 5721860. The source-attested IPA has the same segmental sequence `klaj` and distinct tone contours (mid vs falling); the records retain CC-BY-SA-4.0 provenance and the `ACTIVE_SOURCE_ATTESTED_NOT_GOLD` status.
- Added regression assertions for provenance, IPA, tone, diphthong, adapter output, and the non-gold warning. Updated the existing source registry test.
- **Status: PARTIAL pending exact-head CI and web static validation.** No local tests are claimed. The change is an evidence-backed exact-form coverage improvement only; it does not establish overall engine accuracy.
- **Unresolved acceptance gate:** independently adjudicated IPA gold remains absent, so overall G2P/IPA/end-to-end accuracy is NOT_MEASURED. The new source-attested overrides must be treated as circular evidence in any diagnostic that compares the runtime against the same source records.


## Source-attested tone-pair continuation — 2026-10-27

- Added exact-form, revision-pinned IPA overrides for `ไกล` (/klaj/, mid tone) and `ใกล้` (/klaj/, falling tone), with CC-BY-SA-4.0 provenance. Both are `ACTIVE_SOURCE_ATTESTED_NOT_GOLD` and feed the typed IPA→Ukrainian adapter.
- Exact-head CI run [40591565959](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40591565959) passed master-table generation and all 203 Python tests, then exposed a stale source-attested diagnostic assertion. Actual diagnostic: 6 source records, 4 circular overrides, 2 independently comparable records, 1 segmental agreement and 2 tone agreements; no accuracy claim.
- Corrected the CI assertion and current audit counts. Follow-up exact-head CI remains pending; this continuation is not yet DONE_VERIFIED and must not be merged until the rerun passes.
- Independent adjudicated IPA gold remains absent; the repository is still a research prototype, not release-ready.


## 2026-10-28 — verified merge and live Pages deployment

- PR [#108](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/108) was squash-merged into `main` as `c6ba73b77766b0169d70619383b6efe27564d774`. This is the single active release path; no user branches were deleted.
- Exact-head CI [40592380586](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40592380586) passed both `test` and `master-artifact`. Web static validation [40592380619](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40592380619) passed, including browser JavaScript syntax, Python/browser parity fixtures, and IPA→Ukrainian/UI contracts.
- GitHub Pages deployment [40592864388](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40592864388) passed its build and deploy jobs. The post-deploy workflow verified the live whole-text interface, strict/soft/super-soft modes, and IPA adapter contract at https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/.
- The Python/browser lexical IPA adapters now both handle the source-pinned pair `ไกล` and `ใกล้` as phonemic /klaj/, preserve mid vs falling tone, return the same Ukrainian candidate `клай`, and withhold surface IPA because the dictionary source does not provide an independently verified surface-phonetic form. Both entries remain `SOURCE_ATTESTED_NOT_GOLD`.
- The source-attested diagnostic reports 6 records, 4 circular source overrides, 2 independently comparable records, 1 segmental agreement and 2 tone agreements. This is source-comparison evidence, not an accuracy score. `data/benchmark/gold.tsv` remains without independently adjudicated IPA gold; overall G2P/IPA/end-to-end accuracy is still NOT_MEASURED.
- Post-merge CI run [40592864584](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40592864584) had its `test` job pass; its separate `master-artifact` job was still running at audit time. The exact-head PR CI above passed both jobs, and the Pages build independently generated the master table and passed its Python/browser checks.
- PR #101 was closed as a duplicate of #104; PR #104 was closed/deferred because its separate research-only morphology overlay was based on an older main and had not been reconciled against the deployed head. Both source branches are preserved. Reopen/port that feature only after rebasing, exact-head CI and browser parity, and keeping morphology outside practical phonetic output.
- Readiness: engineering and deployment checks are verified; the project remains a research prototype, not release-ready for accuracy claims, pending independent IPA gold and Ukrainian target-form adjudication.


## 2026-10-28 — phonology completeness and ambiguous readings

- Added source-backed coverage matrix: `docs/phonology-ambiguity-coverage.md`.
- The current engine correctly keeps unlisted `ทร`, `รร`, `ฤ/ฤๅ/ฦ/ฦๅ`, false-cluster and thanthakhat constructions analysis-dependent. Source-backed exact lexical readings must not be extrapolated into global spelling rules.
- Royal Institute 2011 material distinguishes `ทราย` meaning sand (historically non-cluster /s/) from the deer-name sense (true cluster reading). A context-free override is unsafe without word/sense context.
- Added Python regression coverage for fail-closed behavior and for the exact lexical `ทราบ` reading not generalizing to `ทราย`.
- Current status: implementation coverage audit is PARTIAL; exact-head CI has started but remains in progress at `generate_master_table.py`. No test pass is claimed for this new branch yet. Independent IPA gold and Ukrainian target adjudication remain separate blockers.


## 2026-10-28 — sense-scoped ทราย reading

- Added the source-pinned compound `ทะเลทราย → ทะ|เล|ซาย` from en.wiktionary oldid 87239667, which records `/tʰa˦˥.leː˧.saːj˧/`. The source is dictionary evidence, not independent gold.
- Isolated `ทราย` remains withheld because the Royal Institute distinguishes the sand sense from the deer-name sense with a true cluster. This resolves one documented context without generalizing the `ทร` spelling rule.
- Python and browser regression tests are added; the final branch CI remains in progress at the master-table generator, so these tests are not yet verified.


### Verification note — regression harness correction

The first run with the new coverage tests completed master-table generation and ran 209 Python tests. The source-attested `ทะเลทราย` compound test, the ambiguity sentinels, and all tone-table tests passed; one newly added `ทราบ` regression failed because it called the structural parser but asserted final IPA. The test now calls `api.analyze_syllable()`. The latest branch head requires a full rerun; no green status is claimed yet.


### Verification closure — 2026-10-28

- Exact code head `7a47e1f86862f33bb8eadfb34de75aeba5fd3809`: CI run [40645028725](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40645028725) passed all 209 Python tests and all downstream diagnostics/browser checks; its `master-artifact` job passed and verified 351,780 rows / 41 vowel records.
- Web static validation [40645028587](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40645028587) passed.
- Overall status remains research prototype / PARTIAL for full linguistic coverage and accuracy because independent IPA gold, independent Ukrainian target adjudication, broad lexical coverage and connected speech are not complete.


## Production closeout — 2026-10-28

- PR #110 merged to `main` as `403e0bc02dee5e469511d91bba64d64010b2594d`.
- Post-merge CI [40645764144](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40645764144) passed the full test and master-artifact jobs.
- Pages deployment [40645764146](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40645764146) succeeded; published homepage contract verified at https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/.
- Readiness remains **research prototype / PARTIAL linguistic coverage**. Independent IPA gold and Ukrainian target adjudication are still absent; source-attested lexical entries are not accuracy evidence.


## 2026-10-28 — aspiration marker policy (merged and deployed via PR #115)

- The IPA→Ukrainian adapter previously mapped aspirated stops/affricate to the plain Ukrainian letter and recorded aspiration as neutralized. This contradicted the approved project decision.
- Changed Python and browser mappings so /kʰ pʰ tʰ tɕʰ/ produce к' п' т' ч'. The apostrophe is appended to the adapted consonant segment, before any following segment; plain /k p t tɕ/ remain к п т ч. /h/ remains «г» and /ʔ/ remains separately handled.
- Added matched positive/negative tests. Exact-head CI passed in run [40691939835](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40691939835); independent linguistic review remains evidence-limited. This is a project transcription convention, not an official Ukrainian norm.


## Production closeout — RTGS and aspiration, 2026-10-28

- PR #115 merged to `main` as `fa75fe153a845aadbc7aad6b3e47a1ac5a6965f5`.
- Full exact-head CI, including the `master-artifact` job, passed: [40691939835](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40691939835). Web static validation passed: [40691940070](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40691940070).
- GitHub Pages deployment [40692707861](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40692707861) passed and verified the published RTGS panel plus `src/rtgs-reference.js` at https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/.
- The Pages build now runs the RTGS browser regression tests, pinned PyThaiNLP 5.4.0 parity, and IPA-adapter tests before deployment; the post-deploy job verifies the actual published JavaScript markers.
- **DONE_VERIFIED — public site copy:** PR #116 merged as `f4cc4d061c529fc5aec094af896dea5aaec9378f`; exact-head CI [40693398363](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40693398363), static validation [40693398375](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40693398375), and post-merge Pages deployment [40694421367](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40694421367) passed. The deployment job verified the published homepage and system-page copy plus the RTGS module.
- Readiness remains **research prototype / PARTIAL linguistic coverage**. Independent expert-adjudicated Thai IPA, word boundaries and Ukrainian target forms remain absent; no general accuracy claim is justified.


## Public-site content audit register — 2026-10-28

| ID | Surface / issue | User impact | Status | Evidence / implementation | Acceptance / remaining work |
|---|---|---|---|---|---|
| PUB-001 | Homepage invited long text without foregrounding Thai word-boundary uncertainty | Users could mistake article-level output for reliable transcription | DONE_VERIFIED | Homepage recommends one word first and warns that continuous Thai text may have uncertain boundaries. Pages run [40694421367](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40694421367) verified the served HTML. | Complete; keep the caution visible if the input flow is redesigned. |
| PUB-002 | Soft/super-soft labels could imply that more coverage means more accuracy | Misleading confidence in approximate output | DONE_VERIFIED | Mode labels now call these provisional candidates and explicitly state that more coverage does not mean greater accuracy. Exact-head UI contract and Pages checks passed. | Complete; any new fallback mode must carry the same uncertainty disclosure. |
| PUB-003 | IPA adaptation was presented as a separate mode despite already running in the main pipeline | Duplicate workflow obscured the algorithm and could imply IPA conversion was detached from Thai analysis | PARTIAL | Standalone form removed; method note now explains the existing IPA-first path and feature neutralization. Exact-head CI and live Pages verification pending on branch `ux/integrate-ipa-adaptation-into-main-flow-20261028`. | Pass UI contract and deployment checks; confirm IPA, per-syllable rule audit, and neutralized-feature disclosure remain in the main flow. |
| PUB-004 | Public research status and segmentation metrics could be read as end-to-end transcription accuracy | Overstated linguistic evidence | DONE_VERIFIED | System page distinguishes regression tests, source-attested lexical readings and segmentation diagnostics from independent expert gold; the prior headline segmentation metrics were removed from the primary explanation. | Complete; do not reintroduce accuracy claims without an independently adjudicated corpus. |
| PUB-005 | UI contract test asserted superseded homepage wording | CI failures and stale public copy contract | DONE_VERIFIED | UI contract updated for short-input guidance, fallback labels, RTGS and revised evidence copy; exact-head CI [40693398363](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40693398363) passed. | Complete; keep assertions aligned with the public contract. |
| PUB-006 | Independent expert-adjudicated Thai IPA, word boundaries and Ukrainian target forms are unavailable | Linguistic accuracy cannot be established | BLOCKED | Current source-attested examples and engineering parity are not independent gold. | Obtain a versioned, licensed, independently adjudicated corpus; publish per-layer metrics and error analysis before making general accuracy claims. |
| PUB-007 | Live published HTML/JavaScript had not been independently checked after deployment | Risk of merging code that was not actually published | DONE_VERIFIED | Pages deployment [40694421367](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40694421367) fetched the served homepage, system page and JS modules, then verified the updated guidance and RTGS contract. | Automated deployment contract complete; manual browser visual review remains open. |

## Production closeout — public guidance, 2026-10-28

- PR #116 merged to `main` as `f4cc4d061c529fc5aec094af896dea5aaec9378f`.
- Exact-head CI [40693398363](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40693398363) passed; web static validation [40693398375](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40693398375) passed.
- Pages deployment [40694421367](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40694421367) passed and confirmed the updated public guidance and RTGS panel at https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/.
- Manual visual review was not performed. Automated deployment checks prove the served content and module markers, not visual polish across browsers or devices.
- Readiness remains **research prototype / PARTIAL linguistic coverage**, not release-ready, because independent expert IPA, segmentation and Ukrainian target-form gold are absent.


## Final repository checkpoint — 2026-10-28

- PR #117 merged as `713f42ec816856d352ea2efbacfd534590e456df`; full exact-head CI including `master-artifact` passed in [40695138890](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40695138890).
- PR #112 was closed as superseded after its unique copy and UI-contract changes were ported through PR #116 and the audit register was ported through PR #117.
- The site is live at https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/. RTGS deployment [40692707861](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40692707861) and public-guidance deployment [40694421367](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40694421367) passed served-content checks.
- Manual browser visual review remains PARTIAL; independent linguistic gold remains BLOCKED. No end-to-end accuracy claim is made.

## 2026-10-28 — UX accessibility polish

- Starting main: `25ebb8f70264ee76f3a93c48b42fd35154cfb77e` (the UX refresh and corrected Pages contract were already present).
- Increased navigation, mode disclosure, and methodology-link hit areas to 44px, including mobile navigation; bumped both stylesheet cache keys so browsers fetch the refinement.
- Added UI contract assertions for target sizes, keyboard focus, and cache keys. Strict-mode default, uncertainty copy, IPA-first output and separate RTGS reference remain intact; no pronunciation rules changed.
- **DONE_VERIFIED — code and tests at `00fbd12780d6951fe9d820027d29f12ac1861974`:** CI [40718211681](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40718211681) and web static validation [40718211647](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40718211647) passed.
- **PARTIAL — publication:** the 44px target/cache-key follow-up still requires merge and a successful post-merge Pages live-content gate. Real-browser visual review and WCAG 2.2 AA checks remain unperformed; linguistic gold remains evidence-limited.

## 2026-10-28 — UX refresh publication verified

- **DONE_VERIFIED:** PR [#123](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/123) merged as `275d615424ef425599d2cce550b0bbc100348719`.
- **DONE_VERIFIED:** Pages deployment and live single-flow UI/IPA/RTGS content contract passed in [run 40719517666](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40719517666); web static validation passed in [run 40719517689](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40719517689). Full CI including `master-artifact` passed at the exact PR head in [run 40719154739](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40719154739).
- Public site: https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/ .
- **PARTIAL:** manual real-browser visual review and full WCAG 2.2 AA verification were not performed in this connector-only workflow. Independent expert-adjudicated Thai IPA, segmentation and Ukrainian target-form gold remain unavailable; the project is a research prototype, not release-ready.

## 2026-10-28 — UX status-language clarity follow-up

- Starting main: `77d8cd4c4328342e0ca11344c4bc2af9f5c6f25e` (UX refresh and publication evidence already merged).
- Replaced raw token segmentation codes in the detailed result card's visible status/badge with plain Ukrainian explanations (e.g. «Словниковий запис», «Попередній структурний розбір», «Розбір не встановлено»). The original machine status remains visible as a technical code for research traceability.
- Removed obsolete CSS for the retired standalone IPA input panel; the IPA-first adapter, main continuous IPA result and syllable-level adaptation audit are unchanged.
- Added regression assertions and a published-content contract for human-readable statuses; stylesheet cache keys were bumped.
- **Acceptance pending:** exact-head CI and static validation, PR review/merge, and successful GitHub Pages published-content gate.
- **Evidence limits:** no real-browser screenshots/manual device review or full WCAG 2.2 AA assessment claimed; independent expert-adjudicated Thai IPA/word-boundary/Ukrainian-target gold remains unavailable. No phonological rules changed.

### Verification update — 2026-10-28

- Exact code/test commit `82d7fd5d6469b3d2c2fcad98158bf98dcb452135`: full CI passed, including Python unit tests, RTGS tests/parity, IPA→Ukrainian tests, browser parity, UI contract tests and the 351,780-row master-artifact gate: [CI run 40723829479](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40723829479).
- Web static validation passed: [run 40723829245](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40723829245).
- **Still pending:** PR #125 merge and post-merge GitHub Pages live-content verification. Do not describe the status-label change as published until that gate passes.


## 2026-10-28 — final interaction and result hierarchy polish

- Branch: `ux/final-interaction-and-result-polish-20261028`, based on `main` at `3b70e3e78ae83f72a345c077464cb3b2d825e48f`.
- Implemented: RTGS output is now a collapsed secondary disclosure by default; the primary Ukrainian candidate and IPA remain visible. The selected engine mode dynamically explains its consequence and uncertainty in Ukrainian. Copy and clear controls use a consistent 44px minimum target; small eyebrow labels are increased; CSS/JS cache keys are refreshed.
- Added UI regression assertions for RTGS disclosure and mode-specific guidance, and added published-content checks for the new markers.
- **DONE_VERIFIED — code and automated acceptance:** PR [#126](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/126) merged as `743a412cd9343cbbbe4ccf3428f0a3c736d8cf58`. Exact-head full CI passed [40729153978](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40729153978); web static validation passed [40729160689](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40729160689). GitHub Pages published-content verification passed [40729942455](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40729942455).
- Evidence limits: no browser screenshot or real-device session was available through the connector-only workflow; do not claim manual visual QA or WCAG 2.2 AA certification. Independent expert-adjudicated Thai IPA, word-boundary, and Ukrainian target-form gold remain unavailable.


## Final UX/UI polish closeout — 2026-10-28

- **DONE_VERIFIED:** primary Ukrainian candidate and IPA remain visible; secondary RTGS is collapsed by default. Mode-specific uncertainty copy updates on selection, copy/clear targets meet a 44px minimum height, and asset cache keys are refreshed.
- **DONE_VERIFIED:** UI contract, Python/browser/IPA regression suite and generated master-artifact gate passed at PR head `2978a4cd1d93f6c71aaff1b22e1b6b6e7fe5a136` in [CI 40729153978](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40729153978). Static validation passed in [40729160689](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40729160689).
- **DONE_VERIFIED — published:** merged commit `743a412cd9343cbbbe4ccf3428f0a3c736d8cf58`; GitHub Pages deployment and live contract passed in [40729942455](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40729942455). Public URL: https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/
- **PARTIAL / evidence-limited:** no real-browser screenshots or physical-device sessions were available in this connector-only execution; no WCAG 2.2 AA conformance claim. Independent Thai IPA, word-boundary and Ukrainian target-form gold remain unavailable. Project remains a research prototype, not release-ready for accuracy claims.


## 2026-10-28 — user-directed result order supersedes collapsed RTGS

- User requirement: the three result types must be visible immediately on screen, ordered **RTGS romanization → IPA → Ukrainian candidate**. RTGS must not be a hidden disclosure/tab.
- Implementation on `ux/show-romanization-ipa-ukrainian-in-order-20261028`: three separate continuous panels, explicit numbered headings, concise RTGS limits (including aspirated `ph/th/kh` notation), shortened first-use copy, refreshed cache keys, and UI/Pages regression checks for order and visibility.
- Architectural distinction retained: the displayed order is not the computation order. The source pipeline remains Thai structural/phonological analysis → IPA → Ukrainian adaptation; RTGS is a separate reference romanization and never the input to Ukrainian adaptation.
- **DONE_VERIFIED — published:** PR [#128](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/128) merged as `086e62f252f0b16f6c4035ccb80b4b2183ef5a17`. Exact-head full CI and 351,780-row master-artifact gate passed in [40743456590](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40743456590); static validation passed in [40743456356](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40743456356). Post-merge Pages deployment and live order/visibility contract passed in [40744444939](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40744444939).
- **Evidence-limited:** connector-only work does not provide a real-browser screenshot/device session; do not claim manual visual QA or WCAG 2.2 AA. Independent expert-adjudicated Thai IPA, word-boundary and Ukrainian target-form gold remain unavailable.


### Publication evidence closeout — 2026-10-28

- **DONE_VERIFIED:** all three result panels are visible in the requested order: RTGS romanization → IPA → Ukrainian candidate; RTGS is not hidden in a disclosure. The main processing contract remains Thai structural/phonological analysis → IPA → Ukrainian adaptation, with RTGS as a separate reference.
- **DONE_VERIFIED:** exact PR-head CI passed, including UI tests, Python regression tests, browser/Python parity, IPA adapter tests, research diagnostics and the 351,780-row master artifact. Static validation passed.
- **DONE_VERIFIED — live:** GitHub Pages build/deployment and the published-content contract passed after merge. Public URL: https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/
- **PARTIAL / evidence-limited:** connector-only execution did not provide a real-browser screenshot or physical-device session; no WCAG 2.2 AA conformance claim. Independent expert-adjudicated Thai IPA, word-boundary and Ukrainian target-form gold remain unavailable; the project is still a research prototype, not release-ready for accuracy claims.



## Final audit update — 2026-10-30: Thai copy/methodology publication

- PASS — user-facing copy: PR #129 merged at 2bb0e264ed74e4d10c1a0c59ecf1d1990bcb9241; homepage copy is task-first and explains RTGS, IPA, Ukrainian candidate and uncertainty in accessible terms.
- PASS — researcher documentation separation: system.html now identifies its audience as researchers and developers and retains technical pipeline, IPA boundary, statuses, evidence and limitations.
- PASS — regression/deployment contract: PR #131 merged at feef61cba8d1a5ee6d1a79b72bfaa952f53b5e66; Pages checks new visible markers rather than stale pre-edit wording.
- PASS — exact PR-head CI: run 41073081887; both test and master-artifact jobs succeeded. Master artifact: 351,780 rows, 41 vowel records. Automated diagnostics explicitly retain evidence grades and do not claim linguistic accuracy.
- PASS — publication: Pages run 41073985170 succeeded including build, deploy and published-content checks. Live homepage and methodology page were independently fetched and contain the expected updated copy.
- PENDING at audit write time: post-merge main CI run 41073985130 had test job success while master-artifact generation was still running. Update once complete.
- No linguistic/runtime change: these PRs modify copy, a UI text assertion and Pages workflow smoke-test expectations only; Thai engine, RTGS algorithm, IPA generation and Ukrainian adapter are unchanged.
- Not release-ready for accuracy claims: no independent expert-adjudicated Thai IPA/segmentation/Ukrainian target-form gold corpus; no real-browser/device QA or WCAG 2.2 AA audit in this connector-only session.
- PR #111 (ทร lexical exception) remains an independent open task, untouched by this copy-only work.


### Final status correction — post-merge CI completed (2026-10-30)

- The post-merge main CI run 41073985130, which was pending at the time of the preceding audit entry, has completed successfully. Both test and master-artifact jobs passed; the generated master table passed the 351,780-row and 41-vowel assertions.
- PR #132 merged the documentation closeout as 78e24924ece18c92a9d872afbfe40e1f842b912b. The three canonical tracking documents now contain the verified closeout and completed CI status.


### Repository closeout reference — 2026-10-30

- Final main commit for this completed documentation closeout: fafb38143de4fecbebc143eb4b98ca71aed94cf6.
- Post-merge main CI run 41073985130 completed successfully: test and master-artifact jobs passed; master artifact contains 351,780 rows and 41 vowel records.
- Pages deployment and live-content verification passed in run 41073985170. Both public pages were fetched live and show the intended audience split.



## Final audit update — 2026-10-30: plain-language follow-up

- **PASS — homepage copy:** PR #135 merged at `867974bb16050bd815050d1b4a976283de47cdbf`. The main page now starts with a simple action and result explanation; research acronyms are no longer the primary labels for the three visible output panels. Mode descriptions explain user consequences rather than internal algorithmic behavior.
- **PASS — system page:** explains the process in plain Ukrainian first; researcher-only implementation detail is in a collapsed section. Beta and uncertainty disclosures remain visible and do not overclaim accuracy.
- **PASS — technical behavior preserved:** changes are limited to `web/index.html`, `web/system.html`, visible copy in `web/src/app.js`, UI tests, and Pages smoke-test expectations. No engine, segmentation, RTGS, IPA or Ukrainian adapter behavior changed.
- **PASS — PR-head CI:** run 41079488713; test and master-artifact both passed. Web static validation run 41079488733 passed. Master artifact assertions: 351,780 rows and 41 vowel records.
- **PASS — deployment:** Pages run 41080245447 passed build, deployment and plain-language content/pipeline assertions. Both public pages were independently fetched after deployment.
- **PASS — post-merge main CI:** run 41080245372; both test and master-artifact jobs passed, including the 351,780-row / 41-vowel assertion.
- **PARTIAL — user evidence:** automated copy contract is green, but wording has not been moderated with non-specialist users. Do not describe it as user-tested.
- **Not release-ready for linguistic accuracy:** independent expert-adjudicated Thai IPA/segmentation/Ukrainian target-form gold remains unavailable. Real-device visual QA and WCAG 2.2 AA review also remain outstanding.
- PR #111 (`ทร` lexical exception) was closed as superseded by PR #144, which forward-ported the source-attested exception to current main; the historical branch remains preserved.


## Final audit update — 2026-10-31: API internal-error disclosure

- **PASS — regression reproduced:** test-only commit e2e0e6783d277092ecf05ac87a2b712d9c03f260 failed the new test because unexpected API exceptions were not logged and their text was still exposed by the old response path.
- **PASS — implementation:** commit 60ac49dd1d3f6c387c306616e1c5a435dea4662a logs unexpected exceptions server-side and returns a generic 500 payload without the exception string.
- **PASS — exact code-head CI:** run [41139203848](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41139203848) completed all three jobs successfully: test, wheel-install-smoke, and master-artifact.
- **PASS — test evidence:** 215 Python tests passed; the new test checks both the generic client response and server-side exception logging. Existing malformed JSON/non-object request behavior remains 400.
- **PASS — packaging and generated artifact:** isolated sdist→wheel→install smoke passed; master table asserted 351,780 rows and 41 vowel records.
- The change does not alter Thai parsing, phonology, segmentation, IPA, RTGS, or Ukrainian adaptation. It does not change the documented local-by-default deployment boundary.
- PR integration and post-merge main CI are recorded in the continuation handoff after merge.

## Final audit update — 2026-10-31: HTTP Content-Length framing

- **PASS — regression reproduced:** test-only commit `3814af5e8b083117d93634531a5c62e1db5757d8`; CI [41141368949](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41141368949) failed only the new raw-socket regression. The old handler accepted `Content-Length: -1`, read the body without a declared bound, and returned HTTP 200 for a valid JSON payload.
- **PASS — implementation:** commit `47c3f335fb5aa902784f4964a842dd00e5ea01c7` validates the header as ASCII decimal digits before conversion and body reading. Invalid values use the existing 400 `invalid_request` response path.
- **PASS — exact PR-head test and packaging checks:** CI [41141511448](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41141511448) passed 216 Python tests, Ruff, browser IPA/parity/UI tests, research diagnostics and isolated wheel installation.
- **PASS — exact PR-head master artifact:** CI [41141850559](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41141850559) asserted 351,780 rows and 41 vowel/rime records and uploaded the artifact.
- **PASS — integration:** PR [#153](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/153) was squash-merged to `main` as `8a539193798e55c3010e3a6a72a0e2578ea413c9`.
- **PASS — post-merge main checks:** CI [41142211674](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41142211674) passed test (216 Python tests) and wheel-install-smoke; its separate master-artifact job also passed, asserting 351,780 rows and 41 vowel/rime records. Pages [41142211675](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41142211675) passed build, deploy and published-content/pipeline verification.
- No linguistic or browser runtime behavior changed.


## Final audit update — 2026-10-31: CI master-table artifact reuse

- **PASS — duplicate generation removed:** the `test` job uploads the already-generated master CSV, two-column CSV and JSON. The separate `master-artifact` job downloads that exact artifact and validates it rather than checking out, installing the package and regenerating the 351,780-row table.
- **PASS — integrity and structural gate preserved:** `actions/download-artifact@v8.0.2` verified the artifact SHA-256 digest; the independent job passed the 351,780-row and 41 vowel/rime assertions.
- **PASS — exact PR CI:** [41143491570](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41143491570) passed all three jobs, including 216 Python tests, Ruff, browser parity/UI, research diagnostics, wheel-install smoke and artifact download/validation.
- **PASS — post-merge main CI:** [41143907732](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41143907732) passed all three jobs.
- **Measured improvement:** the previous master-artifact generator step took approximately 126.9 seconds; the new download plus validation took approximately 1.1 seconds. This removes roughly 126 seconds of duplicate work from the dependent job on each full CI run.
- PR [#155](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/155) merged as `3325e98b98bde6926f36c74ad76dc94fe35480b0`. No application or linguistic behavior changed.
