# IPA

The phonological reference follows a Standard Thai description with 21 onset consonant phonemes, nine core final phonemes, short/long vowels and five contrastive tones.

Phonemic categories and surface phonetic realization remain separate. Final p/t/k may be represented as unreleased surface phones where the phonetic layer requires it.

Narrow acoustic contours are not generated without empirical evidence.

## Adapter contract

The Python pipeline exposes a typed `PhoneticResult` at the phonology/adaptation boundary (`src/thai_ukrainian/phonetic_result.py`). It preserves:

- `phonemic_ipa`: the segmental phonemic string consumed by the Ukrainian adapter;
- `broad_surface_ipa`: a separate conservative surface representation, never silently substituted for phonemic IPA;
- per-segment phonemic IPA, segment kind, and aligned surface realization when alignment is safe;
- syllable boundary offsets, vowel-length category, tone category and tone contour metadata;
- rule/source provenance and uncertainty notes;
- `SUPPORTED`, `UNCERTAIN`, or `UNSUPPORTED` status.

The Python adapter in `ukrainian_adaptation.py` accepts only `PhoneticResult`. It contains no Thai grapheme, Thai vowel-ID, or Thai coda mapping. An unsupported IPA symbol causes the adapter to withhold output. Tone remains separate from segmental Ukrainian spelling; vowel length and aspiration may be neutralized only by explicit adaptation rules.

The browser implementation has its own IPA adapter and tests. It must remain aligned with the same declared mapping policy; the browser test suite alone is not evidence that the Python implementation is correct, and vice versa.

## Evidence boundary

A typed representation makes the data flow auditable; it does **not** by itself establish that a Thai reading is lexically correct. Structural validity, lexical attestation, IPA accuracy, and Ukrainian adaptation quality remain separate validation questions. The project makes no corpus-level accuracy claim until the challenge corpus is independently adjudicated and a pinned benchmark run is published.
