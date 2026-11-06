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
- TLTK fallback provenance is mechanically verified at the pinned revisions: five assets are byte-identical and the sixth is the exact BZip2-decompressed counterpart of TLTK's `.pklz` asset. Their total is 19,883,873 bytes raw and 5,911,457 bytes under deterministic gzip level 9 (70.27% smaller; estimate, not measured Pages transfer). The pinned TLTK snapshot is the 2025-10-20 `update tltl 1.9.1` commit; its setup.py, README and LICENSE.txt state BSD-3-Clause, and official [PyPI TLTK 1.9.1 release metadata](https://pypi.org/project/tltk/1.9.1/) also declares BSD-3-Clause. MANIFEST.in includes LICENSE.txt. The conflicting root LICENSE is unchanged since the 2018-11-23 initial commit; PKG-INFO is unchanged since 2018-11-29 version 1.1.7 and contains stale GPLv3 metadata. Evidence therefore supports BSD-3-Clause for the published 1.9.1 package and packaged fallback files, while the root notice remains a historical conflict. Preserve both notices and attribution; this is not legal advice or an author-issued clarification.
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


## Latest branch-head reconciliation — 2026-11-06

- Latest code/test head: `228d80d51d58a4437ab0f70ba12597a1259902e8`.
- The native-first UI contract test was updated to mock both workers: dictionary-covered requests use only the native Worker; only a `native_dictionary_miss` creates the Pyodide Worker. The test also retains incomplete-IPA fail-closed and stale-response checks.
- Exact-head CI, Web Static, site API and Pyodide compatibility PR runs are queued/pending; no current-head pass is claimed. Earlier dictionary-only differential and isolated native Worker evidence remains on head `24e4605b7921524b60dc1c5a3e3e9a66965a3206`.


## Exact-head verification update — 2026-11-06

- Latest code/test commit: `37e0ee6b6fb1385bd4c98bfdd582d8eee3dac5c1`.
- The first UI contract runs exposed a fake-worker test ordering issue: the native path awaits its ready promise before posting a convert request. The test attempted to invoke its deferred callback before that microtask ran. The test now flushes one microtask and asserts the callback exists; production code is unchanged.
- Corrected-head Web Static [42198840129](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42198840129) and Site API [42198840133](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42198840133) passed. Full CI [42198840130](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42198840130) and Pyodide compatibility [42198840192](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42198840192) were still running at this update. Native-first UI acceptance remains PARTIAL until both finish successfully.
- Keep the existing Pyodide fallback for OOV. Full native OOV parity, TLTK rights disposition, mobile/offline performance and manual accessibility remain open. Linguistic accuracy remains `NOT_MEASURED`.


## Mainline integration update — 2026-11-06

- PR #214 was squash-merged to main as `29b63b8f58db1f6d7ff068d131df0b0759895115`.
- Final PR head `0d4503ed55ff726807917e2cfbf14c0ad30eb624` passed Full CI #42199395072, Web Static #42199395225, Site API #42199395069 and Pyodide compatibility #42199395284.
- The mainline browser path is hybrid native-first. The existing Pyodide worker remains the OOV fallback. The post-merge Pages deployment/live smoke is not yet verified; do not claim public-site cutover or Pyodide removal.


## TLTK rights disposition update — 2026-11-06

The six TLTK fallback assets are now classified as BSD-3-Clause for the pinned TLTK 1.9.1 package scope. Evidence: the versioned README's license-change statement, setup.py's 1.9.1/BSD declaration and package_data list containing all six assets, MANIFEST.in's inclusion of LICENSE.txt, the BSD terms in LICENSE.txt, and PyPI's 1.9.1 release metadata. The repository-root LGPL-3.0 file is retained as a separate historical repository notice; stale PKG-INFO is version 1.1.7/GPLv3. See [the detailed source-based license review](fastthaig2p-license-review-2026-11-05.md) and [public notices](../web/third-party-notices.html).

This clears the TLTK package-license evidence gate for use and redistribution of those six packaged assets under BSD-3-Clause conditions. It does **not** complete the browser-native OOV algorithm or its parity gate. Full TLTK OOV implementation remains TODO; Pyodide remains the OOV fallback until native output matches the pinned Python service contract.


## Alternative JavaScript package review — 2026-11-06

The npm package `tltk-js@0.1.4` was inspected as a possible shortcut. It is not accepted as a production dependency or as the parity reference:

- The npm package metadata declares WTFPL, while the package README declares MIT. This license metadata mismatch is not a clean compliance basis.
- The published package reports 66,340,514 bytes unpacked, which is disproportionate for this browser-first runtime.
- Its README describes an optional heuristic fallback for unknown syllables that intentionally differs from the Python TLTK behavior. That cannot satisfy this project's exact FastThaiG2P/TLTK OOV parity contract.
- It is not pinned to the exact FastThaiG2P parser/data combination used by this repository.

Use it only as a non-authoritative comparison reference. Continue implementing against the pinned FastThaiG2P parser source and TLTK 1.9.1 packaged tables; never substitute its heuristic output for an unsupported or failed native parse.

Sources: [npm package page](https://www.npmjs.com/package/tltk-js), [published package metadata](https://registry.npmjs.org/tltk-js).


## Browser-native TLTK OOV port — 2026-11-06

The native worker now has a browser JavaScript implementation of the pinned FastThaiG2P/TLTK 1.3.8 OOV path. It ports TLTK syllable-pattern matching, literal syllable dictionary entries, stable consonant mapping, tone assignment and exceptions, syllable transformations, syllable trigram segmentation, word segmentation and collocation scoring, phone-trigram candidate selection, and TLTK romanization-to-IPA. The lazy same-origin data pack is JSON/gzip (no Python or pickle) and verifies compressed and decompressed SHA-256. It is loaded only after a miss in the filtered native IPA dictionary. Pyodide remains a fail-closed last-resort compatibility fallback if native TLTK cannot produce a complete result.

**Exact-head evidence on PR #216 head `d4f35892adc02eb03b1fd345a0193c46c07b1eb7`:** the pinned Python generator produced 64 OOV reference cases (zero rejected); module parity 64/64 and Worker parity 64/64 passed; Chromium confirmed lazy TLTK loading and no Python/Pyodide/wheels/API/CDN requests for a TLTK-supported OOV input. CI 42217143967, Web Static 42217143995, Pages build 42217143962, and Pyodide compatibility 42217144084 all passed. The PR Pages build validates the owner-approved bundle but does not publish on a pull_request event. Actual post-merge Pages deployment and live smoke remain pending.

The six TLTK 1.9.1 packaged fallback assets are supported by package-level BSD-3-Clause evidence. Preserve copyright notice, conditions, disclaimer and no-endorsement clause. Retain the separate repository-root LGPL-3.0 notice and stale 1.1.7/GPLv3 metadata as historical context; do not generalize the package conclusion to the entire TLTK repository. See [the license review](fastthaig2p-license-review-2026-11-05.md).

This establishes implementation parity with the pinned Python engine, not independent phonetic correctness. Thai IPA gold and Ukrainian expert validation remain absent; accuracy is NOT_MEASURED. Cold/warm/offline/mobile performance, memory, and manual accessibility remain TODO.


## Follow-up verification after PR #217 — 2026-11-06

The native TLTK OOV implementation is now integrated into main. PR #217 merged as `533cd3f8df6112b000f5c91524f8050026b4d79a`. Its exact head passed CI 42226080426 (401 passed, 1 skipped, 1211 subtests; Ruff and wheel smoke), Pages build 42226080435 (public bundle artifact produced), and Pyodide compatibility 42226080581. The Python generator produced 64 OOV references with no rejected candidates; typed service parity passed 64/64 in the module and 64/64 in the native Worker. Chromium verified the native Worker and same-origin Pyodide fallback path. A regression assertion now locks the pinned TLTK segmentation/scoring behavior for `กขส`.

The PR Pages build does not deploy. The main-push Pages workflow is configured and contains live checks for the public page, native and Pyodide workers, TLTK OOV manifest/data, SHA-256, and notices. The post-merge run/live URL could not be independently observed with the available GitHub/web access; deployment remains NOT_VERIFIED.

The six TLTK 1.9.1 packaged fallback assets are treated as BSD-3-Clause under the versioned package evidence. Research use needs no special exemption; redistribution is allowed with the required notices/conditions/disclaimer/no-endorsement clause. The repository-root LGPL-3.0 and stale 1.1.7/GPLv3 metadata remain separate historical context.

