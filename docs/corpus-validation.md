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


## Current external corpus triage — verified 2026-10-25

This section records resource candidates and constraints; it does not claim that any corpus has been ingested or that ClippyFirst accuracy has been measured.

| Resource | Best use | License / provenance | Decision |
|---|---|---|---|
| [CCOST v1.0, Zenodo DOI 10.5281/zenodo.17366698](https://doi.org/10.5281/zenodo.17366698) | Acoustic/phone/toneme review; controlled 206-word list, 25 sentences and spontaneous speech | CC BY-NC-SA 4.0; ~12 hours, 49 speakers; audio + TextGrid | Highest-priority independent phonetic adjudication candidate. Keep data outside repository; local use only after reviewing license, annotation manual and split policy. |
| [PyThaiNLP Thai G2P Wiktionary corpus](https://github.com/PyThaiNLP/thai-g2p-wiktionary-corpus) | Broad source-attested IPA regression and lexicon error discovery | CC BY-SA 3.0; derived from Wiktionary via WikiPron | Useful secondary source, **not independent gold** against Wiktionary-derived engines. Freeze snapshot and record exact source revision per row. |
| [NLP for Thai word-segmentation resource index](https://nlpforthai.com/tasks/word-segmentation/) | Independent lexical boundary evaluation | Listed options include Wisesight samples CC0-1.0, Blackboard Treebank CC BY 3.0, VISTEC-TP-TH-21 CC BY-SA 3.0, and BEST I CC BY-SA-NC 4.0 | Use a separately held-out dataset; validate upstream provenance, access conditions and license before use. Segmentation gold is not pronunciation gold. |
| [BEST-2010 benchmark index](https://opencodepapers-b7572d.gitlab.io/benchmarks/thai-word-tokenization-on-best-2010.html) | Context for reported word-boundary F1 results | Results depend on corpus version, official split and tokenization convention | External comparison only; do not claim these scores for ClippyFirst or compare against an explicit lexicon without matched evaluation. |

## Required evaluation contract

1. **Segmentation first.** Evaluate word-boundary precision/recall/F1, exact sequence match, unknown-word abstention/coverage, and lexicon coverage separately. Report macro/domain-stratified results; do not let common words hide unknown-word failures.
2. **Phonology second.** Evaluate only cases with independently adjudicated pronunciation labels. Report strict IPA exact match with tone, length and syllable boundaries preserved; also segment-level onset, vowel quality/length, coda, tone and syllable-boundary errors where alignment permits. Use speaker-aware/domain-aware holdouts for audio-derived labels.
3. **No leakage.** Check whether lexicon entries, external-engine dictionaries and gold labels share Wiktionary or other source provenance. Split by lexical item and, for audio, by speaker/recording where appropriate. Keep source-attested and independently adjudicated labels in separate statuses.
4. **Parity is a distinct gate.** Compare Python and browser output fields on the same fixtures: normalized input, segmentation, syllable boundaries, typed IPA status, phonemic IPA, surface IPA, tone/length metadata, provenance/uncertainty and Ukrainian adapter result. A parity pass proves implementation consistency, not that the shared output is linguistically correct.
5. **Score honesty.** Existing benchmark harness only scores `ADJUDICATED` rows with non-empty IPA, source ID and profile; missing predictions remain in the denominator. Empty gold yields `NOT_MEASURED`. Current benchmark files are header-only, so current independent-gold count is zero and accuracy remains unmeasured.

## Immediate next work

- Review the CCOST annotation manual and select a stratified, license-compliant sample; get independent Thai expert adjudication for orthography → segmentation → broad IPA → tone and document disagreements.
- Select a CC0 or otherwise compatible word-segmentation holdout, pin exact revision/hash, and implement a deterministic boundary scorer with synthetic unit tests before running any score.
- Run existing exact-head CI, generated-artifact drift checks and Python/browser parity; record the exact SHA and workflow result. Do not mark a task DONE_VERIFIED from the existence of a test file alone.
