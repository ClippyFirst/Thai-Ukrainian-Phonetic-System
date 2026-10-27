# External Thai G2P and segmentation systems — comparison register

**Purpose:** identify reproducible comparators and design patterns for ClippyFirst's Thai → typed IPA → Ukrainian pipeline. This register does not authorize importing outputs as truth, copying code/data, or changing the project's IPA-first adapter boundary.

## Candidate systems inspected

| Resource | Verified public repository facts | Useful comparison | Restrictions / caveats | Decision |
|---|---|---|---|---|
| [FastThaiG2P](https://github.com/awslabs/FastThaiG2P) | Public Python project; repository metadata declares Apache-2.0. README describes text normalization, PyThaiNLP newmm tokenization, a 62k IPA dictionary, and a TLTK-derived syllable-parser fallback. | Strong candidate for an optional external baseline on shared Thai inputs; compare normalization, OOV coverage, segmentation and IPA, separately. | A repository-level license does not automatically settle every bundled corpus, generated dictionary entry, or vendored component's provenance. Inspect per-file notices and upstream terms before reuse. Its generated pronunciations are not independent gold evidence. | **Benchmark-only first.** Do not vendor code or data in this step. |
| [TLTK](https://github.com/attapol/tltk) | Repository `master` README.rst identifies TLTK 1.9.1 and describes word/syllable segmentation, G2P, IPA transcription and romanization. `setup.py` and README state BSD-3-Clause / New BSD, but the same branch's root `LICENSE` contains GNU LGPL v3 text while `LICENSE.txt` contains a BSD-style 3-clause license. This is an unresolved repository-level licensing conflict, not a clean license determination. | Strong research comparator for segmentation and rule-based transcription; useful for tracing established approaches. | Do not copy, vendor, or make distribution decisions until the maintainers clarify which license applies to which files/version. Pin a commit and audit source/data files individually. Normalize transcription conventions and lexical coverage before comparing. | **Benchmark/research only; reuse BLOCKED by conflicting license artifacts.** |
| [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp) | Thai NLP toolkit; newmm is a dictionary-driven segmentation baseline used by multiple systems. | Segmentation baseline, not a pronunciation oracle. Compare boundary precision/recall on the same independently adjudicated sample. | Dictionary choice and tokenizer version affect output. Do not conflate tokenizer agreement with phonological correctness. Check package/data licenses before distributing assets. | **Segmentation-only baseline.** |



### License/provenance audit correction (2026-10-27)

A direct inspection of [`attapol/tltk` `README.rst`](https://github.com/attapol/tltk/blob/master/README.rst), [`setup.py`](https://github.com/attapol/tltk/blob/master/setup.py), [`LICENSE`](https://github.com/attapol/tltk/blob/master/LICENSE), and [`LICENSE.txt`](https://github.com/attapol/tltk/blob/master/LICENSE.txt) found conflicting license signals: the README and package metadata state New BSD / BSD-3-Clause, the root `LICENSE` contains GNU LGPL v3 text, and `LICENSE.txt` contains a BSD-style 3-clause notice. Do not resolve this by choosing whichever file is convenient; TLTK reuse is blocked until file/version scope is clarified by maintainers or authoritative release packaging. The external comparison remains a research lead, not permission to copy code.

FastThaiG2P's root `LICENSE` declares Apache-2.0 and its `pyproject.toml` declares `pythainlp>=5.3.4` as a runtime dependency; however, the README describes bundled/generated IPA dictionary and a TLTK-derived fallback. The license/provenance of each distributed dictionary entry and the fallback-derived files has not been independently cleared here. Keep it benchmark-only and do not vendor its data. PyThaiNLP's README states Apache-2.0 for code and CC0-1.0 / CC-BY-4.0 for data/models; individual model cards and resource-specific terms still govern each selected asset.

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
