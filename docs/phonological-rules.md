# Phonological rules

Implemented core rules:

1. final consonant neutralization metadata;
2. live/dead classification;
3. separation of written onset class from tone-bearing consonant class in multi-consonant onsets;
4. tone determination from tone-bearing class, syllable type, vowel quantity and tone mark.

Planned evidence-gated rules:

- broader ห นำ and class-changing constructions beyond the implemented leading ห + low-single rule;
- assimilation;
- resyllabification;
- connected-speech reduction;
- morphophonological alternation;
- lexical exceptions.

For multi-consonant onsets, the current tone-class rule uses the first consonant when the second is sonorant and the second consonant when it is non-sonorant. Leading-consonant constructions such as ห นำ are handled separately.

A contextual rule must declare its domain and evidence before becoming an automatic global transformation.
