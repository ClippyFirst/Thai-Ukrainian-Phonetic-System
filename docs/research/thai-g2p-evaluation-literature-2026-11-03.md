# Thai G2P evaluation literature: what published scores do and do not establish

**Reviewed:** 2026-11-03  
**Scope:** Standard Thai G2P, phonological/phonetic reference quality, segmentation, and downstream Ukrainian adaptation.  
**Status:** literature synthesis; no new project accuracy result and no runtime behavior change.

## Executive finding

Published Thai G2P scores are useful methodological comparators, but they are not directly comparable to this repository's 42-item challenge and do not establish independent phonetic accuracy for ClippyFirst. The papers use different dictionaries, splits, output representations, and scoring units. At least two prominent studies use reference pronunciations sourced primarily from pronunciation dictionaries/Wiktionary, with limited or unreported independent annotation and agreement procedures.

The repository should therefore continue to report **coverage/abstention**, **word and syllable segmentation**, **segmental IPA**, **tone**, **vowel length**, **phonemic-vs-surface distinctions**, and **Ukrainian target adaptation** as separate outcomes. A single aggregate accuracy number would hide the evidence boundary and error type.

## Primary G2P studies inspected

### Saychum et al. (2016): CRF-based joint sequence modelling

S. Saychum, S. Kongyoung, A. Rugchatjaroen, P. Chootrakool, S. Kasuriya and C. Wutiwiwatchai, “Efficient Thai Grapheme-to-Phoneme Conversion Using CRF-Based Joint Sequence Modeling,” Interspeech 2016, pp. 1462–1466. [DOI: 10.21437/Interspeech.2016-621](https://doi.org/10.21437/Interspeech.2016-621).

Full-text findings:

- The pronunciation dictionary contains **103,265 unique words**, **19,601 unique pseudo-syllable (PS) segments**, including **14,479 unique isolatable syllables**.
- The held-out evaluation set contains **87,329 dictionary words** not used for training. The paper does not explicitly state the training-word count; 15,936 is only the arithmetic remainder if those sets partition the full dictionary.
- The method first segments text into PS units and assigns character functions, then aligns graphemes and phonemes into graphones for a second CRF. PS units are not simply guaranteed to equal spoken syllables: linking syllables may have phonemes not overtly represented in the graphemes.
- The paper reports **13.67% exact-match word error rate (WER)** and **3.91% WER when tone errors are ignored** for its best JSM2 setting. It separately reports phone error rate (PER): **1.54%** for the five-gram JSM2 setting and **6.68%** for the baseline. These are different metrics and must not be conflated.
- Table 4 reports high error rates for the targeted **vowel-length distortion (60.03%)** and **tone ambiguity (43.79%)** problem categories, compared with **linking syllables (1.80%)** for JSM2.
- Reference pronunciations are described as coming from a large pronunciation dictionary. The paper does not report an independent expert-adjudication protocol or inter-annotator agreement.

**Implication:** this is strong evidence that segmentation/character-function analysis and hidden/linking syllables matter, and that tone and vowel length need explicit diagnostics. Its dictionary WER/PER is not an independent expert IPA benchmark and cannot be compared numerically with this project's 42 hand-selected, currently unadjudicated prompts.

### Yamasaki (2022): neural regression over rule-generated candidates

Tomohiro Yamasaki, “Grapheme-to-Phoneme Conversion for Thai using Neural Regression Models,” NAACL 2022, pp. 4251–4255. [DOI: 10.18653/v1/2022.naacl-main.315](https://doi.org/10.18653/v1/2022.naacl-main.315).

Full-text findings:

- The Thai experiment uses **18,066 vocabulary entries, including phrases**, with pronunciations collected primarily from **Wiktionary**. The authors converted Thai-specific pronunciation notation to IPA.
- Some missing entries were completed from unique orthographic candidates; where pronunciation remained unclear, **two Thai-fluent workers** supplied it. The paper does not report whether they worked independently, how disagreements were adjudicated, or inter-annotator agreement.
- Evaluation uses **10-fold cross-validation** (8/10 train, 1/10 validation, 1/10 test per fold).
- The reported Thai **0.931 accuracy** is the proportion of test entries with **zero phoneme-symbol edit distance** from the reference. It is not a tone-specific, vowel-length-specific, syllable-boundary, or acoustic accuracy measure.
- The rule-generated candidate set contained the reference pronunciation for **17,720 of 18,066 entries (~98.1%)**; 346 references were absent from the candidate sets. Candidate counts had mean 19.6, median 4, and maximum 19,242.
- The result is therefore conditional on candidate generation and a primarily Wiktionary-derived reference set. It is not a uniformly independent expert-labelled IPA gold set.

**Implication:** report candidate/lexical coverage separately from selection accuracy. A model cannot select a correct candidate that its rule lattice never generated. Do not compare the paper's 0.931 exact-match result with ClippyFirst coverage or source-attested lexical overrides.

### Rugchatjaroen et al. (2019): two-stage joint-sequence Thai G2P

A. Rugchatjaroen et al., “Efficient two-stage processing for joint sequence model-based Thai grapheme-to-phoneme conversion,” *Speech Communication* 106 (2019), 105–111. [DOI: 10.1016/j.specom.2018.12.003](https://doi.org/10.1016/j.specom.2018.12.003).

The abstract describes a two-stage CRF system: pseudo-syllable segmentation plus character-function prediction, followed by graphone-based G2P. It reports **9.94% overall WER** and says the dictionary covers over 70% of Thai word usage. The full experimental-label provenance and metric definitions were not independently re-inspected in this pass; treat these as published system results, not as independently adjudicated accuracy for this project.

**Implication:** useful architectural precedent for separating segmentation from G2P; not evidence that this repository should replace its deterministic, evidence-gated parser with a statistical model.

## Phonology and acoustic interpretation

### Lexical categories are not fixed surface contours

Morén and Zsiga, “The Lexical and Post-Lexical Phonology of Thai Tones,” *Natural Language & Linguistic Theory* 24 (2006), 113–178. [DOI: 10.1007/s11049-004-5454-y](https://doi.org/10.1007/s11049-004-5454-y).

The paper's abstract reports an acoustic argument for the mora as Thai's tone-bearing unit and discusses non-final phrasal-position contour simplification. It explicitly supports separating phonological categories from phonetic realization. This supports retaining lexical tone category in the phonological result while treating measured pitch contours as context-dependent surface evidence.

Xu and Zhang, “A cross-linguistic review of citation tone production studies: Methodology and recommendations,” *Journal of the Acoustical Society of America* 156 (2024), 2538–2565. [DOI: 10.1121/10.0032356](https://doi.org/10.1121/10.0032356).

This review identifies variation in speaker sampling, carrier phrases, F0 extraction and reporting conventions. It is a methodological source for any future acoustic tone study; it is not itself a Thai G2P gold set.

## Dataset design and annotation reliability

Pons Bordería and Aliaga, “Inter-annotator agreement in spoken language annotation: Applying uα-family coefficients to discourse segmentation,” *Russian Journal of Linguistics* 25 (2021), 478–506. [DOI: 10.22363/2687-0088-2021-25-2-478-506](https://doi.org/10.22363/2687-0088-2021-25-2-478-506).

The paper discusses unitized alpha coefficients for segmentation and labelling. For this project, boundary agreement and categorical label agreement should be reported separately; a boundary-aware reliability measure is more suitable for interval segmentation than treating each character position as an independent nominal label. The chosen coefficient and unitization protocol must be fixed before scoring.

Jitwiriyanont and Nantanukul, “Measuring phonological complexity in Thai: Adaptation and application of the word complexity measure,” *International Journal of Speech-Language Pathology* (2026). [DOI: 10.1080/17549507.2026.2651739](https://doi.org/10.1080/17549507.2026.2651739).

The abstract reports that seven existing Thai clinical wordlists overrepresent some parameters (including final consonants) and underrepresent clusters, trills and polysyllabic words. This warns against assuming that a familiar clinical wordlist is a balanced G2P challenge. The project should stratify coverage by phonological phenomena and lexical structure rather than relying on raw item count.

## Recommended evaluation protocol for ClippyFirst

The following are project recommendations derived from the studies above; they are not claims that any existing corpus already supplies the required labels.

1. **Freeze the target variety and task.** State Standard Thai scope, speaker/dialect criteria, citation-form versus connected-speech task, and whether the target is phonemic IPA, broad surface IPA, or narrow acoustic transcription. Do not mix them in one gold field.
2. **Keep input prompts separate from labels.** The current 42-item challenge and six supplemental prompts are candidate-blind review inputs, not gold. CCOST's 206-item wordlist is also prompt material only; its A–D source discrepancy must be resolved before freezing a derived packet.
3. **Use independent annotation.** Obtain two qualified Thai phonetic reviewers who annotate independently without seeing system outputs, plus a separate adjudicator for disagreements. Preserve original labels and the adjudication log. Record qualifications, dialect, task instructions, source, and conflicts.
4. **Separate lexical phonology from audio phonetics.** Broad phonemic labels may be established for controlled lexical prompts with explicit dictionary/lexical evidence and independent review. Any claim about actual surface release, glottalization, F0 contour, duration or coarticulation requires a registered audio asset, exact clean interval and acoustic protocol.
5. **Measure each layer independently.**
   - word-boundary and syllable-boundary exact match / precision / recall / F1;
   - exact phonemic IPA sequence and phone error rate;
   - segmental feature errors, with a documented alignment/feature mapping;
   - tone-category accuracy and confusion matrix;
   - vowel-length accuracy;
   - phonemic-vs-surface compatibility and release/aspiration distinctions;
   - coverage, abstention, invalid-input handling and OOV behavior;
   - Ukrainian adaptation agreement on a frozen, independently checked IPA input.
6. **Prevent source leakage.** Exclude same-source lexical overrides from independent agreement calculations. Mark Wiktionary-derived or model-derived labels as source-attested/diagnostic, not expert gold. Never use agreement between two engines as the gold reference.
7. **Report denominators and uncertainty.** Publish item counts per stratum, emitted/abstained counts, missing labels, reviewer agreement and adjudication rates. Keep all prompts in the denominator for coverage; do not silently score only easy emitted cases. If inferential scores are reported, use item/speaker-aware uncertainty estimates and disclose the sampling frame.
8. **Keep Ukrainian evaluation separate.** First validate Thai IPA and its metadata; then present the same frozen IPA inputs to at least two independent Ukrainian-native reviewers. Do not let Ukrainian spelling preferences feed back into Thai IPA labels.

## Consequences for the current repository

- No parser, tone, vowel-length, IPA or Ukrainian mapping rule is changed by this literature review alone. These papers do not adjudicate the four outstanding FastThaiG2P differences in the current challenge.
- The existing 42+6 prompts remain useful for adversarial coverage and reviewer coordination, but not for an accuracy score until independent labels are frozen.
- CCOST remains a potential controlled lexical prompt source, not IPA gold; its A–D mismatch and archive-tier inspection remain separate blockers.
- LOTUSDIS remains a candidate audio source for fresh human annotation only after immutable revision and asset-level provenance are established.
- The project remains an engineering-verified research prototype; phonetic accuracy remains **NOT_MEASURED**.

## Bibliography

- Jitwiriyanont, S. & Nantanukul, K. (2026). [10.1080/17549507.2026.2651739](https://doi.org/10.1080/17549507.2026.2651739).
- Morén, B. & Zsiga, E. C. (2006). [10.1007/s11049-004-5454-y](https://doi.org/10.1007/s11049-004-5454-y).
- Pons Bordería, S. & Aliaga, E. P. (2021). [10.22363/2687-0088-2021-25-2-478-506](https://doi.org/10.22363/2687-0088-2021-25-2-478-506).
- Rugchatjaroen, A. et al. (2019). [10.1016/j.specom.2018.12.003](https://doi.org/10.1016/j.specom.2018.12.003).
- Saychum, S. et al. (2016). [10.21437/Interspeech.2016-621](https://doi.org/10.21437/Interspeech.2016-621).
- Xu, C. & Zhang, C. (2024). [10.1121/10.0032356](https://doi.org/10.1121/10.0032356).
- Yamasaki, T. (2022). [10.18653/v1/2022.naacl-main.315](https://doi.org/10.18653/v1/2022.naacl-main.315).
