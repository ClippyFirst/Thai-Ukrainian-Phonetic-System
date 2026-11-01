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


- **SRC-CCOST-ZENODO-2025 — dataset record:** Pittayaporn, Yang, Jitwiriyanont & Kirby, *Chulalongkorn Corpus of Spoken Thai*, Zenodo v1.0, dataset DOI https://doi.org/10.5281/zenodo.17366698 (published 2025-10-16). The dataset record describes approximately 7 hours of spontaneous and 5 hours of controlled Standard Thai speech from 49 speakers, with WAV audio and TextGrid annotations. The dataset license is **CC BY-NC-SA 4.0** (non-commercial; share-alike applies to adaptations).
- **SRC-CCOST-LREC-2026 — associated paper:** Pittayaporn et al., *The Chulalongkorn Corpus of Spoken Thai (CCOST)*, Proceedings of LREC 2026, pp. 3154–3160, article DOI https://doi.org/10.63317/3ds35jijmgrx; ACL Anthology record https://aclanthology.org/2026.lrec-1.247/. The paper abstract reports ASR/forced-alignment annotation followed by manual correction by phonetically trained native Thai speakers, with orthographic, word-, syllable-, phone-level and toneme annotations.
- **Tier specification verified from the full LREC 2026 paper:** intended TextGrid tiers are ORT (orthographic word), KAN (canonical word pronunciation), KAS (canonical syllabified pronunciation), MAU (phonetic segment), MAS (phonemic syllable), and TRN (orthographic utterance transcript). Phonemic and phonetic labels use X-SAMPA; tone suffixes map `_1=Mid`, `_2=Low`, `_3=Falling`, `_4=High`, `_5=Rising`. The 206-item controlled monosyllable list crosses five tones, four initial-consonant types, three syllable structures and vowel length (contrastive only in closed syllables).
- **Evidence boundary:** trained native Thai research assistants manually corrected alignment boundaries and verified tone/segmental accuracy, with spot checks by senior team members; the paper explicitly reports that formal inter-annotator agreement was not collected. CCOST is a valuable manually corrected external reference, not a two-independent-reviewer gold set. The paper establishes the intended tier map, but actual released TextGrid conformance, the exact X-SAMPA inventory and per-file metadata still require archive inspection. The dataset is CC BY-NC-SA 4.0; keep the 6.2 GB archive external and do not redistribute WAV/TextGrid assets. The dataset and article have different DOI records and distinct license terms; do not conflate them.
- **SRC-CCOST-WORDLIST — separate controlled word-list file:** https://zenodo.org/records/17366698/files/wordlist.csv?download=1. It is a four-column A-D presentation-order file for the paper's 206-item monosyllabic task. It supplies Thai orthographic prompts only, not IPA, phone labels or audio. The local packet generator audits duplicates and order-set differences rather than assuming the four columns are identical. Any generated packet remains unadjudicated until independent Thai reviewers supply broad phonemic labels; the source list alone is not pronunciation gold. Apply CC BY-NC-SA 4.0 non-commercial/share-alike terms.
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


## Special vowel-letter evidence — 2026-10-26

- **SRC-OBEC-SPECIAL-VOWELS-2022** — Office of the Basic Education Commission / IPST teacher guide, *ชุดการจัดกิจกรรมการเรียนรู้ ภาษาไทย ชั้นมัธยมศึกษาปีที่ 1 ภาคเรียนที่ 1*, p. 5: https://academic.obec.go.th/images/document/1649040986_d_1.pdf .
- The guide describes ฤ ฤๅ ฦ ฦๅ as syllabic units broadly comparable to ริ/รึ/รือ/ลึ/ลือ, rather than as freely occurring vowel sounds.
- This supports a conservative orthographic/lexical classification only. It does not establish one IPA value for every word or authorize output for an isolated letter without lexical context. Existing word-level overrides must retain their own lexical evidence, and unsupported forms remain analysis-dependent.
- Separate source **SRC-OBEC-O-NAM-2022** — OBEC's *คู่มือการสอนอ่านเขียน โดยการแจกลูกสะกดคำ*, section 2.9 (printed p. 275): https://academic.obec.go.th/web/images/document/1650944942_d_1.pdf . The guide explicitly lists อ นำ ย examples อย่า, อยู่, อย่าง and อยาก. This supports the scope of the existing lexical family, not a productive rule for arbitrary spellings beginning with อ.


## Verified external phonetic-resource metadata — 2026-10-26

- **CCOST primary dataset record:** Pittayaporn, Yang, Jitwiriyanont & Kirby, *The Chulalongkorn Corpus of Spoken Thai*, Zenodo v1.0, DOI https://doi.org/10.5281/zenodo.17366698. The public record describes approximately 7 hours of spontaneous speech and 5 hours of controlled recordings from 49 speakers, with orthographic, word, syllable and phone/toneme annotations. The record explicitly states **CC BY-NC-SA 4.0** and lists C-COST.zip, CCOST_manual.pdf, speaker/recording metadata, word list and sentence prompts.
- The paper's abstract is independently available at ACL Anthology: https://aclanthology.org/2026.lrec-1.247/. It describes manual correction by phonetically trained native Thai speakers. This establishes that CCOST is a plausible candidate source for independent phonetic review, not that this project has downloaded, inspected, or adjudicated its audio.
- **Acceptance boundary:** before using CCOST, preserve the license and attribution/share-alike terms; verify the manual's exact annotation conventions, permitted processing and publication/redistribution limits; record the exact Zenodo version and archive hash; keep audio/TextGrid files external unless project policy explicitly permits inclusion; select speaker-disjoint items where multiple recordings from a speaker could leak across partitions. Non-commercial terms preclude assuming unrestricted commercial reuse.
- **Official Royal Institute dictionary:** https://dictionary.orst.go.th/ is the Royal Institute dictionary site and can be used to cross-check lexical readings. Dictionary entries are lexical attestation, not acoustic evidence or independent adjudication. The current บรรจุ review case still requires a declared transcription level and contextual decision; one source's /ʔ/ must not be generalized into a universal surface rule.
- **OBEC PDF access check:** the cited official URL https://academic.obec.go.th/images/document/1649040986_d_1.pdf returned HTTP 403 during this continuation (also observed by browser fetch). This remains BLOCKED for full-document inspection. Do not claim all pages were read; keep claims restricted to already accessible, page-scoped evidence and retry only through a lawful, authoritative access route.


## Pinned independent-domain segmentation source — VISTEC-TP-TH-2021

- Upstream repository and dataset README: https://github.com/mrpeerat/OSKut/tree/215a7dc3d384f20eb56af1cbc41fb32b7f8df57c/VISTEC-TP-TH-2021/ . Pinned commit: 215a7dc3d384f20eb56af1cbc41fb32b7f8df57c; CSV Git blob SHA-1: edfcb85907a604c5e30643065ac4975862a0fe90.
- The dataset-specific upstream README states 49,997 samples and manual linguistic annotation for word segmentation, misspelling and named entities; it declares CC-BY-SA 3.0 and supplies a full license text at VISTEC-TP-TH-2021/LICENSE.md. The source is not copied into this repository.
- The annotation field is submissionText, which contains pipe-delimited token boundaries and <ne>/<msp> annotation markup. The new adapter strips those annotation tags, retains the annotated text content, verifies exact reconstruction, and explicitly does not substitute questionText. The convention must remain visible because source correction markup can mean this is not byte-for-byte raw user text.
- This is a separate social-media domain from Wisesight, useful for external source-annotation evaluation. It is **not** independent re-adjudication and should not be called expert gold. The exact-pinned workflow is new and its metric artifact remains pending until that workflow passes.


## CCOST annotation manual review — 2026-11-01

- Primary file: [`CCOST_manual.pdf`](https://zenodo.org/api/records/17366698/files/CCOST_manual.pdf/content), listed by the [Zenodo dataset record](https://zenodo.org/records/17366698); PDF has 19 pages and MD5 `caecb20d26e8458b20c7c269ca22b59e`.
- The document identifies itself as “RA Manual for BKK Thai Tone Project”. It describes recruiting/recording assistants, interview/word-list/sentence tasks, transcription correction in OCTRA, Praat fine-tuning, and the BAS MAUS pipeline. The workflow includes Thai-script normalization, correcting omissions/repetitions, marking non-speech speaker noise as `<usb>`, and correcting time-aligned boundaries.
- The manual's stated aim is time-aligned annotation of words, syllables, consonants and vowels. It names `OCTRA_1` as the input tier and MAUS output symbols as `sampa` in the illustrated pipeline configuration. These operational settings do **not** establish the final released TextGrid's tier schema or a complete phone/toneme label inventory.
- The LREC 2026 paper, rather than this manual, specifies the intended tier map (ORT/KAN/KAS/MAU/MAS/TRN), X-SAMPA representation and tone-number convention. The manual itself documents the correction workflow but not a complete symbol inventory or formal disagreement protocol.
- The paper states that trained native Thai research assistants corrected alignment boundaries and verified tone/segmental accuracy; senior team members spot-checked corrections. It explicitly reports that no formal inter-annotator agreement measures were collected.
- **Status:** manual inspection and paper-tier-map extraction `DONE_VERIFIED`; actual archive tier/label conformance and X-SAMPA-to-IPA mapping remain `BLOCKED / evidence-limited`. CCOST remains an external manually corrected reference, not independent double-reviewed gold. No audio or TextGrid corpus assets were downloaded or bundled.

## LOTUSDIS alternative audio source — 2026-11-01

- Registered `CORP-LOTUSDIS` as a verified **audio/transcript source for fresh human re-annotation**, not as IPA or toneme gold. Official dataset card: [Hugging Face LOTUSDIS](https://huggingface.co/datasets/nectec/LOTUSDIS); pinned project README: [CAI-NECTEC/LOTUSDIS at b6c7e814](https://github.com/CAI-NECTEC/LOTUSDIS/tree/b6c7e81498a92003761ac856348d764c287ee02c); accompanying paper: [arXiv:2509.18722](https://arxiv.org/abs/2509.18722).
- The release describes approximately 114 hours, 86 participants, utterance transcripts and TextGrid, with CC BY-SA 4.0 licensing; the dataset card lists 160,915 rows and approximately 13.2 GB. Its released labels are transcript/alignment material, not phonemic IPA or tone gold. The paper describes three trained transcript annotators and senior review; this does not substitute for independent phonetic annotation.
- Use only as a supplementary source for new acoustic/phonetic expert annotation. Prefer near-field, single-speaker, non-overlapped clips. Record exact dataset revision, asset ID, speaker pseudonym, microphone/channel, interval and file hash before freezing any sample. Do not bundle audio. Preserve CC BY-SA attribution/share-alike for derived annotation data.
- Standard Thai representativeness is not established by the source record alone. A Thai reviewer must confirm dialect/speaker suitability for each selected sample.
- **Decision:** source-level permission is verified and registered; no LOTUSDIS assets have yet been selected, downloaded, or promoted to gold. The 42+6 project-authored blind packet remains the controlled baseline; CCOST remains the preferred controlled tonal stimulus source only if its non-commercial license is acceptable and its A-D discrepancy and TextGrid mapping are resolved.
- Common Voice Thai v27.0 was not selected for a shared reviewer packet: its CC0 data card separately forbids re-hosting/re-sharing the dataset, and it supplies no phone/toneme IPA gold. It may be considered only where reviewers access the original source directly under its terms.


## File-level audio provenance gate — 2026-11-01

- Added header-only `data/benchmark/audio-assets.tsv`. The manifest schema binds each asset to a registered source, exact dataset revision, asset URI, SHA-256, pseudonymous speaker reference, microphone/channel, overlap status, duration and verification record.
- Thai review validation now requires audio-backed rows to reference a VERIFIED asset in that manifest; source ID must match, overlap must be NONE, and the review interval must fit inside the registered duration. This applies to broad phonemic reviews that cite audio as well as NARROW_ACOUSTIC reviews.
- The manifest is intentionally empty: LOTUSDIS assets have not yet been selected/downloaded/pinned, and CCOST remains blocked. No narrow acoustic annotation can be accepted until a specific asset is registered.


- Registry integrity check also found and fixed an existing malformed `data/corpus_sources.csv` row: the TUD record's comma-containing metadata had not been quoted. A regression test now checks the exact seven-column schema and unique source IDs.
