# FastThaiG2P browser/WASM port

**Owner decisions (2026-11-05):** GitHub Pages is the only hosting target. Keep FastThaiG2P and port the shared Python service to the browser using Pyodide. Do not introduce a separate API host, Vercel, serverless functions, CDN runtime dependencies, or a parallel JavaScript G2P implementation.

## Architecture implemented

```
GitHub Pages static files
  ├─ Ukrainian UI
  ├─ module Web Worker
  ├─ self-hosted Pyodide 0.29.5
  ├─ pinned pure-Python wheels + SHA-256 manifest
  └─ shared thai_ukrainian.fastthaig2p_service
       ├─ FastThaiG2P adapter
       ├─ typed phonetic result / IPA boundary
       └─ existing IPA → Ukrainian adaptation
```

- `src/thai_ukrainian/fastthaig2p_service.py` is transport-neutral and shared by the FastAPI reference wrapper and the browser worker.
- `web/src/fastthaig2p-worker.js` initializes Pyodide in a module worker, loads only same-origin assets, checks the manifest, exact wheel versions, filenames, sizes and SHA-256 values, and installs pure-Python wheels locally without micropip or a CDN.
- `web/src/app.js` sends Thai input only to that worker. The browser UI no longer calls `/api/analyze`.
- The Python adapter and IPA→Ukrainian function remain canonical. No parallel JavaScript phonology or transliteration path was introduced.
- Incomplete IPA remains fail-closed; the worker returns the shared service's explicit rejection rather than switching to RTGS or another engine.

## Runtime and browser verification

Code checkpoint `9894c80a4c47fe0b1e3b966ff4f6fb3dcaa2e124` was verified by exact-head workflows:

- [Pyodide compatibility and Chromium worker smoke — 42073702543](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42073702543) — **SUCCESS**.
- [Full CI — 42073702565](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42073702565) — **SUCCESS**, all 3 jobs.
- [Web static validation — 42073702564](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42073702564) — **SUCCESS**.
- [Site API reference wrapper — 42073702559](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42073702559) — **SUCCESS**.
- [Optional external FastThaiG2P smoke — 42073702598](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42073702598) — **SUCCESS**.

The Pyodide workflow:
- compared complete CPython/Pyodide shared-service JSON for four Thai inputs;
- preserved the `สวน → /sua̯n˩˩˦/` regression;
- staged the same-origin Pyodide runtime, wheels and ten hashed license/NOTICE files;
- verified that public Pages packaging is refused while the rights flag is false;
- ran the actual module worker in headless Chromium, passing cold initialization and warm analysis;
- confirmed no `/api/analyze` or CDN request.

The browser test is a real static-site browser smoke, not a live GitHub Pages deployment.

## Browser data provenance and runtime footprint

The pinned FastThaiG2P upstream wheel contains 13,144 Wiktionary-labelled entries and 48,957 model-generated entries. The browser build now retains only the Wiktionary-labelled subset; generated, manual and unknown-source entries are excluded. The tokenizer wordlist is reduced to the same retained IPA keys. The upstream TLTK-derived OOV fallback remains enabled.

Measured source counts from the exact Pyodide workflow:
- Wiktionary retained: **13,144**.
- Model-generated excluded: **48,957**.
- Manual/unknown source rows in pinned runtime metadata: **0**.
- One IPA value (`สวน`) differs from the source metadata's IPA snapshot; the runtime value is preserved and the mismatch is disclosed in the embedded provenance manifest.

The filtered FastThaiG2P wheel embeds `browser-data-provenance.json` and `WIKTIONARY-ATTRIBUTION.md`. See [FastThaiG2P data provenance and redistribution review](fastthaig2p-data-provenance.md).

Verified ephemeral CI footprint:
- 4 pure-Python wheels: **7,823,799 bytes** total; FastThaiG2P wheel **6,317,099 bytes**.
- 14 self-hosted Pyodide runtime files: **12,610,023 bytes**.
- 10 license/NOTICE files: **57,389 bytes**.
- Combined raw footprint: **20,491,211 bytes** before HTTP compression.
- PyThaiNLP 5.4.0: 67,689,272 → 3,648,217 uncompressed member bytes; 37 unused corpus assets removed (64,041,055 bytes). The retained corpus lists are CC0-1.0.

## Public Pages deployment gate

`data/third_party/fastthaig2p-browser-bundle.json` deliberately remains `redistribution_approved: false`.

- The Wiktionary-derived subset is attributed to Wiktionary contributors and Kaikki.org/Wiktextract and labelled CC BY-SA 4.0.
- FastThaiG2P code is Apache-2.0 with Amazon NOTICE.
- The vendored TLTK parser header identifies version 1.3.8 and BSD-3-Clause; five of six fallback data files have exact Git blob matches. The remaining `sylform_var.pkl` transformation from TLTK's `.pklz` asset is not independently reproduced.
- PyThaiNLP Apache-2.0 and CC0 corpus notices, Pyodide MPL-2.0, tzdata Apache-2.0, TLTK BSD-3/LGPL repository evidence, Wiktionary CC BY-SA and project MIT notices are staged and hashed.
- The build and worker require the complete ten-file notice set. The Pages post-deploy smoke will fetch every notice and verify its size/SHA-256 against the manifest.

The Pages workflow also requires the explicit repository variable `FASTTHAIG2P_PYODIDE_BUNDLE_READY=true`; the bundle builder independently refuses `--purpose pages` unless the rights manifest says `redistribution_approved=true`. CI uses ephemeral assets and does not grant public redistribution permission.

No deployment, main-branch change, merge, release tag or repository setting change was made. PR #210 remains open and unmerged. The branch's static preview was tested in Chromium, but a real GitHub Pages URL has not yet been deployed or measured.

## Current acceptance ledger

| Area | Criterion | Status |
|---|---|---|
| Shared service | Same Python service used by API and browser | DONE_VERIFIED |
| Pyodide runtime | Pinned pure-Python wheels import and run | DONE_VERIFIED |
| CPython/Pyodide parity | Complete service JSON matches for 4 Thai inputs | DONE_VERIFIED |
| Browser worker | Cold/warm Chromium run; no API/CDN text transfer | DONE_VERIFIED |
| Bundle integrity | Exact wheel versions, sizes and SHA-256 | DONE_VERIFIED |
| License notices | Ten notices embedded in manifest and checked | DONE_VERIFIED |
| PyThaiNLP footprint | 37 unused corpus assets removed; required CC0 lists retained | DONE_VERIFIED |
| Source filtering | Generated/manual/unknown IPA excluded; 13,144 Wiktionary entries retained | DONE_VERIFIED |
| TLTK fallback | BSD-3 source header and 5/6 data blob matches | PARTIAL — one pickle transformation not independently reproduced |
| Public redistribution | Owner rights flag remains false | BLOCKED — final evidence/approval pending |
| Public Pages deployment | Exact merged main commit deployed and live-smoked | BLOCKED — no merge or deployment |
| Performance | Actual Pages transfer/cold-start and mobile timing | TODO — requires public deployment |

## Product and linguistic limits

This is a runtime-port milestone, not a linguistic validation result. Independent IPA gold remains 0; accuracy remains `NOT_MEASURED`; Ukrainian practical forms remain provisional. No TTS, audio, acoustic validation, or external expert review is required for the owner-approved beta scope.
