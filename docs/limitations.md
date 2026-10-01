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

The deterministic feature ranker does not produce probabilities. A low distance means only lower cost under the declared feature metric.

A future corpus must be used to estimate weights and ambiguity empirically.
