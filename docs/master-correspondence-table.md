# Thai → Ukrainian master correspondence table

## Core principle: ІРА / IPA-first

The master table does **not** collapse Thai into a character-to-character substitution.

The mandatory representation chain is:

**Thai orthography → graphemic analysis → syllable structure → phonology → tone → surface phonetics → IPA → Ukrainian phonetic target → Ukrainian phonology → Ukrainian orthography.**

Here **ІРА means IPA (International Phonetic Alphabet / МФА)** as the central phonetic intermediate representation. Tone remains a separate suprasegmental layer; it is not folded into segment identity.

The Ukrainian column contains the structured Thai-analysis candidate. A separate `ukrainian_from_ipa` field is derived independently from the parser's actual phonemic IPA. Neither is semantic translation or an official Ukrainian transliteration standard.

## Exhaustive scope

The generator enumerates the repository's declared structural space:

**44 initial graphemes × 41 vowel/rime records × (1 + 38 coda options) × 5 tone-mark states = 351,780 rows.**

This is exhaustive **within the declared structural model**. It is not a claim that 343,200 lexical Thai syllables exist.

Each row is re-parsed by the same research pipeline. The table therefore retains disagreements rather than silently forcing a result.

### Positional semantics

The system distinguishes three notions of position: syllable-internal position (onset, nucleus, coda); word position (standalone, initial, medial, final); and sentence/prosodic context, which is not inferred automatically from a word-position label.

For Standard Thai, the strongest deterministic positional alternation currently modeled is in the coda: the coda inventory is restricted, and final /p t k/ have no audible release. Orthographic consonants such as บ and ด therefore do not retain their onset values in the coda. The conservative surface layer represents these final stops as [p̚ t̚ k̚].

The vowel layer deliberately does not invent a new vowel quality merely because a syllable is open or closed. Thai vowel quantity, tone and glottal-stop behavior show documented phonetic/style variation, so deterministic allophonic rules will be added only when the project has an explicit evidence-backed rule.

## Files

- `data/derived/thai_ukrainian_master.csv` — rich audit table.
- `data/derived/thai_ukrainian_master_2col.csv` — exactly the requested presentation view: **Thai | Ukrainian**.
- `data/derived/thai_consonant_correspondence.csv` — graph-level Thai consonant table with separate onset/coda positions, phonemic IPA, conservative surface IPA and Ukrainian candidates.
- `data/derived/thai_vowel_correspondence.csv` — graph-level Thai vowel/rime table with open/closed syllable context, phonemic IPA, surface IPA and Ukrainian candidates.
- `data/derived/thai_ukrainian_master.json` — cardinality and status manifest.

The large CSVs are generated in CI and published as the `thai-ukrainian-master-table` artifact rather than hand-maintained in git.

## Rich-table semantics

The rich table keeps the structurally constructed target IPA separate from the parser's actual phonemic and surface IPA. This prevents unresolved or mismatched rows from being made to look successfully parsed. `ukrainian` is the structured-analysis candidate; `ukrainian_from_ipa` is the independent IPA-derived candidate.

The rich table keeps:

- Thai surface;
- onset grapheme and vowel-record provenance;
- coda grapheme;
- tone mark and resolved phonological tone;
- IPA;
- Ukrainian approximation;
- parser revalidation status;
- explicit non-attestation status.

This makes the two-column table convenient while preserving an inspectable research representation.

## Status discipline

A structural row can be:

- successfully revalidated;
- unresolved because the generated orthography does not license a deterministic analysis;
- invalid because the generated combination violates a declared rule;
- generation-mismatch when the generated surface does not round-trip to the intended IPA/tone.

No row is called lexical or corpus-attested without an external evidence source and an explicit denominator.

## Reproducibility

```bash
python scripts/generate_master_table.py
```

The generator reads the machine-readable Thai registries and derives the table. There is no hand-written 351,780-row lookup list.
