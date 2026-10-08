# IPA → Ukrainian adaptation — design specification

Date: 2026-10-08
Repository: ClippyFirst/Thai-Ukrainian-Phonetic-System
Scope: phonemic/conservative surface IPA → Ukrainian practical phonetic rendering.

## 1. Goal

Build the Ukrainian adaptation layer as a genuinely independent linguistic layer.

The input to this layer is IPA plus structured phonetic metadata. It must not inspect Thai graphemes, Thai consonant classes, Thai vowel signs, or Thai-specific orthographic rules. Thai orthography is resolved upstream.

The central invariant is that Ukrainian rendering is an adaptation, not an IPA character-substitution table.

Canonical regression example:

- IPA input: `kʰaː`
- Ukrainian output: `ка`

The aspirated /kʰ/ and vowel length /aː/ remain truthful in the IPA layer but are not automatically represented as additional Ukrainian letters because Ukrainian orthography does not have those contrasts as independent practical-transcription graphemes in this system.

## 2. Architectural boundary

Pipeline:

Thai orthography
→ orthographic analysis
→ Thai phonology
→ phonemic IPA
→ conservative surface IPA
→ IPA feature analysis
→ Ukrainian candidate generation
→ candidate ranking
→ Ukrainian practical transcription.

The Ukrainian layer must consume a normalized intermediate representation containing, at minimum:

- IPA segment sequence;
- syllable boundaries;
- onset/nucleus/coda roles;
- segment features;
- phonemic vs surface status;
- vowel length;
- aspiration;
- relevant positional metadata;
- evidence/status metadata.

It must never recover Thai identity from the IPA string.

## 3. Approaches considered

### A. Direct IPA → Ukrainian substitution

Example: `kʰ` → `кх`.

Rejected as the primary architecture because it treats phonetic detail as if every IPA distinction required a Ukrainian orthographic symbol. It also becomes brittle for allophony, positional neutralization, and many-to-one adaptation.

### B. IPA → features → Ukrainian candidates → ranking

Recommended foundation.

Each IPA segment is decomposed into relevant phonetic features. The engine generates Ukrainian candidates, records which features are preserved or neutralized, and ranks candidates according to declared adaptation rules.

This permits:

`k` and `kʰ` → `к`

without pretending that aspiration was absent from the source IPA.

### C. Feature candidates plus contextual rule graph

Recommended as the second implementation layer on top of B.

Contextual rules handle onset/coda position, syllable boundaries, adjacent segments, Ukrainian phonotactics, and established adaptation conventions. This is preferable to embedding context in hundreds of unrelated direct substitutions.

## 4. Recommended architecture: B → C

### 4.1 Segment normalization

Parse IPA into a structured sequence rather than manipulating Unicode substrings with ad-hoc replacements.

Each segment/token records:

- base IPA symbol;
- modifiers;
- manner;
- place;
- voicing;
- aspiration;
- vowel quality;
- vowel length;
- glide/semi-vowel status;
- syllable role;
- source status.

Combining marks and multi-codepoint IPA sequences must be normalized before matching.

### 4.2 Feature inventory

The adapter must distinguish at least:

Consonants:
- place: bilabial, labiodental, dental/alveolar, postalveolar/palatal, velar, glottal;
- manner: stop, affricate, fricative, nasal, lateral, rhotic, glide;
- voicing;
- aspiration;
- sonority;
- onset/coda role.

Vowels:
- height;
- backness;
- rounding;
- length;
- diphthong/glide structure.

Only features relevant to Ukrainian adaptation should influence candidate ranking. Retaining a feature in the source representation does not imply that it must survive in Ukrainian spelling.

## 5. Ukrainian adaptation policy

### 5.1 Contrast preservation vs neutralization

The system explicitly classifies each source distinction as:

- preserved;
- neutralized;
- contextually adapted;
- uncertain.

Examples:

| IPA | Practical UA | Treatment |
|---|---|---|
| `k` | к | preserved core place/manner |
| `kʰ` | к | aspiration neutralized |
| `p` | п | preserved core place/manner |
| `pʰ` | п | aspiration neutralized |
| `t` | т | preserved core place/manner |
| `tʰ` | т | aspiration neutralized |
| `a` | а | preserved |
| `aː` | а | length neutralized by default |
| `ŋ` | context-dependent candidate(s) | requires dedicated nasal adaptation |
| `tɕ` | context-dependent candidate(s) | Ukrainian-compatible affricate adaptation |
| `ɯ` | context-dependent candidate(s) | Ukrainian vowel approximation |
| `ɤ` | context-dependent candidate(s) | Ukrainian vowel approximation |

The table is a policy skeleton, not the final exhaustive mapping. Every non-trivial mapping must be backed by a declared rule and regression tests.

### 5.2 The `kʰaː → ка` invariant

This case is mandatory and must remain stable throughout refactoring.

The engine must NOT:

- emit `кха`;
- emit `каа`;
- rewrite upstream IPA from `kʰaː` to `ka`;
- use Thai orthography to special-case the result.

Instead:

1. IPA parser recognizes `kʰ` + `aː`;
2. feature layer identifies aspiration and length;
3. adaptation policy marks aspiration and length as neutralized for the default Ukrainian practical layer;
4. candidate generation produces `ка`;
5. audit metadata records the neutralizations.

This is the model case for the entire architecture.

## 6. Candidate generation

Candidate generation is deterministic and finite.

For each source segment or segment group, generate only candidates licensed by the Ukrainian adaptation registry.

A candidate contains:

- candidate ID;
- Ukrainian output;
- source IPA pattern;
- preserved features;
- neutralized features;
- contextual constraints;
- evidence status;
- priority/ranking weight;
- explanatory note.

Candidates must never be generated merely because an IPA symbol is visually similar to a Ukrainian letter.

## 7. Candidate ranking

Ranking is rule-based and reproducible, not an opaque probability.

Primary ranking dimensions:

1. Ukrainian phonetic plausibility;
2. preservation of salient source contrasts;
3. Ukrainian phonotactic legality;
4. contextual compatibility;
5. consistency with declared adaptation conventions;
6. evidence strength;
7. simplicity / minimum unnecessary orthographic material.

The selected result must retain an audit trail explaining why competing candidates were rejected or ranked lower.

A numerical score may be used internally, but it must not be presented as empirical probability unless calibrated against a declared gold corpus.

## 8. Context and syllable structure

The engine must support:

- onset vs coda;
- word-initial vs medial vs final;
- syllable boundaries;
- consonant adjacency;
- vowel/glide sequences;
- word boundaries.

Contextual adaptation must operate on the IPA representation and structured metadata only.

Thai-specific concepts such as Thai consonant class, tone class, tone mark, or spelling order are forbidden dependencies in this layer.

## 9. Aspiration

Aspiration is represented faithfully upstream and neutralized downstream by policy where Ukrainian practical transcription does not require a separate symbol.

Therefore:

- `pʰ → п`;
- `tʰ → т`;
- `kʰ → к`;
- `tɕʰ` must be evaluated separately from `kʰ`, because the base manner/place differs.

The system must not generalize aspiration deletion by string replacement alone. It must operate on structured segments/features.

## 10. Vowel length

IPA vowel length is preserved in the source layer.

Default Ukrainian practical transcription does not encode length as a doubled vowel.

Therefore:

- `a → а`;
- `aː → а`.

Length remains available in audit metadata so that a future adaptation mode can make a different evidence-backed choice without changing Thai → IPA.

## 11. Tone

Tone remains a separate feature from the segmental Ukrainian output.

Default Ukrainian practical transcription must not invent Ukrainian letters solely to encode Thai tone.

The architecture must allow:

- segmental Ukrainian result;
- tone metadata;
- optional future tone-marking policy.

Tone must not leak into segment substitution rules.

## 12. Unresolved and ambiguous IPA

The adapter must never fabricate Ukrainian output from an unresolved IPA input.

Required states:

- analyzed;
- analysis-dependent;
- unresolved;
- invalid.

For unresolved/invalid source analysis, Ukrainian output is null unless a declared alternative interpretation is explicitly selected.

The UI/API must not turn null into `?` or any other placeholder that looks like a valid transcription.

## 13. Data source and Ukrainian inventory

The canonical Ukrainian phonetic target inventory must come from the project's shared Ukrainian phonetic inventory source rather than being duplicated locally.

This repository may contain a generated, pinned snapshot or adapter-specific view when reproducibility requires it.

The IPA → Ukrainian adaptation registry remains repository-specific because practical transcription policy is not identical to a generic Ukrainian phoneme inventory.

No independent hard-coded IPA inventory may be duplicated in production code.

## 14. Output and audit model

Each syllable/word result should expose:

- source IPA;
- normalized IPA;
- Ukrainian candidates;
- selected Ukrainian candidate;
- applied adaptation rules;
- preserved features;
- neutralized features;
- warnings;
- evidence/status.

The human-readable output remains concise, while the machine-readable analysis remains inspectable.

Example audit record conceptually:

`kʰaː`
→ candidates: `ка`
→ selected: `ка`
→ neutralized: aspiration, vowel-length
→ status: analyzed.

## 15. Testing strategy

TDD is mandatory for behavior changes.

### Core invariants

- `kʰaː → ка`;
- `kaː → ка`;
- `kʰa → ка`;
- `kʰaː` and `ka` may converge in Ukrainian output without becoming identical in source IPA;
- upstream Thai → IPA is never modified to satisfy Ukrainian output.

### Consonant tests

Cover:

- aspirated/unaspirated stops;
- voiced/voiceless distinctions where relevant;
- affricates;
- fricatives;
- nasals;
- `ŋ`;
- liquids;
- glides;
- glottal segments;
- onset/coda differences.

### Vowel tests

Cover:

- short/long pairs;
- front/central/back vowels;
- rounded/unrounded vowels;
- diphthongs and glide sequences;
- context-sensitive vowel adaptation.

### Context tests

Cover:

- onset;
- coda;
- word boundaries;
- syllable boundaries;
- consonant clusters;
- adjacent glides.

### Negative tests

The system must reject or withhold output for:

- malformed IPA;
- unknown IPA symbols;
- unresolved analyses;
- contradictory metadata;
- unsupported feature combinations.

### End-to-end tests

Include Thai examples where the same IPA is produced by different orthographic structures. Their Ukrainian result must depend on IPA/metadata, not Thai spelling identity.

## 16. Python/browser parity

Python remains the reference implementation.

The browser engine must expose the same adaptation semantics and versioned fixtures.

Parity fixtures must compare:

- normalized IPA;
- parsed segment/features;
- candidate set;
- selected candidate;
- applied rules;
- preserved/neutralized features;
- status;
- final Ukrainian output.

Any semantic mismatch fails CI.

## 17. Documentation

Documentation must explicitly explain:

- why IPA is not copied symbol-for-symbol;
- why `kʰaː → ка`;
- which contrasts Ukrainian transcription preserves;
- which contrasts it neutralizes;
- the distinction between phonetic truth and orthographic representation;
- evidence status of non-obvious mappings;
- limitations and unresolved cases.

The project must avoid presenting the adaptation layer as an official Ukrainian transliteration standard unless a separate normative basis exists.

## 18. Non-goals

This stage does not:

- alter Thai → IPA rules;
- infer Thai orthography from IPA;
- encode Thai spelling-specific exceptions downstream;
- claim a universal Ukrainian transliteration standard;
- introduce probabilistic ML ranking without a gold corpus;
- force every IPA distinction into Ukrainian orthography;
- use Ukrainian output to validate upstream Thai phonology.

## 19. Acceptance criteria

The IPA → Ukrainian overhaul is complete only when:

1. the layer consumes IPA/features rather than Thai orthography;
2. `kʰaː → ка` is covered by regression tests and remains stable;
3. aspiration and vowel length can be neutralized without changing upstream IPA;
4. candidate generation and ranking are deterministic and auditable;
5. Ukrainian target inventory is sourced from the shared inventory architecture;
6. no fabricated output is produced for unresolved/invalid IPA;
7. tone remains separate from segmental adaptation;
8. Python and browser implementations are semantically equivalent;
9. high-risk mappings have adversarial tests;
10. generated artifacts are reproducible;
11. documentation describes the actual implementation and evidence status;
12. full CI is green before release.

## 20. Research principle

The system must preserve the distinction between three different questions:

1. **What is the Thai pronunciation?**
2. **What is its IPA representation?**
3. **How should that pronunciation be practically rendered for a Ukrainian reader?**

The answer to question 3 must never be allowed to distort questions 1 or 2.

In particular, `kʰaː → ка` means:

> the Thai pronunciation retains aspiration and vowel length at the IPA layer, while the Ukrainian practical layer deliberately neutralizes those two features.

That separation is the core scientific contract of the IPA → Ukrainian architecture.
