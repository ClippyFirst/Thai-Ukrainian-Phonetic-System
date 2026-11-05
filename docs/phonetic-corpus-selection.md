# Thai phonetic corpus selection

**Historical checkpoint:** 2026-11-01. The current owner decision below supersedes conflicting audio-centric recommendations in this historical comparison. No third-party audio or labels are bundled.

## Current scope decision — 2026-11-05

- **Global TIMIT Thai: EXCLUDED.** Do not pursue access, fees, agreements, audio, text-label acquisition or derived labels.
- **CCOST: primary phonetic-text candidate.** A strict X-SAMPA→IPA converter and long-text TextGrid parser are implemented in docs/ccost-text-only-adapter.md; actual TextGrid files are not yet available for compatibility testing. Obtain a TextGrid-only export from curators. No WAV.
- **FastThaiG2P/Wiktionary: supporting candidate source.** Keep source licenses/provenance separate; generated IPA remains provisional, not gold.
- **LOTUSDIS: optional orthographic context only.** Use public utterance transcripts for conversational vocabulary/robustness if useful; no phone-level IPA gold and no audio work.
- **Audio-specific tasks are OUT OF SCOPE.** No acoustic annotation, interval selection, audio hashes or audio download.


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
| CCOST | Published tier map: ORT/KAN/KAS/MAU/MAS/TRN; X-SAMPA and five tone numerals; 206-item wordlist. | CC BY-NC-SA 4.0; 6.2 GB mixed WAV+TextGrid ZIP; no separate TextGrid-only archive listed. | **PRIMARY phonetic-text candidate.** Adapter/parser implemented against synthetic fixtures only. Actual TextGrid tier labels/encoding remain uninspected; request TextGrid-only export. No audio. |
| Global TIMIT Thai (THAIMIT, LDC2022S13) | Historical source description retained for audit traceability. | LDC User Agreement for Non-Members. | **EXCLUDED by owner decision 2026-11-05.** No access or acquisition work. Historical quality/licensing notes are not active project requirements. |
| LOTUSDIS | 160,915 public utterance-level text rows with speaker/microphone metadata; no verified phone/IPA labels. | CC BY-SA 4.0; attribution and ShareAlike required. | **OPTIONAL orthographic context only** for conversational vocabulary, disfluencies and text robustness. No audio, acoustic review or phone-level gold. |
| Common Voice Thai v27.0 | Approx. 427h, 366,656 clips, 7,997 speakers; CC0 dataset. | CC0, but dataset card separately forbids re-hosting/re-sharing and speaker identification. | Not selected for a shared/re-distributed reviewer packet; no phonemic IPA or tone gold. Reviewers would need direct access under the dataset terms. |

## Recommended design

- **Controlled phonemic baseline:** use the project-authored 42+6 blind packet. Recruit two independent qualified Thai phoneticians/phonologists; preserve raw first-pass labels and abstentions; a distinct adjudicator resolves disagreements.
- **Controlled tonal contrasts:** use CCOST only if the project accepts the NC-SA restriction, the curator resolves the A-D set discrepancy, and the actual TextGrid tier/label/notation mapping is inspected and pinned. The LREC paper's intended tier map is not proof of the released archive's exact tier names.
- **Optional orthographic context:** use LOTUSDIS transcript text only for conversational vocabulary and orthographic robustness. Do not acquire or process its audio under the current project scope.
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
