# FastThaiG2P browser/WASM port

Owner decision (2026-11-05): retain FastThaiG2P and run it in the browser. GitHub Pages is the only hosting target. Do not replace the engine with the JavaScript research engine or introduce a separate API host.

## Target architecture

- GitHub Pages serves the UI, module Web Worker, pinned Pyodide runtime, pinned pure-Python wheels, FastThaiG2P data and the existing Python IPA/UA adapters.
- Pyodide runs in a module Web Worker so startup and analysis do not block the UI.
- Keep Python canonical. Do not independently reimplement G2P or Ukrainian adaptation in JavaScript.
- Preserve raw external IPA, word/syllable groups, dictionary/fallback provenance, tone, length, uncertainty and provisional Ukrainian output.
- Preserve fail-closed behavior for incomplete IPA, unsupported segments and misaligned token/word/syllable paths.
- No Vercel, external API, or request carrying user-entered Thai text.

## Feasibility evidence

- Pinned FastThaiG2P declares Python >=3.11 and one G2P runtime dependency, PyThaiNLP >=5.3.4. ONNX/PyTorch dependencies are optional TTS only.
- G2P, normalizer, tokenizer wrapper and vendored TLTK fallback are Python code; fallback describes itself as standard-library-only.
- PyThaiNLP 5.4.0 is the current native dependency. Exact-wheel compatibility under Pyodide must be tested, not assumed.
- Upstream data includes a 62k-word dictionary, IPA lookup data and about 19 MB fallback data.
- Initial spike pins stable Pyodide 0.29.5 (CPython 3.13).
- Added scripts/fastthaig2p_pyodide_parity.py, web/tests/fastthaig2p-pyodide.test.mjs and .github/workflows/pyodide-compat.yml. The workflow builds exact wheels, creates a CPython reference, runs the same adapter in Pyodide and compares four Thai inputs, including the upstream garden-word correction.
- Initial run 42061102029 was queued at first poll; no pass is claimed.

## Redistribution gate

Browser execution is technically plausible; public redistribution of the complete runtime bundle is not yet cleared. The upstream inventory identifies manual overrides, roughly 13k Wiktionary/kaikki-derived entries, roughly 49k generated IPA entries and TLTK fallback files. Existing audit evidence does not establish file-by-file rights and attribution for every runtime asset. Serving these assets from Pages makes them directly downloadable. A software license does not automatically clear bundled data.

Before public Pages distribution: inspect the exact wheel and hashes; map every dictionary/fallback asset to source, version, terms and notices; resolve Wiktionary/kaikki and generated IPA rights; include applicable Pyodide MPL-2.0, PyThaiNLP Apache-2.0, FastThaiG2P and TLTK BSD-3-Clause notices; generate a version/hash/size/license manifest; fail the Pages build if that manifest is missing or hashes differ. Ephemeral CI wheels are not public deployment or license clearance.

## Acceptance ledger

| Area | Criterion | Status |
|---|---|---|
| Runtime | Exact wheels import/run in Pyodide 0.29.5 | PARTIAL — CI pending |
| Parity | CPython/Pyodide JSON matches | TODO |
| IPA/UA | Same typed adapter and IPA-to-Ukrainian function | TODO |
| Browser | Worker integration and responsive UI | TODO |
| Hosting | All runtime assets on Pages; no API host/text upload | TODO |
| Performance | Bundle size and cold/warm timings recorded | TODO |
| Licensing | Per-file redistribution/attribution manifest | BLOCKED |
| Privacy | UI states input is processed locally | TODO |
| Deployment | Exact merged main commit passes Pages live smoke | TODO |

No TTS, audio, acoustic validation, remote API, Vercel, serverless function or engine fallback. No independent IPA gold, accuracy, official Ukrainian standardisation or WCAG certification claim.

Disposition: PARTIAL. Do not call the port complete, change live Pages or publicly redistribute runtime data until compatibility, parity, browser integration, performance and rights gates have evidence.
