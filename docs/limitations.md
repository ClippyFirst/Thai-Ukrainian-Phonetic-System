# Limitations

The repository is a research-grade foundation, but the following are deliberately not claimed complete:

- exhaustive Thai lexical segmentation;
- exhaustive implicit-vowel grammar;
- complete ห นำ and class-changing grammar;
- complete รร analysis;
- all silent-letter and thanthakhat constructions;
- connected-speech phonetics;
- corpus frequency and lexical coverage;
- calibrated probabilities;
- a validated single Ukrainian spelling for every Thai input.

The parser now explicitly rejects arbitrary adjacent consonants as complex onsets when the sequence is not structurally licensed. This reduces false-positive analyses but means that whitespace-free lexical/morphological inputs may remain unresolved until segmentation evidence is supplied.

The deterministic feature ranker does not produce probabilities. A low distance means only lower cost under the declared feature metric.

A future corpus must be used to estimate weights and ambiguity empirically.

## Super-soft mode: coverage is not accuracy

The optional browser mode super-soft prioritizes complete copyable output. For Thai spans lacking a reviewed lexical reading, it constructs a provisional IPA candidate from the available orthographic structure and passes that candidate through the existing IPA → Ukrainian adapter. The output labels this path as an unverified orthographic fallback.

This mode is not a linguistic accuracy improvement by itself. Word boundaries, silent letters, vowels, tones, proper-name readings and even the approximate sound can be wrong. Use strict/soft modes when withholding uncertain readings is preferable. The fallback must never bypass the IPA adapter or be reported as source-attested evidence.
