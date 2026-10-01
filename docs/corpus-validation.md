# Corpus validation plan

## Primary phonetic gold resource

The Chulalongkorn Corpus of Spoken Thai (CCOST) is suitable for future validation because it is a phonetically annotated Standard Thai corpus with orthographic, syllable and phone-level annotations and toneme labels.

## Secondary G2P resource

The Thai Grapheme to Phoneme Wiktionary Corpus provides Thai forms paired with IPA and is useful for broad G2P regression testing.

## Evaluation

For each gold record:

- parse Thai orthography;
- compare syllable boundaries;
- compare onset and coda;
- compare vowel identity and length;
- compare lexical tone;
- compare broad IPA;
- generate Ukrainian candidate set;
- compare candidate recall against expert-adjudicated target.

Report exact-match, segment accuracy, tone accuracy, syllable-boundary accuracy, top-k candidate recall and ambiguity rate.

Do not mix corpus-level lexical frequency with phonetic accuracy. They answer different questions.
