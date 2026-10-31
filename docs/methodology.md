# Methodology

Thai orthography -> graphemic roles -> syllable constituents -> phonology -> tone -> surface phonetics/IPA -> Ukrainian feature-space target -> Ukrainian phonology -> Ukrainian orthography.

Orthographic evidence and phonological inference are kept separate. Tone marks are not treated as tones. Consonant class is not treated as a phonetic feature.

The correspondence layer is a ranking model. A score is a distance, not a probability, until an empirical calibration corpus exists.

The Thai word-segmentation problem is explicitly separated from Unicode parsing. A whitespace-free Thai sentence may require lexical and morphological evidence that a pure character parser cannot supply.


## Two Ukrainian output methods

The primary phonetic method remains IPA-first:

Thai orthography → structural/lexical analysis → Thai phonology → typed phonemic/surface IPA → Ukrainian adaptation → practical Ukrainian orthography.

The browser additionally exposes an optional RTGS-based method:

Thai orthography → the pinned PyThaiNLP 5.4.0 RTGS port → RTGS consonant/rime sequence → Ukrainian practical rendering.

The second method does not consume IPA and is intentionally not described as phonetic adaptation. Its digraph and rime correspondences are specified in [the complete comparison matrices](ukrainian-correspondence-matrices.md). This allows a methodological comparison with the Thai–Russian practical-transcription approach without treating Russian spellings as Ukrainian norms.

RTGS omits information such as tone and some vowel-length contrasts. A successful RTGS rendering is therefore not evidence that the IPA-first pronunciation is correct. Unsupported RTGS spans remain unresolved. Independent Thai expert and Ukrainian-native review are still required for linguistic validation.
