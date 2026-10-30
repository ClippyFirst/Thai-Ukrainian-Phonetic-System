# Thai Orthographic Rule Engine

## Purpose

This document defines the machine-readable rule layer for context-dependent Thai
graphemes. The rule registry is normative for the implementation; derived tables
are generated from it for publication and audit.

## Processing principle

The system is **Thai-orthography-first**:

`Thai orthography → structural analysis → Thai phonology → Ukrainian adaptation`

IPA is rendered as an independent audit/control layer:

`Thai phonology → phonemic IPA → surface IPA`

The implementation must not require the pipeline

`Thai → IPA → Ukrainian`.

## Context-dependent grapheme: อ

The grapheme อ is not assigned one global phonological value. Its role is
determined from the complete orthographic construction.

### Deterministic precedence

1. Special orthographic constructions, including อย-.
2. Registered vowel and vowel-plus-glide patterns containing อ.
3. Vowel-carrier constructions.
4. Explicit unresolved fallback.

The implementation must never infer a glottal onset solely from the presence of
the character อ.

## Carrier

In an initial vowel construction such as อา, อ may function as a vowel carrier.
The glottal onset, when represented in IPA, belongs to the phonological audit
layer. It has no independent Ukrainian grapheme in the adaptation layer.

Thus:

`อา → structural carrier → /ʔaː/ (audit) → а`

## Vowel component

After a real onset, อ can participate in the spelling of the vowel nucleus:

`พอ → onset พ + vowel construction → /pʰɔː/ (audit) → по`

The parser must not create an additional /ʔ/ from อ in this configuration.

## Special อย-

The sequence อย- is classified before generic carrier logic. Forms such as อยู่,
อย่า and อยาก therefore require the dedicated special-orthography path.

## Evidence and unresolved states

A rule is not a lexical attestation claim. Structural recognition establishes only
that an orthographic construction matches the registry. Lexical frequency,
meaning, morphological segmentation and corpus attestation remain separate
evidence layers.

If no rule safely applies, the implementation returns an explicit unresolved
status instead of guessing.
