# Thai → Ukrainian master correspondence table

## Principle

The table is **IPA-first**:

Thai orthography → graphemic/phonological analysis → IPA → Ukrainian approximation.

The Ukrainian column is not character-for-character substitution and not semantic translation. It is a project-defined phonetic/phonological approximation derived from IPA. Thus Thai /ŋ/ may be rendered approximately as Ukrainian **н** in this layer without claiming that /ŋ/ and /n/ are identical.

## Exhaustive scope

The master artifact exhaustively enumerates the repository's declared structural combinatorial space:

44 initial graphemes × 40 vowel/rime records × (1 + 38 coda options) × 5 tone-mark states = **343,200 rows**.

This is a structural enumeration, not a lexicon. A row can be structurally enumerable while still being orthographically constrained, phonotactically unavailable, non-lexical, or unresolved.

## Artifacts

- `data/derived/thai_ukrainian_master.csv` — audit/research table with IPA, tone, Ukrainian approximation, status and provenance.
- `data/derived/thai_ukrainian_master_2col.csv` — simple presentation view: `Thai | Ukrainian`.
- `data/derived/thai_ukrainian_master.json` — generation manifest and status counts.

The two-column file is deliberately derived from the same generator as the rich artifact. The full CSV is emitted as a GitHub Actions artifact rather than committed to git, keeping the source repository reviewable while preserving a reproducible downloadable table.

## Status

- `tone-resolvable-structural`: the declared tone-rule registry resolves the generated tone.
- `structural-tone-unresolved`: no declared tone rule resolves the generated tone-mark/class/live-dead combination.

Neither status establishes lexical or corpus attestation.

## Reproducibility

Run:

```bash
python scripts/generate_master_table.py
```

The generator reads the machine-readable consonant, vowel and tone-rule registries; there is no hand-maintained 343,200-row substitution list.
