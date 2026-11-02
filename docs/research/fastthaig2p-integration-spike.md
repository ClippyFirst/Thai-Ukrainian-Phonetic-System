# FastThaiG2P integration spike

**Status: experimental comparator; not enabled in the core runtime.**

## Implementation contract

The spike exposes a lazy optional `FastThaiG2PAdapter` in `src/thai_ukrainian/fastthaig2p_adapter.py`, which wraps the upstream public Python API `fastthaig2p.G2P().convert(text)` and runs it against the same frozen 42-item challenge file as ClippyFirst. It records the untouched upstream string, slash-delimited word groups, dot-delimited syllables, dictionary-hit/OOV fallback counts, non-IPA passthrough text, complete-IPA coverage and per-engine wall-clock diagnostics. A response with any non-IPA passthrough is not counted as complete IPA.

FastThaiG2P output is **not** promoted into ClippyFirst's phonemic or broad-surface IPA fields. The typed-boundary continuation adds `FastThaiG2POutput.to_phonetic_results()`, returning one `PhoneticResult` per syllable while retaining upstream word grouping. It extracts the five documented Chao contours into separate tone metadata, preserves segmental length/aspiration/unreleased-stop/affricate/glide features in typed segments, and rejects partial passthrough or unsupported fallback sentinels. Because the upstream convention does not establish whether the mixed dictionary/fallback outputs are phonemic or broad-surface IPA, both IPA-layer string fields remain unset and supported segments are marked `UNCERTAIN`. The existing Ukrainian adapter therefore withholds output. This is a diagnostic typed bridge, not production promotion.

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
| Vendored TLTK fallback parser | The pinned upstream `fastthaig2p/_th2ipa.py` carries a BSD 3-Clause notice and 2018 Chulalongkorn University copyright | Preserve all three conditions and disclaimer if this file is ever copied or modified. This spike does not copy it. |
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


## First paired challenge result — 2026-11-02

**Dedicated comparison CI: PASSED on the pre-extra code head.** Workflow run [41438311972](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41438311972) ran against code head `e924063176d2d7402d98555642e86c0ce4f72077`; its artifact is [fastthaig2p-challenge-comparison](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41438311972/artifacts/13138026677), archive SHA-256 `6ce3489280b56ad00a4e960a6e4ef66526ec110e5e5c88a797f907c879cf139c`. Full repository CI on that same code head passed all three jobs in [41438312216](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41438312216). A subsequent workflow-only change now installs the dependency via the declared optional extra; its exact-head verification is pending.

| Diagnostic | ClippyFirst | FastThaiG2P |
|---|---:|---:|
| Complete/non-empty outputs | 28/42 | 42/42 |
| Median per-input time | 0.390 ms | 0.074 ms |
| p95 per-input time | 1.894 ms | 1.754 ms |

FastThaiG2P produced complete IPA for all 42 inputs with no non-IPA passthrough in this challenge. It processed 50 upstream tokens: 45 dictionary hits and 5 OOV rule-fallback tokens. There were 28 records where both systems emitted a complete result with equal syllable counts, covering 40 syllable pairs. Raw exact syllable-string agreement was 0/40 because FastThaiG2P includes Chao tone contours and uses a tie-bar convention that differs from ClippyFirst. After the explicitly limited segmental projection (remove Chao tone marks, tie bar and upstream fallback sentinel `8`, retain vowel length and other segmental symbols), 25/40 pairs matched (62.5%).

The projection mismatches include short/long vowel differences (`คอมพิวเตอร์`), glottal-stop differences (`กะ`, `บรรจุ`), coda unreleased-stop marks (`ศุกร์`, `สัตว์`, `กอล์ฟ`, `ทราบ`) and diphthong/length differences (`ครอบครัว`). These are review targets, not adjudicated errors. FastThaiG2P also emits non-empty output for both deliberately invalid-input probes and both `ฦ`-series probes where ClippyFirst abstains; more output is not necessarily more valid output.

**Interpretation:** FastThaiG2P clearly has greater output coverage and a lower median runtime on this small diagnostic, while p95 is nearly the same. The 62.5% segmental inter-engine agreement does not identify which engine is correct. Since independent gold remains zero, the question “which is more accurate?” remains `NOT_MEASURED`. No Ukrainian output is generated from FastThaiG2P in this spike.


## Additional data-rights caution

The upstream `data/fallback/` trigram/rule assets are distinct from the BSD-3-Clause source-code notice on `fastthaig2p/_th2ipa.py`; their exact source provenance and data license have not yet been verified independently. Treat this fallback data layer as unresolved rather than assuming that the top-level Apache-2.0 software license clears every bundled asset. The comparison JSON also contains per-input IPA strings that may be sourced from FastThaiG2P's mixed dictionary. The CI artifact is a temporary research diagnostic, not a redistribution-cleared pronunciation dataset; do not republish or incorporate its IPA rows into project lexicons until row-level source provenance and applicable terms are resolved.


## Optional-extra packaging correction — 2026-11-02

The adapter is now declared as a real PEP 621 optional extra in `pyproject.toml`: `fastthaig2p` pins the upstream Git commit `4e82a291b4cf2876326744c6580121e9986ad354` and PyThaiNLP `5.4.0`. The dedicated workflow installs it through `python -m pip install -e ".[dev,fastthaig2p]"`, so the acceptance test exercises the user-facing install contract rather than a hand-assembled equivalent. The resulting exact-head CI and benchmark rerun are pending; prior metrics above remain tied to the prior code head and are not silently attributed to this packaging change.


## Typed diagnostic bridge continuation — 2026-11-02

- Dedicated branch: `research/fastthaig2p-typed-ipa-boundary-20261102`, descended from the existing spike head `a05afd184a7b546f522272df8d2ddc184e4e51c2`.
- Draft stacked PR: [#186](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/186), targeting the existing spike branch so it does not duplicate PR #185's implementation.
- Added per-syllable typed diagnostics grouped by FastThaiG2P word groups. The raw upstream result remains unchanged on `FastThaiG2POutput`.
- Exact canonical Chao contours `˧`, `˨˩`, `˥˩`, `˦˥`, `˩˩˦` map to mid, low, falling, high and rising metadata respectively; the original contour string is retained.
- Segmental symbols are parsed with the repository's existing IPA inventory. Affricate tie bars are normalized only for the typed segment inventory; raw IPA remains untouched.
- The converter refuses partial/passthrough output, checks flattened syllables against word groups, and marks unknown codepoints (including the fallback sentinel `8`) unsupported.
- Neither `phonemic_ipa` nor `broad_surface_ipa` is populated. The source does not prove the IPA layer, and no expert gold exists; status is `UNCERTAIN` or `UNSUPPORTED`. The Ukrainian adapter is tested to withhold output in both cases.
- Exact-head CI and the optional comparison workflow are pending for this continuation. Local execution is not claimed.
