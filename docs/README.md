# Repository guide

This page is the navigation layer for the repository. It distinguishes the maintained product contract from research evidence and the chronological execution record.

## Latest repository audit

Current default branch: main, commit `bbbfeff944304e1010e3d0daed6fcc6710a27ba6` (2026-11-06). Latest main-push CI run [#42247363425](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42247363425) completed successfully. PRs #211–#214 and #216–#220 are merged; PR #215 was closed as superseded by #216. There are no open PRs. The practical transcription rules, browser-native FastThaiG2P/TLTK OOV path, Ukrainian-first interface, /j/ adaptation and Pages smoke repair are integrated. The Pages deployment and live smoke passed on functional commit `e2cfba14815221d6f8cc05db5f1874dd43984ac9` (run #42245944508); the latest docs-only main commit has CI success. The `docs/repository-audit-2026-11-04` branch is 503 commits ahead and 38 behind current main and is intentionally preserved, not merged wholesale. Other non-main refs are historical source refs for already merged work; continue active work from one dedicated branch off main.

## Public beta

The public website is the [GitHub Pages beta](https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/). The service exposes the Thai → Ukrainian practical system on a dedicated [Практична система](../web/transcription.html) page, alongside the live [browser service](../web/index.html) and [method/runtime explanation](../web/system.html). Mainline uses a hybrid native-first FastThaiG2P path: dictionary hits use a same-origin JavaScript Worker; dictionary misses use the browser-native TLTK OOV parser and lazy same-origin data pack; Pyodide remains a fail-closed compatibility fallback only when the native path cannot complete. Exact typed-service JSON parity passed on 64 OOV fixtures in module and Worker tests. The main Pages deployment and live smoke passed on functional commit e2cfba14815221d6f8cc05db5f1874dd43984ac9 (run #42245944508). The latest docs-only main commit bbbfeff944304e1010e3d0daed6fcc6710a27ba6 has CI run #42247363425 SUCCESS. Vercel and remote API hosting are out of scope. The public UI presents a provisional Ukrainian practical adaptation of external IPA; it does not claim expert linguistic validation.

The current browser design contract is in [Website UX and visual system](ui-ux-redesign.md). The deployed site has three distinct entry points: the [interactive browser service](../web/index.html), the [practical Thai–Ukrainian transcription system](../web/transcription.html), and the [runtime/method explanation](../web/system.html). Runtime architecture and interaction boundaries are documented in [Web service architecture](web-service-architecture.md) and [Web service requirements](web-service-requirements.md). Runtime licenses and data attribution are listed on the public [third-party notices page](../web/third-party-notices.html).

## Start here

1. [Project overview and user-facing capabilities](../README.md)
2. [Public browser service](../web/index.html)
3. [Thai–Ukrainian practical transcription system](../web/transcription.html)
4. [Browser runtime explanation](../web/system.html)
5. [Architecture and data flow](architecture.md)
6. [Validation and evidence status](validation-matrix.md)
7. [Current audit findings](final-audit.md)
8. [Current continuation checkpoint and historical handoff](MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md)

## Canonical documentation by concern

| Concern | Canonical source | What belongs there |
|---|---|---|
| System boundaries | [Architecture](architecture.md) | Stable layers, invariants and data flow |
| Thai analysis | [Thai orthography](thai-orthography.md), [syllable structure](thai-syllable-structure.md), [phonological rules](phonological-rules.md), [contextual phonology](contextual-phonology.md) | Linguistic model and rule scope |
| IPA contract | [IPA](ipa.md), [benchmarking and external IPA](benchmarking-and-external-ipa.md) | Typed IPA, provenance, uncertainty and comparator limits |
| Ukrainian output | [Practical transcription overview](thai-ukrainian-practical-transcription.md), [technical specification](practical-transcription.md), [Target layer](ukrainian-target-layer.md), [transcription methodology](ukrainian-transcription-methodology.md), [correspondence matrices](ukrainian-correspondence-matrices.md) | User-facing Thai → Ukrainian system, IPA adaptation, practical orthography and evidence status |
| RTGS | [RTGS reference/parity research](research/rtgs-parity-corpus.json), [external renderer registry](external-ipa-renderers.md) | Separate romanization route; never an IPA substitute |
| Data and licenses | [Evidence registry](evidence.md), [corpus validation](corpus-validation.md), [CCOST text-only adapter](ccost-text-only-adapter.md), [FastThaiG2P data provenance](fastthaig2p-data-provenance.md), `data/corpus_sources.csv`, [third-party corpus notices](../data/THIRD-PARTY-CORPUS-NOTICES.md), [runtime third-party notices](../web/third-party-notices.html) | Provenance, permitted use and evidence grades |
| Interfaces | [CLI and batch API](cli-batch-api.md), [web architecture](web-service-architecture.md), [web requirements](web-service-requirements.md), [FastThaiG2P Pyodide reference port](fastthaig2p-pyodide-port.md), [FastThaiG2P native JavaScript/TypeScript port](fastthaig2p-javascript-port.md), [FastThaiG2P site integration](fastthaig2p-site-integration.md) | Supported interfaces, single website G2P engine and deployment boundaries |
| UI/UX | [Website UX and visual system](ui-ux-redesign.md), [Ukrainian-first UX](ukrainian-first-ux.md) | User journey, responsive rules, Ukrainian language contract, error taxonomy and acceptance criteria |
| Research protocol and literature | [Research protocol](research-protocol.md), [independent adjudication](independent-adjudication-protocol.md), [Thai G2P evaluation literature](research/thai-g2p-evaluation-literature-2026-11-03.md), [text-only corpus and FastThaiG2P rights review](research/corpus-text-only-fastthaig2p-2026-11-05.md) | Reproducible evaluation, corpus text-only rights, published-score caveats and human-review gates |

## Code and data layout

- `src/thai_ukrainian/` — Python reference implementation and public API; adapters/ccost.py and adapters/xsampa.py ingest CCOST TextGrid text only.
- scripts/inspect_ccost_textgrid.py — local TextGrid tier inventory and X-SAMPA conversion report; no audio access.
- scripts/export_textgrid_text.py — explicit orthographic interval export to provenance-rich JSONL; TextGrid members only, no audio access or gold promotion.
- `web/src/` — browser implementation; native JavaScript Workers handle dictionary and TLTK OOV paths first, with `fastthaig2p-worker.js` and self-hosted Pyodide retained as a fail-closed compatibility fallback.
- `web/licenses/` and `web/third-party-notices.html` — runtime license and data-attribution notices for the published Pages bundle.
- `data/thai/` — runtime Thai registries and their provenance/license notices.
- `data/ua_target_vectors.csv` — Ukrainian target feature inventory.
- `data/benchmark/` — benchmark inputs, blind Thai and Ukrainian reviewer packets, adjudication-gold registries and diagnostic run records; evidence grades remain explicit.
- `schemas/` — machine-readable contracts.
- [`scripts/README.md`](../scripts/README.md) — script inventory, ownership, input/output contracts and evidence boundaries.
- `tests/` and `web/tests/` — Python and browser regression suites.
- `.github/workflows/` — CI, static web validation, Pages deployment and opt-in external evaluations.

## Document lifecycle and source of truth

- `README.md` is the public product overview, not the task ledger.
- `architecture.md` and `web-service-architecture.md` describe stable architecture; update them when an actual boundary changes.
- `ui-ux-redesign.md` is the current UI intent and acceptance reference.
- `validation-matrix.md` is the acceptance/task ledger. Each task must have a state and evidence or a concrete blocker.
- `final-audit.md` records audit findings and their evidence.
- `MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md` is a chronological continuation log. Its historical entries are not necessarily current; use its newest dated entry and reconcile it with the matrix and live GitHub state.
- `final-audit.json` is the manually maintained structured companion to `final-audit.md`; update both in the same audit batch. No in-repository generator writes this file.
- `generated-audit.json` and `source-final-manifest.json` are generated by `scripts/generate_derived.py`; `syllable-space.json` is generated by `scripts/generate_syllable_space.py`; the tracked `data/derived/` correspondence tables and master JSON are generated by `scripts/generate_master_table.py`. Do not hand-edit these outputs; update their owning sources and run the generator.
- `docs/archive/` is for superseded design snapshots that remain useful as history. Do not move active evidence or delete historical records merely to reduce file size.

## Change discipline

1. Find the owning source, generator, schema and tests before editing a derived artifact.
2. Keep phonetic IPA-first output and RTGS romanization-based output distinct.
3. Treat source-attested and source-annotated data as such; do not relabel them expert gold.
4. For behavior changes, add a regression test and verify Python/browser parity.
5. Update the matrix and audit only with evidence from the exact commit being described.
6. Do not claim linguistic accuracy or accessibility conformance without the independent review specified by the relevant protocol.

## Repository verification snapshot — 2026-11-01

Current main snapshot: `cc398254c178171f74397aed556766e87356ab84`. Last recorded full main CI [41326865977](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41326865977) and Pages [41326865964](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41326865964) passed on the preceding main code checkpoint `1431c565ff5c160da4944942d687bc30b2f8d0b2`; those runs are not represented as testing the later documentation-only main commit. Research branch `research/independent-adjudication-gates-20261101` continues in PR #182; consult the live PR head for its current ahead count and exact-head checks. PR #181 was closed as superseded after its engine/test/CI changes were ported into combined PR #182; its source branch remains intact. This engineering verification is not a claim of independent linguistic gold or WCAG conformance.


Research continuation closeout: PR [#182](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/182) is open from `research/independent-adjudication-gates-20261101`; PR #181 was closed as superseded after its engine/test/CI changes were ported. The #181 source branch remains intact. Exact code-head CI [41337529189](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41337529189) and Web Static [41337815975](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41337815975) passed. This is engineering verification, not independent linguistic accuracy.


## 2026-11-02 — follow-up validator review

PR #182 remains open on `research/independent-adjudication-gates-20261101`. A narrow-IPA-on-abstention guard was added after a test-first review: the new regression test is in commit `2852b47`, and the one-line implementation is in `e22c686`. Web Static passed on the implementation head; full CI and VISTEC were still running at the time of this snapshot. The test-only CI run was cancelled before the Python suite, so a red result is not claimed. See the newest continuation checkpoint and validation matrix for exact evidence and remaining blockers.

- `scripts/build_ccost_review_worklist.py` — build the CI-published, blind CCOST label-review TSV and provenance manifest from TextGrid members only; preserves source labels and context and does not propose corrections.

- [FastThaiG2P license review](fastthaig2p-license-review-2026-11-05.md) — component-level upstream license evidence, including TLTK 1.9.1 package scope.
- [FastThaiG2P JavaScript port](fastthaig2p-javascript-port.md) — native-first browser runtime, parity gates and remaining OOV work.
