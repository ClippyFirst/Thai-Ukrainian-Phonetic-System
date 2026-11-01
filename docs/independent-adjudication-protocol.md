# Independent phonetic and Ukrainian-target adjudication protocol

Status: **prepared, not adjudicated**. No expert values are pre-filled. These templates do not constitute gold evidence.

## IPA / tone / vowel length

Legacy reconciliation sheet: `data/benchmark/ipa-adjudication-template.tsv` (contains source-attested references and engine candidates; it is **not** a blind annotation sheet). Use `data/benchmark/ipa-adjudication-blind.tsv` for first-pass Thai expert annotation.

1. Before annotation, agree whether the target is broad phonemic IPA, conservative broad surface IPA, or narrow acoustic transcription. Never compare these as if they were the same label layer.
2. For any acoustic claim, use an authorized recording and record a stable asset reference, speaker metadata permitted by the license, and the exact relevant time interval. Text-only dictionary IPA is not acoustic evidence.
3. Two Thai phoneticians annotate independently and blind to the engine output where feasible. Record segmental IPA, syllable boundaries, tone category/contour, vowel length, final glottal realization, stress/context, and uncertainty.
4. Reconcile disagreements only after independent labels are frozen; preserve both original labels and a written disagreement log.
5. Do not count an output sourced from the same dictionary record as agreement with that record. The `เดิน` lexical override is explicitly circular for the source-attested comparison and is excluded from independent agreement counts.
6. Keep CCOST files external and preserve its CC BY-NC-SA 4.0 non-commercial/share-alike terms. This repository does not contain CCOST audio or TextGrid files.
7. The CCOST dataset record (DOI 10.5281/zenodo.17366698) and its LREC 2026 paper (DOI 10.63317/3ds35jijmgrx) are distinct records. The paper abstract reports ASR/forced-alignment followed by manual correction by phonetically trained native Thai speakers. Treat this as manually corrected corpus evidence, not proof of two independent blinded labels per item.
8. `CCOST_manual.pdf` was inspected on 2026-11-01. It is an RA workflow manual describing OCTRA ASR transcript correction, Thai-script normalization, Praat boundary/transcript correction and the BAS `CHUNKPREP → G2P → MAUS → PHO2SYL` pipeline. It names `OCTRA_1` and illustrates MAUS output symbols `sampa`, but does not define the final released TextGrid tier schema, complete phone/toneme inventory, tone-label convention, uncertainty handling or independent double annotation. Do not infer these missing details from the manual's tool configuration.
9. Before using CCOST rows, inspect the released TextGrid tier schema and detailed paper methods; map their labels to the declared target layer and exclude records whose annotation scope cannot be reconciled. Keep text/phone/toneme agreement claims separate from acoustic claims.
10. If the project claims independent adjudication of its own output, two new reviewers must still annotate blindly and independently under this protocol; existing CCOST annotations may be used as external references, but must not be relabelled as ClippyFirst's independent adjudication. Preserve the dataset's CC BY-NC-SA 4.0 non-commercial/share-alike terms and do not copy its audio or TextGrid assets into this repository.

## Ukrainian target-form preference

Template: `data/benchmark/ukrainian-target-adjudication.tsv`.

1. This is a project-specific practical transcription preference task, not a claim that Ukrainian has one official standard for Thai names or words.
2. Define the objective before annotation: e.g. segmental pronunciation readability, consistency, preservation of contrasts, handling of tone, and whether syllable dots are presentation-only.
3. At least two Ukrainian-native reviewers independently evaluate candidate renderings against the agreed IPA target, with source IPA and existing engine output labeled as references rather than gold.
4. Collect free-form preferred forms before exposing the engine candidate, where practical, to reduce anchoring.
5. Freeze a criteria version, retain each reviewer’s original form and rationale, then adjudicate disagreements. Report agreement and abstentions; do not fill blank fields with generated candidates.
6. Keep IPA correctness and Ukrainian orthographic preference as separate evaluation tasks.

## Current blockers and acceptance criteria

- IPA: BLOCKED until a qualified independent Thai phonetician completes the rows with an agreed transcription-level protocol and authorized acoustic assets for acoustic claims.
- Ukrainian adaptation: BLOCKED until two independent Ukrainian-native judgments and an adjudication log exist for the declared sample.
- `บรรจุ` final /ʔ/: remain a review case until broad-vs-surface transcription and stress/context are explicit. No global rule should be inferred from one dictionary form.


## Reproducible segmentation-review sampling — 2026-10-26

The CI artifact built by `scripts/build_segmentation_manual_review.py` is a **review packet, not an adjudicated corpus**. It now samples from all pinned source rows rather than only the highest-ranked error examples:

- deterministic selection of up to 8 rows per heuristic stratum (numbers/dates, URLs/emails, mixed Latin–Thai, Latin/brands, punctuation/quoting, long Thai, engine disagreement, or general review);
- an additional deterministic uniform control sample of 12 rows from the full 993-row source set;
- both dictionary and TUD predictions are recomputed for every source row and must reconstruct the original text exactly;
- every output row retains `gold_status=SOURCE_ANNOTATED`, `adjudicated=NO`, and blank human decision, reviewer and rationale fields;
- sampling strata are heuristics only. A model/source disagreement is not automatically an error, and the TUD model remains research-only.

Reviewers should independently record whether the upstream tokenization is linguistically defensible under a pre-agreed word-boundary convention, classify the reason for any proposed correction, and preserve the original source label. Freeze the annotation guide before review; do not use reviewed Wisesight rows to train/tune the segmenter or claim independent-domain generalization. Report sample inclusion probabilities or clearly label the packet as a targeted diagnostic sample; do not calculate population accuracy from this stratified sample without appropriate sampling weights.

The external acceptance dependency remains: qualified human reviewers must actually fill and sign off the packet. CI can verify sampling reproducibility, provenance, and lossless text reconstruction only; it cannot perform linguistic adjudication.


## CCOST manual review — scope result (2026-11-01)

`CCOST_manual.pdf` is now inspected. The file documents an operational research-assistant workflow, not a complete annotation specification. It directs human correction of ASR transcripts, Thai orthographic normalization, Praat boundary refinement and BAS MAUS alignment. The manual's illustrated pipeline uses `OCTRA_1` as an input tier and `sampa` as MAUS output symbols, but this alone does not prove that the released TextGrids contain a fully documented SAMPA or IPA transcription tier. It does not specify the final TextGrid tier inventory, toneme label scheme, uncertainty handling, or independent double annotation. The manual-inspection task is complete; CCOST benchmark acceptance remains blocked until the released TextGrid schema and detailed paper methods are reconciled with the target transcription layer.

## Blind Thai phonetic packet — operational procedure (2026-11-01)

The frozen 42-item challenge set now has a separate reviewer-facing packet at `data/benchmark/ipa-adjudication-blind.tsv`. It is generated from `data/benchmark/thai_g2p_challenge.jsonl` and deliberately contains no engine output, source-dictionary IPA, or prefilled human labels. Each reviewer must work from a separate copy and must not see the other reviewer's sheet or any engine predictions before their own labels are frozen.

- `word_boundaries`: separate orthographic words with `|`; preserve spaces/punctuation in a separate notes field where needed.
- `syllable_boundaries`: separate syllables with `.`; annotate the actual reading, not a segmentation guessed from spelling.
- `phonemic_ipa`: broad phonemic IPA; `broad_surface_ipa` is optional and must not be conflated with the phonemic target.
- `tone_sequence`: categorical tone labels per syllable; `vowel_length`: short/long/uncertain per syllable; `final_glottal`: PRESENT / ABSENT / CONTEXTUAL / UNKNOWN / NOT_APPLICABLE.
- `orthography_validity`: VALID / INVALID / AMBIGUOUS / UNKNOWN. `uncertainty`: LOW / MEDIUM / HIGH / ABSTAIN. An abstention requires a written reason and must not contain a guessed IPA.
- `transcription_level`: BROAD_PHONEMIC or NARROW_ACOUSTIC. The primary `phonemic_ipa` field is always syllabified; optional `broad_surface_ipa` is a supplementary layer, not a substitute for phonemic IPA. NARROW_ACOUSTIC is accepted only with a stable authorized audio asset reference and a positive time interval. Do not infer narrow phonetics from dictionary IPA.
- `reviewer_id` is a pseudonymous stable reviewer key; `reviewer_qualification_ref` points to the separately retained qualification evidence. Do not commit personal contact details or private credentials.

The blank packet is checked against the frozen challenge set in CI. A completed copy can be checked with:

```bash
python scripts/validate_adjudication_packet.py --mode review --reviewer-id TH-PH-01 data/benchmark/reviewer-a.tsv
python scripts/validate_adjudication_packet.py --mode review --reviewer-id TH-PH-02 data/benchmark/reviewer-b.tsv
python scripts/validate_adjudication_packet.py --mode pair --reviewer-b-packet data/benchmark/reviewer-b.tsv data/benchmark/reviewer-a.tsv
```

The pair gate checks exact item coverage, distinct reviewer IDs, qualification references, dates, explicit abstentions and acoustic time references. It does not judge whether either pronunciation is correct or settle disagreements. Preserve both independent files, then write the adjudication decision and disagreement rationale. Only then may a row be promoted into `data/benchmark/gold.tsv`.

## Ukrainian preference review — conditional on supplied IPA

`data/benchmark/ukrainian-target-preference-blind.tsv` contains the six current source-attested examples, with the engine candidate removed. Reviewers judge the Ukrainian rendering **conditional on the supplied IPA**, not the correctness of the Thai pronunciation. Every row is explicitly marked `SOURCE_ATTESTED_NOT_GOLD`; these judgments cannot be used as an end-to-end Thai→Ukrainian accuracy score.

Criteria version `UA-PRACTICAL-TRANSCRIPTION-0.1` asks reviewers to record:
1. preferred practical Ukrainian form and rationale;
2. whether syllable separators should be preserved, omitted, or treated as display-only;
3. whether aspiration, /ŋ/, affricates, /ɯ/ and vowel contrasts are represented consistently and readably;
4. whether tone is correctly kept in IPA/metadata rather than falsely encoded as ordinary Ukrainian letters;
5. uncertainty or abstention where the supplied IPA itself is insufficient.

Each Ukrainian-native reviewer receives a separate copy without the engine candidate. Keep reviewer forms and the later reconciliation record separate. Do not promote a preference to gold merely because two reviewers agree; retain the IPA reference grade and criteria version.

## Gold benchmark acceptance gate

The IPA scorer now requires two distinct reviewer IDs, both raw IPA labels, an adjudicator, an adjudication record, outcome, transcription level, source URL and license for every `ADJUDICATED` row. `AGREEMENT` requires matching raw labels; `RESOLVED_DISAGREEMENT` requires different raw labels and a written adjudication note. A single run cannot mix BROAD_PHONEMIC and BROAD_SURFACE references. Metrics are also stratified by the frozen profile/stratum.

Current status remains **zero adjudicated gold rows**. The stricter gate and packets are infrastructure, not completed expert review. The six dictionary readings remain source-attested references and must not enter the gold denominator.

## CCOST source decision

CCOST is the strongest current candidate for a licensed acoustic/phone/toneme evaluation: the public LREC 2026 description reports 49 Standard Thai speakers, approximately seven hours of spontaneous interview speech, a repeated 206-item monosyllabic word list, 25 repeated sentences, and orthographic/word/syllable/phone annotations including toneme labels. Zenodo identifies the dataset as CC BY-NC-SA 4.0 and lists a 6.2 GB audio/TextGrid archive. Its paper reports ASR/forced alignment followed by manual correction by phonetically trained native Thai speakers; that does not establish independent double-blind annotation per item.

The repository does not redistribute CCOST. Before importing any labels, obtain the licensed archive under the non-commercial/share-alike terms, inspect actual released TextGrid tier names and label inventory, map tiers to the chosen phonemic/surface/acoustic target, record recording and speaker references plus time intervals, and exclude unmappable or uncertain rows. Existing manual inspection does not resolve the tier-schema blocker. New independent reviewers remain required for this project's own gold labels.


## Reviewer packet schema and evidence separation — 2026-11-01 refinement

The Thai blind packet has 42 rows and 21 columns. It intentionally omits challenge stratum/probe labels as well as all source-dictionary IPA and engine outputs, reducing hypothesis anchoring. It is candidate-blind, not a security boundary: distribute only the packet to reviewers and do not send them model output, diagnostic reports, source-attested worksheets or the other reviewer's sheet.

For each non-abstaining row, the validator requires:
- `lexical_reading` (or explicit `UNRESOLVED`);
- `word_boundaries`: Thai orthographic words separated by `|`;
- `syllable_boundaries`: syllables separated by `.`, with `|` retained between words;
- `tone_sequence`: comma-separated `MID, LOW, FALLING, HIGH, RISING, UNKNOWN, NOT_APPLICABLE`, one value per syllable;
- `vowel_length`: comma-separated `SHORT, LONG, UNKNOWN, NOT_APPLICABLE`, one value per syllable;
- `final_glottal`: comma-separated `PRESENT, ABSENT, CONTEXTUAL, UNKNOWN, NOT_APPLICABLE`, one value per syllable;
- `phonemic_ipa`, uncertainty and a declared transcription level.

Boundary strings must reconstruct the exact Thai input after removing only their declared separators. Tone, vowel-length and glottal arrays must align one-to-one with syllables. Abstention is valid but requires a reason and must contain no phonemic or surface IPA. A narrow acoustic label requires an authorized audio reference and positive time interval.

Completed reviewer copies can be checked independently and as a pair:

```bash
python scripts/validate_adjudication_packet.py --mode review --reviewer-id TH-PH-01 data/benchmark/reviewer-a.tsv
python scripts/validate_adjudication_packet.py --mode review --reviewer-id TH-PH-02 data/benchmark/reviewer-b.tsv
python scripts/validate_adjudication_packet.py --mode pair --reviewer-b-packet data/benchmark/reviewer-b.tsv data/benchmark/reviewer-a.tsv
```

The paired review validator checks distinct reviewer IDs, exact sample coverage, qualification references, source-input identity, syllable-aligned metadata and explicit abstention. It does not decide which pronunciation is correct.

### Separate word- and syllable-segmentation gold

`data/benchmark/segmentation-adjudication-gold.tsv` is an empty registry for future expert boundary labels. Each row declares `segmentation_layer=WORD|SYLLABLE`; a benchmark run may not mix the two. Every `ADJUDICATED` row requires two distinct reviewer IDs, both original tokenizations, qualification references, adjudicator, outcome, record, source URL and license. `AGREEMENT` requires matching reviewer token arrays and gold equal to them. `RESOLVED_DISAGREEMENT` requires different raw arrays and a written adjudication note. Existing Wisesight rows remain `SOURCE_ANNOTATED`, not expert gold.

### Ukrainian-native preference review validation

The six-row `data/benchmark/ukrainian-target-preference-blind.tsv` has no engine candidates and is validated against the frozen source-attested IPA registry. Reviewers record a preferred Ukrainian form (or explicit abstention), rationale, syllable-boundary display policy and tone-rendering policy. Completed-review validation requires a stable reviewer ID, qualification reference, ISO date, rationale and fixed criteria version. Pair validation requires two different Ukrainian reviewer IDs and exact source/input identity.

```bash
python scripts/validate_ukrainian_preference_packet.py --mode review --reviewer-id UK-UA-01 data/benchmark/ukrainian-review-a.tsv
python scripts/validate_ukrainian_preference_packet.py --mode pair --reviewer-b-packet data/benchmark/ukrainian-review-b.tsv data/benchmark/ukrainian-review-a.tsv
```

These are conditional judgments about Ukrainian rendering of supplied dictionary IPA. They remain `SOURCE_ATTESTED_NOT_GOLD` and cannot measure Thai pronunciation or end-to-end accuracy.
