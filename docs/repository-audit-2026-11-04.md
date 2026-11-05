## Latest exact-head repository verification — 2026-11-05

- Branch: `docs/repository-audit-2026-11-04`; HEAD: `f9b6baf1ad3c55057051ff5652ac7827a06fd7c1`; base `main`: `56fba86b4b8be2fe4e67284355e9928108527387`; comparison: **136 commits ahead, 0 behind**.
- PR [#210](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/210) is **OPEN, not merged**, targets `main`, and is mergeable. No mainline change, force-push, branch deletion or release was made.
- Exact-head Full CI [run 42016775144](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42016775144) succeeded on this HEAD. Jobs `test`, `wheel-install-smoke`, and `master-artifact` all passed. The test job reports **385 passed, 1 skipped, 1,206 subtests passed**; Ruff passed; 29 Python/browser parity fixtures passed; generated-artifact drift checks, source/reviewer packet validators, archive inspection, JSONL export, and artifact upload passed.
- The one skip is `tests/test_fastthaig2p_site_api.py` in the generic environment because FastAPI is optional and absent there. Dedicated FastThaiG2P Site API [run 42016775080](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42016775080) passed; optional external Thai G2P smoke [run 42016775087](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42016775087) passed.
- CI re-inspected 578/578 supplied TextGrid files and verified 178,377 orthographic JSONL rows (CCOST 145,434; LOTUSDIS 32,943). The current `textgrid-text-only-jsonl` artifact is [available from run 42016775144](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42016775144/artifacts/13410071688), 12,609,560 bytes, artifact digest `sha256:98089f717561e86116c3f6aeef278d3ca84beaa50c5d0ea5d52a1a27b5ed6323`. It contains text-only exports, manifest and notices; no audio is read or included.
- Linguistic status is unchanged: independent IPA gold rows **0**; accuracy **NOT_MEASURED**. The CCOST adapter remains PARTIAL with 1,014 unsupported labels; `_8`, Unicode IPA-looking strings, unusual sequences and mixed marker/text labels remain fail-closed.
- Current blockers: CCOST curator clarification of `-MAU` aliases and unsupported labels; two qualified independent Thai reviewers plus adjudicator; independent Ukrainian-native target review; hands-on accessibility review; FastThaiG2P bundled-data rights and Python-host preview. Global TIMIT and audio tasks remain DEFERRED/EXCLUDED by owner decision.
- Local tests were not run in this connector-only session. The exact-head GitHub Actions evidence above is the verification record; no local checkout or local test execution is claimed.
- Readiness: **ENGINEERING_VERIFIED_RESEARCH_PROTOTYPE_NOT_RELEASE_READY**. Software/packaging/CI gates pass, but independent linguistic and human accessibility gates remain unmet.

## Supplied TextGrid completion checkpoint — 2026-11-05

- Work branch: `docs/repository-audit-2026-11-04`; PR #210 remains open and unmerged against `main` (`56fba86b4b8be2fe4e67284355e9928108527387`). `main` was not modified. The final implementation/workflow checkpoint verified below is `824c09098d2869256ab8206324b3e1fa1d6d6d81`; subsequent commits in this continuation refresh documentation and source notices.
- Owner-supplied `CCOST textgrid.zip` (488 `.TextGrid` members) and `nectecLOTUSDIS textgrid.zip` (90 `.TextGrid` members plus `textgrid/.DS_Store`) are committed on the branch. Git blob SHA-1s: `3b1e3978c2b3a232dce4fdcfd137bb572ce5467f` and `50518e9a54e0986935e7b1cff122eb43c0b9edbd`; these pin branch files, not upstream publisher checksums.
- Final exact-head CI [42015757949](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42015757949) passed on `824c09098d2869256ab8206324b3e1fa1d6d6d81`: 385 Python tests passed, 1 optional FastAPI test skipped, 1,206 subtests passed; Ruff, wheel-install smoke, master-artifact, 578-file inventory, 178,377-row JSONL export, manifest validation and license-notice artifact upload passed. Dedicated Site API [42015757883](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42015757883) and optional external Thai G2P smoke [42015757971](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42015757971) also passed.
- CI parsed 578/578 supplied TextGrid files. CCOST has observed tiers `ORT-MAU`, `KAN-MAU`, `KAS-MAU`, `MAU`, `MAS`, `TRN`; LOTUSDIS has one recording-named transcript IntervalTier per file and one skipped `.DS_Store` metadata entry. CCOST's 488 file count matches the recording-file total in LREC 2026 Table 1.
- Added `scripts/export_textgrid_text.py` and tests. It exports explicitly selected orthographic intervals with raw text, time bounds, source/tier, archive Git blob SHA-1, license, attribution and `SOURCE_ANNOTATED_NOT_GOLD`. CI verified 178,377 records (CCOST 145,434; LOTUSDIS 32,943) and publishes artifact `textgrid-text-only-jsonl` containing both JSONLs, a validated SHA-256 manifest and the third-party notice. No audio member is read.
- Strict tag-only marker handling now leaves mixed tag-plus-Thai-text labels visible as unsupported. CCOST has 1,014 unsupported phonetic-tier labels; `_8`, Unicode IPA-looking forms, unusual sequences and mixed labels remain fail-closed. The LREC paper documents only `_1`–`_5`.
- Updated `data/corpus_sources.csv`, `data/THIRD-PARTY-CORPUS-NOTICES.md`, validation matrix, corpus validation, CCOST adapter guide, architecture/script inventories, external clarification request and handoff. The former request for a TextGrid-only archive is superseded by a request to clarify `-MAU` tier aliases, `_8`, Unicode IPA-looking forms and annotation tags.
- No audio bytes were read, extracted, hashed or copied. No source annotation has been promoted to gold. Independent IPA gold rows remain 0; linguistic accuracy remains `NOT_MEASURED`.
- Remaining evidence gates: curator clarification of release-specific tier/label semantics; full X-SAMPA/IPA conversion coverage; two qualified independent Thai reviewers plus separate adjudication; independent Ukrainian-native target review; hands-on keyboard/screen-reader/zoom/reflow/mobile accessibility review. Global TIMIT and audio tasks remain DEFERRED/EXCLUDED by owner decision.
- Local tests were not run in this connector-only environment. GitHub Actions is the verification evidence; do not claim a local checkout or local test execution.
---
## Exact-head verification and current source scope — 2026-11-05

- Branch: `docs/repository-audit-2026-11-04`; implementation checkpoint `f8e19499c056afeb2b2532887d2887812472664d`; exact-head CI [41992116524](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41992116524) passed all jobs: 376 Python tests passed, 1 optional FastAPI test skipped, 1,206 subtests passed; Ruff, wheel-install smoke and master-artifact passed.
- Dedicated FastThaiG2P Site API [41992116526](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41992116526) passed; optional external G2P smoke [41992116614](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41992116614) passed.
- The optional FastAPI test is skipped only in the generic development environment because FastAPI is not installed there; the dedicated site-api workflow installs it and passed.
- X-SAMPA output uses canonical NFD. Spaces separate tokens but do not imply syllable boundaries; only explicit periods and CCOST numeric tone suffixes close syllables. Unknown symbols fail closed.
- Global TIMIT is DEFERRED/EXCLUDED by owner decision. LOTUSDIS is optional orthographic text context only. Audio acquisition, hashing, acoustic review and narrow acoustic claims are OUT OF SCOPE.
- CCOST remains the primary phonetic-text candidate. The converter/parser is engineering-verified against synthetic and published Figure 2 fixtures, but actual released TextGrid compatibility remains unverified. Zenodo lists only a mixed 6.2 GB WAV+TextGrid ZIP; no TextGrid-only archive is exposed. No archive/audio was downloaded.
- The TextGrid-only export request is prepared but NOT SENT because no email connector is connected. Independent broad-phonemic IPA gold remains BLOCKED on TextGrid-only sample access, two qualified Thai reviewers and a separate adjudicator; gold rows 0; linguistic accuracy NOT_MEASURED.
- PR reconciliation: PR #193 was closed unmerged; the FastThaiG2P site integration is present on `main` through PR #199, merged 2026-11-04. PRs #184–#186, #188 and #190 are closed unmerged and left untouched. PR #210 is the only currently open PR and remains unmerged. No main change, branch deletion, force-push or release was made.
- Local tests were not run in this connector-only session; GitHub Actions is the verification evidence.

---

## Current owner scope and implementation — 2026-11-05

This current section supersedes earlier Global TIMIT access tasks and LOTUSDIS audio acquisition/validation tasks in the chronological audit below. Those historical notes are retained for traceability, not as active work.

- Global TIMIT Thai: DEFERRED/EXCLUDED by owner decision. Do not pursue LDC access, fees, agreements, text/audio labels or derived files.
- LOTUSDIS: optional text-only orthographic context; no audio acquisition, hashes, acoustic review or phone-level gold.
- CCOST: primary phonetic-text candidate. Implemented strict X-SAMPA→IPA conversion, CCOST numeric tone metadata, Praat long-text TextGrid parsing, tier-aware typed provisional results, synthetic tests and published Figure 2 regression examples.
- No CCOST TextGrid-only export is publicly listed; the mixed 6.2 GB WAV+TextGrid archive was not downloaded. Curator request prepared but not sent because no email action is connected.
- Actual released TextGrid encoding and tier/label inventory remain unverified. No source corpus rows have been promoted to independent gold. Audio is out of scope.
- Branch remains docs/repository-audit-2026-11-04 and PR #210; no merge, new branch, force push, release or main modification.

## Source-register implementation reconciliation — 2026-11-05

- Updated `data/corpus_sources.csv`: LOTUSDIS is now a text corpus with transcript-only scope and no assumed phone/IPA labels; Global TIMIT is explicitly excluded by owner decision. Existing CCOST and Wiktionary source records were retained.
- Added a current text-only policy and task ledger to `docs/corpus-validation.md`. Audio-specific acquisition, hashing and acoustic validation are out of scope.
- Reconciled the CCOST manual evidence: the manual is recorded as inspected on 2026-11-01; actual released TextGrid tier instances and label values remain uninspected.
- Existing FastThaiG2P adapter is preserved: it keeps external IPA separate from typed phonemic/broad-surface IPA and marks output provisional. No generated dictionary rows were promoted to gold.

## User decision — 2026-11-05: Global TIMIT excluded; text-only sources prioritized

The project owner has decided to **exclude Global TIMIT Thai (LDC2022S13)**. Do not pursue LDC access, fees, agreements, audio, or derived labels. Its phone/tone reference role is not a project dependency; alternatives are CCOST text annotations plus selectively reusable, provenance-separated FastThaiG2P/Wiktionary candidates. This is a scope decision, not a claim that Global TIMIT is low quality.

**Active source roles**
- **CCOST — PRIMARY phonetic-text candidate (PARTIAL):** obtain TextGrid-only export/manual; inspect actual MAU/MAS tier instances; implement and test X-SAMPA → typed IPA conversion; independently review a stratified subset. No audio.
- **FastThaiG2P — SUPPORTING lexical/IPA candidates (PARTIAL):** reuse Apache-2.0 code with NOTICE and only the separately licensed Wiktionary-derived subset after source/version attribution. Generated IPA and undocumented manual overrides remain provisional, never gold. Do not redistribute TLTK data until file-level rights are clarified.
- **LOTUSDIS — OPTIONAL orthographic/context corpus (PARTIAL):** conversational vocabulary and text robustness only; not phonetic gold. Audio-specific tasks are OUT OF SCOPE.
- **Global TIMIT — DEFERRED/EXCLUDED by owner decision:** no further acquisition or legal-access work.

**Next acceptance gates:** (1) request CCOST TextGrid-only files and manual; (2) inspect tier values and encoding, not just the published tier names; (3) build a documented X-SAMPA mapping with round-trip/edge-case tests and typed IPA preservation; (4) curate a legally attributable Wiktionary subset separately from generated FastThaiG2P rows; (5) decide whether LOTUSDIS text is useful after inspecting its actual text schema. Do not add corpus rows or claim linguistic accuracy until provenance and review gates pass.

# Repository audit and documentation closeout — 2026-11-04

## Scope and method

Audited the live default branch, recursive repository tree, repository instructions, package metadata, CI workflow, code/data/schema/test layout, documentation ownership, current branch and pull-request state, recent commits, and the current Actions runs. Compared the repository's agent-workflow conventions with the four requested public references: [Unlazy](https://github.com/Leonxlnx/unlazy), [Superpowers](https://github.com/obra/superpowers), [Matt Pocock's skills](https://github.com/mattpocock/skills), and [Ponytail](https://github.com/DietrichGebert/ponytail).

This is a source-tree and GitHub-hosted audit. No local checkout or local test execution was available through the connected GitHub interface. CI evidence below is therefore explicitly GitHub Actions evidence.

## Executive result

The repository already has a mature, unusually explicit structure for a research prototype. It has a root agent contract, a documentation index, architecture ownership map, script inventory, a canonical validation matrix, an audit register, a chronological handoff, machine-readable schemas, provenance/license records, generated-artifact ownership, Python and browser test suites, and static dependency/test-overlap auditing. A wholesale reorganization would create churn and duplicate existing governance. The correct action is to preserve this structure and repair stale status/documentation, not invent a second docs system.

The highest-priority documentation defect was stale repository state. The README's former reference to Draft PR #193 was stale: PR #193 was closed unmerged; the FastThaiG2P site integration is present on main through PR #199, merged 2026-11-04. Production deployment remains separately gated by external data-rights and verified-preview requirements.

## Current GitHub state

- Default branch: `main`.
- Audited base commit: `56fba86b4b8be2fe4e67284355e9928108527387`.
- Live branch inventory: two branches — `main` and `docs/repository-audit-2026-11-04`. The latter is the dedicated documentation/audit branch for this work; no unrelated branch was deleted.
- Open pull requests: one — [PR #210](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/210), this audit branch. The live compare now reports 9 commits ahead and 0 behind `main`; PR #210 remains open and unmerged. The exact-head CI for `41ef3f1e3a3e23f216ee16e6d3cfbb4244b00722` passed run [41921113154](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41921113154). Subsequent documentation-only reconciliation commits are separately awaiting exact-head verification.
- Exact-head Full CI for the inspected PR head `4b3e58a7c714e1f0a517ebf39299f974b5cf5998` passed [run 41919548444](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41919548444): `test`, `wheel-install-smoke`, and `master-artifact` all completed successfully. This is separate from the base-main runs listed below.
- Latest full CI on the audited base: [run 41918227400](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41918227400), completed **success**.
- GitHub Pages workflow on the audited base: [run 41918227410](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41918227410), completed **success**. This is the Pages workflow result; it must not be misrepresented as proof that the separately gated FastThaiG2P production deployment or its Vercel preview has been approved.
- Web static validation [run 41918227382](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41918227382) and FastThaiG2P site API [run 41918227381](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41918227381) succeeded.
- The full CI workflow includes Ruff, generated-artifact drift checks, source/reviewer and blind-packet validators, complete pytest suite, static repository dependency/test inventory, runtime diagnostics, Python/browser parity, UI/accessibility contracts, segmentation diagnostics, and wheel-install smoke. The workflow definition is in `.github/workflows/ci.yml`.

## Architecture and repository organization

The current layout is coherent and should be retained:

| Area | Responsibility | Source of truth / boundary |
|---|---|---|
| `src/thai_ukrainian/` | Python reference engine, public interfaces, typed IPA adapter, segmentation and evidence handling | Python package implementation and public API tests |
| `web/src/` | Browser implementation and presentation | Browser modules; parity tests against Python |
| `data/thai/` | Thai grapheme, vowel, tone, orthographic, lexical and segmentation registries | Human-maintained source registries with dataset-specific provenance/licensing |
| `data/benchmark/` | Frozen and supplemental challenges, blind packets, source-attested/annotated diagnostics and run records | Evidence grades and adjudication state are explicit |
| `data/derived/`, `docs/generated-audit.json`, `docs/source-final-manifest.json`, `docs/syllable-space.json` | Reproducible derived outputs | Owning generators; never hand-edit |
| `schemas/` | Machine-readable analysis, corpus and renderer contracts | Runtime validators and schema tests |
| `scripts/` | Generators, validators, evaluation, audit and packaging checks | `scripts/README.md` is the script ownership map |
| `tests/`, `web/tests/` | Python and browser behavior, negative cases and parity | CI is the executable acceptance contract |
| `docs/` | Architecture, linguistic method, evidence, operational requirements and research history | `docs/README.md` assigns canonical ownership |

The primary pipeline remains Thai orthography → structural analysis → Thai phonology → typed IPA → Ukrainian IPA adaptation → practical Ukrainian orthography. The optional RTGS rendering remains a separately labelled romanization path. This separation is a critical correctness invariant, not a documentation preference.

## Findings

### DONE_VERIFIED — repository structure and governance

- Root `AGENTS.md` explicitly tells agents which canonical docs and CI contract to read, how to work test-first, how to preserve linguistic evidence boundaries, and how to verify before claiming completion.
- `docs/README.md` maps canonical documentation by concern and explains ownership/lifecycle of generated versus hand-maintained documents.
- `docs/architecture.md` maps Python/browser ownership, data flow, typed IPA boundary, RTGS separation and static-audit limits.
- `scripts/README.md` inventories script responsibilities and warns against converting diagnostics into gold evidence.
- CI runs `scripts/audit_repository_structure.py`, producing a static dependency and test-overlap artifact. Its own documentation correctly states that static import analysis is not a complete runtime call graph and that similarity clusters are not automatic grounds for deleting tests.
- Packaging metadata, citation metadata, MIT project license, third-party notices and dataset-specific notices are present.
- No speculative new package hierarchy or second execution ledger is justified.

### DONE_VERIFIED — current code and test organization

- Python implementation is grouped by domain (orthography, parser, phonology, tone, typed IPA, Ukrainian adaptation, segmentation, API/CLI/server).
- Browser modules are similarly separated by analysis, IPA adaptation, RTGS reference and presentation.
- Data schemas, source registries, benchmark inputs and generated outputs have distinct locations.
- CI runs the project-defined checks and the latest main CI run succeeded on the audited SHA.
- The current main commit is therefore engineering-verified by CI; this does not establish independent linguistic accuracy.

### PARTIAL — public product/deployment description

- The README incorrectly described the FastThaiG2P site integration as an unmerged Draft PR #193 and implied the current Pages site was unchanged pending integration.
- Correct status: integration code and API are merged and validated; production deployment remains a separate gate requiring rights clearance and a verified Python-capable preview. A successful Pages workflow is not equivalent to clearing those conditions.
- The RTGS and IPA-first routes must continue to be described as separate methods.

### PARTIAL / BLOCKED — research and external acceptance

These are not structural defects and cannot be closed by reorganizing files or rewriting docs:

- Independent Thai phonetic/segmentation adjudication and independent Ukrainian-native target-form review remain outstanding; linguistic accuracy is `NOT_MEASURED`.
- Global TIMIT Thai data use remains blocked pending written LDC authorization.
- LOTUSDIS audio remains partial until immutable audio bytes, independently computed hashes, and interval/overlap provenance are inspected.
- FastThaiG2P bundled-data rights and a verified Vercel/Python-host preview remain blockers for production deployment.
- Hands-on keyboard, screen-reader, zoom/reflow and mobile accessibility review remains outstanding; automated checks are not a WCAG conformance claim.
- CCOST source/tier questions require curator clarification and lawful archive inspection.

## Task ledger

| Work item | Status | Evidence / acceptance |
|---|---|---|
| Inspect latest default branch, tree, instructions, package metadata and CI | DONE_VERIFIED | Live GitHub tree and source files at `56fba86...`; current CI run succeeded |
| Reconcile live branches and open PRs | DONE_VERIFIED | Live branch endpoint returned `main` and this audit branch; PR search returned only open PR #210 |
| Review documentation and code/data/test ownership | DONE_VERIFIED | `AGENTS.md`, docs index, architecture, scripts guide, CI and recursive tree inspected |
| Preserve existing architecture and documentation system | DONE_VERIFIED | Existing ownership map is internally coherent; no competing plan created |
| Correct README FastThaiG2P deployment status | PARTIAL until PR #210 merges | Wording is updated on this branch; `main` remains unchanged until merge |
| Record current audit and exact GitHub state in canonical registers | PARTIAL until follow-up exact-head CI and PR merge | This report, matrix, audit register and handoff update; inspected predecessor head passed run 41919548444 |
| Independent Thai/Ukrainian adjudication | BLOCKED | Qualified independent reviewers and completed blinded adjudication packets |
| Global TIMIT Thai authorization | BLOCKED | Written LDC authorization defining allowed access/use/redistribution |
| LOTUSDIS audio evidence | PARTIAL | Immutable audio bytes, SHA-256, source revision and clean interval/overlap review |
| FastThaiG2P production deployment | BLOCKED | Source-level rights review and verified Python-host preview |
| Manual accessibility review | PARTIAL | Recorded keyboard, screen-reader, zoom/reflow and mobile results |

## Reference projects: practices adopted, not copied

- **Unlazy** ([README](https://github.com/Leonxlnx/unlazy), [gate contract](https://github.com/Leonxlnx/unlazy/blob/main/references/gates.md)): requires observable acceptance outcomes, runnable `CHECK:`/`EXPECT:` gates, explicit manual handoffs, evidence freshness and parent re-verification. This repository already has an acceptance matrix, a chronological handoff and executable CI, but it does **not** implement Unlazy's gate parser, approval store or evidence-fingerprint protocol. Do not add that separate shell-execution framework merely for stylistic similarity; the existing GitHub Actions jobs remain the executable engineering gates.
- **Superpowers** ([README](https://github.com/obra/superpowers), [TDD skill](https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md), [branch-finishing skill](https://github.com/obra/superpowers/blob/main/skills/finishing-a-development-branch/SKILL.md)): emphasizes requirement discovery, test-first changes, independent review and explicit branch completion. The repository's `AGENTS.md`, regression tests and CI already encode the relevant parts; importing the entire multi-harness skill suite would duplicate the local workflow.
- **Matt Pocock's skills** ([README](https://github.com/mattpocock/skills), [code review](https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md), [codebase design](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md)): favors explicit interfaces/seams, dependency injection and testing through the same interface used by callers. The Python/browser split and typed IPA adapter are real boundaries with parity tests; do not split modules or add abstractions without a second implementation or a demonstrated variation.
- **Ponytail** ([README](https://github.com/DietrichGebert/ponytail), [whole-repo audit](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail-audit/SKILL.md), [change review](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail-review/SKILL.md)): asks for concrete reproducible findings, end-to-end data-flow tracing, explicit expected load, risk-based tests and deletion only when unused code is proven. The repository's static dependency/test-overlap audit is useful inventory, not a runtime call graph or proof that similar tests are redundant.

No upstream skill files, runtime dependencies, hooks or workflows were copied into the project. The review adopted only the practices that fit the existing repository contracts; the upstream repositories are living references, not project dependencies.

## Research cross-check

The connected Undermind workspace contains a completed Thai phonology audit and a completed Thai lexical-segmentation/pronunciation review. The latter includes full-text reads of Boo20, Cho20, Lim21 and Yam22 and reaches the same evidence constraints recorded here: orthographic syllables are a boundary scaffold, not lexical word gold; segmentation conventions and domain shift matter; dictionary/model-derived labels are not independent expert IPA; and Thai pronunciation gold needs trained independent phoneticians and explicit adjudication. The repository's maintained synthesis is [Thai G2P evaluation literature](research/thai-g2p-evaluation-literature-2026-11-03.md); the workspace note is [available in Undermind](https://app.undermind.ai/projects/49bbd978-a5a9-4cac-a7bb-a72848f50e10?path=%2FThai%20lexical%20segmentation%20and%20pronunciation%20evidence%20%E2%80%94%202026-11-03.md). This is literature support for the validation plan, not new project accuracy evidence.

## Documentation and structure changes made in this audit

- Added this dated audit report and linked it from the canonical documentation index.
- Updated the README to distinguish merged FastThaiG2P integration from its still-gated production deployment.
- Added a current exact-main checkpoint to the handoff, matrix and audit register, while retaining prior dated entries as history.
- Did not rename/move source files, benchmark data, scripts, schemas or generated artifacts: the existing layout has clear ownership and automated checks. Moving them now would add risk without demonstrated benefit.
- No linguistic labels, IPA values, corpus rows, license permissions, accuracy claims or benchmark results were invented or changed.

## Verification and stop condition

The audited base commit `56fba86b4b8be2fe4e67284355e9928108527387` passed Full CI run [41918227400](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41918227400), Pages workflow [41918227410](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41918227410), Web Static [41918227382](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41918227382), and Site API [41918227381](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41918227381). No local test run is claimed.

The inspected audit-branch head passed its exact-head Full CI. Any subsequent documentation commit requires a fresh exact-head run before merge; no merge is claimed here. Readiness remains **engineering-verified research prototype**, not release-ready for linguistic accuracy, production deployment or full WCAG 2.2 AA claims.


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
| CCOST TextGrid and tier mapping | BLOCKED | Obtain lawful access to the actual archive/TextGrid files, inspect real tiers and X-SAMPA/IPA conventions, map tiers explicitly, and document curator clarification. CC BY-NC-SA 4.0 applies; do not treat the data as unrestricted or redistribute outside its terms. |

### Evidence policy

Do not mark any gate DONE_VERIFIED because a registry entry, schema, blank reviewer packet, model output, source annotation, static check or documentation paragraph exists. Keep CCOST under CC BY-NC-SA 4.0 restrictions; keep Global TIMIT Thai unused pending written LDC permission. Keep LOTUSDIS PARTIAL until actual WAV bytes and per-file hashes/interval evidence are verified. Keep FastThaiG2P production data and preview gates separate. Do not create or report independent IPA gold rows until the blinded expert adjudication has actually happened.


## Research and corpus-rights reconciliation — 2026-11-05

### CCOST: tier schema documented; archive inspection remains open

The LREC 2026 paper now provides an inspectable published tier map: `ORT` = orthographic word; `KAN` = canonical word pronunciation; `KAS` = canonical syllabified pronunciation; `MAU` = phonetic segment; `MAS` = phonemic syllable; `TRN` = orthographic utterance transcript. Phonemic and phonetic representations use X-SAMPA; tone suffixes `_1`–`_5` map to Mid, Low, Falling, High and Rising respectively. The paper describes MAUS processing and subsequent manual correction by trained native Thai research assistants, including phonetic variants on MAU and removal of misread lexical items from MAS. See [Pittayaporn et al., LREC 2026, §3.3–3.4](https://aclanthology.org/2026.lrec-1.247.pdf) and [the official Zenodo record](https://zenodo.org/records/17366698).

**Status: PARTIAL.** This closes the *published tier-map discovery* subtask, not the actual archive inspection. The Zenodo record identifies a 6.2 GB `C-COST.zip` containing WAV and TextGrid files and a separate `CCOST_manual.pdf`; the manual and archive could not be fetched/inspected in this session. Therefore status is **PARTIAL**: published tier names/conventions are known, but actual TextGrid files, real tier instances, interval alignment, and any discrepancies between archive and paper remain unverified. The dataset is CC BY-NC-SA 4.0; no commercial reuse or redistribution beyond those terms is implied. The paper explicitly reports that no formal inter-annotator agreement measures were collected (§8), so CCOST annotations must not be described as a measured-IAA gold set.

### FastThaiG2P: source-level rights remain unresolved

The upstream [FastThaiG2P repository](https://github.com/awslabs/FastThaiG2P) declares Apache-2.0 for its project code. Its [data README](https://github.com/awslabs/FastThaiG2P/blob/main/data/README.md) distinguishes the runtime dictionary and IPA map from source files: the map combines manual overrides, approximately 13k Wiktionary-derived entries and approximately 49k generated entries; the upstream README attributes the latter to Claude Opus 4.6. It also identifies vendored `tltk` fallback assets. An Apache-2.0 code license does **not** establish redistribution rights for every upstream dictionary entry, generated output, source dump, or vendored data asset. Keep the project's FastThaiG2P bundled-data gate **BLOCKED** until each asset's provenance, upstream license/terms, attribution and redistribution rights are reviewed independently. Keep the Python-host preview as a separate **BLOCKED** deployment gate.

### Primary references

- Pittayaporn, Pittayawat, Cathryn Yang, Sujinat Jitwiriyanont & James Kirby (2026). *The Chulalongkorn Corpus of Spoken Thai (CCOST).* LREC 2026, pp. 3154–3160. [PDF](https://aclanthology.org/2026.lrec-1.247.pdf), [Zenodo dataset record](https://zenodo.org/records/17366698).
- [FastThaiG2P upstream README](https://github.com/awslabs/FastThaiG2P), [data README](https://github.com/awslabs/FastThaiG2P/blob/main/data/README.md), [Apache-2.0 code license](https://github.com/awslabs/FastThaiG2P/blob/main/LICENSE).


## Text-only corpus and FastThaiG2P rights review — 2026-11-05

The user clarified that the project needs only orthographic text and phonetic text labels, not audio. The dedicated research note is [Text-only Thai corpus and FastThaiG2P rights review](research/corpus-text-only-fastthaig2p-2026-11-05.md).

- **Global TIMIT Thai (LDC2022S13):** the catalog exposes Word, Phones, Tones and TextGrid TXT samples. The standard non-member agreement permits non-commercial research and limited excerpts in reports, but not bulk public redistribution. Access is feasible after signing the agreement and checking fees; public release of full extracted labels needs separate LDC permission. Do not acquire audio.
- **LOTUSDIS:** public text rows are available under CC BY-SA 4.0 and include utterance text, speaker, microphone and duration. The paper describes utterance-level orthographic transcripts, speaker labels and overlap tags, not phone/IPA tiers. Keep it optional for conversational vocabulary and orthographic robustness; it is not phonetic gold. Audio hashes/intervals are DEFERRED / OUT OF SCOPE.
- **CCOST:** published TextGrid tiers include MAU phonetic segments and MAS phonemic syllables, plus ORT/KAN/KAS/TRN; labels use X-SAMPA and five tone suffixes. CC BY-NC-SA 4.0 appears compatible with the stated non-commercial public-interest research if attribution and ShareAlike are followed. Prefer requesting TextGrid-only files and manual; do not download WAV. No formal IAA was collected, so independent review of a subset is still required.
- **FastThaiG2P:** Apache-2.0 code can be reused with NOTICE. Its Wiktionary-derived IPA subset has a CC BY-SA 3.0 reuse path. Do not blindly copy the merged 62k dictionary: it combines that subset with ~49k LLM-generated entries and manual overrides. TLTK fallback code has a BSD-3 notice, but vendored TLTK data files need file-level license clarification because upstream exposes conflicting license indicators. The data README's 34-row/17-row gold test files return 404 on current upstream main; accessible tests are smoke tests, not a phonetic benchmark. Keep generated IPA provisional.
- **No runtime corpus rows or phonetic labels were added. No audio was downloaded.** The full source-by-source analysis and links are in the linked research note.
