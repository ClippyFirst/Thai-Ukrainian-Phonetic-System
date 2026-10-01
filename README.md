# Thai → Ukrainian Phonetic-Graphemic Correspondence System

Research-oriented, machine-readable reference implementation for mapping contemporary Standard Thai orthography through phonology and surface IPA into a Ukrainian phonetic/phonological target and orthographic representation.

## Scientific pipeline

Thai orthography → graphemic analysis → syllable structure → phonology → tone → contextual rules → IPA → Ukrainian feature-space candidates → Ukrainian phonological target → Ukrainian orthography.

This is not an RTGS transliterator and not a Thai-character → Ukrainian-character lookup.

## Scope

Primary scope: contemporary Standard Thai, using the Bangkok/central-standard reference pronunciation where supported by the adopted sources.

The model separates graphemes, phonemes, positional realizations, tone marks, phonological tones, IPA and Ukrainian target candidates.

The traditional Thai consonant inventory contains 44 consonant letters; Standard Thai has a much smaller phonemic inventory. Academic descriptions commonly give 21 onset consonant phonemes and nine core final phonemes.

## Ukrainian target

The target foundation is the external repository ClippyFirst/Ukrainian-Phonetic-Inventory. This project intentionally does not duplicate the Ukrainian inventory.

## Current status

Research foundation v0.1.0. Core machine-readable consonant inventory, vowel inventory, tone inventory, tone-rule engine, provenance records, Python API skeleton and automated tests are present.

Remaining research work is explicitly tracked in docs/limitations.md: full vowel grapheme parsing, lexical segmentation, implicit-vowel grammar, class-changing constructions, contextual phonology, full IPA realization, direct Ukrainian feature adapter, corpus validation and expert review.

## Reproducibility

Run:

python scripts/generate_derived.py
python -m unittest discover -s tests -v

Generated audit data must contain computed values only.
