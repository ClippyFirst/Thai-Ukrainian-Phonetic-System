# Thai romanization integration research

**Status:** PARTIAL prototype on branch `feat/thai-rtgs-reference-20261028`; a separate UI panel and conservative fixture adapter exist, but the examples have not yet been verified against a pinned PyThaiNLP release. Do not treat this as a complete RTGS engine.

## Decision

The first comparison layer should be **RTGS (Royal Thai General System of Transcription)**, displayed in parallel with the existing IPA output. It must not be used to generate Ukrainian output. The existing route remains:

`Thai orthography → structural analysis → source phonology → IPA/typed result → Ukrainian adaptation`

RTGS is a separate reference rendering, not an intermediate representation. The interface must label it “RTGS (латинська романізація; не IPA)” and warn that it is lossy: it does not encode tone and does not reliably preserve vowel length or all phonemic distinctions. It is not English pronunciation spelling. In RTGS, `ph`, `th`, and `kh` conventionally represent aspirated Thai stops, not English /f/, /θ/, or English letter-name values.

ISO 11940 is not a substitute for RTGS: it is a reversible orthographic transliteration scheme, useful for inspecting character-level conversion rather than representing pronunciation. If added later, it needs its own explicitly orthographic panel.

## Implementation candidate reviewed

PyThaiNLP documents `romanize(..., engine="royin")` as an RTGS implementation and distinguishes it from phonetic engines such as `thaig2p` and `ipa`. The current PyThaiNLP project is Apache-2.0 licensed; data/models may carry separate CC0/CC-BY terms, so dependency and asset provenance must be checked separately.

- API documentation: https://pythainlp.org/docs/5.4.0/api/transliterate.html
- Current source implementation (SPDX Apache-2.0): https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/transliterate/royin.py
- Project licensing overview: https://github.com/PyThaiNLP/pythainlp

PyThaiNLP itself is Python-only, and the website is a static browser application with CSP `connect-src 'none'`. Calling a remote service is not acceptable. Before porting or packaging the algorithm, inspect its word-tokenization dependency and source version, preserve attribution/license headers, and compare outputs against a pinned PyThaiNLP release over a reviewed fixture corpus. A direct transliteration of each arbitrary Thai substring without word segmentation would not be equivalent to the reference implementation.

## Acceptance gates

1. Pin an immutable PyThaiNLP release/tag and review the RTGS source plus tokenizer dependency/license.
2. Implement or bundle a browser-compatible, offline RTGS adapter; no runtime API/network calls.
3. Ensure the adapter's inputs/outputs are independent from `adaptIpaToUkrainian`; only the IPA result may reach the Ukrainian adapter.
4. Build a versioned parity fixture corpus from reviewed Thai words, including aspirated-stop examples and known RTGS edge cases. Compare browser results with the pinned reference implementation. Do not assert parity without running the reference.
5. Tests currently cover the provisional fixture adapter, unknown/non-Thai input, and separate UI presentation. Remaining: Unicode marks, broader token-boundary cases, and a reference-parity corpus against the pinned release.
6. Run the existing web UI, engine, parity, Python, artifact-drift and deployment checks. Do not claim general linguistic accuracy from romanization parity.
7. Only then expose the RTGS field in the website. If a word's boundaries are not known, show a warning or per-token result rather than inventing spaces.

## Source notes

- PyThaiNLP docs demonstrate that RTGS and IPA are distinct engines and that outputs can differ (e.g. `สามารถ`: RTGS `samant` vs IPA-oriented engines returning phonetic forms).
- ISO 11940: https://www.iso.org/standard/20574.html
- UK BGN/PCGN romanization reference: https://assets.publishing.service.gov.uk/media/5ab4e60aed915d78b9a459f5/ROMANIZATION_OF_THAI.pdf

## Current blockers

- The repository's website has no Python runtime and deliberately prohibits network connections.
- Browser-port/tokenizer compatibility and reference parity have not yet been implemented or tested.
- Independent Thai IPA and Ukrainian target-form gold remain separate research gaps; RTGS does not resolve those gaps.
