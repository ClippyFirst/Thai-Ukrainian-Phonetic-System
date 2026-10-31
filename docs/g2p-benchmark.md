# Independent Thai G2P benchmark: candidate screening and protocol

Status: **pinned raw-output smoke verified; independent accuracy remains unmeasured**  
Last reviewed: 2026-10-20

This document evaluates candidate external engines for use as *comparators*, not as a replacement for the repository's structural analysis. An upstream accuracy claim is not a score for this project. No candidate is integrated as a runtime dependency by this screening alone.

## Requirements for a fair comparison

1. Freeze an explicit Thai input set and gold reading per item before running candidate systems.
2. Record source, dialect/register, lexical reading, segmentation, phonemic IPA, broad surface IPA, tone category, vowel length, and word/syllable boundaries separately.
3. Preserve each engine's raw output and version/configuration. Normalize only documented representational differences (for example, tie-bar encoding); do not silently delete tone or length.
4. Score separately:
   - lexical word segmentation exact match;
   - syllable boundary exact match;
   - segmental IPA exact match;
   - vowel-length accuracy;
   - tone-category accuracy;
   - phonemic-vs-surface representation compatibility;
   - coverage and unsupported/OOV behavior.
5. Keep lexical items, learned/Indic readings, loanwords, and special orthography in separate strata.
6. Use independently adjudicated references. Wiktionary-derived references cannot count as independent evidence for an engine whose dictionary or reported benchmark includes Wiktionary-derived records.
7. Publish false positives as well as successful cases. No engine output is treated as gold merely because it is fluent or phonotactically plausible.

## Candidate screening

| Candidate | Code / runtime | IPA and structure | Data/model considerations | Screening decision |
|---|---|---|---|---|
| [thaiphon](https://github.com/5w0rdf15h/thaiphon) | Repository states Apache-2.0; core has no runtime dependencies and supports Python 3.10+ | Offers an IPA renderer, syllable objects, vowel length, onset/coda and tone. Word boundaries and lexical readings depend materially on the optional `thaiphon-data-volubilis` package. | The companion VOLUBILIS-derived lexicon is separately licensed CC-BY-SA 4.0. Upstream README reports roughly 57% exact match without that lexicon and roughly 75% with it against its stated Wiktionary etalon; those figures are upstream claims, not this project's results. | **First comparator candidate.** Pin release/commit and test core and optional lexicon separately. Audit source overlap before scoring. |
| [FastThaiG2P](https://github.com/awslabs/FastThaiG2P) | Repository LICENSE is Apache-2.0; pure-Python G2P runtime documents PyThaiNLP tokenization as its runtime dependency. Optional TTS has a substantially larger model/runtime footprint and is out of scope. | Dictionary output uses IPA with tone contours, length, syllable dots and spaces; OOV fallback is rule-based. The project's own README says the fallback may differ from native lexical pronunciation. | Its 62k-word dictionary is merged from manual overrides, Wiktionary-derived IPA, and generated entries; provenance and licenses differ by source. Must audit per-entry metadata and source overlap. | **Second comparator candidate.** Compare dictionary hits and OOV fallback as separate strata; do not treat generated entries as independent gold. |
| [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp) | Project code Apache-2.0; project documentation identifies data/model licenses including CC0-1.0 and CC-BY-4.0. The license of the selected model/data must be checked separately. | It is a toolkit and dispatcher, not one fixed G2P model. Documented choices include `thaig2p`, `tltk_ipa`, `thaig2p_v2`, `thaig2p_v4`, `umt5_thaig2p`, and `fastthaig2p`; requirements and outputs differ. | Model cards, model versions, dependencies and weights must be pinned for the exact engine selected. An API name alone is not a reproducible configuration. | **Comparator family, not one score.** Choose one concrete engine/version after dependency and model-card review; do not count FastThaiG2P twice as an independent engine. |

## Corpus priorities

A candidate-only seed list is committed at [`data/benchmark/thai_g2p_challenge.jsonl`](../data/benchmark/thai_g2p_challenge.jsonl). Its records deliberately have null gold fields and `not_adjudicated` statuses; they are coverage prompts, not labeled examples and must not be scored as gold. The 2026-10-27 continuation adds six article-style probes (`ยูเครน`, `ประเทศยูเครน`, `ยูเครนเป็นประเทศหนึ่ง`, `เป็นประเทศหนึ่ง`, `ยุโรปตะวันออก`, `ประเทศในยุโรปตะวันออก`) to test proper-name/OOV and continuous-text behavior seen in a real pasted article. These are diagnostic prompts only: no Thai IPA, tone, syllable boundary, or word boundary is asserted. A pinned optional external run on 2026-10-27 processed all 42 inputs with three comparators (126 raw rows): thaiphon 0.7.0 and FastThaiG2P 0.1.0 returned output for all 42 each; Goruut returned no words for 16/42 overall, including all six article-style probes. The six exact raw-output comparisons are preserved in [`data/benchmark/runs/article-style-external-g2p-2026-10-27.json`](../data/benchmark/runs/article-style-external-g2p-2026-10-27.json) and run [40507249579](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40507249579). FastThaiG2P produced compact candidate outputs for the article phrases, while thaiphon produced many slash-separated fragments; this is a useful discrepancy to adjudicate, **not** a conclusion that one engine is more accurate. Independent gold count remains zero. The file should be adjudicated and versioned before any accuracy run.

The first frozen challenge set should include at least these strata:

- **Core contrasts:** short/long vowels, aspiration, final-stop neutralization, all five tone categories, live/dead syllables and class/mark interactions.
- **Special orthography:** `รร`, `ฤ/ฤๅ`, `ฦ/ฦๅ`, lexical `ทร`, false clusters such as `จร/สร/ศร/ซร`, and silent consonants/การันต์.
- **Word boundaries:** known multi-syllable words, ambiguous Thai segmentation, spaces/punctuation, and unknown continuous Thai text.
- **Lexical/register variation:** loans, learned readings, colloquial variants, and words with multiple accepted pronunciations.
- **Adversarial inputs:** invalid tone-mark combinations, impossible codas, unsupported symbols, and malformed spellings. These test abstention, not pronunciation accuracy.

Each record must distinguish:
- `orthography_validity`: valid / invalid / unresolved;
- `structural_parse_status`: supported / uncertain / unsupported;
- `lexical_attestation_status`: attested / unattested / not_checked;
- `gold_phonemic_ipa` and `gold_broad_surface_ipa`;
- `gold_tone_category`, `gold_vowel_length`, `gold_syllable_boundaries`, and `gold_word_boundaries`;
- citations, source dates, dialect/register and adjudication notes.

## Reproducible run manifest

Every benchmark run must write a machine-readable manifest with:

- repository commit SHA and corpus version/hash;
- engine package version and source commit;
- Python version, platform, dependencies and model/lexicon versions;
- exact engine configuration and text-normalization options;
- source provenance for every gold record and every external dictionary where available;
- metrics by stratum plus aggregate coverage, not just one exact-match percentage.

## Decision gate for integration

An external engine may be integrated only if a pinned, reproducible run demonstrates measurable benefit on an independently adjudicated test set without concealing regressions in tones, length, segmentation, or special-orthography strata. Until that gate is met, engines remain optional benchmark comparators and the deterministic in-repository parser remains the source of structural interpretation.

## References checked

- thaiphon repository and README: https://github.com/5w0rdf15h/thaiphon
- FastThaiG2P repository and README: https://github.com/awslabs/FastThaiG2P
- PyThaiNLP repository: https://github.com/PyThaiNLP/pythainlp
- PyThaiNLP transliteration API documentation: https://pythainlp.org/dev-docs/api/transliterate.html


## Running candidate engines reproducibly

The optional runner [scripts/run_external_g2p_benchmark.py](../scripts/run_external_g2p_benchmark.py) is deliberately outside the production import path. It stores raw output, elapsed time, engine/version metadata and failures for every candidate/input pair. It does not install either engine and does not modify runtime dependencies.

Create an isolated environment (Python 3.10+):

```bash
python -m venv .venv-g2p-benchmark
# Linux/macOS:
. .venv-g2p-benchmark/bin/activate
# Windows PowerShell:
# .\.venv-g2p-benchmark\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install "thaiphon==0.7.0"
python -m pip install "FastThaiG2P @ git+https://github.com/awslabs/FastThaiG2P.git@c4759eef7df03e11fcbb9aa83efe8cf21709fd2f"
python scripts/run_external_g2p_benchmark.py --engine all
```

To isolate the effect of thaiphon's optional lexicon, run a separate environment with the companion package installed and preserve that output under a distinct filename. The lexicon is a separately licensed CC-BY-SA 4.0 data package; do not bundle it or imply the engine's Apache-2.0 license covers the lexicon. Check the companion package's current version and metadata before installation.

```bash
python scripts/run_external_g2p_benchmark.py --engine thaiphon --output data/benchmark/runs/thaiphon-base.jsonl
python scripts/run_external_g2p_benchmark.py --engine fastthaig2p --output data/benchmark/runs/fastthaig2p.jsonl
```

The default output path is a local run artifact and is not committed automatically. Store outputs with environment metadata (Python version, OS, exact package versions, lexicon presence, commit and corpus SHA-256) when publishing a run. Because the challenge corpus currently has no adjudicated gold, this runner is a smoke-test and evidence-capture harness only. It intentionally labels raw-string equality as diagnostic, not accuracy: candidate engines have different tone notation, IPA conventions and segmentation behavior. Do not publish an accuracy ranking until independent gold labels and explicit per-engine normalization/scoring rules are frozen.


## Optional CI smoke workflow (2026-10-24)

The branch adds `.github/workflows/optional-external-g2p.yml`, pinning `thaiphon==0.7.0`, `pythainlp==5.4.0`, and FastThaiG2P commit `c4759eef7df03e11fcbb9aa83efe8cf21709fd2f`. It stores raw candidate outputs plus a run summary as a CI artifact. The optional VOLUBILIS lexicon is intentionally not installed, so the thaiphon run is the base-engine configuration. This is a smoke/diagnostic run against a candidate-only corpus whose gold fields are null; it cannot yield accuracy. Acceptance is pending the workflow result and artifact inspection. No production dependency is added.


## First pinned smoke run — 2026-10-24

- Workflow: [40092505291](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40092505291); artifact `thai-external-g2p-smoke`, SHA-256 `9b2776de9be93f15d16c52b0c336fd196db7b41de6513394ac4a8f9b09218a78`.
- Environment: Python 3.12.15; `thaiphon==0.7.0` without the optional VOLUBILIS lexicon; PyThaiNLP 5.4.0; FastThaiG2P 0.1.0 from upstream commit `c4759eef7df03e11fcbb9aa83efe8cf21709fd2f`.
- Coverage: 36 challenge prompts × 2 engines = 72 raw output rows; 0 initialization/transcription errors; 0 independently adjudicated gold labels; 0 scored comparisons. The harness correctly leaves the gold count and raw-string diagnostic count at zero.
- Diagnostic examples: `ไกล` → thaiphon `/kaj˧/ /la˦˥/`, FastThaiG2P `/klaj˧/`; `จริง` → thaiphon fallback `/tɕa˨˩/ /ri˦˥/ /ŋa˦˥/`, FastThaiG2P `/t͡ɕiŋ˧/`. These examples identify a high-priority lexical/OOV/segmentation investigation, not a score: neither output is a gold label and the thaiphon run deliberately omitted its optional lexicon.
- Task status: reproducible raw-output smoke **DONE_VERIFIED**; phonological accuracy and engine selection remain **BLOCKED** on independently adjudicated, provenance-audited gold data and convention-aware evaluation. No engine was added to production dependencies.


## Merge status (2026-10-24)

The pinned raw-output smoke workflow and documentation are merged to main at `bbe9298b2e643d78c0f9f27127482cfda0c62315`. CI run [40093256851](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40093256851) passed tests and the generated master artifact check; optional smoke [40093259692](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40093259692) passed. Accuracy remains unmeasured until the challenge corpus has independent source-located gold.


## Post-merge main run (2026-10-24)

The main-branch smoke run [40093730177](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40093730177) passed. Inspected artifact SHA-256 `9044719e206505158c9fc1c5da36a9bc8c34d60b4a829b6e98e7623e63b6374a` contains 72 outputs, 0 runtime errors, 0 gold-labeled rows, and 0 scored raw-string comparisons. This is raw-output coverage only, not accuracy.


## External benchmark expansion — 2026-11-01

This review adds candidate datasets to the existing harness; it does not claim a new accuracy score.

### Thai G2P v4: IPA dictionary benchmark candidate

- Dataset card: https://huggingface.co/datasets/pythainlp/thai-g2p-v4-dataset
- Upstream builder: https://github.com/PyThaiNLP/thai-g2p-v4
- Declared dataset license: CC0-1.0. The card exposes `word`, `pronunciation`, and `ipa` fields and reports 126,718 train, 10,055 validation, and 8,076 test rows (144,849 total).
- The card states that the corpus is built from Thai W2P and a Wiktionary `th-pron` transliterator, and that splits are grouped by the first two characters. This is useful lexical coverage and a reproducible held-out dictionary comparison, but it is **not independent acoustic or expert-adjudicated gold**. The declared CC0 status should be preserved as the dataset card's claim; upstream source provenance and any source-level terms must still be reviewed before redistributing rows.
- Recommended use: evaluate the test split only, preserve raw IPA, report strict NFC exact match plus separate tone/length/syllable-boundary diagnostics, and stratify by lexical item type. First run a source-overlap audit against `data/thai/lexical_ipa_overrides.tsv` and the sources of any other runtime lexicons. Rows derived from a runtime override or a shared upstream dictionary must be marked circular/non-comparable, not counted as independent accuracy evidence.
- Do not train or tune on the test split. Do not add the dataset as a production dependency or bundle a copy in the repository. The existing `scripts/benchmark_ipa.py` harness is the scoring boundary once provenance-qualified records are exported into its gold/prediction format.

### Word-segmentation benchmark candidates

| Corpus | Published scale / task | Recommended role | Gate |
|---|---|---|---|
| BEST-2010 / InterBEST2010 | Official TEST_100K described as 2,252 samples, about 128k words and 496k characters; word boundaries | Primary standard-domain Thai segmentation benchmark | Dataset access/licensing is non-commercial/share-alike in published catalogues; verify exact terms and split integrity before use. Do not redistribute raw corpus. |
| LST20 | 74,180 sentences, 3,164,002 words; word boundaries plus POS, NER, clause and sentence layers | Large news-domain out-of-domain segmentation evaluation | NECTEC terms allow non-commercial research/open-source use but prohibit modification and redistribution without permission; commercial use requires a separate arrangement. Keep remote/local data external and seek permission before derived-data publication. |
| Wisesight-1000 | Existing pinned 993 source-annotated rows | Small social-media test-only diagnostic | Already integrated; source annotations are not independent expert adjudication. |
| VISTEC / TUD | Existing pinned social-media evaluation and TUD train/dev/test model | Cross-domain and comparative segmentation diagnostics | Already integrated; preserve source licenses, held-out partitions and evidence grades. |

### Speech corpora: useful, but not text-to-IPA gold

- FLEURS provides parallel read-speech evaluation material across 102 languages, including Thai. It is appropriate for ASR/recognition experiments, not direct scoring of Thai orthography-to-IPA or Thai-to-Ukrainian text output without a separately adjudicated phonetic transcription layer.
- Mozilla Common Voice Thai is a large read-speech resource (the current surfaced 27.0 card reports 366,656 clips and 427.12 hours, including 173.36 validated hours). It can support acoustic/ASR robustness work, but its intended ASR transcripts are not phone-level gold. Respect the dataset's CC0 declaration and explicit prohibition on speaker identification and re-hosting/redistribution.
- CCOST remains the most directly relevant phone/toneme-level candidate already registered in this repository. Its manual and item-level annotation protocol remain uninspected, so it stays BLOCKED for benchmark row selection until the manual is reviewed.

### Benchmark portfolio decision

1. **Segmentation:** retain current Wisesight/VISTEC/TUD evaluations; add BEST-2010 as the next high-priority external benchmark after access and license verification; treat LST20 as gated/non-redistributable.
2. **Thai G2P / IPA:** add Thai G2P v4 as a large source-attested dictionary comparator, but report circular-source exclusions and never label it independent gold.
3. **Acoustic phonetics:** prioritize CCOST manual review; FLEURS/Common Voice are secondary audio/ASR resources, not substitutes for phone-level annotation.
4. **Ukrainian target rendering / end-to-end:** no suitable independent Thai-to-Ukrainian gold benchmark was found. Continue with independent Ukrainian-native adjudication and a frozen end-to-end test set; do not derive gold by consensus among the system and its comparator engines.

No new corpus was downloaded, copied, or bundled in this update. No external score was calculated. The repository's existing accuracy fields remain null until independently adjudicated labels and source-overlap checks are available.

### Primary references reviewed

- PyThaiNLP Thai G2P v4 dataset card: https://huggingface.co/datasets/pythainlp/thai-g2p-v4-dataset
- Thai G2P v4 dataset builder: https://github.com/PyThaiNLP/thai-g2p-v4
- BEST-2010 evaluation details (official test split statistics): https://attapol.github.io/papers/thai_tokenization_manu_coling2020.pdf
- NLP for Thai corpus catalogue and stated BEST/Wisesight license metadata: https://nlpforthai.com/tasks/word-segmentation/
- NECTEC LST20 corpus record and usage conditions: https://opend-portal.nectec.or.th/en/dataset/lst20-corpus
- LST20 dataset card and terms: https://huggingface.co/datasets/lst-nectec/lst20
- FLEURS dataset card: https://huggingface.co/datasets/google/fleurs
- Mozilla Common Voice Thai 27.0 datasheet: https://mozilladatacollective.com/datasets/cmu5x5tj000f2nq0755h8qcy5
- CCOST LREC 2026 paper: https://aclanthology.org/2026.lrec-1.247/
