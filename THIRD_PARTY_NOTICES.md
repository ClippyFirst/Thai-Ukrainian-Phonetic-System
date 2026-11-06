# Third-party notices

## PyThaiNLP RTGS (`royin`) algorithm port

- Upstream project: PyThaiNLP Project
- Pinned upstream release: `v5.4.0` (release commit `7f26adf5ce09c3d77c39ca2ef86f7138e9071088`)
- Source file: https://github.com/PyThaiNLP/pythainlp/blob/v5.4.0/pythainlp/transliterate/royin.py
- License: Apache License 2.0
- License text: [licenses/Apache-2.0-PyThaiNLP.txt](licenses/Apache-2.0-PyThaiNLP.txt)
- Ported component: the RTGS per-token vowel/consonant conversion and syllable-separator logic in `web/src/rtgs-reference.js`.
- Not ported: PyThaiNLP's `newmm` word tokenizer and its dictionary. ClippyFirst token boundaries may differ from the reference package's boundaries.
- Runtime: the website does not import PyThaiNLP, download models, or make network requests. PyThaiNLP 5.4.0 is installed in CI only as a parity oracle.

Copyright 2016-2026 PyThaiNLP Project. The copied/ported algorithm is provided under Apache-2.0; see the full license text linked above.


## ClippyFirst RTGS correction data

The finite correction/abstention layer in `web/src/rtgs-reference.js` is maintained by ClippyFirst and is not copied from PyThaiNLP. The word-level RTGS forms and source scope are documented in `docs/research/thai-romanization-integration.md`; the preposed-vowel and lexical exception handling is separately identified. The PyThaiNLP algorithm port remains under the Apache-2.0 notice above.


## Thai Wiktionary-derived lexical IPA records

- Upstream source: Thai Wiktionary contributors; the compound entry for **ตะวันออก** is taken from English Wiktionary.
- License: [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
- Pinned source revisions used by the current runtime override registry (`data/thai/lexical_ipa_overrides.tsv`):
  - [เงิน — revision 5759179](https://th.wiktionary.org/w/index.php?title=เงิน&oldid=5759179)
  - [เดิน — revision 1908803](https://th.wiktionary.org/w/index.php?title=เดิน&oldid=1908803)
  - [ตะวันออก — revision 86398986](https://en.wiktionary.org/w/index.php?title=ตะวันออก&oldid=86398986) (the syllable-level record for **ออก** is derived from this compound entry)
  - [ไกล — revision 5688545](https://th.wiktionary.org/w/index.php?title=ไกล&oldid=5688545)
  - [ใกล้ — revision 5721860](https://th.wiktionary.org/w/index.php?title=ใกล้&oldid=5721860)
  - [เพิ่ง — revision 1885200](https://th.wiktionary.org/w/index.php?title=เพิ่ง&oldid=1885200)
- Adaptation: selected dictionary IPA, tone and vowel-length fields are normalized into a tab-separated data registry and mirrored in the browser runtime. Each row retains its source ID, revision locator and license. These records are explicitly marked source-attested and not independently adjudicated or acoustic gold; the repository does not claim that dictionary transcription is an audio measurement.
- The broader curated text-lexicon subset is documented separately in [`data/thai/TEXT-LEXICON-DATA-LICENSE.md`](data/thai/TEXT-LEXICON-DATA-LICENSE.md).
- The MIT license applies to project software, not to these separately attributed data records. The CC BY-SA 4.0 terms continue to apply to the adapted Wiktionary-derived data.

## FastThaiG2P website runtime dependency

- Upstream project: [awslabs/FastThaiG2P](https://github.com/awslabs/FastThaiG2P)
- Pinned upstream commit: `4e82a291b4cf2876326744c6580121e9986ad354`
- Upstream software license: Apache License 2.0; preserve upstream copyright, license and NOTICE files as applicable.
- Runtime dependency: PyThaiNLP `5.4.0`, software license Apache-2.0.
- Upstream fallback parser `_th2ipa.py`: upstream identifies a BSD 3-Clause notice and 2018 Chulalongkorn University copyright. The upstream package is installed as a dependency; this repository does not copy that source file.
- Bundled runtime data: upstream `data/README.md` identifies a 62k-word dictionary; `ipa.json` is merged from manual overrides, approximately 13k Wiktionary/kaikki entries and approximately 49k LLM-generated entries. The generated source JSON is gitignored upstream. The upstream build force-includes `data/dict.txt`, `data/ipa.json` and `data/fallback/` in its wheel. The data README does not provide one comprehensive license statement for all runtime data assets.
- Fallback source: upstream identifies the fallback data as vendored from TLTK; `fastthaig2p/_th2ipa.py` carries a BSD 3-Clause notice and 2018 Chulalongkorn University copyright. This code is installed as part of the upstream dependency and is not copied here.
- Dictionary/data limitation: Apache-2.0 for the upstream software does not by itself establish rights for every bundled manual, Wiktionary-derived, generated IPA, dictionary and fallback data record. Exact terms, provenance, attribution and share-alike obligations remain under review.
- ClippyFirst integration: `src/thai_ukrainian/fastthaig2p_adapter.py` still calls the pinned package for the production Pyodide path. The browser-native build additionally copies only the 13,144-entry subset labelled `source=wiktionary`, with the matching filtered tokenizer wordlist; generated, manual and unknown-source IPA entries are excluded. The native build includes `browser-data-provenance.json` and `WIKTIONARY-ATTRIBUTION.md` alongside the data, and records CC BY-SA 4.0 in its native manifest.
- PyThaiNLP browser data: the native build includes `pythainlp/corpus/words_th.txt` from pinned PyThaiNLP 5.4.0 for default newmm/mai yamok tokenization. The wheel's `corpus_license.md` declares CC0; the native manifest records CC0-1.0 and the entry count.
- Native code ports: the FastThaiG2P normalizer is adapted from the pinned Apache-2.0 upstream source; the newmm tokenizer is adapted from PyThaiNLP 5.4.0 under Apache-2.0. Existing upstream license/NOTICE files remain bundled.
- No TLTK fallback code or fallback pickle/data files are copied into the native bundle. OOV remains fail-closed in the native Worker.
- Production gate: the public app continues to use the verified Pyodide worker. A complete native cutover remains gated on a lawful, source-verified TLTK fallback port, full OOV/typed-result parity, and browser/mobile/offline/performance acceptance.

This notice records software attribution and an explicit unresolved data-rights gate; it is not a claim that all upstream bundled data has been cleared for redistribution or commercial use.


### FastThaiG2P data-license clarification (2026-11-04)

The pinned FastThaiG2P data README attributes its Wiktionary-derived IPA subset to a kaikki.org Thai Wiktionary dump. Wiktionary entry text is published under CC BY-SA 4.0; the exact dump revision and attribution mapping used for this 13k subset have not been supplied. A distinct PyThaiNLP Thai G2P Wiktionary corpus declares CC BY-SA 3.0, but it has not been established as the exact FastThaiG2P source and must not be substituted for that missing provenance.

FastThaiG2P's vendored TLTK `_th2ipa.py` identifies version 1.3.8 and carries a BSD-3-Clause notice. Exact PyPI 1.3.8 metadata declares BSD-3-Clause, records release date 2021-04-23 and sdist SHA-256 `f803e9f2e3e16b1f8abba4da4889f6b94bd706c5c519e2be8382178446da4159`; its description says the package license changed to New BSD from 1.2.2 and describes commercial use. TLTK `setup.py` declares BSD-3-Clause and lists fallback data files; `MANIFEST.in` includes `LICENSE.txt`, which is BSD-3-Clause. The repository root also contains an LGPL-3 `LICENSE`, PyPI's JSON has no `license_files` metadata, and the exact 1.3.8 sdist bytes were not inspected. Several fallback filenames correspond to TLTK package data, but no per-file hash/source mapping or third-party corpus clearance is complete. **Disposition: PARTIAL package-level BSD-3 evidence; fallback asset rights remain unresolved pending exact sdist/file and corpus-term review.**

The ~49k LLM-generated IPA records and manual overrides also lack a complete data-specific license/provenance statement in the pinned FastThaiG2P data README. The Apache-2.0 software license does not, by itself, clear these separate data assets. No FastThaiG2P dictionary or fallback data is copied into this repository.


### TLTK 1.3.8 package-level evidence (2026-11-04)

Primary package/source references:
- [PyPI TLTK 1.3.8 release metadata](https://pypi.org/pypi/tltk/1.3.8/json) — BSD-3-Clause, source archive SHA-256 `f803e9f2e3e16b1f8abba4da4889f6b94bd706c5c519e2be8382178446da4159`, uploaded 2021-04-23.
- [TLTK README](https://github.com/attapol/tltk/blob/master/README.rst) — says the package license changed to New BSD (BSD-3-Clause) from 1.2.2 and describes commercial use.
- [TLTK setup.py](https://github.com/attapol/tltk/blob/master/setup.py) — declares BSD-3-Clause and enumerates package data files.
- [TLTK MANIFEST.in](https://github.com/attapol/tltk/blob/master/MANIFEST.in) — explicitly includes `LICENSE.txt`.
- [TLTK LICENSE.txt](https://github.com/attapol/tltk/blob/master/LICENSE.txt) — BSD-3-Clause; [repository LICENSE](https://github.com/attapol/tltk/blob/master/LICENSE) is LGPL-3.

The package-level evidence narrows the license ambiguity, but the exact 1.3.8 sdist contents and byte-level mapping to each FastThaiG2P fallback asset were not retrieved/verified. Do not treat this as blanket asset-level clearance.


### Browser-native FastThaiG2P assets (2026-11-06)

The native front-half is a JavaScript/TypeScript port, not a Python runtime. Its same-origin data assets are:
- `fastthaig2p-ipa.json`: 13,144 Wiktionary-labelled IPA records only; CC BY-SA 4.0; generated/manual/unknown entries excluded.
- `fastthaig2p-normalizer.json`: constant maps extracted from the pinned FastThaiG2P normalizer source; FastThaiG2P software license Apache-2.0.
- `pythainlp-default-words.txt`: PyThaiNLP 5.4.0 default wordlist; CC0-1.0.
- `browser-data-provenance.json`: source filter counts, upstream pin, license and accuracy disclaimer.
- `manifest.json`: asset paths, SHA-256, byte sizes, source pins and license metadata.

The native Worker verifies SHA-256 and byte sizes before parsing its runtime assets. It does not request Pyodide, Python, wheels, WASM or a remote API. The TLTK fallback assets are intentionally absent pending exact file-level source-distribution verification; see the TLTK 1.3.8 evidence below.
