# Repository guide

This page is the navigation layer for the repository. It distinguishes the maintained product contract from research evidence and the chronological execution record.

## Latest repository audit

The latest structural and UX review is repository audit — 2026-11-05 (repository-audit-2026-11-04.md). It reconciles current main, the merged TextGrid work, the live GitHub Pages beta, and the design/recomposition branch. Older entries inside dated audit files and the handoff remain chronological evidence, not current state.

## Public beta

The public website is the GitHub Pages beta: https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/. It runs the pinned FastThaiG2P engine locally in a same-origin Web Worker through self-hosted Pyodide. Vercel and remote API hosting are out of scope. The public UI presents a provisional Ukrainian practical adaptation of unclassified external IPA; it does not claim expert linguistic validation.

The current browser design contract is in ui-ux-redesign.md. Runtime architecture and interaction boundaries are documented in web-service-architecture.md and web-service-requirements.md. Runtime licenses and data attribution are on the public third-party notices page.

## Start here

1. Project overview and user-facing capabilities — ../README.md
2. Architecture and data flow — architecture.md
3. Web runtime architecture — web-service-architecture.md
4. Website UX and visual system — ui-ux-redesign.md
5. Validation and evidence status — validation-matrix.md
6. Current audit findings — final-audit.md
7. Current continuation checkpoint and historical handoff — MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md

## Canonical documentation by concern

| Concern | Canonical source | What belongs there |
|---|---|---|
| System boundaries | architecture.md | Stable layers, invariants and data flow |
| Thai analysis | thai-orthography.md, thai-syllable-structure.md, phonological-rules.md, contextual-phonology.md | Linguistic model and rule scope |
| IPA contract | ipa.md, benchmarking-and-external-ipa.md | Typed IPA, provenance, uncertainty and comparator limits |
| Ukrainian output | ukrainian-target-layer.md, ukrainian-transcription-methodology.md, ukrainian-correspondence-matrices.md | IPA adaptation and practical orthography |
| RTGS | research/rtgs-parity-corpus.json, external-ipa-renderers.md | Separate research route; never an IPA substitute |
| Data and licenses | evidence.md, corpus-validation.md, ccost-text-only-adapter.md, fastthaig2p-data-provenance.md, data/corpus_sources.csv, corpus notices | Provenance, permitted use and evidence grades |
| Interfaces | cli-batch-api.md, web-service-architecture.md, web-service-requirements.md, fastthaig2p-pyodide-port.md, fastthaig2p-site-integration.md | Supported interfaces, single website G2P engine and deployment boundaries |
| UI/UX | ui-ux-redesign.md | User journey, visual language, responsive rules and UI acceptance criteria |
| Research protocol | research-protocol.md, independent-adjudication-protocol.md, text-only corpus and FastThaiG2P rights review | Reproducible evaluation, source scope and human-review gates |

## Code and data layout

- src/thai_ukrainian/ — Python reference implementation and public API; adapters ingest CCOST TextGrid text only.
- web/index.html — public GitHub Pages entry point and static service shell.
- web/src/app.js — browser UI, local worker transport, rendering, status and copy interactions.
- web/src/fastthaig2p-worker.js — Pyodide bootstrap, same-origin runtime integrity and FastThaiG2P invocation.
- web/src/ — browser research/reference modules; the legacy JS engine is not a site fallback.
- web/licenses/ and web/third-party-notices.html — runtime license and data-attribution notices.
- data/ — source registries, canonical inputs and provenance.
- schemas/ — machine-readable contracts.
- scripts/README.md — script inventory, ownership, inputs/outputs and evidence boundaries.
- tests/ and web/tests/ — Python and browser regression suites.
- .github/workflows/ — CI, static web validation, Pyodide compatibility and Pages deployment.

## Document lifecycle and source of truth

- README.md is the public product/research overview, not the task ledger.
- architecture.md and web-service-architecture.md describe actual stable boundaries; update them when an implementation boundary changes.
- ui-ux-redesign.md is the current UI intent and acceptance reference.
- validation-matrix.md is the acceptance/task ledger; each task has a state and evidence or a concrete blocker.
- final-audit.md records current audit findings; final-audit.json is its structured companion.
- MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md is a chronological continuation log. Its newest dated checkpoint is authoritative over older entries.
- Generated manifests, derived tables and fixtures must be changed through their owning source and generator, not hand-edited.
- docs/archive/ preserves superseded designs and historical evidence.

## Change discipline

1. Trace the actual code path, caller, test, data contract and owning document before editing.
2. Keep IPA-first phonetic output and RTGS research output distinct.
3. Treat source-attested/source-annotated data as such; never relabel it expert gold.
4. For UI changes, preserve the worker protocol, privacy, provenance and fail-closed contracts; add regression tests for user-visible behavior.
5. Update the matrix and audit only with evidence from the exact commit being described.
6. Do not claim linguistic accuracy or accessibility conformance without the required independent review.