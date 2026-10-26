# Independent phonetic and Ukrainian-target adjudication protocol

Status: **prepared, not adjudicated**. No expert values are pre-filled. These templates do not constitute gold evidence.

## IPA / tone / vowel length

Template: `data/benchmark/ipa-adjudication-template.tsv`.

1. Before annotation, agree whether the target is broad phonemic IPA, conservative broad surface IPA, or narrow acoustic transcription. Never compare these as if they were the same label layer.
2. For any acoustic claim, use an authorized recording and record a stable asset reference, speaker metadata permitted by the license, and the exact relevant time interval. Text-only dictionary IPA is not acoustic evidence.
3. Two Thai phoneticians annotate independently and blind to the engine output where feasible. Record segmental IPA, syllable boundaries, tone category/contour, vowel length, final glottal realization, stress/context, and uncertainty.
4. Reconcile disagreements only after independent labels are frozen; preserve both original labels and a written disagreement log.
5. Do not count an output sourced from the same dictionary record as agreement with that record. The `เดิน` lexical override is explicitly circular for the source-attested comparison and is excluded from independent agreement counts.
6. Keep CCOST files external until the archive, annotation manual, access terms, and intended non-commercial use have been checked. This repository does not contain CCOST audio or TextGrid files.

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
