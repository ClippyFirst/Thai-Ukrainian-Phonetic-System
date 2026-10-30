# Methodology

Thai orthography -> graphemic roles -> syllable constituents -> phonology -> tone -> surface phonetics/IPA -> Ukrainian feature-space target -> Ukrainian phonology -> Ukrainian orthography.

Orthographic evidence and phonological inference are kept separate. Tone marks are not treated as tones. Consonant class is not treated as a phonetic feature.

The correspondence layer is a ranking model. A score is a distance, not a probability, until an empirical calibration corpus exists.

The Thai word-segmentation problem is explicitly separated from Unicode parsing. A whitespace-free Thai sentence may require lexical and morphological evidence that a pure character parser cannot supply.
