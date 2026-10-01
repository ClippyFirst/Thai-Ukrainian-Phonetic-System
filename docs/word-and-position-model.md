# Word, syllable and positional model

The system distinguishes grapheme correspondence, syllable correspondence, and word/context correspondence.

Thai orthography does not reliably encode word and syllable boundaries with spaces. The reference implementation therefore does not silently invent boundaries. Use analyze_word_syllables(["กา", "นา", "มา"]) for an explicitly segmented word.

Positions are structured metadata: initial, medial, final, or standalone for a one-syllable word.

Position does not automatically change IPA. A position-dependent change is introduced only by an explicit orthographic, phonological, morphological, or lexical rule supported by evidence.

Each syllable retains normalized form, grapheme order, onset, coda, vowel, live/dead status, tone, IPA, Ukrainian candidate ranking, rules, warnings, and sources. The word layer adds syllable index, total count, position, segmentation status, and word-level IPA.

Automatic segmentation and lexical G2P remain a separate corpus/lexicon validation milestone; segmentation errors must not be hidden inside phonological correspondence rules.
