# Architecture

Thai orthography → graphemic analysis → syllable structure → phonology → tone → contextual phonology → IPA → Ukrainian feature-space candidates → Ukrainian phonological target → Ukrainian orthography.

The layers are intentionally non-collapsible.

1. Orthography: Unicode-normalised Thai code points.
2. Graphemics: consonant classes, vowel signs, tone marks and special constructions.
3. Syllable structure: onset, nucleus, coda and live/dead status.
4. Phonology: segmental composition and lexical tone.
5. Surface phonetics: only evidenced rules are allowed.
6. Ukrainian target: the external Ukrainian-Phonetic-Inventory feature model.
7. Orthographic rendering: a downstream optimisation problem, not a character substitution table.

Thai orthographic order is not phonological order. Preposed and surrounding vowel signs are therefore parsed as one nucleus.

The candidate ranker is a deterministic feature-distance model. Its weights are parameters, not probabilities.
