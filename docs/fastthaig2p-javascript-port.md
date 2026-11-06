# FastThaiG2P native JavaScript/TypeScript port

**Owner decision (2026-11-06):** proceed with an original browser-native JavaScript/TypeScript port of the pinned FastThaiG2P pipeline. The existing Pyodide implementation remains the production/reference path until the native implementation reaches exact, evidence-backed acceptance. Do not cut over or remove Pyodide merely because a dictionary-only prototype exists.

## Product and attribution positioning

The deliverable is a **ClippyFirst browser-native JavaScript/TypeScript port of FastThaiG2P**, not a claim that the upstream Python package itself is JavaScript. Preserve the upstream project name, author, immutable source revision, Apache-2.0 license and Amazon NOTICE. Clearly distinguish:
- upstream FastThaiG2P Python source and its license;
- ClippyFirst-authored JavaScript/TypeScript port code;
- third-party dictionary/fallback data and their separate provenance/licensing.

A language port does not automatically transfer copyright in the upstream implementation or clear the rights of its bundled datasets. No generated/manual IPA entries may be reintroduced into the browser dictionary. The currently approved browser dictionary contains only the 13,144 source-labelled Wiktionary records from the pinned upstream snapshot.

## Current baseline

- Repository browser path: native-first JavaScript Worker for dictionary-covered tokens; the existing Pyodide 0.29.5 Worker is loaded lazily only after a native dictionary miss. Pyodide remains the full OOV reference/fallback path.
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
| JavaScript module/result adapter | PARTIAL | `web/src/fastthaig2p-native.js` composes the dictionary-covered service path and is now called by the public UI first. Full native OOV parity is not implemented; browser acceptance for native-first/lazy Pyodide fallback is pending on the current branch head. |
| Source-filtered dictionary + normalizer + default wordlist assets | DONE_VERIFIED | Build emits `web/vendor/native/fastthaig2p-ipa.json` from the exact filtered wheel; provenance, entry count, size and SHA-256 are checked. |
| Text normalization | DONE_VERIFIED | #42181862972: 18 pinned CPython cases passed with the extracted PyThaiNLP default wordlist, including maiyamok. |
| PyThaiNLP newmm tokenizer | DONE_VERIFIED | #42181862972: 16 FastThaiG2P custom-dictionary cases and 18 PyThaiNLP default-wordlist cases passed token-array parity. |
| Dictionary IPA lookup | PARTIAL | Native pipeline uses the 13,144-entry Wiktionary-only map and matches 16 dictionary-only CPython cases; OOV fallback is not yet available. |
| TLTK OOV fallback | BLOCKED / PARTIAL | All six pinned asset transformations are verified. Payload is 19,883,873 bytes raw / 5,911,457 bytes deterministic gzip estimate (70.27% reduction). Rights scope still needs explicit disposition (BSD-3-Clause package metadata/LICENSE.txt vs repository LGPL-3.0 and stale GPLv3 PKG-INFO); native algorithm/data port and parity remain TODO. No fallback data is shipped publicly. |
| Typed IPA result contract | DONE_VERIFIED (dictionary-covered inputs) | 16 complete service JSON responses match pinned CPython, including tone/length, uncertainty, unsupported symbols, word/syllable alignment, provenance, warnings and IPA→Ukrainian adaptation. OOV parity remains outside this result. |
| IPA → Ukrainian adapter | REUSED | Existing `web/src/ipa-ua.js` remains the sole target adaptation boundary; it must not be duplicated. |
| Native pipeline composition | DONE_VERIFIED (dictionary-covered inputs) | `createFastThaiG2PNativePipeline` composes normalization, default/custom newmm, dictionary lookup and existing IPA→Ukrainian adapter; 16 complete service JSON responses match pinned CPython exactly. OOV fallback remains unavailable. |
| Native Worker smoke | DONE_VERIFIED (front-half) | Exact-head Pyodide compatibility #42186384082: real Chromium module Worker matched all 16 pinned CPython normalized-input/token/raw-IPA cases and returned the Ukrainian fail-closed OOV response; request audit confirmed no Pyodide/Python/wheels/WASM/remote requests. |
| Python/JS differential suite | DONE_VERIFIED (dictionary-covered inputs) | Exact-head CI #42186384082 passes 18 normalizer cases, 16 custom tokenizer cases, and 16 complete service JSON parity cases including typed IPA metadata, Ukrainian adaptation, tone/length, rules, provenance and warnings. OOV algorithm parity remains TODO. |
| Browser cold/warm/offline tests | PARTIAL | Isolated Chromium native Worker smoke proves same-origin JS/data-only execution and no Pyodide/Python/wheel/remote requests. New public-UI acceptance checks no Python downloads for dictionary hits and lazy Pyodide only on OOV; current run is pending. Cold-vs-warm timing, memory, cache reuse and offline reload remain TODO. |
| Footprint/performance | TODO | Measure transferred bytes, cold-start, warm latency and memory on desktop and mobile; compare to the 20.5 MB baseline. |
| Documentation and attribution | PARTIAL | This decision/ledger records the intended original port and required upstream/data notices. Update public product claims only after production cutover. |

## Implemented native front-half

The browser-native front-half is split into inspectable modules and is now the first runtime path in the public UI:
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
- The same 16 cases also passed inside the real Chromium module Worker, including manifest/SHA-256 data loading; an OOV probe returned the expected Ukrainian fail-closed error without fetching Python/Pyodide/wheels/remote assets.

This is not a complete FastThaiG2P port: the TLTK-derived OOV fallback still runs through the existing Pyodide Worker after a native dictionary miss. Dictionary-covered service JSON parity is verified; the full native OOV algorithm is not ported. The fallback data is ~19.9 MB raw (5.91 MB gzip estimate), so it is not negligible; measure actual Pages transfer and compare with the Pyodide baseline before considering a native OOV port. The public application now uses the native module Worker first and lazily creates the Pyodide Worker only when the native dictionary does not cover the input.

## Licensing and data boundary

- FastThaiG2P source code is Apache-2.0 with Amazon NOTICE at the pinned revision.
- The filtered dictionary is derived from Wiktionary via Kaikki.org/Wiktextract and is labelled CC BY-SA 4.0; attribution and share-alike obligations continue to apply.
- The newmm tokenizer port is based on PyThaiNLP 5.4.0 source under Apache-2.0; retain the upstream copyright/license notice in the bundled notices.
- TLTK fallback provenance is mechanically verified at the pinned revisions: five assets are byte-identical and the sixth is the exact BZip2-decompressed counterpart of TLTK's `.pklz` asset. Their total is 19,883,873 bytes raw and 5,911,457 bytes under deterministic gzip level 9 (70.27% smaller; estimate, not measured Pages transfer). Rights scope remains unresolved because the TLTK repository contains BSD-3-Clause package metadata and LICENSE.txt alongside an LGPL-3.0 root LICENSE and stale GPLv3 PKG-INFO. Preserve all notices; do not publish these assets in the public bundle until the rights disposition is resolved.
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

Exact-head PR validation on 24e4605b7921524b60dc1c5a3e3e9a66965a3206 now passes the complete CI, Web Static and Pyodide compatibility workflows. The 16 dictionary-covered service responses match Python JSON exactly, and the isolated Chromium Worker matches the front-half plus fail-closed OOV behavior. The six TLTK fallback file transformations are byte/decompression verified; their rights scope remains unresolved and the OOV algorithm is not ported. Public UI remains on Pyodide. Do not claim full browser-native replacement, measured performance improvement or production readiness.


## Exact-head verification update — 2026-11-06

- Code head: `24e4605b7921524b60dc1c5a3e3e9a66965a3206`.
- [Pyodide compatibility #42186384082](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42186384082): SUCCESS. Builds the Pages bundle, smoke-tests the existing Pyodide Worker, and tests the native module Worker in Chromium without Python/Pyodide/wheels/WASM/remote requests.
- [Web Static #42186383919](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42186383919): SUCCESS.
- [Full CI #42186383939](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42186383939): SUCCESS, including the complete Python test suite, master artifact generation/validation, JS contracts and browser segmentation benchmark.
- The pipeline differential suite compares the complete service JSON for 16 dictionary-covered inputs, not just raw IPA. It does not establish OOV fallback parity.
- TLTK's six data-file transformations are reproducibly verified (five byte-identical, one exact BZip2 decompression). License scope remains ambiguous; no TLTK fallback code/data is bundled into the native browser assets.
- Native browser port remains PARTIAL overall: no public UI cutover, no TLTK OOV port, and no measured cold/warm/offline/mobile performance or memory benchmark.


## Native-first public UI integration — 2026-11-06

- `web/src/app.js` now initializes the native module Worker first. Dictionary-covered requests complete without creating the Pyodide Worker. Only the specific `native_dictionary_miss` response triggers the existing full FastThaiG2P Pyodide Worker; other native integrity/runtime errors remain visible rather than silently loading a 20 MB runtime.
- `web/index.html` discloses this behavior to users. `web/system.html` describes the hybrid pipeline and does not claim Pyodide has been removed.
- `scripts/fastthaig2p_native_oov_reference.py` searches the pinned TLTK fallback dictionary for a reproducible token that is not in the filtered IPA map and emits the Python service JSON reference.
- `web/tests/fastthaig2p-browser.test.mjs` now asserts that two dictionary-covered examples make no `/vendor/pyodide/` or `/vendor/wheels/` requests, then verifies a pinned OOV input triggers the same FastThaiG2P Pyodide fallback and matches its IPA.
- Current implementation head before this documentation reconciliation: `0e6479450d6205f0a2b65aa80fb1e3d6a13937b0`. The new native-first browser acceptance, full CI and Web Static runs are pending; do not mark this integration DONE_VERIFIED until those runs pass.
- This is a hybrid browser-native-first deployment, not a full Pyodide replacement. No Python modules are loaded for dictionary-covered inputs; JS modules and the ~2.2 MB native data bundle are still fetched from same-origin GitHub Pages on first use. An OOV input still loads Pyodide and its wheels.
