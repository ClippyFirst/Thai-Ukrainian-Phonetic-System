# External Thai G2P and segmentation systems — comparison register

**Purpose:** identify reproducible comparators and design patterns for ClippyFirst's Thai → typed IPA → Ukrainian pipeline. This register does not authorize importing outputs as truth, copying code/data, or changing the project's IPA-first adapter boundary.

## Candidate systems inspected

| Resource | Verified public repository facts | Useful comparison | Restrictions / caveats | Decision |
|---|---|---|---|---|
| [FastThaiG2P](https://github.com/awslabs/FastThaiG2P) | Public Python project; repository metadata declares Apache-2.0. README describes text normalization, PyThaiNLP newmm tokenization, a 62k IPA dictionary, and a TLTK-derived syllable-parser fallback. | Strong candidate for an optional external baseline on shared Thai inputs; compare normalization, OOV coverage, segmentation and IPA, separately. | A repository-level license does not automatically settle every bundled corpus, generated dictionary entry, or vendored component's provenance. Inspect per-file notices and upstream terms before reuse. Its generated pronunciations are not independent gold evidence. | **Benchmark-only first.** Do not vendor code or data in this step. |
| [TLTK](https://github.com/attapol/tltk) | Thai Language Toolkit; README describes segmentation, G2P and IPA transcription. Repository describes New BSD / BSD-3-Clause licensing for current versions. | Academic/research comparator for segmentation and rule-based transcription; useful for tracing established approaches. | Pin a specific commit/version; verify license and provenance of each dataset/model. Differences in transcription convention and lexical coverage must be normalized explicitly. | **Benchmark-only.** |
| [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp) | Thai NLP toolkit; newmm is a dictionary-driven segmentation baseline used by multiple systems. | Segmentation baseline, not a pronunciation oracle. Compare boundary precision/recall on the same independently adjudicated sample. | Dictionary choice and tokenizer version affect output. Do not conflate tokenizer agreement with phonological correctness. Check package/data licenses before distributing assets. | **Segmentation-only baseline.** |

## Comparison protocol

1. Pin exact release/commit, runtime, dependencies and license metadata for every external run.
2. Keep normalization, word segmentation, syllable segmentation, IPA generation and Ukrainian adaptation as separate measured stages.
3. Use identical inputs and preserve source text, system output, version, options, errors and provenance in JSONL.
4. Score segmentation only against source annotations with their evidence grade stated. Source-annotated rows are **not** expert-adjudicated gold unless independently reviewed.
5. Score IPA only against independently verified pronunciations using an explicitly documented normalization policy; report coverage and abstentions alongside error rates.
6. Never treat ClippyFirst's own lexicon/overrides as independent references for a comparator if those same entries informed the engine (circularity).
7. Do not import a model or dictionary into the default runtime until accuracy, license, reproducibility, size/performance, provenance and IPA-convention compatibility have all been reviewed.
8. Ukrainian adaptation remains downstream of ClippyFirst's typed IPA result. External romanization is not a substitute for IPA and must not become a parallel Thai-grapheme → Ukrainian path.

## Next acceptance gate

Build a small, stratified, manually reviewed evaluation set from source-attested forms and article-style text, with each record carrying source URL/citation, orthographic form, segmentation, phonemic/broad IPA, dialect/scope, evidence grade, adjudication state and uncertainty notes. Compare ClippyFirst strict/soft modes and pinned external baselines on the exact same rows. Until independent adjudication exists, publish diagnostics and error examples, not an accuracy claim.
