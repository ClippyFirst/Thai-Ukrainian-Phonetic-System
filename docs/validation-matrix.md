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
| lexical segmentation | PARTIAL | pinned CC0 dictionary max-match and separate 60,963-entry lexicon; evaluated on held-out Wisesight but current baseline is weak; no claim of production-quality segmentation |
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
