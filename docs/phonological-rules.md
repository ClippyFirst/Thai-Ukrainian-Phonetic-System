# Phonological rules

Implemented core rules:

1. final consonant neutralization metadata;
2. live/dead classification;
3. tone determination from consonant class, syllable type, vowel quantity and tone mark.

Planned evidence-gated rules:

- ห นำ and other class-changing constructions;
- assimilation;
- resyllabification;
- connected-speech reduction;
- morphophonological alternation;
- lexical exceptions.

A contextual rule must declare its domain and evidence before becoming an automatic global transformation.
