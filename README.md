# Thai → Ukrainian Phonetic-Graphemic Correspondence System

Research-oriented, machine-readable reference implementation for mapping contemporary Standard Thai orthography through graphemic structure, phonology and IPA into a Ukrainian phonetic/phonological target.

## Research pipeline

**Non-negotiable architecture invariant:**

`Thai orthography → structural analysis → Thai phonology → typed, inspectable IPA → Ukrainian adaptation from IPA → Ukrainian practical orthography`.

The Thai → IPA stage must resolve the source-language analysis as far as the available evidence permits. The IPA result is a real intermediate representation and the **only** input contract for Ukrainian adaptation—not an audit-only side output. No parallel Thai-grapheme → Ukrainian path, direct vowel-ID mapping, or direct Thai-coda-to-Ukrainian mapping may independently generate the final Ukrainian result.

The typed `PhoneticResult` is that adapter boundary. It carries phonemic IPA and conservative broad surface IPA separately, alongside segment and syllable boundaries, vowel length, tone, provenance, and uncertainty. The Ukrainian adapter consumes the typed IPA result and its declared metadata; it must not inspect Thai graphemes, vowel IDs, or Thai coda fields to decide Ukrainian output. Ukrainian practical orthography is produced only after this IPA-to-Ukrainian adaptation. If the Thai reading or required IPA features cannot be supported, the system must withhold or explicitly qualify downstream output instead of silently guessing.

**Acceptance rule:** test the whole chain `Thai input → IPA intermediate → Ukrainian output`, including tests proving that changing/withholding the IPA result changes/withholds the Ukrainian result accordingly. Python and browser implementations must obey the same boundary and pass cross-runtime parity checks.

The browser IPA adapter is maintained as a separately tested implementation. Cross-runtime parity tests remain required; passing a Python test alone does not establish browser parity. This is **not RTGS** and not a Thai-character → Ukrainian-character substitution table.

## Scope

Primary scope: contemporary Standard Thai with a Bangkok/central-standard reference where the evidence permits.

The model distinguishes:

- grapheme vs phoneme;
- consonant class vs phonetic realization;
- vowel sign vs vowel nucleus;
- tone mark vs phonological tone;
- orthographic order vs phonological order;
- structural combinations vs valid orthography vs phonotactic possibility vs attestation;
- phonemic/broad IPA vs narrower surface phonetics;
- Ukrainian candidate ranking vs a calibrated probability or a unique orthographic answer.

## Implemented

- 44 Thai consonant graphemes with class and positional data.
- Vowel-sign parsing including interleaved Thai spelling and a machine-declared glide/rime registry.
- Conservative complex-onset licensing: arbitrary consonant adjacency is not promoted to a Thai cluster without structural evidence.
- Live/dead syllable classification and explicit tone-bearing consonant-class selection for clusters.
- Five-tone engine with explicit invalid combinations.
- ห นำ handling as an explicit orthographic/phonological transformation.
- Broad phonological and conservative surface-phonetic layers with explicit syllable-internal positional IPA.
- Feature-distance Ukrainian candidate generation using the canonical Ukrainian target snapshot.
- Evidence/provenance registry.
- Machine-readable tone-rule registry consumed by the tone engine.
- Explicit special-orthography analysis layer for lexical/context-dependent constructions.
- Machine-readable context-dependent orthographic rule registry, including role classification for อ.
- Publication-ready orthographic correspondence table generated from the same rule registry used by the parser.
- External lexicon adapter for evidence-backed syllable segmentation.
- Conservative dictionary maximum-matching segmenter backed by a pinned CC0 word list, evaluated separately from the held-out Wisesight source-annotated benchmark.
- Reproducible research-only unigram Viterbi segmentation training experiment on pinned UD Thai TUD train/dev/test splits; Wisesight is never used for training or tuning, and the CC BY-SA 4.0 model artifact preserves attribution/share-alike metadata.
- Project-defined Ukrainian orthographic candidate layer with tone kept separate.
- Generated source→parser→derived consistency manifest enforced by CI.
- Structural combinatorial-space accounting.
- Machine-readable analysis and corpus-record schemas.
- Deterministic JSONL evaluation API and CLI.
- Explicit word model with standalone / initial / medial / final syllable positions.
- Positional regression tests and a documented segmentation boundary.
- Separate generated Thai-consonant and Thai-vowel correspondence tables exposing phonemic IPA, conservative surface IPA, position/context, and Ukrainian candidates derived from IPA.
- Adversarial rejection of non-conforming consonant sequences such as แสดง when supplied as one syllable.
- Evidence-gated handling of false clusters `จร`, `สร`, `ศร`, `ซร` and lexical `ทร` instead of forcing written ร into pronunciation.
- Regression coverage for preposed-vowel true clusters such as `ไกล` /klaj/ and the tone pair `ไกล` vs `ใกล้`.
- Adversarial rejection of multiple tone marks, unconsumed vowel signs and unsupported symbols instead of silently dropping them.
- Regression, negative-input and generated-artifact tests.
- GitHub Actions CI that regenerates derived artifacts and verifies a clean tree.
- Citation metadata, license and research release protocol.

## Whole-text browser output

The browser interface provides two explicit modes. **Strict** (default) preserves the fail-closed contract and withholds IPA/Ukrainian output for unreviewed spans. **Soft** opt-in mode attempts a greedy structural syllable parse for otherwise unknown spans and routes any resolved candidate through the same IPA → Ukrainian adapter; it clearly labels those results as provisional and preserves markers for spans that remain unresolved. Soft segmentation is not a lexical word-boundary claim or a validated pronunciation. The browser interface presents a single copyable Ukrainian phonetic candidate for the full input, alongside a single IPA intermediate output. Source whitespace and punctuation are preserved; syllables within a known word are joined in the Ukrainian candidate, and adjacent recognized Thai segments are separated for Ukrainian readability. Detailed per-segment and per-syllable diagnostics remain available in a collapsible section. Unsupported or unresolved Thai spans are explicitly marked in the continuous output rather than silently omitted or guessed. The mode selector lets users trade strict abstention for a more recall-oriented provisional candidate without changing the default behavior. This improves usability, but does not imply that arbitrary long Thai prose has been linguistically validated or that every word is recognized.

### Pasted article preprocessing

The browser input now has a conservative preprocessing step for recognizable Wikipedia/Markdown/HTML markup: it removes link destinations and common reference markup while retaining visible link labels, decodes common and numeric HTML entities, and shows a notice when the input was changed. Plain unmarked text is passed through unchanged. This is input hygiene, **not** Thai word segmentation or pronunciation inference; it does not make long article text linguistically validated, and it must not be used as evidence that a candidate pronunciation is correct.

## Current release status

**v0.6.1 — research-oriented reference implementation with explicit lexical readings and text-pipeline safeguards.**

The repository is suitable as a transparent research foundation and reference implementation. It includes machine-readable tone rules, special-orthography analysis, evidence-gated lexical readings, external lexical segmentation support, a Ukrainian orthographic candidate layer, and source→parser→derived consistency checks. CI workflows check structural reproducibility, Python regression tests, and browser parity; a commit should be called CI-verified only after its own relevant workflow runs succeed. Empirical corpus accuracy remains explicitly unclaimed.

It is **not** yet an empirically validated benchmark. No corpus accuracy percentage is claimed because a declared gold corpus has not been processed by CI.

### Evidence-gated limitations

- the default public text endpoint remains conservative and withholds phonetic output for unknown unsegmented Thai spans; an opt-in dictionary segmenter exists, and a separately trained TUD unigram-Viterbi experiment remains research-only: exact-head CI and initial cross-domain metrics are recorded in `docs/validation-matrix.md`, but the recall-heavy profile, limited exact-group rates and lower Wisesight precision do not justify production-default integration pending independent error review and a separately defined acceptance gate;
- special orthography is represented conservatively as explicit analysis-dependent alternatives where lexical evidence is required;
- connected-speech narrow phonetics still requires acoustic/phonetic evidence;
- corpus-calibrated probabilities still require a gold dataset;
- Ukrainian orthographic candidates are project-specific and not an official normative standard.

These are evidence gates, not hidden software gaps.

## Quantitative accounting

The generated syllable-space report gives a **structural upper bound**, not the number of Thai syllables:

- initial grapheme options: 44;
- declared vowel/rime records: 41;
- structural coda grapheme options used by the generator: 38;
- tone-mark states: 5;
- combined structural upper bound: 351,780 (44 × 41 × (1 + 38 coda options) × 5 tone-mark states).

This must not be interpreted as a count of valid, lexical or corpus-attested Thai syllables.

## Word and positional model

The reference implementation can analyze an explicitly segmented word with `analyze_word_syllables(["กา", "นา", "มา"])`. It preserves syllable index and position without pretending that Thai orthography alone provides universal word segmentation. See `docs/word-and-position-model.md`.

## Evidence and validation

Core evidence includes Royal Institute of Thailand materials, Tingsabadh & Abramson (1993), corpus-based Thai phoneme-distribution work, CCOST and Thai G2P resources. Third-party corpora are not redistributed.

See:

- Research protocol: docs/research-protocol.md
- Corpus validation: docs/corpus-validation.md
- Evidence registry: docs/evidence.md
- Final audit: docs/final-audit.md
- Independent IPA and Ukrainian target-form adjudication protocol: docs/independent-adjudication-protocol.md

## User interface

The research core is also available as an installable `thai-ua` CLI with single-input analysis, TXT/CSV/TSV/XLSX batch processing and a local JSON API. Excel support is optional: `pip install -e ".[excel]"`.

Examples:

```powershell
thai-ua analyze "กา"
thai-ua batch words.csv -c thai -o results.xlsx
thai-ua serve
```

See `docs/cli-batch-api.md` for the complete CLI and API reference.

## Reproducibility

From a clean Python environment:

~~~bash
pip install -e .
python scripts/generate_derived.py
python scripts/generate_syllable_space.py
python -m unittest discover -s tests -v
~~~

For an external gold JSONL corpus:

~~~bash
python scripts/evaluate_corpus.py path/to/records.jsonl
~~~

For a licensed, adjudicated word-segmentation TSV and matching prediction TSV:

~~~bash
python scripts/evaluate_segmentation.py --gold data/benchmark/segmentation-gold.tsv --predictions data/benchmark/segmentation-predictions.tsv --output reports/segmentation-benchmark.json
~~~

The independent IPA-gold manifest remains empty until a versioned, license-compatible set is independently reviewed. The segmentation evaluator separately supports the pinned 993-row Wisesight source-annotated set, but it must not be described as independently adjudicated gold. A no-gold IPA run is `NOT_MEASURED`, not an accuracy score. See `docs/corpus-validation.md` for resource/license boundaries and the required evaluation protocol.

The evaluator reports numerators and denominators explicitly and excludes missing gold fields from the relevant metric.


## Web service

The repository includes a static two-page web application under `web/`:

- `web/index.html` — public Service interface for Thai analysis;
- `web/system.html` — methodology and evidence page;
- `web/src/engine.js` — browser-safe implementation of the declared analysis pipeline;
- `web/tests/fixtures.json` — versioned parity probes;
- `scripts/generate_web_fixtures.py` — generates the authoritative fixture values from the Python core.
- `scripts/generate_web_word_dictionary.py` — validates the pinned CC0 word-list snapshot and creates an ignored, reproducible browser index before browser tests and Pages packaging. The index uses two-code-point prefix buckets (with a one-code-point fallback for single-character entries) to reduce candidate scans; it carries boundary evidence only, not pronunciation data.

The browser uses the CC0 list for **word-boundary evidence only**. A dictionary match does not imply a known pronunciation: IPA and Ukrainian output are still withheld unless the word has curated syllabification or a typed source-attested IPA override. To run browser tests locally, first run `python scripts/generate_web_word_dictionary.py`; the generated `web/src/word-dictionary.generated.js` is a build artifact and is not committed.

The web CI gate compares the browser engine against the Python reference on the same probes before the Pages artifact is eligible for deployment. GitHub Pages is a static presentation/deployment layer; it does not run the Python package server-side.

## Research workspace

- Notion: https://app.notion.com/p/3ec40df389698138be8beb43b78971a2?pvs=204
- Lucid: https://lucid.app/lucidchart/bd12788f-bec1-4f10-a01d-0def1efea509/view

## Citation

Use the repository's CITATION.cff. The software is released under the MIT License.

## Final principle

A result is only called **empirical** when it has a named/versioned evidence source and an explicit evaluation denominator. Structural generation, heuristic candidate ranking and documented linguistic rules are valuable research components, but they are not substitutes for corpus validation.


## Master correspondence table

The repository can deterministically generate an exhaustive structural Thai → Ukrainian master table using the IPA-first pipeline. It contains 351,780 structural rows from 44 initial graphemes, 41 vowel/rime records, 38 coda options plus open syllables, and 5 tone-mark states. The downloadable generated artifacts are attached to the **master-artifact** CI job; see `docs/master-correspondence-table.md` for semantics and limitations.


## Text analysis pipeline

Version 0.6 adds a text-level preprocessing layer above the syllable analyzer:

- Unicode-aware tokenization separates Thai text, punctuation, Latin text, numbers, and Thai repetition/orthographic markers.
- A curated lexical segmentation layer can split known multisyllabic Thai words into explicit syllable units before phonological analysis.
- Unknown Thai words are **not guessed**: they remain marked as segmentation-unresolved, preserving the research system's evidence-first policy.
- Browser and Python implementations share the same regression probes for tokenization and segmentation.

This layer deliberately does not claim general-purpose Thai word segmentation. Expanding the lexical corpus is a separate evidence-gated task.


## 0.6.1 adversarial hardening

The text pipeline now distinguishes productive orthographic parsing from evidence-gated lexical readings for high-frequency irregular spellings. Regression coverage includes silent-marker words (e.g. จันทร์, ศุกร์, เสาร์, สัตว์, ฟิล์ม), false-cluster readings (จริง, สร้าง, เศร้า, ไซร้), อ นำ forms (อย่า, อยู่, อย่าง, อยาก), and ฤ/ฤๅ readings (ฤดู, ฤทธิ์, ฤๅษี, ทฤษฎี). Lexical readings are explicit data, not a claim that arbitrary Thai text can be segmented or pronounced without lexical evidence.


## External IPA renderers and G2P candidates

The research registry records external pronunciation engines, IPA dictionaries, and Unicode IPA display fonts without treating unvalidated output as ground truth. See [`docs/external-ipa-renderers.md`](docs/external-ipa-renderers.md) and the machine-readable [`data/external-ipa-renderers.json`](data/external-ipa-renderers.json). These are candidate inventories only; no third-party engine is enabled by default, and the ClippyFirst IPA → Ukrainian adapter remains the sole target adaptation boundary.


### Run the ClippyFirst challenge set (runtime diagnostics)

To inspect how the current engine handles each challenge input—including segmentation status, phonemic/surface IPA, tone, vowel length, Ukrainian output, and abstention—run:

```bash
python scripts/run_challenge_diagnostics.py
```

The report is written to `reports/challenge-runtime-diagnostics.json`. This is a runtime and abstention diagnostic, **not** an accuracy benchmark: the challenge set does not yet contain independently adjudicated Thai IPA and word-boundary gold. Unknown multi-grapheme words remain unresolved rather than receiving guessed output. Use `--input` and `--output` to select alternate paths.


## Pinned evaluation resources (2026-10-25)

- `data/benchmark/segmentation-gold.tsv` contains 993 human source-annotated word-tokenization records from PyThaiNLP/Wisesight, pinned to upstream commit `c1d063649abc3a6870b5fd1aae26cd1c64bdde7b` and licensed CC0-1.0. They are marked `SOURCE_ANNOTATED`, held out as test-only, and are **not represented as independently expert-adjudicated labels**. Provenance and conversion rules are in `data/benchmark/wisesight1000-source.json`.
- `scripts/run_wisesight_segmentation_diagnostic.py` evaluates the existing no-automatic-word-segmentation baseline and preserves the gold evidence grade in the JSON report. CI validates dataset integrity and uploads the report.
- `data/benchmark/source-attested-ipa.tsv` contains six revision-pinned dictionary IPA/tone/vowel-length records, marked `SOURCE_ATTESTED_NOT_GOLD`. These are useful for review and error triage, not independent accuracy scoring.
- Five source-attested lexicon entries are documented in `data/thai/text_lexicon_sources.csv`. Their CC BY-SA 4.0 data provenance is separate from the MIT software license; see `data/thai/TEXT-LEXICON-DATA-LICENSE.md`.
- The word `เงิน` now has a narrowly scoped typed lexical-IPA override (`data/thai/lexical_ipa_overrides.tsv`) preserving source-attested short /ɤ/, mid tone, source revision, and license through the same `PhoneticResult` → Ukrainian adapter boundary. This dictionary transcription is not independent expert/acoustic gold; no general lexical override behavior is inferred from this single entry.


Segmentation source decisions are tracked in [`data/corpus_sources.csv`](data/corpus_sources.csv). LST20 and VISTEC are candidate sources only and are not bundled; their license and annotation compatibility must be reviewed before use. The pinned Wisesight snapshot remains test-only and must not be used for training or lexicon construction.


For a text-only discrepancy report over the six pinned dictionary IPA records, run `python scripts/run_source_attested_ipa_diagnostic.py --output /tmp/source-attested-ipa-diagnostic.json`. It compares segmental IPA, tone categories, and vowel-length metadata without claiming accuracy. The `เงิน` override is mirrored in the browser adapter and covered by a cross-runtime fixture; the latest browser parity head's CI status is recorded in the execution matrix and handoff.


## Segmentation evaluation and evidence grades

The pinned Wisesight source-annotated benchmark remains test-only. The TUD unigram-Viterbi segmenter is research-only and must not replace the dictionary baseline on the strength of source-label metrics alone.

An additional opt-in GitHub Actions workflow evaluates both systems on the separately sourced VISTEC-TP-TH-2021 social-media corpus. It checks out the exact upstream commit and CSV blob, converts pipe-delimited annotated tokens from the upstream submissionText field, verifies lossless reconstruction, and uploads a JSON report. The source dataset is not bundled. Its dataset README declares CC-BY-SA 3.0; attribution and share-alike obligations apply.

Run the external workflow from the Actions tab or by changing the relevant adapter/scorer/workflow files in a pull request. Report metrics remain explicitly SOURCE_ANNOTATED, not independently re-adjudicated gold. The workflow does not use VISTEC to train or tune either system. See docs/corpus-validation.md and docs/independent-adjudication-protocol.md for provenance and limitations.
