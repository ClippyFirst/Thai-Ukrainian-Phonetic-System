## 2026-11-06 — Ukrainian syllable-initial /j/ rule (PR #220)

| Gate | Status | Evidence / acceptance |
|---|---|---|
| Browser IPA adapter | PARTIAL — implementation present | Boundary-aware `/ja/→я`, `/je,jɛ/→є`, `/ji/→ї`, `/jo,jɔ/→йо`, `/ju/→ю`; plain `/e,ɛ/→е`, coda `/j/→й`; `/jɯ,jɤ/` remain `йи/йе`. Web Static #42243685711 SUCCESS; full CI pending. |
| Python IPA adapter parity | PARTIAL — implementation and unit cases present | Python adapter applies the same rule only at IPA start or after explicit `.`/space. Regression cases cover all mappings, plain e/ɛ, coda and boundaries. Exact-head CI #42243685764 pending. |
| Public system and methodology | DONE_IMPLEMENTED / verification pending | System page and three method documents describe the same distinction. |
| Exact-head regression/runtime parity | TODO / RUNNING | CI #42243685764 pending; Pyodide #42243685724 in progress; Web Static #42243685711 SUCCESS; Site API #42243685705 SUCCESS. |
| Independent linguistic adjudication | BLOCKED / EVIDENCE-LIMITED | Code parity is not expert gold. Independent Thai IPA and Ukrainian-native reviews remain separate gates. |

Rule contract: apply `/j/` + vowel as a Ukrainian iotated sequence only when `/j/` is syllable-initial and the boundary is explicit. Do not infer missing boundaries. Plain `/e, ɛ/` stay **е**; coda `/j/` stays **й**.

---

## 2026-11-06 — current post-merge acceptance checkpoint

This section supersedes earlier PR #215 preparation-only snapshots below. PR #216, #217, #218 and #219 are merged; the native TLTK OOV implementation and Pages smoke repair are present in main. Historical sections remain for provenance and must not be read as the current runtime state.

| Gate | Status | Evidence / acceptance |
|---|---|---|
| Native FastThaiG2P/TLTK OOV JavaScript port | DONE_VERIFIED (implementation parity) | PR #216 merged as `77a80a5e28f9b7566cb9c3ef8b11417d081d2c82`; 64/64 typed-service JSON parity in module and Worker; Chromium verifies supported OOV avoids Python, Pyodide, wheels, API and CDN. Pyodide remains a fail-closed last-resort compatibility fallback. |
| TLTK package-level rights for six shipped fallback assets | DONE_VERIFIED (source-based scope) | TLTK 1.9.1 README, setup.py/package_data, MANIFEST.in, LICENSE.txt and PyPI metadata support BSD-3-Clause for the packaged files. Preserve BSD conditions, disclaimer and no-endorsement clause; retain root LGPL-3.0 and stale 1.1.7/GPLv3 metadata as separate historical context. Not legal advice. |
| PR #217 regression anchor | DONE_VERIFIED | Merged as `533cd3f8df6112b000f5c91524f8050026b4d79a`; pinned TLTK syllable segmentation/scoring regression guard for `กขส`. Exact PR-head CI #42226080426, Pages build #42226080435 and Pyodide compatibility #42226080581 succeeded. CI: 401 passed, 1 skipped, 1,211 subtests; Ruff and wheel-install smoke passed. PR Pages deploy correctly skipped. |
| Mainline CI | DONE_VERIFIED | Merge commit `b4896bc7ad50e8e4cdb6dd8a9367cb22cbdec5e8`; main push CI #42233360770 SUCCESS; repair-branch exact-head CI #42232494753 SUCCESS. |
| Mainline GitHub Pages deployment and live smoke | DONE_VERIFIED | PR #219 merged at `b4896bc7ad50e8e4cdb6dd8a9367cb22cbdec5e8`. Main Pages run #42233360749 SUCCESS: build, deploy and post-deploy live smoke all SUCCESS. Smoke fetched the published homepage/app, native worker/modules, Pyodide worker, native/OOV manifests and data; verified SHA-256/size, TLTK 1.9.1 BSD-3-Clause metadata, third-party notices, Pyodide 0.29.5 bundle and absence of CDN dependency. Public URL: https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/. |
| Cold/warm/offline/mobile latency, transfer and memory | PARTIAL (static artifact inventory only) / TODO | Main Pages artifact #13505189970: 27,718,221 file-payload bytes; first native-analysis path 2,325,420 raw bytes (gzip-9 estimate 476,444); OOV pack 2,844,409 compressed. Existing Node segmentation diagnostic is not FastThaiG2P browser latency. Actual HTTP transfer, G2P cold/warm/offline, physical mobile and memory still require instrumented browser/device runs. |
| Manual keyboard, screen reader, zoom/reflow and device acceptance | TODO | Human test evidence required for keyboard-only, representative screen readers, 200%/400% zoom, narrow viewport/reflow, clipboard and real device checks. Static tests do not establish WCAG conformance. |
| Independent Thai IPA gold and Ukrainian adaptation review | BLOCKED / EVIDENCE-LIMITED | Independent IPA gold remains 0; accuracy remains `NOT_MEASURED`. Requires qualified Thai phonetics reviewers/adjudication and a separate Ukrainian-native review of target forms. Source annotations and Python/JS parity are not expert gold. |

### Branch and PR consolidation

- Default branch remains `main`; starting HEAD was `9f279ce04c14b81fa4728a15e81fb89ab046b753`; PR #219 is merged to main as `b4896bc7ad50e8e4cdb6dd8a9367cb22cbdec5e8`.
- PRs #211–#214 and #216–#218 that represent the current site redesign, Ukrainian-first UX, native front-half, native TLTK OOV, parity follow-up and documentation checkpoints are merged into main.
- PR #215 is an obsolete preparation PR: its head `5fd73a4abb489ac43b2531abcdb86a026ac6e48c` is an ancestor of the merged PR #216 branch head (74 commits later). Its work is superseded by #216; PR #215 was closed as superseded after this reconciliation, retaining its source branch as history.
- The ten extant non-main refs are retained source/history refs (including merged PR branches and the repair branch). The canonical working branch is `main`; do not force-update or bulk-delete historical refs. The divergent `docs/repository-audit-2026-11-04` branch remains 503 ahead/23 behind and is not safe to merge wholesale. `docs/repository-audit-2026-11-04` remains highly divergent (503 commits ahead and 23 behind main at this audit) and must not be wholesale-merged; retain it and port only a separately evidenced missing change.
- PR #219 (`fix/pages-smoke-and-audit-consolidation-2026-11-06`) passed exact-head CI #42232494753, was merged, and its main-push Pages deployment/live smoke #42233360749 passed. The repair branch is no longer the active work branch; continue from `main`.

---


## 2026-11-06 follow-up — Pages and TLTK package rights

| Item | Status | Evidence / next acceptance |
|---|---|---|
| Live GitHub Pages native-first content and assets | PARTIAL_VERIFIED | Live HTTP fetches confirmed homepage, app.js, native Worker/module, native manifest and all five declared native data assets, bundle manifest, system page and legal notices. This proves current public content/asset reachability, not the corrected post-deploy SHA smoke or native OOV runtime. |
| Pages deployment smoke | PARTIAL_IMPLEMENTED | Fixed stale pre-recomposition string assertions; now checks current native-first UI, both workers, native and OOV manifests/data hashes, legal notices, and retained Pyodide assets. Added PR build trigger while deploy remains main-only. Requires successful PR Pages build and post-merge main deployment smoke. |
| TLTK 1.9.1 fallback package rights | DONE_VERIFIED | Pinned README 1.9.1, setup.py version/license/package_data, MANIFEST.in, LICENSE.txt and PyPI 1.9.1 metadata support BSD-3-Clause for the six packaged fallback assets. Root LGPL-3.0 notice and stale PKG-INFO 1.1.7/GPLv3 are retained as historical/repository context. BSD notice, conditions, disclaimer and no-endorsement clause must be preserved. |
| TLTK fallback source/asset mapping | DONE_VERIFIED | Five files byte-identical; sylform_var.pkl is exact BZip2 decompression of TLTK sylform_var.pklz. |
| Native OOV data extraction | PARTIAL | Deterministic CP874/pickle-to-JSON/gzip build extractor added. It includes the five data tables used by g2p() -> sylparse() -> wordparse(), and excludes sylform_var.pkl because SYLVAR has no reads in that call path. Parser constants are extracted from the pinned BSD parser source AST. |
| Native JavaScript OOV algorithm | TODO | No JS TLTK parser has been integrated yet. The data pack is preparatory only and is not used by the public UI. Keep Pyodide OOV fallback. Acceptance: complete raw IPA and full typed service JSON parity against pinned Python for a multi-case OOV fixture set, then real browser Worker parity and lazy-load/hash checks. |

---

## Post-merge execution checkpoint — PR #214 integrated (2026-11-06)

| Work item | Status | Evidence / remaining acceptance |
|---|---|---|
| PR #214 native-first FastThaiG2P browser port | DONE_VERIFIED (PR-head engineering gates) | Squash-merged to main as `29b63b8f58db1f6d7ff068d131df0b0759895115`. Exact final PR head `0d4503ed55ff726807917e2cfbf14c0ad30eb624`: Full CI #42199395072, Web Static #42199395225, Site API #42199395069 and Pyodide compatibility #42199395284 all SUCCESS. Full CI: 399 passed, 1 skipped, 1,211 subtests passed; Ruff passed. The one skip was optional `tests/test_fastthaig2p_site_api.py` (FastAPI absent from generic CI), separately covered by the successful Site API workflow. Post-merge main push CI/Pages deployment still require independent verification. |
| Native-first UI stale-response test correction | DONE_VERIFIED | Test-only microtask flush and callback assertion in `37e0ee6b6fb1385bd4c98bfdd582d8eee3dac5c1`; final exact-head suite passed. |
| Browser-native TLTK OOV algorithm | BLOCKED / PARTIAL | Full native OOV parity not implemented. TLTK BSD-3-Clause metadata/LICENSE.txt conflicts with LGPL-3.0 root LICENSE and stale GPLv3 PKG-INFO. Keep Pyodide OOV fallback and do not bundle TLTK assets/code until file-level rights are resolved. |
| Mainline Pages deployment after PR #214 | BLOCKED / NOT VERIFIED | PR-head tests passed, but post-merge Pages workflow and live smoke were not accessible through the available commit-run lookup. Verify main push CI, Pages deployment and deployed assets before claiming the hybrid UI is live. |
| Native cold/warm/offline/mobile performance and memory | TODO | Measure actual same-origin transfer, first-use/cached latency, offline reload and memory on desktop/mobile. No speedup claim. |
| Manual accessibility acceptance | TODO / DEFERRED_UNVERIFIED | Keyboard-only, screen-reader, 200%/400% zoom/reflow, real clipboard and screenshot/visual review require human/browser testing. Static tests do not prove WCAG conformance. |
| Independent linguistic validation | BLOCKED / EVIDENCE-LIMITED | Independent IPA gold = 0; accuracy = `NOT_MEASURED`; Ukrainian candidates remain provisional. Requires qualified independent Thai reviewers/adjudicator and Ukrainian-native target review. |
| Branch consolidation | DONE_VERIFIED for active PR work; historical refs preserved | PR #210–#214 are integrated. The audit branch remains preserved because it is 503 commits ahead/8 behind and includes older code; no whole-history merge or branch deletion. |

### Mainline and branch disposition

- `main`: default and active integration branch; PR #214 merge commit `29b63b8f58db1f6d7ff068d131df0b0759895115`.
- `design/site-recomposition-2026-11-05`: integrated by PR #211; historical source ref retained.
- `docs/post-211-pages-verification-2026-11-06`: integrated by PR #212; historical source ref retained.
- `feat/ukrainian-first-ux-2026-11-06`: integrated by PR #213; historical source ref retained.
- `feat/fastthaig2p-native-ts-port-2026-11-06`: integrated by PR #214; historical source ref retained.
- `docs/repository-audit-2026-11-04`: preserved, 503 ahead/8 behind; no wholesale merge.

The branch list still contains historical refs because no user branch was deleted. The single active development/integration line is `main`.

---

## Current execution checkpoint — branch consolidation and native-first port (2026-11-06)

| Work item | Status | Evidence / next acceptance |
|---|---|---|
| Existing repository documentation architecture | DONE_VERIFIED | `AGENTS.md`, `docs/README.md`, `scripts/README.md`, architecture, validation matrix, audit, schemas, provenance and generated-artifact ownership already exist. Preserve and maintain these canonical sources; do not create a duplicate documentation system. |
| PR #211 site redesign | DONE_VERIFIED | Merged to `main` as `476cb6ed0e4421ab02bb564ff232c99b6c19e008`; exact-head CI/Web Static/Site API/Pyodide checks passed on the tested PR head. |
| PR #212 post-merge documentation reconciliation | DONE_VERIFIED | Closed after documentation reconciliation; its content is represented in mainline history. |
| PR #213 Ukrainian-first UX and localized diagnostics | DONE_VERIFIED | Merged to `main`; commit `f7ce29d6bbae03a8d5a8d03e8c09dbbd5dd01662`. |
| PR #214 browser-native FastThaiG2P port | PARTIAL — exact-head verification in progress | Latest code/test commit `37e0ee6b6fb1385bd4c98bfdd582d8eee3dac5c1`. Web Static #42198840129 and Site API #42198840133 passed. Full CI #42198840130 and Pyodide compatibility #42198840192 were still running at checkpoint. Merge only after both pass and PR diff is reviewed. |
| PR #214 stale-response UI regression fixture | DONE_VERIFIED (fix committed; rerun checks pending) | Initial CI/Web Static/Site API all exposed `TypeError: deferredNativeWorkerResponse is not a function`. Root cause was test timing across the native-ready promise microtask. Commit `37e0ee6` flushes the microtask and asserts callback installation before delivery; no production code changed. |
| Native TLTK OOV implementation and rights | BLOCKED / PARTIAL | Rights scope is conflicting (BSD-3-Clause package metadata/LICENSE.txt vs LGPL-3.0 repository LICENSE and stale GPLv3 PKG-INFO). Keep native OOV code/data out of the browser bundle until file-level distribution scope is cleared; retain Pyodide fallback. |
| Desktop/mobile cold/warm/offline performance and memory | TODO | Measure transferred bytes, cold/warm latency, caching, offline reload and memory on real desktop/mobile browsers. Do not infer a speedup from avoiding Pyodide on dictionary hits. |
| Manual accessibility acceptance | TODO / DEFERRED_UNVERIFIED | Keyboard-only, screen reader, 200%/400% zoom/reflow, real clipboard and visual review require human/browser testing; static checks are not WCAG conformance evidence. |
| Independent linguistic validation | BLOCKED / EVIDENCE-LIMITED | Independent IPA gold rows = 0; accuracy = `NOT_MEASURED`; Ukrainian candidates remain provisional. Requires qualified Thai reviewers/adjudicator and independent Ukrainian target review. |
| Branch consolidation | PARTIAL | PR #211/#212/#213 and prior PR #210 work are already integrated in main. PR #214 is pending. The 503-ahead divergent audit branch is preserved, not wholesale-merged. Historical source branches are not deleted or rewritten. |

### Current branch disposition

- `main`: current default branch; starting audited HEAD `f7ce29d6bbae03a8d5a8d03e8c09dbbd5dd01662`.
- `design/site-recomposition-2026-11-05`: content integrated by PR #211; source ref retained.
- `docs/post-211-pages-verification-2026-11-06`: content integrated by PR #212; source ref retained.
- `feat/ukrainian-first-ux-2026-11-06`: content integrated by PR #213; source ref retained.
- `feat/fastthaig2p-native-ts-port-2026-11-06`: active PR #214; 129 commits ahead, 0 behind main at checkpoint.
- `docs/repository-audit-2026-11-04`: 503 commits ahead, 7 behind; preserve without wholesale merge because the history is divergent and earlier audit explicitly rejected it.

A branch existing on GitHub is not proof its work is absent from main. Do not re-merge squash-integrated work or delete historical branches merely to make the branch list shorter.

---

## Post-merge verification update — 2026-11-06

- `main` now contains PR #211 at merge commit `476cb6ed0e4421ab02bb564ff232c99b6c19e008`.
- Exact PR-head verification (`8200255df8d7c2cfb4f8aa30d218785e9a625b08`): Full CI [42117563464](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42117563464), Web Static [42117563510](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42117563510), Site API [42117563500](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42117563500), Pyodide compatibility [42117563482](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42117563482): all SUCCESS.
- Post-merge Pages workflow [42120159047](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42120159047) was `in_progress` at the latest check. Live deployment and its post-deploy smoke assertions remain NOT VERIFIED.
- Manual acceptance remains open: keyboard/screen-reader, 200%/400% zoom and narrow reflow, real clipboard, screenshot review, mobile cold/warm performance. Do not infer WCAG conformance from static checks.
- Linguistic evidence remains unchanged: independent IPA gold = 0, accuracy `NOT_MEASURED`, Ukrainian candidates provisional. See [current handoff](MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md).

---

## Current Pages beta and UI/UX checkpoint — 2026-11-05

- Default branch remains `main` at `f0d41996e854185bd6bd92f0ffa8f6b83e71f777`; the previously published research beta remains live. This PR does not modify main or deployment settings.
- Dedicated branch `design/site-recomposition-2026-11-05`, exact tested HEAD `d5c880a082ae553bf944d31f6d341f38f33690c8`; PR [#211](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/211) is OPEN, mergeable and not merged. The supplied audit branch was inspected and preserved; its divergent history was not imported.
- Exact-head Full CI [42110596982](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42110596982) SUCCESS: test, wheel-install-smoke and master-artifact all passed. Test job: **398 passed, 1 skipped, 1,211 subtests passed**; Ruff passed; 29 Python/browser parity fixtures passed; generated-artifact, evidence, TextGrid, packaging and research diagnostics completed.
- The single generic-CI skip is `tests/test_fastthaig2p_site_api.py` because FastAPI is optional and absent in that environment. Dedicated Site API [42110596971](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42110596971) SUCCESS.
- Exact-head Web Static [42110596991](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42110596991) SUCCESS. Exact-head Pyodide compatibility [42110597073](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42110597073) SUCCESS, including CPython/Pyodide parity, Pages bundle build and same-origin Worker smoke in Chromium.
- UI contract verifies explicit analysis, example fill without auto-run, stale-output invalidation, fail-closed engine behavior, Ukrainian-first/IPA-second outputs, progressive detail, and discarding a delayed Worker response after input changes.
- Documentation aligns public Pages/Pyodide architecture, legal/publication status, UI requirements, audit and handoff. The UI redesign remains isolated in PR #211; it is not deployed until merge and a successful Pages deployment.
- Manual gates remain PARTIAL/NOT VERIFIED: keyboard-only and screen-reader use, 200%/400% zoom and narrow viewport visual reflow, actual browser clipboard interaction, deployed mobile cold/warm performance. Automated source checks are not a WCAG conformance audit. No screenshot-based visual review of the PR branch was available.
- Linguistic evidence unchanged: independent IPA gold = 0; accuracy = `NOT_MEASURED`; Ukrainian candidates remain provisional. No phonological rules, corpus labels, gold status or linguistic claims changed.
- Upstream UI UX Pro Max, Superpowers, Matt Pocock skills, Ponytail and Unlazy were reviewed selectively. No upstream code, skills, hooks, frameworks, CSS libraries or runtime dependencies were installed.
- Release posture: **engineering-verified UI beta candidate; not yet deployed; not a linguistic validation release**.

---

## Current verified checkpoint — 2026-11-05 (text-only scope)

- Branch `docs/repository-audit-2026-11-04`, HEAD `2ce66a5ace012675c0d9fea06aca5ae962003092`; base `main` HEAD `56fba86b4b8be2fe4e67284355e9928108527387`. PR [#210](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/210) is OPEN, mergeable, and not merged. No mainline mutation, branch deletion, force-push, or release.
- Exact-head Full CI [42040828931](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42040828931) passed all three jobs (`test`, `wheel-install-smoke`, `master-artifact`). Dedicated Site API [42040828955](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42040828955) and optional external G2P smoke [42040829124](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42040829124) also passed. Local tests were not run in this connector-only session.
- Supplied text-only archives: CCOST 488/488 TextGrids and LOTUSDIS 90/90 TextGrids parse. CI exports 178,377 orthographic intervals (CCOST 145,434; LOTUSDIS 32,943). The reviewed worklist has 1,975 rows; all 11 reviewer/adjudicator fields are blank. CI asserts `audio_members_read=0`; no audio was read, extracted, hashed, or required.
- CCOST worklist: `_8` appears 868 times at tier level (397 exact file/interval groups; 438 file/interval/raw-label events; 22 strings; 119 files). Generic MAUS permits suffixes `_1`–`_9`, but the CCOST paper maps only `_1`–`_5`; `_8` remains unmapped for CCOST and is not guessed. Unknown markers `<P>`, `<P:>`, `<:p>`, `<Fail>` remain fail-closed; `<notProcessedChunk>` is a documented processing failure, not a phone.
- **Owner scope:** text and phonetic transcription only. Global TIMIT acquisition and all audio/acoustic work are DEFERRED/OUT OF SCOPE. Broad-phonemic text-based review remains possible; narrow surface/acoustic claims are not in scope.
- **Remaining evidence gates:** two independent qualified Thai reviewers plus a separate adjudicator; independent Ukrainian-native target-form review; authoritative CCOST-specific clarification/recovery for unresolved markers and `_8`; resolve CCOST controlled-wordlist A–D discrepancy; hands-on accessibility review. FastThaiG2P optional dependency use is permitted with notices; bulk vendoring of mixed dictionary/TLTK fallback data remains restricted by component-level provenance/licensing.
- **Readiness:** ENGINEERING_VERIFIED_RESEARCH_PROTOTYPE_NOT_LINGUISTICALLY_RELEASE_READY. CI proves software/packaging contracts, not pronunciation accuracy. Independent IPA gold rows remain 0; linguistic accuracy remains NOT_MEASURED.

This checkpoint supersedes earlier chronological notes that say CCOST TextGrids were unavailable, that the TextGrid parser had not been tested against the supplied archives, or that audio acquisition was an active acceptance gate. Those entries remain as historical records only.

---

## Public-source clarification checkpoint — 2026-11-05

- Branch: `docs/repository-audit-2026-11-04`; work remains on PR #210, no mainline mutation.
- CCOST tier suffixes are now **DONE_VERIFIED** from the BAS WebServices tutorial: `ORT-MAU` = MAUS-tokenized word segmentation; `KAN-MAU` = canonical X-SAMPA word pronunciation; `KAS-MAU` = G2P phonological syllable segmentation. The earlier curator blocker for `-MAU` is closed.
- `<notProcessedChunk>` is now **DONE_VERIFIED** as a MAUS dummy segment inserted when a chunk could not be processed; likely causes include transcript/signal mismatch or a chunk too short for its expected phone sequence. It is not a phone/IPA label. `<P>`, `<P:>`, `<:p>`, and `<Fail>` remain unresolved. `_8` is permitted by generic BAS/MAUS tone syntax (`_1`–`_9`) but is unmapped in the CCOST paper's five-category scheme (`_1`–`_5`); its CCOST-specific meaning remains unknown and fail-closed. The public CCOST manual was text-extracted and searched; it contains no definition for `_8` or those four tag spellings.
- FastThaiG2P source-code use remains **PERMITTED** under the pinned Apache-2.0 grant with NOTICE. The browser wheel now isolates the Wiktionary subset under CC BY-SA 4.0 and excludes generated/manual/unknown IPA. TLTK fallback asset transformations are verified, but the parser header says 1.3.8/BSD-3 while the data-source repository snapshot says setup.py 1.9.1/BSD-3 and contains root LGPL-3, module BSD-style LICENSE.txt and stale 1.1.7/GPLv3 PKG-INFO. Full bundle redistribution remains **BLOCKED** pending file-level TLTK license-scope review and owner approval.
- Sources: [BAS tier tutorial](https://clarin.phonetik.uni-muenchen.de/BASWebServices/help/tutorial), [BAS chunk failure FAQ](https://clarin.phonetik.uni-muenchen.de/BASWebServices/help/help_examples), [FastThaiG2P data README](https://github.com/awslabs/FastThaiG2P/blob/4e82a291b4cf2876326744c6580121e9986ad354/data/README.md), [FastThaiG2P merge script](https://github.com/awslabs/FastThaiG2P/blob/4e82a291b4cf2876326744c6580121e9986ad354/scripts/merge_ipa.py), [TLTK package metadata](https://github.com/attapol/tltk/blob/master/setup.py), [TLTK BSD notice](https://github.com/attapol/tltk/blob/master/LICENSE.txt).

---

## Latest exact-head repository verification — 2026-11-05

- Branch: `docs/repository-audit-2026-11-04`; documentation checkpoint HEAD: `45bbd7386ede98c6fa63b015c9c7a303c436e699`; implementation checkpoint: `f9b6baf1ad3c55057051ff5652ac7827a06fd7c1`; base `main`: `56fba86b4b8be2fe4e67284355e9928108527387`; comparison at this checkpoint: **137 commits ahead, 0 behind**.
- PR [#210](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/210) is **OPEN, not merged**, targets `main`, and is mergeable. No mainline change, force-push, branch deletion or release was made.
- Exact-head Full CI [run 42018381197](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42018381197) succeeded on the documentation checkpoint HEAD. Jobs `test`, `wheel-install-smoke`, and `master-artifact` all passed. The test job reports **385 passed, 1 skipped, 1,206 subtests passed**; Ruff passed; 29 Python/browser parity fixtures passed; generated-artifact drift checks, source/reviewer packet validators, archive inspection, JSONL export, and artifact upload passed.
- The one skip is `tests/test_fastthaig2p_site_api.py` in the generic environment because FastAPI is optional and absent there. Dedicated FastThaiG2P Site API [run 42018381263](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42018381263) passed; optional external Thai G2P smoke [run 42018381361](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42018381361) passed.
- CI re-inspected 578/578 supplied TextGrid files and verified 178,377 orthographic JSONL rows (CCOST 145,434; LOTUSDIS 32,943). The current `textgrid-text-only-jsonl` artifact is [available from run 42018381197](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42018381197/artifacts/13411240199), 12,609,560 bytes, artifact digest `sha256:260ff20858e588f78152fdfb01d969f7160fbfc530ed2a8945758f80ee3c0fcb`. It contains text-only exports, manifest and notices; no audio is read or included.
- Linguistic status is unchanged: independent IPA gold rows **0**; accuracy **NOT_MEASURED**. The CCOST adapter remains PARTIAL with 1,014 unsupported labels; `_8`, Unicode IPA-looking strings, unusual sequences and mixed marker/text labels remain fail-closed.
- Current blockers: CCOST curator clarification of `-MAU` aliases and unsupported labels; two qualified independent Thai reviewers plus adjudicator; independent Ukrainian-native target review; hands-on accessibility review; FastThaiG2P bundled-data rights and Python-host preview. Global TIMIT and audio tasks remain DEFERRED/EXCLUDED by owner decision.
- Local tests were not run in this connector-only session. The exact-head GitHub Actions evidence above is the verification record; no local checkout or local test execution is claimed.
- Readiness: **ENGINEERING_VERIFIED_RESEARCH_PROTOTYPE_NOT_RELEASE_READY**. Software/packaging/CI gates pass, but independent linguistic and human accessibility gates remain unmet.


---

## Current checkpoint — 2026-11-05: CCOST text-only adapter implementation

- Work branch: docs/repository-audit-2026-11-04; keep all changes on this single branch and PR #210. No main merge or new branch.
- Global TIMIT is EXCLUDED by owner decision; audio is OUT OF SCOPE.
- Added strict X-SAMPA→IPA converter, CCOST tier-aware TextGrid reader, typed provisional IPA boundary, synthetic regression tests, and a local text-only inspection script. No CCOST archive/audio or source labels were downloaded.
- CCOST TextGrid-only export is BLOCKED pending curator response. A request is prepared but NOT SENT because no email action is connected. The public Zenodo file list exposes one mixed 6.2 GB WAV+TextGrid ZIP and no TextGrid-only archive.
- The parser currently supports Praat long-text TextGrid only. Real release encoding and MAU/MAS/KAS/KAN symbol inventory remain unverified. Unknown X-SAMPA fails closed.
- Exact-head CI [41992116524](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41992116524) passed after correcting the stale Global TIMIT registry assertion and the X-SAMPA diacritic/boundary fixture. Results: 376 passed, 1 skipped, 1,206 subtests; Ruff, wheel-install smoke and master-artifact passed.
- Local tests are not available in the connector-only environment. Linguistic accuracy remains NOT_MEASURED; independent IPA gold rows remain 0.

### Task ledger
| Task | Status | Acceptance / blocker |
|---|---|---|
| Global TIMIT | DEFERRED | Explicitly excluded; no further acquisition |
| X-SAMPA→IPA converter | PARTIAL | Synthetic tests and exact-head CI; verify against actual CCOST tier labels before corpus use |
| Praat long-text TextGrid parser | PARTIAL | Synthetic fixture tests; actual CCOST encoding unverified |
| CCOST TextGrid-only export | BLOCKED | Curator must provide export or confirm a lawful text-only extraction method |
| CCOST phonetic gold | BLOCKED | Two independent qualified Thai reviewers plus adjudication; CCOST annotations alone are not independent gold |
| LOTUSDIS | OPTIONAL / PARTIAL | Orthographic text context only; no audio |

---

## User decision — 2026-11-05: Global TIMIT excluded; text-only sources prioritized

The project owner has decided to **exclude Global TIMIT Thai (LDC2022S13)**. Do not pursue LDC access, fees, agreements, audio, or derived labels. Its phone/tone reference role is not a project dependency; alternatives are CCOST text annotations plus selectively reusable, provenance-separated FastThaiG2P/Wiktionary candidates. This is a scope decision, not a claim that Global TIMIT is low quality.

**Active source roles**
- **CCOST — PRIMARY phonetic-text candidate (PARTIAL):** obtain TextGrid-only export/manual; inspect actual MAU/MAS tier instances; implement and test X-SAMPA → typed IPA conversion; independently review a stratified subset. No audio.
- **FastThaiG2P — SUPPORTING lexical/IPA candidates (PARTIAL):** reuse Apache-2.0 code with NOTICE and only the separately licensed Wiktionary-derived subset after source/version attribution. Generated IPA and undocumented manual overrides remain provisional, never gold. Do not redistribute TLTK data until file-level rights are clarified.
- **LOTUSDIS — OPTIONAL orthographic/context corpus (PARTIAL):** conversational vocabulary and text robustness only; not phonetic gold. Audio-specific tasks are OUT OF SCOPE.
- **Global TIMIT — DEFERRED/EXCLUDED by owner decision:** no further acquisition or legal-access work.

**Next acceptance gates:** (1) request CCOST TextGrid-only files and manual; (2) inspect tier values and encoding, not just the published tier names; (3) build a documented X-SAMPA mapping with round-trip/edge-case tests and typed IPA preservation; (4) curate a legally attributable Wiktionary subset separately from generated FastThaiG2P rows; (5) decide whether LOTUSDIS text is useful after inspecting its actual text schema. Do not add corpus rows or claim linguistic accuracy until provenance and review gates pass.

## Previous checkpoint — 2026-11-05 (superseded by CCOST adapter batch)

- Branch `docs/repository-audit-2026-11-04`; base `main` `56fba86b4b8be2fe4e67284355e9928108527387`; compare: **26 commits ahead, 0 behind**.
- PR #210 remains **OPEN / NOT MERGED**. Latest branch head `3b18a3b35a35c0573cadc2d81cdbcbd455b85a91` exact-head Full CI [41986104461](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41986104461) completed successfully: `test`, `wheel-install-smoke`, and `master-artifact` all passed.
- CI covered Ruff, generators/drift, source/reviewer/blind-packet validators, full pytest, Python/browser parity, IPA→Ukrainian adapter, UI/accessibility contracts, segmentation diagnostics, and isolated wheel install. Local tests were not run in the connector-only environment.
- Linguistic accuracy remains `NOT_MEASURED`; independently adjudicated IPA gold rows: **0**. Status: engineering-verified research prototype, not linguistically release-ready.

---

## Latest exact-head reconciliation — 2026-11-03 (PR #189)

- Current branch HEAD `d9958db0e877944e5a75183c053681cdbdd525dc`; compare against `main`: **144 commits ahead, 0 behind**. Base `main` remains `75c331f69aa3c8e5b4db3ccc5a6da85124600a01`. PR [#189](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/189) remains open as Draft.
- Exact-head Full CI [41714533758](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41714533758) completed successfully; all three jobs passed: `test`, `wheel-install-smoke`, and `master-artifact`. Exact-head Web Static [41714533792](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41714533792) passed. External VISTEC segmentation evaluation [41714533797](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41714533797) passed.
- The superseded push-triggered CI run [41714525970](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41714525970) was cancelled; the PR-triggered exact-HEAD run above passed.
- Relative to runtime/workflow checkpoint `69d56b52b7f687948cac4250e4c7eb98e86ab67f`, the only source-file follow-up is docstring-only commit `ac603c4ae96bf6ffbc8f2edb095b4f2375d57ce5`; other follow-ups are audit/research documentation. No parser, IPA, Ukrainian-adaptation, segmentation behavior or public API change is introduced by this reconciliation.
- The latest audit correction deliberately sets unavailable internal artifact SHA-256 values to `null`; only independently verified archive SHA-256 values remain recorded. Do not infer an inner JSON hash from a ZIP hash.
- Wisesight (993 rows) and VISTEC (50,000 rows) remain source-annotated diagnostics with **0 expert-adjudicated rows**. Dictionary max-match Wisesight boundary F1 is **0.847036** with **204/993** exact sequences; TUD is **0.748623** with **119/993**. These are source-label diagnostics, not independent accuracy. Linguistic accuracy remains `NOT_MEASURED`.
- Remaining acceptance gates: independent Thai segmentation/phonetic reviewers and adjudication; independent Ukrainian-native target-form review; CCOST A–D curator clarification and lawful TextGrid/archive inspection; immutable LOTUSDIS audio objects, hashes and clean-interval provenance; hands-on keyboard, screen-reader, zoom/reflow and mobile accessibility review.
- Local tests were not run in this connector-only environment. Exact-head GitHub Actions are the available verification evidence. Readiness remains **engineering-verified research prototype**, not release-ready for linguistic accuracy or full WCAG 2.2 AA claims.
- This reconciliation is based on exact-head CI/Web Static/VISTEC results for `d9958db0e877944e5a75183c053681cdbdd525dc`. The documentation-only reconciliation commit created from it requires its own exact-head CI; no result is inherited automatically.

---

## Current branch reconciliation — 2026-11-03 (Thai orthographic cluster boundary fix)

- Repository: ClippyFirst/Thai-Ukrainian-Phonetic-System. Default branch main remains at 75c331f69aa3c8e5b4db3ccc5a6da85124600a01; this continuation did not modify main.
- Work branch: fix/benchmark-error-clusters-20261102; Draft PR #189 remains open. Latest verified runtime/workflow checkpoint: 69d56b52b7f687948cac4250e4c7eb98e86ab67f; follow-up ac603c4ae96bf6ffbc8f2edb095b4f2375d57ce5 only clarifies the segmentation function docstring. This register refresh does not change runtime behaviour.
- Exact-head verification of the runtime/workflow state: Full CI 41711547837 passed all three jobs; Web Static 41711547920 passed; External VISTEC 41711547913 passed. The docstring-only follow-up and this documentation refresh are separately checked by the branch's exact-head Actions runs.
- Full suite: Ruff All checks passed; pytest 328 passed, 1,192 subtests passed. Generated-table drift, 351,780-row master artifact, source/reviewer and blind-packet validators, 42-input runtime diagnostics, IPA-to-Ukrainian adapter, Python/browser parity, UI/accessibility contracts, browser latency diagnostic, Wisesight segmentation diagnostics, source-attested IPA checks, TUD held-out diagnostics, manual-review sample checks, and isolated wheel installation all passed.
- Wisesight-1000: 993 CC0-1.0 test rows, all source-annotated and 0 expert-adjudicated. Dictionary max-match: boundary F1 0.847036, precision 0.833461, recall 0.861061, 2,390 false splits, 1,930 false merges, 204/993 exact token sequences (20.54%). TUD unigram Viterbi on the same rows: F1 0.748623, 8,722 false splits, 363 false merges, 119/993 exact sequences. Diagnostic comparison against source labels, not independent accuracy.
- VISTEC: 50,000 immutable source-annotated rows, 0 expert-adjudicated. Dictionary max-match boundary F1 0.832767 (77/50,000 exact sequences); TUD Viterbi F1 0.753023 (16/50,000). This is source-label evaluation, not expert gold. Preserve upstream README's 49,997-sample versus pinned CSV's 50,000-row discrepancy.
- The fix aligns Python segmentation with the browser engine for Thai postposed vowel letters U+0E30, U+0E32 and U+0E33. Regression tests cover กะ, กา, กำ, เกะ, ก่า, เก่า and the coda-boundary control กาก. No dependency or new segmentation model was added.
- Research review: four full texts were inspected for Thai segmentation/G2P evidence. Orthographic syllables can constrain candidate word boundaries but do not determine lexical words; segmentation is context-sensitive; domain shift and OOV vocabulary matter. TUD remains research-only; dictionary max-match remains the conservative default.
- Current engineering state remains an engineering-verified research prototype, not release-ready for independent linguistic accuracy. Remaining external gates: independent Thai segmentation/IPA reviewers and adjudication, independent Ukrainian-native target judgments, CCOST A-D curator clarification and lawful TextGrid/archive inspection, immutable LOTUSDIS audio provenance, and hands-on keyboard/screen-reader/zoom/reflow/mobile accessibility review.

---

## 2026-11-03 — Thai orthographic cluster-boundary correction and evidence refresh

| Work item | Status | Evidence | Remaining acceptance |
|---|---|---|---|
| Python Thai postposed-vowel cluster boundaries | DONE_VERIFIED | TDD RED on dd58b9adc3a92d40a54e3d26d661ce28ebcb7c7d: seven new boundary subtests failed for the expected split. Minimal fix commits dc9c292a213f7e38a20e10ae3f3730ecf34d408f and fb564db7fe9988b9a5885ed9cd4ceb1a5436654b add U+0E30/U+0E32/U+0E33 to cluster continuations and update all uses. Tests cover กะ, กา, กำ, เกะ, ก่า, เก่า and กาก. | No further runtime acceptance; broader syllabification is a separate linguistic task. |
| Wisesight diagnostic snapshot and CI evidence gate | DONE_VERIFIED — source-annotation diagnostic only | Dictionary exact sequences increased from 192 to 204/993; boundary F1 0.847036, precision 0.833461, recall 0.861061, 2,390 false splits and 1,930 false merges. Test snapshot and CI assertion both updated to 204. Full CI 41711547837 passed. | 993 labels remain source-annotated, 0 independently adjudicated; do not call this accuracy. |
| Same-row dictionary vs TUD comparison | DONE_VERIFIED — diagnostic only | Same 993 Wisesight rows: dictionary F1 0.847036 / 204 exact; TUD F1 0.748623 / 119 exact. Both error classes and provenance gates passed; comparative artifact 13267884921. | Keep TUD research-only; human review and independent segmentation gold remain required. |
| External VISTEC evaluation | DONE_VERIFIED — source-annotation diagnostic only | Run 41711547913 passed; 50,000 pinned rows; dictionary F1 0.832767 / 77 exact, TUD F1 0.753023 / 16 exact; artifact 13267463783. | 0 expert-adjudicated rows; preserve README 49,997 vs CSV 50,000 discrepancy. |
| Thai segmentation literature review | DONE_VERIFIED — research synthesis | Full-text reads of Boo20, Cho20, Lim21 and Yam22 plus Aroonmanakun 2007; see docs/research/thai-g2p-evaluation-literature-2026-11-03.md. | LST20 and VISTEC labels are not independent gold; license/annotation gates remain. |
| Third-party engineering-method review | DONE_VERIFIED — process guidance only | Pinned Superpowers, Matt Pocock skills and Ponytail README/TDD/implementation/review revisions inspected. Applied TDD, vertical-slice testing, minimal diffs and review of the changed call path. | No third-party skill code or dependency imported. |

## Current branch reconciliation — 2026-11-03 (authoritative checkpoint)

- Repository: `ClippyFirst/Thai-Ukrainian-Phonetic-System`; base `main` remains `75c331f69aa3c8e5b4db3ccc5a6da85124600a01`.
- Current branch: `fix/benchmark-error-clusters-20261102`; current verified tip before this documentation-only reconciliation: `e7ebb28e64afd5ec70fc136a12d6723ccebdd59e`. GitHub compare reports **110 commits ahead, 0 behind** main.
- PR [#189](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/189) remains open as Draft; no merge, force-push, main update, or release was performed.
- Exact-tip Full CI [41643230493](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41643230493) completed successfully: `test`, `wheel-install-smoke`, and `master-artifact` all passed. The test job log confirms Ruff **All checks passed**, pytest **327 passed / 1,185 subtests passed**, and Python/browser parity **29 fixtures passed**. Generated-artifact drift, source/reviewer/blind-packet validators, runtime and segmentation diagnostics, IPA→Ukrainian adapter, isolated wheel install, and master artifact validation passed. Web Static [41643230575](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41643230575) passed.
- This supersedes older branch-head counts and pending-verification notes in the historical entries below. Older SHA/run references are retained as historical evidence, not current status.
- Local tests were not run in the connector-only environment. Linguistic accuracy remains `NOT_MEASURED`; independent Thai phonetic/segmentation adjudication, independent Ukrainian-native target review, CCOST release-archive/tier reconciliation, LOTUSDIS immutable audio evidence, and hands-on WCAG review remain external acceptance gates.
- Readiness: **engineering-verified research prototype**, not release-ready for linguistic-accuracy or full WCAG 2.2 AA claims.

---

## 2026-11-03 — per-token diagnostic completeness guard and exact-head verification

| Work item | Status | Evidence | Remaining acceptance |
|---|---|---|---|
| Runtime diagnostic completeness guard | DONE_VERIFIED | Added a regression test proving that a resolved Thai token with an empty syllable list must prevent the text from being counted as complete. Test-first RED: CI run [41640676532](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41640676532) failed only on the new assertion (1 failed, 326 passed, 1,185 subtests passed). Minimal fix committed as `94eaadb5bda2318dfa864eee7dae1b3715b70374`. | None for this diagnostic invariant. The check is internal to the runtime report and does not alter parser, IPA, Ukrainian adaptation or public API behaviour. |
| Exact code-head verification | DONE_VERIFIED | On `94eaadb5bda2318dfa864eee7dae1b3715b70374`: Full CI [41641516453](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41641516453) passed all three jobs (`test`, `wheel-install-smoke`, `master-artifact`); Web Static [41641516658](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41641516658) passed. Ruff passed; pytest **327 passed, 1,185 subtests passed**; browser parity **29 fixtures** passed; source/reviewer/blind-packet validation, generated-artifact drift, IPA→Ukrainian adapter, diagnostics, isolated wheel installation and master artifact passed. | Local execution remains unavailable in this connector-only session; no local pytest/npm result is claimed. |
| Academic Writing Toolkit recheck | PARTIAL — parser limitations recorded | British-English checker flagged only `Modeling`, which is part of the exact published title and must remain unchanged. Paragraph review flagged two one-sentence “Full-text findings” labels; they are intentional section cues, not prose defects. Harvard citation audit still reports unmatched Yamasaki/Rugchatjaroen source-note pairs despite correctly formatted Source lines; DOI bibliography and source links were manually inspected. | Do not distort published titles or rewrite sound bibliography entries merely to satisfy parser false positives. Automated citation consistency is NOT_CLEAN, not passed. |
| Engineering-method references | DONE_REVIEWED_APPLIED_SELECTIVELY | Applied Superpowers’ test-first/verification discipline, Matt Pocock’s behaviour-focused test and seam guidance, and Ponytail’s dataflow-first, minimum-complete-diff review. | No external skills, hooks, code or dependencies were copied or installed. No independent subagent reviewer is available in this connector-only environment. |
| Open-PR and branch reconciliation | DONE_VERIFIED | PR #189 remains Draft/open, based on `main`; current code head is **108 commits ahead, 0 behind**. #184/#185/#186 remain distinct FastThaiG2P research branches (#186 stacked on #185); #188 remains a separate restricted-source review with overlapping source-registry/audit paths; #190 remains an independent accessibility contrast fix. | Keep all research PRs separate. Reconcile shared registry/document paths deliberately if #188 merges; do not infer approval or merge readiness from CI. |

**Current branch checkpoint:** `fix/benchmark-error-clusters-20261102`; PR [#189](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/189); base `main` = `75c331f69aa3c8e5b4db3ccc5a6da85124600a01`; code head `94eaadb5bda2318dfa864eee7dae1b3715b70374`; 108 ahead / 0 behind. No changes to `main`, no merge, force-push, branch deletion or release.

**External evidence blockers remain:** two independently qualified Thai phonetic/segmentation reviewers plus adjudicator; independent Ukrainian-native target-form review; CCOST A–D curator clarification and actual released TextGrid tier inspection; immutable LOTUSDIS audio object/revision/hash/clean interval; hands-on keyboard, screen-reader, zoom/reflow, mobile and assistive-technology WCAG review. Linguistic accuracy remains `NOT_MEASURED`; accessibility conformance remains unclaimed.

**Documentation verification:** this documentation-only checkpoint at `27300590d598f22505f61e147bc0e591d390e3b5` was exact-head verified: Full CI [41642479329](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41642479329) passed all three jobs and Web Static [41642479264](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41642479264) passed. Ruff, 327 pytest tests, 1,185 subtests, 29 browser parity fixtures, wheel install and master artifact passed. This follow-up register closeout is documentation-only.

---

## Benchmark error-cluster continuation — 2026-11-02

| Priority | Status | Work completed | Remaining acceptance gate |
|---|---|---|---|
| FastThaiG2P / ClippyFirst challenge triage | PARTIAL — runtime recovery and exact-head CI verified; independent phonetic adjudication pending | Inspected the pinned 42-input comparison artifact (run 41454481686; artifact SHA-256 `a166828e7a175af4759120d609ba8511c661db2845a25cab5fab1685c17b0da5`). Added a 42-row coordination TSV. Identified 11/40 syllable-pair differences caused only by unreleased-stop `̚` notation, leaving four candidate phonological differences (short-open glottalization ×2, vowel length ×1, diphthong realization ×1). Added source-evidenced lexical recovery for `ทฤษฎี` and `ฤๅษี`, plus text-lexicon reachability for existing `เตอร์/เทอร์` parser readings. Exact-head CI #41471961004 passed all three jobs; Web Static #41471960975 passed. | The four recovered challenge cases and Python/browser parity are verified on `55f2ef9966da065326873014e8066acc43b2a151`. Independent reviewers must adjudicate the four remaining differences; do not change glottalization, vowel length or diphthong rules based only on FastThaiG2P. |
| Challenge abstention coordination | DONE_VERIFIED — per-record labels and both runtime paths verified | Extended `run_challenge_diagnostics.py` to label abstention clusters and separately report opt-in dictionary-word-segmented output without replacing the conservative endpoint. Exact-head artifact `thai-challenge-runtime-diagnostics` from run #41471961004 confirms 32/42 conservative outputs and 36/42 opt-in word-segmented outputs; four continuous-text probes now complete in the opt-in path. Six abstentions remain: three standalone special-vowel forms, ambiguous `ทราย`, and two malformed inputs. | Keep the six evidence-limited/expected abstentions fail-closed; do not interpret output coverage as accuracy or dictionary boundaries as gold. |
| Source-backed special-orthography recovery | PARTIAL — source pinned, implementation and tests CI-verified; independent review pending | `ฤๅษี → รือ|สี` pinned to Thai Wiktionary oldid 1774048; `ทฤษฎี → ทฺริด-สะ-ดี` and /tʰrit̚˦˥.sa˨˩.diː˧/ pinned to en.wiktionary oldid 87195875. Exact `ทริด → ทริท` normalization does not generalize to arbitrary `ทร`. | Exact-head CI #41471961004 and source-registry checks passed. Independent expert review remains necessary before these entries count as gold. |


**Exact-head verification note:** runtime/code changes are verified on `55f2ef9966da065326873014e8066acc43b2a151` (CI #41471961004; Web Static #41471960975). The audit/matrix/handoff checkpoint `2523002cd0a06c0b30efed6669ca4ba012cb3e10` passed CI #41474317754 and Web Static #41474317862; the structured open-PR/branch inventory checkpoint `7a048753e3fb90e0f3e66157a5d36f5fae181222` passed CI #41475098304 and Web Static #41475098261; the final text-lexicon license note checkpoint `8be5e89d1a9190eaa37c15dbe9340ac1242283e0` passed CI #41475777693 and Web Static #41475777686. These are documentation-only commits after the verified runtime code head; the current audit-register refresh is also documentation-only and receives a final exact-head rerun.

## Priority research continuation — 2026-11-02

| Priority | Status | Work completed in this continuation | Remaining acceptance gate |
|---|---|---|---|
| Independent Thai phonetics and segmentation adjudication | BLOCKED — external reviewers | Rechecked the existing blind 42-item Thai challenge, six-item supplemental packet, protocol and reviewer shortlist. The shortlist now identifies five public institutional candidates; official Chula institutional contacts for CCOST curators are verified, and a copy-ready Thai reviewer invitation is prepared in `docs/external-review-and-source-requests.md`. No person has been contacted, qualified, consented, or registered; no labels were invented. Audio/narrow acoustic work is out of scope. | Two independently qualified Standard Thai reviewers must submit frozen blind labels for broad phonemic IPA, word/syllable boundaries, tone and vowel length from a text-only sample; a separate adjudicator resolves disagreements. Do not claim narrow acoustic/surface validation without audio; audio is not part of this project scope. |
| CCOST A–D wordlist discrepancy | BLOCKED — curator clarification | Reconfirmed the Zenodo v1.0 primary record: 206-item monosyllabic list, official MD5 `e62f500d87b4ff8c6deb4c4595854d34`; the existing reconstruction has 206 unique entries per column and no within-column duplicates, but B/C/D each differ from A by two missing and two extra entries (208-item union). The LREC 2026 paper independently describes a 206-item word list read twice by each speaker. | Official Chula institutional emails for data curators Pittayawat Pittayaporn and Sujinat Jitwiriyanont have been verified; a precise clarification request is prepared in `docs/external-review-and-source-requests.md`, but no outbound message was sent. Obtain a curator/author statement that explains whether A–D are intended to contain identical items or a corrected source/erratum. Do not silently normalize or freeze the 208-item union. |
| CCOST released TextGrid archive | BLOCKED — archive access/inspection | Rechecked the primary Zenodo record and LREC 2026 paper. The record lists `C-COST.zip` (6.2 GB) containing WAV and TextGrid files, plus separate metadata/manual. The paper describes orthographic, word, syllable, phone and toneme annotations and manual correction by phonetically trained native Thai speakers. | Inspect the actual released archive, record exact file hashes and tier inventories, enumerate X-SAMPA labels and tone suffixes, reconcile each actual tier with the paper/manual, and validate a sample before scoring. No archive contents are claimed inspected in this continuation. |
| LOTUSDIS audio assets | PARTIAL — source metadata refreshed; no asset pinned | Rechecked the official HF dataset card and CAI-NECTEC README. The HF card exposes 16 kHz audio plus `sentence`, `speaker_id`, `mic` and `duration`; it lists 120,245 train, 13,090 validation and 27,580 test rows (160,915 total; 13.2 GB). The HF history page displays upload revision prefix `45145d7`; the separate GitHub README is pinned at `b6c7e81498a92003761ac856348d764c287ee02c`. The latter pins documentation, not the Parquet audio snapshot. The audio asset registry remains header-only. | Resolve the full immutable HF dataset revision; select a real row/asset and obtain its audio bytes or immutable object URI; record SHA-256, speaker pseudonym, exact `mic` value, duration, interval start/end and interval-level overlap evidence. No asset, hash or clean interval was fabricated. |
| WCAG 2.2 AA accessibility | PARTIAL — static checks added; manual review blocked | Added `web/tests/accessibility-contract.test.mjs`, wired into CI, Web Static and Pages build. It checks document language, skip links, landmarks, visible labels, described-by targets, status semantics, dynamic Thai/IPA language metadata, keyboard focus selectors, reduced-motion handling and 12 selected text/background contrast pairs. The source-level contrast calculation gives a minimum of approximately 5.71:1. | An explicit test matrix is now recorded in `docs/external-review-and-source-requests.md` (criteria 2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.4.11, 2.5.8, 1.4.10, 1.4.12, 1.4.11, 3.3.1, 3.3.2, 4.1.2, 4.1.3). Complete hands-on keyboard-only, screen-reader, browser zoom/reflow, mobile viewport and assistive-technology testing; record environment, defects, fixes and retest evidence. Static checks do not establish WCAG conformance. |
| Architecture/dependency graph and test redundancy | DONE_VERIFIED — static graph and test-overlap inventory | Exact-head CI artifact: 99 Python modules, 157 Python import edges, 9 browser modules, 7 browser test files, 391 browser assertion calls, 22 browser import edges, 3 HTML assets, 44 workflow script references, 319 Python test functions, 0 exact duplicate test names/bodies, 2 near-name candidates and 5 reviewed dynamic-import sites; 0 parse errors. The `../src/util.js` fixture exposed and now verifies normalized relative-import resolution. The one exact duplicate parser-only test was changed to exercise `analyze_syllable`; no test was deleted. Dynamic imports are intentional test harness loading. | A complete runtime call graph is not claimed and remains DEFERRED; static inventory and overlap review are complete. Keep the two near-name tests because they cover different API/vowel behavior. |

## Exact-head engineering verification — 2026-11-02

- Implementation code checkpoint `c68580a490f89af1cf08224d5811429e74f8ef5b` was squash-merged by PR #182 into main as `65584d9a3d3d64a8e520dbd32411bef4b0a3dd9e` (base `cc398254c178171f74397aed556766e87356ab84`). The verified implementation is now on main and published to GitHub Pages.
- Exact-head CI [41418718922](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41418718922) passed all three jobs: `test`, `wheel-install-smoke`, `master-artifact`. Ruff passed; pytest reported 319 passed and 1,169 subtests passed; generated registries had no drift; source/reviewer registries and all three blind packets validated; Python/browser parity, runtime diagnostics, static accessibility contracts, segmentation diagnostics and master artifact passed. The source distribution was built, its wheel installed in isolation, and package data smoke-tested outside the checkout.
- Exact-head Web Static [41418718843](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41418718843) and external VISTEC evaluation [41418718412](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41418718412) passed on the same code head.
- The static audit artifact reports 99 Python modules, 157 Python import edges, 9 browser modules, 7 browser test files, 391 browser assertion calls, 22 browser import edges, 3 HTML asset edges, 44 workflow script references, 319 test functions, 0 exact duplicate test names, 0 exact duplicate test bodies, 2 near-name candidates and 5 intentional dynamic-import review sites; there are no parse errors. The two near-name candidates were retained because they test different behavior. The pipeline-level cluster test now exercises `analyze_syllable`, while parser-level coverage remains in `test_core.py`.
- Source-attested IPA diagnostic: 7 dictionary rows, 5 circular runtime/source comparisons, 2 non-circular comparisons, no accuracy claim. Wisesight's 993 rows and VISTEC's 50,000 rows remain source-annotated, not expert-adjudicated. Dictionary segmentation boundary F1 was 0.8395 on Wisesight and 0.8283 on VISTEC; the TUD research segmenter was lower at 0.7486 and 0.7530 respectively. TUD is not the production default. The 66-row manual segmentation review sample remains unadjudicated.
- Browser segmentation latency diagnostic: 500-code-point case median 5.538 ms, p95 8.555 ms on Node 22; diagnostic only, no enforced threshold and no accuracy implication.
- The current live site is the successful post-merge Pages deployment at `65584d9a3d3d64a8e520dbd32411bef4b0a3dd9e`, run [41420468875](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41420468875). Main CI [41420468842](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41420468842) and Web Static [41420468939](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41420468939) also passed. The published-content verification step passed; [open the updated site](https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/).
- No independent Thai or Ukrainian reviewers are registered; the reviewer registry and audio asset registry remain empty. WCAG static contracts pass, but hands-on keyboard/screen-reader/device testing remains unperformed. Linguistic accuracy remains `NOT_MEASURED`; this is an engineering-verified research prototype, not a linguistic-accuracy release.

| GitHub Pages publication | DONE_VERIFIED — PR #182 squash-merged and deployed | Main CI, Web Static and Pages Deployment all passed on merge commit 65584d9; post-deploy verification checked the published plain-language service, assets, UI modes and system page. | Site URL responds through the successful Pages workflow; deployment run 41420468875. |

## Post-merge deployment closeout — 2026-11-02

- PR #182 was squash-merged as main commit `65584d9a3d3d64a8e520dbd32411bef4b0a3dd9e`.
- Main CI [41420468842](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41420468842): all three jobs passed. Web Static [41420468939](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41420468939): passed. Pages Deployment [41420468875](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41420468875): build, deploy and published-content verification passed.
- The live site now includes the six source-attested exact-form lexical IPA overrides in both runtimes, the shared IPA → Ukrainian adapter path, updated browser adversarial tests, source/license disclosures and revised system page. Published site: [https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/](https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/).
- This is an engineering-verified research prototype, not a linguistic-accuracy release. Thai and Ukrainian reviewer registries remain empty, audio asset registry remains empty, and linguistic accuracy remains `NOT_MEASURED`.

**Evidence boundary:** no external reviewer outreach, dataset download, CCOST archive extraction, or live screen-reader/device session was completed here. Researcher-provided permission does not create missing source bytes, immutable hashes, reviewer independence, or human annotations. Linguistic accuracy remains `NOT_MEASURED`.

## Independent review and CCOST benchmark readiness — 2026-11-01

| Add a separate candidate-blind Thai review supplement for the user's reported failures | DONE_VERIFIED | Six prompt-only rows cover `วันนี้`, `เห็น` in context, `เพิ่ง`, `อะไรบ้าง`, `อธิบาย` and `ฤๅษี`; separate source record pins the supplement without mutating the original 42-item challenge. The validator test requires exact ID/input coverage and blank/null labels. |
| Add a source-attested regression reference for the reported `เพิ่ง` failure | DONE_VERIFIED | Thai Wiktionary revision 1885200 records monosyllabic `/pʰɤŋ˥˩/` and explicitly labels the vowel short. Added as `SOURCE_ATTESTED_NOT_GOLD`; added to the seven-row Ukrainian-native conditional preference packet and generated IPA→UA candidate registry. It is now a runtime lexical-IPA override in both Python and browser engines, routed through the typed `PhoneticResult` → Ukrainian adapter boundary. It remains source-attested, not independently adjudicated or acoustic gold. |
| Task / acceptance criterion | State | Evidence / next acceptance |
|---|---|---|
| Correct source-use gate so text-only IPA inputs cannot be scored as broad-surface IPA | DONE_VERIFIED | `benchmark_ipa.py` maps `BROAD_PHONEMIC` and `BROAD_SURFACE` to distinct source-registry permissions; project challenge and CCOST wordlist sources permit only broad phonemic labels. Exact-head CI 41341792448 passed. |
| Register project-authored challenge text as input provenance for independent broad-phonemic gold | DONE_VERIFIED — registry/test authored | `CLIPPYFIRST-THAI-CHALLENGE-CC398` is pinned to the 42-item source file and may only supply broad-phonemic input text and segmentation inputs; it is not acoustic evidence. |
| Prepare a controlled CCOST monosyllabic review packet generator | PARTIAL — exact-source run completed; source anomaly blocks freeze | Reconstructed Zenodo `wordlist.csv` is byte-identical by official MD5; SHA-256 is pinned in `source-registry.tsv`. The generator finds 206 rows/206 unique items per order, no duplicates, but A differs from B/C/D by two missing and two extra items each; union=208; status `SOURCE_ORDER_DISCREPANCY_REQUIRES_RECONCILIATION`, `scoreable=false`. No CCOST-derived packet committed. Acceptance: data curator confirms intent or supplies correction/erratum; then regenerate and freeze. |
| Audit the exact published CCOST wordlist and run the packet generator | DONE_VERIFIED — source integrity verified | Zenodo preview reconstruction matches official MD5 `e62f500d87b4ff8c6deb4c4595854d34`; SHA-256 `e3836f6204c674a8d972dfd49de369eea7856ca6f00d520aafcd62f4e7273223`; 206 rows/order, 206 unique/order, zero duplicates, 208-item union. The generator correctly flags A-D set mismatch and refuses to mark the packet scoreable. |
| Resolve CCOST A-D order-set discrepancy | BLOCKED — data-curator clarification | B/C/D each have two items absent from A and two items not in A; no duplicates. Acceptance: authors confirm these are intentional differences or publish corrected wordlist/erratum; do not freeze the 208-item union until resolved. |
| Map CCOST intended annotation tiers and phonetic conventions from the LREC 2026 paper | DONE_VERIFIED — primary paper | ORT/KAN/KAS/MAU/MAS/TRN, X-SAMPA and tone suffixes `_1–_5` are documented; MAU is phonetic segment, MAS phonemic syllable, KAN/KAS canonical forms. |
| Verify actual released CCOST TextGrid archive and map X-SAMPA labels | BLOCKED / evidence-limited | 6.2 GB WAV/TextGrid archive not downloaded; paper's intended schema is known but actual files and full symbol inventory remain uninspected. No CCOST annotation row is scored. |
| Obtain independent Thai phonetic/segmentation reviews | BLOCKED — external human input | 42 frozen project prompts, six supplemental blind regression prompts and a CCOST 206-item generator are prepared; reviewer registry remains empty. Recruitment shortlist is documented in `docs/reviewer-outreach-shortlist.md`; reviewer registry remains empty. Acceptance: two qualified Thai reviewers, frozen independent labels and disagreement log; acoustic claims additionally require authorized audio/time intervals. |
| Obtain Ukrainian-native practical-transcription preferences | BLOCKED — external human input | Seven candidate-blind prompts and criteria protocol are prepared; reviewer registry remains empty. Recruitment shortlist is documented in `docs/reviewer-outreach-shortlist.md`; reviewer registry remains empty. Acceptance: two independent Ukrainian-native reviewers, frozen criteria, original preferences and adjudication log. |
| Measure phonetic accuracy | BLOCKED — no adjudicated gold | IPA and segmentation gold registries remain empty; accuracy is NOT_MEASURED. |

| Identify potential independent reviewer candidates | PARTIAL — outreach not sent | Public university profiles and peer-reviewed work support a shortlist in `docs/reviewer-outreach-shortlist.md`; no availability, native status, conflicts or consent have been verified. Acceptance: confirm qualifications/independence and receive two frozen reviews per layer. |

**Evidence boundary:** code and packet validation cannot substitute for real Thai/Ukrainian reviewers. CCOST manual correction is valuable external evidence, but the LREC paper reports no formal inter-annotator agreement. The CCOST wordlist contains prompts only. Do not claim independent gold, acoustic validity or accuracy before the acceptance criteria above are met.

**Exact-head verification:** `536f03327f11d258a4e7638091797128754b6602`; CI [41342132989](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41342132989) passed all three jobs. Ruff passed; pytest reported **296 passed, 1168 subtests passed**; browser/IPA/RTGS/diagnostic checks passed; wheel-install smoke and master-artifact validation passed. Web Static [41342132990](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41342132990) passed; external VISTEC segmentation evaluation [41342132985](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41342132985) passed. Local tests were not run because the repository was accessed through the GitHub connector only.

---

## Repository structure cleanup checkpoint — 2026-11-01

| Task / acceptance criterion | State | Evidence / next acceptance |
|---|---|---|
| Add repository documentation navigation and ownership guide | DONE_VERIFIED | PR [#171](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/171), merged as `85ced007f6fab7572a78380553ebfe42ccb18e07`; exact-head CI [41310072386](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41310072386) passed all three jobs. |
| Align architecture guide with the actual typed-IPA pipeline and module ownership | DONE_VERIFIED | PR [#172](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/172), merged as `5d7a2ee9ca38ff37e3ea286de747828dfabe0c32`; post-merge CI [41311528849](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41311528849) passed. |
| Inventory scripts, responsibilities, inputs/outputs and evidence boundaries | DONE_VERIFIED | PR [#174](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/174), merged as `fa33cb46aa8f5081e901241b6fb437e3fbf12306`; exact-head CI [41312645359](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41312645359) passed. `scripts/README.md` inventories all 24 scripts. |
| Remove unused browser direct Thai-grapheme → Ukrainian maps | DONE_VERIFIED | PR [#173](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/173), merged as `3d6e9f7dc184cdfd69f3aa284cd15ca2b48c78b1`; exact-head CI [41312044065](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41312044065) and Web Static [41312044090](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41312044090) passed. Browser low-class consonants are derived from the canonical `C` registry. |
| Detect drift in committed generated master-table registries | DONE_VERIFIED | PR [#175](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/175), merged as `b957bd01d0a4269dc8d2a7d87f98c7519f0e193a`; exact-head CI [41323955237](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41323955237) passed all three jobs. The gate exposed stale orthographic/vowel outputs and manifest metadata; the generator now writes deterministic LF CSVs and the tracked outputs were regenerated from their owning sources. |
| Remove duplicate Python consonant maps | DONE_VERIFIED | PR [#176](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/176), merged as `bd0b3d7da60c2060a1c30d56ef22f069c21a41da`; exact-head CI [41324492017](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41324492017) passed all three jobs. `ONSET_IPA` and `LOW_SINGLE` are now derived from `data/thai/consonants.csv`, with a registry-parity regression test. |
| Correct the master manifest's IPA boundary description | DONE_VERIFIED | PR [#177](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/177), merged as `1e0c2b3432a49178c6f00fbfb631a0258a7cc6fc`; exact-head CI [41324845398](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41324845398) passed all three jobs. The manifest now states that typed IPA is the mandatory adapter boundary. |
| Review duplicate UI assertions | DONE_VERIFIED — narrow scope | PR #170 removed two immediately repeated UI assertions and was merged as `b2075aa9079512551c76e247af941a3d158a5313`; this does not establish that all similar tests are redundant. |
| Complete repository-wide import/call/reference graph and prove suspected dead code | PARTIAL | Module import surfaces and ownership boundaries were inspected; a complete caller/reference graph and dead-code proof have not been established in the connector-only environment. Acceptance: run repository-wide static reference analysis on a clean checkout and review all dynamic/entry-point consumers. |
| Review test redundancy without reducing acceptance coverage | PARTIAL | Immediate duplicate assertions were removed in #170; broader test/fixture overlap remains to be reviewed by contract and layer, not by matching names alone. |
| Split or archive large chronological audit/handoff files | DEFERRED | Preserve the historical evidence for now. Acceptance requires a complete cross-reference/link inventory and a verified archive plan; no active evidence or history was moved or deleted. |
| Prune historical branches | PARTIAL — owner policy required | 10 branch refs currently exist including this documentation branch; 9 are non-main. No branch was deleted. PR #178 is the sole open PR and carries this documentation closeout. Acceptance requires commit-level provenance review and an owner-approved retention policy. |
| Configure main branch protection | TODO — owner configuration | Branch listing reports `protected=false`. Acceptance requires the owner to choose required checks/review policy and configure a ruleset; no settings were changed. |
| Independent Thai IPA/segmentation and Ukrainian target-form adjudication | BLOCKED / evidence-limited | Requires qualified independent Thai reviewers and two independent Ukrainian-native reviewers, frozen criteria, dual labels and disagreement logs; issue #114. |
| CCOST paper-tier map and archive reconciliation | PARTIAL | LREC 2026 paper specifies ORT/KAN/KAS/MAU/MAS/TRN, X-SAMPA and tone suffixes _1–_5; the paper reports no formal inter-annotator agreement. Actual released TextGrid conformance and full X-SAMPA mapping remain BLOCKED pending local archive inspection. |
| Manual browser/device and WCAG 2.2 AA review | BLOCKED | Requires recorded human keyboard, screen-reader, viewport and device review; automated CI is not a substitute. |

**Main at cleanup start:** `69dafe58a9458d33a645cdcd517e61e9978abdbd`. **Latest main at documentation closeout start:** `1e0c2b3432a49178c6f00fbfb631a0258a7cc6fc`. **Documentation branch:** `docs/repository-cleanup-closeout-20261101`. PR #178 is the sole open PR at this checkpoint. No branch deletion or repository-setting change was made.

## External benchmark research refresh — 2026-11-01

| Task / acceptance criterion | State | Evidence / next acceptance |
|---|---|---|
| Screen external Thai G2P/IPA benchmark | DONE_VERIFIED — research screening | Added Thai G2P v4 to `data/corpus_sources.csv` and `docs/g2p-benchmark.md`. Dataset card declares CC0-1.0 and reports 8,076 test rows, but source lineage includes Thai W2P and Wiktionary; use only as a source-attested comparator after runtime lexical-overlap audit, not independent gold. |
| Screen external Thai segmentation corpora | DONE_VERIFIED — research screening | BEST-2010 official TEST_100K and LST20 identified. BEST license/access must be verified before acquisition; LST20 terms prohibit redistribution/modification absent permission and require separate commercial arrangements. No corpus copied. |
| Separate ASR resources from phonetic gold | DONE_VERIFIED — scope clarification | FLEURS and Common Voice Thai are speech/ASR resources, not phone-level IPA or Ukrainian-target gold. CCOST remains the closest phone/toneme candidate; its manual is inspected, but the released TextGrid tier/toneme schema remains unverified. |
| Exact-head CI for benchmark registry, CCOST manual-review updates and test changes | DONE_VERIFIED on PR #169 head `0dee9e36cd5391b599c8b785a8b2c1b81ea325a7` | Run [41300790280](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41300790280): `test`, `wheel-install-smoke`, and `master-artifact` all passed. This is the current exact PR head; PR remains open/unmerged. |
| Execute new accuracy benchmark | BLOCKED / evidence-limited | No new score calculated; requires source-overlap filtering, legal/access review, and independently adjudicated Thai IPA plus Ukrainian target labels. |

---

## 2026-10-31 — exact-head verification refresh (PRs #169–#170)

| Task / acceptance criterion | State | Evidence / next acceptance |
|---|---|---|
| Verify final CCOST provenance/audit PR head | DONE_VERIFIED | PR #169 head `8690b42ccbf5bbff35e57646c8624620f093880c`; exact-head CI [41243882073](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41243882073): `test`, `wheel-install-smoke`, and `master-artifact` all passed. |
| Verify UI assertion cleanup | DONE_VERIFIED | PR #170 head `1cdc3d7971498ce3312ff9a79b23ee84b8d917aa`; CI [41243709726](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41243709726) and Web Static [41243709639](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41243709639) passed. |
| Keep PR-only integration contract | DONE_VERIFIED | Both PRs remain open; no merge to `main` performed. Both branches are zero commits behind `main` at this checkpoint. |
| Protect `main` | TODO — owner configuration | `protected=false`; acceptance requires owner decision on required checks/reviews and configuration of a ruleset. |
| Retrieve and inspect CCOST annotation manual | DONE_VERIFIED — document inspection | Official Zenodo `CCOST_manual.pdf` (19 pages; MD5 `caecb20d26e8458b20c7c269ca22b59e`) inspected. It documents OCTRA ASR correction, Thai-script normalization, Praat transcript/boundary correction and BAS `CHUNKPREP → G2P → MAUS → PHO2SYL`; it does not define the released TextGrid tier/phone/toneme schema or independent double annotation. |
| Independent Thai IPA/segmentation adjudication | BLOCKED / evidence-limited | Qualified independent Thai reviewers, frozen annotation protocol, dual labels and disagreement log; issue #114. |
| Ukrainian target-form adjudication | BLOCKED / evidence-limited | Two independent Ukrainian-native reviewers, predeclared criteria and adjudication log; issue #114. |
| Manual browser/device and WCAG 2.2 AA review | BLOCKED | Human keyboard, screen-reader, viewport and device review with recorded findings; issue #114. |
| Historical branch retention | PARTIAL | Current branch listing reconciled across both API pages: 184 refs total (100 + 84). Retention/disposition remains unreviewed at commit level; no destructive pruning without provenance review and owner-approved retention policy. |

**Current main:** `8759fc5f12c1d27bd13f4d6c32a364d5cc7ac1c8`.  
**Readiness:** engineering-verified research prototype; not release-ready for general linguistic-accuracy claims.

---

## 2026-10-31 — CCOST source provenance reconciliation (PR #169)

| Task / acceptance criterion | State | Evidence / next acceptance |
|---|---|---|
| Distinguish CCOST dataset DOI from its LREC 2026 paper DOI and record the annotation process | DONE_VERIFIED | Primary Zenodo and LREC/ACL records identify separate dataset/article DOIs, dataset license, corpus composition, annotation layers and manual-correction provenance. The public abstract does not establish two independent blinded labels per item; the evidence is explicitly bounded. |
| Enforce CCOST provenance/license metadata in tests | DONE_VERIFIED | Added assertions in `tests/test_corpus_source_registry.py` for both DOI records, manual-correction provenance and the stated limit on independent adjudication. Exact-head CI [41242513053](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41242513053) passed `test`, `wheel-install-smoke`, and `master-artifact` on head `a331131567f6e17f9dd5fe96c8624620f093880c`. |
| Preserve corpus licensing and non-redistribution | DONE_VERIFIED | Dataset remains external; no WAV/TextGrid files were copied. The registry retains CC BY-NC-SA 4.0 non-commercial/share-alike terms. |

- **Base main:** `8759fc5f12c1d27bd13f4d6c32a364d5cc7ac1c8` (PR #168 closeout merged).
- **PR:** [#169](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/169), documentation/audit closeout extended with CCOST evidence provenance; code/data/test changes passed all three jobs on prior head `a331131567f6e17f9dd5fe96c8624620f093880c` in run [41242513053](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41242513053). The final audit/handoff-only refresh is now on the PR branch; its exact-head CI is pending. The preceding code/data/test head `a331131567f6e17f9dd5fe96c8624620f093880c` passed all three jobs in [41242513053](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41242513053). Do not treat that prior run as verification of the final documentation head.
- **Branch inventory:** 184 refs (research 25, chore 8); the temporary research branch remains preserved, not deleted.
- **PR #170:** separate test-only cleanup removes two immediately repeated assertions in `web/tests/ui-contract.test.mjs`; exact-head CI [41243709726](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41243709726) and Web Static [41243709639](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41243709639) are queued. No runtime behavior changes.
- **Readiness:** engineering-verified research prototype; independent Thai/UA adjudication, CCOST manual/annotation protocol review, and manual accessibility review remain external blockers.

---

## 2026-10-31 — PRs #165–#167 integration closeout

| Task / acceptance criterion | State | Evidence / next acceptance |
|---|---|---|
| Reconcile agent contract, canonical handoff, validation matrix and RTGS research contract | DONE_VERIFIED | PR [#165](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/165), squash-merged as `d27e8ec2d7f233d62c1bb849566e4756ebeceffe`; exact-head CI [41236396997](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41236396997) and post-merge main CI [41239400828](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41239400828) passed. |
| Verify every RTGS rime row and onset/coda/sequence matrix against runtime adapter | DONE_VERIFIED | PR [#166](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/166), squash-merged as `e5738560bddd4c2b9d0557bd2ad84d58446f6252`; exact-head CI [41236181030](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41236181030), Web Static [41236181002](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41236181002), post-merge main CI [41239420358](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41239420358), Web Static [41239420400](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41239420400), and Pages [41239420395](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41239420395) passed. |
| Cancel superseded CI/Web Static runs on non-main refs while preserving main runs | DONE_VERIFIED | PR [#167](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/167), squash-merged as `72a77cb42ad05c33274d70c4dcd9f20e07432b64`; exact-head CI [41237340250](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41237340250), Web Static [41237340267](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41237340267), post-merge main CI [41239440616](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41239440616), and Web Static [41239440643](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41239440643) passed. |
| Final main CI test suite and package smoke | DONE_VERIFIED | Run [41239440616](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41239440616): 251 pytest tests and 1,164 subtests passed; Ruff, Python/browser parity (29 fixtures), diagnostics, generated-data drift and isolated wheel-install smoke passed. |
| Independent master artifact | DONE_VERIFIED | Same run [41239440616](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41239440616): artifact SHA-256 `74f40079c2bae8a4f875fa8e2c860ac8a202bbb1bd8e4ae72d834f48d93adc09`; 3,086,353 bytes; independent download/hash check and assertions passed at 351,780 rows / 41 rime records. |
| Exact post-merge Web Static validation | DONE_VERIFIED | Run [41239440643](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41239440643) passed. |
| Historical branch retention | PARTIAL | 182 refs inventoried. No destructive pruning: unique historical work may exist, no owner-approved retention/archive policy exists, and the connected GitHub tools expose no branch-deletion action. Acceptance: commit-level provenance review plus explicit retention policy. |
| Main branch protection | TODO — owner configuration | GitHub reports `protected=false`; no rulesets configured. Acceptance: owner configures required CI checks and decides review requirements. |
| Independent Thai segmentation / phonology / IPA gold | BLOCKED / evidence-limited | Requires qualified independent Thai reviewers, agreed transcription layer, authorized acoustic assets where acoustic claims are made, dual labels and disagreement log. Issue #114. |
| Ukrainian target-form adjudication | BLOCKED / evidence-limited | Requires two independent Ukrainian-native reviewers, predefined criteria, blinded judgments and adjudication log. Issue #114. |
| Manual browser/device and WCAG 2.2 AA review | BLOCKED | Requires human keyboard, screen-reader, viewport and device review; automated static/served-content tests are not a substitute. Issue #114. |
| TUD segmentation model | PARTIAL / research-only | Same-row comparison is diagnostic on source-annotated data; do not promote to production default without human error review, predeclared thresholds and independent licensed-domain evaluation. |
| Thai tokenizer integration | DEFERRED | Requires separate provenance, license and browser-compatibility review; outside current Thai phonetic/RTGS completion scope. |
| Local checkout/test execution | BLOCKED | Container DNS cannot resolve `github.com`; no local test result is claimed. GitHub Actions provides verification evidence. |

**Current main:** `72a77cb42ad05c33274d70c4dcd9f20e07432b64`.  
**Implementation PRs:** none after #167. Documentation-only PR [#168](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/168) carries this audit/handoff refresh. **Canonical external blocker:** issue #114.  
**Readiness:** engineering-verified research prototype; not release-ready for general linguistic-accuracy claims.

---
## 2026-10-31 — PR #164 RTGS-based Ukrainian output mode and full method matrices

| Task / acceptance criterion | State | Evidence / next acceptance |
|---|---|---|
| Separate user-selectable phonetic and romanization-based output modes | DONE_VERIFIED | PR [#164](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/164), merged as `01631b98173b2e54695bdf757a538735fca8fdff`. UI selector keeps IPA-first phonetic output separate from RTGS-first practical rendering. |
| RTGS Ukrainian renderer is independent of IPA adapter | DONE_VERIFIED | `web/src/rtgs-ukrainian.js` consumes the RTGS token sequence and does not call the IPA adapter; tests assert module and UI boundaries. |
| Preserve unsupported spans and non-Thai text | DONE_VERIFIED | Unsupported RTGS tokens remain explicit unresolved markers; punctuation, digits, whitespace and non-Thai text are preserved by the token renderer; regression tests cover these contracts. |
| Full phonetic and RTGS correspondence matrices | DONE_VERIFIED — inventory coverage | `docs/ukrainian-correspondence-matrices.md`: 44 Thai consonant graphemes with onset/coda inventories and 41 registered rime records in each method matrix; RTGS digraph/rime mappings and comparison examples included. Automated tests compare matrix inventories against source registries. |
| Preserve RTGS rime `iao` without component loss | DONE_VERIFIED | Regression expects `iao → іау`; matrix and adapter use the same output. |
| Exact PR-head CI | DONE_VERIFIED | Runs [41234077035](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41234077035) and [41234072432](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41234072432) succeeded. |
| Exact PR-head Web static validation | DONE_VERIFIED | Run [41234077207](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41234077207) succeeded. |
| RTGS integration research contract and historical PR status | DONE_VERIFIED | `docs/research/thai-romanization-integration.md` now distinguishes the optional RTGS → Ukrainian practical-rendering route from the mandatory IPA-first phonetic route; stale PR #111/#112 open-state claims were reconciled against GitHub. |
| Post-merge main CI and Pages publication | TODO / QUEUED | Main CI runs 41235954608 and 41235967491, Pages 41235954575, Web static validation 41235954576; all queued at latest poll, no failure reported. Record success only after completion. |
| Independent Thai phonology, segmentation and IPA adjudication | BLOCKED / evidence-limited | Requires independent Thai expert review and adjudicated reference records; issue #114. |
| Independent Ukrainian-native target-form adjudication | BLOCKED / evidence-limited | Requires Ukrainian-native review with recorded decisions and rationale; issue #114. |
| Manual browser/device and WCAG 2.2 AA review | BLOCKED | Requires real browser/device testing and accessibility review; automated static validation is not a substitute. |

- The RTGS route is a separately labelled romanization-based practical rendering, not IPA transcription and not ISO 11940 orthographic transliteration.
- RTGS does not preserve tone and all vowel-length distinctions. Matrix completeness is an inventory/programming fact, not independent proof of linguistic correctness or an official Ukrainian standard.
- `AGENTS.md` and the stale RTGS research integration contract are reconciled on open PR #165 (exact-head CI queued). PR #166 adds all-row matrix/runtime checks (exact-head CI and static validation queued). Issue #114 has been updated. Neither follow-up is merged yet.

## 2026-10-31 — PR #162 typed-IPA boundary and complete test discovery

| Task | State | Evidence / next acceptance |
|---|---|---|
| Secondary Ukrainian candidate renderer uses typed IPA | DONE_VERIFIED | PR [#162](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/162), merged as `1b1480c5a79b6dd38dc8b916d52ad599e38a9748`. The Thai analysis API now passes the supported `PhoneticResult` object to the secondary candidate renderer; unsupported, uncertain, empty and malformed IPA withholds candidates. |
| Complete Python test discovery | DONE_VERIFIED | CI now runs `python -m pytest -q -ra`; the prior `unittest discover` invocation imported but did not execute 35 module-level test functions across five files. Exact-head run [41229053598](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41229053598) reports **251 passed, 1164 subtests passed**. Ruff passed. |
| Preserve source orthographic role across lexical rewrites | DONE_VERIFIED | Parser captures the role from the original normalized Thai form before applying an exact lexical working-form rewrite. Regression coverage verifies special `อย-` role metadata remains inspectable. No new pronunciation is inferred. |
| Typed IPA / source evidence regression contracts | DONE_VERIFIED | Tests preserve the distinction between dictionary segmental IPA and absent surface IPA, canonical vs normalized IPA notation, one-syllable parser vs multi-syllable word, and practical output vs secondary candidates. |
| Practical transcription documentation reconciliation | DONE_VERIFIED | `docs/practical-transcription.md` now reflects the executable typed-IPA boundary and the project-specific aspirated-onset apostrophe convention already recorded in issue #114 and implemented by the adapter. It is not represented as an official Ukrainian norm. |
| PR #162 exact-head CI | DONE_VERIFIED | Run [41229053598](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41229053598) passed all three jobs. |
| PR #162 post-merge main CI | DONE_VERIFIED | Main run [41229435682](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41229435682) passed `test`, `wheel-install-smoke` and `master-artifact`. Master artifact SHA-256 verified; 351,780 rows / 41 vowel-rime records. |
| Published Pages deployment | DONE_VERIFIED | Run [41229435706](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41229435706) passed build and deploy, including published-service/transcription-pipeline verification. |
| Mainline / open PR inventory | DONE_VERIFIED | Current code checkpoint: `1b1480c5a79b6dd38dc8b916d52ad599e38a9748`; PR #162 merged; no open PRs. Issue #114 remains the external evidence tracker. |
| Historical branch retention | PARTIAL | 176 refs (100 + 76). No destructive pruning: no owner-approved retention/archive policy and no safe branch-deletion action. Acceptance: inspect unique commits/provenance and approve retention policy before pruning. |
| Main branch protection | TODO — owner configuration | GitHub reports `protected=false`. Not changed because repository settings are outside this run's authorized write scope. Acceptance: owner configures a ruleset requiring successful CI checks and decides review requirements. |
| Local checkout | BLOCKED | Container DNS cannot resolve `github.com`; no local test result is claimed. GitHub Actions runs above provide verification evidence. |

**Internal engineering status:** the secondary IPA adapter path, complete Python test discovery, parser metadata preservation, packaging, artifact generation/drift, parity and automated diagnostics are verified at `1b1480c5a79b6dd38dc8b916d52ad599e38a9748`. Branch protection and branch retention are administrative owner decisions.

**External validation status (not internal technical debt):** independent Thai segmentation/IPA adjudication, independent Ukrainian-native target-form adjudication, and manual browser/device plus WCAG 2.2 AA review remain pending qualified reviewers and recorded evidence. Wisesight source annotations, source-attested dictionary IPA, TUD diagnostics and automated UI checks are not expert gold.

**Readiness:** engineering-verified research prototype. Not release-ready for general linguistic-accuracy claims until external evidence gates are satisfied.

---

## 2026-10-31 — canonical repository state at PR #158 merge

| Task | State | Evidence / next acceptance |
|---|---|---|
| PR #153 HTTP Content-Length validation | DONE_VERIFIED | Merged as `8a539193798e55c3010e3a6a72a0e2578ea413c9`; negative and malformed lengths are rejected before body reads. Test-first red run [41141368949](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41141368949); exact PR CI [41141850559](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41141850559), post-merge main CI [41142211674](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41142211674), and Pages [41142211675](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41142211675) passed. |
| PR #154 HTTP closeout documentation | DONE_VERIFIED | Merged as `0f7c41a753efa7abb88ea279ddc6a22ccdf11c6d`; exact-head CI [41142947816](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41142947816) and post-merge main CI [41143370393](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41143370393) passed. |
| PR #155 master-artifact CI reuse | DONE_VERIFIED | Merged as `3325e98b98bde6926f36c74ad76dc94fe35480b0`; exact PR CI [41143491570](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41143491570) and post-merge main CI [41143907732](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41143907732) passed all three jobs and 216 Python tests. The master artifact is generated once, uploaded, downloaded, SHA-256 checked, and validated at 351,780 rows / 41 vowel-rime records. |
| PR #156 audit/handoff reconciliation | DONE_VERIFIED | Merged as `c4216d69982ec2564b5ed615b06d088d18143b4f`; exact PR CI [41144610012](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41144610012) and post-merge main CI [41144968470](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41144968470) passed. |
| PR #157 canonical status refresh | DONE_VERIFIED | Merged as `2bba0fc43ebba08e82555a554c2e97e5d952e22f`; exact-head PR CI [41183616913](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41183616913) passed all three jobs; post-merge main CI [41184009121](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41184009121) passed all jobs, including Python/Node tests, generation, drift checks, diagnostics and master-artifact validation. |
| PR #158 post-merge verification closeout | DONE_VERIFIED | Squash-merged as `0f155dc36a0046d3ed02457a9459a1fa6d755b75`; exact-head CI [41187802957](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41187802957) passed all three jobs; post-merge main CI [41188107607](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41188107607) passed all three jobs, including tests, wheel-install smoke and master-artifact validation. |
| Mainline / PR inventory | DONE_VERIFIED | Main at this checkpoint is `0f155dc36a0046d3ed02457a9459a1fa6d755b75`; no open pull requests remained after PR #158 merged. Open issue #114 retains the independent research and manual accessibility gates. |
| Historical branch hygiene | PARTIAL | 171 branch refs were observed at this checkpoint (100 on page 1 and 71 on page 2); no branches were deleted because historical evidence may exist, no owner-approved retention policy exists, and the connected GitHub actions expose no branch-deletion operation. |
| Independent Thai segmentation / IPA gold | BLOCKED / evidence-limited | Requires qualified independent Thai reviewers, a frozen annotation protocol, authorized audio where acoustic claims are made, dual labels and a disagreement log. Current source-attested dictionaries and source-annotated Wisesight labels are not independent gold. |
| Ukrainian target-form adjudication | BLOCKED / evidence-limited | Requires two independent Ukrainian-native reviewers, blinded judgments against agreed IPA targets, criteria versioning and an adjudication log. Existing adapter output is a project candidate, not gold. |
| Manual browser/device visual and WCAG 2.2 AA review | BLOCKED | Automated UI-contract and served-content checks pass, but they do not replace human keyboard, screen-reader, viewport and device review. Acceptance requires recorded manual results and resolved findings. |
| TUD segmentation research model | PARTIAL / research-only | Held-out/source-annotated comparisons are diagnostic, not independent gold. Do not promote it to production default without human error review, predeclared thresholds and independent licensed-domain evaluation. |
| Thai tokenizer integration | DEFERRED | Requires separate provenance, license, browser-compatibility and parity review before bundling. |
| Local checkout | BLOCKED | Container DNS could not resolve `github.com`; no local test run is claimed. GitHub Actions is the verification source for this run. |

**Main at this checkpoint:** `0f155dc36a0046d3ed02457a9459a1fa6d755b75`.
**Latest main CI:** [41188107607](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41188107607) — SUCCESS.
**Latest published-site verification:** [41142211675](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41142211675) — PASS; PRs #153–#158 changed no web runtime source.
**Readiness:** engineering-verified research prototype; not release-ready for independent Thai segmentation, IPA or Ukrainian target-accuracy claims.

---

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
| JSON API request contract | DONE_VERIFIED_ON_BRANCH | Non-object JSON bodies (array, null, string) now return 400 `invalid_request`, not an accidental 500. Test-first run [41128931305](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41128931305) failed in the unittest job after the regression was added; implementation head `16a58185cd42b687a982bb59dabbf1a49d161fed` passed test and master-artifact in [41129088376](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41129088376). |
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

| Task | State | Evidence / next acceptance |
|---|---|---|
| PR #141 repository hygiene | DONE_VERIFIED | Merged to main previously; version single-source, TSV delimiter regression and core/Pages action upgrades retained. |
| PR #144 lexical evidence forward-port | DONE_VERIFIED_FOR_IMPLEMENTATION | Squash-merged as `cb7ff2a49731d3c02ddba400a4ddbc166395d493`. Exact-head checks on `72a0e147fbbcd6d21fefc40a4219f9fb7c0bfc0b`: 5/5 check runs successful (Python/browser tests, master artifact and web-static validation). Adds bounded `ทราม → ซาม` handling and ten enumerated regression forms; no productive `ทร → ซ` rule. Evidence grade remains SOURCE_ATTESTED_NOT_GOLD. |
| Historical PR #111 | DONE — superseded | Closed after the same 13-file bounded change was forward-ported onto current main through PR #144. Original branch/history preserved; no force-rebase. |
| Mainline post-merge CI | PARTIAL / RUNNING at handoff | Main SHA `cb7ff2a49731d3c02ddba400a4ddbc166395d493`; CI run [41128531462](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41128531462) and Pages run [41128531547](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41128531547) were still in progress at last check. Web Static run [41128531495](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41128531495) passed. Do not call post-merge CI/Pages complete until those runs finish successfully. |
| Branch inventory | PARTIAL | 156 branch refs observed across two API pages. No mass deletion or force-rebase; classify unique commits and retain branch provenance before any destructive pruning. |
| Optional G2P/VISTEC action pins | DEFERRED | Older action pins remain in external research workflows. Updating them triggers external benchmark jobs; handle as a bounded workflow-maintenance change with explicit result inspection. |
| Dependency/tooling hygiene | TODO | `pyproject.toml` currently declares only the setuptools build requirement and optional `openpyxl`; there is no declared development extra or formatter/linter/type-checker gate. Audit actual imports and CI commands before adding dependencies. |
| Changelog synchronization | DONE_VERIFIED | Added v0.6.1 closeout entry reflecting merged implementation and evidence boundaries. |
| Linguistic accuracy / release readiness | BLOCKED / evidence-limited | Independent expert-adjudicated Thai segmentation, IPA and Ukrainian target-form gold is still absent. Source-attested dictionary forms and parity tests are not accuracy gold. Manual browser/device and WCAG 2.2 AA review also remain outstanding. |

**Current main:** `cb7ff2a49731d3c02ddba400a4ddbc166395d493`.
**Working branch:** `chore/closeout-docs-and-debt-register-20261030` (documentation-only follow-up).
**Public service:** https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/

---

## 2026-10-30 — Thai lexical exception forward-port

| Task | State | Evidence |
|---|---|---|
| Exact lexical `ทราม → ซาม` and false-cluster guards | PARTIAL — fresh mainline branch | Ported PR #111's bounded change onto current main; added source registry/text lexicon entries, Python/browser exact mappings, and tests for ten enumerated forms through typed IPA → Ukrainian adaptation. No productive `ทร → ซ` rule; isolated ambiguous forms remain fail-closed. |
| Linguistic evidence scope | SOURCE_ATTESTED_NOT_GOLD | Royal Institute Journal 36(4), 2011, p. 557 discusses `ทราม` among historical /s/-reading forms; Wiktionary records `/saːm˧/`. Neither is independent expert/acoustic IPA gold. |
| TDD | DONE_VERIFIED_FOR_RED_STAGE | Browser parity run `41124129117` and Python run `41124128896` failed on the expected missing lexical handling/source-registry row before implementation. |
| Exact-head acceptance | TODO / pending | Must pass full Python suite, browser parity, generated-data drift checks and 351,780-row master-artifact assertions before merge. |
| Historical PR #111 | DEFERRED / preserved | Original branch remains untouched and 452 commits behind main. Its bounded change is forward-ported; close as superseded after PR #144 merges. |

## 2026-10-30 — repository hygiene integration and follow-up

| Task | State | Evidence |
|---|---|---|
| PR #141 repository hygiene | DONE_VERIFIED | Squash-merged to `main` as `4d087e66778854503a0e6d355d605d83a50354f8`. Exact PR CI `41121318912` and Web Static `41121319014` passed. Post-merge CI `41122595309`, Web Static `41122595149`, and Pages build/deploy/live-content verification `41122595375` passed. Master artifact asserted 351,780 rows and 41 vowel records. |
| Citation metadata version alignment | DONE_VERIFIED | PR #142 merged as `81123ef50fbfc0335e22e6f16f4a5b02d967bb14`; exact-head CI `41123979097` passed (212 Python tests and master artifact), post-merge main CI `41125905331` and Pages verification `41125905186` passed. CFF version is 0.6.1; unverified `date-released` removed. |
| PR #111 lexical exception | PARTIAL — forward-port PR #144 | Historical PR #111 is closed as superseded on its stale base; the bounded `ทราม → ซาม` change is ported to a fresh current-main branch. Exact-head CI is pending. |
| Historical branch cleanup | PARTIAL | Existing branch inventory is retained. No destructive deletion or force-rebase; branch disposition requires review of unique commit content. |
| Linguistic validation | BLOCKED / evidence-limited | Independent expert-adjudicated Thai segmentation, IPA and Ukrainian target-form gold is still absent. |

## 2026-10-30 — repository hygiene: version and TSV contract

| Task | State | Evidence |
|---|---|---|
| Single package-version source | DONE_VERIFIED on `chore/repository-hygiene-20261030` | Added `src/thai_ukrainian/_version.py`; setuptools reads its value dynamically; package `__version__` and HTTP server banner use the same value. Regression test compares both with installed distribution metadata. |
| TSV input delimiter | DONE_VERIFIED | `.tsv` input now uses a tab delimiter while `.csv` remains comma-delimited. Added a real-file regression test for a two-column TSV. |
| TDD evidence | DONE_VERIFIED | Test-only commit `e770511cae4d2e0ddf85a66b3eb785cda1453c5b` failed as expected in CI run [41118188899](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41118188899) with exactly the two regressions above. Implementation head `9f488a983b77393c161afa0bfe01f0550d7c2cf3` passed full CI run [41118657251](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41118657251): 211 Python tests; browser parity, IPA adapter, UI contract and research diagnostics; master-artifact job passed with 351,780 rows and 41 vowel records. |
| Core CI and web-static action runtime | DONE_VERIFIED | Updated checkout/setup-python/setup-node/upload-artifact to v7. Web static run [41120184197](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41120184197) passed; exact-head CI run [41120192415](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41120192415) completed test and master-artifact jobs successfully. Test job passed 211 Python tests and no longer emitted the Node.js 20 deprecation warning. |
| Pages workflow action runtime | PARTIAL | Updated configure-pages to v6, upload-pages-artifact to v5 and deploy-pages to v5. Deployment was not triggered from this unmerged branch to avoid publishing unmerged content; validate on the next main deployment. |
| Optional external workflow action pins | DEFERRED | Optional G2P and VISTEC workflows retain older action pins. Updating their own workflow files would trigger long-running external comparator/corpus jobs; defer to a dedicated run. |
| Local clean clone/test execution | BLOCKED | `git clone` could not resolve `github.com` in the execution container. Verification evidence is from GitHub Actions; no local test run is claimed. |
| Branch inventory and reconciliation | PARTIAL | 151 branch refs inventoried: 44 `docs/`, 24 `research/`, 22 `feat/`, 22 `fix/`, plus the remaining categories. PR #140 was squash-merged into `main` as `37a2b5be62896a758ddc59b9b91184e448b4d963`. PR #111 remains an untouched historical ref; its source-attested lexical change is forward-ported in PR #144 and the old PR will be closed as superseded after merge. Historical branches were not mass-rebased or deleted because doing so would rewrite or discard distinct work. |
| Linguistic/release readiness | BLOCKED / evidence-limited | Independent expert-adjudicated Thai segmentation, IPA and Ukrainian target-form gold remains unavailable. Automated CI verifies implementation contracts, not linguistic accuracy. |

Working branch is based on main after PR #140. PR #141 is open against the post-PR-140 main head. The verified implementation/workflow head is `caab0adfd5b22fd07702e0aa0f86635aa46d5406`; subsequent commits update only the audit/handoff documents. The branch inventory is recorded without destructive branch rewriting; old branches remain preserved for review.

---

## 2026-10-30 — strictness scale and responsive layout — merged and published

| Component | State | Validation |
|---|---|---|
| User-facing strictness control | DONE_VERIFIED — PR #138 merged as `398a25e7f884f11bee85e0888026a6b2875bdf8f` | Three-position range control: 1/3 heuristic, 2/3 structural, 3/3 conservative (default). Higher values are stricter. |
| Mode semantics and evidence caveat | DONE_VERIFIED | Existing `super-soft`, `soft`, and `strict` engine policies map to the scale; lower strictness increases coverage, not accuracy. The positions are strategy profiles, not calibrated confidence scores. |
| Responsive layout and accessibility baseline | DONE_VERIFIED — PR #139 merged as `720b528e0f6560912d87750158c510fc746a3044` | Consolidated responsive stylesheet; 44px slider/control targets; visible focus styles; mobile layout; updated cache-busting keys. |
| README and canonical project records | DONE_VERIFIED | README now documents the 1/3–3/3 scale. Validation matrix, final audit and handoff updated in place. |
| Exact-head CI for PR #139 | DONE_VERIFIED | Head `8558efd9f7690938be629c3d659d6701f4597898`: test and master-artifact passed in [41109778299](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41109778299) and [41109785725](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41109785725); Web static validation passed in [41109778408](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41109778408) and [41109786238](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41109786238). |
| Post-merge main CI | DONE_VERIFIED | Run [41110504231](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41110504231): `test` and `master-artifact` passed; generated master table asserted 351,780 rows and 41 vowel records. |
| Post-merge static validation | DONE_VERIFIED | Web static validation [41110501009](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41110501009) passed on main `720b528e0f6560912d87750158c510fc746a3044`. |
| Pages publication and served-CSS contract | DONE_VERIFIED | Pages run [41110501072](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41110501072): build, deploy and live-content checks passed. The published stylesheet was fetched using its versioned URL and checked for the strictness scale and 44px slider target. |
| Manual browser/device visual QA and WCAG 2.2 AA | PARTIAL / not performed | Automated static and published-content checks do not substitute for screenshot review, physical-device testing, keyboard/screen-reader checks or a full WCAG audit. |
| Linguistic accuracy | BLOCKED / evidence-limited | Independent expert-adjudicated Thai segmentation, IPA and Ukrainian target-form gold remains unavailable. UI and CI changes do not validate pronunciation accuracy. |

- PR #111 was superseded by PR #144 source-attested `ทร` lexical-exception task on an older base; it was not included in either UI merge.

## 2026-10-30 — Korean editorial reference applied; Thai copy closeout

| Component | State | Validation |
|---|---|---|
| User-facing Thai service copy | DONE_VERIFIED — merged in PR #129 | Applied the Korean service's user-oriented editorial pattern (commit `2a16bae3bb6d4297225d358180adcefa0f301de8`): task-first wording, concise output explanations, plain-language mode trade-offs and explicit uncertainty. Full exact-head CI run 41070939453 and static validation 41070939558 passed. |
| Researcher methodology framing | DONE_VERIFIED — merged in PR #129 | The system page identifies its researcher/developer audience and retains technical pipeline, IPA boundary, statuses, sources and evidence limits. Full exact-head CI and static validation passed. |
| Korean copy-edit reference | DONE_VERIFIED — editorial precedent applied | Reviewed Korean repository commit `2a16bae3bb6d4297225d358180adcefa0f301de8`. This is a reviewed copy revision, not a standalone formatter executable. No executable corrector invocation is claimed. |
| Thai UI copy contract | DONE_VERIFIED | Updated stale assertion for the revised homepage hint. Full CI passed UI contract and both test/master-artifact jobs; static validation passed. |
| Publication | PARTIAL | PR #129 merged as `2bb0e264ed74e4d10c1a0c59ecf1d1990bcb9241`; post-merge Pages/live-content verification not observed in this session. |
| Linguistic validation | BLOCKED / evidence-limited | No independent expert-adjudicated Thai segmentation, IPA and Ukrainian target-form gold set; copy changes do not affect or resolve this gate. |

## 2026-10-30 — service copy verification follow-up

| Component | State | Validation |
|---|---|---|
| Homepage copy contract | PARTIAL — stale assertion corrected | Initial CI failed because the test expected the previous hint string. Updated `web/tests/ui-contract.test.mjs` to assert the revised phrase. Web static validation run 41070448695 passed on head 49f7c4924ca851bfe2e7dfe46653cbd9965338ac; full CI run 41070448275 was still at master-table generation. Require a fresh full CI pass on the final documentation-updated PR head. |

## 2026-10-30 — public service copy vs researcher methodology

| Component | State | Validation |
|---|---|---|
| User-facing Thai service copy | PARTIAL — revised on PR #129 | Homepage copy now describes the input and three output forms in plain Ukrainian and explains the strict/soft/super-soft choice without implying that broader coverage means greater accuracy. Web static validation run 41070023201 passed on initial PR head; exact-head full CI and UI-contract test still required. |
| Researcher methodology page framing | PARTIAL — revised on PR #129 | Page title, navigation and introduction now identify the page as research/developer methodology; existing technical pipeline, evidence and limitation detail is preserved. Exact-head CI pending. |
| In-repository Ukrainian copy corrector | BLOCKED — no dedicated corrector/formatter found in tracked repository files or declared project dependencies | No execution can be claimed. Use existing static/UI-contract checks for HTML and required-copy regressions; if a specific corrector was intended, its path or dependency must be identified. |

## 2026-10-28 — UX/UI refresh post-merge acceptance

- **PARTIAL — code merged; published-content contract needs a marker correction.** Main commit `ad2f899978b66d3bbcb92124688b62261bb5225d`; PR exact-head CI and static validation passed, and the post-merge CI test job passed.
- Pages deployment run [40712965523](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40712965523) deployed the site, but its final live-content check failed on a stale privacy-copy marker. Correct expected text to `Текст аналізується локально у браузері`.
- Follow-up branch: `fix/pages-contract-and-ux-handoff-20261028`. Acceptance requires branch CI/static checks and a successful post-merge Pages live-content contract.
- Manual visual QA and real-device/accessibility testing remain unperformed; no WCAG certification or linguistic-accuracy claim.


## 2026-10-28 — IPA adaptation explained in the main flow; redundant input panel removed

- User-facing correction: the standalone “02 / IPA → УКРАЇНСЬКА” form duplicated an adapter that already runs in the main Thai-text pipeline. It is removed from the public homepage; IPA remains the mandatory internal boundary, not a second user workflow.
- The main method note now explains the actual flow (Thai text → structural/phonological analysis → IPA → Ukrainian adaptation), longest supported segment matching, aspiration apostrophes, standalone /h/ → «г», fail-closed unknown-segment handling, and neutralization of tone/length/stress. Per-syllable output continues to expose applied rules and neutralized features.
- Python/browser adapter modules and their unit tests remain intact. Only the duplicate homepage controls and their UI-specific test path are removed.
- Exact-head CI and Pages deployment are pending for branch `ux/integrate-ipa-adaptation-into-main-flow-20261028`; do not mark DONE_VERIFIED until CI, UI-contract tests, and the live published-content contract pass.
- Acceptance: homepage has no standalone IPA input IDs; main flow still exposes IPA and the per-syllable adaptation audit; unknown IPA segments remain fail-closed in adapter tests.

## 2026-10-27 — super-soft full-coverage fallback

- Added an opt-in **Суперм’який** browser mode for whole-text transcription. For unresolved Thai orthographic fragments it produces a provisional segmental IPA candidate, then obtains the Ukrainian candidate exclusively through the existing IPA → Ukrainian adapter.
- This mode is designed to avoid unresolved placeholders in the continuous Ukrainian/IPA output for Thai fragments. It preserves non-Thai spans, punctuation, whitespace, and numbers. It does not promise correct word segmentation, lexical reading, tone, or sound quality.
- Existing strict and soft modes remain distinct. Research-only morphology and open PRs #101/#104 are untouched.
- Acceptance gate: exact-head GitHub CI + Web static validation must pass; UI and parity regressions must verify full coverage on article-like inputs and prove each provisional Ukrainian form equals the adapter result for its IPA. No independent linguistic-accuracy claim is made.

| Component | State | Validation |
|---|---|---|
| Super-soft whole-text coverage | DONE_VERIFIED for code commit 6f53ca955a2702db8e070a04c181dbb68d6d6900; not merged/deployed | Web static run 40577745185 and full CI run 40577745331 passed, including browser parity/UI tests and master-artifact generation. Documentation-only checkpoint 502940ea61005b8b3494d074688301d23a1aeb29 follows the verified code commit. PR #105 remains draft because PR #104 overlaps changed files. Coverage is not pronunciation accuracy. |

## 2026-10-27 — direct IPA input and notation normalization

- Added a separate website IPA → Ukrainian panel for externally sourced Thai IPA. It calls the same `adaptIpaToUkrainian` adapter used by the Thai→IPA pipeline; no direct Thai-grapheme-to-Ukrainian path was added.
- Python and browser adapters normalize common presentation conventions: outer brackets/slashes, Thai tone letters, selected combining tone marks, stress, length, selected phonetic modifiers, and tied notation for the Thai alveolo-palatal affricate. Unknown segments and tone-only input are withheld.
- Regression coverage includes notation variants, direct UI adaptation, visible fail-closed behavior, and ambiguous combining breve U+0306 (which can mark extra-shortness and therefore must not be silently deleted).
- **DONE_VERIFIED for merged code at `070687575026ebc6d5d5dabdd0bb7bf647656bfc`:** exact-head CI [40569408788](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40569408788) passed, including `test` and `master-artifact`; Web static validation [40569408783](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40569408783) passed before merge. PR #103 was merged into PR #102's branch, then PR #102 was merged to `main`. A follow-up Pages workflow change adds a live contract check for the IPA panel and adapter; deployment result must be confirmed from the Pages run before claiming the public site is updated.
- **Not claimed:** successful parsing does not certify lexical IPA correctness or an official Ukrainian spelling. Independent IPA and Ukrainian-form adjudication remain open.

# Validation matrix

| Component | State | Validation |
|---|---|---|
| Direct IPA input + adapter normalization and delimiter validation | DONE_VERIFIED for merged implementation; public deployment verification pending | Python/browser tests cover common notation variants, ambiguous breve preservation, unknown symbols, and malformed `[.../`, `/...]`, unclosed `[` and stray `]`. Exact-head CI and generated master artifact passed on pre-merge head `e9295d26f41f278848396913b19b3877c2935c01`; Web static validation passed on the same head. Main merge commit: `070687575026ebc6d5d5dabdd0bb7bf647656bfc`. Pages workflow now checks the live IPA form and `src/ipa-ua.js`; require that deployment job to pass before marking the live-site acceptance criterion DONE_VERIFIED. These tests validate software contracts, not transcription accuracy or official Ukrainian spellings. |
| Pasted Wikipedia/Markdown/HTML input cleanup | DONE_VERIFIED — code fix and published-page contract passed | PR #91 fixed nested IPA-link cleanup; PR #93 corrected the live contract to check `softSyllabify` in `engine.js`. Post-merge Pages run [40509900075](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40509900075) succeeded, including the published whole-text UI contract; static validation [40508000658](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40508000658) and main CI [40509900074](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40509900074) passed.
| External G2P license/provenance gate | PARTIAL — TLTK license scope is contradictory in current repository artifacts; FastThaiG2P bundled dictionary/fallback provenance not cleared | TLTK README.rst/setup.py say BSD-3-Clause while root LICENSE contains LGPL v3 and LICENSE.txt contains BSD-style terms. No external code/data imported. Acceptance: authoritative clarification of applicable TLTK license by file/version, and resource-level license/provenance audit for any selected model or dictionary. |
| 44 consonant graphemes | implemented | inventory tests |
| 5 lexical tone categories | implemented | tone engine |
| tone mark vs tone | implemented | separate model fields |
| live/dead syllables | implemented | structural fixtures |
| vowel/rime registry | implemented | parser + source registry consistency test |
| implicit vowel flagging | implemented conservatively | negative fixtures |
| onset/coda distinction | implemented | กรา / กาน / carrier-coda negative test |
| feature-ranked Ukrainian candidates | implemented | deterministic adapter |
| broad IPA composition | implemented | pipeline tests |
| connected-speech phonetics | partial | intentionally conservative |
| lexical segmentation | PARTIAL | pinned CC0 dictionary max-match and separate 60,963-entry lexicon; evaluated on held-out Wisesight but current baseline is weak; no claim of production-quality segmentation |
| TUD Viterbi word-segmentation model | PARTIAL — reproducible research model exists but is not used by the production browser engine | Pinned UD Thai TUD source commit `67413969add552b7030184f16f24fa9f630913bc`, CC BY-SA 4.0; 5,319-word unigram model. Held-out TUD test boundary F1 `0.872932`; Wisesight source-annotated test-only F1 `0.792101`, precision `0.6592`, recall `0.9921`, 0 expert-adjudicated rows. Model artifact `thai-tud-word-segmentation-model-and-report` (run `40503671201`, artifact `12734023167`). Candidate only for opt-in provisional segmentation; production integration requires browser/Python parity, license attribution/share-alike handling, and representative expert-reviewed error analysis.
| Source-attested three-syllable word `ตะวันออก` | PARTIAL — exact-head CI exposed missing IPA for `ออก`; source-pinned lexical IPA override and Python/browser regressions added on `feat/source-attested-east-thai-lexicon-20261027`; revalidation pending | Pinned en.wiktionary revision 86398986 records `ตะ-วัน-ออก` and `/ta˨˩.wan˧.ʔɔːk̚˨˩/`. Initial CI failed because the parser returned no IPA for `ออก`; the follow-up uses a pinned source-attested `ʔɔːk` override with low tone and long vowel, still routed through typed IPA → Ukrainian adaptation. Exact-head CI and static validation must pass before merge. This is not independent expert/acoustic gold or a general accuracy claim. |
| Source-attested Europe / Eastern Europe lexical forms | PARTIAL — source-pinned lexical segmentation and Python/browser pipeline assertions added; latest-head CI pending | en.wiktionary revision 91325849 attests `ยุโรป` / `/ju˦˥.roːp̚˨˩/`; revision 87721830 attests `ยุโรปตะวันออก` / `/ju˦˥.roːp̚˨˩.ta˨˩.wan˧.ʔɔːk̚˨˩/`. Tests require `йуроп` and `йуроптаванок` from the typed IPA adapter. Source-attested only; not independent expert/acoustic gold or a general accuracy claim. |
| Source-attested proper-name reading `ยูเครน` | DONE_VERIFIED — PR #94 merged; post-merge CI and Pages deployment passed | Pinned en.wiktionary revision 88025965 attests `/juː˧.kʰreːn˧/` and two syllables `ยู|เครน`; the implementation routes both syllables through the existing typed IPA → Ukrainian adapter. Exact-head CI [40510490288](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40510490288), post-merge main CI [40511892392](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40511892392), and Pages deployment [40511892093](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40511892093) passed. This is source-attested lexical evidence, not independent expert/acoustic gold and not evidence of general G2P accuracy. |
| Article-style G2P challenge probes | PARTIAL — merged in PR #95; CI and optional external smoke passed; evidence remains unadjudicated | Six target-relevant probes cover `ยูเครน`, country-name compounds, continuous Thai prose and Eastern Europe. Branch CI [40510716596](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40510716596), optional external smoke [40510554606](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40510554606), and post-merge main CI [40511892392](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40511892392) passed. Run [40507249579](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40507249579) preserves 126 raw outputs across three engines. No independent gold labels exist; this is a diagnostic set, not an accuracy benchmark. |
| Browser segmentation latency diagnostic | DONE_VERIFIED as a reproducible non-gating runtime diagnostic; not an accuracy benchmark | Post-PR #85 CI artifact [12739570652](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40513578523) on Node v22.23.3, 5 warmups / 30 samples: target 100 → actual 113 code points, median/p95 2.102/3.294 ms; target 250 → actual 261, 5.636/8.600 ms; target 500 → actual 500, 7.386/11.115 ms. Inputs append complete Thai lexical units rather than slicing arbitrary code points. These measurements are runner/JIT-dependent and say nothing about segmentation correctness or phonetic accuracy. |
| corpus validation | infrastructure implemented | external licensed JSONL; no CI gold corpus claimed |
| malformed syllable surface rejection | implemented | repeated tone/vowel signs, concatenated material and unsupported-symbol probes |
| calibrated probability | not claimed | calibration dataset still required |
| strict/soft browser modes | DONE_VERIFIED — published UI contract passed; empirical phonological quality remains PARTIAL | Main Pages run [40509900075](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40509900075) confirms the deployed whole-text UI, selector and served engine markers. This verifies deployment wiring, not pronunciation accuracy; soft mode remains provisional and strict mode abstains on unsupported spans.


| tone-bearing class in consonant clusters | implemented for declared cluster rule | separate `tone_class` field + adversarial cluster fixture |
| parser/source vowel-ID consistency | implemented | registry regression |


| machine-readable tone rules | implemented | `data/thai/tone_rules.csv` + data-driven engine |
| special orthography registry | implemented conservatively | `รร`, `ฤ/ฦ`, `์`, `ทร`, `อ นำ` become explicit analysis-dependent cases |
| source → parser → derived consistency | implemented | generated source-final manifest + CI diff check |
| Ukrainian orthographic target | implemented as project candidate layer | deterministic candidate renderer; explicitly not an official standard |


Current readiness status — 2026-10-24

- Current main HEAD at this checkpoint: `822797042dd3f6980202c2f92e491f2a53df80b0`; current-main CI [40096100740](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40096100740) passed generated-data checks, master-table generation, Python tests, Node IPA-to-UA tests, and Python/browser parity. Master-table assertions passed for 351,780 rows and 41 vowel records.
- The final-velar-stop regression for ตรอก is present and passing; its test asserts onset ต ร, coda ก, and Ukrainian final к.
- Optional external G2P smoke: run [40507249579](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40507249579), 42 inputs / 126 raw outputs, zero independently gold-labeled rows. thaiphon 0.7.0 and FastThaiG2P 0.1.0 emitted output for all 42; pinned Goruut returned no words on 16/42. Six article-style cases are preserved in `data/benchmark/runs/article-style-external-g2p-2026-10-27.json`. This is a raw-output diagnostic, not an accuracy benchmark.
- Engineering validation: DONE_VERIFIED. Empirical accuracy, lexical coverage, calibrated confidence, and broad connected-speech claims: TODO/BLOCKED until independently adjudicated data and explicit scope criteria exist.
- Latest observed Pages deploy passed at 40091525305 for code-equivalent site sources; an exact current-HEAD redeploy has not been observed.


## Current validation status — 2026-10-24

## Evidence-gated completion update — 2026-10-25

| Component | State | Evidence / acceptance boundary |
|---|---|---|
| Wisesight source-annotated word-boundary set | DONE_VERIFIED | 993 rows, CC0-1.0, pinned upstream commit/blob SHA, exact reconstruction check, test-only split; status explicitly `SOURCE_ANNOTATED`, not expert-adjudicated |
| Segmentation scorer source-status handling | DONE_VERIFIED | Scores `ADJUDICATED` and `SOURCE_ANNOTATED` separately; rejects mixed-grade gold sets; whitespace-only boundaries excluded |
| ClippyFirst segmentation baseline | DONE_VERIFIED (baseline only) | CI runs `scripts/run_wisesight_segmentation_diagnostic.py` and uploads JSON; baseline is expected to expose the current no-auto-segmentation limitation, not prove a production score |
| Source-attested IPA/tones/length contrasts | DONE_VERIFIED (source-attested only) | Seven pinned Wiktionary entries; `SOURCE_ATTESTED_NOT_GOLD`; includes short /ɤ/ in เงิน vs long /ɤː/ in เดิน |
| Runtime lexical coverage | PARTIAL | Five source-backed challenge lexicon entries added; diagnostic must report new counts; not representative coverage |
| Typed source-attested lexical IPA overrides (เงิน, เดิน) | IMPLEMENTED; exact-head CI pending | Pinned Thai Wiktionary revisions; typed IPA→UA adapter path; grapheme-only ambiguity remains separate; source agreement from an injected override is excluded from independent-comparison metrics |
| Independent expert/acoustic IPA gold | BLOCKED | CCOST license/annotation manual and local scope must be reviewed, then an independent Thai phonetician must adjudicate a pinned sample with disagreement log and speaker-aware split |
| Context-dependent `รร`, `ฤ/ฤๅ`, `ฦ/ฦๅ`, `ทร`, silent letters | PARTIAL | Keep lexical/context-dependent abstention until source-located readings and independent review exist |
| Connected speech and Ukrainian target preference | BLOCKED | Requires acoustic evidence and a separately adjudicated Ukrainian target preference set |

The Wisesight rows establish a usable source-annotated segmentation benchmark; they do **not** satisfy the independent-expert criterion. The IPA dataset remains source-attested-only, with no accuracy claim.


- The fail-closed unknown-word correction merged in PR #27 as `975bd0504ad05392e277f00d85b746d21c5fe729`. Unknown multi-grapheme words no longer expose whole-word syllable/IPA/Ukrainian output without lexical segmentation; curated lexicon entries are unchanged.
- Engineering validation is DONE_VERIFIED on the current code path: Python tests, Python/browser parity, build, master-artifact validation and deployment have passed on recent main-equivalent runs. This is separate from phonological accuracy.
- Latest external smoke evidence is being reconciled in PR #41: 36 inputs, 72 outputs, 0 runtime errors; `thaiphon` and FastThaiG2P agree exactly on 13/36 inputs, and on 14/36 after a tone-only diagnostic. The diagnostic is not an accuracy metric; independent gold count remains zero.
- Empirical accuracy, lexical coverage, calibrated confidence and broad connected-speech claims remain TODO/BLOCKED until a representative, independently adjudicated held-out corpus and explicit scope criteria exist.


## Current validation status — 2026-10-25 (PR #71)

- **DONE_VERIFIED — software gates:** exact-head CI test job [40229701920](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40229701920) passed generated-data drift checks, master-table generation, 143 Python tests, runtime diagnostic guards, IPA→Ukrainian adapter tests, Python/browser parity (27 fixtures) and UI contract checks.
- **DONE_VERIFIED — evaluator integrity:** only prediction rows with `status=ok` score; non-success rows abstain; boundary F1 handles zero predicted boundaries correctly; empty runtime challenge inputs fail closed.
- **PARTIAL — challenge runtime:** challenge set expanded from 36 to 42 with six article-style Thai probes. The external run is reproducible, but all gold IPA/boundary fields remain null; no pronunciation accuracy or lexical-coverage claim is supported.
- **PARTIAL — special orthography:** source-backed lexical cases and conservative analysis-dependent statuses exist. PR #68 is a separate green but currently non-mergeable branch; no automatic merge was performed.
- **BLOCKED — empirical validation:** zero independently adjudicated Thai IPA/word-boundary gold rows; CCOST requires license-compliant local handling and independent adjudication; a segmentation holdout still needs exact version, license, annotation convention, split and hash.
- **BLOCKED — broader claims:** connected-speech phonetics, calibrated probability and Ukrainian orthographic preference require separate evidence sets.
- **Environment limitation:** local clone/test commands were not executed because GitHub DNS resolution failed; remote CI is the test evidence.


## Exact-head CI outcome — 2026-10-25

- Code-bearing acceptance commit: `818a378d37b248d74628243b9a8d62fb82029815`.
- GitHub Actions run [40233825012](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40233825012) passed both `test` and `master-artifact` jobs.
- Python suite: 150 tests passed. Generated-data drift check passed. Master generator passed; artifact guard confirmed 351,780 rows and 41 vowel/rime records. Challenge diagnostic ran all 36 forms. Node IPA→UA, Python/browser parity and UI contract checks passed. Wisesight diagnostic passed and artifact `wisesight1000-segmentation-baseline` (artifact ID `12614106636`) uploaded.
- Wisesight source-annotated baseline: 993/993 predictions emitted; boundary precision 0.6383, recall 0.0919, F1 0.1606; exact sequence rate 0.0312. Evidence status is `SOURCE_ANNOTATED`, not expert-adjudicated.
- Challenge runtime diagnostic: lexicon resolution 28/36; complete output 25/36; 11 abstentions/incomplete outputs. This is not an accuracy estimate.

The latest code-bearing commit is engineering-verified by the above run. A documentation-only reconciliation commit follows this matrix update; its own CI must be checked before claiming the final branch head is green.


## Final documentation-head check — 2026-10-25

- Documentation head `b3eaddde55de0474e47abe01ece7692467f1a229` passed both CI jobs in [run 40234324067](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40234324067).
- This confirms the source-annotated benchmark, 150 Python tests, generated-data drift check, Python/browser parity, UI contract, 993-row baseline artifact and master-table artifact all remained green after the audit/matrix/handoff updates.
- A final wording-only audit JSON reconciliation follows this checkpoint; no code/data changes are included. Its own CI is pending and will be checked before ending this run.


## Text-evidence continuation — 2026-10-25

| Workstream | Status | Evidence / acceptance |
|---|---|---|
| Text-attested IPA registry | PARTIAL | `data/benchmark/source-attested-ipa.tsv` pins six Thai Wiktionary revisions; status remains `SOURCE_ATTESTED_NOT_GOLD`. These records are dictionary evidence, not independent or acoustic gold. |
| Runtime lexical IPA override | PARTIAL | `data/thai/lexical_ipa_overrides.tsv` contains six exact-form, source-pinned dictionary readings, including short /ɤ/ in `เงิน` and short /ɤ/ + falling tone in `เพิ่ง`. Each is explicitly `ACTIVE_SOURCE_ATTESTED_NOT_GOLD`; the IPA-first adapter and warning preserve that evidence grade. Coverage remains narrow and is not an accuracy claim. |
| Word-boundary corpus | PARTIAL | Pinned Wisesight 993-row CC0 source-annotated snapshot remains test-only. No use for training or dictionary construction; it is not independently re-adjudicated. |
| Automatic word segmentation | TODO | No production segmenter is claimed. A valid implementation needs training data distinct from the pinned test snapshot and an untouched, source-annotated evaluation set. |
| Orthographic exceptions | PARTIAL | `รร`, `ฤ/ฤๅ`, `ฦ/ฦๅ`, `ทร`, and silent letters remain lexical/context dependent; no universal rule inferred from a few examples. |
| Connected speech / Ukrainian target preferences | BLOCKED for empirical claims | Textual transcription analysis and consistency checks are feasible; acoustic validation and independent Ukrainian target-form adjudication are not established by the current text-only evidence. |

Verified code/data head: [CI 40238202167](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40238202167) and [Web static validation 40238202181](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40238202181) passed on `43687b2753379b1d617b1c925f87358f8aad13bd`. The final documentation head `6a153e26e17c4929fdc166b3dbeb73444668f2b1` also passed [CI 40238672074](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40238672074) and [Web static validation 40238671983](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40238671983). This is engineering verification, not a phonetic-accuracy claim.


## Latest text-only implementation checkpoint — 2026-10-25

| Task | Status | Evidence / acceptance |
|---|---|---|
| Typed lexical IPA override for `เงิน` | PARTIAL | Source-pinned override is active in Python and browser, runs through the IPA→Ukrainian adapter, and carries `SOURCE_ATTESTED_NOT_GOLD` provenance. Exact-head browser CI and Web static validation passed on the code head; the final documentation-only head also passed. |
| Text pipeline routing and parity | PARTIAL | Python text pipeline recognizes the override; browser engine and text UI have matching fixture assertions. Exact-head CI passed after the fixture expectation/order correction. |
| Source-attested IPA discrepancy diagnostic | DONE_VERIFIED on current code/data checkpoint | Seven source rows; five rows are circular because the same dictionary source feeds runtime overrides; two non-circular, complete rows remain independently comparable. The diagnostic is `SOURCE_ATTESTED_NOT_GOLD` and reports no accuracy score. |
| Corpus license/access registry | DONE_VERIFIED on prior code/data checkpoint | Wisesight 993-row source-annotated test-only snapshot; LST20 and VISTEC candidate gates; CCOST CC BY-NC-SA 4.0 and 6.2 GB TextGrid archive recorded. |
| Automatic word segmentation | TODO | No production segmenter or distinct license-cleared training corpus. Wisesight remains test-only. |
| Independent IPA/tone/length gold and Ukrainian target gold | BLOCKED | Requires independent adjudication and, for acoustic claims, access to the matching audio. |

## Follow-up implementation batch — 2026-10-26


| TUD statistical segmentation experiment | IMPLEMENTED; exact-head CI pending | Pinned UD Thai TUD commit 67413969add552b7030184f16f24fa9f630913bc; train-only token counts, dev-only penalty selection, separate TUD test and Wisesight test-only report; CC BY-SA 4.0 obligations recorded |
| Independent IPA/acoustic gold | BLOCKED | Requires independent Thai phonetician adjudication, agreed broad-vs-surface transcription protocol, and authorized CCOST recording/TextGrid access |
| Final glottal stop in บรรจุ | PARTIAL / EVIDENCE-LIMITED | Dictionary IPA and engine disagree; no global phonological rule is added. Need agreement on transcription level, stress/context, and independent adjudication |
| Ukrainian target-form preferences | BLOCKED | Existing adapter and generated candidates establish reproducibility only; require independently adjudicated Ukrainian candidate choices and written criteria |


## Continuation status — 2026-10-26

| Component | State | Evidence / next acceptance criterion |
|---|---|---|
| Dictionary max-match segmentation | PARTIAL | Opt-in baseline and pinned dictionary exist; Wisesight source-annotated metrics are diagnostic only. Keep distinct from adjudicated gold. |
| TUD unigram-Viterbi research segmenter | PARTIAL — research metrics measured | Exact-head CI passed: held-out TUD test boundary F1 0.872932 (375 groups), exact-group rate 0.432; Wisesight test-only F1 0.792101 (2,848 filtered groups). Not independent expert gold, not full-text metrics, not production default; preserve CC BY-SA 4.0. |
| `เดิน` lexical IPA | PARTIAL | Typed source-pinned override `/dɤːn˧/` is separate from parser-only vowel-length ambiguity and routed through IPA→Ukrainian adapter; regression expectations fixed, exact-head CI pending. Not independent gold. |
| `บรรจุ` final `/ʔ/` | BLOCKED | Source/transcription-level discrepancy remains unresolved; requires qualified Thai phonology/phonetics review with exact transcription conventions, not a global rule patch. |
| Independent IPA/acoustic gold | BLOCKED | No independently adjudicated IPA/audio labels currently available. CCOST is a candidate only; access, annotation, and NC-SA conditions must be satisfied before a gold claim. |
| Independent Ukrainian target forms | BLOCKED | Template/protocol exists; independent Ukrainian-language review and source-scoped decisions are still needed. |
| Exact-head CI for code/data head `4c3d01d9b726b410c98048878441082d8d5c8299` | DONE_VERIFIED | CI run `40296520186` and Web static validation run `40296520175` passed; 176 Python tests, Node IPA→UA/parity/UI, generated-artifact checks, diagnostics, TUD training and artifact uploads passed. Recheck final documentation-only head separately. |


## Verified checkpoint — 2026-10-26

- Exact code/data head: `4c3d01d9b726b410c98048878441082d8d5c8299`; CI [40296520186](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40296520186) PASS; Web static validation [40296520175](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40296520175) PASS.
- Candidate TSV regeneration check now passes byte-for-byte; malformed quoting of JSON fields was the prior failure and is fixed.
- Source-attested IPA diagnostic: 6 records, 2 circular source overrides excluded, 4 comparable records, 3 segmental agreements, 4 tone agreements; `SOURCE_ATTESTED_NOT_GOLD`, no accuracy claim.
- Wisesight-1000: 993 source-annotated rows, 0 adjudicated. Text tokenizer F1 0.160604; dictionary max-match F1 0.839471; exact sequence rates 0.031219 and 0.193353 respectively. Diagnostic only, not expert gold.
- TUD research segmenter: dev F1 0.889023; held-out TUD test F1 0.872932 (375 groups); Wisesight test-only F1 0.792101 (2,848 filtered groups). TUD labels inherit source tokenization; no production integration decision or independent accuracy claim.
- Readiness remains **research prototype / not release-ready**. Independent phonetic/acoustic gold, Ukrainian target-form adjudication, and context-specific resolution of `บรรจุ` remain evidence-limited.


## Final continuation review — 2026-10-26

| Workstream | State | Verified result / next acceptance |
|---|---|---|
| Final documentation HEAD | DONE_VERIFIED | CI [40297155713](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40297155713) passed test + master-artifact jobs; Web static validation [40297155831](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40297155831) passed on `cb8832ca99e4ccce53b6fb2b6988b5945acaad71`. |
| TUD unigram-Viterbi segmenter quality review | PARTIAL — production integration declined for now | Held-out TUD: boundary P/R/F1 0.7886/0.9775/0.8729; exact-group rate 0.432. Wisesight test-only: P/R/F1 0.6592/0.9921/0.7921; exact-group rate 0.3852. F1 falls by 0.080831 cross-domain; recall-heavy profile and low exact sequence rates do not justify production-default integration. These are filtered groups, not full-text scores or independent expert gold. Next: manual error analysis, deployment thresholds, and independent untouched-domain review. |
| Independent IPA/acoustic gold | BLOCKED | Needs qualified independent Thai phonetician, agreed transcription-level protocol, and authorized audio/TextGrid access; acceptance requires independent labels and a disagreement log. |
| Ukrainian target forms | BLOCKED | Needs independent Ukrainian-native reviewers, blinded criteria-based judgments, and a disagreement log. |
| `บรรจุ` final `/ʔ/` | PARTIAL / EVIDENCE-LIMITED | Keep discrepancy open until context/transcription-level expert adjudication; do not add a global rule. |
| Release readiness | NOT READY | Engineering checks pass, but empirical pronunciation/target-form gold and production segmentation quality are not established. |


## Special-letter source contract — 2026-10-26

- The official OBEC/IPST guide registered as `SRC-OBEC-SPECIAL-VOWELS-2022` (p. 5 for special vowel letters; printed p. 275 in separate source `SRC-OBEC-O-NAM-2022` for อ นำ ย) supports classifying `ฤ`, `ฤๅ`, `ฦ`, and `ฦๅ` as syllabic/lexical constructions and documents the lexical `อ นำ ย` family `อย่า`, `อยู่`, `อย่าง`, `อยาก`.
- The parser deliberately continues to return `analysis-dependent:special-orthography` with no IPA or Ukrainian output for isolated special vowel letters. The source is a scope constraint, not a universal word-reading or pronunciation gold set.
- Python/browser fail-closed regressions passed in exact-head CI [40315032771](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40315032771); Web static validation [40315032788](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40315032788) passed. This verifies uncertainty handling and source-registry integrity, not universal IPA readings or pronunciation gold.


## Mandatory pipeline architecture gate — 2026-10-26

| Gate | Required contract | Status |
|---|---|---|
| Thai → IPA → Ukrainian serial flow | Thai structural/phonological analysis produces the typed IPA intermediate; Ukrainian output is generated from that IPA, not via a parallel grapheme-to-Ukrainian path | DONE_VERIFIED for tested paths — typed PhoneticResult is the Python adapter input; exact-head CI 40315032771 passed |
| IPA adapter input contract | Ukrainian adapter consumes typed IPA and documented metadata; it does not independently read Thai graphemes, vowel IDs or coda fields | DONE_VERIFIED — Python IPA mutation test and browser end-to-end adapter test pass; adapter modules do not read Thai graphemes |
| Fail-closed uncertainty | Unsupported/ambiguous Thai analysis cannot yield an unjustified IPA or confident Ukrainian result | DONE_VERIFIED for tested special letters and unsupported/empty/uncertain IPA — no confident Ukrainian output leaks from these cases |
| End-to-end data-flow coverage | Tests establish Thai input → exposed IPA → Ukrainian output and that withholding/changing the IPA intermediate changes/withholds dependent target output | DONE_VERIFIED — end-to-end IPA mutation and fail-closed tests pass in Python and browser |
| Feature preservation | Phonemic/surface distinction, tone, vowel length, syllable/segment boundaries, provenance and uncertainty survive to the IPA boundary | DONE_VERIFIED for tested metadata — tone, vowel length, syllable boundaries, provenance and uncertainty are asserted; broad surface IPA remains separately inspectable |
| Python/browser parity | Both runtimes implement the same boundary and derive Ukrainian output from equivalent IPA results | DONE_VERIFIED — 180 Python tests, 28 parity fixtures and browser/UI checks passed on exact head cb775d6156f62392fa2d0f4bcf8d1aa30d219530; this is not linguistic gold |

**Resolved exact-head regression — 2026-10-26:** The 12 failures in CI [40313439910](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40313439910) came from four special-letter rows missing their `pattern` column in `data/thai/special_orthography.csv`. The resulting positional shift made `analysis_status` contain IPA candidates and prevented the parser from recognizing the special letters. The data rows were repaired in commit `a0bd6f598c5117154db1c78f02ae25b6d6fbf1bc`; tests now assert each row's pattern, status, candidates, and source provenance.

Exact-head CI [40315032771](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40315032771) passed both jobs: 180 Python tests, generated-data drift, 351,780-row master artifact with 41 rime records, Node IPA→Ukrainian, 28 Python/browser parity fixtures, UI contract, challenge/Wisesight/source-attested IPA diagnostics, candidate registry check, TUD research training/evaluation and artifact uploads. Web static validation [40315032788](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40315032788) passed. The IPA-first boundary now has mutation and fail-closed regression tests in both runtimes. These checks verify software behavior only; they do not supply independent Thai IPA gold or Ukrainian target-form adjudication.


## Exact-head verification refresh — 2026-10-26

| Gate | Latest verified evidence | State |
|---|---|---|
| Python and repository CI | [Run 40316202183](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40316202183), documentation checkpoint `4c61866d98312e8cf08f78bc8ab0f213bc8dc8c0`; 180 Python tests and both CI jobs passed | DONE_VERIFIED for that checkpoint |
| Generated master artifact | Same run; 351,780 rows, 41 vowel/rime records; artifact uploaded | DONE_VERIFIED for that checkpoint |
| Python/browser IPA→Ukrainian and parity | Same run; Node adapter, 28 parity fixtures and UI contract passed | DONE_VERIFIED for tested contract; not phonetic accuracy |
| Web static validation | [Run 40316202145](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40316202145) passed | DONE_VERIFIED for that checkpoint |
| TUD research segmenter | TUD held-out boundary F1 0.872932 / exact-group rate 0.432; Wisesight source-annotated test-only boundary F1 0.792101 / exact-group rate 0.385 | PARTIAL; research-only, not production default |
| Independent Thai IPA/acoustic gold | No independent adjudicated rows; CCOST audio/TextGrid access and annotation protocol not yet completed | BLOCKED — qualified Thai phonetician, lawful pinned assets, independent labels and disagreement log required |
| Ukrainian target-form preference | No independent adjudication set | BLOCKED — two independent Ukrainian-native reviewers, frozen criteria and adjudication log required |
| `บรรจุ` final `/ʔ/` | Source-attested discrepancy retained; no global rule | PARTIAL — transcription layer, stress/context and lexical evidence must be adjudicated |
| Segmentation production readiness | No representative manual false-split/false-merge review or independent untouched-domain evaluation | PARTIAL — publish error analysis, predefine deployment thresholds and evaluate independent licensed data |
| Release readiness | No independent IPA/UA gold; segmentation remains research-only; special orthography remains evidence-gated | NOT RELEASE-READY |

The latest verified checkpoint above is not automatically evidence for later documentation commits. The audit/handoff synchronization that follows must itself pass exact-head CI and Web static validation. Engineering tests must not be reported as linguistic accuracy.


## Segmentation error review — implementation added 2026-10-26

| Task | State | Evidence / acceptance boundary |
|---|---|---|
| Deterministic false-split/false-merge report | DONE_VERIFIED — software/report contract | Exact-head CI [40320450844](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40320450844) passed 182 Python tests and the evidence-grade/error-report gate; Web static validation [40320450587](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40320450587) passed. Artifact `thai-segmentation-error-review` contains 993 source-annotated rows, 2,574 false splits, 1,981 false merges, boundary F1 0.839471 and 192/993 exact sequences; artifact ID `12648833301`. |
| Evidence-grade separation | Required gate | The 993 rows are `SOURCE_ANNOTATED`, CC0-1.0, test-only, with zero independent expert-adjudicated rows. The report is triage, not independent gold. |
| Human error review / production decision | PARTIAL | The generated artifact is a deterministic triage aid, not human adjudication. Inspect representative false splits and false merges, document error categories, set acceptance thresholds in advance, and evaluate an independent untouched domain. Until then, keep both dictionary and TUD segmenters out of production-default selection. |

The code-bearing report was added in `e80606e641d631966b566999027ee9d2b4d00bb`; exact-sequence tuple/list parity was corrected in `bec1b7027f34a4f70f0b6f9fdc415ef43343eab9`, with regression `aba6832eb97cb4b84f2e62fa058fa963cfb34803` and CI assertion `c189cdb9209d85780c3baeb1df23800101840b16`. The first artifact's zero exact-sequence count was a type-comparison bug and is superseded. Exact-head CI and Web static validation for the final branch head are required before this is marked DONE_VERIFIED.


## Comparative segmentation error review — 2026-10-26

| Task | State | Evidence / acceptance boundary |
|---|---|---|
| Dictionary false-split/false-merge triage | DONE_VERIFIED — report software | Exact-head CI [40320450844](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40320450844) verified the 993-row source-annotated report, including 2,574 false splits, 1,981 false merges and 192 exact sequences. This does not independently adjudicate each difference. |
| Same-row dictionary vs TUD error comparison | DONE_VERIFIED — report software and same-row metrics | Exact-head CI [40323209539](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40323209539) passed both jobs; Web static validation [40323209471](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40323209471) passed. Artifact from code checkpoint [40322960615](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40322960615): same 993 rows; dictionary F1 0.839471 / exact 192 (19.34%); TUD F1 0.748623 / exact 119 (11.98%). TUD false splits 8,722 vs dictionary 2,574; all labels are source-annotated, not expert gold. |
| Preliminary error-pattern notes | PARTIAL — non-expert triage only | Existing report samples visibly include numeric/punctuation and URL/Latin fragmentation, brand/name handling, and inconsistent token granularity for longer Thai sequences. These are candidate review strata, not expert-linguistic error labels; the source annotation itself may reflect its own conventions. |
| Production segmentation | PARTIAL — not accepted for production | Require a representative manually reviewed sample, predeclared acceptance thresholds, an independent licensed untouched domain, and explicit integration decision. Wisesight is source-annotated and test-only, not independent expert gold. |

The comparative report is deliberately scheduled **after** the pinned TUD training step so it consumes the exact generated model from that run. CI asserts both engines have false-split and false-merge examples and that the shared evaluation set still has zero expert-adjudicated rows. No comparative metrics are claimed until the new exact-head workflow passes.


### Verified same-row comparative result — 2026-10-26

| Engine | Boundary precision | Boundary recall | Boundary F1 | False splits | False merges | Exact token sequences |
|---|---:|---:|---:|---:|---:|---:|
| Dictionary max-match | 0.822287 | 0.857390 | 0.839471 | 2,574 | 1,981 | 192/993 (19.34%) |
| TUD unigram-Viterbi | 0.608000 | 0.973868 | 0.748623 | 8,722 | 363 | 119/993 (11.98%) |

Both engines were evaluated against the same 993 pinned Wisesight rows using the same full-text boundary policy, with non-Thai runs preserved. This is more comparable than the earlier TUD-only metrics on filtered Thai-only runs; those filtered metrics must not be directly compared with the full-text row above. The TUD system is strongly recall-heavy and over-splits on this full-text evaluation, while the dictionary baseline has better boundary F1 and exact-sequence rate. These source-annotation metrics support **not integrating TUD as production default**, but they do not establish linguistic gold accuracy.

- Code checkpoint CI [40322960615](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40322960615): both comparative-report and evidence-grade steps passed; artifact `thai-segmentation-comparative-error-review`, ID `12649094231`, SHA-256 `8005cc91939ea06b852c1717fee9fb72d370709e74267b8f99636a6476d30775`.
- Final documentation HEAD `e4ab3fd46e9c48c4220afb1f73ae5c6127b328ff): full CI [40323209539](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40323209539) passed `test` and `master-artifact`; Web static validation [40323209471](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40323209471) passed.
- Evidence grade remains `SOURCE_ANNOTATED`; expert-adjudicated rows = 0. Human review and independent-domain evaluation remain separate production acceptance gates.


## Comparative segmentation review handoff — 2026-10-26

| Task | Status | Evidence / acceptance criterion |
|---|---|---|
| Comparative JSON artifact inspection | DONE_VERIFIED | Run 40322960615, artifact 12649094231, digest `8005cc91939ea06b852c1717fee9fb72d370709e74267b8f99636a6476d30775`; artifact JSON independently parsed and metrics/provenance checked |
| Same-row dictionary vs TUD comparison | DONE_VERIFIED (source-annotated diagnostic only) | 993 rows; dictionary F1 0.839471 / exact 192; TUD F1 0.748623 / exact 119; 0 independently adjudicated rows; TUD remains research-only |
| Human-review TSV generator | PARTIAL pending exact-head CI | Script joins complete pinned source text and both available predictions, checks lossless reconstruction, adds heuristic strata and blank adjudication fields; acceptance: tests + CI artifact validation + exact-head Web static validation |
| Independent segmentation adjudication | BLOCKED | Qualified Thai reviewers must adjudicate a prespecified sample, document tokenization convention and disagreements, and produce stable IDs and decision rationale; do not tune on the test set |
| Independent Thai IPA/acoustic gold | BLOCKED | Thai phonetician/acoustic evidence and pinned lawful corpus with adjudication log |
| Independent Ukrainian target forms | BLOCKED | Two independent Ukrainian-language reviewers, blinded candidate review and documented resolution |
| `บรรจุ` final /ʔ/ | BLOCKED | Context and transcription convention must be specified, then source/audio evidence independently reviewed |
| Cross-domain segmentation evaluation | TODO | Identify license-compatible independent domain, freeze split and acceptance thresholds before any tuning |
| Full OBEC official PDF | BLOCKED | Obtain accessible official full PDF or verified local official copy; inspect full relevant pages before broadening claims |


## One-pass execution ledger — 2026-10-26 (current continuation)

| Task | Status | Evidence / acceptance criterion |
|---|---|---|
| IPA-first pipeline and Python/browser adapter boundary | DONE_VERIFIED on prior exact-head CI | Typed IPA carries tone/length/boundary/provenance/uncertainty; mutation and fail-closed tests exist. Latest-head CI is tracked separately below. |
| Dictionary vs TUD segmentation comparison | DONE_VERIFIED on comparative artifact head | Same 993 pinned CC0 Wisesight source-annotated rows; dictionary F1 0.839471 / 192 exact sequences, TUD F1 0.748623 / 119 exact sequences. These are source-label diagnostics, not independent accuracy. Keep TUD research-only. |
| Human segmentation-review sample design | PARTIAL; new implementation awaiting exact-head CI | Deterministic stratified sample plus uniform controls, full predictions for all source rows, exact reconstruction and blank adjudication fields. Acceptance: CI pass, artifact inspection, then human review. |
| Independent Thai IPA/acoustic gold | BLOCKED — external specialist + authorized audio required | CCOST is a public candidate under CC BY-NC-SA 4.0, but its manual/archive/hash and use scope still need review; qualified Thai phoneticians must independently annotate and reconcile a speaker-aware sample. |
| Independent Ukrainian target-form judgments | BLOCKED — two Ukrainian-native reviewers required | Complete existing TSV with independent blind preferences, criteria version, rationale, agreement and adjudication log. Do not infer target preference from IPA or engine output. |
| บรรจุ final /ʔ/ | PARTIAL / evidence-limited | Thai Wiktionary revision 5686263 explicitly records /ban˧.t͡ɕuʔ˨˩/. This is source-attested lexical evidence only. Decide broad phonemic vs surface transcription and contextual treatment; do not generalize a single dictionary form. |
| Independent segmentation domain | BLOCKED — licensed corpus/annotation convention not yet cleared | Choose a second corpus with verified license and immutable source snapshot; define split before evaluation; keep it untouched by training/tuning; report same-boundary-policy metrics and human error analysis. |
| Full official OBEC PDF inspection | BLOCKED — official URL returned HTTP 403 | No claim of full-PDF review. Acceptance requires lawful official access and page/section-scoped source notes; existing accessible page-scoped claims remain narrowly scoped. |
| Latest branch CI + web static validation | PARTIAL / pending | New review-sampling commits trigger fresh runs. Do not mark DONE_VERIFIED until both workflows finish successfully on the final exact HEAD. |
| Release readiness | BLOCKED | No release until engineering gates pass on final HEAD and empirical gates/declared scope are accepted. Research prototype remains the accurate classification. |

### New review-sampling implementation

- Updated `scripts/build_segmentation_manual_review.py` to compute both system predictions over the full pinned source set and select deterministic rows by heuristic strata plus uniform controls, instead of restricting the packet to top-ranked error examples.
- Updated `tests/test_segmentation_manual_review.py` to cover deterministic sampling, controls, provenance, lossless reconstruction, and fail-closed behavior.
- Updated CI to pass the generated TUD model to the sampler and verify that every selected row reconstructs exactly and all human adjudication fields remain blank.
- The packet remains `SOURCE_ANNOTATED`; the script does not promote source labels to expert gold. Exact-head workflow status must be checked after the latest commit.


## External segmentation-domain evaluation — 2026-10-26

| Task | Status | Evidence / acceptance |
|---|---|---|
| VISTEC dataset provenance and license | DONE_VERIFIED (metadata) | Dataset-specific upstream README at pinned commit 215a7dc3d384f20eb56af1cbc41fb32b7f8df57c declares CC-BY-SA 3.0; CSV Git blob SHA-1 edfcb85907a604c5e30643065ac4975862a0fe90; 49,997 samples described upstream; pinned CSV contains 50,000 data rows. |
| VISTEC annotation adapter | IMPLEMENTED; tests pending exact-head CI | Reads submissionText, splits pipe-delimited annotations, strips only documented <ne>/<msp> tags, preserves annotated text and verifies exact reconstruction. It does not use raw questionText. |
| VISTEC external evaluation workflow | IMPLEMENTED; workflow run pending | Pinned external checkout, source blob/license checks, current research-only TUD model, both segmenters, common scorer and report artifact. Acceptance requires workflow success and artifact inspection. |
| Independent segmentation-domain evidence | PARTIAL | VISTEC is a separate source/domain, but labels are still SOURCE_ANNOTATED rather than independently re-adjudicated. Report separately from Wisesight and do not tune on either test set. |
| Large-corpus scorer complexity | IMPLEMENTED; tests pending exact-head CI | Evaluator now indexes gold rows once, avoiding repeated full-list scans for every prediction; needed for ~50k-row external evaluation. |

No VISTEC metric is claimed before the external workflow finishes on this branch. Even a passing run establishes reproducible cross-domain source-annotation diagnostics, not independent expert accuracy.


## VISTEC annotation parser hardening — 2026-10-26

| Task | Status | Acceptance / evidence |
|---|---|---|
| Reject malformed empty annotation fields | IMPLEMENTED; exact-head CI pending | `parse_submission_text` now rejects any empty token after documented markup removal instead of silently filtering it. Regression cases cover repeated separators, markup-only empty tokens, leading separators and all-empty input. Code head: `1cbf97036ec931266f4a6ed5eb747a00e5b7ad29`. |
| Verify compatibility with pinned VISTEC source | BLOCKED_PENDING_WORKFLOW | The 50,000-row CSV (upstream README describes 49,997 samples) adapter must run against the immutable CSV snapshot. No metric is claimed until the external workflow succeeds and its artifact is inspected. |
| Exact-head CI and Web validation | PENDING / not yet surfaced | GitHub connector returned no workflow runs or combined statuses for the new head at the last check. This is not a pass; refresh workflow state before merge. |



## Exact-head run status refresh — 2026-10-26

The GitHub connector now reports the following runs for branch head `550f26fdbf6fd66a0d1c2cb1caa9bd6bd10de196`; each remains queued, with no conclusion yet:

| Check | Run | Current state | Acceptance |
|---|---|---|---|
| CI | [40346688497](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40346688497) | QUEUED | All repository test and generated-artifact gates pass on this exact head |
| Web static validation | [40346688520](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40346688520) | QUEUED | Static validation passes on this exact head |
| External VISTEC evaluation | [40346688621](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40346688621) | QUEUED | Pinned 50,000-row CSV (upstream README describes 49,997 samples) is accepted; report artifact inspected; no claim of independent gold |

The earlier “not yet surfaced” state is superseded by this timestamped refresh. Queueing is not a successful validation result.


## Follow-up after failed validation — 2026-10-26

| Task | Status | Evidence / acceptance |
|---|---|---|
| Stale corpus-license unit assertion | FIXED_PENDING_EXACT_HEAD_CI | CI run 40346688497 failed because the test expected old wording; updated to assert the registry's pinned-source declaration. |
| VISTEC row-count contract | FIXED_PENDING_EXTERNAL_RERUN | Run 40346688621 verified the pinned commit/blob but evaluator rejected 50,000 actual CSV data rows against stale expected count 49,997. Evaluator/workflow now assert 50,000; corpus registry explicitly records upstream README's 49,997 claim separately from CSV count. |
| Web static validation | DONE_VERIFIED_FOR_PRIOR_CODE_HEAD | Run 40346688520 passed; final code-bearing head must be checked if workflows trigger. |

No VISTEC metric is claimed until the corrected workflow completes and its report artifact is inspected. Source labels remain unadjudicated.


## Corrected exact-head verification — 2026-10-26

The stale unit-test assertion and the VISTEC 50,000-row count contract are fixed in code. Latest observed runs for the corrected workflow head: CI [40353097806](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40353097806), Web static validation [40353097480](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40353097480), VISTEC [40353097539](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40353097539). All were queued at the last poll. Acceptance remains pending successful exact-head CI, successful full 50,000-row evaluation, and report-artifact inspection.


## Latest verification and regression repair — 2026-10-26

| Task | Status | Evidence / acceptance |
|---|---|---|
| VISTEC external evaluation on corrected 50,000-row snapshot | DONE_VERIFIED (source-annotation diagnostic only) | Run [40354836797](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40354836797) succeeded on prior head; confirms immutable source checks and evaluator execution, not expert-adjudicated accuracy. Inspect artifact before reporting metrics. |
| Web static validation | DONE_VERIFIED for prior head only | Run [40354836884](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40354836884) passed; rerun after the latest test-only fix if workflow triggers. |
| VISTEC source registry license test | FIXED_PENDING_EXACT_HEAD_CI | CI [40354836807](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40354836807) exposed one stale assertion among 194 tests: expected `verify upstream terms` despite the pinned source README declaring CC-BY-SA-3.0. Updated the test to assert `attribution/share-alike required` at commit `0e60b2d277facee573839335b7e1681d5520a224`. Acceptance: exact-head CI passes all tests. |
| Overall engineering validation | PARTIAL | VISTEC and static validation passed on the preceding head; Python CI failed one outdated assertion and must be rerun after the repair. |
| Research / release readiness | BLOCKED / research prototype | Expert linguistic/target adjudication and lawful official OBEC PDF review remain outstanding. |


## VISTEC report result (source-annotated diagnostic only) — 2026-10-26

The successful external run [40354836797](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40354836797) evaluated 50,000 source-annotated rows (0 expert-adjudicated). The JSON printed in the workflow log reports:

| Segmenter | Boundary precision | Boundary recall | Boundary F1 | Exact sequences |
|---|---:|---:|---:|---:|
| Dictionary maximum matching | 0.76880 | 0.89788 | 0.82834 | 76/50,000 (0.152%) |
| Research-only TUD unigram Viterbi | 0.60640 | 0.99316 | 0.75302 | 16/50,000 (0.032%) |

Both had 100% output coverage, which is not accuracy. These scores measure agreement with source-provided annotations, not expert-adjudicated segmentation. The low exact-sequence rates mean neither system is production-ready. Artifact ZIP ID 12667445022 exists and its digest is recorded in the handoff; the archive itself still needs inspection. Exact-head checks after the latest test-only repair remain queued.


Artifact verification: downloaded and inspected VISTEC artifact ZIP 12667445022; it contains one JSON report (3,803 bytes), schema 1.0. Parsed report matches the metrics above and explicitly records 50,000 SOURCE_ANNOTATED rows and 0 adjudicated rows. Artifact integrity/contents: DONE_VERIFIED; linguistic gold quality remains BLOCKED pending human adjudication.

## Public beta site update — 2026-10-26

| Task | Status | Acceptance / evidence |
|---|---|---|
| Visible beta disclosure on service page | IMPLEMENTED; exact-head checks pending | Homepage now identifies the tool as a research beta and links to evidence/limitations. |
| Evidence disclosure on system page | IMPLEMENTED; exact-head checks pending | Shows VISTEC and Wisesight source-annotation diagnostics with explicit zero independently expert-reviewed rows; labels segmentation as not production-ready. |
| Responsive styling for beta notice | IMPLEMENTED; exact-head checks pending | Added mobile layout rules; automated UI contract assertions added. |
| Publish updated branch to public GitHub Pages | BLOCKED by release path | Pages workflow deploys on pushes to `main`; PR #71 is still draft. Do not deploy the draft branch over the current public site or merge its 304-commit diff blindly. Publish after the reviewed PR is merged, or create a separate preview host. |
| Empirical linguistic validation | BLOCKED | No independent Thai IPA/acoustic gold, independent Ukrainian target-form judgments, or expert-adjudicated segmentation rows. |

Latest successful pre-UI-update verification is on `17eac785a00ce1e8a95ac904db348ddf8c286040`: CI run 40372261539, Web static validation 40372261553, VISTEC evaluation 40372261718 all succeeded. The beta UI/test edits are newer and must pass their own exact-head checks before they are considered verified.

## Beta-site publication attempt — 2026-10-26

| Task | Status | Evidence / blocker |
|---|---|---|
| Beta notice, evidence panel, responsive CSS and UI regression | DONE_VERIFIED on code checkpoint `274371594cc8a0b65677bb126242d90acc17caf5` | Pages build [40377552366](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40377552366) passed Python regression tests, Python/browser parity and the new UI-contract test. Static validation [40377552367](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40377552367) and VISTEC diagnostic [40377560151](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40377560151) passed. |
| Publish branch build to GitHub Pages | BLOCKED | The same Pages run's `deploy` job failed immediately with no steps/logs; the build job succeeded. The latest successful public deployment is still main commit `18ab41db87192dc7be69683ef85e53cb04db5517` from run [40225366216](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40225366216). The known deployment path is main-only; the research PR remains draft. |
| Avoid unintended repeated deployment attempts | DONE_VERIFIED | Restored `.github/workflows/pages.yml` to trigger Pages deployment only on `main`; retained the UI-contract check in the Pages build. |
| Latest exact-head overall CI | PARTIAL / running | Latest branch head is `048b89d9234ac91e3d592c0bca7d816f4a5ae5b5`; CI runs 40378276967 and 40378286378 were still in progress at audit refresh. Do not mark the latest exact head fully green until the master-artifact job completes. |
| Public beta URL | BLOCKED for the new branch build | The existing site remains at [GitHub Pages](https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/) on the last successful main deployment. Do not claim the newly edited pages are live. To publish this exact engine, the owner must either merge the reviewed research PR to `main` after accepting the documented evidence gates, or authorize a separate preview host. No environment protections were changed and no PR was merged.

## Post-merge publication status — 2026-10-26 20:51 EET

This section supersedes the earlier pre-merge publication statements above.

| Task | Status | Evidence / acceptance |
|---|---|---|
| Merge reviewed research-beta code | DONE_VERIFIED | PR [#71](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/71) merged to `main` as `b4ae9e9f88a79d6f55cb1207363ac6877df080ba`. The UI remains explicitly labelled research beta and does not claim independent pronunciation accuracy. |
| Beta build and regression checks | DONE_VERIFIED for merged code checkpoint | Pages run [40378981918](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981918) build job passed Python regression tests, generated-fixture parity, browser parity, UI-contract checks, and Pages artifact upload. Web static validation [40378982254](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378982254) passed. CI run [40378981710](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981710) had its test job pass; master-artifact job remains queued. |
| Publish beta artifact to public GitHub Pages | BLOCKED by deployment queue | At 2026-10-26 20:51 EET, run 40378981918 remained `queued` despite build success; deploy job 121775188761 had no runner assigned and no steps. Pending deployment approval endpoint returned an empty list. The exact infrastructure cause is not observable from available data. Do not state that the new beta is live. Last successful deployment remains run [40225366216](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40225366216), main commit `18ab41db87192dc7be69683ef85e53cb04db5517`. |
| Pages workflow scope | DONE_VERIFIED | `.github/workflows/pages.yml` deploys only from `main`; no environment protections or external settings were changed. |
| Linguistic validation / release readiness | BLOCKED / research-only | Independent Thai IPA/acoustic gold, human segmentation adjudication, independent Ukrainian target-form reviews, contextual review of บรรจุ final /ʔ/, and lawful access to the full official OBEC PDF remain unresolved. VISTEC/Wisesight source-annotated metrics are diagnostics, not expert gold. |

## Final deployment status correction — 2026-10-26 22:08 EET

This update supersedes the prior row stating that the Pages deployment was blocked by a queue.

| Task | Status | Evidence / acceptance |
|---|---|---|
| GitHub Pages deployment of research beta | DONE_VERIFIED at workflow level | Run [40378981918](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981918) completed successfully: build job 121769734639 PASS and deploy job 121775188761 PASS. Public URL: https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/. Direct live HTML inspection was unavailable, so the workflow deployment is verified but served-markup details are not independently confirmed. |
| Main CI, including generated master artifact | DONE_VERIFIED | Run [40378981710](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981710): test job PASS; master-artifact job PASS. |
| Web static validation | DONE_VERIFIED | Run [40378982254](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378982254): PASS. |
| Release readiness / linguistic evidence | BLOCKED / research-only | Deployment success does not close evidence gates: independent Thai IPA/acoustic gold, human segmentation adjudication, two independent Ukrainian target-form reviews, contextual review of บรรจุ final /ʔ/, and lawful full official OBEC PDF access remain outstanding. The source-annotated segmentation scores are diagnostic only, not expert gold. |


## Whole-text web input segmentation — 2026-10-26

| Task | Status | Evidence / acceptance boundary |
|---|---|---|
| Web UI accepts whole text | DONE_VERIFIED on code head `3ccf84f564add02c189524c3b9ca794154d35c8b` | CI `test` and `master-artifact` both passed in [40402504410](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504410); static validation passed in [40402504394](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504394). Punctuation, whitespace, Latin text, and numbers remain separate tokens. Merged in commit `e49b5f2b54d42e577f732b4308080e11e410d557`; live Pages publication has not been independently confirmed. |
| Segment adjacent unspaced Thai text into known lexicon entries | PARTIAL implementation; regression tests DONE_VERIFIED | Browser engine applies greedy longest-known-entry matching inside continuous Thai-script runs and preserves unmatched spans as `unresolved`. Covered cases: `กาไฟมา`, mixed known/unknown `ทดสอบกาไฟ`, reviewed full-sentence entry `กินข้าวกับไข่และผลไม้` (seven IPA outputs), punctuation `กา,ไฟ!มา`, whitespace/punctuation `กาไฟ มา!`, and adjacent lexical IPA overrides `เงินเดิน`. Code checkpoint `3ccf84f564add02c189524c3b9ca794154d35c8b` passed CI `test` + `master-artifact` in [40402504410](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504410) and static validation in [40402504394](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504394). PR #73 merged as `e49b5f2b54d42e577f732b4308080e11e410d557`; the documentation reconciliation PR #74 then passed CI `test` + `master-artifact` in [40404124198](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40404124198) and was merged as `605d849c2148b7242fac56e581b6319bb17fd4f4`. **Limitation:** this proves code/test-contract behavior, not linguistic segmentation accuracy; greedy matching can misidentify substrings in unknown words. Live Pages publication remains unverified. |
| General Thai word segmentation | TODO / evidence-limited | Dictionary max-match is a baseline, not a linguistically complete or context-aware segmenter. Ambiguous boundaries, unknown vocabulary, repetition markers, compounds, and context-sensitive readings require evaluated coverage and adjudicated boundary data. Do not claim arbitrary Thai text is fully recognized. |
| IPA for every arbitrary text span | BLOCKED by linguistic evidence and coverage | IPA is shown only for deterministic, reviewed lexicon entries or typed source-attested overrides. Unknown spans are preserved and withheld from guessed IPA/Ukrainian output. |
| Example-button IPA contract | DONE_VERIFIED on code head `3ccf84f564add02c189524c3b9ca794154d35c8b` | Homepage examples use supported lexicon entries and the CI UI-contract test requires phonological IPA for every example. CI `test` + `master-artifact` passed in [40402504410](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504410); static validation passed in [40402504394](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504394). |


## Current authoritative status — 2026-10-26 23:41 EET

This section is the current decision record for the whole-text Thai input work. Older rows above contain historical checkpoints and may describe earlier branches, runs, or deployment queues; do not interpret those older statements as the current state when they conflict with this section.

- **Current `main` after merged code and documentation:** `605d849c2148b7242fac56e581b6319bb17fd4f4` (PR #73 code merge `e49b5f2b54d42e577f732b4308080e11e410d557`, followed by PR #74 documentation reconciliation).
- **Code-bearing checkpoint actually tested:** `3ccf84f564add02c189524c3b9ca794154d35c8b`. CI `test` + `master-artifact` passed in [40402504410](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504410); web static validation passed in [40402504394](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504394). PR #74 documentation-only follow-up also passed CI `test` + `master-artifact` in [40404124198](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40404124198).
- **Documentation cleanup:** PR #75 consolidates duplicated whole-text evidence and makes the segmentation limitation explicit. Its current head is `16febbadc20c013e8cc3c208ef3742ab04bd7a52`; it is open and must not be treated as merged until its required checks pass and merge status is confirmed.
- **Implementation status:** whole-text UI and tested known-word segmentation baseline are present. The segmenter uses greedy longest-match and can falsely split a substring inside an unknown word; tests prove deterministic behavior on listed examples, not general Thai segmentation accuracy.
- **Public deployment:** UNVERIFIED. The Pages workflow is configured for relevant pushes to `main`, but the available connector only reports pull-request-triggered workflow runs, while direct retrieval of served HTML was unavailable. Do not claim the merged changes are live without confirming a successful Pages deploy and inspecting served HTML.
- **Research/release classification:** PARTIAL RESEARCH PROTOTYPE, not release-ready. Independent Thai segmentation adjudication, Thai IPA/acoustic gold, Ukrainian target-form review, contextual treatment of `บรรจุ` final /ʔ/, and lawful full official OBEC PDF access remain evidence-gated blockers. Source-annotated Wisesight/VISTEC metrics remain diagnostics, not expert gold.


## Current authoritative status — 2026-10-27 (supersedes stale 2026-10-26 status)

- **Current main merge commit:** `581231596a0df6b3ab58964dacedeec7a8fd8908`, which merged documentation PR #75. PR #75 CI run [40406992550](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40406992550) completed successfully: both `test` and `master-artifact` jobs passed. The test job includes Python tests, generated-artifact drift checks, the 351,780-row/41-vowel master table assertion, IPA→Ukrainian tests, Python/browser parity, UI-contract checks, and segmentation/IPA diagnostics.
- **Code-bearing implementation checkpoint:** `3ccf84f564add02c189524c3b9ca794154d35c8b`; CI `test` + `master-artifact` passed in [40402504410](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504410), and web static validation passed in [40402504394](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504394). Documentation-only PR #75 did not change runtime code.
- **Whole-text input:** DONE_VERIFIED. **Greedy matching against known entries:** PARTIAL. **Arbitrary Thai segmentation:** TODO / evidence-limited. **IPA for every arbitrary text span:** BLOCKED by vocabulary coverage and independent linguistic evidence. The engine intentionally withholds IPA for unresolved spans rather than inventing a reading.
- **Known limitation:** greedy longest-match can select a known substring inside a larger unknown word and can choose the wrong boundary in ambiguous contexts. The tests prove the declared cases only; they do not establish general Thai segmentation accuracy.
- **Live GitHub Pages:** UNVERIFIED for the whole-text change. The prior Pages deployment at run [40378981918](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981918) predates this change. Current acceptance criterion: confirm a successful Pages build and deploy after the relevant `main` change and inspect the served homepage HTML for the updated examples and whole-text hint.
- **Still evidence-blocked:** independent Thai word-boundary adjudication; independent Thai IPA/acoustic gold; two independent Ukrainian target-form reviews; contextual review of `บรรจุ` final /ʔ/; lawful full official OBEC PDF; and per-resource license/attribution compliance.
- **Readiness:** PARTIAL RESEARCH PROTOTYPE, not release-ready for arbitrary Thai text. Source-annotated Wisesight/VISTEC results are diagnostics, not expert-adjudicated accuracy.


## Current authoritative status — 2026-10-27, browser dictionary fallback merged

- **Main HEAD:** `96c2af3c2a24d0ea95455b5d6af4c079e5609d29` (PR #77). PR [#77](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/77) adds a reproducible browser word index generated from the existing pinned 60,963-entry CC0 Thai dictionary. Generated output is 1,615,714 bytes across 51 first-character buckets and is intentionally ignored/not committed.
- **Verified behavior:** the browser now chooses the longer match from the CC0 dictionary or curated lexical entries, with curated entries winning ties. The regression `กาแฟ` prevents a known substring `กา` from receiving partial IPA inside a longer dictionary word. A regression on `เงินเดิน` caught a grapheme-boundary bug: a following preposed vowel was being consumed as a combining mark; the implementation now excludes preposed vowels from that mark set.
- **Evidence grade:** the dictionary provides boundary evidence only, not pronunciation gold. A dictionary-matched word without curated syllabification or typed source-attested IPA remains unresolved; no IPA or Ukrainian candidate is invented.
- **Tests:** web static validation passed for latest pre-merge head `7b2c9572feb542fb3ee81558b9758bb4fa5f2bef` in [run 40411659863](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40411659863). The full CI `test` job passed on runtime code head `3eb1155631da158b7e04436f608711680750e475` in [run 40411558761](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40411558761); the `master-artifact` job remained queued, and exact-head CI for `7b2c9572` was queued. These must not be described as exact-head full CI/master-artifact passes.
- **Post-merge workflow state:** Pages deployment [run 40412224812](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40412224812), main CI [run 40412224673](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40412224673), and web static validation [run 40412224629](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40412224629) were queued at the last check. The Pages workflow now retries a post-deploy HTTP check until the live homepage exposes the expected whole-text hint, examples, and beta notice. Do not claim live deployment until that job succeeds.
- **Remaining status:** whole-text input = DONE_VERIFIED; browser dictionary-backed max-match = PARTIAL; context-aware arbitrary Thai segmentation = TODO/evidence-limited; complete IPA for arbitrary text = BLOCKED by lexical coverage and independent linguistic evidence; live deployment = BLOCKED/queued pending the Pages workflow.
- **Research blockers remain:** independent Thai boundary adjudication, independent Thai IPA/acoustic gold, two Ukrainian target-form reviews, contextual review of `บรรจุ` final /ʔ/, lawful access to the full official OBEC PDF, and per-resource licensing/attribution review.
- **Readiness:** partial research prototype, not release-ready for arbitrary Thai text.


## Browser dictionary lookup optimization — 2026-10-27

- **PARTIAL / awaiting exact-head CI:** the browser's pinned CC0 Thai word dictionary is now indexed by the first two Unicode code points instead of the first code point alone. Candidate matching semantics remain longest match with curated lexical entries winning ties; dictionary-only matches still authorize boundaries only, never IPA or Ukrainian output.
- The generator validates each bucket key against each word and reports the largest bucket so CI logs provide a deterministic candidate-scan bound for the pinned snapshot.
- Existing UI contract tests continue to guard `กาแฟ` (no false partial IPA for `กา`), adjacent known entries, unresolved spans, lexical IPA overrides, punctuation, and whole-sentence input.
- Acceptance: exact-head CI `test` + `master-artifact`, web static validation, and Pages build/deploy must pass. This optimization is not evidence of linguistic accuracy; independent segmentation adjudication and IPA/UA review remain blocked by missing human evidence.

## Browser prefix-index performance change — 2026-10-27

- **TODO / exact-head verification pending:** branch `perf/browser-dictionary-prefix-index-20261027` changes the generated CC0 dictionary index from one-code-point to two-code-point prefixes. Lookup checks the longer-prefix bucket first and falls back to the one-code-point bucket for single-character dictionary entries, preserving longest-match behavior.
- **Tests added:** generated index must contain all 60,963 pinned unique entries, every word must be in the correct prefix bucket, and every bucket must be sorted longest-first with deterministic code-point ordering. Existing Python/browser parity and UI regressions cover user-visible segmentation behavior, including `กาแฟ` and unresolved unknown spans.
- **Acceptance:** exact branch-head CI `test` + `master-artifact`, web static validation, and Pages workflow where applicable. No measured speedup is claimed until a reproducible benchmark is run; this is an algorithmic candidate-scan reduction, not a linguistic accuracy improvement.
- **Unchanged blocker:** independent expert segmentation/IPA gold and independent Ukrainian target-form adjudication remain unavailable; arbitrary-text IPA coverage remains partial.

## Prefix-index change — final evidence reconciliation (2026-10-27)

- **DONE_VERIFIED — implementation and browser acceptance:** PR #79 merged as `c799dbed4247ac9743845acc0fd4131922cfbb74`. Code-bearing commit `e17a7f96fef9989f6375d36331f30ce0246e378a` passed CI run [40466046264](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466046264) and Web static validation [40466046237](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466046237). The CI run completed both `test` and `master-artifact`; the static run passed the generated dictionary integrity checks, 28 Python/browser parity fixtures, text regressions and UI contract.
- **DONE_VERIFIED — post-merge site build/deployment:** main run [40466830868](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466830868) passed Pages build, deployment and the live served-homepage contract check. Main Web static validation [40466830820](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466830820) also passed. Main CI run [40466830808](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466830808) passed its `test` job; its duplicate `master-artifact` packaging job was still running at the time of this update. The equivalent code-bearing commit had already passed that job.
- **Observed generated-index metrics:** 60,963 words; 1,085 two-code-point buckets; largest bucket 1,521 entries; generated JavaScript 1,629,301 bytes. Previous one-code-point index was 1,615,714 bytes, so the uncompressed artifact grew by 13,587 bytes (about 0.84%). This is an index-size/candidate-bucket observation, not a measured runtime speedup.
- **Invariant preserved:** dictionary membership is boundary evidence only. It does not license IPA or Ukrainian output. Curated lexical entries retain tie precedence; unresolved spans still abstain. No linguistic-accuracy claim was added.
- **Still PARTIAL/BLOCKED:** arbitrary Thai segmentation quality and complete IPA for arbitrary text require independent boundary adjudication, independent Thai IPA/acoustic gold, and independent Ukrainian target-form reviews. The product remains a partial research prototype, not release-ready for arbitrary Thai text.

## Browser segmentation latency diagnostic — 2026-10-27

- **PARTIAL / awaiting exact-head CI:** added `scripts/benchmark_web_segmentation.mjs` and a CI step that publishes `thai-browser-segmentation-latency-diagnostic` for 100-, 250- and 500-code-point Thai runs. Each case uses five warmups and 30 measured runs; the report records median, p95, min/max, runtime version and basic output counts.
- **Measurement contract:** this is a wall-clock diagnostic, not a fixed-threshold performance gate. CI-runner timing is environment-specific; compare only like-for-like runs. It measures neither segmentation accuracy nor IPA/Ukrainian correctness.
- **Acceptance:** exact-head CI must pass and the artifact must be inspectable before reporting measured timings. Do not claim a speedup without a comparable pre-index baseline on the same runner/runtime. Unknown text must continue to abstain from IPA/Ukrainian output.
- **Unchanged evidence blockers:** independent Thai word-boundary adjudication, independent Thai IPA/acoustic gold, independent Ukrainian target-form reviews, contextual review of `บรรจุ` final /ʔ/, lawful access to the complete official OBEC PDF, and per-resource license/attribution review.


## 2026-10-27 — Thai → Ukrainian context-sensitive methodology matrix

- Added [docs/ukrainian-transcription-methodology.md](ukrainian-transcription-methodology.md), a human-readable first-pass method table covering onset consonants, coda neutralization, vowel/rime mapping, tone separation, context-sensitive glide handling, special orthography, statuses and evidence gates.
- Added comparison references for the published Thai–Russian practical transcription and a Thai dictionary transcription resource. Russian mappings are explicitly comparison material, not copied as Ukrainian normative rules.
- README links to the method document. The table is a specification for review, not a runtime truth source and not a claim of accuracy.
- **PARTIAL:** documentation commit only; no engine rules changed and no new phonetic accuracy was measured. IPA/adaptation adjudication and held-out evaluation remain required. Any questionable or lexical-dependent reading must remain gated rather than be guessed.

- Follow-up completeness correction: methodology doc now explicitly inventories all 44 traditional consonants (including obsolete ฃ/ฅ), the conventional 32 vowel forms, four tone marks, relevant diacritics/special symbols, Thai digits and mixed-text handling; cites NECTEC, W3C Thai Layout Requirements and Thai Orthography Notes. This is inventory-level documentation, **not yet a verified character-by-character runtime coverage result**.
- Status remains **PARTIAL** until an executable inventory test confirms the implementation’s actual behavior for each category and phonetic exceptions have evidence-backed tests.


## 2026-10-27 — українсько-російські відмінності в тайській транскрипції

- Додано [матрицю українських особливостей](ukrainian-vs-russian-thai-transcription.md): /ɯ/, /h/, придих /kʰ pʰ tʰ/, /j/ перед голосними, /w/, /ɛ/~/e/, українські г/ґ, йотовані літери та межі застосування дж/дз.
- Основні дослідницькі джерела: офіційне видання «Українського правопису» 2026 року, стаття Уляни Головач (2022), порівняльна тайсько-російська таблиця та JIPA-опис тайської.
- **PARTIAL / EVIDENCE-LIMITED:** це джерельно орієнтована матриця кандидатів, а не затверджена транскрипційна норма. Поточне /h/ → «х» позначено як проєктну конвенцію; альтернативу «г» треба перевірити на україномовних тайських назвах. /ɯ/ → «и» — наближення, не точна IPA-тотожність. Runtime не змінювався.
- Acceptance: зібрати джерельно підтверджений набір українських тайських назв; провести незалежне IPA та українське редакторське оцінювання; лише після ад’юдикації затвердити machine-readable правила й тести. Не заявляти нормативність чи точність до виконання цих кроків.


## 2026-10-27 — українські відповідники /h/, придиху та тайських африкат

- Прийнято проєктну політику **тайський /h/ → українське «г»**; IPA /h/ лишається незмінним, тобто це адаптація, а не фонетична тотожність із українським /ɦ/. Усталені назви можуть бути окремими лексичними винятками.
- Придих /kʰ pʰ tʰ tɕʰ/ не отримує додаткової української літери: практичні відповідники **к/п/т/ч**; придих зберігається в типізованому IPA.
- Стандартні тайські /tɕ/ і /tɕʰ/ — глухі альвеоло-палатальні африкати, що розрізняються придихом. Обидві передаємо «ч» у практичному шарі; **«дж» /d͡ʒ/ не доречне**, бо є дзвінким відповідником і додає відсутню дзвінкість. «Ч» — наближення, не точна тотожність.
- **Статус PARTIAL:** документаційна політика зафіксована; runtime-код та регресійні fixtures ще не змінено. Приймання потребує окремих тестів IPA→UA, тестів для ห/ฮ, จ/ฉ/ช/ฌ та перевірки усталених українських назв. Немає заяви про приріст точності рушія.


### Follow-up update — runtime implementation added after the initial note

The Python and browser IPA adapters now map Thai /h/ to Ukrainian «г», and regression cases cover /h/, /kʰ pʰ tʰ/, /tɕ/ and /tɕʰ/. The generated consonant correspondence table was aligned. This supersedes the earlier statement that no runtime code had changed. Status remains PARTIAL until exact-head CI and generated-artifact checks pass; no linguistic-accuracy improvement is claimed.


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

| Component | State | Evidence / acceptance |
|---|---|---|
| Exact-form lexical IPA coverage for `ไกล` and `ใกล้` | PARTIAL — awaiting exact-head CI | Added pinned Wiktionary revisions 5688545 and 5721860, source-attributed records explicitly marked `ACTIVE_SOURCE_ATTESTED_NOT_GOLD`, and tests for segmental IPA, tone, diphthong, and IPA→Ukrainian adapter output. |
| Independent IPA accuracy benchmark | BLOCKED | `data/benchmark/gold.tsv` remains header-only. Acceptance: independently adjudicated, source-cited gold rows with clear transcription level/profile; reproducible predictions from the tested commit; held-out metrics. |
| Claims of overall engine improvement | BLOCKED / NOT MEASURED | These lexical overrides improve known-form coverage only; no global accuracy claim is justified without an adjudicated evaluation set. |


## Latest source-attested lexical coverage continuation — 2026-10-27

- Added pinned source-attested IPA overrides for `ไกล` and `ใกล้`; both remain `SOURCE_ATTESTED_NOT_GOLD` and pass through the typed IPA→Ukrainian adapter.
- The runtime diagnostic still has 6 source records. Because the new overrides are sourced from the same entries being compared, the measured diagnostic now marks 4 records circular and leaves 2 independently comparable records; segmental agreements = 1 and tone agreements = 2. These are source-comparison counts, not accuracy.
- Exact-head CI run [40591565959](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40591565959) exposed a stale workflow assertion that still expected 2 circular / 4 comparable records. The workflow expectation and current audit counts have been corrected; follow-up CI is pending.
- Independent adjudicated IPA gold remains absent; no overall G2P accuracy or before/after score is available. Release readiness remains blocked by independent IPA and Ukrainian target-form adjudication.


## 2026-10-28 — verified merge and live Pages deployment

- PR [#108](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/108) was squash-merged into `main` as `c6ba73b77766b0169d70619383b6efe27564d774`. This is the single active release path; no user branches were deleted.
- Exact-head CI [40592380586](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40592380586) passed both `test` and `master-artifact`. Web static validation [40592380619](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40592380619) passed, including browser JavaScript syntax, Python/browser parity fixtures, and IPA→Ukrainian/UI contracts.
- GitHub Pages deployment [40592864388](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40592864388) passed its build and deploy jobs. The post-deploy workflow verified the live whole-text interface, strict/soft/super-soft modes, and IPA adapter contract at https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/.
- The Python/browser lexical IPA adapters now both handle the source-pinned pair `ไกล` and `ใกล้` as phonemic /klaj/, preserve mid vs falling tone, return the same Ukrainian candidate `клай`, and withhold surface IPA because the dictionary source does not provide an independently verified surface-phonetic form. Both entries remain `SOURCE_ATTESTED_NOT_GOLD`.
- The source-attested diagnostic reports 6 records, 4 circular source overrides, 2 independently comparable records, 1 segmental agreement and 2 tone agreements. This is source-comparison evidence, not an accuracy score. `data/benchmark/gold.tsv` remains without independently adjudicated IPA gold; overall G2P/IPA/end-to-end accuracy is still NOT_MEASURED.
- Post-merge CI run [40592864584](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40592864584) had its `test` job pass; its separate `master-artifact` job was still running at audit time. The exact-head PR CI above passed both jobs, and the Pages build independently generated the master table and passed its Python/browser checks.
- PR #101 was closed as a duplicate of #104; PR #104 was closed/deferred because its separate research-only morphology overlay was based on an older main and had not been reconciled against the deployed head. Both source branches are preserved. Reopen/port that feature only after rebasing, exact-head CI and browser parity, and keeping morphology outside practical phonetic output.
- Readiness: engineering and deployment checks are verified; the project remains a research prototype, not release-ready for accuracy claims, pending independent IPA gold and Ukrainian target-form adjudication.


## 2026-10-28 — phonology completeness / ambiguity matrix

| Component | State | Acceptance evidence / remaining work |
|---|---|---|
| Productive tone rules and syllable class/quantity interactions | DONE_VERIFIED as implemented rule tables; accuracy over arbitrary text not claimed | `data/thai/tone_rules.csv`, parser/tone tests, source basis JIPA 1993; still depends on correct syllable segmentation. |
| Special-orthography ambiguity handling | PARTIAL, fail-closed | New `docs/phonology-ambiguity-coverage.md` documents `ทร`, `รร`, `ฤ/ฤๅ/ฦ/ฦๅ`, silent letters, false clusters, and `ห นำ`/`อ นำ`. Exact-head tests pending CI. |
| Sense-dependent `ทราย` and lexical `ทร` readings | PARTIAL, intentionally unresolved absent lexical/sense evidence | Royal Institute 2011 source distinguishes sand /s/ from deer-name cluster reading. Exact lexical readings such as `ทราบ` must not generalize to arbitrary `ทร` forms. |
| Connected-speech phonetics, lexical exception completeness, independent IPA gold | TODO / BLOCKED by evidence | Need sourced lexical/context rules and independent Thai phonetic adjudication; dictionary transcriptions remain SOURCE_ATTESTED_NOT_GOLD. |


| Productive tone rule table coverage | DONE_VERIFIED on tested code head `7a47e1f86862f33bb8eadfb34de75aeba5fd3809` (CI 40645028725) | Added `tests/test_tone_rule_coverage.py` with an explicit 15-condition truth table, uniqueness check, runtime lookup checks and restricted tone-mark negative cases. Acceptance met on tested code head `7a47e1f86862f33bb8eadfb34de75aeba5fd3809`: all 209 Python tests, downstream parity/generated-artifact checks and the 351,780-row master artifact passed. This proves rule-table completeness only, not end-to-end accuracy. |


| Context-specific ทราย disambiguation | DONE_VERIFIED as a source-pinned exact compound case on tested code head `7a47e1f86862f33bb8eadfb34de75aeba5fd3809` (CI 40645028725); broader sense coverage remains PARTIAL | Added pinned lexical segmentation `ทะเลทราย → ทะ|เล|ซาย` from English Wiktionary oldid 87239667, with matching Python/browser tests. The isolated homograph remains unresolved. Acceptance: exact-head CI verifies IPA `tʰa|leː|saːj`, tones high/mid/mid, UA `та|ле|сай`, and no forced IPA for isolated `ทราย`. |


| Special-orthography registry performance | DONE_VERIFIED on tested code head `7a47e1f86862f33bb8eadfb34de75aeba5fd3809` (CI 40645028725) | Cached `load_special_rules()` with `lru_cache(maxsize=1)` to avoid reopening the static CSV for every parser call during the 351,780-row master generator. Acceptance met: master-table generation and downstream Python/browser checks passed; master artifact verified 351,780 rows. |


| Exact lexical ทร regression test API | FIXED, rerun pending | First CI execution: 208/209 tests passed; the new `ทราบ` test incorrectly asserted phonemic IPA from the structural-only `parse_syllable()` function. Switched it to `api.analyze_syllable()` so the assertion covers the full phonology pipeline. Latest-head CI is the acceptance gate. |


| Main merge and deployment | DONE_VERIFIED | PR #110 squash-merged as `403e0bc02dee5e469511d91bba64d64010b2594d`; post-merge CI `40645764144` passed test/master-artifact jobs; Pages deploy `40645764146` passed and verified the live homepage contract. This does not close independent IPA/UA gold or full lexical coverage. |


## 2026-10-28 — aspiration marker policy (PR #115 continuation)

- **PARTIAL until exact-head CI:** Python and browser IPA→Ukrainian adapters encode IPA aspiration on /kʰ pʰ tʰ tɕʰ/ with an apostrophe immediately after the consonant output (к' п' т' ч'), rather than silently neutralizing aspiration or using «х».
- Regression cases cover aspirated/non-aspirated pairs, consonant clusters, standalone /h/ → «г», and /ʔ/ as a separate segment. RTGS remains a separate reference output and is not consulted by the adapter.
- Acceptance: exact-head CI must pass Python tests, browser adapter tests, parity, generated artifact checks and master-artifact; review any expected-output drift before calling this DONE_VERIFIED. Independent linguistic review of the project apostrophe convention remains evidence-limited.


### Latest checkpoint — 2026-10-28, adapter/data/UI reconciliation

- **PASS:** Web static validation on code head `8c855b9ec1d557d70135a9353c30df7c20b8f26f` (run [40688615996](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40688615996)).
- **PASS:** the RTGS browser unit tests, pinned PyThaiNLP 5.4.0 parity script, derived-data generation and structural-space generation completed successfully in the current full CI run before its longer master-table stage.
- **PARTIAL:** full exact-head CI and generated master-artifact are not yet confirmed. Earlier run `40688279406` failed three Python assertions because the new aspirated outputs had not yet been reflected in tests; those expected outputs were corrected. Do not mark the feature DONE_VERIFIED until a subsequent full CI passes.
- **Implementation coverage:** canonical Python/browser adapters, IPA-based candidate renderer, generated consonant correspondence CSV, regression tests, public IPA panel, system page, methodology and Ukrainian-vs-Russian comparison matrix all reflect the apostrophe convention.


### Latest checkpoint — 2026-10-28, RTGS merged and live

- **DONE_VERIFIED:** PR #115 merged as `fa75fe153a845aadbc7aad6b3e47a1ac5a6965f5`; exact-head CI including `master-artifact` passed in [40691939835](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40691939835), and web static validation passed in [40691940070](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40691940070).
- **DONE_VERIFIED:** Pages deployment [40692707861](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40692707861) passed at https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/. The deploy job fetched the deployed app and RTGS module and verified the RTGS panel and exported romanization function.
- **DONE_VERIFIED:** Pages build itself runs RTGS browser regression tests, pinned PyThaiNLP 5.4.0 parity and IPA-adapter tests before upload.
- **DONE_VERIFIED:** public content audit merged in PR #116 as `f4cc4d061c529fc5aec094af896dea5aaec9378f`. Exact-head CI [40693398363](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40693398363), static validation [40693398375](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40693398375), and Pages deployment [40694421367](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40694421367) passed; the served homepage, system page and RTGS JavaScript contract were verified.
- **BLOCKED:** independent expert-adjudicated Thai IPA/segmentation and Ukrainian target-form gold remains unavailable. No linguistic accuracy claim is inferred from implementation parity.


### Latest checkpoint — 2026-10-28, public guidance live

- **DONE_VERIFIED:** PR #116 merged to `main` as `f4cc4d061c529fc5aec094af896dea5aaec9378f`.
- **PASS:** exact-head CI [40693398363](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40693398363), web static validation [40693398375](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40693398375), and post-merge Pages deployment [40694421367](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40694421367).
- **DONE_VERIFIED:** deployed homepage advises one-word-first use, foregrounds segmentation uncertainty, labels fallback modes as approximate, explains IPA feature neutralization and describes RTGS as a parallel lossy Latin reference. The system page separates engineering tests from linguistic gold.
- **PARTIAL:** manual visual review across browsers/devices was not performed. Automated live-page checks validate served HTML/JavaScript contracts, not visual quality.
- **BLOCKED:** independent expert-adjudicated Thai IPA, segmentation and Ukrainian target-form gold remains unavailable. The project is still a research prototype, not release-ready.


### Final checkpoint — 2026-10-28, audit and handoff reconciled

- **PASS:** PR #117 exact-head CI [40695138890](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40695138890), including `test` and `master-artifact`.
- **DONE_VERIFIED:** PR #112 closed as superseded; its unique copy/UI changes and public audit findings are preserved in merged PRs #116/#117.
- **DONE_VERIFIED:** live RTGS and public guidance confirmed by Pages deployments [40692707861](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40692707861) and [40694421367](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40694421367).
- **PARTIAL:** manual browser visual QA was not performed.
- **BLOCKED:** independent expert-adjudicated Thai IPA, segmentation and Ukrainian target-form gold remain unavailable; the system is not release-ready.

### UX accessibility polish — 2026-10-28

- **DONE_VERIFIED — code and CI at `00fbd12780d6951fe9d820027d29f12ac1861974`:** CI [40718211681](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40718211681) and web static validation [40718211647](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40718211647) passed. The code is verified; **PARTIAL — publication** until merge and post-merge Pages verification.
- Primary UX refresh and corrected live Pages contract were already on main before this follow-up. No phonological rules changed.
- Real-browser responsive review/WCAG audit not performed; independent linguistic gold remains blocked by missing expert-adjudicated Thai IPA, segmentation, and Ukrainian targets.

### UX refresh publication verified — 2026-10-28

- **DONE_VERIFIED:** merged commit `275d615424ef425599d2cce550b0bbc100348719`; Pages deployment/live content contract [40719517666](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40719517666) and web static validation [40719517689](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40719517689) passed.
- **DONE_VERIFIED:** full CI, including `test` and `master-artifact`, passed at exact PR head `54f42190db100613adac9151053c62beea35c6a4` in [run 40719154739](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40719154739). The squash merge contains the same verified code and docs.
- **PARTIAL:** manual browser/device review and full WCAG 2.2 AA verification were not performed. **BLOCKED/evidence-limited:** independent expert-adjudicated Thai IPA, segmentation, and Ukrainian target-form gold remain absent; not release-ready linguistically.

## 2026-10-28 — UX status-language clarity

- **PARTIAL → pending verification:** token-level technical segmentation identifiers are now paired with user-facing Ukrainian status labels; technical identifiers remain inspectable in detailed mode.
- **DONE_VERIFIED criteria:** UI contract tests cover known, soft, and super-soft status labels; Pages deployment verifies the same labels in the served browser bundle; exact-head CI/static validation pass.
- **Preserved:** strict mode remains default; uncertainty is not hidden; IPA stays the intermediate source for Ukrainian adaptation; RTGS stays a separate reference; no pronunciation behavior changed.
- **Remaining evidence-limited work:** real-browser responsive screenshots/manual keyboard and screen-reader checks; WCAG 2.2 AA validation; independent linguistic gold corpus.

### Verification update — 2026-10-28

- **DONE_VERIFIED — code and automated acceptance at `82d7fd5d6469b3d2c2fcad98158bf98dcb452135`:** full CI passed [40723829479](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40723829479), including the UI contract and 351,780-row master-artifact gate; static validation passed [40723829245](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40723829245).
- **PARTIAL — publication:** PR #125 is open; the live Pages contract must pass after merge.
- **BLOCKED/evidence-limited:** manual real-browser/mobile/screen-reader review and independent linguistic gold corpus are not available in this no-Work session.


## UX/UI follow-up — final interaction polish (2026-10-28)

| Check | Acceptance criterion | Final state |
|---|---|---|
| Primary-result hierarchy (superseded by user requirement 2026-10-28) | All three outputs visible in order RTGS → IPA → Ukrainian | SUPERSEDED; see latest acceptance section below |
| Mode comprehension | Selecting strict/soft/super-soft updates a concise Ukrainian explanation of the uncertainty trade-off | DONE_VERIFIED — UI contract |
| Interaction targets | Copy and clear controls have at least 44px minimum height; disclosure summary is keyboard-focusable | DONE_VERIFIED — static CSS contract |
| Regression coverage | UI test covers RTGS disclosure and all three dynamic mode explanations | DONE_VERIFIED — full CI |
| Deployment contract | Pages workflow checks the new public JS markers after deployment | DONE_VERIFIED — Pages run 40729942455 |
| Visual/accessibility QA | Browser screenshots, real-device checks, contrast/focus/zoom/screen-reader tests | BLOCKED in this connector-only session; requires browser/device execution |


## 2026-10-28 — user-directed result order and visibility

The user's explicit requirement supersedes the prior UX decision to collapse RTGS. Keep the existing linguistic architecture and present the three separate outputs immediately on screen, in this visual order:

| Check | Acceptance criterion | State |
|---|---|---|
| Result visibility | RTGS, IPA and Ukrainian candidate render as three visible continuous panels; none is inside a disclosure | DONE_VERIFIED — exact-head CI + Pages content gate |
| Result order | RTGS first, IPA second, Ukrainian candidate third | DONE_VERIFIED — UI regression + published-content order check |
| Semantic clarity | RTGS is labelled a separate Latin romanization, not IPA and not the source of the Ukrainian result; page copy distinguishes display order from computation order | DONE_VERIFIED — UI contract + Pages gate |
| First-use friction | Remove redundant workbench intro while preserving beta caveat, input guidance, examples and mode uncertainty copy | DONE_VERIFIED — UI contract + static validation |
| Responsive hierarchy | Retain 44px interaction targets, visible focus, reduced-motion support and mobile one-column layout; distinguish the three output panels without relying on color alone | PARTIAL — static CSS/UI contracts pass; real-browser/device evidence still needed |
| Regression protection | UI test asserts all three panels exist in requested order and no RTGS disclosure remains | DONE_VERIFIED — exact-head full CI + master-artifact gate |
| Published-content gate | Pages workflow checks the new cache keys and exact visible result order markers in the deployed JavaScript | DONE_VERIFIED — Pages run 40744444939 |

- Branch: `ux/show-romanization-ipa-ukrainian-in-order-20261028`, based on main `8fa745a87d548f0145f6c367f85291ca85f9cb1f`.
- No phonological/romanization rules changed; this is a presentation and explanation change only.
- Manual browser screenshots, real-device checks and WCAG 2.2 AA remain evidence-limited until performed in an actual browser/device environment.


### Publication closeout — 2026-10-28

- **DONE_VERIFIED:** PR [#128](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/128) merged to `main` as `086e62f252f0b16f6c4035ccb80b4b2183ef5a17`.
- **DONE_VERIFIED:** exact PR-head full CI, including the 351,780-row master-artifact gate, passed in [run 40743456590](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40743456590); static validation passed in [run 40743456356](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40743456356).
- **DONE_VERIFIED — published:** post-merge GitHub Pages build, deployment and live-content contract passed in [run 40744444939](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40744444939). The live gate verifies RTGS → IPA → Ukrainian order and absence of a hidden RTGS disclosure.
- Public site: https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/
- **PARTIAL / evidence-limited:** no real-browser screenshots or physical-device sessions were captured; do not claim full manual visual QA or WCAG 2.2 AA. Independent expert-adjudicated Thai IPA, word-boundary and Ukrainian target-form gold remain unavailable.



## 2026-10-30 — service copy and methodology publication

| Acceptance criterion | State | Evidence |
|---|---|---|
| User-facing copy explains the task and outputs without exposing research jargon as primary instructions | DONE_VERIFIED | PR #129, merge 2bb0e264ed74e4d10c1a0c59ecf1d1990bcb9241; live homepage |
| Research methodology is clearly separated and labelled for researchers/developers | DONE_VERIFIED | PR #129; live system.html |
| UI copy contract matches revised mode prompt | DONE_VERIFIED | Exact-head CI run 41073081887 |
| Pages publication gate checks new copy markers | DONE_VERIFIED | PR #131; Pages run 41073985170 |
| Live homepage and methodology page contain revised text | DONE_VERIFIED | Live fetch after merge; Pages deployment gate |
| Runtime/linguistic behavior unchanged by copy-only work | DONE_VERIFIED | PR diffs limited to HTML, UI test assertion and Pages workflow |
| Exact-head full CI + master artifact | DONE_VERIFIED | 41073081887; 351,780 rows, 41 vowel records |
| Post-merge main CI | PARTIAL at entry time | Test job success; master-artifact still running in 41073985130; update after completion |
| Manual browser/device visual QA and WCAG 2.2 AA | BLOCKED | Requires actual browser/device and accessibility review |
| Independent expert-adjudicated Thai IPA, word boundaries and Ukrainian target forms | BLOCKED / evidence-limited | Gold reference corpus and expert adjudication not yet available |

- Editorial precedent: Korean reviewed copy revision 2a16bae3bb6d4297225d358180adcefa0f301de8; treated as a style/structure reference, not as proof that an executable corrector was run.
- PR #130 superseded and closed; clean PR #131 merged as feef61cba8d1a5ee6d1a79b72bfaa952f53b5e66. PR #111 remains separate and untouched.
- Status: published copy update DONE_VERIFIED; overall project remains a research prototype, not release-ready for linguistic-accuracy claims.


### Post-merge CI result update — 2026-10-30

- The previously pending post-merge main CI run 41073985130 is now DONE_VERIFIED: both test and master-artifact jobs succeeded. Master artifact asserted exactly 351,780 rows and 41 vowel records.
- The handoff/matrix/audit closeout was merged in PR #132 as 78e24924ece18c92a9d872afbfe40e1f842b912b.


### Repository closeout reference — 2026-10-30

- Final main commit for this completed documentation closeout: fafb38143de4fecbebc143eb4b98ca71aed94cf6.
- Post-merge main CI run 41073985130 completed successfully: test and master-artifact jobs passed; master artifact contains 351,780 rows and 41 vowel records.
- Pages deployment and live-content verification passed in run 41073985170. Both public pages were fetched live and show the intended audience split.



## 2026-10-30 — second plain-language copy pass

| Acceptance criterion | State | Evidence |
|---|---|---|
| Homepage begins with the user's task and explains the Ukrainian-letter output without research jargon | DONE_VERIFIED | PR #135, merge `867974bb16050bd815050d1b4a976283de47cdbf`; live homepage |
| Main result headings and uncertainty/mode explanations use ordinary Ukrainian | DONE_VERIFIED | PR #135; UI contract passed in CI 41079488713 |
| Research page explains the process plainly before technical detail | DONE_VERIFIED | PR #135; live `system.html` |
| Technical details remain available separately for researchers | DONE_VERIFIED | Collapsed “Технічні подробиці для дослідників” section |
| IPA-first adapter boundary and all language-engine behavior preserved | DONE_VERIFIED | Code diff restricted to copy, UI assertions and Pages smoke tests; IPA adapter/parity tests passed |
| PR-head full CI and master artifact | DONE_VERIFIED | 41079488713; 351,780 rows, 41 vowel records |
| Pages build, deployment and live copy contract | DONE_VERIFIED | 41080245447; live homepage and system page fetched after deployment |
| Post-merge main CI | DONE_VERIFIED | 41080245372; both test and master-artifact jobs passed |
| Plain-language wording validated with non-specialist users | PARTIAL | No moderated user test performed |
| Independent expert-adjudicated Thai IPA, word boundaries and Ukrainian target forms | BLOCKED / evidence-limited | Gold reference corpus and expert adjudication not yet available |
| Manual browser/device QA and WCAG 2.2 AA | BLOCKED | Requires actual browser/device and accessibility review |

- PR #135 supersedes the insufficient first copy pass for the user-facing text; it does not alter the engine or research claims.
- Overall project remains a research prototype, not release-ready for linguistic-accuracy claims. PR #111 was closed as superseded; its source-attested lexical exception was forward-ported to main through PR #144, while the historical branch remains preserved.


## 2026-10-31 — JSON API internal-error disclosure hardening

| Acceptance criterion | State | Evidence |
|---|---|---|
| Unexpected analysis exceptions do not expose internal exception text to API clients | DONE_VERIFIED | Regression test: test_unexpected_api_error_is_logged_but_not_exposed; client receives a stable generic 500 response |
| Unexpected exceptions remain diagnosable server-side | DONE_VERIFIED | Regression test asserts the exception is logged through thai_ukrainian.server |
| Existing malformed-request behavior remains 400 | DONE_VERIFIED | Existing non-object JSON regression remains green |
| Full Python/browser/diagnostic CI and package smoke | DONE_VERIFIED on code head | CI [41139203848](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41139203848): 215 Python tests, wheel-install smoke, browser parity/UI contracts and research diagnostics passed |
| Master artifact | DONE_VERIFIED on code head | Same CI run generated and asserted 351,780 structural rows and 41 vowel records |

- Test-first evidence: test-only commit e2e0e6783d277092ecf05ac87a2b712d9c03f260 failed only the new regression because no error log was emitted; implementation commit 60ac49dd1d3f6c387c306616e1c5a435dea4662a passed the full CI workflow.
- Runtime change is limited to server-side logging and redaction of unexpected 500 responses. Expected malformed-request exceptions retain their existing 400 response contract.
- This is API error-hygiene hardening, not a claim that the local standard-library server is production-ready for public internet exposure.

## 2026-10-31 — HTTP Content-Length framing validation

| Acceptance criterion | State | Evidence |
|---|---|---|
| Reject negative and malformed Content-Length values before reading the request body | DONE_VERIFIED on PR head | `APIHandler.do_POST` now requires ASCII decimal digits before conversion; malformed values use the existing 400 `invalid_request` response path. |
| Prevent negative Content-Length from turning `read(n)` into unbounded `read(-1)` | DONE_VERIFIED on PR head | Raw-socket regression sends a valid JSON body with `Content-Length: -1`; exact PR-head CI passes the assertion. |
| Preserve the 1 MB request-size limit and existing valid-request behavior | DONE_VERIFIED on PR head | Existing API contract tests pass; implementation changes only the length-field validation. |
| Python, browser/parity, research diagnostics and isolated wheel smoke | DONE_VERIFIED on PR head | CI [41141511448](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41141511448): 216 Python tests, browser IPA/parity/UI, diagnostics and wheel smoke passed. |
| Master artifact | DONE_VERIFIED on exact PR head | CI [41141850559](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41141850559) passed the 351,780-row / 41-vowel assertion and uploaded the artifact. The post-merge main master-artifact job [41142211674](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41142211674) also passed. |

- Test-first commit `3814af5e8b083117d93634531a5c62e1db5757d8`; red CI [41141368949](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41141368949) failed only the new test: the old server returned HTTP 200 and analyzed the body despite `Content-Length: -1`.
- Implementation commit `47c3f335fb5aa902784f4964a842dd00e5ea01c7`; exact PR-head CI passed 216 Python tests, including the regression.
- Scope is limited to HTTP request framing. No parser, Thai phonology, segmentation, IPA, RTGS, Ukrainian adaptation or browser behavior changed.
- PR [#153](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/153) was squash-merged as `8a539193798e55c3010e3a6a72a0e2578ea413c9`. Post-merge main CI [41142211674](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41142211674) passed test and wheel-install-smoke; the separate master-artifact job was still running. Pages build/deploy and published-content verification [41142211675](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41142211675) passed.


## 2026-10-31 — CI master-table artifact reuse

| Acceptance criterion | State | Evidence |
|---|---|---|
| Generate the exhaustive master table once per workflow run | DONE_VERIFIED | The `test` job generates the three files once for `test_master_table.py`, then uploads them as `thai-ukrainian-master-table`. |
| Preserve an independent master-artifact validation job | DONE_VERIFIED | `master-artifact` downloads the artifact with `actions/download-artifact@v8.0.2`, verifies the artifact digest, and asserts 351,780 rows plus 41 vowel/rime records. |
| Preserve the existing artifact contract and Python/browser/research checks | DONE_VERIFIED | Exact PR CI [41143491570](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41143491570) passed all three jobs, including 216 Python tests, Ruff, browser parity/UI, research diagnostics, wheel smoke and downloaded-artifact validation. |
| Verify the optimized workflow on main | DONE_VERIFIED | Post-merge main CI [41143907732](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41143907732) passed test, wheel-install-smoke and master-artifact. |

- PR [#155](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/155) merged as `3325e98b98bde6926f36c74ad76dc94fe35480b0`.
- Before optimization, the master-artifact job regenerated the table in approximately 126.9 seconds. After optimization, artifact download plus validation took approximately 1.1 seconds; the independent assertion and artifact name are unchanged.
- No application code, generated data content, Thai parsing, phonology, IPA, RTGS, Ukrainian adaptation or browser behavior changed.


## 2026-10-31 — Branch inventory and retention boundary

- **PARTIAL — 169 branch refs inventoried.** Prefix counts: `docs/` 49, `feat/` 26, `fix/` 26, `research/` 24, `audit/` 8, `ux/` 7, unprefixed 7, `chore/` 5, `test/` 4, `ci/` 2, `copy/` 2, `design/` 2, `perf/` 2, and one each under `polish/`, `finalize/`, `site/`, `ui/`, `web/`.
- All implementation PRs reconciled in this run are merged; the remaining refs are historical/work branches rather than unmerged open PRs.
- No branch deletion was performed. Historical refs may contain unique research/evidence work; no owner-approved retention policy exists, and the connected GitHub action set exposes no branch-deletion operation.
- Acceptance: review unique commits and obtain an explicit archive/delete policy before pruning. Keep `BRANCH-HYGIENE-001` PARTIAL until that decision and cleanup are complete.


## CCOST annotation manual review — 2026-11-01

| Task / acceptance criterion | State | Evidence / next acceptance |
|---|---|---|
| Retrieve and inspect the official CCOST annotation manual | DONE_VERIFIED — document inspection | Official Zenodo file `CCOST_manual.pdf` (19 pages; MD5 `caecb20d26e8458b20c7c269ca22b59e`) inspected. It describes OCTRA ASR transcript correction, Thai-script normalization, Praat boundary/transcript correction and BAS `CHUNKPREP → G2P → MAUS → PHO2SYL`; it names `OCTRA_1` and illustrates MAUS output `sampa`. |
| Establish the released TextGrid phone/toneme annotation contract | BLOCKED / evidence-limited | The manual does not define final released TextGrid tiers, full phone/toneme inventory, tone-label scheme, uncertainty policy or independent double annotation. Acceptance requires inspection of released TextGrid schema and detailed LREC paper methods, then mapping each label to a declared target layer. |
| Use CCOST as independent phonetic gold | BLOCKED / evidence-limited | Manual inspection does not establish dual blinded annotation. Require two qualified Thai phoneticians' independent labels under the project protocol for independent accuracy claims; keep CCOST external under CC BY-NC-SA 4.0. |


## Current continuation checkpoint — 2026-11-01 (PR #169)

| Task / acceptance criterion | State | Evidence / next acceptance |
|---|---|---|
| Verify exact current PR #169 head | DONE_VERIFIED | Head `0dee9e36cd5391b599c8b785a8b2c1b81ea325a7`; CI [41300790280](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41300790280) completed successfully with `test`, `wheel-install-smoke`, and `master-artifact`. |
| Verify exact current PR #170 head | DONE_VERIFIED | Head `1cdc3d7971498ce3312ff9a79b23ee84b8d917aa`; CI [41243709726](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41243709726) and Web Static [41243709639](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41243709639) succeeded. |
| Review submissions and inline threads on #169/#170 | DONE_VERIFIED — none present at inspection | GitHub review and review-thread endpoints returned empty collections for both PRs. |
| Reconcile CCOST manual-inspection status | DONE_VERIFIED | Manual retrieval/inspection is complete; released TextGrid tier schema and detailed LREC-method reconciliation remain BLOCKED / evidence-limited. |
| Independent Thai IPA/segmentation adjudication | BLOCKED / evidence-limited | Requires qualified independent Thai reviewers, frozen layer-specific protocol, dual blind labels and disagreement log; issue #114. |
| Ukrainian target-form adjudication | BLOCKED / evidence-limited | Requires two independent Ukrainian-native reviewers, predeclared criteria and adjudication log; issue #114. |
| Manual browser/device and WCAG 2.2 AA review | BLOCKED | Requires human keyboard, screen-reader, viewport and device review with recorded findings; issue #114. |
| Main branch protection | TODO — owner configuration | `protected=false`; acceptance requires owner decision on required checks/reviews and ruleset configuration. No setting changed. |

**Current main:** `8759fc5f12c1d27bd13f4d6c32a364d5cc7ac1c8` (unchanged). **PR #169 current head before this matrix refresh:** `0dee9e36cd5391b599c8b785a8b2c1b81ea325a7`. **Readiness:** engineering-verified research prototype; not release-ready for general linguistic-accuracy claims.


## Final repository-cleanup verification — 2026-11-01 (PRs #178–#179)

| Task / acceptance criterion | State | Evidence / next acceptance |
|---|---|---|
| Reconcile the audit, matrix and handoff with merged cleanup work | DONE_VERIFIED | PR #178 merged as `a5856b4539148f5347da91a719a07aead614decd`; exact-head CI [41326222309](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41326222309) passed `test`, `wheel-install-smoke` and `master-artifact`. The previously stale `final-audit.md` now contains the cleanup checkpoint. |
| Remove the hidden `word.py → api.py` reverse dependency | DONE_VERIFIED | PR #179 merged as `1431c565ff5c160da4944942d687bc30b2f8d0b2`; exact-head CI [41326533814](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41326533814) passed all three jobs. `word.analyze_word` now receives the syllable analyzer as an explicit callable; the public API supplies it. A focused regression test covers the dependency boundary and explicit segmentation. |
| Verify final merged main and published site | DONE_VERIFIED | Main CI [41326865977](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41326865977) passed `test`, `wheel-install-smoke` and `master-artifact`; Pages [41326865964](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41326865964) passed `build` and `deploy`. Main: `1431c565ff5c160da4944942d687bc30b2f8d0b2`. |
| Complete the repository-wide import/call/reference graph and prove suspected dead code | PARTIAL | One concrete reverse dependency was removed. A complete static graph plus manual review of dynamic imports, entry points and runtime consumers remains required; connector-only access did not provide a clean local checkout or a reliable repository-wide analyzer run. |
| Review broad test/fixture redundancy without reducing acceptance coverage | PARTIAL | Two immediately duplicated UI assertions were previously removed in #170. The wider suite has not been exhaustively deduplicated by semantic contract; no tests were removed on naming similarity alone. |
| Reorganize large historical documents | DEFERRED | Preserve the chronological handoff and audit history. Do not split/archive until all internal and external references are mapped and the archive plan is verified. |
| Review/prune historical branches | PARTIAL — owner policy required | 12 refs exist (11 non-main); merged feature branches remain. No branch was deleted. Commit provenance and owner-approved retention policy are required before pruning. |
| Configure main branch protection | TODO — owner configuration | Main still reports `protected=false`; required checks/review policy and ruleset are owner decisions. |
| Independent linguistic adjudication and manual accessibility review | BLOCKED / evidence-limited | Thai IPA/segmentation, Ukrainian target forms, CCOST released TextGrid schema/method, and manual browser/device/WCAG 2.2 AA review remain external acceptance gates. |

**Final verified main:** `1431c565ff5c160da4944942d687bc30b2f8d0b2`. **Post-merge CI:** [41326865977](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41326865977), all three jobs successful. **Pages:** [41326865964](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41326865964), build and deploy successful. Local pytest/npm were not run in this connector-only environment.


## Independent adjudication infrastructure — 2026-11-01 (research continuation)

| Task / acceptance criterion | State before exact-head CI | Evidence / remaining acceptance |
|---|---|---|
| Prepare candidate-blind Thai phonetic review set | DONE_VERIFIED — full CI passed | `data/benchmark/ipa-adjudication-blind.tsv`: 42 frozen inputs, no source IPA, engine output, stratum or probe labels; exact ID/input coverage checked by validator. |
| Validate independent Thai reviews and syllable metadata | DONE_VERIFIED — full CI passed | Validator checks qualification/date, lexical reading, lossless word/syllable boundaries, per-syllable tone/length/glottal alignment, explicit abstention and audio intervals; pair gate requires distinct reviewers and identical source text. |
| Prepare Ukrainian-native preference review | DONE_VERIFIED — full CI passed | Seven candidate-blind rows in `data/benchmark/ukrainian-target-preference-blind.tsv`; IPA explicitly `SOURCE_ATTESTED_NOT_GOLD`; validator binds to exact source records and supports individual/pair review under criteria v0.1. |
| Require double-reviewed IPA gold | DONE_VERIFIED — full CI passed | Scorer requires two distinct reviewers, both raw IPA labels, adjudicator/outcome/record, source/license and transcription layer; consensus must equal both labels; mixed phonemic/surface runs are rejected and metrics stratified by profile. |
| Require double-reviewed word/syllable segmentation gold | DONE_VERIFIED — full CI passed | Empty `data/benchmark/segmentation-adjudication-gold.tsv`; scorer requires two independent tokenizations, distinct reviewers, adjudication record and one WORD or SYLLABLE layer per run. Existing 993 Wisesight records remain SOURCE_ANNOTATED. |
| Independent Thai expert submissions | BLOCKED / external reviewer required | Two qualified Thai phoneticians must complete separate blind packets, freeze raw labels and adjudicate disagreements. Acceptance: auditable qualification references, raw labels, abstentions, record IDs and adjudication notes. |
| Independent Ukrainian-native submissions | BLOCKED / external reviewer required | Two Ukrainian-native reviewers must complete separate candidate-blind sheets. Acceptance: preferred forms, rationale, criteria version, boundary/tone policy, uncertainty and disagreement reconciliation. Judgments remain conditional on supplied source IPA. |
| CCOST acoustic corpus import | BLOCKED / access and schema evidence | CC BY-NC-SA 4.0; 6.2 GB archive not bundled. Inspect released TextGrid tiers/labels and map to phonemic/surface/acoustic targets before selecting rows. |

Verified code checkpoint: `a4de40b6479b217b24aed98a26bdade23e6e1dab`; branch base main `cc398254c178171f74397aed556766e87356ab84`; 45 commits ahead at the code checkpoint. Full push CI [41337529189](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41337529189) passed all three jobs. Web Static [41337815975](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41337815975) passed on documentation closeout head `ce8d4b0450d67e465f76f140dde3b27ca45e313f`. PR #182 is open; PR #181 was closed as superseded after its code/test/CI fix was ported. No local test run is claimed in the connector-only environment. Vercel was not used.


### Ported three-mode fallback regression — DONE_VERIFIED

The fix and test from draft PR #181 are included in this branch. A structurally provisional orthographic fallback now clears computed tone, tone contour and surface IPA instead of presenting them as confirmed. The segmental IPA candidate remains provisional and feeds the existing IPA-to-Ukrainian adapter. Ten adversarial cases exercise all three profiles (30 profile/input combinations), including six strict-abstention controls. CI 41337529189 and Web Static 41337815975 passed.


## Evidence provenance hardening — 2026-11-01

| Task / acceptance criterion | Status | Evidence / remaining acceptance |
|---|---|---|
| Register external source URL, exact license, scope and allowed benchmark use | DONE_VERIFIED after CI | `data/benchmark/source-registry.tsv`; `scripts/validate_evidence_registry.py`; exact source ID, URL, license and allowed-use match enforced by IPA/segmentation/UA review validators. |
| Require verified language-specific reviewer qualification | DONE_VERIFIED after CI | `data/benchmark/reviewer-qualifications.tsv`; reviewer role, language, exact qualification reference, verification state, verifier and date are checked by Thai/UA review and gold-scoring paths. |
| Reject non-independent adjudicator identity | DONE_VERIFIED after CI | IPA and segmentation gold rows require adjudicator distinct from both reviewers and a registered adjudicator role/reference. |
| Keep CCOST blocked until TextGrid tier/label mapping is evidenced | DONE_VERIFIED | Source registry marks CCOST `BLOCKED`; it cannot be used as IPA gold until schema and transcription-layer reconciliation is completed. |
| Obtain and verify two Thai phoneticians, Thai segmentation reviewers and Ukrainian-native reviewers | BLOCKED / external human dependency | Reviewer registry intentionally contains no real people. Acceptance: independently verified qualifications and separate blind submissions, then disagreement adjudication. |
| Establish independent IPA gold and measure phonetic accuracy | BLOCKED / source and reviewer dependency | No currently approved source for IPA gold; CCOST remains blocked pending tier schema and licensed access. Accuracy remains NOT MEASURED. |

The source registry does not itself create gold data. Wisesight and VISTEC remain source-annotated segmentation diagnostics; Wiktionary and Thai G2P v4 remain reference-only for IPA. No reviewer identity or qualification was fabricated.


## Annotation-layer and denominator hardening — 2026-11-01

| Task | State | Evidence / boundary |
|---|---|---|
| Separate narrow acoustic IPA from broad phonemic IPA | DONE_VERIFIED after exact-head CI | Added `narrow_ipa`; narrow review requires square-bracketed label, syllable alignment and audio/time provenance. Broad phonemic IPA remains separate; narrow labels are not scored by the broad IPA scorer. |
| Validate both frozen Thai blind packets in CI | DONE_VERIFIED after exact-head CI | CI validates the 42-item base packet and the separate six-item user-regression supplement against their exact frozen source prompts. |
| Correct independently-comparable denominator invariant | DONE_VERIFIED after exact-head CI | The summary excludes both circular overrides and incomplete/withheld engine outputs; a focused regression test covers both exclusion conditions. |
| Independent Thai expert and Ukrainian-native submissions | BLOCKED / external human dependency | Reviewer registry remains empty. No identity, consent, qualification, or linguistic annotation is fabricated. |


| Task | State | Evidence / boundary |
|---|---|---|
| Bind narrow acoustic labels to a verified, licensed audio source | DONE_VERIFIED after exact-head CI | Added `audio_source_id`; validator checks source registry status, exact URL/license and `ACOUSTIC_PHONETICS_RESEARCH` permission. Blocked CCOST is rejected. |
| Report descriptive inter-reviewer agreement | DONE_VERIFIED after exact-head CI | Thai and Ukrainian pair validators return NFC-normalized exact agreement by field, missing-label counts and joint/one-sided abstentions. No chance-corrected reliability or gold status is implied. |


## Corpus-source decision — 2026-11-01

| Task | State | Evidence / boundary |
|---|---|---|
| Register a commercial-compatible Thai audio source for expert re-annotation | DONE_VERIFIED at source/license level | `CORP-LOTUSDIS` registered CC BY-SA 4.0 for acoustic research and broad IPA annotation input. It supplies audio/transcripts/TextGrid, not IPA gold. |
| Select and pin individual LOTUSDIS audio assets | TODO / asset-level evidence | Requires exact dataset revision, file hash, asset ID, speaker pseudonym, mic/channel, non-overlap/near-field review and time interval. No assets downloaded or bundled. |
| Use CCOST as controlled tonal/phonetic source | BLOCKED / evidence-limited | CC BY-NC-SA 4.0, A-D list mismatch and unreconciled TextGrid tier/label mapping remain. |
| Use Common Voice Thai as a shared review packet | DEFERRED | CC0 dataset card separately prohibits re-hosting/re-sharing; no phone/toneme gold. |


| Task | State | Evidence / boundary |
|---|---|---|
| Enforce file-level audio provenance, not just a non-empty asset string | DONE_VERIFIED after exact-head CI | Added `audio-assets.tsv` manifest; review validator requires exact source match, VERIFIED asset, SHA-256, speaker/mic metadata, non-overlap and interval within duration. Manifest is header-only until actual samples are pinned. |


| Task | State | Evidence / boundary |
|---|---|---|
| Require immutable dataset revisions and absolute asset URIs | DONE_VERIFIED after exact-head CI | Audio asset manifest rejects moving aliases such as `main`/`latest` and requires an absolute HTTP(S) asset URI; file SHA-256 and duration are also mandatory. |


| Task | State | Evidence / boundary |
|---|---|---|
| Repair malformed corpus-source CSV row and enforce schema | DONE_VERIFIED after exact-head CI | Quoted the TUD row's comma-containing fields; added test requiring exact seven-column header, no missing/extra columns and unique source IDs. |

| Verify exact all-mode/adjudication branch head | DONE_VERIFIED | Head `6412f34accdd913d8d4ad0525a5b3bf89d50f56a`; CI [41352166930](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41352166930) passed 314 Python tests / 1169 subtests, Ruff, wheel install and master artifact; Web Static [41352166906](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41352166906) and VISTEC [41352166908](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41352166908) passed. |

| Withhold unsupported special-vowel word segmentation for `ฤๅษี` | DONE_VERIFIED | Removed the unsourced `ฤๅษี → รือ|สี` entry from the Python text lexicon and both `ฤๅษี → รือ|สี` / `ฤษี → รึ|สี` browser lexicon entries. Python text-pipeline and browser parity/mode regressions require strict-mode abstention; no IPA or Ukrainian form is emitted as confirmed. |

| Verify removal of unsourced special-vowel word split | DONE_VERIFIED | Exact code/test head `036fb2837c6e1df247e055df115d52c4b3c48b16`; Python text-pipeline and browser parity/mode tests pass in CI [41353088633](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41353088633). Strict mode withholds `ฤๅษี`; the unreferenced `ฤๅษี → รือ|สี` and browser-only `ฤษี → รึ|สี` mappings are removed. |


## Abstention IPA-layer guard follow-up — 2026-11-02

| Task / acceptance criterion | State | Evidence / remaining acceptance |
|---|---|---|
| Reject narrow acoustic IPA on an explicitly abstained Thai review row | PARTIAL — implementation and regression test committed; full exact-head CI pending | Test-first commit `2852b47a3c07eabc2512e686d56673dbe9e0ad50` adds `test_abstention_cannot_include_narrow_ipa_without_audio_evidence`. Implementation commit `e22c686128d0f65dbd078713d4d4428d24a09f62` adds `narrow_ipa` to the existing abstention guard. Exact-head CI [41356275693](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41356275693) was still running at `generate_master_table.py` when recorded; Web Static [41356275500](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41356275500) passed; VISTEC [41356275512](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41356275512) was still running. |
| Verify a red test run before implementation | BLOCKED — CI execution did not reach the Python suite | The test-only push run [41356118838](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41356118838) was cancelled during the push/PR workflow transition; its PR run [41356122208](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41356122208) was cancelled when the implementation commit advanced the PR head, before the complete Python suite started. Do not claim a CI-observed RED result. |
| Run local focused or full Python tests | BLOCKED — no local checkout/network in this session | GitHub connector access is available, but `git clone` could not resolve `github.com`; no local test result is claimed. |

The fix is deliberately limited to the existing abstention guard; no schema, runtime pronunciation, IPA adapter or linguistic data changed. Acceptance requires the full exact-head CI to complete successfully and the new regression test to be included in its Python suite.

## 2026-11-02 — seven acceptance gates and repository continuation

| Direction | State | Evidence / exact closure criterion |
|---|---|---|
| Thai IPA and segmentation | BLOCKED | Blind 42-item challenge and six-item regression supplement are prepared and validators are present, but reviewer qualification registry is header-only and there are zero adjudicated rows. Close only after two qualified independent Thai reviewers submit frozen annotations, an adjudicator records every disagreement/resolution, and segmentation labels are independently reviewed. Acoustic/narrow claims additionally require authorized, asset-pinned recordings and exact intervals. |
| Ukrainian practical transcription | BLOCKED | Seven candidate-blind, source-attested preference prompts are prepared; there are zero reviewer submissions and no verified Ukrainian reviewer records. Close only after two independent Ukrainian-native reviewers submit original preferences under frozen criteria and disagreements/adjudication are recorded. This remains separate from Thai IPA correctness. |
| CCOST wordlist | BLOCKED | Reconstructed source matches official MD5; each A–D order has 206 unique rows, but B/C/D each differ from A by two missing and two extra items (208-item union). Do not freeze a derived packet. Close only with written curator/author clarification or an official corrected wordlist/erratum. |
| CCOST TextGrid | BLOCKED | Paper-level tier map is documented, but the released 6.2 GB archive, actual TextGrid tier structure and complete X-SAMPA label inventory have not been inspected. Close only after inspecting the actual archive, confirming tier names and item-level provenance, enumerating all observed labels, and mapping each label to an explicit phonetic/phonemic layer. |
| LOTUSDIS | PARTIAL | Source card/repository and CC BY-SA 4.0 provenance are registered; the source is suitable only as audio/transcript input for new human annotation, not existing IPA gold. Asset registry is header-only. Close only after immutable dataset revision, concrete asset IDs/URIs, SHA-256 hashes, speaker pseudonyms, microphone/channel, overlap status, duration and exact intervals are verified and recorded. Preserve attribution/share-alike; no unverified assets are used. |
| WCAG 2.2 AA | BLOCKED | Automated browser/UI checks are not manual accessibility evidence. Close only with recorded keyboard-only, screen-reader, viewport/device and assistive-technology review, defects, fixes and retest evidence against WCAG 2.2 AA. |
| Dependency/reference graph | PARTIAL | Module ownership and script entry points are documented, but no complete import/call/reference graph or dynamic-entry-point analysis exists. A clean local checkout is unavailable in this session: `git clone` failed because `github.com` could not resolve. Close only after full static import/call/reference extraction plus manual review of CLI, browser, generated, plugin/dynamic and data-driven entry points. |
| Test redundancy | PARTIAL | Two immediately repeated UI assertions were removed in PR #170; this is not a repository-wide redundancy review. Close only after mapping tests to acceptance contracts/layers, identifying overlapping fixtures/assertions, and demonstrating no acceptance-coverage loss through targeted mutation/negative tests or equivalent evidence. |
| Branch protection | TODO — owner decision | Branch protection is an owner-controlled repository policy. Close only after the owner chooses required status checks, review count, stale-review dismissal and bypass policy, then configures and verifies the ruleset. No settings were changed. |

**Exact engineering verification:** commit `d2d3043b61710496f48851f232f69ba836c8e0bc` has successful CI run [41356471529](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41356471529) (all three jobs, including full Python pytest, wheel-install smoke and master-artifact validation), Web Static [41356471455](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41356471455), and external VISTEC [41356471544](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41356471544). This verifies the software state only; it does not close any external/manual gate or establish linguistic accuracy. The narrow-IPA-on-ABSTAIN regression is included in this exact-head full Python suite. A CI-observed RED run for that regression was not obtained.

**PR and branch state:** PR #182 was squash-merged into `main` as `65584d9a3d3d64a8e520dbd32411bef4b0a3dd9e`. PR #181 remains closed unmerged; its all-mode adversarial browser changes are included in PR #182. The branch inventory contains 16 refs, including the dedicated work and post-merge documentation branches; no branch was deleted. No force-push or repository-setting change was made.

**Environment limitation:** repository-wide local graph generation, full test-overlap analysis, local test execution, and actual CCOST archive inspection were not possible through the connector-only session. A direct clone attempt failed with DNS resolution for `github.com`; no local test result is claimed. Source/license constraints remain active: CCOST is CC BY-NC-SA 4.0 and LOTUSDIS is CC BY-SA 4.0. Research intent does not waive these terms.

**Readiness:** engineering-verified research prototype; not release-ready for linguistic accuracy claims. Thai/segmentation accuracy remains `NOT_MEASURED`.



## Audio-evidence granularity follow-up — 2026-11-02

- **DONE_VERIFIED (engineering):** audio assets now retain a required exact `microphone_id` in addition to the normalized microphone category. This preserves the source-level LOTUSDIS `mic` value (the Hugging Face dataset card exposes `mic` as a string field, with values such as `con123`).
- **DONE_VERIFIED (engineering):** whole-file `overlap_status` is descriptive metadata and no longer disqualifies an otherwise usable asset. Each Thai review row now carries `audio_interval_overlap_status`; any audio-backed phonetic claim requires the reviewed interval to be explicitly `NONE`. This allows a verified clean interval in a recording with overlap elsewhere, while still rejecting intervals marked `PRESENT` or `UNKNOWN`.
- Added regression coverage for exact microphone ID requirement and interval-level overlap rejection; the valid narrow-IPA fixture exercises an asset whose whole-file overlap status is `PRESENT` while the selected interval is `NONE`.
- The blind packet headers were updated without pre-filling any reviewer labels. The committed audio asset manifest remains header-only; no real asset, hash, reviewer, or annotation was fabricated.
- Exact code-head verification: `964b4930321e68c77ba5e956e1c0ecd12164ccfa`; CI run [41406087052](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41406087052) passed all three jobs (Python/browser suite, wheel-install smoke, master artifact); Web Static [41406087069](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41406087069) and external VISTEC [41406087050](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41406087050) passed. This is engineering verification, not linguistic accuracy evidence.


## Exact-head verification closeout — 2026-11-02 (supersedes pending status above)

- The earlier note that CI was still running at master-table generation is superseded by the completed exact-head run: CI [41406424727](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41406424727) completed **successfully** on `826fcddad4d66471b1ba95f00c4cc5b5f430e237`.
- All three jobs passed: `test`, `wheel-install-smoke`, and `master-artifact`. The test job completed lint, browser/reference and parity checks, generated-artifact drift checks, source/blind-packet validators, the full Python suite, runtime diagnostics, source-attested IPA diagnostic, segmentation diagnostics, and Ukrainian candidate build check. The wheel was built from the sdist, installed in isolation, and smoke-tested outside the checkout.
- Exact-head Web Static [41406424761](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41406424761) and external VISTEC segmentation evaluation [41406424960](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41406424960) also passed on the same head.
- Provenance distinction: CI [41406087052](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41406087052) ran on implementation commit `964b4930321e68c77ba5e956e1c0ecd12164ccfa`. The additional regression tests for required `microphone_id`, file-level overlap with a clean selected interval, and rejection of an overlapping selected interval were committed in `826fcddad4d66471b1ba95f00c4cc5b5f430e237`; **41406424727 is the CI run that verifies those tests**.
- This is **DONE_VERIFIED engineering**, not linguistic validation. No audio assets or expert annotations were added; Thai IPA/segmentation and Ukrainian practical transcription accuracy remain **NOT MEASURED**. The external evidence gates below remain open.


## Thai G2P literature review — 2026-11-03

| Task / acceptance criterion | State | Evidence / next acceptance |
|---|---|---|
| Audit published Thai G2P evaluation metrics and reference-label provenance | DONE_VERIFIED — literature review completed | Full text inspected for Saychum et al. (2016) and Yamasaki (2022); abstract-level evidence recorded separately for Rugchatjaroen et al. (2019), Morén & Zsiga (2006), Xu & Zhang (2024), Pons Bordería & Aliaga (2021), and Jitwiriyanont & Nantanukul (2026). See `docs/research/thai-g2p-evaluation-literature-2026-11-03.md`. This verifies the literature synthesis, not ClippyFirst accuracy. |
| Keep literature-reported scores separate from this project's evidence | DONE_VERIFIED — reporting rule documented | Saychum's dictionary WER/PER and Yamasaki's primarily Wiktionary-derived 0.931 exact-sequence accuracy are not independent expert gold for this project. Current 42+6 prompts remain unadjudicated; no cross-study numeric comparison or runtime rule change is justified. |
| Independently adjudicate remaining Thai phonology, segmentation and Ukrainian target outputs | BLOCKED — external reviewers required | Existing blind packets and protocols remain prepared; reviewer registry is empty. Acceptance: two qualified independent Thai reviewers plus adjudicator; separate two Ukrainian-native reviewers; frozen labels and disagreement/adjudication logs. |


**Exact-head engineering evidence:** literature checkpoint `450fe4b6527c8019ea7399218daf30222fe190e2` passed Full CI [41536529764](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41536529764) and Web Static [41536529768](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41536529768). Full CI passed `test`, `wheel-install-smoke` and `master-artifact`; pytest 326 passed / 1,185 subtests passed; Ruff, source/blind-packet validators, generators/drift, Python/browser IPA-UA parity, UI/accessibility static checks and segmentation diagnostics passed. This verifies the software/documentation checkpoint, not linguistic accuracy. The subsequent documentation reconciliation requires final exact-head CI.

**Final documentation checkpoint:** `7391688c4c19b295f701812e8d6336bcf6abeb02` passed exact-head Full CI [41537375617](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41537375617) and Web Static [41537375633](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41537375633), including all three Full CI jobs. The structured audit update following that checkpoint is documentation-only and receives its own exact-head run.


## Development methodology review — 2026-11-03

| Item | State | Evidence / acceptance |
|---|---|---|
| Review Superpowers TDD and code-review workflow | DONE_VERIFIED — source reviewed | Inspected upstream `test-driven-development` and `requesting-code-review`; adopt red/green/refactor, expected failure verification and independent review. No skill copied. |
| Review Matt Pocock primary-source research workflow | DONE_VERIFIED — source reviewed | Inspected `skills/engineering/research/SKILL.md`; adopt primary-source traceability and durable notes. Do not adopt its unguarded nested-agent delegation or treat its "primary source" test as sufficient without manual source-quality verification. |
| Review Ponytail minimal-change workflow | DONE_VERIFIED — source reviewed | Inspected `skills/ponytail/SKILL.md`, `AGENTS.md`, README; adopt dataflow-first reading, reuse and minimum complete diff; never remove trust-boundary validation, error handling or accessibility. No benchmark claims imported. |
| Vendor/install upstream skills or dependencies | DEFERRED — unnecessary | No runtime skill host installation requested; no code dependency justified. All three upstream repositories declare MIT, but no code was copied. |
| Correct audit JSON vs PR head drift | DONE_VERIFIED — documentation corrected; final CI pending | Prior PR head 9135187 / 80 ahead / CI 41539140734 and Web Static 41539140594 passed. Structured audit had stale ba71 / 79 ahead values. Current JSON now records the 913 checkpoint and this documentation batch; final exact-head verification required. |
| Academic citation/style checks | PARTIAL — manual correction applied | Academic Writing Toolkit flagged volume/year parentheticals as false-positive citations and did not accept supplied reading-note schema. Reworded volume/year metadata; manual DOI/bibliography inspection retained. British spelling suggestions not applied without a repo-wide style decision. |

**Current documentation checkpoint:** this matrix and the canonical audit/handoff were updated after code checkpoint 913518797bb2eb1e42bc77a7b6fb797ec7b85420. Exact-head CI and Web Static for the resulting documentation commit are required before marking the current docs batch DONE_VERIFIED.


**Exact-head verification:** methodology/audit reconciliation checkpoint `0416fd332382b804b76ab0242ea8ff0b415062ce` passed Full CI [41603648158](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41603648158) and Web Static [41603648119](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41603648119). Full CI passed `test`, `wheel-install-smoke`, and `master-artifact`; Ruff passed; pytest 326 passed / 1,185 subtests passed; evidence/blind-packet validators, generators/drift, diagnostics, IPA-UA/browser parity, static accessibility, segmentation review, wheel install and master artifact passed. This is engineering verification, not expert linguistic validation.


## Terminal exact-head verification — 2026-11-03

- Branch `fix/benchmark-error-clusters-20261102`, PR #189 remains open as Draft; exact branch head `2ec6393655f7d4f58d7b840abd194bf4d0b07efe` is **95 commits ahead of main, 0 behind** (compare against main `75c331f69aa3c8e5b4db3ccc5a6da85124600a01`). Main was not changed.
- Exact-head Full CI [41610404742](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41610404742) completed successfully; all three jobs passed: `test`, `wheel-install-smoke`, and `master-artifact`. Exact-head Web Static [41610404753](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41610404753) passed.
- The test job passed Ruff; pytest **326 passed, 1,185 subtests passed**; source/reviewer and blind-packet validators; generated-artifact drift and master-table registry checks; runtime challenge diagnostics; IPA→Ukrainian adapter; browser parity (**29 fixtures**); UI/accessibility static contracts; segmentation diagnostics; and held-out TUD evaluation. The isolated wheel-install smoke and master-artifact validation passed.
- This is engineering verification only. Challenge coverage remains 32/42 conservative and 36/42 opt-in word-segmented; those are not accuracy scores. Linguistic accuracy remains `NOT_MEASURED`; no independent Thai/Ukrainian gold is claimed. Local tests were not run in the connector-only environment.
- The exact-head result supersedes earlier notes that the final structured-register refresh was pending. PR #189 has no submitted reviews or inline review threads as of this check. Separate research/accessibility PRs and branches were left intact; no branch was deleted, merged or force-pushed.


**Register follow-up:** this terminal section records the last fully verified checkpoint. A subsequent documentation-only reconciliation of the structured audit, matrix, handoff and narrative audit is being committed; its new branch head must receive its own exact-head CI and Web Static checks. No runtime behavior changes in that follow-up.



## Full-text literature audit follow-up — 2026-11-03

The Thai G2P literature synthesis was checked against primary full texts for Saychum et al. (2016) and Yamasaki (2022), and against the publisher abstract for Rugchatjaroen et al. (2019). Saychum's abstract reports 13.66% exact-match WER, while its conclusion and Figure 4 report 13.67%; 3.91% tone-ignored WER and 1.54% 5-gram JSM2 PER remain separate metrics. This discrepancy is now recorded rather than silently selecting one value. Yamasaki's 18,066 Wiktionary-derived entries, two Thai-fluent workers for unresolved entries, 17,720/18,066 candidate coverage, 10-fold evaluation and 0.931 zero-difference accuracy were verified from the ACL Anthology PDF. Rugchatjaroen's 9.94% WER and dictionary coverage above 70% are verified from the publisher abstract only; the full experimental label provenance remains unverified because the publisher full text returned 403.

Academic Writing Toolkit checks: two project-authored US spellings ("behavior") were corrected to British English ("behaviour"); "Modeling" was retained in the exact published title. The two short-paragraph flags correspond to "Full-text findings:" labels, not prose defects, and were not expanded artificially. No new accuracy result or runtime change is claimed. Exact-head CI at `fdc66473f183f3b1d4072aabccebd69d99e6f255` passed after this literature update: [CI 41627403379](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41627403379) (`test`, `wheel-install-smoke`, `master-artifact`) and [Web Static 41627403409](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41627403409). The handoff/matrix/audit reconciliation that follows is documentation-only and changes no runtime or tests.


## Exact-head verification update — 2026-11-03 (supersedes pending notes above)

The previous handoff entries correctly marked the post-`e7ebb28e64afd5ec70fc136a12d6723ccebdd59e` documentation-only reconciliation as awaiting CI. That wait is now resolved: the exact current branch HEAD `fba3e63deeda6e61565e0444dc4685f248dbb763` (116 commits ahead of `main`, 0 behind; main `75c331f69aa3c8e5b4db3ccc5a6da85124600a01`) passed both required workflows:

- Full CI [41646388428](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41646388428): all three jobs passed — `test`, `wheel-install-smoke`, and `master-artifact`. The test job reports Ruff passed; pytest **327 passed, 1,185 subtests passed**; generated-artifact drift, source/reviewer and blind-packet validators, challenge diagnostics (42 inputs; diagnostic only, not accuracy), IPA→Ukrainian adapter, 29-fixture Python/browser parity, UI/accessibility static contracts, Wisesight and dictionary segmentation diagnostics, source-attested IPA diagnostic, held-out TUD evaluation and evidence-grade checks passed. The isolated source-distribution/wheel build and install smoke passed; master artifact validation passed.
- Web Static [41646388317](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41646388317): static validation, browser dictionary generation, JavaScript syntax, required pages, accessibility contract and no-remote-runtime-dependency checks passed.

The test workflow uploaded the current diagnostic and master artifacts (including the Thai challenge runtime diagnostic, segmentation review artifacts and master table). This is engineering verification, not independent linguistic or WCAG conformance evidence. Linguistic accuracy remains `NOT_MEASURED`; source-annotated Wisesight rows remain unadjudicated; hands-on accessibility and external reviewer/corpus provenance gates remain open. Local tests were not run in this connector-only environment. PR #189 remains open Draft; no review submissions or inline review threads were present. No merge, force-push, main update, branch deletion or release was performed.


## Exact-head verification — packaging metadata correction — 2026-11-03

- Code head: `3f5bbbbff4b40899eb273333ec0c06a028d862fd` (**121 commits ahead of main, 0 behind**; main remains `75c331f69aa3c8e5b4db3ccc5a6da85124600a01`). Branch `fix/benchmark-error-clusters-20261102`; PR #189 remains open as Draft.
- Replaced deprecated PEP 621 license-table metadata with SPDX string `license = "MIT"` and raised the declared build-system floor to `setuptools>=77`, the minimum supporting that form. No runtime dependency or linguistic behavior changed.
- Exact-head Full CI [41651609638](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41651609638) completed successfully: `test`, `wheel-install-smoke`, and `master-artifact` all passed. Exact-head Web Static [41651609695](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41651609695) passed.
- Test job: Ruff passed; pytest **327 passed, 1,185 subtests passed**; generated-artifact drift, source/reviewer and blind-packet validators, challenge diagnostics, IPA→Ukrainian adapter, 29-fixture Python/browser parity, UI/accessibility static contracts, segmentation diagnostics/error review, held-out TUD evaluation and evidence-grade checks passed. Wheel job built sdist and wheel, installed the wheel in an isolated environment and smoke-tested packaged data. Master artifact validation passed.
- Build logs show no `SetuptoolsDeprecationWarning` for the former license-table form. A generic pip root-user warning remains informational and unrelated to project metadata.
- This is engineering/packaging verification, not independent linguistic or WCAG conformance evidence. Accuracy remains `NOT_MEASURED`; Thai and Ukrainian expert adjudication, CCOST curator/TextGrid evidence, immutable LOTUSDIS audio provenance, and hands-on accessibility review remain blockers. Local tests were not run in the connector-only environment.


## Exact-head verification — documentation reconciliation — 2026-11-03

- Exact branch HEAD: `3831230c1cf43fae48259b2b2a93c9634ad1e30c`; compare against `main` `75c331f69aa3c8e5b4db3ccc5a6da85124600a01`: **125 ahead, 0 behind**.
- Full CI [41654235310](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41654235310) completed successfully. All three jobs passed: `test`, `wheel-install-smoke`, and `master-artifact`.
- Web Static [41654235435](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41654235435) completed successfully.
- The test job's recorded successful steps include Ruff, generated-artifact drift and master-table registry checks, source/reviewer and blind-packet validators, complete Python tests, 42-input runtime diagnostics explicitly guarded against accuracy claims, IPA→Ukrainian adapter, 29-fixture Python/browser parity, UI/accessibility static contracts, segmentation diagnostics, source-attested IPA evidence-grade checks, and held-out TUD evaluation. The wheel-install and master-artifact jobs also passed.
- This closes the exact-head engineering verification gap for the documentation checkpoint. It does not establish independent Thai/Ukrainian linguistic accuracy or WCAG 2.2 AA conformance. Linguistic accuracy remains `NOT_MEASURED`; Thai and Ukrainian expert adjudication, CCOST curator/TextGrid evidence, immutable LOTUSDIS audio provenance, and hands-on accessibility testing remain open. Local tests were not run in the connector-only environment.
- PR #189 remains open Draft; no review submissions or inline review threads were present at this check. `main` was not changed; no merge, force-push, branch deletion, or release was performed.


## Session verification reconciliation — 2026-11-03

- Current PR #189 branch head before this documentation-only update: `7ba27004ba5dc9e60fd1f9c57a686b90cf490ae9`; current `main`: `75c331f69aa3c8e5b4db3ccc5a6da85124600a01`; GitHub compare reports 129 commits ahead, 0 behind.
- Exact-head Full CI [41656371625](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41656371625) completed successfully on `7ba27004ba5dc9e60fd1f9c57a686b90cf490ae9`; all jobs passed: `test`, `wheel-install-smoke`, `master-artifact`. The test job reports Ruff clean, pytest **327 passed, 1,185 subtests passed**, generated-artifact drift and master-table checks, evidence/blind-packet validators, 42-input runtime diagnostics explicitly labelled non-accuracy, IPA→Ukrainian checks, 29-fixture Python/browser parity, static UI/accessibility checks, segmentation diagnostics/error review, held-out TUD evaluation, and evidence-grade assertions passed. Exact-head Web Static [41656371599](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41656371599) also passed.
- Engineering review comment [5758597272](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/189#pullrequestreview-5758597272) records the source/provenance and fail-closed review. PR #189 remains Draft and unmerged; no runtime changes were made in this reconciliation. `main` was not changed.
- The lexical recovery remains evidence-limited: pinned Wiktionary revisions support lexical segmentation/reading entries, but are CC BY-SA 4.0 source-attested references, not independent Thai expert or acoustic gold. Runtime coverage is not accuracy. Linguistic accuracy remains `NOT_MEASURED`.
- Related open drafts remain separate: #190 (narrow source-level form-control contrast correction; manual WCAG testing still blocked), #188 (restricted Global TIMIT Thai source review), and #184–#186 (optional FastThaiG2P research/typed diagnostic work; not production promotion). They are not merged or silently consolidated because their scopes, evidence gates and overlapping audit/source-registry changes differ.
- Remaining acceptance gates: two qualified independent Thai reviewers plus adjudication for IPA/tones/length/segmentation; two independent Ukrainian-native reviewers and adjudication; CCOST A–D curator clarification and actual TextGrid/X-SAMPA archive inspection; immutable LOTUSDIS audio revision and asset hashes/interval metadata; hands-on keyboard, screen-reader, zoom/reflow and mobile accessibility testing. Global TIMIT remains restricted and is not IPA gold.
- Environment boundary: connector-only GitHub access; no local checkout or local pytest/browser/device run is claimed. No audio assets, gold labels, accuracy scores, releases, force-pushes or branch deletions were created.


## 2026-11-04 consolidated integration gate — PR #199

| Workstream | State | Remaining acceptance gate |
|---|---|---|
| Thai spacing-vowel segmentation (#191) | DONE_VERIFIED on base main | Preserve Python/browser parity in combined CI |
| G2P challenge triage and lexical recoveries (#189) | PARTIAL pending combined CI | Run generated-artifact, test and source-registry gates on final head |
| Global TIMIT Thai (#188) | BLOCKED | Written LDC authorization; not gold and no download before rights |
| LOTUSDIS metadata (#192) | Metadata DONE_VERIFIED; audio PARTIAL | Actual WAV bytes, recomputed SHA-256, interval and overlap/channel review |
| FastThaiG2P adapters/typed IPA (#184–186) | PARTIAL pending combined CI | Preserve provenance, uncertainty and fail-closed unsupported output |
| FastThaiG2P site API/runtime (#193) | PARTIAL | Resolve upstream data rights and verify deployment preview |
| Accessibility contrast (#190) | Static check passed on revised head | Hands-on keyboard, screen-reader and device testing |
| Independent phonetic validation | BLOCKED | Qualified independent Thai/Ukrainian reviewers and acoustic gold |

DONE_VERIFIED for the consolidated batch requires all checks on the final PR #199 head. Individual PR-head CI and base-main CI are supporting evidence only.


## Final consolidated status — 2026-11-04

| Workstream | Final status | Evidence / remaining blocker |
|---|---|---|
| Thai spacing-vowel segmentation (#191) | DONE_VERIFIED | Present in starting main; regression coverage passed in consolidated CI |
| G2P challenge triage and lexical recoveries (#189) | DONE_VERIFIED (engineering) | Consolidated CI, generated master artifact and evidence registries passed |
| Global TIMIT Thai source audit (#188) | DONE_VERIFIED as restricted-source audit; data use BLOCKED | Source/rights limits registered and validated; LDC authorization remains absent |
| LOTUSDIS immutable snapshot (#192) | Metadata DONE_VERIFIED; audio PARTIAL | Shard manifest and stable row locator present; WAV bytes/hash/interval/overlap review remain missing |
| FastThaiG2P adapters and typed IPA (#184–186) | DONE_VERIFIED (engineering) | Typed boundary, challenge workflow, optional smoke and integration checks passed |
| FastThaiG2P site API/runtime (#193) | DONE_VERIFIED (engineering); production deployment BLOCKED | Site API tests passed; no rights-cleared Vercel preview yet |
| Non-text contrast/accessibility (#190) | Static DONE_VERIFIED; manual PARTIAL | Static contract and selected contrast checks passed; keyboard/screen-reader/device checks remain |
| Final main Pages workflow | DONE_VERIFIED (validation only) | Run 41898680278 succeeded; deploy intentionally skipped pending Vercel preview gate |
| Independent linguistic validation | BLOCKED | Independent Thai/Ukrainian reviewers and acoustic gold are not available |

**Final engineering integration:** DONE_VERIFIED on main `324632e59b6da68ece1c40c90dd3e4f4e1287447`. **Release readiness:** NOT READY; linguistic accuracy remains NOT_MEASURED and the rights/deployment/reviewer blockers above remain open.


## Evidence registry regression closeout — 2026-11-04

| Item | Status | Verification |
|---|---|---|
| Six source-attested lexical references (#189) | DONE_VERIFIED — registry + regression tests | Exact URL, CC-BY-SA-4.0, allowed lexical/IPA-reference use and disallowed gold use are tested |
| Global TIMIT Thai restricted source (#188) | DONE_VERIFIED — audit + regression test; data use remains BLOCKED | LDC URL, non-member agreement, restricted allowed-use and blocked gold-use assertions are tested |
| Consolidated evidence registry | DONE_VERIFIED | PR #202 CI run 41899981649: full test, wheel-install-smoke and master-artifact all passed |

Latest main at this checkpoint: `5b2f65e9745bf396a37fd8775504256bb1e193cc`.


## Final integration status — 2026-11-04

| Workstream | Status | Evidence / remaining gate |
|---|---|---|
| Thai spacing-vowel segmentation (#191) | DONE_VERIFIED | Already on main before consolidated integration; combined CI passed |
| Lexical/G2P challenge recovery (#189) | DONE_VERIFIED (engineering) | Runtime diagnostics, source-pinned entries, Python/browser parity and combined CI passed; no accuracy claim |
| Global TIMIT Thai (#188) | DONE_VERIFIED as restricted-source audit; data use BLOCKED | Source and rights limits registered; written LDC authorization still required |
| LOTUSDIS (#192) | Metadata DONE_VERIFIED; audio PARTIAL | Immutable shard manifest and row locator present; audio bytes/hash/interval/overlap review missing |
| FastThaiG2P adapters and typed IPA (#184–186) | DONE_VERIFIED (engineering) | Optional adapter, typed boundary, comparison and integration checks passed; external data rights remain unresolved |
| FastThaiG2P site API/runtime (#193) | DONE_VERIFIED (engineering); production deployment BLOCKED | Site API checks passed; Vercel preview and data rights not cleared; Pages deployment gate intentionally skipped |
| Non-text contrast/accessibility (#190) | Static DONE_VERIFIED; manual PARTIAL | Static contrast/accessibility checks passed; hands-on keyboard/screen-reader/device review outstanding |
| Post-merge regression/audit (#200–203) | DONE_VERIFIED | Pages gate, audit, evidence registry tests and docs closeout merged |
| Open pull requests | NONE | GitHub open-PR query returned an empty list |

**Final main before this doc refresh:** `a65b0d24ccb4f1eb2720d800a17578d552f067a2`; exact-head CI [41901296995](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41901296995) passed test, wheel-install-smoke and master-artifact. Engineering integration is DONE_VERIFIED; release readiness remains NOT READY and linguistic accuracy remains NOT_MEASURED.


## Live reconciliation — 2026-11-05

- Branch: `docs/repository-audit-2026-11-04`; verified head: `41ef3f1e3a3e23f216ee16e6d3cfbb4244b00722`. GitHub compare against `main` reports **9 commits ahead, 0 behind** (base `56fba86b4b8be2fe4e67284355e9928108527387`).
- PR [#210](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/210) remains **OPEN / NOT MERGED**. No merge, force-push, branch deletion, release or change to `main` is claimed.
- Exact-head GitHub Actions CI run [41921113154](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41921113154) for `41ef3f1e3a3e23f216ee16e6d3cfbb4244b00722` completed **success**. This is GitHub-hosted CI evidence; no local test run is claimed.
- Readiness remains **engineering-verified research prototype**. Linguistic accuracy is **NOT_MEASURED**; there are still **zero independently adjudicated IPA gold rows**.

### External evidence and rights gates — current status

| Gate | Status | What is required to change status |
|---|---|---|
| Independent Standard Thai phonetic/segmentation expertise | BLOCKED | Qualified independent Thai reviewers, blind first-pass annotations, documented adjudication and inter-annotator agreement; no engine-derived labels counted as gold. |
| Independent Ukrainian-native target review | BLOCKED | Independent native-speaker review of target forms and a recorded adjudication outcome, separate from Thai IPA review. |
| Global TIMIT Thai | BLOCKED | Written authorization from LDC covering the intended access, processing, evaluation and any redistribution; until then, do not download, process, publish or redistribute restricted Thai material. |
| LOTUSDIS audio | PARTIAL | Obtain the actual authorized WAV assets; verify each file's SHA-256 from bytes; pin source/version; verify speaker/channel, clean intervals, overlap and alignment against the annotation records. Metadata or archive hashes alone do not satisfy this. |
| FastThaiG2P bundled-data rights | BLOCKED | Source-by-source license/terms and attribution review demonstrating that redistribution and intended use are permitted. Keep data excluded from production bundles until cleared. |
| FastThaiG2P Python-host preview | BLOCKED | Deploy to a Python-capable preview host and record a reproducible live smoke/contract test against the deployed URL; a static Pages pass or API unit test is not a hosted preview. |
| Manual accessibility review | PARTIAL | Record keyboard-only, screen-reader, zoom/reflow and mobile checks against the active UI, including browser/AT versions, steps, outcomes and defects. Automated checks are not conformance evidence. |
| CCOST TextGrid and tier mapping | PARTIAL | Published LREC 2026 paper verifies ORT/KAN/KAS/MAU/MAS/TRN, X-SAMPA and tone suffix mapping; actual 6.2 GB archive/TextGrid files and manual remain uninspected. Complete file-level tier/interval verification and document discrepancies. CC BY-NC-SA 4.0 applies; no unrestricted redistribution. No formal IAA was collected in the paper. |

### Evidence policy

Do not mark any gate DONE_VERIFIED because a registry entry, schema, blank reviewer packet, model output, source annotation, static check or documentation paragraph exists. Keep CCOST under CC BY-NC-SA 4.0 restrictions; keep Global TIMIT Thai unused pending written LDC permission. Keep LOTUSDIS PARTIAL until actual WAV bytes and per-file hashes/interval evidence are verified. Keep FastThaiG2P production data and preview gates separate. Do not create or report independent IPA gold rows until the blinded expert adjudication has actually happened.


## Text-only corpus and FastThaiG2P rights review — 2026-11-05

| Work item | Status | Evidence / decision | Next acceptance |
|---|---|---|---|
| Global TIMIT Thai text-only phones/tones | BLOCKED_FOR_ACCESS | LDC2022S13 provides Word/Phones/Tones/TextGrid TXT; non-member agreement allows non-commercial research and limited publication excerpts but forbids bulk redistribution outside the research group. Audio is not required for our intended text-only use. | Obtain signed non-member agreement and fee/access details; ask LDC whether a small derived phonetic test subset may be published. Do not publish full extracted labels. |
| LOTUSDIS text-only transcripts | PARTIAL | CC BY-SA 4.0; public Hugging Face rows expose sentence, speaker, mic and duration. Paper documents utterance-level transcripts, speaker labels and overlap tags, not phone/IPA tiers. Audio/hash work is DEFERRED / OUT OF SCOPE. | Keep optional for conversational vocabulary and orthographic robustness; inspect TextGrid only if word-level text alignment would materially help. Do not count as phonetic gold. |
| CCOST text-only phonetic annotations | PARTIAL | LREC 2026 publishes ORT/KAN/KAS/MAU/MAS/TRN tiers, X-SAMPA and tone suffixes; CC BY-NC-SA 4.0 is compatible with stated non-commercial research subject to attribution and ShareAlike. No formal IAA was collected. | Request TextGrid-only export/manual; inspect actual tiers and intervals; independently review a stratified subset. No WAV required. |
| FastThaiG2P code and data | PARTIAL | Apache-2.0 code reusable with NOTICE; Wiktionary IPA subset is CC BY-SA 3.0; merged 62k map includes generated IPA; TLTK fallback data has unresolved file-level license mapping. Upstream's cited 34/17 gold files return 404. | Reuse code selectively; isolate Wiktionary subset with attribution/ShareAlike; keep generated IPA provisional; obtain TLTK file-level license clarification before bundling. |
| FastThaiG2P Python-host preview | BLOCKED | Separate deployment gate; unrelated to text-data reuse. | Verify live Python-capable preview independently if the web deployment remains in scope. |

**Scope correction:** LOTUSDIS audio bytes, per-file WAV hashes, waveform overlap and audio interval verification are no longer acceptance tasks for this text-only research objective. Preserve any historical audio-oriented audit entries as history, but treat them as DEFERRED/OUT OF SCOPE rather than blockers. No audio was downloaded in this review.


## Source-level follow-up — CCOST labels and FastThaiG2P rights (2026-11-05)

| Task | Status | Evidence / next acceptance |
|---|---|---|
| Inspect 488 CCOST TextGrids | DONE_VERIFIED | Run 42018381197; 488/488 parsed, text-only |
| Inventory CCOST failure occurrences | DONE_VERIFIED | 1,014 occurrences / 116 unique raw labels, classified in `docs/ccost-label-review-2026-11-05.md` |
| Confirm `<p:>`, `<usb>`, `<nib>` semantics | DONE_VERIFIED | CCOST LREC 2026 §3.3 and BAS Partitur Format |
| Classify `<P>`, `<P:>`, `<:p>`, `<Fail>`, `<notProcessedChunk>` | BLOCKED | No corpus-specific definition located; curator response required |
| Resolve `_8` (868 occurrences) | BLOCKED | Generic BAS/MAUS syntax allows `_1`–`_9`, but CCOST paper documents only `_1`–`_5`; source-specific meaning of `_8` is unknown |
| Confirm `-MAU` aliases | BLOCKED | Exact names observed; semantic mapping not defined by paper/manual |
| FastThaiG2P source-code license | DONE_VERIFIED | Exact pinned commit contains Apache-2.0 LICENSE and Amazon NOTICE; TLTK parser retains BSD-3 notice |
| FastThaiG2P bundled-data redistribution | BLOCKED | Wiktionary/kaikki subset has CC BY-SA/GFDL; generated/manual/TLTK fallback asset rights need per-component evidence |
| Promote CCOST/FastThaiG2P candidates to gold | BLOCKED | Independent Thai review and adjudication still required; gold rows remain 0 |

The current X-SAMPA converter remains a declared partial subset. These findings do not promote any source label or FastThaiG2P output to independent IPA gold.


### CCOST marker handling correction — 2026-11-05

- Corrected `is_ccost_nonphonetic_label`: it recognizes only source-documented `<p:>`, `<nib>`, and `<usb>`.
- Unknown tag-only labels (`<Fail>`, `<P>`, `<P:>`, `<:p>`, `<notProcessedChunk>`) now remain unsupported and raise rather than being silently skipped.
- Added regression test `test_undocumented_tag_only_labels_fail_closed`; existing mixed-marker tests remain.
- Acceptance: code and regression test changes are committed; exact-head CI is still required before marking this behavior DONE_VERIFIED.


## Follow-up evidence review — CCOST and FastThaiG2P — 2026-11-05

### Evidence established from primary sources

- The CCOST LREC 2026 paper §3.3–3.4 defines MAU as the phonetic segment tier, MAS as the phonemic syllable tier, KAN as canonical word pronunciation, KAS as canonical syllabified pronunciation, ORT as orthographic word, and TRN as orthographic utterance transcript. It says phonemic/phonetic labels use X-SAMPA and documents only tone suffixes _1–_5.
- The paper does **not** explain the extra -MAU suffix in the supplied release's ORT-MAU, KAN-MAU, KAS-MAU names. Their relationship to the unsuffixed tiers remains curator-confirmation work.
- CCOST source paper and BAS docs support <p:>, <usb>, and <nib> as non-phonetic event markers in the applicable annotation context. <P>, <P:>, <:p>, <Fail>, and <notProcessedChunk> remain unresolved.
- FastThaiG2P's pinned source-code license is Apache-2.0, its NOTICE identifies Amazon, and its vendored TLTK parser has a BSD-3-Clause file header. Its bundled runtime dictionary is mixed-provenance: Wiktionary/kaikki entries (CC BY-SA/GFDL), model-generated entries, and manual overrides; TLTK fallback data is also bundled. No single blanket license/complete rights ledger for all bundled dictionary and fallback assets was found.
- The TLTK project README states BSD-3-Clause for package versions from 1.2.2, but file-level rights/provenance for every copied fallback data asset remain unconfirmed.

### Updated task ledger

| Task | Status | Acceptance / blocker |
|---|---|---|
| Define base MAU/MAS/KAN/KAS/ORT/TRN tier roles | DONE_VERIFIED | CCOST LREC 2026 paper §3.3–3.4 |
| Explain ORT-MAU/KAN-MAU/KAS-MAU suffix semantics | BLOCKED | Curator response needed; raw names preserved |
| Explain 868 _8 occurrences / 22 strings | BLOCKED | Generic MAUS allows _1–_9; CCOST paper maps only _1–_5; do not infer a CCOST category |
| Clarify unresolved tag spellings and mixed labels | BLOCKED | Curator response needed; fail-closed behavior retained |
| Verify FastThaiG2P source-code license | DONE_VERIFIED | Pinned LICENSE Apache-2.0; NOTICE checked |
| Verify vendored TLTK parser notice | DONE_VERIFIED | Pinned source carries BSD-3-Clause notice |
| Clear redistribution of all FastThaiG2P bundled dictionary/fallback data | BLOCKED | No complete component-level rights ledger; do not bulk redistribute |
| Contact CCOST authors/curators | PARTIAL | Official emails and copy-ready request prepared; NOT SENT because no email-sending connector is available |
| Receive curator explanation | BLOCKED | No message sent / no response received |

The copy-ready request and public contact evidence are in [external-review-and-source-requests.md](external-review-and-source-requests.md). The detailed reviews are [CCOST labels](ccost-label-review-2026-11-05.md) and [FastThaiG2P rights](fastthaig2p-license-review-2026-11-05.md). Linguistic accuracy remains NOT_MEASURED; independent IPA gold rows remain 0.

## Current task reconciliation — 2026-11-05 (CCOST adjudication worklist)

The following entries supersede earlier rows that described the entire CCOST archive or `_8` problem as wholly uninspected. Historical entries remain for chronology; this is the current task ledger for the three requested workstreams.

| Work item | Status | Evidence / remaining acceptance |
|---|---|---|
| Inspect supplied CCOST TextGrids | DONE_VERIFIED | CI parsed 488/488 long-text TextGrids; no audio member was read. |
| Classify documented `-MAU` tier names | DONE_VERIFIED | BAS tutorial defines ORT-MAU, KAN-MAU and KAS-MAU; exact release names are preserved. |
| Establish CCOST meaning of `_8` | BLOCKED | Generic BAS/MAUS syntax allows `_1`–`_9`; CCOST paper maps only `_1`–`_5`. `_8` has no established CCOST category mapping; do not infer a value. |
| Recover intended values for `_8` | BLOCKED | 868 tier occurrences = 397 exact interval groups = 438 file/interval/raw-label events across 119 files. Worklist supplies orthographic/cross-tier context; two independent Thai reviewers and a separate adjudicator must supply evidence-backed corrections or abstentions. No automatic replacement. |
| Determine semantics of `<P>`, `<P:>`, `<:p>`, `<Fail>` | BLOCKED | Existing whole-archive counts: 394, 4, 22, 16 appearances respectively. Worklist scans all tiers and preserves case/interval/context. No reliable public corpus-specific definition located; expert adjudication or authoritative corpus documentation required. |
| Generate contextual blind CCOST review worklist | DONE_VERIFIED_IMPLEMENTATION_CHECKPOINT; FINAL_WORKFLOW_ASSERTIONS_PENDING | Generator, tests and CI artifact step are committed; exact-head CI must pass and artifact counts must be inspected before DONE_VERIFIED. |
| Independent Thai phonetic review and adjudication | BLOCKED | Reviewer registry is empty; no reviewer contacted or appointed; no blind packets completed; no adjudication report; independent IPA gold rows remain 0. Acceptance: two verified independent reviewers, frozen original annotations, separate adjudicator, documented disagreements/abstentions and agreement report. |
| Acoustic validation of surface realizations | DEFERRED / OUT OF SCOPE | User scope is text/phonetic-text only; no audio is read or distributed. Do not claim acoustic tone, duration or allophonic accuracy. |

The new worklist uses stable event-group IDs and includes exact raw labels, tier/time provenance, overlapping cross-tier labels and adjacent same-tier labels. See [CCOST label review](ccost-label-review-2026-11-05.md), [independent adjudication protocol](independent-adjudication-protocol.md), and [reviewer qualification shortlist](reviewer-outreach-shortlist.md).


## Exact all-tier CCOST review-worklist reconciliation — 2026-11-05 (supersedes prior count scope)

| Work item | Status | Evidence / acceptance |
|---|---|---|
| Build blind CCOST review worklist | PARTIAL_PENDING_EXACT_HEAD_CI | `scripts/build_ccost_review_worklist.py`, focused tests and CI artifact step exist. Full CI run 42034879862 passed all jobs on implementation checkpoint 47db8ac988836014663a435e08e2afe470342fe8; artifact 13418750385 was downloaded and inspected (1,975 rows, all 11 expert fields blank, audio_members_read=0). A later workflow-only assertion commit remains pending its exact-head CI. |
| `_8` grouping | DATA_INVENTORY_DONE; VALUE_RECOVERY_BLOCKED | 868 tier occurrences; 397 exact file/interval groups; 438 file/interval/raw-label events; 22 raw strings; 119 files. Two blind Thai reviews and separate adjudication must produce supported corrections or abstentions. |
| Unknown markers in all tiers | INVENTORY_DONE; SEMANTICS_BLOCKED | Worklist all-tier: 821 intervals with any marker, 871 marker appearances; per-marker interval counts `<P>` 771, `<Fail>` 24, `<P:>` 4, `<:p>` 22; appearance counts `<P>` 821, `<Fail>` 24, `<P:>` 4, `<:p>` 22. These counts were checked in downloaded artifact 13418750385. Earlier inspector figures `<P>` 394 and `<Fail>` 16 cover phonetic tiers only. Neither inventory establishes marker semantics. |
| Documented MAUS processing failure | DONE_VERIFIED | `<notProcessedChunk>`: 142 intervals/appearances in the worklist; retain as processing failure, never convert to IPA. |
| Independent Thai phonetic review/adjudication | BLOCKED | Reviewer registry empty; no consent/contact/appointment or completed independent annotations. Acceptance: two verified qualified independent Thai phoneticians, blind first-pass annotations, separate adjudicator, frozen originals, disagreement/abstention log, and validator-approved provenance. |
| Audio/acoustic surface validation | DEFERRED / OUT OF SCOPE | User-prioritized scope is TextGrid text only. No audio member is read. Do not claim acoustic tone contour, duration, speaker-specific allophony or surface realization accuracy. |

The all-tier worklist counts are deliberately distinct from the phonetic-tier-only inspector counts. Preserve both denominators and scope labels in future reports. Artifact inspection is complete for implementation checkpoint 47db8ac; only the subsequent workflow-only assertion update awaits its exact-head CI.


## Independent Thai expert panel — public-source screening (2026-11-05)

Public qualification evidence now supports a plausible, uncontacted panel:
- Chutamanee Onsuwan, Ph.D. — Thai temporal phonetics; laboratory phonetics, speech science and phonology (Thammasat official profile).
- Phanintra Teeranon, Ph.D. — peer-reviewed acoustic/perceptual studies of Standard Thai tones (University of Phayao public CV and publications).
- Rungpat Roengpitya — peer-reviewed acoustic studies of Thai tones, vowel length and fricatives (Mahidol profile and proceedings).

Proposed role split: Onsuwan + Teeranon as independent first-pass reviewers; Roengpitya as separate adjudicator. Public bibliographic evidence shows none is a CCOST paper author. This is only a candidate panel: verify current qualifications, Standard Thai competence, IPA/X-SAMPA familiarity, independence/conflicts, availability, consent and permission to retain qualification evidence before adding anyone to the reviewer registry.

Lena Maluleem remains a qualified phonetics/prosody candidate, but her public publication and doctoral-supervision record links her to CCOST author Pittayawat Pittayaporn. Treat this as a potential conflict for independent CCOST review; do not count her as independent without a documented assessment.

The reviewer registry remains empty. No one has been contacted, appointed or consented. Independent IPA gold rows remain 0.


## Latest exact-head continuation — 2026-11-05

| Work item | Status | Evidence / remaining acceptance |
|---|---|---|
| All-tier unresolved-marker interval inventory | DONE_VERIFIED | 821 tier-interval rows, 871 appearances, 398 exact file+interval groups; per-marker groups: <P> 375, <P:> 4, <:p> 11, <Fail> 8. CI asserts all denominators. |
| Exact-interval cross-tier _8 counterpart scan | DONE_VERIFIED_INVENTORY_ONLY | 14/397 _8 groups have another phonetic tier with a mapped _1–_5 suffix at the exact same interval: MAU _2 7; MAS _2 4; MAS _3 4; KAN-MAU _3 1. This is review evidence, not a repair rule. |
| _8 original-value recovery | BLOCKED | Generic MAUS allows _1–_9; CCOST paper maps only _1–_5. Recover only with positive source-specific evidence and independent Thai review; abstain otherwise. |
| <P>, <P:>, <:p>, <Fail> semantics | BLOCKED | 398 exact time groups are inventoried; exact spelling and case retained. No authoritative public CCOST definition located. |
| Worklist generator, focused tests and CI artifact | DONE_VERIFIED | Full CI run 42036060620 passed all three jobs on ebd1f0a55b2987c40725659b1524d26ad21abc0c; test log: 394 passed, 1 skipped, 1,211 subtests passed; Ruff passed. Artifact 13418563592 downloaded and inspected: 1,975 rows; all 11 human fields blank; audio_members_read=0. |
| Independent Thai expert adjudication | BLOCKED | Reviewer registry empty; no consent/contact/appointment or completed blind annotations. Acceptance requires two verified independent Thai phoneticians, frozen blind submissions, a separate adjudicator, disagreement/abstention log and validated provenance. |
| Audio-backed review | BLOCKED_PENDING_SELECTIVE_AUDIO_ACCESS_AND_NONCOMMERCIAL_SCOPE_CONFIRMATION | Zenodo lists a 6.2 GB WAV+TextGrid archive under CC BY-NC-SA 4.0. No audio was downloaded. Implement opt-in selective per-recording retrieval; do not download full archive in routine CI. |

**Convention correction:** _8 is not generically invalid MAUS syntax (BAS allows _1–_9); it is unmapped in CCOST's published five-tone mapping. This distinction is binding for all future documentation and prevents a false claim that _8 is a sixth Thai tone or an invalid MAUS token.


## Final exact-head acceptance — 2026-11-05

| Work item | Status | Evidence / remaining acceptance |
|---|---|---|
| CCOST blind worklist and exact interval context | DONE_VERIFIED | Full CI 42039619729 on 43fa978d passed all 3 jobs; test 395 passed, 1 skipped, 1,211 subtests; Ruff and 29 parity fixtures passed. Artifact 13421040388 downloaded and inspected: 1,975 rows, 488 TextGrids, all 11 human fields blank, no audio read. |
| All-tier marker group counts | DONE_VERIFIED_INVENTORY_ONLY | 871 literal appearances; 821 tier-interval rows; 398 exact file+interval groups. Per marker: <P> 375, <P:> 4, <:p> 11, <Fail> 8. Semantics remain BLOCKED. |
| Exact-interval cross-tier mapped-tone candidates | DONE_VERIFIED_INVENTORY_ONLY | 14 of 397 _8 groups; MAU _2 7, MAS _2 4, MAS _3 4, KAN-MAU _3 1. Context only, no repairs. |
| Recover original _8 values | BLOCKED | Generic MAUS permits _1–_9; CCOST paper maps _1–_5 only. Requires positive source-specific evidence and independent Thai adjudication. |
| Resolve <P>, <P:>, <:p>, <Fail> semantics | BLOCKED | No authoritative CCOST-specific definitions located. Preserve exact spelling/case. |
| Independent Thai expert review/adjudication | BLOCKED | Reviewer registry header-only; no contacts, consent, appointments or annotations. Acceptance requires two qualified independent first-pass reviewers, a separate adjudicator, frozen submissions, disagreement/abstention log and validated provenance. |
| Acoustic review | BLOCKED_PENDING_SELECTIVE_AUDIO_ACCESS_AND_NONCOMMERCIAL_SCOPE_CONFIRMATION | Zenodo lists a 6.2 GB WAV+TextGrid archive under CC BY-NC-SA 4.0; no audio accessed. Selective per-recording retrieval and non-commercial scope check required; no full archive download in routine CI. |

Exact-head Site API run 42039619784 and external G2P smoke run 42039619715 both SUCCESS on 43fa978d.


---

## Owner-approved beta scope update — 2026-11-05

- The owner has selected a **beta release** rather than a linguistically validated release. Two independent Thai reviewers plus adjudicator, and independent Ukrainian-native target-form review, are **DEFERRED** and are not beta acceptance gates. Do not represent these items as completed.
- Audio acquisition and acoustic/narrow-phonetic validation remain **DEFERRED / OUT OF SCOPE**. No audio is required for this beta.
- Unknown CCOST labels and tone suffix _8 remain **PARTIAL / fail-closed**. Preserve raw labels and abstain; beta scope does not authorize guessed mappings.
- Manual accessibility certification is **DEFERRED as a certification gate**, not passed. Static source review is recorded in docs/beta-release-scope.md; browser keyboard, screen-reader, zoom/reflow, forced-colors and device checks remain unverified. Do not claim WCAG conformance.
- FastThaiG2P vendoring remains deferred; the pinned optional dependency path is retained. Do not redistribute mixed assets without component-level attribution/notices.
- The mfwarren/entrepreneur-claude-skills repository is used only for relevant operational patterns (SOP, product feedback, decision-making and landing-page communication). It contains no dedicated accessibility skill; WCAG criteria remain the accessibility basis. No third-party skill files were copied.
- Beta engineering readiness is **BETA_CANDIDATE_ENGINEERING_VERIFIED; PUBLIC_DEPLOYMENT_NOT_YET_VERIFIED**. The previous exact-head code CI on 5a7f6888420009e288f6b43332bd0dd4b560fddd passed Full CI, Site API and optional external G2P smoke. The subsequent documentation-only commits have not yet been verified by their own exact-head CI at the time of this note.
- Acceptance to proceed from candidate to public beta: exact-head CI on the final candidate; verified Python-capable hosting preview with same-origin API; published feedback path; dependency/corpus notices; beta warnings; known limitations and manual accessibility gaps disclosed. No release tag, production cutover or merge is performed here.

Canonical scope and checklist: docs/beta-release-scope.md.



## GitHub Pages-only FastThaiG2P port — evidence reconciliation (2026-11-05)

This section supersedes earlier requirements for a Python-capable external preview or Vercel hosting. The owner selected GitHub Pages as the only hosting target and approved the Pyodide browser port. No remote API or CDN is part of the browser path.

| Work item | Status | Evidence / acceptance |
|---|---|---|
| Shared Python service in self-hosted Pyodide 0.29.5 | DONE_VERIFIED | Same service adapter is used by CPython and browser worker; CPython/Pyodide JSON parity passed four Thai cases. |
| Same-origin Chromium worker | DONE_VERIFIED | Cold initialization and warm analysis passed; no `/api/analyze` or CDN requests. |
| FastThaiG2P dictionary provenance filter | DONE_VERIFIED | 13,144 Wiktionary entries retained; 48,957 generated entries excluded; manual/unknown excluded by policy; one stale metadata IPA value for `สวน` is disclosed. |
| TLTK fallback asset provenance | DONE_VERIFIED | Five assets byte-identical; `sylform_var.pkl` equals exact bzip2 decompression of TLTK `sylform_var.pklz`; all six asserted by `scripts/verify_tltk_fallback_provenance.py`. |
| Runtime notices | DONE_VERIFIED | Ten source license/NOTICE files staged; bundle builder checks required filenames and hashes. |
| Transparent share-alike dataset copy | PARTIAL | Build emits a standalone ZIP containing filtered `dict.txt`, `ipa.json`, provenance, attribution and CC BY-SA 4.0 notice; new ZIP packaging and deploy hash assertion await exact-head CI. |
| TLTK license scope | PARTIAL | Vendored parser header says 1.3.8/BSD-3; pinned data-source snapshot says setup.py 1.9.1/BSD-3, root LGPL-3, module BSD-style LICENSE.txt and stale PKG-INFO 1.1.7/GPLv3. Both notices are preserved; file-level scope unresolved. |
| Public Pages redistribution | BLOCKED | `redistribution_approved=false`; explicit owner approval and final TLTK license-scope review required. Do not change repository variables or publish the runtime without approval. |
| Pages deployment/live smoke | BLOCKED | No merge to `main`, Pages deployment or production cutover has occurred. After rights approval and merge, verify manifest, notice hashes, dataset ZIP hash, Pyodide runtime and actual browser interaction at the published Pages URL. |
| Linguistic validation | PARTIAL / NOT A DEPLOYMENT GATE | Independent IPA gold 0; accuracy `NOT_MEASURED`; Ukrainian practical forms provisional. |

Exact verified runtime checkpoint: `80adb489105e6f2b447fb07331bfdf0c09c888b3`.
- Pyodide compatibility + TLTK verifier + Chromium: [42085653176 SUCCESS](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42085653176).
- Web static: [42085653505 SUCCESS](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42085653505).
- Site API reference wrapper: [42085653055 SUCCESS](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42085653055).
- Optional external smoke: [42085652951 SUCCESS](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42085652951).
- Full CI run 42085653265 was cancelled by subsequent pushes; do not count it as passed. The later dataset archive changes require a fresh exact-head Full CI and Pyodide run.

Canonical implementation and rights records: `docs/fastthaig2p-pyodide-port.md`, `docs/fastthaig2p-data-provenance.md`, `data/third_party/fastthaig2p-browser-bundle.json`, and `web/third-party-notices.html`.

---

## Exact-head GitHub Pages port verification — 2026-11-05

| Work item | Status | Evidence / remaining acceptance |
|---|---|---|
| Shared Python service used by FastAPI wrapper and browser worker | DONE_VERIFIED | Exact-head Pyodide and Site API workflows 42090379707 / 42090379612 passed. |
| Pyodide 0.29.5 CPython parity | DONE_VERIFIED | Four Thai inputs passed in 42090379707. |
| Real same-origin Chromium worker | DONE_VERIFIED | Cold/warm run, FastThaiG2P IPA regression, no API/CDN requests; run 42090379707. |
| Source-filtered FastThaiG2P browser wheel | DONE_VERIFIED | 13,144 Wiktionary records retained; 48,957 generated records excluded; manual/unknown fail-closed; one metadata mismatch disclosed. |
| TLTK fallback asset transformations | DONE_VERIFIED | Five byte-identical files plus one exact bzip2 decompression; source verifier passed in earlier run 42085653176. |
| TLTK file-level license scope | PARTIAL / PUBLICATION BLOCKER | Preserve BSD-3 and LGPL-3 notices; owner/legal review must establish which terms apply to each copied file. |
| Third-party notice page and ten local notices | DONE_VERIFIED | Web Static 42090379866 and Full CI 42090379627 passed; the CC BY-SA legal code and transparent dataset archive are linked. |
| Public Pages redistribution | BLOCKED | `redistribution_approved=false`; explicit owner authorization and TLTK license-scope review required. |
| Live Pages bundle hash and browser smoke | BLOCKED | Run only after authorization and merge; deploy workflow validates every runtime/notice/dataset hash and real interaction. |
| Actual Pages cold-start/mobile performance | TODO | Measure after the authorized deployment. |
| Manual accessibility testing | DEFERRED / UNVERIFIED | Not a beta certification gate; do not claim WCAG conformance. |

Exact-head verification: `ba22872679869371e92ab9ad511db4ed74627da2`; workflows Pyodide 42090379707, Site API 42090379612, Web Static 42090379866, optional external smoke 42090379819, Full CI 42090379627 all SUCCESS. PR #210 remains open/unmerged; main unchanged. Public deployment has not occurred.



## Current publication status — 2026-11-05 (supersedes earlier deployment blockers)

| Work item | Status | Evidence / acceptance |
|---|---|---|
| Owner authorization for research-project publication | DONE_VERIFIED | Recorded in the browser bundle rights manifest on the PR branch and merged to main; authorization does not waive third-party terms. |
| PR #210 integration | DONE_VERIFIED | Squash merge `c5618d8adfdfd0a12415fc083e5f5a518ae4c5c1`. |
| GitHub Pages build and deployment | DONE_VERIFIED | [Run 42098396098 SUCCESS](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42098396098). |
| Post-deploy live content/worker contract | DONE_VERIFIED | Run 42098396098 checked page copy, worker JS, styles, system page, no API/CDN path, Pyodide manifest and runtime. |
| Dataset ZIP path and integrity | DONE_VERIFIED | Smoke corrected to `/vendor/{dataset.path}`; exact size and SHA-256 passed in run 42098396098. |
| Third-party notices and attribution | DONE_VERIFIED | Ten required notices fetched live and checked by size/SHA-256; third-party page attribution checks passed in run 42098396098. |
| Pyodide runtime and browser parity | DONE_VERIFIED | [Run 42098395877 SUCCESS](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42098395877), including real Chromium same-origin worker smoke. |
| Main CI | DONE_VERIFIED | [Run 42099035122](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42099035122) SUCCESS on main `f0d41996e854185bd6bd92f0ffa8f6b83e71f777`; the earlier 42098395810 run was an intermediate checkpoint and is superseded. |
| TLTK file-level license scope | PARTIAL / DISCLOSED | Both LGPL-3.0 and BSD-3-Clause notices preserved; owner approved research-project publication, but this does not resolve the ambiguity or alter third-party obligations. |
| Deployed performance and manual accessibility | TODO / DEFERRED | Measure cold-start/repeat latency, memory/mobile performance; manual keyboard, screen-reader, zoom/reflow and forced-colors checks remain unverified. No WCAG conformance claim. |
| Linguistic accuracy | PARTIAL / NOT MEASURED | Independent IPA gold = 0; Ukrainian forms provisional. External Thai/Ukrainian expert audits and acoustic validation are deferred from beta scope. |

Live beta: https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/ .


## Ukrainian-first UX implementation checkpoint — 2026-11-06

| Work item | Status | Evidence / remaining acceptance |
|---|---|---|
| Central Ukrainian user-message catalog | IMPLEMENTED_PENDING_EXACT_HEAD_CI | `web/src/messages.uk.js` defines progress, empty, success, clipboard and error copy plus stable `UA-*` support IDs. |
| Prevent upstream English errors reaching user copy | IMPLEMENTED_PENDING_EXACT_HEAD_CI | Worker sends error codes and separate diagnostics; UI maps codes to Ukrainian copy and uses a generic Ukrainian fallback for unknown codes. |
| Optional technical diagnostics | IMPLEMENTED_PENDING_EXACT_HEAD_CI | Collapsed details panel; raw diagnostic is separate from user copy; Worker redacts exact input text before posting exception details. |
| Localize engine warnings and provenance caption | IMPLEMENTED_PENDING_EXACT_HEAD_CI | Result renderer maps known English warning classes to Ukrainian and uses a conservative Ukrainian fallback; provenance caption translated. |
| Automated localization/UI regression tests | IMPLEMENTED_PENDING_EXACT_HEAD_CI | New `web/tests/ukrainian-first.test.mjs`; UI contract expanded; Web Static workflow runs both suites and syntax checks. |
| GitHub beta feedback form | IMPLEMENTED_PENDING_EXACT_HEAD_CI | `.github/ISSUE_TEMPLATE/beta-feedback.yml` is now Ukrainian; test checks name, category, field labels, privacy confirmation and absence of English labels. Web Static also triggers when the template changes. |
| Full public-page language inventory | TODO | Audit all static pages, aria labels, titles, placeholders, feedback templates and notices; preserve proper names and legal source titles. |
| Manual browser and assistive-technology acceptance | DEFERRED / NOT VERIFIED | Keyboard, screen reader, 200%/400% zoom, narrow mobile reflow and real clipboard permissions require browser/device review. |
| Privacy explanation | TODO / EVIDENCE REQUIRED | Verify GitHub Pages logging and any storage/telemetry facts before publishing claims. |
| Ukrainian phonetics glossary and plain-language help | TODO | Explain IPA, tone, vowel length and provisional adaptation in Ukrainian; linguistic claims require evidence review. |

Implementation branch: `feat/ukrainian-first-ux-2026-11-06`. Do not mark the implementation DONE_VERIFIED until exact-head CI and the Pages deployment/browser smoke succeed. No phonetic rules or linguistic accuracy claims changed. See [Ukrainian-first UX contract](ukrainian-first-ux.md).


## Owner-approved FastThaiG2P native JavaScript/TypeScript port — 2026-11-06

| Work item | Status | Evidence / acceptance |
|---|---|---|
| Owner decision and port scope | DONE_VERIFIED | Decision recorded in `docs/fastthaig2p-javascript-port.md`; prior Pyodide-only constraint superseded. |
| Native dictionary IPA/result adapter | PARTIAL | `web/src/fastthaig2p-native.js` parses slash/dot IPA, preserves Chao tone and vowel length, and delegates to existing IPA→Ukrainian adapter. Unit contract added; not integrated into public UI. |
| Filtered native dictionary + normalizer + wordlist assets | DONE_VERIFIED | Pyodide compatibility #42181862972 built 5 native assets and verified sizes/SHA-256; source pins and CC BY-SA / Apache-2.0 / CC0 licenses recorded. |
| Normalizer port | DONE_VERIFIED | #42181862972: 18 pinned CPython cases passed with the extracted PyThaiNLP default wordlist, including mai yamok, numbers, symbols, abbreviations, email and units. |
| PyThaiNLP newmm tokenizer | DONE_VERIFIED | #42181862972: 16 custom FastThaiG2P token-array cases passed; 18 default-wordlist cases also passed inside normalizer parity. |
| TLTK OOV fallback | BLOCKED / PARTIAL | All six transforms verified. Data is 19,883,873 bytes raw / 5,911,457 bytes deterministic gzip estimate. Rights scope still needs explicit disposition (BSD package metadata/LICENSE.txt vs LGPL root LICENSE and stale GPLv3 PKG-INFO); algorithm/parity not ported. |
| Native front-half pipeline parity | DONE_VERIFIED | #42181862972: 16 dictionary-only CPython pipeline cases matched normalized text, tokens and raw IPA. Full typed/result JSON parity including OOV remains TODO. |
| Native Worker smoke | DONE_VERIFIED | #42184407769: Chromium native Worker matched all 16 CPython front-half cases and fail-closed OOV; same-origin JS/data only, no Python/Pyodide/wheels/WASM/remote requests. | 
| Cold/warm/offline and mobile performance | TODO | Isolated Worker smoke passes; still measure transfer size, cold/warm latency, cache reuse, offline reload, memory and mobile devices. |
| Public UI runtime selector and cutover | DEFERRED | Only after TLTK rights, OOV parity, full result parity, cold/warm/offline, CSP and performance gates pass. |
| Pyodide removal | DEFERRED | Remove only after production cutover is verified and rollback path is retained. |

The public site still uses Pyodide. The native normalizer, default/custom newmm tokenizers, dictionary-only pipeline and isolated Chromium Worker smoke have differential evidence, but the TLTK OOV fallback and UI cutover are not complete; do not claim full replacement or a speed improvement. No IPA or Ukrainian phonetic rules were changed; linguistic accuracy remains `NOT_MEASURED`.


## Native FastThaiG2P exact-head reconciliation — 2026-11-06

The following replaces earlier, now-stale native-port status rows above. Historical entries are retained for audit traceability.

| Work item | Current status | Exact evidence / remaining acceptance |
|---|---|---|
| Native normalizer and newmm tokenizer | DONE_VERIFIED | Exact-head Pyodide compatibility #42186384082 passed 18 normalizer and 16 custom tokenizer differential cases against pinned Python references. |
| Native dictionary-covered service pipeline | DONE_VERIFIED | The 16-case reference compares the complete service JSON, including Ukrainian adaptation, tone/length metadata, rules, provenance and warnings; all cases passed. This does not cover OOV. |
| Native Chromium module Worker | DONE_VERIFIED (isolated) | #42186384082 passed 16 real Chromium Worker cases plus Ukrainian fail-closed OOV. Request audit found no Python, Pyodide, wheel, WASM or remote API requests. |
| TLTK fallback data provenance | DONE_VERIFIED (transformation only) | Six pinned source transformations verified: five byte-identical and one exact BZip2 decompression. Report retains SHA-256 evidence and contradictory license records. |
| TLTK fallback rights and native OOV port | BLOCKED / PARTIAL | BSD-3-Clause package metadata and LICENSE.txt coexist with LGPL-3.0 root LICENSE and stale GPLv3 PKG-INFO. Keep fallback code/data out of native bundle until rights disposition; then port algorithm and verify OOV/result parity. |
| Web Static | DONE_VERIFIED | #42186383919 SUCCESS on exact code head 24e4605b7921524b60dc1c5a3e3e9a66965a3206. |
| Full CI | DONE_VERIFIED | #42186383939 SUCCESS on exact code head; test, wheel-install smoke and master-artifact generation/validation all succeeded. |
| Pyodide compatibility and browser checks | DONE_VERIFIED | #42186384082 SUCCESS on exact code head; Pages bundle build, production Pyodide Worker smoke and isolated native Worker smoke all succeeded. |
| Public UI native runtime integration/cutover | DEFERRED | Keep current Pyodide production path until TLTK rights/OOV parity, typed contract, mobile/offline/CSP and measured performance acceptance pass. |
| Cold/warm/offline/mobile performance and memory | TODO | Measure actual Pages transfer and browser cache behavior, startup and repeat latency, memory, offline reload and mobile devices against the same Pyodide baseline. |

Current branch head at this verification: 24e4605b7921524b60dc1c5a3e3e9a66965a3206. Public site still uses Pyodide. Overall native port is a verified dictionary-covered prototype, not a complete FastThaiG2P replacement; accuracy remains NOT_MEASURED and no speedup is claimed.


## Native-first UI reconciliation — 2026-11-06

This section supersedes the earlier statement that the native Worker was not connected to the public UI. The code implementation is present; the current acceptance run is pending.

| Work item | Current status | Evidence / acceptance |
|---|---|---|
| Native dictionary-covered runtime | DONE_VERIFIED (earlier exact head) | 16 complete service JSON cases match pinned CPython; real Chromium native Worker smoke passed with no Pyodide/Python/wheel/WASM/remote requests on head 24e4605b7921524b60dc1c5a3e3e9a66965a3206. |
| Public UI native-first integration | DONE_VERIFIED on PR #216 head; post-merge deploy pending | Dictionary hits use the native Worker; misses first lazy-load the TLTK OOV pack and native parser; Pyodide is last-resort only. Exact-head CI, Web Static, Pages build and Pyodide/Chromium compatibility passed on d4f35892adc02eb03b1fd345a0193c46c07b1eb7. Live post-merge Pages smoke remains TODO. |
| OOV reference fixture | DONE_VERIFIED | Pinned Python reference generator produced 64 single-token OOV cases with zero rejected candidates; all 64 exact typed-service outputs match the native module and native Worker. Chromium UI smoke confirms lazy same-origin TLTK loading and no Python/Pyodide/API/CDN requests for supported OOV. |
| Native TLTK OOV implementation | DONE_VERIFIED for pinned FastThaiG2P/TLTK path; Pyodide retained as last resort | Browser-native port implements TLTK syllable parsing, tone assignment, transformations, segmentation/collocation, candidate scoring and IPA conversion. 64/64 exact Python-service parity cases and real Worker/Chromium tests passed. TLTK 1.9.1 packaged fallback assets are supported by BSD-3-Clause package evidence; retain separate root LGPL-3.0 and stale 1.1.7/GPLv3 notices as historical context. |
| Native UI user disclosure | DONE_VERIFIED (code present) | Input hint and system page explain native-first dictionary handling, lazy TLTK OOV loading, and Pyodide as last-resort compatibility fallback. |
| Cold/warm/offline/mobile performance and memory | TODO | Measure same-origin transfer, cold/warm latency, browser cache, offline reload, memory and mobile performance against the Pyodide baseline. |
| Exact-head CI/Web Static/Pages build/Pyodide compatibility | DONE_VERIFIED on PR #216 head | d4f35892adc02eb03b1fd345a0193c46c07b1eb7: CI 42217143967 SUCCESS (401 passed, 1 skipped, 1211 subtests); Web Static 42217143995 SUCCESS; Pages build 42217143962 SUCCESS; Pyodide compatibility 42217144084 SUCCESS. Main-branch post-merge CI and live Pages deploy remain TODO. |

The application is hybrid native-first, not a complete Pyodide removal. Dictionary-covered inputs use the browser JavaScript worker and do not fetch Python/Pyodide. OOV inputs first lazy-load the TLTK 1.9.1 data-only pack (2,844,409 compressed bytes; 19,848,231 uncompressed bytes: 267 syllable patterns, 2,127 syllable dictionary entries, 68,702 phone trigrams, 364,726 syllable trigrams and 65,431 word-dictionary entries). TLTK-supported OOV cases run in native JavaScript; Pyodide is retained as the last-resort compatibility path only when TLTK cannot complete. The initial native dictionary/normalizer/default-wordlist assets remain approximately 2.2 MB; the larger OOV pack is lazy. Exact parity with 64 independently generated pinned Python-service OOV cases passed in both module and worker tests, and Chromium verified no Python/Pyodide/wheel/API/CDN requests for supported OOV. This establishes engine parity, not independent phonetic accuracy; accuracy remains NOT_MEASURED. No speedup claim is made; cold/warm/offline/mobile performance and memory remain TODO.


Latest verified code head: `d4f35892adc02eb03b1fd345a0193c46c07b1eb7`. Exact-head CI 42217143967, Web Static 42217143995, Pages build 42217143962 and Pyodide compatibility 42217144084 passed. Documentation checkpoint `06fa145f476ade86996a065983b3014a20b2a5a8` also passed CI 42218587500 (401 passed, 1 skipped, 1211 subtests), Web Static 42218587220, Pages build 42218587339 and Pyodide compatibility 42218587302. Post-merge main CI and live Pages deployment remain TODO.


## Native TLTK OOV follow-up — 2026-11-06

| Gate | Status | Evidence / acceptance |
|---|---|---|
| PR #217 / mainline TLTK OOV parity | DONE_VERIFIED | PR #217 merged as `533cd3f8df6112b000f5c91524f8050026b4d79a`. Exact PR-head CI 42226080426 SUCCESS (401 passed, 1 skipped, 1211 subtests; Ruff and wheel-install smoke passed); Pages build 42226080435 SUCCESS (17,205,333-byte artifact; deploy skipped on PR event); Pyodide compatibility 42226080581 SUCCESS. TLTK OOV: 64/64 module parity, 64/64 Worker parity, Chromium checks passed. |
| TLTK 1.9.1 package rights for six fallback assets | DONE_VERIFIED_WITH_CONDITIONS | BSD-3-Clause package scope evidenced by README, setup.py/package_data, MANIFEST.in, LICENSE.txt and PyPI metadata. Research use requires no special exception. Redistribution requires retained notice, conditions, disclaimer and no-endorsement clause. Separate root LGPL-3.0 and stale 1.1.7/GPLv3 metadata remain disclosed; no blanket license claim for all repository files. |
| Post-merge main Pages deployment and live URL smoke | BLOCKED_EVIDENCE_ACCESS | Pages workflow's main-push trigger and live smoke commands are present. PR build passed, but PR deploy is skipped by design. Current GitHub connector exposes PR-triggered workflow runs only; combined status has no contexts; public Pages fetch was inaccessible and Firecrawl credits were exhausted. Acceptance: main push deploy SUCCESS and live fetch/hash checks for app, native worker, TLTK manifest/data, notices and Pyodide fallback. |
| Performance, manual accessibility, independent linguistic accuracy | TODO / NOT_MEASURED | No cold/warm/offline/mobile or memory benchmark; no manual AT/device audit; no independently adjudicated Thai IPA gold or Ukrainian expert validation. |

