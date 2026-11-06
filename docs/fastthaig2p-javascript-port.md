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
| TLTK OOV fallback | BLOCKED / PARTIAL | `scripts/verify_tltk_fallback_provenance.py` verifies all six pinned fallback assets: five byte-identical and `sylform_var.pkl` exactly equal to BZip2-decompressed TLTK `.pklz`. The remaining blocker is rights scope (BSD-3-Clause package metadata and LICENSE.txt versus repository LGPL-3.0 and stale GPLv3 PKG-INFO), followed by native algorithm/data port and parity. No fallback data is shipped in the public bundle. |
| Typed IPA result contract | PARTIAL | Tone contours and segmental IPA are parsed; exact parity for uncertainty, unsupported symbols, word/syllable alignment and metadata remains TODO. |
| IPA → Ukrainian adapter | REUSED | Existing `web/src/ipa-ua.js` remains the sole target adaptation boundary; it must not be duplicated. |
| Native pipeline composition | PARTIAL | `createFastThaiG2PNativePipeline` composes normalization, default/custom newmm, dictionary lookup and existing IPA→Ukrainian adapter; 16 dictionary-only cases match CPython. OOV fallback is missing. |
| Native Worker smoke | DONE_VERIFIED | Pyodide compatibility #42183434605: real Chromium Worker initialized, loaded only same-origin JS/data, matched CPython raw IPA, and requested no Pyodide/Python/wheel/remote assets on current PR head. |
| Python/JS differential suite | PARTIAL | 18 normalizer, 16 custom tokenizer and 16 dictionary-only front-half cases pass. Typed IPA metadata and full service JSON/OOV differential remain TODO. |
| Browser cold/warm/offline tests | PARTIAL | Isolated Chromium native Worker smoke proves same-origin JS/data-only execution and no Pyodide/Python/wheel/remote requests. Cold-vs-warm timing, memory, cache reuse and offline reload remain TODO. |
| Footprint/performance | TODO | Measure transferred bytes, cold-start, warm latency and memory on desktop and mobile; compare to the 20.5 MB baseline. |
| Documentation and attribution | PARTIAL | This decision/ledger records the intended original port and required upstream/data notices. Update public product claims only after production cutover. |

## Implemented native front-half

The browser-native front-half is split into inspectable modules:
- `web/src/fastthaig2p-normalizer.js` ports the pinned normalization order and numeric/email/symbol/abbreviation rules. Its constant maps are AST-extracted from the pinned FastThaiG2P Python source at build time.
- `web/src/fastthaig2p-tokenizer.js` ports PyThaiNLP 5.4.0 newmm, including TCC boundaries, trie prefix matching, graph traversal, unknown chunks and formatted-number rejoining.
- Two tokenizer instances use the exact PyThaiNLP default wordlist (for mai yamok) and the FastThaiG2P custom filtered dictionary (for G2P segmentation).
- `web/src/fastthaig2p-native.js` composes normalization → default newmm → custom newmm → Wiktionary-only IPA lookup → the existing IPA→Ukrainian adapter. It preserves slash/dot IPA, Chao tone and vowel-length metadata, and fails closed on dictionary misses.
- `web/src/fastthaig2p-native-worker.js` runs this front-half in a separate module Worker; `loadFastThaiG2PNativeAssets` verifies each same-origin data asset against the manifest before constructing the pipeline.
- The native bundle emits source-attributed JSON/text data assets with source pins, license metadata, sizes and SHA-256 integrity records. These are data assets; they are not Python modules or executable wheels.

Differential evidence on the exact tested code head:
- 18 normalizer cases matched pinned CPython, including maiyamok using the extracted default wordlist;
- 16 custom FastThaiG2P newmm cases matched PyThaiNLP;
- 16 dictionary-only end-to-end front-half cases matched CPython raw IPA.

This is not a complete FastThaiG2P port: the TLTK-derived OOV fallback and full typed IPA/result JSON parity are still missing. An isolated native module Worker is implemented and passes Chromium smoke, but is not yet integrated into the public application, which continues to use the verified Pyodide worker.

## Licensing and data boundary

- FastThaiG2P source code is Apache-2.0 with Amazon NOTICE at the pinned revision.
- The filtered dictionary is derived from Wiktionary via Kaikki.org/Wiktextract and is labelled CC BY-SA 4.0; attribution and share-alike obligations continue to apply.
- The newmm tokenizer port is based on PyThaiNLP 5.4.0 source under Apache-2.0; retain the upstream copyright/license notice in the bundled notices.
- TLTK fallback provenance is now mechanically verified at the pinned revisions: five assets are byte-identical and the sixth is the exact BZip2-decompressed counterpart of TLTK's `.pklz` asset. Rights scope remains unresolved because the TLTK repository contains BSD-3-Clause package metadata and LICENSE.txt alongside an LGPL-3.0 root LICENSE and stale GPLv3 PKG-INFO. Preserve all notices; do not publish these assets in the public bundle until the rights disposition is resolved.
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
python scripts/verify_tltk_fallback_provenance.py --fastthaig2p build/FastThaiG2P --tltk build/TLTK --report build/tltk-fallback-provenance.json
python scripts/validate_github_workflows.py
python -m unittest discover -s tests -v
node web/tests/fastthaig2p-pyodide.test.mjs build/pyodide-wheels build/fastthaig2p-native.json
node web/tests/fastthaig2p-browser.test.mjs
```

The native front-half differential suite and isolated Chromium Worker smoke pass on the cited code head, but the TLTK OOV algorithm has not yet been ported and full typed-result parity remains unverified. The six upstream fallback data transformations are verified; the remaining gate is license scope and implementation parity. Do not claim full browser-native capability, performance improvement or production readiness.
