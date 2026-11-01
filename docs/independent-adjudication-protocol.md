# Independent phonetic and Ukrainian-target adjudication protocol

Status: **prepared, not adjudicated**. No expert values are pre-filled. These templates do not constitute gold evidence.

## IPA / tone / vowel length

Template: `data/benchmark/ipa-adjudication-template.tsv`.

1. Before annotation, agree whether the target is broad phonemic IPA, conservative broad surface IPA, or narrow acoustic transcription. Never compare these as if they were the same label layer.
2. For any acoustic claim, use an authorized recording and record a stable asset reference, speaker metadata permitted by the license, and the exact relevant time interval. Text-only dictionary IPA is not acoustic evidence.
3. Two Thai phoneticians annotate independently and blind to the engine output where feasible. Record segmental IPA, syllable boundaries, tone category/contour, vowel length, final glottal realization, stress/context, and uncertainty.
4. Reconcile disagreements only after independent labels are frozen; preserve both original labels and a written disagreement log.
5. Do not count an output sourced from the same dictionary record as agreement with that record. The `เดิน` lexical override is explicitly circular for the source-attested comparison and is excluded from independent agreement counts.
6. Keep CCOST files external and preserve its CC BY-NC-SA 4.0 non-commercial/share-alike terms. This repository does not contain CCOST audio or TextGrid files.
7. The CCOST dataset record (DOI 10.5281/zenodo.17366698) and its LREC 2026 paper (DOI 10.63317/3ds35jijmgrx) are distinct records. The paper abstract reports ASR/forced-alignment followed by manual correction by phonetically trained native Thai speakers. Treat this as manually corrected corpus evidence, not proof of two independent blinded labels per item.
8. `CCOST_manual.pdf` was inspected on 2026-11-01. It is an RA workflow manual describing OCTRA ASR transcript correction, Thai-script normalization, Praat boundary/transcript correction and the BAS `CHUNKPREP → G2P → MAUS → PHO2SYL` pipeline. It names `OCTRA_1` and illustrates MAUS output symbols `sampa`, but does not define the final released TextGrid tier schema, complete phone/toneme inventory, tone-label convention, uncertainty handling or independent double annotation. Do not infer these missing details from the manual's tool configuration.
9. Before using CCOST rows, inspect the released TextGrid tier schema and detailed paper methods; map their labels to the declared target layer and exclude records whose annotation scope cannot be reconciled. Keep text/phone/toneme agreement claims separate from acoustic claims.
8. If the project claims independent adjudication of its own output, two new reviewers must still annotate blindly and independently under this protocol; existing CCOST annotations may be used as external references, but must not be relabelled as ClippyFirst's independent adjudication. Preserve the dataset's CC BY-NC-SA 4.0 non-commercial/share-alike terms and do not copy its audio or TextGrid assets into this repository.

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