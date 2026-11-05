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

- `src/thai_ukrainian/fastthaig2p_service.py` is transport-neutral and shared by the FastAPI wrapper and the browser worker.
- `web/src/fastthaig2p-worker.js` initializes Pyodide in a module worker, loads only same-origin assets, checks the manifest and exact wheel versions/sizes/SHA-256, and installs pure-Python wheels locally without micropip or a CDN.
- `web/src/app.js` sends Thai input only to that worker. The browser UI no longer calls `/api/analyze`.
- The Python adapter and IPA→Ukrainian function remain canonical. No parallel JavaScript phonology or transliteration path was introduced.
- Incomplete IPA remains fail-closed; the worker returns the shared service's explicit rejection rather than switching to RTGS or another engine.

## Runtime and browser verification

At code checkpoint `8ff38629c5e51dc6e6e709f7a91c786520d148d3`:

- Pyodide 0.29.5 parity passed for four Thai inputs against the same CPython service JSON, including `สวน → /sua̯n˩˩˦/`.
- Chromium loaded the actual module worker and same-origin runtime assets; both cold and warm analysis passed.
- Browser smoke confirmed no `/api/analyze` request and no CDN request.
- The exact runtime bundle staged by CI contained four wheels (8,673,701 bytes) and 12,610,023 bytes of Pyodide runtime files: about 20.3 MiB raw before compression.
- PyThaiNLP 5.4.0's wheel was trimmed from 67,689,272 to 3,648,217 uncompressed member bytes by removing 37 unused corpus assets; only required Python source, `words_th.txt`, `stopwords_th.txt`, and the corpus license notice remain.
- `tzdata==2026.6` is required because PyThaiNLP resolves `ZoneInfo("Asia/Bangkok")`.

Exact workflow evidence at that checkpoint:
- [Pyodide compatibility and Chromium worker smoke — 42066731247](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42066731247)
- [Web static validation — 42066731252](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42066731252)
- [Site API wrapper — 42066731528](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42066731528)
- [Full CI — 42066735544](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42066735544)

These runs predate the source-filtering changes below. They prove the initial browser runtime, not the later filtered wheel.

## Browser data provenance changes

The pinned upstream wheel includes a merged IPA dictionary. Upstream `data/README.md` and `scripts/merge_ipa.py` identify three source classes: manual, Wiktionary, and model-generated. The runtime wheel does not include the source metadata file.

The browser build now clones the exact upstream commit and runs `scripts/prepare_fastthaig2p_browser_source.py` before building the wheel:
- retain only records whose per-entry source label is `wiktionary` or `manual`;
- exclude model-generated and unknown-source records;
- reduce the tokenizer wordlist to the retained IPA keys;
- preserve upstream ordering and report source counts;
- report stale differences between `ipa.json` and the IPA snapshot in `ipa_metadata.json` without silently changing the source label;
- keep the upstream TLTK-derived OOV fallback enabled.

Focused tests cover source filtering, invalid IPA rejection, and metadata/runtime IPA differences. The workflow must pass on the exact current head before the new filtered wheel is marked verified. See [FastThaiG2P data provenance and redistribution review](fastthaig2p-data-provenance.md).

## Public Pages deployment gate

`data/third_party/fastthaig2p-browser-bundle.json` remains `redistribution_approved: false`.

The remaining legal/evidence work is specific:
- publish Wiktionary/Kaikki attribution and the filtered derived dataset under the applicable CC BY-SA/GFDL terms;
- establish the exact TLTK release/commit used for the vendored fallback files and reconcile its file-level license notices;
- include FastThaiG2P, PyThaiNLP, Pyodide, tzdata, TLTK, and retained corpus license/NOTICE material in the public bundle;
- verify the exact public bundle file/hash manifest.

The Pages workflow builds the runtime only when `FASTTHAIG2P_PYODIDE_BUNDLE_READY=true`, and the builder independently refuses `--purpose pages` unless the rights manifest says `redistribution_approved=true`. The deploy job is also gated on the repository variable. CI uses ephemeral assets and does not grant public redistribution permission.

No deployment, main-branch change, merge, or repository setting change was made. PR #210 remains open and unmerged. The branch's static preview was tested in Chromium, but a real GitHub Pages URL has not yet been deployed or measured.

## Current acceptance ledger

| Area | Criterion | Status |
|---|---|---|
| Shared service | Same Python service used by API and browser | DONE_VERIFIED |
| Pyodide runtime | Pinned pure-Python wheels import and run | DONE_VERIFIED at 8ff38629; reverify after filtered wheel |
| CPython/Pyodide parity | Complete service JSON matches | DONE_VERIFIED at 8ff38629; reverify after filtered wheel |
| Browser worker | Cold/warm Chromium run, no API/CDN text transfer | DONE_VERIFIED at 8ff38629; reverify after exact version checks |
| PyThaiNLP footprint | Unused corpus assets removed; required CC0 lists retained | DONE_VERIFIED |
| Source filtering | Generated/unknown IPA excluded from browser wheel | PARTIAL — latest workflow verification pending |
| Wiktionary/Kaikki attribution | Share-alike data notice and transparent copy | TODO |
| TLTK fallback provenance | Exact vendored release and license file mapping | BLOCKED — upstream does not record exact version; source repository contains multiple license files |
| Dependency notices | All license/NOTICE texts included in Pages artifact | TODO |
| Public Pages deployment | Exact merged main commit deployed and live-smoked | BLOCKED — rights flag false; merge and repository settings not changed |
| Performance | Actual Pages transfer/cold-start and mobile timing | TODO |

## Product and linguistic limits

This is a runtime-port milestone, not a linguistic validation result. Independent IPA gold remains 0; accuracy remains `NOT_MEASURED`; Ukrainian practical forms remain provisional. No TTS, audio, acoustic validation, or external expert review is required for the owner-approved beta scope.
