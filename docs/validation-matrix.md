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
| lexical segmentation | infrastructure implemented | explicit lexicon adapter; no bundled lexicon asserted as gold |
| corpus validation | infrastructure implemented | external licensed JSONL; no CI gold corpus claimed |
| malformed syllable surface rejection | implemented | repeated tone/vowel signs, concatenated material and unsupported-symbol probes |
| calibrated probability | not claimed | calibration dataset still required |


| tone-bearing class in consonant clusters | implemented for declared cluster rule | separate `tone_class` field + adversarial cluster fixture |
| parser/source vowel-ID consistency | implemented | registry regression |


| machine-readable tone rules | implemented | `data/thai/tone_rules.csv` + data-driven engine |
| special orthography registry | implemented conservatively | `รร`, `ฤ/ฦ`, `์`, `ทร`, `อ นำ` become explicit analysis-dependent cases |
| source → parser → derived consistency | implemented | generated source-final manifest + CI diff check |
| Ukrainian orthographic target | implemented as project candidate layer | deterministic candidate renderer; explicitly not an official standard |


Current readiness status — 2026-10-24

- Current main HEAD at this checkpoint: `822797042dd3f6980202c2f92e491f2a53df80b0`; current-main CI [40096100740](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40096100740) passed generated-data checks, master-table generation, Python tests, Node IPA-to-UA tests, and Python/browser parity. Master-table assertions passed for 351,780 rows and 41 vowel records.
- The final-velar-stop regression for ตรอก is present and passing; its test asserts onset ต ร, coda ก, and Ukrainian final к.
- Optional external G2P smoke is reproducible: 40093730177, 72 raw outputs, zero runtime errors, zero independent gold rows. This is not an accuracy benchmark.
- Engineering validation: DONE_VERIFIED. Empirical accuracy, lexical coverage, calibrated confidence, and broad connected-speech claims: TODO/BLOCKED until independently adjudicated data and explicit scope criteria exist.
- Latest observed Pages deploy passed at 40091525305 for code-equivalent site sources; an exact current-HEAD redeploy has not been observed.


## Additional fail-closed validation — 2026-10-24

- Finding: both Python and browser text pipelines labeled unknown multi-grapheme words as `unresolved` while still returning a whole-word syllable analysis. This could expose IPA/Ukrainian output despite missing lexical segmentation.
- Correction and regression tests were merged through PR [#27](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/27) at `975bd0504ad05392e277f00d85b746d21c5fe729`. Unknown multi-grapheme tokens now return no syllable analyses and explicitly withhold IPA/Ukrainian output; curated lexicon entries remain unchanged.
- Current main verification is running: CI [40113793581](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40113793581), web static validation [40113793624](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40113793624), and Pages deployment [40113793688](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40113793688). Do not mark the merged correction fully verified until these complete.
- Follow-up PR [#28](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/28) clarifies that the current text endpoint does not implement automatic word segmentation; unresolved words must be added to a reviewed lexicon or analyzed individually through the syllable API.
- Linguistic scope unchanged: independent gold IPA corpus remains absent, so empirical accuracy is not measured.
