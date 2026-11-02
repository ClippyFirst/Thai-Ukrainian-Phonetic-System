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

## Optional FastThaiG2P comparator dependency (not vendored)

- Upstream: [awslabs/FastThaiG2P](https://github.com/awslabs/FastThaiG2P)
- Pinned comparator commit: `c4759eef7df03e11fcbb9aa83efe8cf21709fd2f` (`fastthaig2p==0.1.0`).
- Software license: Apache License 2.0; upstream NOTICE attributes Amazon.com, Inc. or its affiliates. The package is an optional Python dependency and is not copied into this repository or imported by the default runtime.
- Runtime dependency: `pythainlp>=5.3.4`; FastThaiG2P requires Python >=3.11. The optional extra is pinned in `pyproject.toml`.
- Data is not covered by a blanket software-license conclusion. Upstream describes a 62,112-word IPA dictionary merged from manual overrides, Wiktionary-derived records and approximately 49k generated records. The Wiktionary source is identified as CC BY-SA 3.0 by the NLP for Thai corpus catalogue; generated IPA has no distinct dataset license in the inspected pinned repository; manual overrides have no separate data-license statement there.
- The fallback's vendored `fastthaig2p/_th2ipa.py` contains a BSD 3-Clause notice for Chulalongkorn University's Department of Linguistics. The fallback statistical/lexical data files are described as vendored TLTK data, but no per-file license/provenance manifest was found in the pinned repository.
- ClippyFirst does not redistribute the upstream dictionary, IPA JSON, source dumps or fallback data. Do not copy these assets into this repository unless row/file-level rights and attribution are verified.

See [the integration spike license register](docs/fastthaig2p-integration-spike.md) for inspected layers, sources and unresolved data questions.
