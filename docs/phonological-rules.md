# Phonological rules

Implemented core rules:

1. final consonant neutralization metadata;
2. live/dead classification;
3. explicit licensing of standard complex onsets;
4. separation of written onset class from tone-bearing consonant class;
5. tone determination from tone-bearing class, syllable type, vowel quantity and tone mark;
6. withholding phonology/tone when syllable segmentation is unresolved.

Complex onset parsing is deliberately conservative. The current core recognizes standard two-consonant onset structures with second elements /r, l, w/ and the implemented leading-consonant pathway for ห + low-single onsets. Arbitrary adjacent consonants are not promoted to a cluster merely because they occur before a vowel. This is necessary because Thai orthography can contain consonant sequences that represent multiple syllables or non-conforming constructions.

For a nonconforming sequence such as แสดง supplied as one syllable, the system returns an unresolved segmentation status instead of inventing /sd-/ and a tone from the wrong consonant.

A contextual rule must declare its domain and evidence before becoming an automatic global transformation.

The remaining special-orthography domains (รร, broader ห นำ, silent letters, lexical exceptions and connected speech) remain evidence-gated.
