# Evidence registry

## Core sources

- SRC-ORST — Royal Institute of Thailand official linguistic standards and publications.
- SRC-JIPA-1993 — Tingsabadh & Abramson, Thai, Journal of the International Phonetic Association, 1993, DOI 10.1017/S0025100300004746.
- SRC-CORPUS — Munthuli et al., corpus-based study of Thai phoneme distribution.
- SRC-NRCT — Thai phonology and orthography research thesis.
- SRC-CCOST — Pittayaporn et al., Chulalongkorn Corpus of Spoken Thai, LREC 2026.
- SRC-G2P-WIKI — PyThaiNLP Thai Grapheme to Phoneme Wiktionary Corpus.

## Orthographic ambiguity evidence

- **SRC-ORST-VOWEL-LENGTH-2021** — International Journal of the Royal Society of Thailand (2021), *The Thai Writing System: Reasons behind Its System*, Table 14. The source explicitly documents shared written forms with final consonants and contrasts **เกิน** /ɤː/ with **เงิน** /ɤ/, demonstrating that the closed **เ-ิ-** spelling cannot by itself determine vowel length. This is treated as an orthographic/lexical ambiguity, not as a parser failure.

## Coda-position evidence

Standard Thai permits a restricted final inventory; consonant graphemes such as ฉ, ผ, ฝ, ห, อ and ฮ are not licensed as ordinary codas. The parser therefore treats an otherwise structurally detectable final occurrence of one of these graphemes as `invalid:coda-not-licensed` rather than silently dropping it. This is an orthographic/phonotactic validation rule, not a claim about lexical attestation. The JIPA Standard Thai description and independent descriptions of Thai final consonants support the restricted-coda analysis.

## Evidence policy

A source can support a claim, but implementation status is tracked separately. The project distinguishes core evidence, analysis-dependent rules, and unresolved cases.

For publication, each important rule should eventually have a claim-level record containing source, page or section, exact claim, competing analysis, implementation consequence and confidence.

The official Royal Institute material is particularly important for Thai orthographic phenomena such as leading consonants and consonant clusters. CCOST is reserved for empirical phonetic validation rather than for defining orthographic rules.


## Claim-level anchors used in the current audit

- **SRC-JIPA-1993:** Tingsabadh & Abramson, *Thai*, Journal of the International Phonetic Association 23(1), pp. 24–28. The description establishes the Standard Thai reference scope, nine vowel qualities with contrastive length, /w/ and /j/ as final components in phonetic diphthongs, five tones, and the restricted final-consonant inventory. DOI: https://doi.org/10.1017/S0025100300004746
- **SRC-ORST-TH:** Royal Institute of Thailand publications are used for orthographic phenomena such as leading consonants and the interaction of written structure with pronunciation. These are orthographic evidence, not a substitute for corpus-based phonetic validation.

The implementation deliberately uses a broader machine-readable rime registry than the nine-vowel-quality phonological inventory because several orthographic rimes and glide sequences are represented as separate structural parsing records. **Registry cardinality is not phoneme-inventory cardinality.**


## False-cluster evidence

Standard Thai cluster descriptions distinguish true clusters from false clusters. In particular, **จร, สร, ศร, ซร** can contain a written ร that is not pronounced, while **ทร** has lexical readings that may diverge from a compositional /thr/ analysis. Examples documented in reference descriptions include **จริง** /tɕiŋ/, **สร้าง** /saːŋ/, **เศร้า** /saw/ and **ไซร้** /saj/. The implementation therefore treats these constructions as analysis-dependent until lexical evidence resolves the reading. Sources: SRC-ORST; the independent cluster reference used in the audit.


## Source-attested lexical false-cluster reading

- **SRC-RID-2011-SRI** — Royal Institute Dictionary (2011 edition), entry for **ศรี**, exposed through the Longdo dictionary interface: https://dict.longdo.com/search/ศรี . The entry explicitly supplies the reading `[สี]`. This supports a lexical orthographic override `ศรี → สี`; it is not an independently adjudicated IPA record and must not be counted as phonetic gold.
- The Python and browser lexical-reading registries now include this exact override. Regression tests verify normalized spelling and the engine's derived IPA/Ukrainian output, while the evidence note keeps the source's actual claim limited to the lexical reading.


## Sense-ambiguous ทราย reading — 2026-10-25

- **SRC-ORST-CLUSTER-2011-THRAY-SENSE** — Royal Institute of Thailand Journal, “เรื่องยุ่ง ๆ เกี่ยวกับอักษรควบ”, vol. 36 no. 4 (Oct–Dec 2011), p. 556, official source: https://www.orst.go.th/FILEROOM/CABROYINWEB/DRAWER004/GENERAL/DATA0000/00000630.FLP/html/48/ .
- The article explicitly distinguishes two senses of **ทราย**: the sand sense is analyzed as a false cluster with initial /s/, while the deer-name sense is analyzed as a true ทร cluster. This is evidence of sense-dependent orthographic reading, not a blanket rule for every token spelled ทราย.
- The parser has no semantic sense input, so the bare homograph is now left at `analysis-dependent:special-orthography` with IPA and Ukrainian output withheld. Do not infer the intended sense from frequency or from the existing text-segmentation lexicon.
- This source supports the ambiguity decision only. It does not provide independent acoustic IPA gold or authorize an accuracy score.


## Corpus and benchmark source register — 2026-10-25

## Additional pinned evidence — 2026-10-25

- **SRC-WISESIGHT1000-CC0** — PyThaiNLP, `word-tokenization/wisesight-1000-samples-tokenised.label`, immutable source commit `c1d063649abc3a6870b5fd1aae26cd1c64bdde7b`, blob SHA-1 `279aeb2d4323fd8032306160144d33dcb5b2df84`, CC0-1.0. The pinned file contains 993 manually tokenized records. The repository retains these labels as `SOURCE_ANNOTATED`, not expert-adjudicated gold. See `data/benchmark/wisesight1000-source.json` for conversion and split contract. This source is for word-boundary evaluation only, not IPA/tone gold.
- **SRC-WIKTIONARY-TH-LEXICON-2026-10-25** — six source-attested IPA records are maintained separately in `data/benchmark/source-attested-ipa.tsv`; the runtime lexicon subset added from exact Thai Wiktionary revisions is enumerated in `data/thai/text_lexicon_sources.csv`. Per-page revision locators and CC BY-SA 4.0 terms are explicit. These are source-attested readings, not independent expert/acoustic gold.
- The short-vowel reading of `เงิน` (/ŋɤn˧/) is source-attested, but it remains intentionally excluded from the runtime text lexicon until a typed lexical-pronunciation override preserves that lexical length through the IPA-first adapter. Do not substitute a parser default for this lexical fact.


- **SRC-CCOST-ZENODO-2025** — Pittayaporn, Yang, Jitwiriyanont & Kirby, *Chulalongkorn Corpus of Spoken Thai*, Zenodo v1.0, DOI https://doi.org/10.5281/zenodo.17366698 (published 2025-10-16). The record describes approximately 7 hours of spontaneous and 5 hours of controlled Standard Thai speech from 49 speakers, with audio and TextGrid annotations; the dataset license is CC BY-NC-SA 4.0. Use as a candidate for independent acoustic/phonetic adjudication only after reviewing the annotation manual and terms. Do not redistribute the corpus in this repository.
- **SRC-G2P-WIKI-2022** — PyThaiNLP, Thai Grapheme to Phoneme Wiktionary Corpus, https://github.com/PyThaiNLP/thai-g2p-wiktionary-corpus. Upstream states that its IPA corpus was scraped from Wiktionary via WikiPron and is licensed CC BY-SA 3.0; 2020 and 2022 TSV snapshots are available. Treat as source-attested regression data, not independent gold against systems that may share Wiktionary-derived entries.
- **SRC-THAI-SEGMENTATION-INDEX** — NLP for Thai, Word Segmentation corpus index, https://nlpforthai.com/tasks/word-segmentation/. It lists candidate word-boundary resources and reported licenses including Wisesight samples (CC0-1.0), Blackboard Treebank (CC BY 3.0), VISTEC-TP-TH-21 (CC BY-SA 3.0) and BEST I (CC BY-SA-NC 4.0; access may require registration). The index is discovery metadata; verify the exact upstream release, terms, split and annotation guideline before evaluation.
- **SRC-THAI-SEGMENTATION-BENCHMARK-INDEX** — OpenCodePapers, Thai word tokenization on BEST-2010 benchmark index, https://opencodepapers-b7572d.gitlab.io/benchmarks/thai-word-tokenization-on-best-2010.html. Its listed F1 results are external, split-specific research reports, not reproduced ClippyFirst scores. Do not use them as a direct baseline until dataset version, split, metric and tokenization convention match.

These sources identify candidate resources and external claims; they do not add adjudicated records to `data/benchmark/gold.tsv` and do not change the current independent-gold count of zero.


## Text-attested IPA diagnostic findings — 2026-10-25

The six entries in `data/benchmark/source-attested-ipa.tsv` remain `SOURCE_ATTESTED_NOT_GOLD`. The diagnostic run compares segmental IPA separately from tone categories and records vowel-length metadata. On the verified Python checkpoint, five records produced complete outputs; four matched source segmental IPA and five matched tone categories. One form was withheld because the engine still cannot resolve its vowel-length ambiguity. One discrepancy remains for `บรรจุ`: the dictionary transcription includes final `/ʔ/`, while the engine's segmental output omits it.

This is not automatically classified as an engine error or patched into runtime output. Published descriptions of Thai report that final glottal realization can vary with stress and may be absent in unstressed syllables; compare transcription conventions and context before forcing a universal rule. See [Tingsabadh & Abramson, *Thai* (JIPA)](https://doi.org/10.1017/S0025100300004746) and the [Thai phonology reference](https://www.thai-language.com/resources/slayden-thai-phonology.pdf). These references justify review of the mismatch, not an acoustic claim about this particular token.

## CCOST license and text-only availability

The CCOST source record is pinned to [Zenodo DOI 10.5281/zenodo.17366698](https://doi.org/10.5281/zenodo.17366698). The source states CC BY-NC-SA 4.0; the TextGrid annotations are inside the 6.2 GB `C-COST.zip` archive alongside WAV files. TextGrid labels are textual and can be inspected without playback for a first-pass comparison, but no TextGrid files are currently present in this repository. Separate wordlist/sentence files do not substitute for the phone/toneme annotations. No CCOST-derived records or metrics are claimed.

## Segmentation training provenance

- **CORP-TUD-TH** — Universal Dependencies Thai TUD, upstream commit `67413969add552b7030184f16f24fa9f630913bc`, license CC BY-SA 4.0. The treebank README describes 3,627 retained trees sourced from Thai National Corpus and Wikipedia; initial tokenization used PyThaiNLP `newmm` and was subsequently reviewed by trained annotators. The research trainer pins each source file by Git blob SHA and derives source-document-disjoint train/dev/test partitions to reduce leakage. This is segmentation evidence, not pronunciation gold. Preserve attribution and share-alike obligations for derived model artifacts. Sources: [upstream README](https://github.com/UniversalDependencies/UD_Thai-TUD/blob/67413969add552b7030184f16f24fa9f630913bc/README.md), [license](https://github.com/UniversalDependencies/UD_Thai-TUD/blob/67413969add552b7030184f16f24fa9f630913bc/LICENSE.txt), [TACL paper](https://doi.org/10.1162/tacl_a_00745).
