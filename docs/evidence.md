# Evidence registry

## Core sources

- SRC-ORST — Royal Institute of Thailand official linguistic standards and publications.
- SRC-JIPA-1993 — Tingsabadh & Abramson, Thai, Journal of the International Phonetic Association, 1993, DOI 10.1017/S0025100300004746.
- SRC-CORPUS — Munthuli et al., corpus-based study of Thai phoneme distribution.
- SRC-NRCT — Thai phonology and orthography research thesis.
- SRC-CCOST — Pittayaporn et al., Chulalongkorn Corpus of Spoken Thai, LREC 2026.
- SRC-G2P-WIKI — PyThaiNLP Thai Grapheme to Phoneme Wiktionary Corpus.

## Orthographic ambiguity evidence

- **SRC-ORST-VOWEL-LENGTH-2021** — International Journal of the Royal Society of Thailand (2021), *The Thai Writing System: Reasons behind Its System*, Table 14. The source explicitly documents shared written forms with final consonants and contrasts **เกิน** /ɤː/ with **เงิน** /ɤ/, demonstrating that the closed **เ-ิ-** spelling cannot by itself determine vowel length. This is treated as an orthographic/lexical ambiguity, not as a parser failure.

## Coda-position evidence

Standard Thai permits a restricted final inventory; consonant graphemes such as ฉ, ผ, ฝ, ห, อ and ฮ are not licensed as ordinary codas. The parser therefore treats an otherwise structurally detectable final occurrence of one of these graphemes as `invalid:coda-not-licensed` rather than silently dropping it. This is an orthographic/phonotactic validation rule, not a claim about lexical attestation. The JIPA Standard Thai description and independent descriptions of Thai final consonants support the restricted-coda analysis.

## Evidence policy

A source can support a claim, but implementation status is tracked separately. The project distinguishes core evidence, analysis-dependent rules, and unresolved cases.

For publication, each important rule should eventually have a claim-level record containing source, page or section, exact claim, competing analysis, implementation consequence and confidence.

The official Royal Institute material is particularly important for Thai orthographic phenomena such as leading consonants and consonant clusters. CCOST is reserved for empirical phonetic validation rather than for defining orthographic rules.


## Claim-level anchors used in the current audit

- **SRC-JIPA-1993:** Tingsabadh & Abramson, *Thai*, Journal of the International Phonetic Association 23(1), pp. 24–28. The description establishes the Standard Thai reference scope, nine vowel qualities with contrastive length, /w/ and /j/ as final components in phonetic diphthongs, five tones, and the restricted final-consonant inventory. DOI: https://doi.org/10.1017/S0025100300004746
- **SRC-ORST-TH:** Royal Institute of Thailand publications are used for orthographic phenomena such as leading consonants and the interaction of written structure with pronunciation. These are orthographic evidence, not a substitute for corpus-based phonetic validation.

The implementation deliberately uses a broader machine-readable rime registry than the nine-vowel-quality phonological inventory because several orthographic rimes and glide sequences are represented as separate structural parsing records. **Registry cardinality is not phoneme-inventory cardinality.**


## False-cluster evidence

Standard Thai cluster descriptions distinguish true clusters from false clusters. In particular, **จร, สร, ศร, ซร** can contain a written ร that is not pronounced, while **ทร** has lexical readings that may diverge from a compositional /thr/ analysis. Examples documented in reference descriptions include **จริง** /tɕiŋ/, **สร้าง** /saːŋ/, **เศร้า** /saw/ and **ไซร้** /saj/. The implementation therefore treats these constructions as analysis-dependent until lexical evidence resolves the reading. Sources: SRC-ORST; the independent cluster reference used in the audit.
