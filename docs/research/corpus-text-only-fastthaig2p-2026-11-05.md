# Text-only Thai corpus and FastThaiG2P rights review — 2026-11-05

## Scope and decision

This review is deliberately **text-only**. The project does not need to download, store, process, or redistribute WAV/FLAC audio for the planned lexical/phonetic text evaluation. The useful assets are orthographic transcripts, word/phone/toneme labels, and text annotations such as Praat TextGrid tiers. No audio archive was downloaded or inspected in this review.

**Owner decision update (2026-11-05): Global TIMIT Thai is excluded from this project.** Do not pursue LDC access, fees, agreements, audio, or derived labels. Its role is not a dependency; alternatives are CCOST phonetic text and selectively reusable FastThaiG2P/Wiktionary candidates. This is a scope decision, not a quality judgment.

The remaining corpora serve different purposes:

- **Global TIMIT Thai** is **EXCLUDED by owner decision**. Its earlier licensing analysis is retained below as historical rationale only; no access or acquisition work should be scheduled.
- **LOTUSDIS** is an openly licensed conversational transcript resource, but the published corpus description does not identify phone-level or IPA labels. It can help with conversational vocabulary, code-switching and orthographic robustness; it is not a Thai IPA gold source.
- **CCOST** is the strongest match for phonetic text validation: its published TextGrid schema includes phonetic segments and phonemic syllables with tone labels. The non-commercial project purpose appears compatible with its CC BY-NC-SA 4.0 terms, provided attribution and ShareAlike are followed. Obtain a TextGrid-only export or selectively extract text annotations; do not fetch audio just because it is packaged beside them.

## 1. Global TIMIT Thai (LDC2022S13)

### What we can use without audio

The official LDC catalog confirms 50 Standard Thai speakers, 6,000 utterances, 2,124 sentence types, and separate sample types for **Word (TXT), Phones (TXT), Tones (TXT), and TextGrid (TXT)**. Each speech file has accompanying phone and word segmentation and Praat TextGrid material. The phones and tones files are directly relevant to a text-only phonetic reference set; WAV/FLAC is not needed for the intended use. See the [LDC catalog entry](https://catalog.ldc.upenn.edu/LDC2022S13).

### Access and redistribution

The catalog specifies the **LDC User Agreement for Non-Members**. The standard agreement permits use only for non-commercial linguistic education, research and technology development. It permits limited excerpts in articles/reports describing that research, but otherwise prohibits publishing, retransmitting, copying or redistributing the LDC databases outside the user's research group. The signed agreement names the individual and research group and must be sent to LDC. See the [LDC Non-Member User Agreement](https://catalog.ldc.upenn.edu/license/ldc-non-members-agreement.pdf).

Consequences for this project:

- Our stated non-commercial/public-interest research purpose is within the purpose category allowed by the standard agreement, subject to signing it and meeting its conditions.
- We can seek access specifically to the text/phones/tones/TextGrid files and avoid using audio in our workflow.
- We must not put the full extracted phone/word/toneme files, a reconstructed lexicon, or a bulk-derived corpus into this public repository under the standard agreement.
- Limited examples in research reports are allowed by the agreement; for a public machine-readable evaluation subset or wider release, obtain separate written permission from LDC.
- The current catalog page requires login to view the applicable fee; no fee amount is asserted here.

**Current status: DEFERRED / EXCLUDED by owner decision.** No further LDC contact, access, fees, agreement, data acquisition, or derived-label work is planned.

## 2. LOTUSDIS

### What the public text data contains

The official [Hugging Face dataset page](https://huggingface.co/datasets/nectec/LOTUSDIS) exposes text rows with a Thai sentence, speaker_id, mic, and duration; it reports 160,915 rows across splits and declares **CC BY-SA 4.0**. The paper describes approximately 20 hours of unique conversational sessions represented by 114 hours across microphones, 86 participants, and utterance-level transcripts with speaker labels and overlap masks. The annotation protocol used three trained annotators followed by senior review; it includes tags for noise, silence, unintelligible spans and dialectal uncertainty. See the [LOTUSDIS paper](https://arxiv.org/abs/2509.18722).

### What it does not establish

The paper describes utterance-level orthographic transcripts, not phoneme/phone IPA labels. Neither the public dataset viewer schema nor the paper establishes a phonetic tier equivalent to CCOST's MAU or MAS. A Praat TextGrid download link is not, by itself, evidence of phone-level phonetic transcription. The actual TextGrid tier schema has not been inspected here.

### Usefulness for our project

- Useful optional source for conversational Thai vocabulary, disfluencies, code-switching, colloquial forms and orthographic input robustness.
- Potentially useful for word-segmentation research only after confirming how the transcripts encode Thai word boundaries; ordinary Thai spaces are often phrase boundaries, not reliable word boundaries.
- Not a phonetic IPA gold source and not a substitute for CCOST or independently reviewed phone labels.
- Because the project does not need audio, do not fetch WAV assets or perform per-audio SHA-256/overlap checks. Those earlier audio-centric tasks are **DEFERRED / OUT OF SCOPE** for this text-only objective.

### License

The dataset page and paper state **CC BY-SA 4.0**, which permits commercial and non-commercial reuse subject to attribution and ShareAlike. For our non-commercial research, text-only extraction and redistribution of adapted annotations appear compatible if the repository includes proper attribution, source/version references and a CC BY-SA 4.0 notice for the derived data. Keep that dataset license separate from the repository's software license.

**Recommended status: PARTIAL — TEXT TRANSCRIPTS AVAILABLE, NO PUBLISHED PHONE-LEVEL GOLD.** Keep as optional contextual/orthographic data, not as a primary phonetics dependency.

## 3. CCOST

### Why this is the best fit

The LREC 2026 paper describes approximately 12 hours of annotated Standard Thai, 49 speakers, 130,436 word tokens and 5,158 word types. It includes spontaneous interview speech and controlled word/sentence reading tasks. Its published TextGrid tiers are:

| Tier | Published meaning | Value to this project |
|---|---|---|
| ORT | Orthographic word | Aligns source spelling with pronunciation |
| KAN | Canonical word pronunciation | Canonical pronunciation candidate |
| KAS | Canonical syllabified pronunciation | Syllable-level candidate |
| MAU | Phonetic segment | Actual phone-level realization; captures variants |
| MAS | Phonemic syllable | Phonemic/syllabic representation |
| TRN | Orthographic utterance transcript | Context and transcript |

The paper states that phonemic and phonetic representations use **X-SAMPA**, with tone suffixes _1 = Mid, _2 = Low, _3 = Falling, _4 = High and _5 = Rising. Trained native Thai research assistants manually corrected alignment, tone and segmental accuracy; phonetic variants are recorded at MAU. See [Pittayaporn et al., LREC 2026, §§3.3–3.4](https://aclanthology.org/2026.lrec-1.247.pdf) and the [official Zenodo record](https://zenodo.org/records/17366698).

For our pipeline, MAU and MAS are the most valuable tiers. They offer a route to compare phonetic realizations and phonemic syllables without needing to keep the audio. X-SAMPA must be converted by a documented, tested mapping into our typed IPA representation; do not relabel X-SAMPA strings as IPA without conversion.

### License and non-commercial use

The official record and paper specify **CC BY-NC-SA 4.0**. This permits sharing and adaptation for non-commercial purposes with attribution and ShareAlike. Given the project's stated non-commercial, public-interest research purpose, text-only use appears to fit the license's intended non-commercial scope, provided that:
- the corpus authors/source are credited and the license/version is retained;
- extracted or adapted TextGrid annotation data are released under CC BY-NC-SA 4.0 (or a license explicitly compatible with it);
- the project does not use the corpus for commercial advantage or monetized product distribution;
- the software license (MIT) remains distinct from the dataset license.

This is a practical project assessment, not a legal opinion on every future funding or deployment scenario. If the project later becomes commercial, reassess before that use.

### Quality limitation

The paper reports trained native-speaker correction and senior spot checks, but explicitly states that **no formal inter-annotator agreement measures were collected**. CCOST is therefore a valuable source-annotated phonetic reference, not a formally measured-IAA or independently adjudicated gold set. We should independently review a stratified subset before using it to make accuracy claims.

### Text-only acquisition path

The Zenodo record lists a 6.2 GB C-COST.zip containing WAV and TextGrid files plus a separate CCOST_manual.pdf; no separate TextGrid-only archive was verified. Do not download the combined archive merely to obtain files we do not need. Preferred next step: ask the authors/curators for a TextGrid-only export and manual. If they confirm that no separate export exists, decide whether a selective TextGrid-only extraction from the licensed archive can be performed without retaining or publishing any audio. Actual tier instances, intervals, and manual instructions remain uninspected.

**Recommended status: PARTIAL — PUBLISHED PHONE/TONE TIER MAP VERIFIED; TEXTGRID-ONLY EXPORT AND FILE-LEVEL CHECK PENDING.** CCOST should be our first corpus to pursue for phonetic text validation.

## 4. FastThaiG2P: what can be reused

Upstream reviewed: [repository](https://github.com/awslabs/FastThaiG2P), [data README](https://github.com/awslabs/FastThaiG2P/blob/main/data/README.md), [LICENSE](https://github.com/awslabs/FastThaiG2P/blob/main/LICENSE), [NOTICE](https://github.com/awslabs/FastThaiG2P/blob/main/NOTICE).

### Reuse map

| Component | Published/source license or provenance | Recommendation |
|---|---|---|
| FastThaiG2P Python code | Apache-2.0; Amazon NOTICE present | **Reusable** with Apache license/NOTICE and modification notices retained |
| PyThaiNLP tokenizer dependency | Apache-2.0 software; data/model assets have their own licenses | **Reusable as a dependency**; review each separately bundled corpus/model |
| data/sources/wiktionary_ipa.json (~13k entries) | Derived from Wiktionary/Kaikki; the PyThaiNLP Thai G2P Wiktionary corpus declares CC BY-SA 3.0 | **Potentially reusable** with attribution and ShareAlike; keep this subset separate and mark it source-attested, not expert gold |
| data/dict.txt and merged data/ipa.json | Dictionary keys plus a merge of Wiktionary, manual overrides and generated entries | **Do not copy wholesale** until per-entry source filtering and rights are established |
| ~49k generated IPA entries | Claude Opus 4.6 generated; source README says generated file is gitignored, while the merged runtime dictionary includes the output | **Candidate baseline only**, not gold; preserve source metadata and do not claim expert verification |
| manual_overrides.json | Described as user corrections; individual reviewer credentials/source evidence are not documented in the file description | **Use only as provisional candidate data** until provenance and review are supplied |
| Vendored TLTK fallback code | _th2ipa.py contains a BSD-3-Clause notice | **Code is reusable** with the notice retained |
| Vendored TLTK fallback data | sylseg.3g, thaisyl.dict, PhSTrigram.sts, thdict, sylform_var.pkl etc. are identified as TLTK assets; the TLTK repository exposes conflicting top-level license indicators (LGPL-3.0 LICENSE, BSD-3-Clause LICENSE.txt, older package metadata saying GPLv3, setup metadata saying BSD-3-Clause) | **Do not redistribute these assets until upstream clarifies which license covers each data file** |

The Wiktionary corpus source explicitly states CC BY-SA 3.0: [PyThaiNLP Thai G2P Wiktionary corpus](https://github.com/PyThaiNLP/thai-g2p-wiktionary-corpus). TLTK license references: [upstream LICENSE](https://github.com/attapol/tltk/blob/master/LICENSE), [LICENSE.txt](https://github.com/attapol/tltk/blob/master/LICENSE.txt), [setup.py](https://github.com/attapol/tltk/blob/master/setup.py), [PyPI metadata](https://pypi.org/project/tltk/).

### Quality and test-evidence limits

The FastThaiG2P paper reports a 500-word prompt validation against Wiktionary with 78.8% exact match and 1.8% fatal error rate under its own error classification. Tone, vowel length, diphthong and coda differences are classified as non-fatal; some irregular loanword classes are excluded from the fatal count. This is a prompt-validation exercise against Wiktionary, not an independent evaluation of the full 62k dictionary or of the Ukrainian transcription system. See [the upstream paper](https://arxiv.org/abs/2608.12814).

The current upstream data README mentions tests/ground_truth_ipa.json (34 rows) and tests/blind_test_ipa.json (17 rows), but both paths return 404 on the current main branch. The accessible test_g2p.py checks a few fixed outputs and includes permissive OOV assertions; these are software smoke tests, not a statistically meaningful phonetic gold set.

### Practical reuse decision

1. Reuse/adapt the Apache-2.0 code paths we actually need (normalization, tokenizer integration, IPA adapter logic), retaining NOTICE and source headers.
2. If a dictionary is useful, start from the isolated Wiktionary-derived subset under CC BY-SA 3.0, with its own data license notice and provenance. Do not copy the merged 62k runtime dictionary blindly.
3. Keep LLM-generated IPA as provisional external candidates only. It may help identify words and hypotheses, but must not become source gold or independent accuracy evidence.
4. Do not bundle TLTK fallback data until the exact file-level license is clarified. A no-fallback mode or our existing conservative Thai phonology path is preferable to importing unclear data.
5. Keep the existing Python-host preview gate separate: rights clearance does not prove deployment works, and a working preview does not clear data rights.

**Recommended overall FastThaiG2P rights status: PARTIAL — CODE AND A SEPARATE WIKTIONARY SUBSET HAVE A REUSE PATH; GENERATED AND TLTK BUNDLES NEED SOURCE-SPECIFIC TREATMENT.**

## 5. Recommended project priority

1. **First: CCOST TextGrid-only export** — request text-only files and manual, inspect actual tier instances, convert X-SAMPA to typed IPA, and independently review a stratified subset.
2. **Second: FastThaiG2P selective reuse** — Apache-2.0 code + separately licensed Wiktionary subset first; generated dictionary only as provisional candidates; TLTK data only after file-level license clarification.
3. **Optional: LOTUSDIS text** — use for conversational vocabulary and orthographic robustness, not phonetic gold. No audio acquisition or hash work is required.
4. **Global TIMIT Thai: excluded** — do not spend further effort on it.

No corpus-derived rows, phonetic labels, IPA conversions, accuracy figures, or license permissions were added to runtime data in this review. No audio was downloaded.

## Owner scope decision — 2026-11-05

Global TIMIT is excluded. Its earlier access/licensing discussion above is historical only and must not be treated as an active task. The active order is CCOST → selective FastThaiG2P/Wiktionary reuse → optional LOTUSDIS text. All corpus work remains text-only; audio is out of scope.
