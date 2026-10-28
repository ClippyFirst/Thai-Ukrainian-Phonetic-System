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


## Completeness and ambiguity boundary (2026-10-28)

See [`docs/phonology-ambiguity-coverage.md`](phonology-ambiguity-coverage.md) for the source-backed review matrix. Core tone/segmental rules are implemented, but lexical readings of `ทร`, `รร`, `ฤ/ฤๅ/ฦ/ฦๅ`, silent-letter constructions and connected speech are not exhaustive. Unlisted ambiguous forms must remain analysis-dependent; dictionary-attested readings are not independent IPA gold. Regression tests enforce fail-closed behavior for unlisted special-orthography forms and ensure an exact lexical reading such as `ทราบ` does not become a global rule for `ทร`.
