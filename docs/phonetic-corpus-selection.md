# Thai phonetic corpus selection

**Checkpoint:** 2026-11-01. This is a source-selection decision, not a gold dataset. No third-party audio or labels are bundled.

## What the benchmark must measure

The target evidence layers are separate:

1. Thai orthographic word segmentation and lexical reading.
2. Syllable boundaries and broad phonemic IPA.
3. Lexical tone category, vowel length and final glottal status.
4. Broad surface/narrow acoustic IPA only where a licensed recording and time-aligned asset are available.
5. Ukrainian practical transcription conditional on a separately graded IPA reference.

A corpus with transcripts or audio is not automatically phonetic gold. A source-annotated corpus is not independent adjudication.

## Corpus comparison

| Source | Useful evidence | License / access | Limitations and decision |
|---|---|---|---|
| Project-authored challenge | 42 frozen Thai prompts plus six supplemental regression prompts; controlled blind review, no model output or source IPA in reviewer sheet. | MIT project-authored prompts. | **Use as the controlled baseline.** No audio; expert reviewers must supply lexical, segmentation, IPA, tone, length and glottal labels. |
| CCOST | 49 speakers; approx. 7h spontaneous + 5h controlled speech; 206-item controlled monosyllabic list; paper describes ORT/KAN/KAS/MAU/MAS/TRN tiers, X-SAMPA and five tone numerals. | CC BY-NC-SA 4.0; 6.2 GB audio/TextGrid archive. | Best controlled tonal/phonetic design, but non-commercial share-alike; paper reports no formal IAA; A-D wordlist columns differ by two items and released TextGrid schema remains uninspected. **Keep BLOCKED** until curator and archive checks. |
| LOTUSDIS | Approx. 114h Thai conversational meeting speech, 86 participants; utterance transcripts and TextGrid; dataset card lists 160,915 rows / approx. 13.2 GB. | CC BY-SA 4.0; repository states academic and commercial use subject to license. | **Register as supplementary audio for fresh human re-annotation.** No phone/toneme IPA gold; multi-channel/far-field and overlapping speech; select clean near-field single-speaker clips. Standard Thai representativeness must be checked per speaker. |
| Common Voice Thai v27.0 | Approx. 427h, 366,656 clips, 7,997 speakers; CC0 dataset. | CC0, but dataset card separately forbids re-hosting/re-sharing and speaker identification. | Not selected for a shared/re-distributed reviewer packet; no phonemic IPA or tone gold. Reviewers would need direct access under the dataset terms. |

## Recommended design

- **Controlled phonemic baseline:** use the project-authored 42+6 blind packet. Recruit two independent qualified Thai phoneticians/phonologists; preserve raw first-pass labels and abstentions; a distinct adjudicator resolves disagreements.
- **Controlled tonal contrasts:** use CCOST only if the project accepts the NC-SA restriction, the curator resolves the A-D set discrepancy, and the actual TextGrid tier/label/notation mapping is inspected and pinned. The LREC paper's intended tier map is not proof of the released archive's exact tier names.
- **Supplementary acoustic evidence:** use LOTUSDIS for new expert labels, not as pre-existing phonetic gold. Select clear near-field, single-speaker, non-overlapped clips. Pin the dataset revision, file hash, asset ID, speaker pseudonym, microphone/channel and exact interval. Do not copy audio into the repository.
- **Ukrainian target adaptation:** use a separate two-reviewer Ukrainian-native preference process conditional on source IPA. Never treat this as a validation of the Thai IPA itself.

## Gold acceptance gate

A row may be called independent gold only after:

1. The exact source, license, allowed use, dataset revision and asset/time reference are recorded.
2. Two qualified Thai reviewers independently complete the blind sheet; reviewer identities/qualification evidence are verified by the project owner.
3. Raw reviewer A/B labels are frozen before discussion.
4. A distinct qualified adjudicator records agreement or resolves disagreement with a rationale and record ID.
5. Broad phonemic, broad surface and narrow acoustic layers are never mixed in one score. Narrow acoustic labels require registered audio provenance.
6. The evaluation split is by speaker/recording, not random utterance, to avoid speaker leakage. Tone, length, coda, onset and syllable-structure strata must be reported separately where sample size permits.

## Current state

- Thai expert submissions: **0**.
- Ukrainian-native preference submissions: **0**.
- Adjudicated Thai IPA gold: **0**.
- Adjudicated word/syllable segmentation gold: **0**.
- LOTUSDIS source/license: verified and registered; individual audio assets not yet selected or pinned.
- CCOST: blocked pending source-order and archive-tier clarification.
- Therefore phonetic accuracy remains **NOT MEASURED**.
