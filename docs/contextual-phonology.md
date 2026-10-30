# Thai contextual phonology and IPA audit layer

## Purpose

The correspondence system separates phonological identity from surface realization. A Thai grapheme can therefore have one phonological value in the inventory and a different surface realization when it occupies a different syllable-internal position.

## Position hierarchy

1. Grapheme role: consonant, vowel sign, tone mark, special orthography.
2. Syllable-internal position: onset, nucleus, coda.
3. Word-syllable position: standalone, initial, medial, final.
4. Sentence/prosodic context: a separate evidence layer; never inferred from word position alone.

## Consonants

The core implementation distinguishes onset IPA from coda IPA. Thai has a restricted final consonant inventory. In particular, final /p t k/ are not audibly released in the conservative surface representation, so the implementation renders them as [p̚ t̚ k̚]. Orthographic consonants with voiced onset values can therefore have a voiceless final phonological value: for example ด is /d/ in onset position but has coda_ipa=t in the project inventory and surface [t̚].

## Vowels

The project keeps vowel phonemic IPA and surface IPA separate, but currently does not force a deterministic vowel-quality alternation solely from open versus closed syllable context. This is intentional. Thai vowel duration and spectral properties have documented phonetic variation, and vowel quantity, tone and glottal-stop behavior can vary with speech style. Such variation should enter the machine model only as an explicit rule with evidence and a declared scope.

## Ukrainian layer

The Ukrainian candidate layer consumes IPA, not Thai grapheme identity. Thus the audit path is:

Thai grapheme → Thai orthographic analysis → phonological segment → phonemic IPA → surface IPA → Ukrainian phonetic/phonological candidate → Ukrainian orthographic candidate.

Tone remains a separate suprasegmental field.

## Evidence boundary

This layer is a conservative deterministic surface model, not a claim to reproduce every connected-speech token. Acoustic allophony, stress-dependent reduction, sandhi, speech-rate effects and lexical exceptions require separate evidence-backed rules.

Primary references used for this boundary include Tingsabadh & Abramson, Illustration of the IPA: Thai (1993), and Iwasaki & Ingkaphirom, A Reference Grammar of Thai.