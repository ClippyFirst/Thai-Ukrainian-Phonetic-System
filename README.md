# Thai → Ukrainian Phonetic-Graphemic Correspondence System

Research-oriented, machine-readable reference implementation for mapping contemporary Standard Thai orthography through graphemic structure, phonology and IPA into a Ukrainian phonetic/phonological target.

## Pipeline

Thai orthography → graphemic analysis → syllable structure → phonology → lexical tone → contextual phonology → IPA → Ukrainian feature-space candidates → Ukrainian phonological target → Ukrainian orthography.

This is not RTGS and not a Thai-character → Ukrainian-character substitution table.

## Scope

Primary scope: contemporary Standard Thai with a Bangkok/central-standard reference where the evidence permits. The model separates graphemes, phonemes, positional realisations, tone marks, phonological tones, IPA and Ukrainian candidates.

The traditional Thai consonant inventory has 44 consonant letters; the phonological inventory is substantially smaller. The system keeps this distinction explicit.

## Evidence

Core implementation sources include Royal Institute publications and the JIPA description by Tingsabadh & Abramson (1993). The repository also records corpus resources for future validation, including CCOST and Thai G2P data.

## Ukrainian target

The canonical target is ClippyFirst/Ukrainian-Phonetic-Inventory. This repository uses a reproducible feature-vector adapter rather than duplicating the entire target inventory.

## Status

This release is a substantially expanded research foundation. Implemented: 44-letter consonant inventory, vowel-sign parser, tone engine, live/dead logic, conservative broad IPA composition, feature-ranked Ukrainian candidate generation, evidence registry, combinatorial-space accounting, validation schemas, tests and CI.

Not claimed complete: exhaustive lexical segmentation, complete special-spelling grammar, connected-speech phonetics, corpus-calibrated probabilities, or universally validated Ukrainian orthographic output.

## Reproducibility

Run:

python scripts/generate_derived.py
python scripts/generate_syllable_space.py
python -m unittest discover -s tests -v

Derived JSON files contain computed values only.
