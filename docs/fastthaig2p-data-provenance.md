# FastThaiG2P browser data provenance and redistribution review

**Scope:** the exact FastThaiG2P source pin used by the browser/WASM port:
`4e82a291b4cf2876326744c6580121e9986ad354`.

## Upstream source composition

The pinned upstream `data/README.md` describes:
- `dict.txt`: a 62k-word runtime word list used for tokenization and IPA lookup;
- `ipa.json`: a flat runtime lookup merged from Wiktionary and generated IPA;
- `ipa_metadata.json`: per-word source metadata used for auditing;
- `data/fallback/`: TLTK-derived OOV syllable parser data.

The upstream `scripts/merge_ipa.py` defines source priority as manual > Wiktionary > generated. The source metadata records the source category but no explicit per-entry license field. The runtime wheel includes the merged `ipa.json` and `dict.txt`, but not the audit metadata.

## Source-filtered browser wheel — verified

`scripts/prepare_fastthaig2p_browser_source.py` prepares a dedicated browser wheel from the pinned source checkout:
1. Reads `ipa_metadata.json`, `ipa.json` and `dict.txt`.
2. Retains only records explicitly labelled `wiktionary`.
3. Excludes model-generated, manual and unknown/missing source records.
4. Requires a valid slash-delimited IPA value for every retained record.
5. Reduces the tokenizer wordlist to exactly the retained IPA keys, preserving upstream word order.
6. Reports stale differences between `ipa.json` and the IPA snapshot in `ipa_metadata.json` without silently changing the source label.
7. Embeds `browser-data-provenance.json` and `WIKTIONARY-ATTRIBUTION.md` inside the FastThaiG2P wheel.

**Measured pinned-source counts (CI run 42073702543):**

| Source class | Before filter | Browser wheel |
|---|---:|---:|
| Wiktionary | 13,144 | 13,144 |
| Model-generated | 48,957 | 0 |
| Manual | 0 in runtime metadata | 0 |
| Unknown/missing | 0 in runtime metadata | 0 |
| **Total retained IPA records** | **62,101** | **13,144** |

The tokenizer wordlist is also reduced to 13,144 keys. One entry, `สวน`, has a runtime IPA value that differs from the IPA snapshot in `ipa_metadata.json`; the source label is still Wiktionary. The build preserves the runtime IPA string and records this single metadata mismatch explicitly. This is a provenance discrepancy, not a linguistic correction or an accuracy claim.

The upstream TLTK-derived OOV fallback remains enabled. It is not replaced by an invented JavaScript or Ukrainian fallback.

### Exact CI evidence

- [Pyodide compatibility, filtered wheel, and Chromium worker smoke — 42073702543](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42073702543) — **SUCCESS**.
- [Full CI — 42073702565](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42073702565) — **SUCCESS**, including Python tests, registry/data validation, browser contracts and master artifact.
- [Web static validation — 42073702564](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42073702564) — **SUCCESS**.
- [FastThaiG2P Site API reference wrapper — 42073702559](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42073702559) — **SUCCESS**.
- [Optional external FastThaiG2P smoke — 42073702598](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42073702598) — **SUCCESS**.

The Pyodide run verified four Thai inputs against the same CPython service response, then ran the real same-origin Web Worker in Chromium. The browser test passed cold initialization and warm analysis, checked the `สวน` IPA regression, and confirmed no `/api/analyze` or CDN request.

### Runtime footprint

The verified CI bundle contains:
- 4 pure-Python wheels: **7,823,799 bytes** total;
- FastThaiG2P filtered wheel: **6,317,099 bytes**;
- 14 self-hosted Pyodide runtime files: **12,610,023 bytes**;
- 10 license/NOTICE files: **57,389 bytes**;
- combined raw bundle/notice footprint: **20,491,211 bytes** before HTTP compression.

PyThaiNLP 5.4.0's wheel was trimmed from 67,689,272 to 3,648,217 uncompressed member bytes by removing 37 unused corpus assets (64,041,055 bytes). The browser wheel retains Python source, `words_th.txt`, `stopwords_th.txt`, and the corpus license notice. Both retained corpus lists are CC0-1.0.

The build manifest records exact package versions, wheel sizes and SHA-256 hashes, Pyodide runtime file hashes, and the ten license/attribution notice hashes. The browser worker checks the exact wheel versions, filenames, sizes and SHA-256 values before installing them.

## Source and license evidence

### Wiktionary-derived records

- FastThaiG2P source documentation identifies `wiktionary_ipa.json` as a roughly 13k-entry extraction from kaikki.org.
- Kaikki's Thai Wiktionary data page says its extracted data is available under the same licenses as Wiktionary: CC BY-SA and GFDL.
- Wiktionary's copyright page identifies CC BY-SA 4.0 and GFDL as the dual licenses for original entry text.

Sources:
- https://github.com/awslabs/FastThaiG2P/blob/4e82a291b4cf2876326744c6580121e9986ad354/data/README.md
- https://github.com/awslabs/FastThaiG2P/blob/4e82a291b4cf2876326744c6580121e9986ad354/scripts/merge_ipa.py
- https://kaikki.org/thwiktionary/index.html
- https://en.wiktionary.org/wiki/Wiktionary:Copyrights

The filtered pronunciation data is a modified subset of Wiktionary-derived records. Attribution is to Wiktionary contributors and Kaikki.org/Wiktextract. The build excludes generated/manual/unknown-source records, reduces the tokenizer wordlist to retained IPA keys, and preserves one current runtime IPA value that differs from the audit snapshot. The filtered data is labelled CC BY-SA 4.0, and the wheel embeds the attribution and build provenance. The public notices page links to the license and source. This is a source-based compliance assessment, not legal advice.

### Manual and model-generated records

Manual and model-generated records are excluded from the browser wheel. The pinned upstream repository says the generated layer contains roughly 49k IPA entries produced with Claude Opus 4.6. Its per-record redistribution provenance is not established here. Excluding this layer avoids representing it as Apache-only or silently relicensing it. No manual records are present in the pinned runtime metadata count; manual source labels are excluded if they appear in a future upstream snapshot.

### TLTK-derived fallback

The pinned FastThaiG2P README and data README say the OOV fallback is vendored from TLTK.

- FastThaiG2P's vendored `fastthaig2p/_th2ipa.py` header explicitly identifies **TLTK version 1.3.8** and includes a BSD-3-Clause notice.
- The PyPI TLTK 1.3.8 release page identifies BSD-3-Clause; the TLTK `LICENSE.txt` also contains BSD-3-Clause terms.
- Five of the six fallback data files have identical Git blob SHA values to the matching files in the public `attapol/tltk` repository.
- The sixth file, FastThaiG2P's `sylform_var.pkl`, is byte-identical to `bz2.decompress(TLTK/tltk/sylform_var.pklz)`. The exact transform is reproduced and asserted by `scripts/verify_tltk_fallback_provenance.py`.
- The TLTK repository also contains a separate root `LICENSE` file for LGPL-3.0 and an older `PKG-INFO` with GPLv3 metadata. The release-specific PyPI page and vendored source header support BSD-3-Clause for TLTK 1.3.8, but the separate repository file remains disclosed rather than silently ignored.

Sources:
- https://pypi.org/project/tltk/1.3.8/
- https://pypi.org/project/tltk/
- https://github.com/attapol/tltk
- https://github.com/awslabs/FastThaiG2P/blob/4e82a291b4cf2876326744c6580121e9986ad354/fastthaig2p/_th2ipa.py
- https://github.com/awslabs/FastThaiG2P/blob/4e82a291b4cf2876326744c6580121e9986ad354/data/README.md

The BSD-3-Clause and LGPL-3.0 repository license texts are both retained in the browser notices directory. The remaining evidence item is the exact source transformation for `sylform_var.pkl`; it is not a reason to misstate the TLTK 1.3.8 code header or PyPI license metadata.

### Other runtime dependencies

- FastThaiG2P software: Apache-2.0, pinned upstream commit above, with Amazon NOTICE.
- PyThaiNLP 5.4.0 software: Apache-2.0. Only the Python package source and two CC0 corpus lists remain in the browser wheel.
- Pyodide 0.29.5: MPL-2.0.
- tzdata 2026.6: Apache-2.0.
- This project: MIT.
- The ten notice files are staged in `web/licenses/`; the bundle builder requires them and records their hashes. The third-party notices page is linked from both primary web pages.

## Public Pages gate and acceptance ledger

`data/third_party/fastthaig2p-browser-bundle.json` deliberately remains `redistribution_approved: false`. The CI bundle is ephemeral; passing parity does not itself grant public redistribution permission.

| Criterion | Status |
|---|---|
| Per-entry Wiktionary-only filter | DONE_VERIFIED — 13,144 retained; 48,957 generated excluded |
| Source-filtered IPA and tokenizer dictionary parity | DONE_VERIFIED — 4 CPython/Pyodide inputs |
| Stale metadata discrepancy disclosed | DONE_VERIFIED — one mismatch, `สวน` |
| Generated/manual/unknown records excluded | DONE_VERIFIED |
| TLTK fallback asset provenance | DONE_VERIFIED — TLTK 1.3.8 header; five byte-identical assets and one exact bzip2 decompression; CI 42085653176 |
| TLTK license scope | PARTIAL — BSD-3-Clause package/header evidence and separate root LGPL-3.0 repository notice both retained pending final file-level review |
| Third-party license/NOTICE files staged and hashed | DONE_VERIFIED — 10 files |
| Transparent filtered dataset ZIP | DONE_VERIFIED — 194,745 bytes; five expected members and 13,144-entry provenance asserted in CI 42086644531 |
| Public Pages bundle refused while rights flag is false | DONE_VERIFIED |
| Public Pages deployment/live smoke | BLOCKED — no merge or deployment; rights flag remains false and owner approval is pending |
| Live Pages transfer and mobile cold-start performance | TODO — requires public deployment |

The Pages workflow is configured to refuse a public bundle unless the rights manifest and explicit repository variable approve publication. No deployment, merge, main-branch change, release tag or repository setting change was made.

**No accuracy claim:** source filtering does not establish pronunciation correctness. Independent IPA gold remains 0; accuracy remains `NOT_MEASURED`; Ukrainian practical forms remain provisional.
