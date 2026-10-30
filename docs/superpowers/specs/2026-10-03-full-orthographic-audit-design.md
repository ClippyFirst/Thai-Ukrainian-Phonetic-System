# Full Thai Orthographic / Syllable Audit — design specification

## Goal

Apply the same evidence-first methodology used for `อ` to the remaining context-dependent Thai grapheme and syllable constructions in the declared Standard Thai scope.

Primary pipeline:

`Thai orthography → structural orthographic analysis → Thai phonology → Ukrainian adaptation`

Independent audit:

`Thai phonology → phonemic IPA → conservative surface IPA`

IPA must remain a control/audit layer and must not become the source string for Ukrainian output.

## Audit findings

The repository is structurally strong but the `อ` audit exposed four additional material classes that are not yet modeled with the same rigor:

1. **Composite vowels containing `อ` after a real onset**
   - `พอ, ขอ, คอ, งอ, ของ, กร` require the `-อ` /ɔː/ construction rather than treating `อ` as an onset or leaving the vowel implicit.
   - `คือ, มือ, หนังสือ` require the `-ือ` /ɯː/ construction.
   - `เธอ` and related `เ-อ` forms must remain distinct from carrier `อ`.

2. **Reduced `อัว` written with `ว`**
   - `สวน, กวน, ควร, รวม` and related forms use `ว` as a vowel component, not an ordinary onset/coda.
   - This must be resolved structurally before generic consonant splitting.

3. **Unwritten/inherent vowels**
   - A supplied bare consonant sequence can encode an inherent vowel.
   - For a supplied single-syllable surface, the conservative deterministic rule is:
     - two consonants with the second serving as a licensed final → short inherent /o/;
     - a licensed complex onset followed by a licensed final → short inherent /o/;
     - single bare consonants and ambiguous multi-syllable consonant strings remain unresolved without lexical evidence.
   - This prevents both the old “guess /a/” problem and the current over-conservative rejection of clear closed inherent-o syllables.

4. **Orthographic role of `ย` / `ว`**
   - These remain ordinary consonants in onset/coda contexts.
   - They become vowel/glide components only when consumed by a registered rime construction.
   - The parser must expose that structural decision rather than silently treating every occurrence as a consonant.

## Source-backed scope

The audit uses:
- NECTEC Standardization and Implementations of Thai: 44 consonants, 32 core vowel forms, vowel-composing consonants `ย ว อ`, tone marks and Thai character classes.
- Tingsabadh & Abramson (JIPA) for the Standard Thai phonological inventory.
- Royal Institute material for orthographic order and vowel construction.
- Slayden Central Thai phonology/reference material for inherent vowels, `ออ`/reduced `อัว`, clusters and positional structure.

The implementation must distinguish normative orthographic facts, phonological modeling decisions, project Ukrainian adaptations, and lexical/corpus evidence.

## Implementation decisions

### A. Vowel registry

Extend the machine-readable rime registry with the missing reduced `อัว` construction as a dedicated record.

Correct `ไ/ใ` metadata to short rather than long; its syllable can still be live because the final glide is /j/.

Do not collapse orthographic variants merely because their phonemic output is identical.

### B. Vowel detection

Make vowel detection construction-aware:
- match composite patterns before generic single signs;
- recognize `-อ` as /ɔː/ after a real onset;
- recognize `-ือ` as /ɯː/ after a real onset;
- recognize reduced `-ว-` /ua/ when structural evidence shows `ว` is the vowel component;
- preserve explicit terminal glide information;
- never consume a vowel-component `ย`/`ว` as an onset/coda.

### C. Inherent vowel

Add a machine-readable rule registry for the deterministic closed-syllable inherent /o/ case.

The parser must retain an explicit evidence status such as `registry` / `analysis-dependent`, and must not claim lexical segmentation.

Tone calculation must use the resulting syllable structure and the existing cluster tone rules.

### D. Special constructions

Keep lexical/morphology-dependent constructions explicit:
- `รร`
- `ฤ/ฤๅ`
- `ฦ/ฦๅ`
- `ทร`
- `์`
- `อย-`

These remain analysis-dependent unless a deterministic structural rule is justified.

### E. Ukrainian adaptation

Keep the structured Thai→Ukrainian layer separate from IPA candidate ranking.

Use explicit mapping semantics:
- /ʔ/ → zero
- /h/ → `г` as the project orthographic adaptation default
- /ŋ/ → `нг` as an orthographic sequence
- /tɕ/ and /tɕʰ/ → `ч`
- /w/ → `в`
- /j/ → `й`

These are project adaptations, not claims of IPA identity or an official Thai→Ukrainian standard.

### F. Validation

Add regression fixtures covering at minimum:
- `พอ, ขอ, คอ, งอ, สอง, ของ, คือ, มือ, เธอ`
- `สวน, กวน, ควร, รวม`
- `กบ, คน, ผล, ส่ง, กร`
- `อา, อัน, อาย, ไอ`
- `ไก่, ขาย, ไหม, ไหว้`
- `หงา, หมา, หนู`
- `อยู่, อย่า, อยาก`
- malformed/ambiguous bare consonant strings must remain unresolved where lexical evidence is genuinely required.

Add invariants:
1. every parser vowel ID exists in the registry;
2. every consumed structural vowel component is absent from onset/coda;
3. no registered terminal glide is duplicated as coda;
4. every analyzed syllable has a deterministically explained structural path;
5. Ukrainian output is generated from structured analysis, not IPA;
6. publication tables are generated from the same registries used by the parser.

## Explicit non-goals

This pass does not claim:
- complete Thai lexical segmentation;
- complete morphology-dependent orthography;
- complete learned/Pali-Sanskrit pronunciation;
- complete connected-speech phonetics;
- empirical Ukrainian orthographic preference;
- corpus accuracy.

## Acceptance gate

The implementation is complete only when:
- unit/regression tests pass;
- the exhaustive generator completes locally/CI;
- generated artifacts are synchronized;
- the final audit document records remaining unresolved classes explicitly;
- no release document claims a green CI state for a commit that has not actually been verified.
