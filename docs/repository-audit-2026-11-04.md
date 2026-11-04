# Repository audit and documentation closeout — 2026-11-04

## Scope and method

Audited the live default branch, recursive repository tree, repository instructions, package metadata, CI workflow, code/data/schema/test layout, documentation ownership, current branch and pull-request state, recent commits, and the current Actions runs. Compared the repository's agent-workflow conventions with the four requested public references: [Unlazy](https://github.com/Leonxlnx/unlazy), [Superpowers](https://github.com/obra/superpowers), [Matt Pocock's skills](https://github.com/mattpocock/skills), and [Ponytail](https://github.com/DietrichGebert/ponytail).

This is a source-tree and GitHub-hosted audit. No local checkout or local test execution was available through the connected GitHub interface. CI evidence below is therefore explicitly GitHub Actions evidence.

## Executive result

The repository already has a mature, unusually explicit structure for a research prototype. It has a root agent contract, a documentation index, architecture ownership map, script inventory, a canonical validation matrix, an audit register, a chronological handoff, machine-readable schemas, provenance/license records, generated-artifact ownership, Python and browser test suites, and static dependency/test-overlap auditing. A wholesale reorganization would create churn and duplicate existing governance. The correct action is to preserve this structure and repair stale status/documentation, not invent a second docs system.

The highest-priority documentation defect was stale repository state: older top sections in the matrix/audit/handoff still described a 2026-11-03 branch/PR checkpoint even though main had advanced through the 2026-11-04 integration work. The README also described FastThaiG2P site integration as still sitting in Draft PR #193. That is no longer accurate: the implementation is integrated, while production deployment remains separately gated by external data-rights and verified-preview requirements.

## Current GitHub state

- Default branch: `main`.
- Audited base commit: `56fba86b4b8be2fe4e67284355e9928108527387`.
- Live branch inventory: two branches — `main` and `docs/repository-audit-2026-11-04`. The latter is the dedicated documentation/audit branch for this work; no unrelated branch was deleted.
- Open pull requests: one — [PR #210](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/210), this audit branch, 7 commits ahead and 0 behind `main` at the inspected checkpoint. The PR remains open; no merge is claimed.
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
