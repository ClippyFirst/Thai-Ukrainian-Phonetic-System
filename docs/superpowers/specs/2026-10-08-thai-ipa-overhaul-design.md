# Thai → IPA overhaul — design specification

Date: 2026-10-08
Repository: ClippyFirst/Thai-Ukrainian-Phonetic-System
Scope: Thai orthography → IPA only. Ukrainian rendering is explicitly out of scope for this overhaul.

## 1. Goal
Make the Thai→IPA layer research-grade, deterministic where the orthography and evidence license a deterministic analysis, and explicitly non-fabricating where the evidence does not.
The system must distinguish: phonological/broad IPA; conservative surface/narrow IPA; tone category vs phonetic contour; established deterministic rules vs evidence-dependent analyses.
No Ukrainian output is used to validate Thai IPA.

## 2. Source of truth
Machine-readable inventories are authoritative for segmental IPA: consonant inventory supplies onset/coda IPA; vowel inventory supplies vowel nuclei and registered glide/rime patterns; tone rules supply tone category and evidence status.
Python and browser code must not contain independent duplicated IPA inventories.
Every IPA symbol used by the engine must be traceable to a data record or an explicitly documented rule.

## 3. Segmental representation
The engine must correctly model the 44 Thai consonant graphemes and their phonological classes; onset vs coda neutralization; aspiration contrasts; /tɕ/ vs /tɕʰ/; /ʔ/ as a carrier/onset where linguistically appropriate, never as a final consonant; /ŋ n m k t p j w/ coda classes; sonorant/liquid behavior; ห นำ without retaining silent ห as an extra phonetic segment; valid consonant clusters and cluster-specific IPA; special orthographic analyses only when explicitly evidenced.
The implementation must never create an IPA string containing an unresolved placeholder such as ?.

## 4. Vowels and rimes
The core inventory must represent the Standard Thai contrastive vowel system with length, including /i iː e eː ɛ ɛː ɯ ɯː ɤ ɤː a aː u uː o oː ɔ ɔː/ and /ia iaː ɯa ɯaː ua uaː/ where the repository's adopted analysis treats them as diphthongs.
Contextual complex nuclei/glide sequences such as /aj am aw ew/ are represented only where the orthographic parse licenses them.
The data model must not imply that every registered contextual rime is a separate phonemic vowel.
Long/short status must be preserved independently from spelling pattern. Closed-syllable behavior must be explicit rather than silently changing the underlying vowel.

## 5. Tone
Tone assignment is separated into: orthographic tone-class derivation; phonological tone category; IPA tone representation.
The engine preserves the five-way Standard Thai contrast and validates tone-marker/class/live-dead combinations.
Tone letters or Chao-value contours may be exposed only when their evidence status is explicit. A contour must not be presented as universally exact acoustic realization.
If literature provides multiple defensible phonetic contour analyses, the system marks the representation evidence-dependent rather than inventing a single narrow contour.
Invalid combinations return no tone IPA and no syllable IPA.

## 6. Phonemic vs phonetic IPA contract
phonemic_ipa is the conservative segmental analysis plus phonological tone metadata; it must be reproducible from evidence-backed inventories/rules.
phonetic_ipa is a deliberately conservative surface layer. It may add only documented deterministic positional realizations, such as final stop unreleasedness, supported by repository evidence.
It must not pretend to be an acoustic measurement.
Both fields are null for non-analyzed/invalid syllables.

## 7. Status semantics
First-class states: analyzed; analysis-dependent; unresolved; invalid.
analyzed → complete IPA may be returned. analysis-dependent → IPA only if the selected interpretation is explicitly evidence-backed; otherwise null. unresolved → null IPA. invalid → null IPA.
No UI or API layer may turn null into ? and call it IPA.

## 8. Orthographic edge cases
Regression coverage must include: preposed vowels (เกะ, เก, เกา, ไกล, ใกล้, ไก่); ห นำ (หงา, ไหม, ไหว้); special orthography (รร, ทร, จร, สร, ศร, ซร, ฤ/ฤๅ, ฦ/ฦๅ, การันต์); implicit/inherent vowel (คน and comparable forms); coda licensing and final neutralization; consonant clusters vs false clusters; invalid tone forms such as ค๊า; punctuation/unsupported input; obsolete consonant graphemes; carrier อ.

## 9. API and browser parity
The browser service must consume the same semantic rules/data as Python wherever technically possible.
Parity fixtures compare normalized input, segmentation, status, onset/coda, vowel ID/length, tone category, tone representation and evidence status, phonemic IPA, and phonetic IPA.
A parity mismatch fails CI.

## 10. Documentation and evidence
Documentation must state the adopted Thai analysis, source provenance for each major rule family, broad vs narrow IPA policy, limits of acoustic claims, unresolved/analysis-dependent cases, and why registry cardinality is not phoneme-inventory cardinality.
Primary evidence should include JIPA Thai, Royal Institute material, and relevant Thai phonology/phonetics literature. Competing analyses must be identified where they materially affect implementation.

## 11. Testing standard
Use TDD for behavior changes.
Required classes: inventory completeness; every consonant onset/coda behavior; vowel inventory and length; tone-rule exhaustiveness and invalid combinations; cluster parsing; special orthography; edge-case IPA; status/IPA invariants; Python/browser parity; generated artifacts; full repository test suite.
A test that can pass with an unresolved placeholder or fabricated IPA is insufficient.

## 12. Non-goals
This release does not optimize Ukrainian transliteration; redesign Ukrainian candidate ranking; claim dialect coverage beyond the adopted Standard Thai/Bangkok-oriented evidence; infer speaker-specific acoustic trajectories without acoustic data; or treat every Thai spelling as lexically unambiguous.

## 13. Acceptance criteria
The overhaul is complete only when: all IPA is traceable to data/rules; no duplicated IPA source remains in production code; invalid/unresolved/analysis-dependent cases cannot emit fabricated IPA; tone semantics and phonetic contour claims are explicitly separated; edge-case tests cover the complete high-risk inventory; Python and web outputs are semantically equivalent; generated artifacts are reproducible; full CI is green; documentation matches implementation; Notion records final evidence-backed status and remaining scientific limitations.