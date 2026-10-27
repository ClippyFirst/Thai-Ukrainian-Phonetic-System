# Validation matrix

| Component | State | Validation |
|---|---|---|
| Pasted Wikipedia/Markdown/HTML input cleanup | DONE_VERIFIED — code fix and published-page contract passed | PR #91 fixed nested IPA-link cleanup; PR #93 corrected the live contract to check `softSyllabify` in `engine.js`. Post-merge Pages run [40509900075](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40509900075) succeeded, including the published whole-text UI contract; static validation [40508000658](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40508000658) and main CI [40509900074](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40509900074) passed.
| External G2P license/provenance gate | PARTIAL — TLTK license scope is contradictory in current repository artifacts; FastThaiG2P bundled dictionary/fallback provenance not cleared | Research-register correction committed on branch `research/correct-tltk-license-audit-20261027`; TLTK README.rst/setup.py say BSD-3-Clause while root LICENSE contains LGPL v3 and LICENSE.txt contains BSD-style terms. No external code/data imported. Acceptance: authoritative clarification of applicable TLTK license by file/version, and resource-level license/provenance audit for any selected model or dictionary. |
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
| lexical segmentation | PARTIAL | pinned CC0 dictionary max-match and separate 60,963-entry lexicon; evaluated on held-out Wisesight but current baseline is weak; no claim of production-quality segmentation |
| TUD Viterbi word-segmentation model | PARTIAL — reproducible research model exists but is not used by the production browser engine | Pinned UD Thai TUD source commit `67413969add552b7030184f16f24fa9f630913bc`, CC BY-SA 4.0; 5,319-word unigram model. Held-out TUD test boundary F1 `0.872932`; Wisesight source-annotated test-only F1 `0.792101`, precision `0.6592`, recall `0.9921`, 0 expert-adjudicated rows. Model artifact `thai-tud-word-segmentation-model-and-report` (run `40503671201`, artifact `12734023167`). Candidate only for opt-in provisional segmentation; production integration requires browser/Python parity, license attribution/share-alike handling, and representative expert-reviewed error analysis.
| Source-attested proper-name reading `ยูเครน` | DONE_VERIFIED — PR #94 merged; post-merge CI and Pages deployment passed | Pinned en.wiktionary revision 88025965 attests `/juː˧.kʰreːn˧/` and two syllables `ยู|เครน`; the implementation routes both syllables through the existing typed IPA → Ukrainian adapter. Exact-head CI [40510490288](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40510490288), post-merge main CI [40511892392](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40511892392), and Pages deployment [40511892093](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40511892093) passed. This is source-attested lexical evidence, not independent expert/acoustic gold and not evidence of general G2P accuracy. |
| Article-style G2P challenge probes | PARTIAL — merged in PR #95; CI and optional external smoke passed; evidence remains unadjudicated | Six target-relevant probes cover `ยูเครน`, country-name compounds, continuous Thai prose and Eastern Europe. Branch CI [40510716596](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40510716596), optional external smoke [40510554606](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40510554606), and post-merge main CI [40511892392](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40511892392) passed. Run [40507249579](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40507249579) preserves 126 raw outputs across three engines. No independent gold labels exist; this is a diagnostic set, not an accuracy benchmark. |
| Browser segmentation latency diagnostic | DONE_VERIFIED as a reproducible non-gating runtime diagnostic; not an accuracy benchmark | Post-PR #85 CI artifact [12739570652](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40513578523) on Node v22.23.3, 5 warmups / 30 samples: target 100 → actual 113 code points, median/p95 2.102/3.294 ms; target 250 → actual 261, 5.636/8.600 ms; target 500 → actual 500, 7.386/11.115 ms. Inputs append complete Thai lexical units rather than slicing arbitrary code points. These measurements are runner/JIT-dependent and say nothing about segmentation correctness or phonetic accuracy. |
| corpus validation | infrastructure implemented | external licensed JSONL; no CI gold corpus claimed |
| malformed syllable surface rejection | implemented | repeated tone/vowel signs, concatenated material and unsupported-symbol probes |
| calibrated probability | not claimed | calibration dataset still required |
| strict/soft browser modes | DONE_VERIFIED — published UI contract passed; empirical phonological quality remains PARTIAL | Main Pages run [40509900075](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40509900075) confirms the deployed whole-text UI, selector and served engine markers. This verifies deployment wiring, not pronunciation accuracy; soft mode remains provisional and strict mode abstains on unsupported spans.


| tone-bearing class in consonant clusters | implemented for declared cluster rule | separate `tone_class` field + adversarial cluster fixture |
| parser/source vowel-ID consistency | implemented | registry regression |


| machine-readable tone rules | implemented | `data/thai/tone_rules.csv` + data-driven engine |
| special orthography registry | implemented conservatively | `รร`, `ฤ/ฦ`, `์`, `ทร`, `อ นำ` become explicit analysis-dependent cases |
| source → parser → derived consistency | implemented | generated source-final manifest + CI diff check |
| Ukrainian orthographic target | implemented as project candidate layer | deterministic candidate renderer; explicitly not an official standard |


Current readiness status — 2026-10-24

- Current main HEAD at this checkpoint: `822797042dd3f6980202c2f92e491f2a53df80b0`; current-main CI [40096100740](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40096100740) passed generated-data checks, master-table generation, Python tests, Node IPA-to-UA tests, and Python/browser parity. Master-table assertions passed for 351,780 rows and 41 vowel records.
- The final-velar-stop regression for ตรอก is present and passing; its test asserts onset ต ร, coda ก, and Ukrainian final к.
- Optional external G2P smoke: run [40507249579](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40507249579), 42 inputs / 126 raw outputs, zero independently gold-labeled rows. thaiphon 0.7.0 and FastThaiG2P 0.1.0 emitted output for all 42; pinned Goruut returned no words on 16/42. Six article-style cases are preserved in `data/benchmark/runs/article-style-external-g2p-2026-10-27.json`. This is a raw-output diagnostic, not an accuracy benchmark.
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
| Typed source-attested lexical IPA overrides (เงิน, เดิน) | IMPLEMENTED; exact-head CI pending | Pinned Thai Wiktionary revisions; typed IPA→UA adapter path; grapheme-only ambiguity remains separate; source agreement from an injected override is excluded from independent-comparison metrics |
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
- **PARTIAL — challenge runtime:** challenge set expanded from 36 to 42 with six article-style Thai probes. The external run is reproducible, but all gold IPA/boundary fields remain null; no pronunciation accuracy or lexical-coverage claim is supported.
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


## Final documentation-head check — 2026-10-25

- Documentation head `b3eaddde55de0474e47abe01ece7692467f1a229` passed both CI jobs in [run 40234324067](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40234324067).
- This confirms the source-annotated benchmark, 150 Python tests, generated-data drift check, Python/browser parity, UI contract, 993-row baseline artifact and master-table artifact all remained green after the audit/matrix/handoff updates.
- A final wording-only audit JSON reconciliation follows this checkpoint; no code/data changes are included. Its own CI is pending and will be checked before ending this run.


## Text-evidence continuation — 2026-10-25

| Workstream | Status | Evidence / acceptance |
|---|---|---|
| Text-attested IPA registry | PARTIAL | `data/benchmark/source-attested-ipa.tsv` pins six Thai Wiktionary revisions; status remains `SOURCE_ATTESTED_NOT_GOLD`. These records are dictionary evidence, not independent or acoustic gold. |
| Runtime lexical IPA override | PARTIAL | `data/thai/lexical_ipa_overrides.tsv` enables the narrowly scoped source-attested short-vowel reading of `เงิน`; provenance and tone/length metadata are preserved through `PhoneticResult` and the IPA→Ukrainian adapter. Extend only with individually reviewed records and regression tests. |
| Word-boundary corpus | PARTIAL | Pinned Wisesight 993-row CC0 source-annotated snapshot remains test-only. No use for training or dictionary construction; it is not independently re-adjudicated. |
| Automatic word segmentation | TODO | No production segmenter is claimed. A valid implementation needs training data distinct from the pinned test snapshot and an untouched, source-annotated evaluation set. |
| Orthographic exceptions | PARTIAL | `รร`, `ฤ/ฤๅ`, `ฦ/ฦๅ`, `ทร`, and silent letters remain lexical/context dependent; no universal rule inferred from a few examples. |
| Connected speech / Ukrainian target preferences | BLOCKED for empirical claims | Textual transcription analysis and consistency checks are feasible; acoustic validation and independent Ukrainian target-form adjudication are not established by the current text-only evidence. |

Verified code/data head: [CI 40238202167](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40238202167) and [Web static validation 40238202181](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40238202181) passed on `43687b2753379b1d617b1c925f87358f8aad13bd`. The final documentation head `6a153e26e17c4929fdc166b3dbeb73444668f2b1` also passed [CI 40238672074](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40238672074) and [Web static validation 40238671983](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40238671983). This is engineering verification, not a phonetic-accuracy claim.


## Latest text-only implementation checkpoint — 2026-10-25

| Task | Status | Evidence / acceptance |
|---|---|---|
| Typed lexical IPA override for `เงิน` | PARTIAL | Source-pinned override is active in Python and browser, runs through the IPA→Ukrainian adapter, and carries `SOURCE_ATTESTED_NOT_GOLD` provenance. Exact-head browser CI and Web static validation passed on the code head; the final documentation-only head also passed. |
| Text pipeline routing and parity | PARTIAL | Python text pipeline recognizes the override; browser engine and text UI have matching fixture assertions. Exact-head CI passed after the fixture expectation/order correction. |
| Source-attested IPA discrepancy diagnostic | DONE_VERIFIED on prior code/data checkpoint | Six source rows; 5 complete outputs, 4 segmental agreements, 5 tone-category agreements, 1 withheld; `บรรจุ` final-`/ʔ/` difference is retained for review, not auto-corrected. |
| Corpus license/access registry | DONE_VERIFIED on prior code/data checkpoint | Wisesight 993-row source-annotated test-only snapshot; LST20 and VISTEC candidate gates; CCOST CC BY-NC-SA 4.0 and 6.2 GB TextGrid archive recorded. |
| Automatic word segmentation | TODO | No production segmenter or distinct license-cleared training corpus. Wisesight remains test-only. |
| Independent IPA/tone/length gold and Ukrainian target gold | BLOCKED | Requires independent adjudication and, for acoustic claims, access to the matching audio. |

## Follow-up implementation batch — 2026-10-26


| TUD statistical segmentation experiment | IMPLEMENTED; exact-head CI pending | Pinned UD Thai TUD commit 67413969add552b7030184f16f24fa9f630913bc; train-only token counts, dev-only penalty selection, separate TUD test and Wisesight test-only report; CC BY-SA 4.0 obligations recorded |
| Independent IPA/acoustic gold | BLOCKED | Requires independent Thai phonetician adjudication, agreed broad-vs-surface transcription protocol, and authorized CCOST recording/TextGrid access |
| Final glottal stop in บรรจุ | PARTIAL / EVIDENCE-LIMITED | Dictionary IPA and engine disagree; no global phonological rule is added. Need agreement on transcription level, stress/context, and independent adjudication |
| Ukrainian target-form preferences | BLOCKED | Existing adapter and generated candidates establish reproducibility only; require independently adjudicated Ukrainian candidate choices and written criteria |


## Continuation status — 2026-10-26

| Component | State | Evidence / next acceptance criterion |
|---|---|---|
| Dictionary max-match segmentation | PARTIAL | Opt-in baseline and pinned dictionary exist; Wisesight source-annotated metrics are diagnostic only. Keep distinct from adjudicated gold. |
| TUD unigram-Viterbi research segmenter | PARTIAL — research metrics measured | Exact-head CI passed: held-out TUD test boundary F1 0.872932 (375 groups), exact-group rate 0.432; Wisesight test-only F1 0.792101 (2,848 filtered groups). Not independent expert gold, not full-text metrics, not production default; preserve CC BY-SA 4.0. |
| `เดิน` lexical IPA | PARTIAL | Typed source-pinned override `/dɤːn˧/` is separate from parser-only vowel-length ambiguity and routed through IPA→Ukrainian adapter; regression expectations fixed, exact-head CI pending. Not independent gold. |
| `บรรจุ` final `/ʔ/` | BLOCKED | Source/transcription-level discrepancy remains unresolved; requires qualified Thai phonology/phonetics review with exact transcription conventions, not a global rule patch. |
| Independent IPA/acoustic gold | BLOCKED | No independently adjudicated IPA/audio labels currently available. CCOST is a candidate only; access, annotation, and NC-SA conditions must be satisfied before a gold claim. |
| Independent Ukrainian target forms | BLOCKED | Template/protocol exists; independent Ukrainian-language review and source-scoped decisions are still needed. |
| Exact-head CI for code/data head `4c3d01d9b726b410c98048878441082d8d5c8299` | DONE_VERIFIED | CI run `40296520186` and Web static validation run `40296520175` passed; 176 Python tests, Node IPA→UA/parity/UI, generated-artifact checks, diagnostics, TUD training and artifact uploads passed. Recheck final documentation-only head separately. |


## Verified checkpoint — 2026-10-26

- Exact code/data head: `4c3d01d9b726b410c98048878441082d8d5c8299`; CI [40296520186](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40296520186) PASS; Web static validation [40296520175](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40296520175) PASS.
- Candidate TSV regeneration check now passes byte-for-byte; malformed quoting of JSON fields was the prior failure and is fixed.
- Source-attested IPA diagnostic: 6 records, 2 circular source overrides excluded, 4 comparable records, 3 segmental agreements, 4 tone agreements; `SOURCE_ATTESTED_NOT_GOLD`, no accuracy claim.
- Wisesight-1000: 993 source-annotated rows, 0 adjudicated. Text tokenizer F1 0.160604; dictionary max-match F1 0.839471; exact sequence rates 0.031219 and 0.193353 respectively. Diagnostic only, not expert gold.
- TUD research segmenter: dev F1 0.889023; held-out TUD test F1 0.872932 (375 groups); Wisesight test-only F1 0.792101 (2,848 filtered groups). TUD labels inherit source tokenization; no production integration decision or independent accuracy claim.
- Readiness remains **research prototype / not release-ready**. Independent phonetic/acoustic gold, Ukrainian target-form adjudication, and context-specific resolution of `บรรจุ` remain evidence-limited.


## Final continuation review — 2026-10-26

| Workstream | State | Verified result / next acceptance |
|---|---|---|
| Final documentation HEAD | DONE_VERIFIED | CI [40297155713](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40297155713) passed test + master-artifact jobs; Web static validation [40297155831](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40297155831) passed on `cb8832ca99e4ccce53b6fb2b6988b5945acaad71`. |
| TUD unigram-Viterbi segmenter quality review | PARTIAL — production integration declined for now | Held-out TUD: boundary P/R/F1 0.7886/0.9775/0.8729; exact-group rate 0.432. Wisesight test-only: P/R/F1 0.6592/0.9921/0.7921; exact-group rate 0.3852. F1 falls by 0.080831 cross-domain; recall-heavy profile and low exact sequence rates do not justify production-default integration. These are filtered groups, not full-text scores or independent expert gold. Next: manual error analysis, deployment thresholds, and independent untouched-domain review. |
| Independent IPA/acoustic gold | BLOCKED | Needs qualified independent Thai phonetician, agreed transcription-level protocol, and authorized audio/TextGrid access; acceptance requires independent labels and a disagreement log. |
| Ukrainian target forms | BLOCKED | Needs independent Ukrainian-native reviewers, blinded criteria-based judgments, and a disagreement log. |
| `บรรจุ` final `/ʔ/` | PARTIAL / EVIDENCE-LIMITED | Keep discrepancy open until context/transcription-level expert adjudication; do not add a global rule. |
| Release readiness | NOT READY | Engineering checks pass, but empirical pronunciation/target-form gold and production segmentation quality are not established. |


## Special-letter source contract — 2026-10-26

- The official OBEC/IPST guide registered as `SRC-OBEC-SPECIAL-VOWELS-2022` (p. 5 for special vowel letters; printed p. 275 in separate source `SRC-OBEC-O-NAM-2022` for อ นำ ย) supports classifying `ฤ`, `ฤๅ`, `ฦ`, and `ฦๅ` as syllabic/lexical constructions and documents the lexical `อ นำ ย` family `อย่า`, `อยู่`, `อย่าง`, `อยาก`.
- The parser deliberately continues to return `analysis-dependent:special-orthography` with no IPA or Ukrainian output for isolated special vowel letters. The source is a scope constraint, not a universal word-reading or pronunciation gold set.
- Python/browser fail-closed regressions passed in exact-head CI [40315032771](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40315032771); Web static validation [40315032788](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40315032788) passed. This verifies uncertainty handling and source-registry integrity, not universal IPA readings or pronunciation gold.


## Mandatory pipeline architecture gate — 2026-10-26

| Gate | Required contract | Status |
|---|---|---|
| Thai → IPA → Ukrainian serial flow | Thai structural/phonological analysis produces the typed IPA intermediate; Ukrainian output is generated from that IPA, not via a parallel grapheme-to-Ukrainian path | DONE_VERIFIED for tested paths — typed PhoneticResult is the Python adapter input; exact-head CI 40315032771 passed |
| IPA adapter input contract | Ukrainian adapter consumes typed IPA and documented metadata; it does not independently read Thai graphemes, vowel IDs or coda fields | DONE_VERIFIED — Python IPA mutation test and browser end-to-end adapter test pass; adapter modules do not read Thai graphemes |
| Fail-closed uncertainty | Unsupported/ambiguous Thai analysis cannot yield an unjustified IPA or confident Ukrainian result | DONE_VERIFIED for tested special letters and unsupported/empty/uncertain IPA — no confident Ukrainian output leaks from these cases |
| End-to-end data-flow coverage | Tests establish Thai input → exposed IPA → Ukrainian output and that withholding/changing the IPA intermediate changes/withholds dependent target output | DONE_VERIFIED — end-to-end IPA mutation and fail-closed tests pass in Python and browser |
| Feature preservation | Phonemic/surface distinction, tone, vowel length, syllable/segment boundaries, provenance and uncertainty survive to the IPA boundary | DONE_VERIFIED for tested metadata — tone, vowel length, syllable boundaries, provenance and uncertainty are asserted; broad surface IPA remains separately inspectable |
| Python/browser parity | Both runtimes implement the same boundary and derive Ukrainian output from equivalent IPA results | DONE_VERIFIED — 180 Python tests, 28 parity fixtures and browser/UI checks passed on exact head cb775d6156f62392fa2d0f4bcf8d1aa30d219530; this is not linguistic gold |

**Resolved exact-head regression — 2026-10-26:** The 12 failures in CI [40313439910](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40313439910) came from four special-letter rows missing their `pattern` column in `data/thai/special_orthography.csv`. The resulting positional shift made `analysis_status` contain IPA candidates and prevented the parser from recognizing the special letters. The data rows were repaired in commit `a0bd6f598c5117154db1c78f02ae25b6d6fbf1bc`; tests now assert each row's pattern, status, candidates, and source provenance.

Exact-head CI [40315032771](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40315032771) passed both jobs: 180 Python tests, generated-data drift, 351,780-row master artifact with 41 rime records, Node IPA→Ukrainian, 28 Python/browser parity fixtures, UI contract, challenge/Wisesight/source-attested IPA diagnostics, candidate registry check, TUD research training/evaluation and artifact uploads. Web static validation [40315032788](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40315032788) passed. The IPA-first boundary now has mutation and fail-closed regression tests in both runtimes. These checks verify software behavior only; they do not supply independent Thai IPA gold or Ukrainian target-form adjudication.


## Exact-head verification refresh — 2026-10-26

| Gate | Latest verified evidence | State |
|---|---|---|
| Python and repository CI | [Run 40316202183](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40316202183), documentation checkpoint `4c61866d98312e8cf08f78bc8ab0f213bc8dc8c0`; 180 Python tests and both CI jobs passed | DONE_VERIFIED for that checkpoint |
| Generated master artifact | Same run; 351,780 rows, 41 vowel/rime records; artifact uploaded | DONE_VERIFIED for that checkpoint |
| Python/browser IPA→Ukrainian and parity | Same run; Node adapter, 28 parity fixtures and UI contract passed | DONE_VERIFIED for tested contract; not phonetic accuracy |
| Web static validation | [Run 40316202145](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40316202145) passed | DONE_VERIFIED for that checkpoint |
| TUD research segmenter | TUD held-out boundary F1 0.872932 / exact-group rate 0.432; Wisesight source-annotated test-only boundary F1 0.792101 / exact-group rate 0.385 | PARTIAL; research-only, not production default |
| Independent Thai IPA/acoustic gold | No independent adjudicated rows; CCOST audio/TextGrid access and annotation protocol not yet completed | BLOCKED — qualified Thai phonetician, lawful pinned assets, independent labels and disagreement log required |
| Ukrainian target-form preference | No independent adjudication set | BLOCKED — two independent Ukrainian-native reviewers, frozen criteria and adjudication log required |
| `บรรจุ` final `/ʔ/` | Source-attested discrepancy retained; no global rule | PARTIAL — transcription layer, stress/context and lexical evidence must be adjudicated |
| Segmentation production readiness | No representative manual false-split/false-merge review or independent untouched-domain evaluation | PARTIAL — publish error analysis, predefine deployment thresholds and evaluate independent licensed data |
| Release readiness | No independent IPA/UA gold; segmentation remains research-only; special orthography remains evidence-gated | NOT RELEASE-READY |

The latest verified checkpoint above is not automatically evidence for later documentation commits. The audit/handoff synchronization that follows must itself pass exact-head CI and Web static validation. Engineering tests must not be reported as linguistic accuracy.


## Segmentation error review — implementation added 2026-10-26

| Task | State | Evidence / acceptance boundary |
|---|---|---|
| Deterministic false-split/false-merge report | DONE_VERIFIED — software/report contract | Exact-head CI [40320450844](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40320450844) passed 182 Python tests and the evidence-grade/error-report gate; Web static validation [40320450587](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40320450587) passed. Artifact `thai-segmentation-error-review` contains 993 source-annotated rows, 2,574 false splits, 1,981 false merges, boundary F1 0.839471 and 192/993 exact sequences; artifact ID `12648833301`. |
| Evidence-grade separation | Required gate | The 993 rows are `SOURCE_ANNOTATED`, CC0-1.0, test-only, with zero independent expert-adjudicated rows. The report is triage, not independent gold. |
| Human error review / production decision | PARTIAL | The generated artifact is a deterministic triage aid, not human adjudication. Inspect representative false splits and false merges, document error categories, set acceptance thresholds in advance, and evaluate an independent untouched domain. Until then, keep both dictionary and TUD segmenters out of production-default selection. |

The code-bearing report was added in `e80606e641d631966b566999027ee9d2b4d00bb`; exact-sequence tuple/list parity was corrected in `bec1b7027f34a4f70f0b6f9fdc415ef43343eab9`, with regression `aba6832eb97cb4b84f2e62fa058fa963cfb34803` and CI assertion `c189cdb9209d85780c3baeb1df23800101840b16`. The first artifact's zero exact-sequence count was a type-comparison bug and is superseded. Exact-head CI and Web static validation for the final branch head are required before this is marked DONE_VERIFIED.


## Comparative segmentation error review — 2026-10-26

| Task | State | Evidence / acceptance boundary |
|---|---|---|
| Dictionary false-split/false-merge triage | DONE_VERIFIED — report software | Exact-head CI [40320450844](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40320450844) verified the 993-row source-annotated report, including 2,574 false splits, 1,981 false merges and 192 exact sequences. This does not independently adjudicate each difference. |
| Same-row dictionary vs TUD error comparison | DONE_VERIFIED — report software and same-row metrics | Exact-head CI [40323209539](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40323209539) passed both jobs; Web static validation [40323209471](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40323209471) passed. Artifact from code checkpoint [40322960615](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40322960615): same 993 rows; dictionary F1 0.839471 / exact 192 (19.34%); TUD F1 0.748623 / exact 119 (11.98%). TUD false splits 8,722 vs dictionary 2,574; all labels are source-annotated, not expert gold. |
| Preliminary error-pattern notes | PARTIAL — non-expert triage only | Existing report samples visibly include numeric/punctuation and URL/Latin fragmentation, brand/name handling, and inconsistent token granularity for longer Thai sequences. These are candidate review strata, not expert-linguistic error labels; the source annotation itself may reflect its own conventions. |
| Production segmentation | PARTIAL — not accepted for production | Require a representative manually reviewed sample, predeclared acceptance thresholds, an independent licensed untouched domain, and explicit integration decision. Wisesight is source-annotated and test-only, not independent expert gold. |

The comparative report is deliberately scheduled **after** the pinned TUD training step so it consumes the exact generated model from that run. CI asserts both engines have false-split and false-merge examples and that the shared evaluation set still has zero expert-adjudicated rows. No comparative metrics are claimed until the new exact-head workflow passes.


### Verified same-row comparative result — 2026-10-26

| Engine | Boundary precision | Boundary recall | Boundary F1 | False splits | False merges | Exact token sequences |
|---|---:|---:|---:|---:|---:|---:|
| Dictionary max-match | 0.822287 | 0.857390 | 0.839471 | 2,574 | 1,981 | 192/993 (19.34%) |
| TUD unigram-Viterbi | 0.608000 | 0.973868 | 0.748623 | 8,722 | 363 | 119/993 (11.98%) |

Both engines were evaluated against the same 993 pinned Wisesight rows using the same full-text boundary policy, with non-Thai runs preserved. This is more comparable than the earlier TUD-only metrics on filtered Thai-only runs; those filtered metrics must not be directly compared with the full-text row above. The TUD system is strongly recall-heavy and over-splits on this full-text evaluation, while the dictionary baseline has better boundary F1 and exact-sequence rate. These source-annotation metrics support **not integrating TUD as production default**, but they do not establish linguistic gold accuracy.

- Code checkpoint CI [40322960615](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40322960615): both comparative-report and evidence-grade steps passed; artifact `thai-segmentation-comparative-error-review`, ID `12649094231`, SHA-256 `8005cc91939ea06b852c1717fee9fb72d370709e74267b8f99636a6476d30775`.
- Final documentation HEAD `e4ab3fd46e9c48c4220afb1f73ae5c6127b328ff): full CI [40323209539](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40323209539) passed `test` and `master-artifact`; Web static validation [40323209471](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40323209471) passed.
- Evidence grade remains `SOURCE_ANNOTATED`; expert-adjudicated rows = 0. Human review and independent-domain evaluation remain separate production acceptance gates.


## Comparative segmentation review handoff — 2026-10-26

| Task | Status | Evidence / acceptance criterion |
|---|---|---|
| Comparative JSON artifact inspection | DONE_VERIFIED | Run 40322960615, artifact 12649094231, digest `8005cc91939ea06b852c1717fee9fb72d370709e74267b8f99636a6476d30775`; artifact JSON independently parsed and metrics/provenance checked |
| Same-row dictionary vs TUD comparison | DONE_VERIFIED (source-annotated diagnostic only) | 993 rows; dictionary F1 0.839471 / exact 192; TUD F1 0.748623 / exact 119; 0 independently adjudicated rows; TUD remains research-only |
| Human-review TSV generator | PARTIAL pending exact-head CI | Script joins complete pinned source text and both available predictions, checks lossless reconstruction, adds heuristic strata and blank adjudication fields; acceptance: tests + CI artifact validation + exact-head Web static validation |
| Independent segmentation adjudication | BLOCKED | Qualified Thai reviewers must adjudicate a prespecified sample, document tokenization convention and disagreements, and produce stable IDs and decision rationale; do not tune on the test set |
| Independent Thai IPA/acoustic gold | BLOCKED | Thai phonetician/acoustic evidence and pinned lawful corpus with adjudication log |
| Independent Ukrainian target forms | BLOCKED | Two independent Ukrainian-language reviewers, blinded candidate review and documented resolution |
| `บรรจุ` final /ʔ/ | BLOCKED | Context and transcription convention must be specified, then source/audio evidence independently reviewed |
| Cross-domain segmentation evaluation | TODO | Identify license-compatible independent domain, freeze split and acceptance thresholds before any tuning |
| Full OBEC official PDF | BLOCKED | Obtain accessible official full PDF or verified local official copy; inspect full relevant pages before broadening claims |


## One-pass execution ledger — 2026-10-26 (current continuation)

| Task | Status | Evidence / acceptance criterion |
|---|---|---|
| IPA-first pipeline and Python/browser adapter boundary | DONE_VERIFIED on prior exact-head CI | Typed IPA carries tone/length/boundary/provenance/uncertainty; mutation and fail-closed tests exist. Latest-head CI is tracked separately below. |
| Dictionary vs TUD segmentation comparison | DONE_VERIFIED on comparative artifact head | Same 993 pinned CC0 Wisesight source-annotated rows; dictionary F1 0.839471 / 192 exact sequences, TUD F1 0.748623 / 119 exact sequences. These are source-label diagnostics, not independent accuracy. Keep TUD research-only. |
| Human segmentation-review sample design | PARTIAL; new implementation awaiting exact-head CI | Deterministic stratified sample plus uniform controls, full predictions for all source rows, exact reconstruction and blank adjudication fields. Acceptance: CI pass, artifact inspection, then human review. |
| Independent Thai IPA/acoustic gold | BLOCKED — external specialist + authorized audio required | CCOST is a public candidate under CC BY-NC-SA 4.0, but its manual/archive/hash and use scope still need review; qualified Thai phoneticians must independently annotate and reconcile a speaker-aware sample. |
| Independent Ukrainian target-form judgments | BLOCKED — two Ukrainian-native reviewers required | Complete existing TSV with independent blind preferences, criteria version, rationale, agreement and adjudication log. Do not infer target preference from IPA or engine output. |
| บรรจุ final /ʔ/ | PARTIAL / evidence-limited | Thai Wiktionary revision 5686263 explicitly records /ban˧.t͡ɕuʔ˨˩/. This is source-attested lexical evidence only. Decide broad phonemic vs surface transcription and contextual treatment; do not generalize a single dictionary form. |
| Independent segmentation domain | BLOCKED — licensed corpus/annotation convention not yet cleared | Choose a second corpus with verified license and immutable source snapshot; define split before evaluation; keep it untouched by training/tuning; report same-boundary-policy metrics and human error analysis. |
| Full official OBEC PDF inspection | BLOCKED — official URL returned HTTP 403 | No claim of full-PDF review. Acceptance requires lawful official access and page/section-scoped source notes; existing accessible page-scoped claims remain narrowly scoped. |
| Latest branch CI + web static validation | PARTIAL / pending | New review-sampling commits trigger fresh runs. Do not mark DONE_VERIFIED until both workflows finish successfully on the final exact HEAD. |
| Release readiness | BLOCKED | No release until engineering gates pass on final HEAD and empirical gates/declared scope are accepted. Research prototype remains the accurate classification. |

### New review-sampling implementation

- Updated `scripts/build_segmentation_manual_review.py` to compute both system predictions over the full pinned source set and select deterministic rows by heuristic strata plus uniform controls, instead of restricting the packet to top-ranked error examples.
- Updated `tests/test_segmentation_manual_review.py` to cover deterministic sampling, controls, provenance, lossless reconstruction, and fail-closed behavior.
- Updated CI to pass the generated TUD model to the sampler and verify that every selected row reconstructs exactly and all human adjudication fields remain blank.
- The packet remains `SOURCE_ANNOTATED`; the script does not promote source labels to expert gold. Exact-head workflow status must be checked after the latest commit.


## External segmentation-domain evaluation — 2026-10-26

| Task | Status | Evidence / acceptance |
|---|---|---|
| VISTEC dataset provenance and license | DONE_VERIFIED (metadata) | Dataset-specific upstream README at pinned commit 215a7dc3d384f20eb56af1cbc41fb32b7f8df57c declares CC-BY-SA 3.0; CSV Git blob SHA-1 edfcb85907a604c5e30643065ac4975862a0fe90; 49,997 samples described upstream; pinned CSV contains 50,000 data rows. |
| VISTEC annotation adapter | IMPLEMENTED; tests pending exact-head CI | Reads submissionText, splits pipe-delimited annotations, strips only documented <ne>/<msp> tags, preserves annotated text and verifies exact reconstruction. It does not use raw questionText. |
| VISTEC external evaluation workflow | IMPLEMENTED; workflow run pending | Pinned external checkout, source blob/license checks, current research-only TUD model, both segmenters, common scorer and report artifact. Acceptance requires workflow success and artifact inspection. |
| Independent segmentation-domain evidence | PARTIAL | VISTEC is a separate source/domain, but labels are still SOURCE_ANNOTATED rather than independently re-adjudicated. Report separately from Wisesight and do not tune on either test set. |
| Large-corpus scorer complexity | IMPLEMENTED; tests pending exact-head CI | Evaluator now indexes gold rows once, avoiding repeated full-list scans for every prediction; needed for ~50k-row external evaluation. |

No VISTEC metric is claimed before the external workflow finishes on this branch. Even a passing run establishes reproducible cross-domain source-annotation diagnostics, not independent expert accuracy.


## VISTEC annotation parser hardening — 2026-10-26

| Task | Status | Acceptance / evidence |
|---|---|---|
| Reject malformed empty annotation fields | IMPLEMENTED; exact-head CI pending | `parse_submission_text` now rejects any empty token after documented markup removal instead of silently filtering it. Regression cases cover repeated separators, markup-only empty tokens, leading separators and all-empty input. Code head: `1cbf97036ec931266f4a6ed5eb747a00e5b7ad29`. |
| Verify compatibility with pinned VISTEC source | BLOCKED_PENDING_WORKFLOW | The 50,000-row CSV (upstream README describes 49,997 samples) adapter must run against the immutable CSV snapshot. No metric is claimed until the external workflow succeeds and its artifact is inspected. |
| Exact-head CI and Web validation | PENDING / not yet surfaced | GitHub connector returned no workflow runs or combined statuses for the new head at the last check. This is not a pass; refresh workflow state before merge. |



## Exact-head run status refresh — 2026-10-26

The GitHub connector now reports the following runs for branch head `550f26fdbf6fd66a0d1c2cb1caa9bd6bd10de196`; each remains queued, with no conclusion yet:

| Check | Run | Current state | Acceptance |
|---|---|---|---|
| CI | [40346688497](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40346688497) | QUEUED | All repository test and generated-artifact gates pass on this exact head |
| Web static validation | [40346688520](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40346688520) | QUEUED | Static validation passes on this exact head |
| External VISTEC evaluation | [40346688621](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40346688621) | QUEUED | Pinned 50,000-row CSV (upstream README describes 49,997 samples) is accepted; report artifact inspected; no claim of independent gold |

The earlier “not yet surfaced” state is superseded by this timestamped refresh. Queueing is not a successful validation result.


## Follow-up after failed validation — 2026-10-26

| Task | Status | Evidence / acceptance |
|---|---|---|
| Stale corpus-license unit assertion | FIXED_PENDING_EXACT_HEAD_CI | CI run 40346688497 failed because the test expected old wording; updated to assert the registry's pinned-source declaration. |
| VISTEC row-count contract | FIXED_PENDING_EXTERNAL_RERUN | Run 40346688621 verified the pinned commit/blob but evaluator rejected 50,000 actual CSV data rows against stale expected count 49,997. Evaluator/workflow now assert 50,000; corpus registry explicitly records upstream README's 49,997 claim separately from CSV count. |
| Web static validation | DONE_VERIFIED_FOR_PRIOR_CODE_HEAD | Run 40346688520 passed; final code-bearing head must be checked if workflows trigger. |

No VISTEC metric is claimed until the corrected workflow completes and its report artifact is inspected. Source labels remain unadjudicated.


## Corrected exact-head verification — 2026-10-26

The stale unit-test assertion and the VISTEC 50,000-row count contract are fixed in code. Latest observed runs for the corrected workflow head: CI [40353097806](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40353097806), Web static validation [40353097480](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40353097480), VISTEC [40353097539](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40353097539). All were queued at the last poll. Acceptance remains pending successful exact-head CI, successful full 50,000-row evaluation, and report-artifact inspection.


## Latest verification and regression repair — 2026-10-26

| Task | Status | Evidence / acceptance |
|---|---|---|
| VISTEC external evaluation on corrected 50,000-row snapshot | DONE_VERIFIED (source-annotation diagnostic only) | Run [40354836797](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40354836797) succeeded on prior head; confirms immutable source checks and evaluator execution, not expert-adjudicated accuracy. Inspect artifact before reporting metrics. |
| Web static validation | DONE_VERIFIED for prior head only | Run [40354836884](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40354836884) passed; rerun after the latest test-only fix if workflow triggers. |
| VISTEC source registry license test | FIXED_PENDING_EXACT_HEAD_CI | CI [40354836807](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40354836807) exposed one stale assertion among 194 tests: expected `verify upstream terms` despite the pinned source README declaring CC-BY-SA-3.0. Updated the test to assert `attribution/share-alike required` at commit `0e60b2d277facee573839335b7e1681d5520a224`. Acceptance: exact-head CI passes all tests. |
| Overall engineering validation | PARTIAL | VISTEC and static validation passed on the preceding head; Python CI failed one outdated assertion and must be rerun after the repair. |
| Research / release readiness | BLOCKED / research prototype | Expert linguistic/target adjudication and lawful official OBEC PDF review remain outstanding. |


## VISTEC report result (source-annotated diagnostic only) — 2026-10-26

The successful external run [40354836797](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40354836797) evaluated 50,000 source-annotated rows (0 expert-adjudicated). The JSON printed in the workflow log reports:

| Segmenter | Boundary precision | Boundary recall | Boundary F1 | Exact sequences |
|---|---:|---:|---:|---:|
| Dictionary maximum matching | 0.76880 | 0.89788 | 0.82834 | 76/50,000 (0.152%) |
| Research-only TUD unigram Viterbi | 0.60640 | 0.99316 | 0.75302 | 16/50,000 (0.032%) |

Both had 100% output coverage, which is not accuracy. These scores measure agreement with source-provided annotations, not expert-adjudicated segmentation. The low exact-sequence rates mean neither system is production-ready. Artifact ZIP ID 12667445022 exists and its digest is recorded in the handoff; the archive itself still needs inspection. Exact-head checks after the latest test-only repair remain queued.


Artifact verification: downloaded and inspected VISTEC artifact ZIP 12667445022; it contains one JSON report (3,803 bytes), schema 1.0. Parsed report matches the metrics above and explicitly records 50,000 SOURCE_ANNOTATED rows and 0 adjudicated rows. Artifact integrity/contents: DONE_VERIFIED; linguistic gold quality remains BLOCKED pending human adjudication.

## Public beta site update — 2026-10-26

| Task | Status | Acceptance / evidence |
|---|---|---|
| Visible beta disclosure on service page | IMPLEMENTED; exact-head checks pending | Homepage now identifies the tool as a research beta and links to evidence/limitations. |
| Evidence disclosure on system page | IMPLEMENTED; exact-head checks pending | Shows VISTEC and Wisesight source-annotation diagnostics with explicit zero independently expert-reviewed rows; labels segmentation as not production-ready. |
| Responsive styling for beta notice | IMPLEMENTED; exact-head checks pending | Added mobile layout rules; automated UI contract assertions added. |
| Publish updated branch to public GitHub Pages | BLOCKED by release path | Pages workflow deploys on pushes to `main`; PR #71 is still draft. Do not deploy the draft branch over the current public site or merge its 304-commit diff blindly. Publish after the reviewed PR is merged, or create a separate preview host. |
| Empirical linguistic validation | BLOCKED | No independent Thai IPA/acoustic gold, independent Ukrainian target-form judgments, or expert-adjudicated segmentation rows. |

Latest successful pre-UI-update verification is on `17eac785a00ce1e8a95ac904db348ddf8c286040`: CI run 40372261539, Web static validation 40372261553, VISTEC evaluation 40372261718 all succeeded. The beta UI/test edits are newer and must pass their own exact-head checks before they are considered verified.

## Beta-site publication attempt — 2026-10-26

| Task | Status | Evidence / blocker |
|---|---|---|
| Beta notice, evidence panel, responsive CSS and UI regression | DONE_VERIFIED on code checkpoint `274371594cc8a0b65677bb126242d90acc17caf5` | Pages build [40377552366](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40377552366) passed Python regression tests, Python/browser parity and the new UI-contract test. Static validation [40377552367](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40377552367) and VISTEC diagnostic [40377560151](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40377560151) passed. |
| Publish branch build to GitHub Pages | BLOCKED | The same Pages run's `deploy` job failed immediately with no steps/logs; the build job succeeded. The latest successful public deployment is still main commit `18ab41db87192dc7be69683ef85e53cb04db5517` from run [40225366216](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40225366216). The known deployment path is main-only; the research PR remains draft. |
| Avoid unintended repeated deployment attempts | DONE_VERIFIED | Restored `.github/workflows/pages.yml` to trigger Pages deployment only on `main`; retained the UI-contract check in the Pages build. |
| Latest exact-head overall CI | PARTIAL / running | Latest branch head is `048b89d9234ac91e3d592c0bca7d816f4a5ae5b5`; CI runs 40378276967 and 40378286378 were still in progress at audit refresh. Do not mark the latest exact head fully green until the master-artifact job completes. |
| Public beta URL | BLOCKED for the new branch build | The existing site remains at [GitHub Pages](https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/) on the last successful main deployment. Do not claim the newly edited pages are live. To publish this exact engine, the owner must either merge the reviewed research PR to `main` after accepting the documented evidence gates, or authorize a separate preview host. No environment protections were changed and no PR was merged.

## Post-merge publication status — 2026-10-26 20:51 EET

This section supersedes the earlier pre-merge publication statements above.

| Task | Status | Evidence / acceptance |
|---|---|---|
| Merge reviewed research-beta code | DONE_VERIFIED | PR [#71](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/71) merged to `main` as `b4ae9e9f88a79d6f55cb1207363ac6877df080ba`. The UI remains explicitly labelled research beta and does not claim independent pronunciation accuracy. |
| Beta build and regression checks | DONE_VERIFIED for merged code checkpoint | Pages run [40378981918](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981918) build job passed Python regression tests, generated-fixture parity, browser parity, UI-contract checks, and Pages artifact upload. Web static validation [40378982254](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378982254) passed. CI run [40378981710](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981710) had its test job pass; master-artifact job remains queued. |
| Publish beta artifact to public GitHub Pages | BLOCKED by deployment queue | At 2026-10-26 20:51 EET, run 40378981918 remained `queued` despite build success; deploy job 121775188761 had no runner assigned and no steps. Pending deployment approval endpoint returned an empty list. The exact infrastructure cause is not observable from available data. Do not state that the new beta is live. Last successful deployment remains run [40225366216](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40225366216), main commit `18ab41db87192dc7be69683ef85e53cb04db5517`. |
| Pages workflow scope | DONE_VERIFIED | `.github/workflows/pages.yml` deploys only from `main`; no environment protections or external settings were changed. |
| Linguistic validation / release readiness | BLOCKED / research-only | Independent Thai IPA/acoustic gold, human segmentation adjudication, independent Ukrainian target-form reviews, contextual review of บรรจุ final /ʔ/, and lawful access to the full official OBEC PDF remain unresolved. VISTEC/Wisesight source-annotated metrics are diagnostics, not expert gold. |

## Final deployment status correction — 2026-10-26 22:08 EET

This update supersedes the prior row stating that the Pages deployment was blocked by a queue.

| Task | Status | Evidence / acceptance |
|---|---|---|
| GitHub Pages deployment of research beta | DONE_VERIFIED at workflow level | Run [40378981918](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981918) completed successfully: build job 121769734639 PASS and deploy job 121775188761 PASS. Public URL: https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/. Direct live HTML inspection was unavailable, so the workflow deployment is verified but served-markup details are not independently confirmed. |
| Main CI, including generated master artifact | DONE_VERIFIED | Run [40378981710](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981710): test job PASS; master-artifact job PASS. |
| Web static validation | DONE_VERIFIED | Run [40378982254](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378982254): PASS. |
| Release readiness / linguistic evidence | BLOCKED / research-only | Deployment success does not close evidence gates: independent Thai IPA/acoustic gold, human segmentation adjudication, two independent Ukrainian target-form reviews, contextual review of บรรจุ final /ʔ/, and lawful full official OBEC PDF access remain outstanding. The source-annotated segmentation scores are diagnostic only, not expert gold. |


## Whole-text web input segmentation — 2026-10-26

| Task | Status | Evidence / acceptance boundary |
|---|---|---|
| Web UI accepts whole text | DONE_VERIFIED on code head `3ccf84f564add02c189524c3b9ca794154d35c8b` | CI `test` and `master-artifact` both passed in [40402504410](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504410); static validation passed in [40402504394](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504394). Punctuation, whitespace, Latin text, and numbers remain separate tokens. Merged in commit `e49b5f2b54d42e577f732b4308080e11e410d557`; live Pages publication has not been independently confirmed. |
| Segment adjacent unspaced Thai text into known lexicon entries | PARTIAL implementation; regression tests DONE_VERIFIED | Browser engine applies greedy longest-known-entry matching inside continuous Thai-script runs and preserves unmatched spans as `unresolved`. Covered cases: `กาไฟมา`, mixed known/unknown `ทดสอบกาไฟ`, reviewed full-sentence entry `กินข้าวกับไข่และผลไม้` (seven IPA outputs), punctuation `กา,ไฟ!มา`, whitespace/punctuation `กาไฟ มา!`, and adjacent lexical IPA overrides `เงินเดิน`. Code checkpoint `3ccf84f564add02c189524c3b9ca794154d35c8b` passed CI `test` + `master-artifact` in [40402504410](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504410) and static validation in [40402504394](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504394). PR #73 merged as `e49b5f2b54d42e577f732b4308080e11e410d557`; the documentation reconciliation PR #74 then passed CI `test` + `master-artifact` in [40404124198](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40404124198) and was merged as `605d849c2148b7242fac56e581b6319bb17fd4f4`. **Limitation:** this proves code/test-contract behavior, not linguistic segmentation accuracy; greedy matching can misidentify substrings in unknown words. Live Pages publication remains unverified. |
| General Thai word segmentation | TODO / evidence-limited | Dictionary max-match is a baseline, not a linguistically complete or context-aware segmenter. Ambiguous boundaries, unknown vocabulary, repetition markers, compounds, and context-sensitive readings require evaluated coverage and adjudicated boundary data. Do not claim arbitrary Thai text is fully recognized. |
| IPA for every arbitrary text span | BLOCKED by linguistic evidence and coverage | IPA is shown only for deterministic, reviewed lexicon entries or typed source-attested overrides. Unknown spans are preserved and withheld from guessed IPA/Ukrainian output. |
| Example-button IPA contract | DONE_VERIFIED on code head `3ccf84f564add02c189524c3b9ca794154d35c8b` | Homepage examples use supported lexicon entries and the CI UI-contract test requires phonological IPA for every example. CI `test` + `master-artifact` passed in [40402504410](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504410); static validation passed in [40402504394](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504394). |


## Current authoritative status — 2026-10-26 23:41 EET

This section is the current decision record for the whole-text Thai input work. Older rows above contain historical checkpoints and may describe earlier branches, runs, or deployment queues; do not interpret those older statements as the current state when they conflict with this section.

- **Current `main` after merged code and documentation:** `605d849c2148b7242fac56e581b6319bb17fd4f4` (PR #73 code merge `e49b5f2b54d42e577f732b4308080e11e410d557`, followed by PR #74 documentation reconciliation).
- **Code-bearing checkpoint actually tested:** `3ccf84f564add02c189524c3b9ca794154d35c8b`. CI `test` + `master-artifact` passed in [40402504410](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504410); web static validation passed in [40402504394](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504394). PR #74 documentation-only follow-up also passed CI `test` + `master-artifact` in [40404124198](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40404124198).
- **Documentation cleanup:** PR #75 consolidates duplicated whole-text evidence and makes the segmentation limitation explicit. Its current head is `16febbadc20c013e8cc3c208ef3742ab04bd7a52`; it is open and must not be treated as merged until its required checks pass and merge status is confirmed.
- **Implementation status:** whole-text UI and tested known-word segmentation baseline are present. The segmenter uses greedy longest-match and can falsely split a substring inside an unknown word; tests prove deterministic behavior on listed examples, not general Thai segmentation accuracy.
- **Public deployment:** UNVERIFIED. The Pages workflow is configured for relevant pushes to `main`, but the available connector only reports pull-request-triggered workflow runs, while direct retrieval of served HTML was unavailable. Do not claim the merged changes are live without confirming a successful Pages deploy and inspecting served HTML.
- **Research/release classification:** PARTIAL RESEARCH PROTOTYPE, not release-ready. Independent Thai segmentation adjudication, Thai IPA/acoustic gold, Ukrainian target-form review, contextual treatment of `บรรจุ` final /ʔ/, and lawful full official OBEC PDF access remain evidence-gated blockers. Source-annotated Wisesight/VISTEC metrics remain diagnostics, not expert gold.


## Current authoritative status — 2026-10-27 (supersedes stale 2026-10-26 status)

- **Current main merge commit:** `581231596a0df6b3ab58964dacedeec7a8fd8908`, which merged documentation PR #75. PR #75 CI run [40406992550](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40406992550) completed successfully: both `test` and `master-artifact` jobs passed. The test job includes Python tests, generated-artifact drift checks, the 351,780-row/41-vowel master table assertion, IPA→Ukrainian tests, Python/browser parity, UI-contract checks, and segmentation/IPA diagnostics.
- **Code-bearing implementation checkpoint:** `3ccf84f564add02c189524c3b9ca794154d35c8b`; CI `test` + `master-artifact` passed in [40402504410](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504410), and web static validation passed in [40402504394](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40402504394). Documentation-only PR #75 did not change runtime code.
- **Whole-text input:** DONE_VERIFIED. **Greedy matching against known entries:** PARTIAL. **Arbitrary Thai segmentation:** TODO / evidence-limited. **IPA for every arbitrary text span:** BLOCKED by vocabulary coverage and independent linguistic evidence. The engine intentionally withholds IPA for unresolved spans rather than inventing a reading.
- **Known limitation:** greedy longest-match can select a known substring inside a larger unknown word and can choose the wrong boundary in ambiguous contexts. The tests prove the declared cases only; they do not establish general Thai segmentation accuracy.
- **Live GitHub Pages:** UNVERIFIED for the whole-text change. The prior Pages deployment at run [40378981918](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40378981918) predates this change. Current acceptance criterion: confirm a successful Pages build and deploy after the relevant `main` change and inspect the served homepage HTML for the updated examples and whole-text hint.
- **Still evidence-blocked:** independent Thai word-boundary adjudication; independent Thai IPA/acoustic gold; two independent Ukrainian target-form reviews; contextual review of `บรรจุ` final /ʔ/; lawful full official OBEC PDF; and per-resource license/attribution compliance.
- **Readiness:** PARTIAL RESEARCH PROTOTYPE, not release-ready for arbitrary Thai text. Source-annotated Wisesight/VISTEC results are diagnostics, not expert-adjudicated accuracy.


## Current authoritative status — 2026-10-27, browser dictionary fallback merged

- **Main HEAD:** `96c2af3c2a24d0ea95455b5d6af4c079e5609d29` (PR #77). PR [#77](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/77) adds a reproducible browser word index generated from the existing pinned 60,963-entry CC0 Thai dictionary. Generated output is 1,615,714 bytes across 51 first-character buckets and is intentionally ignored/not committed.
- **Verified behavior:** the browser now chooses the longer match from the CC0 dictionary or curated lexical entries, with curated entries winning ties. The regression `กาแฟ` prevents a known substring `กา` from receiving partial IPA inside a longer dictionary word. A regression on `เงินเดิน` caught a grapheme-boundary bug: a following preposed vowel was being consumed as a combining mark; the implementation now excludes preposed vowels from that mark set.
- **Evidence grade:** the dictionary provides boundary evidence only, not pronunciation gold. A dictionary-matched word without curated syllabification or typed source-attested IPA remains unresolved; no IPA or Ukrainian candidate is invented.
- **Tests:** web static validation passed for latest pre-merge head `7b2c9572feb542fb3ee81558b9758bb4fa5f2bef` in [run 40411659863](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40411659863). The full CI `test` job passed on runtime code head `3eb1155631da158b7e04436f608711680750e475` in [run 40411558761](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40411558761); the `master-artifact` job remained queued, and exact-head CI for `7b2c9572` was queued. These must not be described as exact-head full CI/master-artifact passes.
- **Post-merge workflow state:** Pages deployment [run 40412224812](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40412224812), main CI [run 40412224673](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40412224673), and web static validation [run 40412224629](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40412224629) were queued at the last check. The Pages workflow now retries a post-deploy HTTP check until the live homepage exposes the expected whole-text hint, examples, and beta notice. Do not claim live deployment until that job succeeds.
- **Remaining status:** whole-text input = DONE_VERIFIED; browser dictionary-backed max-match = PARTIAL; context-aware arbitrary Thai segmentation = TODO/evidence-limited; complete IPA for arbitrary text = BLOCKED by lexical coverage and independent linguistic evidence; live deployment = BLOCKED/queued pending the Pages workflow.
- **Research blockers remain:** independent Thai boundary adjudication, independent Thai IPA/acoustic gold, two Ukrainian target-form reviews, contextual review of `บรรจุ` final /ʔ/, lawful access to the full official OBEC PDF, and per-resource licensing/attribution review.
- **Readiness:** partial research prototype, not release-ready for arbitrary Thai text.


## Browser dictionary lookup optimization — 2026-10-27

- **PARTIAL / awaiting exact-head CI:** the browser's pinned CC0 Thai word dictionary is now indexed by the first two Unicode code points instead of the first code point alone. Candidate matching semantics remain longest match with curated lexical entries winning ties; dictionary-only matches still authorize boundaries only, never IPA or Ukrainian output.
- The generator validates each bucket key against each word and reports the largest bucket so CI logs provide a deterministic candidate-scan bound for the pinned snapshot.
- Existing UI contract tests continue to guard `กาแฟ` (no false partial IPA for `กา`), adjacent known entries, unresolved spans, lexical IPA overrides, punctuation, and whole-sentence input.
- Acceptance: exact-head CI `test` + `master-artifact`, web static validation, and Pages build/deploy must pass. This optimization is not evidence of linguistic accuracy; independent segmentation adjudication and IPA/UA review remain blocked by missing human evidence.

## Browser prefix-index performance change — 2026-10-27

- **TODO / exact-head verification pending:** branch `perf/browser-dictionary-prefix-index-20261027` changes the generated CC0 dictionary index from one-code-point to two-code-point prefixes. Lookup checks the longer-prefix bucket first and falls back to the one-code-point bucket for single-character dictionary entries, preserving longest-match behavior.
- **Tests added:** generated index must contain all 60,963 pinned unique entries, every word must be in the correct prefix bucket, and every bucket must be sorted longest-first with deterministic code-point ordering. Existing Python/browser parity and UI regressions cover user-visible segmentation behavior, including `กาแฟ` and unresolved unknown spans.
- **Acceptance:** exact branch-head CI `test` + `master-artifact`, web static validation, and Pages workflow where applicable. No measured speedup is claimed until a reproducible benchmark is run; this is an algorithmic candidate-scan reduction, not a linguistic accuracy improvement.
- **Unchanged blocker:** independent expert segmentation/IPA gold and independent Ukrainian target-form adjudication remain unavailable; arbitrary-text IPA coverage remains partial.

## Prefix-index change — final evidence reconciliation (2026-10-27)

- **DONE_VERIFIED — implementation and browser acceptance:** PR #79 merged as `c799dbed4247ac9743845acc0fd4131922cfbb74`. Code-bearing commit `e17a7f96fef9989f6375d36331f30ce0246e378a` passed CI run [40466046264](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466046264) and Web static validation [40466046237](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466046237). The CI run completed both `test` and `master-artifact`; the static run passed the generated dictionary integrity checks, 28 Python/browser parity fixtures, text regressions and UI contract.
- **DONE_VERIFIED — post-merge site build/deployment:** main run [40466830868](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466830868) passed Pages build, deployment and the live served-homepage contract check. Main Web static validation [40466830820](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466830820) also passed. Main CI run [40466830808](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40466830808) passed its `test` job; its duplicate `master-artifact` packaging job was still running at the time of this update. The equivalent code-bearing commit had already passed that job.
- **Observed generated-index metrics:** 60,963 words; 1,085 two-code-point buckets; largest bucket 1,521 entries; generated JavaScript 1,629,301 bytes. Previous one-code-point index was 1,615,714 bytes, so the uncompressed artifact grew by 13,587 bytes (about 0.84%). This is an index-size/candidate-bucket observation, not a measured runtime speedup.
- **Invariant preserved:** dictionary membership is boundary evidence only. It does not license IPA or Ukrainian output. Curated lexical entries retain tie precedence; unresolved spans still abstain. No linguistic-accuracy claim was added.
- **Still PARTIAL/BLOCKED:** arbitrary Thai segmentation quality and complete IPA for arbitrary text require independent boundary adjudication, independent Thai IPA/acoustic gold, and independent Ukrainian target-form reviews. The product remains a partial research prototype, not release-ready for arbitrary Thai text.

## Browser segmentation latency diagnostic — 2026-10-27

- **PARTIAL / awaiting exact-head CI:** added `scripts/benchmark_web_segmentation.mjs` and a CI step that publishes `thai-browser-segmentation-latency-diagnostic` for 100-, 250- and 500-code-point Thai runs. Each case uses five warmups and 30 measured runs; the report records median, p95, min/max, runtime version and basic output counts.
- **Measurement contract:** this is a wall-clock diagnostic, not a fixed-threshold performance gate. CI-runner timing is environment-specific; compare only like-for-like runs. It measures neither segmentation accuracy nor IPA/Ukrainian correctness.
- **Acceptance:** exact-head CI must pass and the artifact must be inspectable before reporting measured timings. Do not claim a speedup without a comparable pre-index baseline on the same runner/runtime. Unknown text must continue to abstain from IPA/Ukrainian output.
- **Unchanged evidence blockers:** independent Thai word-boundary adjudication, independent Thai IPA/acoustic gold, independent Ukrainian target-form reviews, contextual review of `บรรจุ` final /ʔ/, lawful access to the complete official OBEC PDF, and per-resource license/attribution review.
