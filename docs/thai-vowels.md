# Thai vowels

The dataset separates **phonological vowel qualities** from **orthographic rime/parsing records**.

The Standard Thai reference description used by the project treats nine vowel qualities as having contrastive short/long counterparts, with /ia/, /ɯa/ and /ua/ as the principal diphthongal series. The project also models orthographic glide/rime constructions separately because the Thai writing system distributes vowel and glide information across multiple graphemes.

The machine-readable registry currently contains **41 rime records**:
- 24 core short/long vowel records (18 monophthongs + 6 diphthongs);
- 17 contextual, glide-sequence or reduced-rime records used by the orthographic parser.

These 41 records are **not** a claim of 41 phonemic vowel qualities. Registry cardinality and phoneme-inventory cardinality are intentionally separate.

Vowel quantity is retained explicitly because it can affect tone determination in low-class dead syllables. The IPA layer also keeps /j/ and /w/ glide components explicit where the evidence model treats them as part of the rime.
## Orthographic ambiguity requiring lexical evidence

The parser does not assume that every written rime uniquely determines vowel quantity. A particularly important case is the closed **เ-ิ-** spelling: Royal Society evidence documents long **เกิน** /ɤː/ and short **เงิน** /ɤ/ within this spelling family. Therefore the reference implementation exposes an **analysis-dependent:vowel-length** state and retains both candidates when the input supplies no lexical evidence. This is intentional and prevents a syllable-only parser from converting orthographic ambiguity into false IPA or tone output.
