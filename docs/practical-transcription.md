# Thai → Ukrainian Practical Transcription

## 1. Purpose

This document specifies a practical Thai → Ukrainian transcription layer built on top of the repository's research-oriented Thai orthographic and phonological model.

The practical layer is intended for personal names, geographical names, organization and institution names, cultural and historical names, titles, and editorial/reference use where a readable Ukrainian form is required.

It is not a new Thai parser and it is not an official Ukrainian transliteration standard.

The formal distinction is: transliteration preserves a writing-system correspondence; transcription represents pronunciation or a phonologically motivated approximation. This project uses the latter as its primary objective.

## 2. Architectural principle

The practical output must never be produced by direct Thai-character substitution.

Canonical pipeline:

**Thai orthography → graphemic analysis → syllable structure → Thai phonology → tone analysis → IPA audit → Ukrainian phonetic/phonological target → practical Ukrainian orthography**

The practical layer is therefore a projection of the research model, not an independent lookup table.

The IPA layer remains independently inspectable. It is an audit/control representation; the implementation may derive the Ukrainian target directly from structured Thai phonology where this is explicitly declared.

## 3. Output contract

| Field | Meaning |
|---|---|
| thai | original Thai surface |
| segmentation | explicit syllable segmentation status |
| onset | Thai onset grapheme(s) |
| vowel | registered vowel/rime record |
| coda | Thai coda grapheme, if present |
| tone | resolved Thai tone |
| phonemic_ipa | phonemic representation |
| surface_ipa | conservative surface representation |
| ua_phonological_candidate | Ukrainian phonological candidate |
| ua_practical | practical Ukrainian spelling |
| rules | rules that produced the result |
| status | accepted / unresolved / invalid / analysis-dependent |
| evidence | source or evidence class |

A practical string must never hide an unresolved analysis.

## 4. Consonant policy

The practical system inherits the repository's positional consonant model.

Thai consonants are mapped according to their phonological value and syllable role, not according to their graphic identity alone.

| Thai phonological value | Ukrainian practical output | Principle |
|---|---|---|
| /k/ | к | aspirated/unaspirated contrast is not represented by a separate Ukrainian consonant |
| /kʰ/ | к | aspiration is not represented as х |
| /tɕ/ | ч | nearest established Ukrainian affricate target |
| /tɕʰ/ | ч | aspiration is not separately represented |
| /s/ | с | direct phonological approximation |
| /d/ | д | direct target |
| /t/ | т | direct target |
| /tʰ/ | т | aspiration is not separately represented |
| /n/ | н | direct target |
| /m/ | м | direct target |
| /p/ | п | direct target |
| /pʰ/ | п | aspiration is not separately represented |
| /b/ | б | direct target |
| /f/ | ф | direct target |
| /j/ | й | consonantal/glide realization |
| /r/ | р | onset realization |
| /l/ | л | onset realization |
| /w/ | в | Ukrainian practical approximation |
| /h/ | г | project-specific Ukrainian phonetic adaptation; not an IPA identity |
| /ŋ/ | нг* | practical Ukrainian rendering proposal |
| /ʔ/ | ∅* | no independent Ukrainian consonant letter |

* The /ŋ/ and /ʔ/ entries require explicit distinction between the research candidate layer and the practical orthographic layer. The current main correspondence registry records /ŋ/ → н as an approximate candidate; the practical layer proposes нг because it exposes the velar nasal rather than conflating it with /n/. This proposal must be represented in the Ukrainian target adapter and empirically adjudicated before being described as normative.

For /ʔ/, the absence of a consonant letter is the default practical policy. An apostrophe or other visible marker must not be introduced unless a separate editorial convention explicitly requires it.

## 5. Coda neutralization

Thai final consonants are not copied from their onset values.

| Thai onset value | Final phonological value | Ukrainian |
|---|---|---|
| /p, pʰ, b/ | /p/ | п |
| /t, tʰ, d, s/ | /t/ | т |
| /k, kʰ/ | /k/ | к |
| /m/ | /m/ | м |
| /n/ | /n/ | н |
| /ŋ/ | /ŋ/ | нг* |
| /j/ | /j/ | й |
| /w/ | /w/ | в |
| /r, l/ | /n/ | н |

The practical spelling therefore follows the pronounced final category, not the historical Thai consonant letter.

Examples: ด as onset → /d/ → д; as coda → /t/ → т. บ as onset → /b/ → б; as coda → /p/ → п. ร as onset → /r/ → р; as coda → /n/ → н. ล as onset → /l/ → л; as coda → /n/ → н.

## 6. Vowel policy

Vowels are mapped from the registered Thai vowel/rime analysis, not from the visual position of vowel signs.

The practical layer should preserve the principal vowel distinctions that can be represented naturally in Ukrainian while avoiding artificial distinctions that Ukrainian orthography cannot encode.

| Thai IPA | Ukrainian practical target |
|---|---|
| /i, iː/ | і |
| /e, eː/ | е |
| /ɛ, ɛː/ | е |
| /ɯ, ɯː/ | и |
| /ɤ, ɤː/ | е* |
| /a, aː/ | а |
| /u, uː/ | у |
| /o, oː/ | о |
| /ɔ, ɔː/ | о |

* /ɤ/ → е is a practical Ukrainian approximation, not a claim that Thai /ɤ/ and Ukrainian /e/ are identical.

Vowel length is not normally marked by doubling the Ukrainian vowel. Quantity remains part of the Thai phonological representation and may affect tone/liveness, but practical Ukrainian spelling normally requires a readable segmental representation rather than phonetic length notation.

## 7. Diphthongs and vowel + glide sequences

Registered Thai rimes must be treated as units before final-coda assignment.

The parser already distinguishes structures such as /aj/, /am/, /aːj/, /aːw/, /iw/, /uj/, /ew/, /eːw/, /ɛːw/, /ɤːj/, /ɔːj/, /oːj/, /aw/, /iaw/, /uaj/ and /ɯaj/.

The practical renderer must consume the registered rime output instead of independently translating each visible Thai vowel sign.

A rime containing /j/ or /w/ must not be mistaken for a coda consonant merely because the glide is written near the end of the Thai orthographic sequence.

## 8. Context-dependent grapheme อ

The grapheme อ has no single global practical value.

The repository's structural precedence is: special orthographic construction; registered vowel or vowel-plus-glide construction; vowel-carrier construction; explicit unresolved fallback.

Consequently, an initial carrier function does not automatically create a Ukrainian consonant; อ after a real onset can participate in /ɔː/ constructions; อ in -ือ participates in /ɯː/; standalone ไอ retains its carrier role; unresolved uses must remain unresolved rather than being forced into a letter.

The practical renderer receives the resolved structural interpretation, not the raw character อ.

## 9. Preposed vowels

Thai orthographic order and phonological order are different.

The practical system must parse preposed vowels such as ไ-, ใ-, เ-, แ- and โ- before rendering the Ukrainian output.

For example: ไ + onset → /aj/. Tone-bearing consonant selection must also occur before practical rendering.

## 10. ห นำ and effective onset

ห นำ is an orthographic/phonological transformation.

The practical renderer must distinguish the written leading ห, the effective onset for pronunciation, and the consonant class used for tone determination.

It must not simply output a Ukrainian consonant for every written Thai consonant.

For a registered ห นำ construction, the effective onset is the lower consonant while the high-class environment is retained for tone computation.

## 11. Tone

The default practical output does not encode Thai lexical tone with Ukrainian diacritics.

Tone remains a separate analytical field. Ukrainian orthography has no established one-to-one marking system for the five Thai tones, and adding tone marks would make ordinary practical output less natural.

Therefore: **Thai tone → analysis metadata**, rather than **Thai tone → mandatory Ukrainian accent mark**.

A future scholarly or pronunciation mode may expose tone separately as IPA or tone labels without changing the practical Ukrainian string.

## 12. Special orthography

The following constructions remain evidence-gated:

- รร
- ฤ / ฤๅ
- ฦ / ฦๅ
- ์ and silent-letter constructions
- lexical ทร
- อ นำ / อย
- automatic lexical segmentation
- connected-speech processes

The practical system must return an explicit analysis-dependent status where lexical evidence is necessary.

It must never convert an unresolved lexical construction into a confident spelling merely because a generic rule happens to produce a string.

## 13. Word and multi-syllable names

Thai spaces cannot be treated as universal word boundaries.

The practical system therefore supports explicitly segmented mode, where the caller supplies syllables or words and the engine preserves syllable index, standalone / initial / medial / final word position, and syllable-internal onset/nucleus/coda.

Lexicon-assisted mode may use an external lexical source for segmentation and/or pronunciation evidence.

The core engine must not invent lexical segmentation. This is especially important for proper names, where a wrong syllable boundary can propagate into tone, coda and Ukrainian spelling.

## 14. Practical rendering algorithm

1. Normalize Thai input.
2. Validate supported characters.
3. Parse Thai orthographic order.
4. Apply special orthographic rules with highest precedence.
5. Resolve registered vowel/rime construction.
6. Resolve onset and coda.
7. Apply complex-onset licensing.
8. Determine live/dead status.
9. Determine effective tone-bearing consonant class.
10. Resolve Thai tone.
11. Resolve phonemic IPA.
12. Resolve conservative surface IPA for audit.
13. Generate Ukrainian phonological candidates from the canonical Ukrainian target.
14. Apply the project-defined practical orthographic policy.
15. Render the practical Ukrainian string.
16. Preserve rules, warnings, status and evidence.
17. If a required analysis is unresolved, return unresolved rather than guessing.

Formally:

**Output = PracticalOrthography(UkrainianTarget(ThaiPhonology(Parse(ThaiOrthography(input)))))**

not:

**Output = CharacterSubstitution(input)**

## 15. Determinism and ambiguity

The system must be deterministic for all rules declared as deterministic.

Where multiple analyses are linguistically possible, preserve all declared candidates, retain analysis-dependent status, do not assign a probability unless a calibrated corpus exists, and do not label one candidate correct solely because it is generated first.

The practical layer may choose a default candidate only when the project has an explicit policy for that construction.

## 16. Examples

These examples illustrate the architecture rather than claiming corpus-wide validation.

| Thai | Structural interpretation | Practical Ukrainian |
|---|---|---|
| กา | /kaː/ | ка |
| ขา | /kʰaː/ | ка |
| คอ | /kʰɔː/ | ко |
| พอ | /pʰɔː/ | по |
| งอ | /ŋɔː/ | нго* |
| ไก่ | onset + /aj/ + tone | кай* |
| ไกล | onset + /aj/ + coda /l/ → /n/ | кан* |
| กบ | /kop̚/ | коп |
| คน | /kʰon/ | кон |
| มือ | /mɯː/ | ми |
| คือ | /kʰɯː/ | ки |
| สวน | /suaːn/ | суан |

* These practical strings depend on the /ŋ/ and rime policies described above and should be treated as implementation examples until corpus/adjudication work confirms the preferred Ukrainian spellings.

## 17. Relation to the master correspondence table

The 343,200-row structural master table remains a research artifact. It is not itself a list of 343,200 recommended Ukrainian spellings.

The practical system should instead expose a compact graph-level correspondence table, a rule registry, a deterministic renderer, an audit-rich output, and a practical two-column export.

The practical two-column artifact should be generated from the same source registries as the research table. No manually maintained duplicate rule table should become authoritative.

## 18. Recommended generated artifacts

Add or generate:

- data/derived/thai_ukrainian_practical_correspondence.csv
- data/derived/thai_ukrainian_practical_examples.csv
- data/derived/thai_ukrainian_practical_rules.json
- docs/practical-transcription.md

Suggested practical correspondence schema:

source_id,thai_input,role,thai_ipa,ua_phonological_candidate,ua_practical,rule_id,status,evidence

## 19. Validation protocol

The practical system should not be released as empirically validated until a versioned evaluation corpus exists.

Recommended evaluation strata:

1. Thai geographical names
2. personal names
3. institutional names
4. cultural/historical names
5. common lexical items
6. multi-syllable names
7. special orthography
8. coda-heavy words
9. tone-marked words
10. ห นำ and preposed-vowel constructions

Metrics should include exact practical-string match, syllable-level match, segment-level accuracy, candidate recall, unresolved/ambiguity rate, rule coverage, and error rate by construction class.

Every metric must publish its numerator and denominator.

## 20. Normative status

This document defines the project's proposed practical transcription layer, not an official Ukrainian national standard.

Three statuses must remain separate:

- implemented — encoded in the repository;
- evidence-supported — supported by declared linguistic evidence;
- empirically validated — tested against a versioned gold corpus.

The practical layer should only be promoted from project proposal to project default after the Ukrainian output has undergone corpus evaluation and, ideally, expert adjudication.

## 21. Source-of-truth policy

Thai linguistic data remain in the machine-readable Thai registries.

The Ukrainian target remains the separate canonical Ukrainian-Phonetic-Inventory project and its reproducible adapter snapshot.

Generated practical tables are derived artifacts.

Documentation must describe the same rules that the executable implementation actually consumes.

Any discrepancy between source registry, parser, generated table, practical renderer, and documentation is a release-blocking integrity issue.

## 22. Current implementation boundary

The research repository already provides the necessary foundation: 44 Thai consonant graphemes; registered Thai vowel/rime inventory; positional onset/coda analysis; live/dead classification; five-tone rule engine; ห นำ; special-orthography layer; IPA audit layer; Ukrainian candidate generation; provenance; generated correspondence tables; CLI/batch/API interfaces; regression and negative-input testing.

The remaining work for a fully operational practical transcription mode is to make the practical Ukrainian rendering policy an explicit, machine-readable layer, synchronize it with the canonical Ukrainian target adapter, add gold examples, and validate the resulting outputs.

## 23. Design principle

The practical system should be simple at the point of use while remaining rigorous under the hood.

The user should be able to enter Thai text and receive a Ukrainian practical rendering while still being able to inspect the complete chain: Thai orthography → analysis → IPA → Ukrainian target → practical output.

That separation is the central design requirement of the project.