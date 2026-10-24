# Independent Thai G2P benchmark: candidate screening and protocol

Status: **candidate screening complete; pinned optional smoke workflow added; empirical run pending CI artifact review**  
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

A candidate-only seed list is committed at [`data/benchmark/thai_g2p_challenge.jsonl`](../data/benchmark/thai_g2p_challenge.jsonl). Its records deliberately have null gold fields and `not_adjudicated` statuses; they are coverage prompts, not labeled examples and must not be scored as gold. The file should be adjudicated and versioned before any accuracy run.

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
