# Corpus validation

## Purpose

This repository contains validation infrastructure, not a redistributed copy of third-party corpora. A licensed/local corpus is supplied by the researcher and evaluated deterministically.

## Registered resources

- **CCOST** — phonetically annotated Standard Thai resource suitable for orthography, word, syllable, phone and toneme analysis. The primary source states CC BY-NC-SA 4.0; the 6.2 GB `C-COST.zip` contains WAV audio and TextGrid annotations, while the manual, metadata, wordlist, and sentences are separate files. This repository does not redistribute the archive.
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

## Pinned source-annotated segmentation benchmark — 2026-10-25

A reproducible, permissively licensed segmentation dataset is now available at `data/benchmark/segmentation-gold.tsv`:

- Upstream: [PyThaiNLP/Wisesight Sentiment Corpus with Word Tokenization Label](https://github.com/PyThaiNLP/wisesight-sentiment/tree/c1d063649abc3a6870b5fd1aae26cd1c64bdde7b/word-tokenization), exact source file `word-tokenization/wisesight-1000-samples-tokenised.label`.
- Immutable source commit: `c1d063649abc3a6870b5fd1aae26cd1c64bdde7b`; upstream Git blob SHA-1: `279aeb2d4323fd8032306160144d33dcb5b2df84`.
- License: CC0-1.0. The source annotation file has 993 records; the published task notes seven spam messages were removed from the nominal 1,000-sample set.
- Annotation: human word tokenization following the Aroonmanakun (2007) segmentation standard, as described in the dataset/paper. This is **SOURCE_ANNOTATED**, not an assertion of independent expert adjudication or inter-annotator agreement.
- Split: all 993 pinned records are designated `test` for this project; do not use them for training or for constructing the runtime lexicon.
- Conversion: pipe-delimited tokens were converted to a TSV with JSON token arrays. Empty zero-width delimiter fields are dropped because they contribute no characters; each row is required to reconstruct its text exactly. The scorer excludes boundaries touching explicit whitespace tokens from lexical word-boundary metrics.

Run `python scripts/run_wisesight_segmentation_diagnostic.py --output /tmp/wisesight1000-segmentation-baseline.json`. The diagnostic preserves source annotation grade and evaluates the current text-tokenizer/no-automatic-segmentation baseline. It does not measure pronunciation or prove representative coverage of Standard Thai.

## Source-attested IPA contrast records — not gold

`data/benchmark/source-attested-ipa.tsv` records six revision-pinned Thai Wiktionary readings, including the contrast `เงิน /ŋɤn˧/` (short /ɤ/) vs `เดิน /dɤːn˧/` (long /ɤː/). These are CC BY-SA 4.0 source-attested dictionary records, explicitly labeled `SOURCE_ATTESTED_NOT_GOLD`. They support claim-level inspection and regression triage; they do not satisfy independent acoustic/expert adjudication and must not enter the gold scorer.

The new curated lexicon additions have exact per-entry locators and data-license attribution in `data/thai/text_lexicon_sources.csv`; the derived subset's share-alike obligations are documented in `data/thai/TEXT-LEXICON-DATA-LICENSE.md`. The spelling `เงิน` is enabled only through the typed lexical-IPA override in `data/thai/lexical_ipa_overrides.tsv`, which preserves its source-attested short-vowel reading through the IPA-first adapter. It remains `SOURCE_ATTESTED_NOT_GOLD`, not independently adjudicated or acoustically verified.

## Remaining phonetic evidence gate

CCOST v1.0 remains the strongest candidate for acoustic/phone/toneme review, but the repository does not claim it was downloaded, reviewed locally, or adjudicated. Its CC BY-NC-SA 4.0 license permits only non-commercial sharing/adaptation under share-alike terms. A trained Thai phonetician must independently review a pinned, speaker-aware sample against the annotation manual before any CCOST-derived labels can be called expert-adjudicated gold. No gold IPA, tone, or vowel-length score is emitted by this commit.


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


## Segmentation evaluator

A deterministic standard-library scorer is available at `scripts/evaluate_segmentation.py`:

```bash
python scripts/evaluate_segmentation.py --gold data/benchmark/segmentation-gold.tsv --predictions data/benchmark/segmentation-predictions.tsv --output reports/segmentation-benchmark.json
```

The input contract is tab-separated: gold columns `id, text, gold_tokens_json, gold_status, source_id, license, split`; predictions columns `id, engine, predicted_tokens_json, status, version`. Token arrays are JSON string arrays. Tokens must concatenate exactly to the NFC-normalized source text; the evaluator does not silently remove whitespace or rewrite text. It reports boundary precision/recall/F1, exact token-sequence rate and coverage separately. Only `ADJUDICATED` gold rows with source, license and split enter the denominator; absent predictions count as misses, and no adjudicated rows yields `NOT_MEASURED`. Only prediction rows with `status=ok` are scoreable; all other statuses are treated as abstentions even if a stale or partial token array is present. Empty token arrays are also abstentions. Coverage counts only non-empty `ok` predictions. The added tests use synthetic fixtures only; no empirical score is implied.

The input files are not yet populated with corpus records. Before running an empirical benchmark, acquire a license-compatible corpus, pin version/hash and split, verify the tokenization annotation convention, and record provenance per row. Keep CCOST audio/annotations outside the repository under its CC BY-NC-SA 4.0 terms; it is a research adjudication candidate, not a freely redistributable fixture.


## Segmentation corpus source register — 2026-10-25

Candidate and active sources are recorded in `data/corpus_sources.csv` so license state and intended use stay inspectable:

- **Wisesight-1000 word-tokenization labels** — CC0-1.0; the exact 993-row snapshot in this repository is marked `SOURCE_ANNOTATED` and held out as test-only. It is not independent expert gold, and must not be used to train a model or construct the runtime lexicon.
- **LST20** — candidate for news-domain segmentation. This repository does not bundle it; the source register explicitly requires review of the exact license and redistribution terms before use.
- **VISTEC-TP-TH-2021** — candidate for social-media segmentation. The dataset card reports CC BY-SA 3.0; verify the upstream revision, attribution, and applicable terms before redistributing any derived data.

Do not mix these sources into one benchmark until annotation policies, normalization, document-level split strategy, and license compatibility are documented. A candidate source's existence does not make its labels compatible with Wisesight or the project's test split.


### CCOST text-annotation feasibility and boundary

Praat TextGrid annotations are textual records and can be analyzed without playing the corresponding audio for a first-pass comparison of source-attested orthography, word boundaries, syllable labels, phone labels, and toneme labels. However, the archive is 6.2 GB and the TextGrid files are inside `C-COST.zip`; only the separate wordlist/sentences and metadata are directly small enough for a selective workflow. Those separate files are not substitutes for phone/toneme annotation. No CCOST TextGrid files are currently bundled or available as repository inputs, so no CCOST-derived records or metrics are claimed in this checkpoint.

The corpus license is CC BY-NC-SA 4.0. Do not copy its annotations or derived datasets into a distribution intended for commercial use without separately confirming permission. A future local importer should accept a user-downloaded TextGrid path, record the corpus revision and file checksum, map tier names from the manual explicitly, preserve speaker/session IDs, and emit only the text fields needed for evaluation. It must not silently convert forced-alignment labels into independent phonetic gold. Acoustic validation still requires access to the corresponding audio.


## Source-attested IPA discrepancy diagnostic

Run `python scripts/run_source_attested_ipa_diagnostic.py --output /tmp/source-attested-ipa-diagnostic.json` to compare the six pinned dictionary transcriptions with the current text pipeline. The report separates segmental IPA, tone categories, and vowel-length metadata; it records withheld outputs and mismatches without calling the source data gold. On the last successful Python checkpoint it produced five complete outputs, four segmental agreements, five tone-category agreements, and one withheld result. The `บรรจุ` final-`/ʔ/` discrepancy remains a review item.

## License-cleared segmentation training experiment — 2026-10-26

The repository now has a reproducible, standard-library-only training experiment in `scripts/train_tud_word_segmenter.py` using **UD Thai TUD**, pinned to upstream commit `67413969add552b7030184f16f24fa9f630913bc`. The upstream treebank declares **CC BY-SA 4.0**, describes 3,627 retained dependency trees from Thai National Corpus and Wikipedia, and documents that tokenization was initially performed with PyThaiNLP `newmm` and then reviewed by annotators. The upstream train/dev/test files are individually pinned by Git blob SHA in the script. The project pools only those pinned snapshots and deterministically re-splits by normalized source filename (80/10/10), so sentences from one source document cannot cross train/dev/test. See the [upstream treebank README](https://github.com/UniversalDependencies/UD_Thai-TUD/blob/67413969add552b7030184f16f24fa9f630913bc/README.md), [license](https://github.com/UniversalDependencies/UD_Thai-TUD/blob/67413969add552b7030184f16f24fa9f630913bc/LICENSE.txt), and [TACL paper](https://doi.org/10.1162/tacl_a_00745).

Protocol:
1. Pool the three pinned TUD source snapshots and group by source filename (strip a trailing `-PART<number>` component).
2. Assign source groups deterministically to train/dev/test at 80/10/10 by SHA-256 of the normalized filename; assert source-disjointness.
3. Fit word-frequency counts on the derived **train** split only.
4. Select the Viterbi token penalty on the derived **dev** split only using a fixed grid.
5. Report the source-disjoint derived **test** split separately.
4. Report Wisesight's 993 source-annotated rows as a separate external test-only set. Wisesight never contributes to training or hyperparameter selection.
5. Verify the downloaded source bytes against the pinned Git blob SHA-1 before parsing.
6. Keep the trained model/report as CI artifacts with CC BY-SA 4.0 attribution/share-alike metadata; do not silently treat derived weights as public-domain or change the repository's code license.

Run:
```bash
python scripts/train_tud_word_segmenter.py --model /tmp/thai-tud-word-model.json --report /tmp/thai-tud-word-segmentation-report.json
python scripts/train_tud_word_segmenter.py --model /tmp/thai-tud-word-model.json --text "ภาษาไทย"
```

This is a research segmentation model, not the production default. It learns a unigram word-frequency Viterbi model; its evaluation is restricted to contiguous Thai-only runs with at least two gold tokens. These metrics must not be conflated with the full-text Wisesight dictionary-max-match baseline. A stronger sequence model and independent cross-domain adjudication remain future acceptance criteria. The source license is compatible with a research artifact only if attribution and share-alike obligations are preserved; redistribution and deployment terms should be re-reviewed before release.



## Independent external segmentation domain candidate — VISTEC-TP-TH-2021 (2026-10-26)

A reproducible external evaluation path has been added for VISTEC-TP-TH-2021, a separate Thai social-media corpus whose upstream README describes 49,997 samples and word segmentation manually annotated by linguists. The dataset-specific README declares CC-BY-SA 3.0. The pinned source is commit 215a7dc3d384f20eb56af1cbc41fb32b7f8df57c; the CSV Git blob SHA-1 is edfcb85907a604c5e30643065ac4975862a0fe90. Upstream: https://github.com/mrpeerat/OSKut/tree/215a7dc3d384f20eb56af1cbc41fb32b7f8df57c/VISTEC-TP-TH-2021.

The adapter reads the annotated submissionText field, splits pipe-delimited tokens, strips only the documented <ne> and <msp...> annotation tags, and requires exact reconstruction. It intentionally evaluates the annotation's text, not the distinct raw questionText field. The report records the source commit/blob, license, row count, and evidence grade. The external workflow checks out the exact source snapshot, verifies the Git blob SHA and declared license, trains the research-only TUD model from its separate pinned training corpus, evaluates both segmenters, and uploads a report without bundling the third-party dataset.

**Status: IMPLEMENTED; exact workflow run pending.** Until the workflow succeeds, no VISTEC metric is claimed. Even after success, these are metrics against the source's annotations, not independent expert re-adjudication by this project. Keep Wisesight and VISTEC reports separate because annotation conventions and domains differ; neither set may be used to tune the TUD model or production dictionary.


## Independent adjudication and gold promotion gate — 2026-11-01

The 42 frozen challenge prompts now have a **blind Thai review packet** at `data/benchmark/ipa-adjudication-blind.tsv`. It is bound to the challenge JSONL by exact ID, Thai input, stratum and probe; all reviewer fields must remain blank in the committed template. CI checks this invariant. Each expert works on a separate copy, blind to engine output and to the other reviewer.

The packet records lexical reading, word and syllable boundaries, phonemic IPA, optional broad surface IPA, tone categories, vowel length, final glottal status, transcription level, uncertainty and abstention rationale. Narrow acoustic IPA requires an authorized recording reference and time interval. The review validator enforces exact item coverage, one stable reviewer ID per file, qualification reference, ISO review date, explicit abstention and valid acoustic intervals. Pair validation requires distinct reviewer IDs and matching item coverage; it does not automatically resolve disagreements.

The IPA gold registry now records both independent IPA labels, reviewer IDs, adjudicator, outcome, transcription layer, source/license and adjudication record. The scorer rejects one-reviewer labels, inconsistent agreement/disagreement declarations, missing provenance and mixed phonemic/surface layers. It reports metrics separately by profile. **The current gold registry still has zero adjudicated rows, so IPA accuracy remains NOT MEASURED.**

The Ukrainian preference packet `data/benchmark/ukrainian-target-preference-blind.tsv` is candidate-blind but uses six source-attested dictionary IPA references. Its purpose is to review Ukrainian adaptation conditional on those IPA strings, not to adjudicate Thai pronunciation. Every row remains `SOURCE_ATTESTED_NOT_GOLD`; this work cannot be described as end-to-end accuracy. Reviewers independently record preferred Ukrainian forms, syllable-boundary policy, tone-rendering policy, uncertainty and rationale.

## CCOST suitability and remaining access gate

The CCOST paper describes 49 Standard Thai speakers, about seven hours of spontaneous speech plus five hours of controlled word-list/sentence material, and orthographic, word, syllable, phone and toneme annotations. The paper specifies the intended tiers: ORT (orthographic word), KAN (canonical word pronunciation), KAS (canonical syllabified pronunciation), MAU (phonetic segment), MAS (phonemic syllable), and TRN (orthographic utterance transcript). Phonemic and phonetic representations use X-SAMPA; tone numerals map _1=Mid, _2=Low, _3=Falling, _4=High, _5=Rising. The 206-item monosyllabic word list was designed to cross five tones, four initial-consonant types, three syllable structures and vowel length. The paper reports manual correction by trained native Thai research assistants but no formal inter-annotator agreement measures. Zenodo lists a 6.2 GB audio/TextGrid archive under CC BY-NC-SA 4.0. The paper establishes the intended schema; actual released TextGrid conformance and exact label mapping still require local archive inspection. Keep the archive external and preserve non-commercial/share-alike obligations; no CCOST labels are currently counted as this project's independent gold.

Primary references: [LREC 2026 CCOST paper](https://aclanthology.org/2026.lrec-1.247/), [Zenodo CCOST v1.0](https://zenodo.org/records/17366698), [Tingsabadh & Abramson, Thai (JIPA 1993)](https://doi.org/10.1017/S0025100300004746).


## Separate expert word/syllable segmentation gold — 2026-11-01

The blank `data/benchmark/segmentation-adjudication-gold.tsv` registry is reserved for two-reviewer word- or syllable-boundary adjudication. Each row declares `segmentation_layer=WORD|SYLLABLE`, preserves both original token arrays, two distinct reviewer IDs and qualification references, an adjudicator, outcome, record, source URL and license. The scorer checks exact reconstruction, requires consensus labels to match the final gold, requires different raw tokenizations for a resolved disagreement, and refuses to mix WORD and SYLLABLE reports. The existing Wisesight rows remain source-annotated WORD evidence; they are not promoted to expert gold.

No expert segmentation rows have been submitted yet. The new registry is intentionally header-only and does not create an accuracy metric.


The adjudication infrastructure and three-mode fallback correction are verified by full CI 41337529189 and Web Static 41337815975. This does not add expert labels: the adjudicated segmentation registry remains header-only and all 993 Wisesight records retain SOURCE_ANNOTATED status.


The project-authored 42-item Thai challenge set is registered as input-text provenance for independent expert gold (`CLIPPYFIRST-THAI-CHALLENGE-CC398`). This does not turn the prompt text into phonetic evidence: pronunciation labels must still be independently supplied, qualified, and adjudicated. This registry record allows the IPA scorer's `IPA_GOLD_INPUT` gate to be satisfied without treating Wiktionary or a model-derived corpus as gold.
