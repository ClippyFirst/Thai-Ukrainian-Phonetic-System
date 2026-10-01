# Validation matrix

| Component | State | Validation |
|---|---|---|
| 44 consonant graphemes | implemented | inventory tests |
| 5 lexical tone categories | implemented | tone engine |
| tone mark vs tone | implemented | separate model fields |
| live/dead syllables | implemented | structural fixtures |
| vowel/rime registry | implemented | parser + source registry consistency test |
| implicit vowel flagging | implemented conservatively | negative fixtures |
| onset/coda distinction | implemented | กรา / กาน / carrier-coda negative test |
| feature-ranked Ukrainian candidates | implemented | deterministic adapter |
| broad IPA composition | implemented | pipeline tests |
| connected-speech phonetics | partial | intentionally conservative |
| lexical segmentation | not claimed | requires corpus/lexicon |
| corpus validation | not claimed | requires annotated corpus |
| calibrated probability | not claimed | requires gold data |


| tone-bearing class in consonant clusters | implemented for declared cluster rule | separate `tone_class` field + adversarial cluster fixture |
| parser/source vowel-ID consistency | implemented | registry regression |
