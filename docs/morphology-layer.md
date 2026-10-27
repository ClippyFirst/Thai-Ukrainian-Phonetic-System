# Conservative Thai morphology diagnostics — research-only

## Status

**PARTIAL / research-only.** The web UI now displays a separate set of contextual grammatical-marker candidates. This is not a complete Thai morphological analyzer, a POS tagger, a syntactic parser, or an independently validated morphological gold system.

The implementation is deliberately downstream of tokenization and separate from phonology. It does not change syllable analysis, IPA, tone, or the IPA → Ukrainian adapter. It must never be described as “fully correct Thai morphology”.

## What is implemented

The analyzer consumes an existing token sequence and emits rule-ID-bearing candidate annotations for a limited closed set of forms:

| Rule | Surface cue | Candidate function | Guard / uncertainty |
|---|---|---|---|
| TH-MORPH-NEG-001 | ไม่ followed by a Thai token | Negation marker | Scope and predicate boundary are not established |
| TH-MORPH-MOD-001 | จะ before a Thai token | Prospective/modal marker | Not a verb inflection; lexical/modal ambiguity remains |
| TH-MORPH-ASP-001/002 | กำลัง … อยู่ | Progressive-construction candidates | Both elements can have other uses; tokenization and scope remain unverified |
| TH-MORPH-ASP-003 | แล้ว after a Thai token | Completive/change-of-state candidate | Context-dependent; lexical/discourse uses are possible |
| TH-MORPH-ASP-004 | เคย before a Thai token | Experiential marker | Predicate and scope are not parsed |
| TH-MORPH-Q-001 | ไหม at the end of input or before a politeness closer | Polar-question particle | Clause-final status is inferred from the supplied span, not a sentence parser |
| TH-MORPH-POL-001 | ครับ/ค่ะ/คะ/จ้ะ/จ๊ะ at the end | Politeness/register particle | Speaker, interactional context and lexical use are unknown |
| TH-MORPH-COORD-001 | และ between Thai tokens | Coordinator | Constituent categories are unknown |
| TH-MORPH-GEN-001 | ของ between Thai tokens | Possessive/genitive linker | Relationship between constituents is unverified |
| TH-MORPH-NOM-001 | การ/ความ before a Thai token | Nominalizer candidate | The base, construction and lexicalization must be checked |
| TH-MORPH-VOICE-001 | ถูก/โดน before a Thai token | Passive/affected-construction candidate | These forms can also be lexical verbs |
| TH-MORPH-AMB-001 | อยู่ after another token without a prior กำลัง | Aspectual or lexical use | Explicitly analysis-dependent |

The browser and Python implementations use the same stable rule IDs and candidate semantics. The Python opt-in entry point is `thai_ukrainian.text.analyze_text_morphology(text)`. It returns the segmented token sequence, the segmenter's completeness metadata, and the separate morphology result. The public website shows candidates in a visibly provisional panel; it does not silently change the main phonetic output.

## Why this is not a full morphology engine

Thai has limited inflection compared with many Indo-European languages, but morphology and morphosyntax are not absent. Relevant phenomena include compounding, derivation/nominalization, reduplication, classifier constructions, serial-verb constructions, particles, lexicalization, and context-sensitive category changes. A list of function words cannot resolve all of those phenomena.

The implementation inherits boundaries from the existing dictionary maximum-match segmenter. That segmenter is known to be partial and can choose incorrect boundaries. Consequently, a candidate can be missed or assigned to the wrong token if upstream segmentation is wrong. No POS tags, dependency structure, confidence scores, or gold accuracy values are fabricated.

## Evidence and sources

- Iwasaki, Shoichi & Preeya Ingkaphirom. 2005. *A Reference Grammar of Thai*. Cambridge University Press. The reference grammar treats aspect, pragmatic particles, relative clauses, question formation, passive and causative constructions, and word structure as distinct topics. [Publisher record](https://books.google.com/books/about/A_Reference_Grammar_of_Thai.html?id=YE29njS4qSUC).
- Smyth, David. *Thai: An Essential Grammar*, 3rd ed. Routledge. The reference covers noun phrases/classifiers, sentence particles, negation, questions, time and Thai speech conventions. [Publisher record](https://www.routledge.com/Thai-An-Essential-Grammar-3rd-Edition/Smyth/p/book/9781032956299).
- Li, Aliang. 2024. “Nominalizations and its grammaticalization in standard Thai.” *Folia Linguistica* 58(2): 291–326. DOI: [10.1515/flin-2024-2006](https://doi.org/10.1515/flin-2024-2006). The paper analyzes การ, ความ, and การที่ nominalization strategies, supporting the decision to treat nominalizer cues as construction-dependent rather than universal prefix rules.
- Dékány, Éva. 2026. “The (post-)syntax of repeater classifiers: A case study in Thai.” *Journal of Linguistics*. DOI: [10.1017/S0022226726101169](https://doi.org/10.1017/S0022226726101169). This research shows why classifier/reduplication phenomena require dedicated structural analysis rather than token matching.

These sources motivate the covered categories; they do **not** adjudicate each output candidate for arbitrary text. No source sentence is being redistributed as a dataset, and no source is claimed to provide the missing project-specific morphological gold set.

## Acceptance gates for a genuine morphology release

1. Define a versioned annotation schema for word boundaries, morpheme boundaries, lexical category, grammatical function, scope, ambiguity and source provenance.
2. Build a rights-cleared, representative Standard Thai corpus with independently adjudicated word and morpheme boundaries; keep training, development and test splits disjoint.
3. Include compounds, productive and lexicalized reduplication, derivational nominalizers, classifiers, negation, aspect/modality, questions, politeness particles, serial verbs, names, punctuation, informal text and ambiguous forms.
4. Require at least two independent annotators plus documented adjudication for the held-out gold sample; report inter-annotator agreement and exact/segment-level precision, recall and F1 by phenomenon.
5. Evaluate segmentation separately from morphology. Never treat agreement with a dictionary tokenizer as morphological correctness.
6. Add adversarial cases for token-boundary errors and polyfunctional forms; the analyzer must preserve alternatives or abstain where evidence is insufficient.
7. Keep morphology output independent of the IPA → Ukrainian path and prove by regression that adding/removing morphology annotations cannot change phonetic output.
8. Verify Python/browser rule parity and the deployed UI contract on the exact commit before calling the website update deployed.

Until these gates pass, the honest status is **a conservative morphology-candidate overlay on a partial research prototype**, not a complete or fully accurate morphology engine.
