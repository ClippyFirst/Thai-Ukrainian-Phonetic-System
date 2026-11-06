# FastThaiG2P native JavaScript/TypeScript port

**Owner decision (2026-11-06):** proceed with an original browser-native JavaScript/TypeScript port of the pinned FastThaiG2P pipeline. The existing Pyodide implementation remains the production/reference path until the native implementation reaches exact, evidence-backed acceptance. Do not cut over or remove Pyodide merely because a dictionary-only prototype exists.

## Product and attribution positioning

The deliverable is a **ClippyFirst browser-native JavaScript/TypeScript port of FastThaiG2P**, not a claim that the upstream Python package itself is JavaScript. Preserve the upstream project name, author, immutable source revision, Apache-2.0 license and Amazon NOTICE. Clearly distinguish:
- upstream FastThaiG2P Python source and its license;
- ClippyFirst-authored JavaScript/TypeScript port code;
- third-party dictionary/fallback data and their separate provenance/licensing.

A language port does not automatically transfer copyright in the upstream implementation or clear the rights of its bundled datasets. No generated/manual IPA entries may be reintroduced into the browser dictionary. The currently approved browser dictionary contains only the 13,144 source-labelled Wiktionary records from the pinned upstream snapshot.

## Current baseline

- Repository production baseline: Pyodide 0.29.5 in a same-origin module Web Worker, with pinned wheels and integrity manifest.
- Upstream pin: `awslabs/FastThaiG2P@4e82a291b4cf2876326744c6580121e9986ad354`.
- The current filtered dictionary contains 13,144 Wiktionary-labelled entries; generated/manual/unknown records are excluded.
- The Python reference adapter is `src/thai_ukrainian/fastthaig2p_adapter.py`; the shared response contract is `src/thai_ukrainian/fastthaig2p_service.py`.
- The current runtime bundle is approximately 20.5 MB raw including Pyodide, wheels, notices and the filtered dataset ZIP. Exact figures vary only if the pinned artifacts change; see `docs/fastthaig2p-pyodide-port.md`.

## Pipeline that must be ported

```
Thai source text
  → upstream-compatible normalization
  → PyThaiNLP newmm tokenization with the same custom/default dictionaries
  → per-token Wiktionary-only IPA lookup
  → TLTK-derived OOV syllable segmentation and pronunciation fallback
  → slash/dot IPA output
  → ClippyFirst typed external-IPA adapter
  → existing IPA → Ukrainian adaptation
  → identical user-visible result contract
```

Do not conflate this work with the separate ClippyFirst Thai orthographic research engine. Do not generate Ukrainian directly from Thai graphemes. IPA remains the adapter boundary.

## Implementation ledger

| Component | Status | Acceptance |
|---|---|---|
| JavaScript module/result adapter | PARTIAL | First dictionary adapter exists in `web/src/fastthaig2p-native.js`; unit tests cover parsing, tone extraction, IPA→Ukrainian adaptation and fail-closed dictionary misses. It is not wired into the public UI. |
| Source-filtered dictionary build asset | IMPLEMENTED_PENDING_EXACT_HEAD_CI | Build emits `web/vendor/native/fastthaig2p-ipa.json` from the exact filtered wheel; provenance, entry count, size and SHA-256 are checked. |
| Text normalization | IMPLEMENTED_PENDING_EXACT_PARITY | JavaScript implementation and AST-extracted upstream data are added; the pinned CPython differential suite must pass for numeric, symbol, abbreviation, email and maiyamok cases. |
| PyThaiNLP newmm tokenizer | TODO | Port the pinned tokenizer algorithm and exact effective default/custom dictionary inputs; token-array parity on a versioned corpus. |
| Dictionary IPA lookup | PARTIAL | Adapter supports an injected map; the exact filtered JSON asset is generated and integrity-manifested. Production tokenizer/lookup integration remains TODO. |
| TLTK OOV fallback | BLOCKED / PARTIAL | The current fallback depends on `_th2ipa.py`, six TLTK-derived data assets, trigram statistics and a pickled syllable-variant structure. The source repository contains conflicting LGPL-3.0/BSD-3-Clause evidence for the data package. Acceptance requires an explicit asset-level licensing disposition and deterministic JSON serialization of the pickle before porting. |
| Typed IPA result contract | PARTIAL | Tone contours and segmental IPA are parsed; exact parity for uncertainty, unsupported symbols, word/syllable alignment and metadata remains TODO. |
| IPA → Ukrainian adapter | REUSED | Existing `web/src/ipa-ua.js` remains the sole target adaptation boundary; it must not be duplicated. |
| Worker integration | TODO | Add a separate native worker and an explicit runtime selector for CI only; production remains on Pyodide until all gates pass. |
| Python/JS differential suite | TODO | Same normalized text, tokens, IPA groups, typed fields and complete service JSON for the same frozen input set. |
| Browser cold/warm tests | TODO | Chromium smoke proves no Pyodide, Python, wheel or API assets are requested by the native path; verify offline repeat use after dictionary cache. |
| Footprint/performance | TODO | Measure transferred bytes, cold-start, warm latency and memory on desktop and mobile; compare to the 20.5 MB baseline. |
| Documentation and attribution | PARTIAL | This decision/ledger records the intended original port and required upstream/data notices. Update public product claims only after production cutover. |

## First implementation slice

`web/src/fastthaig2p-native.js` implements an isolated dictionary-only adapter:
- parses the upstream slash/dot IPA envelope;
- preserves tone contours and vowel-length metadata;
- delegates segmental IPA adaptation to the existing `ipa-ua.js`;
- refuses missing dictionary entries instead of guessing or invoking an unrelated engine;
- labels itself `dictionary-adapter-only`.
- `web/src/fastthaig2p-normalizer.js` ports the upstream normalization sequence; it consumes data maps extracted from the pinned Python source and receives the word tokenizer for maiyamok expansion.

This is a development seam, not a complete FastThaiG2P port. It intentionally does not normalize text, segment unspaced Thai, or provide OOV fallback. The public application continues to use the verified Pyodide worker.

## Licensing and data boundary

- FastThaiG2P source code is Apache-2.0 with Amazon NOTICE at the pinned revision.
- The filtered dictionary is derived from Wiktionary via Kaikki.org/Wiktextract and is labelled CC BY-SA 4.0; attribution and share-alike obligations continue to apply.
- TLTK-derived parser/data licensing remains unresolved at file/package scope. Preserve both existing BSD-3-Clause and LGPL-3.0 notices. Do not copy, transform or redistribute the TLTK fallback assets into the native bundle until the exact applicable terms are established.
- The project MIT license applies to ClippyFirst-authored code only; it does not relicense upstream code or third-party data.

## Verification commands

```bash
node --check web/src/fastthaig2p-native.js
node web/tests/fastthaig2p-native.test.mjs
python scripts/validate_github_workflows.py
python -m unittest discover -s tests -v
node web/tests/fastthaig2p-pyodide.test.mjs build/pyodide-wheels build/fastthaig2p-native.json
node web/tests/fastthaig2p-browser.test.mjs
```

The native test is a unit contract only. Do not claim runtime parity, full browser-native capability, performance improvement or production readiness until the relevant acceptance rows are verified.
