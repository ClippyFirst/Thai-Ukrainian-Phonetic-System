# Corpus validation

## Purpose

This repository contains validation infrastructure, not a redistributed copy of third-party corpora. A licensed/local corpus is supplied by the researcher and evaluated deterministically.

## Registered resources

- **CCOST** — phonetically annotated Standard Thai resource suitable for orthography, syllable, phone and toneme validation.
- **Thai Grapheme to Phoneme Wiktionary Corpus** — Thai forms paired with IPA, suitable for broad G2P regression.
- **Thai National Corpus II / Thai Textbook Corpus** — useful for lexical frequency and distribution checks, not substitutes for phonetic gold labels.

## Input contract

The evaluator consumes JSONL. Every record requires id, thai, and source. Gold fields such as ipa and tone are optional, but a missing gold field is excluded from that metric rather than counted as correct.

The record schema is schemas/corpus-record.schema.json.

## Metrics

The evaluator reports explicit numerators and denominators:

- ipa_exact_correct / ipa_exact_total
- tone_correct / tone_total
- exact-match accuracy for each metric, or null when its denominator is zero.

These metrics are not lexical coverage metrics. A separate corpus inventory report should be used for lexical coverage, frequency and attestation.

## Recommended evaluation protocol

1. Record the corpus name, version/access date and license.
2. Keep the corpus itself outside the repository when redistribution is not permitted.
3. Normalize only according to a declared preprocessing protocol.
4. Evaluate syllable segmentation before segment-level IPA.
5. Compare onset, coda, vowel identity/length and tone separately.
6. Report exact IPA only as one strict metric; add segment-level metrics when gold alignment is available.
7. Stratify errors by orthographic construction, tone class, vowel type, coda type and ambiguity.
8. Never infer empirical accuracy from the structural syllable-space upper bound.
9. Never convert heuristic Ukrainian candidate distance into a probability without calibration data.

## Command

python scripts/evaluate_corpus.py path/to/records.jsonl

The command prints deterministic JSON and returns a non-zero exit code for malformed input.

## Current empirical status

No third-party corpus is bundled or processed by CI. Therefore **corpus accuracy, lexical coverage and candidate calibration remain unmeasured** in the repository release. The infrastructure is ready for a licensed local evaluation.


## Current software status

The repository now also exposes:
- an external TSV lexicon adapter for evidence-backed syllable segmentation;
- explicit special-orthography candidate records;
- project-defined Ukrainian orthographic candidates downstream of broad IPA.

None of these additions turns an external corpus into gold automatically. Gold status still depends on a named source, version/access date, license and adjudication protocol.
