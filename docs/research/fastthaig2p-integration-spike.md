# FastThaiG2P integration spike

**Status: experimental comparator; not enabled in the core runtime.**

## Implementation contract

The spike uses the upstream public Python API `fastthaig2p.G2P().convert(text)` and runs it against the same frozen 42-item challenge file as ClippyFirst. It records the untouched upstream string, slash-delimited word groups, dot-delimited syllables, dictionary-hit/OOV fallback counts, output coverage and per-engine wall-clock diagnostics.

FastThaiG2P output is **not** silently promoted into ClippyFirst's typed `PhoneticResult`. The upstream output contains Chao tone contours while ClippyFirst exposes phonemic IPA and separate tone metadata. A convention-aware, feature-preserving conversion plus dedicated tests is required before the external output may enter the shared IPA-to-Ukrainian adapter. This spike therefore does not emit Ukrainian output from FastThaiG2P and does not alter the production path.

Run in a clean Python 3.11+ environment:

```bash
python -m pip install "git+https://github.com/awslabs/FastThaiG2P.git@4e82a291b4cf2876326744c6580121e9986ad354"
python scripts/run_fastthaig2p_challenge.py
pytest -q tests/test_fastthaig2p_challenge.py
```

The report is written to `reports/fastthaig2p-challenge-comparison.json`. It is generated output and should be retained as a CI artifact, not committed as if it were a gold dataset.

## Interpretation

- Coverage, dictionary hit rate and OOV fallback count measure availability, not correctness.
- Exact syllable-string agreement is only inter-engine agreement. The two systems currently use different IPA conventions, so the report deliberately does not label it accuracy.
- Latency is a same-process diagnostic, not a controlled benchmark; initialization and environment differences matter.
- The challenge file currently contains no independently adjudicated IPA, tone, vowel-length or word/syllable-boundary labels. Accuracy and error rates against gold remain `NOT_MEASURED`.
- The challenge is a hand-selected adversarial set, not a representative sample of Thai text.

## License and provenance by layer

| Layer | Evidence currently verified | Conditions / unresolved points |
|---|---|---|
| FastThaiG2P Python implementation | Upstream `LICENSE` is Apache-2.0; pinned commit `4e82a291b4cf2876326744c6580121e9986ad354` | Preserve license and any NOTICE/attribution; check exact vendored file notices before redistributing modified source. |
| PyThaiNLP runtime dependency | Upstream FastThaiG2P declares `pythainlp>=5.3.4`; PyThaiNLP software is Apache-2.0 | Runtime dependency is installed separately; its corpus/model assets have their own licenses and are not automatically covered by its software license. |
| Vendored TLTK fallback parser | FastThaiG2P README identifies the fallback as TLTK-derived | Preserve the upstream file-level license/notice. Exact file-level notice and license text must be confirmed before copying or modifying that parser in this repository. |
| FastThaiG2P word dictionary / IPA data | Upstream README describes 62,112 entries: manual overrides, ~13k Wiktionary-derived and ~49k LLM-generated entries | Apache-2.0 software license does not, by itself, establish the rights or provenance of every data row. Wiktionary-derived entries need attribution/share-alike analysis; generated entries need upstream provenance/terms review. Do not copy the dictionary into this repository. |
| ClippyFirst software | MIT | MIT covers project code, not separately licensed datasets or third-party data. |
| ClippyFirst lexical IPA data | CC BY-SA 4.0 for the identified Wiktionary-derived records | Keep existing attribution and share-alike notices. Do not merge FastThaiG2P data into this registry without row-level provenance and license review. |
| Challenge corpus | Project-authored prompts; gold labels currently absent | Inputs are evaluation prompts, not pronunciation evidence. No external corpus annotations are bundled by this spike. |

The upstream Apache-2.0 code license is not the only license question: the dictionary and vendored fallback parser are separate provenance layers. This spike installs the pinned upstream package for execution and does not redistribute its dictionary or fallback data as ClippyFirst assets.

## Acceptance gates before production adapter promotion

1. Obtain independent expert IPA and boundary labels for a frozen subset, with source/license metadata.
2. Specify a lossless conversion from Chao tone contours and upstream IPA symbols into the existing typed IPA model; reject unsupported or ambiguous strings.
3. Test tone, vowel length, aspiration, unreleased stops, affricate tie bars, glottal stops, syllable and word boundaries, and OOV behavior.
4. Route only the validated typed result through the existing IPA-to-Ukrainian adapter; never create a parallel Thai-grapheme-to-Ukrainian path.
5. Recheck upstream commit, package hashes, notices and data provenance before any bundled distribution.
