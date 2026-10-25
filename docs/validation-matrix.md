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


## Current validation status — 2026-10-24

## Evidence-gated completion update — 2026-10-25

| Component | State | Evidence / acceptance boundary |
|---|---|---|
| Wisesight source-annotated word-boundary set | DONE_VERIFIED | 993 rows, CC0-1.0, pinned upstream commit/blob SHA, exact reconstruction check, test-only split; status explicitly `SOURCE_ANNOTATED`, not expert-adjudicated |
| Segmentation scorer source-status handling | DONE_VERIFIED | Scores `ADJUDICATED` and `SOURCE_ANNOTATED` separately; rejects mixed-grade gold sets; whitespace-only boundaries excluded |
| ClippyFirst segmentation baseline | DONE_VERIFIED (baseline only) | CI runs `scripts/run_wisesight_segmentation_diagnostic.py` and uploads JSON; baseline is expected to expose the current no-auto-segmentation limitation, not prove a production score |
| Source-attested IPA/tones/length contrasts | DONE_VERIFIED (source-attested only) | Six pinned Wiktionary entries; `SOURCE_ATTESTED_NOT_GOLD`; includes short /ɤ/ in เงิน vs long /ɤː/ in เดิน |
| Runtime lexical coverage | PARTIAL | Five source-backed challenge lexicon entries added; diagnostic must report new counts; not representative coverage |
| Lexical IPA override for เงิน | TODO | Must preserve /ŋɤn˧/ short-vowel reading through typed IPA and UA adaptation, with Python/browser parity; current graphemic lexicon cannot safely encode this |
| Independent expert/acoustic IPA gold | BLOCKED | CCOST license/annotation manual and local scope must be reviewed, then an independent Thai phonetician must adjudicate a pinned sample with disagreement log and speaker-aware split |
| Context-dependent `รร`, `ฤ/ฤๅ`, `ฦ/ฦๅ`, `ทร`, silent letters | PARTIAL | Keep lexical/context-dependent abstention until source-located readings and independent review exist |
| Connected speech and Ukrainian target preference | BLOCKED | Requires acoustic evidence and a separately adjudicated Ukrainian target preference set |

The Wisesight rows establish a usable source-annotated segmentation benchmark; they do **not** satisfy the independent-expert criterion. The IPA dataset remains source-attested-only, with no accuracy claim.


- The fail-closed unknown-word correction merged in PR #27 as `975bd0504ad05392e277f00d85b746d21c5fe729`. Unknown multi-grapheme words no longer expose whole-word syllable/IPA/Ukrainian output without lexical segmentation; curated lexicon entries are unchanged.
- Engineering validation is DONE_VERIFIED on the current code path: Python tests, Python/browser parity, build, master-artifact validation and deployment have passed on recent main-equivalent runs. This is separate from phonological accuracy.
- Latest external smoke evidence is being reconciled in PR #41: 36 inputs, 72 outputs, 0 runtime errors; `thaiphon` and FastThaiG2P agree exactly on 13/36 inputs, and on 14/36 after a tone-only diagnostic. The diagnostic is not an accuracy metric; independent gold count remains zero.
- Empirical accuracy, lexical coverage, calibrated confidence and broad connected-speech claims remain TODO/BLOCKED until a representative, independently adjudicated held-out corpus and explicit scope criteria exist.


## Current validation status — 2026-10-25 (PR #71)

- **DONE_VERIFIED — software gates:** exact-head CI test job [40229701920](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40229701920) passed generated-data drift checks, master-table generation, 143 Python tests, runtime diagnostic guards, IPA→Ukrainian adapter tests, Python/browser parity (27 fixtures) and UI contract checks.
- **DONE_VERIFIED — evaluator integrity:** only prediction rows with `status=ok` score; non-success rows abstain; boundary F1 handles zero predicted boundaries correctly; empty runtime challenge inputs fail closed.
- **PARTIAL — challenge runtime:** 23/36 forms resolve via the curated lexicon, 13 remain unresolved; 21/36 complete outputs and 15/36 abstentions/incomplete outputs. Hand-picked runtime counts are not accuracy or general coverage.
- **PARTIAL — special orthography:** source-backed lexical cases and conservative analysis-dependent statuses exist. PR #68 is a separate green but currently non-mergeable branch; no automatic merge was performed.
- **BLOCKED — empirical validation:** zero independently adjudicated Thai IPA/word-boundary gold rows; CCOST requires license-compliant local handling and independent adjudication; a segmentation holdout still needs exact version, license, annotation convention, split and hash.
- **BLOCKED — broader claims:** connected-speech phonetics, calibrated probability and Ukrainian orthographic preference require separate evidence sets.
- **Environment limitation:** local clone/test commands were not executed because GitHub DNS resolution failed; remote CI is the test evidence.


## Exact-head CI outcome — 2026-10-25

- Code-bearing acceptance commit: `818a378d37b248d74628243b9a8d62fb82029815`.
- GitHub Actions run [40233825012](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40233825012) passed both `test` and `master-artifact` jobs.
- Python suite: 150 tests passed. Generated-data drift check passed. Master generator passed; artifact guard confirmed 351,780 rows and 41 vowel/rime records. Challenge diagnostic ran all 36 forms. Node IPA→UA, Python/browser parity and UI contract checks passed. Wisesight diagnostic passed and artifact `wisesight1000-segmentation-baseline` (artifact ID `12614106636`) uploaded.
- Wisesight source-annotated baseline: 993/993 predictions emitted; boundary precision 0.6383, recall 0.0919, F1 0.1606; exact sequence rate 0.0312. Evidence status is `SOURCE_ANNOTATED`, not expert-adjudicated.
- Challenge runtime diagnostic: lexicon resolution 28/36; complete output 25/36; 11 abstentions/incomplete outputs. This is not an accuracy estimate.

The latest code-bearing commit is engineering-verified by the above run. A documentation-only reconciliation commit follows this matrix update; its own CI must be checked before claiming the final branch head is green.
