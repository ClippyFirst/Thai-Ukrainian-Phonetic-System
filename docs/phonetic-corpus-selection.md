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
| Global TIMIT Thai (THAIMIT, LDC2022S13) | Approx. 11.77h read Standard Thai; 50 speakers; 6,000 utterances; aligned word, phone and tone tiers; separate .phones, .tones, .words and Praat TextGrid files. | LDC User Agreement for Non-Members; paid/authorized access; non-commercial research only; no redistribution outside research group. | Phone labels are aligner-specific DARPABET, not IPA. Official README describes custom HTK forced alignment using SWATH tokenization, Haas dictionary and ~1,000 added pronunciations; the 2018 GlobalTIMIT paper reports proof-listening and a final phone-sequence/alignment check for each collection, but no Thai-specific quantitative phone/tone accuracy, independent double labels or IAA. Its 93.2% within-20-ms alignment result is for Mandarin, not Thai. **Candidate for restricted audio/re-annotation and alignment tooling only, not gold; commercial product release requires LDC for-profit membership/fees.** Sample phone/tone files not inspected because browser fetch rejected binary content. |
| LOTUSDIS | Approx. 114 aggregate microphone-channel hours (about 20h unique session time), 86 participants; nine separately recorded single-channel devices, utterance transcripts, TextGrid and overlap masks; dataset card lists 160,915 rows / approx. 13.2 GB. | CC BY-SA 4.0; repository states academic and commercial use subject to license. | **Register as supplementary audio for fresh human re-annotation.** No phone/toneme IPA gold; device placement ranges near-to-far field and overlap is explicitly marked; select clear near-field, non-overlapped single-speaker intervals after checking the actual device and mask. Standard Thai representativeness must be checked per speaker. |
| Common Voice Thai v27.0 | Approx. 427h, 366,656 clips, 7,997 speakers; CC0 dataset. | CC0, but dataset card separately forbids re-hosting/re-sharing and speaker identification. | Not selected for a shared/re-distributed reviewer packet; no phonemic IPA or tone gold. Reviewers would need direct access under the dataset terms. |

## Recommended design

- **Controlled phonemic baseline:** use the project-authored 42+6 blind packet. Recruit two independent qualified Thai phoneticians/phonologists; preserve raw first-pass labels and abstentions; a distinct adjudicator resolves disagreements.
- **Controlled tonal contrasts:** use CCOST only if the project accepts the NC-SA restriction, the curator resolves the A-D set discrepancy, and the actual TextGrid tier/label/notation mapping is inspected and pinned. The LREC paper's intended tier map is not proof of the released archive's exact tier names.
- **Supplementary acoustic evidence:** use LOTUSDIS for new expert labels, not as pre-existing phonetic gold. Select clear near-field, single-speaker, non-overlapped intervals. The corpus reports roughly 114 aggregate device/channel hours but only about 20 hours of unique session time; it uses nine separate single-channel devices. Pin the dataset revision, file hash, asset ID, speaker pseudonym, microphone/channel and exact interval. Do not copy audio into the repository.
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
- LOTUSDIS source/license: verified and registered; `data/benchmark/audio-assets.tsv` is header-only. Individual audio assets, hashes, speaker/mic metadata and intervals are not yet selected or pinned.
- CCOST: blocked pending source-order and archive-tier clarification.
- Therefore phonetic accuracy remains **NOT MEASURED**.

## Global TIMIT Thai source review — 2026-11-02

The LDC catalog, official README.txt and 2018 GlobalTIMIT paper were inspected. The corpus is a potentially useful source of time-aligned Standard Thai read speech, but its labels must not be mistaken for independently reviewed phonetic gold. The README states that a custom HTK aligner generated word, phone and tone timestamps from corrected transcripts, SWATH tokenization and pronunciation resources; .phones labels use aligner-specific DARPABET. The paper adds that each collection received initial proof-listening and a final phone-sequence/alignment check. Neither source establishes two independent labels per item, formal inter-annotator agreement, Thai-specific quantitative phone/tone accuracy or a DARPABET-to-IPA mapping.

Access is a material constraint: the catalog identifies the LDC Non-Member User Agreement. That agreement restricts use to non-commercial linguistic education/research/technology development and prohibits redistribution outside the user's research group; a commercial product release requires LDC for-profit membership and applicable fees. The non-member agreement requires a signed copy to be emailed or faxed to LDC and disclaims warranties of data accuracy/completeness. Do not copy corpus audio, alignments or derived label files into this repository or public reviewer packets. The catalog sample .phones and .tones downloads were not inspected because the browser could not fetch their binary content. Treat source discovery as verified, actual data access and label validation as blocked.

**Decision:** register as a restricted candidate for authorized internal tooling/re-annotation only. Do not use it as independent IPA/tone gold, do not score ClippyFirst accuracy from its aligner output, and do not use it for commercial product development without written LDC authorization appropriate to that use.
