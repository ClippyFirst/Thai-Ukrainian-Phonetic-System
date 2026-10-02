# Thai → Ukrainian master correspondence table

## Core principle: ІРА / IPA-first

The master table does **not** collapse Thai into a character-to-character substitution.

The mandatory representation chain is:

**Thai orthography → graphemic analysis → syllable structure → phonology → tone → surface phonetics → IPA → Ukrainian phonetic target → Ukrainian phonology → Ukrainian orthography.**

Here **ІРА means IPA (International Phonetic Alphabet / МФА)** as the central phonetic intermediate representation. Tone remains a separate suprasegmental layer; it is not folded into segment identity.

The Ukrainian column is therefore a **phonetic/phonological approximation**, not semantic translation and not an official Ukrainian transliteration standard. A Ukrainian rendering is only generated from the IPA layer, never directly from the Thai grapheme.

## Exhaustive scope

The generator enumerates the repository's declared structural space:

**44 initial graphemes × 40 vowel/rime records × (1 + 38 coda options) × 5 tone-mark states = 343,200 rows.**

This is exhaustive **within the declared structural model**. It is not a claim that 343,200 lexical Thai syllables exist.

Each row is re-parsed by the same research pipeline. The table therefore retains disagreements rather than silently forcing a result.

## Files

- `data/derived/thai_ukrainian_master.csv` — rich audit table.
- `data/derived/thai_ukrainian_master_2col.csv` — exactly the requested presentation view: **Thai | Ukrainian**.
- `data/derived/thai_ukrainian_master.json` — cardinality and status manifest.

The large CSVs are generated in CI and published as the `thai-ukrainian-master-table` artifact rather than hand-maintained in git.

## Rich-table semantics

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

The generator reads the machine-readable Thai registries and derives the table. There is no hand-written 343,200-row lookup list.
