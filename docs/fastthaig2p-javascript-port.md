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
| Source-filtered dictionary + normalizer + default wordlist assets | DONE_VERIFIED | Build emits `web/vendor/native/fastthaig2p-ipa.json` from the exact filtered wheel; provenance, entry count, size and SHA-256 are checked. |
| Text normalization | DONE_VERIFIED | #42181862972: 18 pinned CPython cases passed with the extracted PyThaiNLP default wordlist, including maiyamok. |
| PyThaiNLP newmm tokenizer | DONE_VERIFIED | #42181862972: 16 FastThaiG2P custom-dictionary cases and 18 PyThaiNLP default-wordlist cases passed token-array parity. |
| Dictionary IPA lookup | PARTIAL | Native pipeline uses the 13,144-entry Wiktionary-only map and matches 16 dictionary-only CPython cases; OOV fallback is not yet available. |
| TLTK OOV fallback | BLOCKED / PARTIAL | The current fallback depends on `_th2ipa.py`, six TLTK-derived data assets, trigram statistics and a pickled syllable-variant structure. The source repository contains conflicting LGPL-3.0/BSD-3-Clause evidence for the data package. Acceptance requires an explicit asset-level licensing disposition and deterministic JSON serialization of the pickle before porting. |
| Typed IPA result contract | PARTIAL | Tone contours and segmental IPA are parsed; exact parity for uncertainty, unsupported symbols, word/syllable alignment and metadata remains TODO. |
| IPA → Ukrainian adapter | REUSED | Existing `web/src/ipa-ua.js` remains the sole target adaptation boundary; it must not be duplicated. |
| Native pipeline composition | PARTIAL | `createFastThaiG2PNativePipeline` composes normalization, default/custom newmm, dictionary lookup and existing IPA→Ukrainian adapter; 16 dictionary-only cases match CPython. OOV fallback is missing. |
| Worker integration | TODO | Add a separate native worker and an explicit runtime selector for CI only; production remains on Pyodide until all gates pass. |
| Python/JS differential suite | PARTIAL | 18 normalizer, 16 custom tokenizer and 16 dictionary-only front-half cases pass. Typed IPA metadata and full service JSON/OOV differential remain TODO. |
| Browser cold/warm tests | TODO | No native Worker exists yet; future Chromium smoke must prove no Pyodide, Python, wheel or API requests and verify offline repeat use after data cache. |
| Footprint/performance | TODO | Measure transferred bytes, cold-start, warm latency and memory on desktop and mobile; compare to the 20.5 MB baseline. |
| Documentation and attribution | PARTIAL | This decision/ledger records the intended original port and required upstream/data notices. Update public product claims only after production cutover. |

## Implemented native front-half

The browser-native front-half is split into inspectable modules:
- `web/src/fastthaig2p-normalizer.js` ports the pinned normalization order and numeric/email/symbol/abbreviation rules. Its constant maps are AST-extracted from the pinned FastThaiG2P Python source at build time.
- `web/src/fastthaig2p-tokenizer.js` ports PyThaiNLP 5.4.0 newmm, including TCC boundaries, trie prefix matching, graph traversal, unknown chunks and formatted-number rejoining.
- Two tokenizer instances use the exact PyThaiNLP default wordlist (for mai yamok) and the FastThaiG2P custom filtered dictionary (for G2P segmentation).
- `web/src/fastthaig2p-native.js` composes normalization → default newmm → custom newmm → Wiktionary-only IPA lookup → the existing IPA→Ukrainian adapter. It preserves slash/dot IPA, Chao tone and vowel-length metadata, and fails closed on dictionary misses.
- The native bundle emits source-attributed JSON/text data assets with source pins, license metadata, sizes and SHA-256 integrity records. These are data assets; they are not Python modules or executable wheels.

Differential evidence on the exact tested code head:
- 18 normalizer cases matched pinned CPython, including maiyamok using the extracted default wordlist;
- 16 custom FastThaiG2P newmm cases matched PyThaiNLP;
- 16 dictionary-only end-to-end front-half cases matched CPython raw IPA.

This is not a complete FastThaiG2P port: the TLTK-derived OOV fallback, full typed IPA/result JSON parity and a native Worker are still missing. The public application continues to use the verified Pyodide worker.

## Licensing and data boundary

- FastThaiG2P source code is Apache-2.0 with Amazon NOTICE at the pinned revision.
- The filtered dictionary is derived from Wiktionary via Kaikki.org/Wiktextract and is labelled CC BY-SA 4.0; attribution and share-alike obligations continue to apply.
- The newmm tokenizer port is based on PyThaiNLP 5.4.0 source under Apache-2.0; retain the upstream copyright/license notice in the bundled notices.
- TLTK-derived parser/data licensing remains unresolved at file/package scope. Preserve both existing BSD-3-Clause and LGPL-3.0 notices. Do not copy, transform or redistribute the TLTK fallback assets into the native bundle until the exact applicable terms are established.
- The project MIT license applies to ClippyFirst-authored code only; it does not relicense upstream code or third-party data.

## Verification commands

```bash
node --check web/src/fastthaig2p-native.js
node web/tests/fastthaig2p-native.test.mjs
python scripts/fastthaig2p_normalizer_reference.py > build/fastthaig2p-normalizer-reference.json
python scripts/fastthaig2p_tokenizer_reference.py > build/fastthaig2p-tokenizer-reference.json
python scripts/fastthaig2p_native_pipeline_reference.py > build/fastthaig2p-native-pipeline-reference.json
node web/tests/fastthaig2p-normalizer-parity.test.mjs build/fastthaig2p-normalizer-reference.json web/vendor/native/fastthaig2p-normalizer.json web/vendor/native/pythainlp-default-words.txt
node web/tests/fastthaig2p-tokenizer-parity.test.mjs build/fastthaig2p-tokenizer-reference.json web/vendor/native/fastthaig2p-ipa.json
node web/tests/fastthaig2p-native-pipeline.test.mjs build/fastthaig2p-native-pipeline-reference.json web/vendor/native/fastthaig2p-ipa.json web/vendor/native/fastthaig2p-normalizer.json web/vendor/native/pythainlp-default-words.txt
python scripts/validate_github_workflows.py
python -m unittest discover -s tests -v
node web/tests/fastthaig2p-pyodide.test.mjs build/pyodide-wheels build/fastthaig2p-native.json
node web/tests/fastthaig2p-browser.test.mjs
```

The native front-half differential suite passes on the cited code head, but OOV, typed-result and native Worker parity are still unverified. Do not claim full browser-native capability, performance improvement or production readiness.
