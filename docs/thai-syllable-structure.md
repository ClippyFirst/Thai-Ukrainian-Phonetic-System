# Thai syllable structure

Core representation:

onset + nucleus + optional coda + tone

A common Standard Thai template permits a simple onset or a two-consonant onset cluster followed by a vowel and optional final consonant.

The parser must distinguish orthographic order from phonological order and must not equate a Unicode sequence with a syllable without evidence.

Lexical segmentation is a separate layer from low-level Unicode decomposition.
