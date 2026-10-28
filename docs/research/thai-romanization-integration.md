# Thai romanization integration research

**Status:** PARTIAL — the offline browser port and pinned-reference parity test are implemented, but CI has not completed successfully on the latest head yet. Word-tokenizer parity is explicitly not claimed.

## Decision and pipeline boundary

RTGS (Royal Thai General System of Transcription) is displayed as a parallel Latin reference, never as input to Ukrainian adaptation. The main route remains:

`Thai orthography → structural analysis → source phonology → IPA/typed result → Ukrainian adaptation → Ukrainian practical orthography`

RTGS is lossy: it does not encode tone and does not reliably preserve vowel length or all phonemic distinctions. It is not English pronunciation spelling. In RTGS, `ph`, `th`, and `kh` conventionally represent aspirated Thai stops, not English /f/, /θ/, or English letter-name values.

ISO 11940 is not a substitute: it is a reversible orthographic transliteration scheme, not a pronunciation transcription. If added later, it requires its own explicitly orthographic panel.

## Implementation and provenance

- Upstream: PyThaiNLP `v5.4.0`, `pythainlp/transliterate/royin.py`, release published 2026-10-09; immutable release commit `7f26adf5ce09c3d77c39ca2ef86f7138e9071088`; pinned in CI as `pythainlp==5.4.0`.
- Reference source: https://github.com/PyThaiNLP/pythainlp/blob/v5.4.0/pythainlp/transliterate/royin.py
- API documentation: https://pythainlp.org/docs/5.4.0/api/transliterate.html
- License: Apache-2.0; attribution and license text are included in `THIRD_PARTY_NOTICES.md` and `licenses/Apache-2.0-PyThaiNLP.txt`.
- The browser implementation ports the vowel rules, consonant mapping, normalization, `รร` handling, and the reference syllable-separator rule. It also applies a narrowly scoped orthographic correction for preposed vowels in ห นำ clusters (e.g. ใหม่/ไหม → `mai`, เหงา → `ngao`), because blindly applying the upstream per-token pattern order can misorder the vowel.
- The static website has no runtime dependency on Python, external APIs, model downloads, or network calls. PyThaiNLP is a CI-only oracle.

## Parity corpus and what it proves

`docs/research/rtgs-parity-corpus.json` is a versioned list of token inputs and pre-segmented token sequences. `scripts/test_rtgs_parity.py` invokes the browser implementation under Node and compares results with the private per-token `_romanize` and `_should_add_syllable_separator` functions from pinned PyThaiNLP 5.4.0. CI must pass this test before parity can be called verified.

This is **algorithm parity for supplied token boundaries except the explicitly tested ห นำ orthographic corrections**, not:
- parity with PyThaiNLP's default `newmm` tokenizer or its dictionary;
- proof that either system has the correct segmentation for every Thai sentence;
- an independent IPA, acoustic, or Ukrainian-transcription accuracy benchmark.

The website currently passes token boundaries from ClippyFirst's own analyzer. As a result, a phrase may receive different spaces or RTGS context behavior than PyThaiNLP's full `romanize(text)` function. The UI calls this out rather than silently claiming full package equivalence.

## Acceptance gates

1. [x] Pin a released upstream implementation and preserve license attribution.
2. [x] Implement the per-token RTGS algorithm as an offline browser adapter.
3. [x] Keep RTGS separate from the IPA → Ukrainian adapter.
4. [x] Add a versioned corpus and CI comparison against the pinned upstream implementation.
5. [ ] Verify the full CI run on the final branch head, including the reference parity test.
6. [ ] Review the documented ห นำ correction against an authoritative Thai orthography/RTGS reference and expand lexical edge-case coverage before claiming standards-level completeness.
7. [ ] Decide whether to port or bundle a compatible Thai word tokenizer and dictionary, or keep the documented ClippyFirst-token-boundary contract.
8. [ ] Run browser visual/accessibility checks and confirm deployment/build behavior before promoting the feature out of draft.

## Remaining independent research gaps

- Independent Thai IPA adjudication and Ukrainian target-form review remain separate research requirements; RTGS parity does not resolve them.
- If full PyThaiNLP behavior is required, tokenizer and dictionary provenance/licensing must be inspected separately and parity measured on a reviewed sentence corpus.
- No general accuracy claim should be inferred from passing algorithm parity.
