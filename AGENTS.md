# Agent workflow for this repository

This file is the repository-specific entry point for coding agents that read
`AGENTS.md`. It adapts three public engineering skill sets to this project's
actual constraints. It does not vendor or claim to install those tools.

## Canonical project context

- `docs/README.md` — documentation navigation, code/data layout, source-of-truth rules and document lifecycle.

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
  - [Codebase design](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md)
  - [Improve codebase architecture](https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md)
  - [Code review](https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md)
- **Ponytail** — audit correctness, security, real load, missing tests, speed,
  and unnecessary code; prefer deletion and the smallest complete change:
  - [Repository audit](https://github.com/DietrichGebert/ponytail/blob/main/.openclaw/skills/ponytail-audit/SKILL.md)
  - [Diff review](https://github.com/DietrichGebert/ponytail/blob/main/.openclaw/skills/ponytail-review/SKILL.md)
  - [Debt ledger](https://github.com/DietrichGebert/ponytail/blob/main/.openclaw/skills/ponytail-debt/SKILL.md)

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
