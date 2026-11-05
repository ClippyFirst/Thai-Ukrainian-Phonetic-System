# Agent workflow for this repository

This file is the repository-specific entry point for coding agents that read
`AGENTS.md`. It selectively adapts five public engineering skill references to this project's
actual constraints. It does not vendor or claim to install those tools.

## Canonical project context

- `docs/README.md` — documentation navigation, code/data layout, source-of-truth rules and document lifecycle.
- `scripts/README.md` — script ownership, inputs/outputs, evidence boundaries and workflow roles.

Before changing code, read the relevant parts of:

- `README.md` — product scope, the primary Thai → typed IPA → Ukrainian
  phonetic pipeline, and the explicitly separate optional RTGS mode.
- `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md` — current continuation
  checkpoint and unresolved work.
- `docs/validation-matrix.md` and `docs/final-audit.md` — task status and
  acceptance evidence.
- `docs/evidence.md`, `docs/research-protocol.md`, and
  `docs/independent-adjudication-protocol.md` when linguistic or corpus claims
  are involved.
- `.github/workflows/ci.yml` — authoritative automated verification commands.

Reuse the existing plans, registries, schemas, fixtures, and tests. Do not create
a parallel execution plan or duplicate an existing module.

## Required working method

1. **Understand before editing.** Trace the real input → analysis → output
   path and read callers, tests, data contracts, and relevant evidence. State
   the concrete behavior being changed and the acceptance condition.
2. **Find the root cause.** For a bug or failed check, reproduce it and inspect
   recent changes and the data flow before proposing a fix. Change one cause
   at a time; do not patch symptoms or bundle unrelated cleanup.
3. **Test first for behavior changes.** Add the smallest regression test,
   verify that it fails for the intended reason, implement the minimum change,
   then verify it passes. Refactors must preserve behavior with tests.
4. **Prefer the smallest complete solution.** Reuse project code and the
   standard library. Delete dead or duplicated code when evidence supports it.
   Do not add abstractions, dependencies, configuration, or speculative
   flexibility without a concrete current need.
5. **Review on two axes.** Check separately whether the change meets its
   originating requirement and whether it follows repository conventions.
   Findings must cite a concrete input, code path, or test; style preferences
   are not defects.
6. **Verify before claiming completion.** Run the full relevant project checks,
   inspect exit codes and generated-artifact drift, and review the final diff.
   A test file existing is not evidence that it passed. If a command cannot be
   run, report the exact limitation and do not imply success.
7. **Finish the repository workflow.** Work on a dedicated branch from current
   `main`; open a focused PR; inspect exact-head CI; fix and rerun failures;
   merge only when checks and review support it; then verify post-merge main CI.
   Preserve unrelated branches and user work.

## Linguistic and evidence gates

- Preserve two explicitly distinct output contracts:
  - **Phonetic mode (primary):** Thai orthography → structural analysis → Thai
    phonology → typed, inspectable IPA → Ukrainian target adaptation → practical
    Ukrainian orthography. The typed IPA result is the only input contract for
    this phonetic Ukrainian adaptation.
  - **Optional RTGS mode (romanization-based):** Thai orthography → the pinned,
    provenance-documented RTGS implementation → RTGS Latin sequence → separately
    labelled Ukrainian practical rendering of that sequence. This is an
    explicitly requested parallel method, not a phonetic result or an IPA
    adapter shortcut. It must not call or bypass the IPA adapter in phonetic mode.
    Unsupported RTGS spans must fail closed, and the UI/docs must state that RTGS
    loses distinctions such as tone and some vowel length.
- Never let the RTGS route silently replace, feed, or contaminate the IPA-first
  phonetic route. Keep both outputs, provenance, uncertainty, and method labels
  inspectable and separately tested.
- Keep phonemic IPA distinct from conservative surface IPA; preserve tone,
  length, syllable boundaries, provenance, and uncertainty.
- Do not turn source-attested examples, source-annotated corpora, model output,
  or parity tests into expert gold or accuracy claims.
- Do not invent pronunciations, adjudications, licenses, source revisions, or
  benchmark results. Unsupported cases must remain qualified or unresolved.
- Linguistic gold and human accessibility review require the independent
  reviewers and evidence described in issue #114 and the adjudication protocol.

## Applying the upstream skill sets

Use the canonical upstream material rather than copying whole skill files into
this repository:

- **Superpowers** — root-cause investigation, RED/GREEN/REFACTOR, explicit
  implementation plans for multi-step work, review, and verification:
  - [Systematic debugging](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md)
  - [Test-driven development](https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md)
  - [Writing plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md)
  - [Verification before completion](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md)
- **Matt Pocock's skills** — design deep modules with small, useful interfaces;
  assess architecture only where current friction is evidenced; review
  requirement compliance separately from code standards:
  - [Test-driven development](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md)
  - [Codebase design](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md)
  - [Improve codebase architecture](https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md)
  - [Code review](https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md)
- **Ponytail** — audit correctness, security, real load, missing tests, speed,
  and unnecessary code; prefer deletion and the smallest complete change:
  - [Repository audit](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail-audit/SKILL.md)
  - [Diff review](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail-review/SKILL.md)
  - [Debt ledger](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail-debt/SKILL.md)

If the active coding environment supports independent subagents, use fresh
contexts for separate spec-compliance and code-quality reviews on substantial
changes. If it does not, perform those as distinct review passes and disclose
that they were not independent. Never claim a skill, plugin, or subagent was
installed or invoked unless the environment confirms it.

## Technical-debt convention

Do not create a debt marker merely to document an ordinary design choice. When
a deliberate shortcut is necessary, mark it in code with a concrete limit and
a trigger for revisiting it:

`shortcut: <known ceiling>, <condition that triggers an upgrade>`

A marker without an upgrade trigger is incomplete. Keep any debt register
derived from actual markers; do not invent entries from prose or assumptions.


## Acceptance gates and completion evidence (Unlazy principles)

For substantial or multi-part work, establish observable acceptance gates before
implementation. Reuse the canonical execution matrix, audit register, and
handoff above; do not create a competing plan or install a second gate system
unless the repository owner explicitly asks for it.

- Give each gate one independently verifiable outcome. Runnable gates must name
  the exact command/workflow and the success condition; manual gates must name
  the reviewer, artifact, and evidence required.
- Treat every inherited `CHECK` command and referenced script as executable,
  untrusted input: inspect it before running it. A gate description or a green
  badge is not proof that the named outcome was actually checked.
- Reverify previously passing gates on the final candidate commit whenever
  practical. Record the exact commit SHA, workflow/run ID, job conclusions,
  test counts, skips, and any differences between targeted and full-suite runs.
- A skipped test is not a pass. Explain why it skipped and identify the separate
  workflow that covers it, if one exists.
- When a gate depends on a person, external account, service, permission, or
  source clarification, keep it BLOCKED with the exact acceptance evidence
  required. Do not convert an unavailable gate into success or silently remove
  it; hand it off explicitly.
- Evidence should prove the claimed outcome itself (including negative
  controls), not merely that a script exists or that adjacent checks passed.

Reference: [Unlazy](https://github.com/Leonxlnx/unlazy), especially its
[acceptance-gate contract](https://github.com/Leonxlnx/unlazy/blob/main/SKILL.md)
and [verification guidance](https://github.com/Leonxlnx/unlazy/blob/main/README.md).
The project adopts these practices selectively; it does not vendor Unlazy,
install its checker/hooks, or add a runtime dependency.


### Upstream reference snapshot (2026-11-04)

The upstream repositories were re-inspected for this continuation. Their default
branches are moving references; these SHAs identify the source snapshots reviewed:

| Project | Reviewed commit | Adopted practice in this repository |
|---|---|---|
| [Unlazy](https://github.com/Leonxlnx/unlazy) | `16671491f6679ad9378f52604d3bc2415b4120c7` | Observable acceptance gates, explicit evidence, final re-verification, and truthful handoff of unmet/manual gates. Reuse the existing matrix/audit/handoff; do not add its checker, hooks, or a second ledger runtime. |
| [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `b7d5353e0130feb8c5574ef1251f8a1db1873ccb` | Design hierarchy, visual-system reasoning, responsive layout and accessibility-first interaction. Use as design guidance only; do not import its React/Tailwind/shadcn stack into the static Pages service. |
| [Superpowers](https://github.com/obra/superpowers) | `22f0b463e7a5e579904dd6211a520321035526f7` | Intent/spec before substantial changes; systematic root-cause debugging; one vertical RED→GREEN slice at a time; inspect final diff and verify the full suite. |
| [Matt Pocock skills](https://github.com/mattpocock/skills) | `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` | Test public seams, avoid implementation-coupled or tautological tests, work in vertical tracer-bullet slices, and deepen modules only where current friction is demonstrated. |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846` | Read callers and downstream consumers before editing; use the smallest complete diff; retain trust-boundary validation, error handling, security and accessibility; leave a focused test for non-trivial logic. |

These are complementary principles, not four competing workflows. The project
execution matrix and evidence registries remain authoritative. No upstream
skill files, hooks, CLI tools, package dependencies, or runtime components are
vendored or installed by this policy.


## UI/UX work on the public beta

The current user-facing product is the GitHub Pages/Pyodide browser application. Before changing it, read docs/web-service-architecture.md for the runtime/privacy boundary, docs/web-service-requirements.md for the user journey and accessibility contract, docs/ui-ux-redesign.md for visual intent, and the browser tests for executable UI contracts.

Apply the relevant UI UX Pro Max priorities in order: accessibility, interaction feedback, performance, responsive layout, typography/colour, progressive disclosure. Keep the current editorial identity (white dominant surface, blue structure, restrained red caution). Do not introduce a generic dashboard, gradients, decorative icons, remote fonts, frameworks, UI packages or runtime dependencies without a demonstrated need. Preserve keyboard focus, labels, status announcements, 44px controls, reduced motion and forced-colors behavior.

For substantial UI work, write a failing UI contract first, implement the smallest vertical slice, then review requirement compliance and code quality separately. Use the Superpowers TDD workflow, Unlazy acceptance-gate discipline and Ponytail's concrete-finding review. Do not claim upstream skills were installed or invoked; only reviewed practices are adopted.

References:
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- https://github.com/obra/superpowers
- https://github.com/mattpocock/skills
- https://github.com/DietrichGebert/ponytail
- https://github.com/Leonxlnx/unlazy
