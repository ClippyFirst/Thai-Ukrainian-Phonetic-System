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

The finite correction/abstention layer in `web/src/rtgs-reference.js` is maintained by ClippyFirst and is not copied from PyThaiNLP. The word-level RTGS forms are documented with source links in `docs/research/thai-romanization-integration.md`; the orthographic correction for preposed vowels is separately identified. The PyThaiNLP algorithm port remains under the Apache-2.0 notice above.


## ClippyFirst RTGS correction data

The finite correction/abstention layer in `web/src/rtgs-reference.js` is maintained by ClippyFirst and is not copied from PyThaiNLP. The word-level RTGS forms and source scope are documented in `docs/research/thai-romanization-integration.md`; the preposed-vowel and lexical exception handling is separately identified. The PyThaiNLP algorithm port remains under the Apache-2.0 notice above.
