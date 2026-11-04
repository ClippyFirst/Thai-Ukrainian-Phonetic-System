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
- ClippyFirst integration: `src/thai_ukrainian/fastthaig2p_adapter.py` calls the pinned package; no upstream dictionary or fallback dataset is copied into this repository.
- Production gate: do not publicly deploy the FastThaiG2P endpoint until the exact pinned package's bundled data assets and applicable terms/attribution have been inspected and recorded in the integration audit.

This notice records software attribution and an explicit unresolved data-rights gate; it is not a claim that all upstream bundled data has been cleared for redistribution or commercial use.


### FastThaiG2P data-license clarification (2026-11-04)

The pinned FastThaiG2P data README attributes its Wiktionary-derived IPA subset to a kaikki.org Thai Wiktionary dump. Wiktionary entry text is published under CC BY-SA 4.0; the exact dump revision and attribution mapping used for this 13k subset have not been supplied. A distinct PyThaiNLP Thai G2P Wiktionary corpus declares CC BY-SA 3.0, but it has not been established as the exact FastThaiG2P source and must not be substituted for that missing provenance.

FastThaiG2P's vendored TLTK `_th2ipa.py` identifies version 1.3.8 and carries a BSD-3-Clause notice. PyPI describes TLTK as BSD-3-Clause since 1.2.2, but the current TLTK repository root LICENSE contains LGPL-3 text while its `setup.py` declares BSD-3-Clause. FastThaiG2P does not pin the exact TLTK revision for each fallback data asset. Treat the fallback-data license as unresolved pending an upstream source/revision and terms clarification.

The ~49k LLM-generated IPA records and manual overrides also lack a complete data-specific license/provenance statement in the pinned FastThaiG2P data README. The Apache-2.0 software license does not, by itself, clear these separate data assets. No FastThaiG2P dictionary or fallback data is copied into this repository.
