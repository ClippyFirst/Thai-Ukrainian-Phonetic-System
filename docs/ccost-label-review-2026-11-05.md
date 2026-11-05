# CCOST label and marker review — 2026-11-05

## Scope and evidence

This review covers the owner-supplied `CCOST textgrid.zip` only. The inspection workflow read the 488 Praat long-text `.TextGrid` members and did not extract, open, hash, or otherwise process audio. The archived machine report is the CI artifact [textgrid-archive-inspection, run 42018381197](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42018381197/artifacts/13410038957). Its SHA-256 artifact digest is `dd3b0f263fe72e17af7d6de1e429385286140fb55d1df0b6e3ba3a33c3925cc2`.

Primary sources:
- [CCOST LREC 2026 paper, §3.3–3.4](https://aclanthology.org/2026.lrec-1.247/): explicitly identifies X-SAMPA for phonemic/phonetic representations; defines only tone suffixes `_1`–`_5`; says disfluencies are marked `<usb>` and pauses `<p:>`; describes phonetic variants at MAU level.
- [CCOST Zenodo record and manual](https://zenodo.org/records/17366698): CC BY-NC-SA 4.0 and release documentation. I extracted/search-inspected the public `CCOST_manual.pdf`: it documents the RA workflow and the CHUNKPREP → G2P → MAUS → PHO2SYL pipeline, but is not a phonetic-symbol key; the extracted text contains no `_8` or definitions for `<P>`, `<P:>`, `<:p>`, or `<Fail>`.
- [BAS Partitur Format, MAU tier](https://www.phonetik.uni-muenchen.de/Bas/BasFormatseng.html): defines generic MAU labels `<nib>` (non-speech event), `<p:>` (pause), and `<usb>` (speaker event that cannot be classified, e.g. unintelligible words).
- [BAS WebServices FAQ](https://clarin.phonetik.uni-muenchen.de/BASWebServices/help/help_examples): generic MAUS tone suffix syntax permits `_1`–`_9` and disallows `_0`; this is a generic syntax rule, not the CCOST language-specific mapping. The CCOST paper maps only `_1`–`_5`.

## Observed release tier names

All 488 files parsed. The release uses six non-empty tier names:

| Observed tier | Non-empty labels | Interpretation |
|---|---:|---|
| `ORT-MAU` | 133,344 | Tokenized orthographic word segmentation based on MAUS (BAS definition) |
| `KAN-MAU` | 133,338 | Canonical word pronunciation in X-SAMPA, aligned through MAUS (BAS definition) |
| `KAS-MAU` | 133,340 | Phonological syllable segmentation based on G2P, aligned through MAUS (BAS definition) |
| `MAU` | 445,723 | Phone-level phonetic segmentation |
| `MAS` | 195,288 | Phonemic syllable tier |
| `TRN` | 12,090 | Orthographic utterance transcript |

The CCOST paper defines the base annotation roles and X-SAMPA convention. The BAS WebServices tutorial independently defines the exact suffixed tier names found in this release: `ORT-MAU` is tokenized word segmentation based on MAUS; `KAN-MAU` is the same with canonical pronunciation encoded in X-SAMPA; `KAS-MAU` is phonological syllable segmentation based on G2P. Thus the `-MAU` suffix identifies the MAUS-based output layer/workflow, not an unexplained corpus-specific phonetic symbol. The suffix semantics are now **DONE_VERIFIED** from the BAS documentation. Keep the literal tier names in raw records; map their roles explicitly rather than destructively renaming them to `ORT`/`KAN`/`KAS`.

## Exact failure inventory

The inspector recorded **1,014 failed conversion occurrences**, representing **116 distinct raw label strings**. Occurrences are tier-level failures; the same interval/label may appear in multiple tiers, so 1,014 is not a count of unique underlying speech events.

| Failure class | Occurrences | Distinct raw strings | Interpretation / action |
|---|---:|---:|---|
| Unmapped CCOST tone suffix `_8` | 868 | 22 | The CCOST paper maps `_1`–`_5`; general BAS/MAUS syntax permits numeric tone suffixes `_1`–`_9`. `_8` is syntactically possible in MAUS but has no published CCOST category mapping in the paper. Its corpus-specific meaning is unresolved; do not map it to IPA. |
| Slash/alternative notation | 58 | 27 | Includes frequent `r/` (23 occurrences) and compound strings. Meaning unresolved; do not rewrite slash as a phoneme or boundary. |
| MAUS marker mixed with phonetic/text material | 26 | 20 | Preserve entire raw label. Do not strip marker and convert the remainder automatically. |
| Non-ASCII phonetic-looking sequences | 17 | 9 | Includes `ɹ`, `ɾ`, `tʃ`, `ʔ`, `nˠ`, and a combining ring. They resemble IPA, but are not self-authenticating IPA fields. |
| Thai-script text or mixed Thai/phonetic label | 10 | 8 | Treat as text/mixed/unknown, not as an IPA string. |
| Truncated or malformed token | 14 | 13 | Includes trailing markers such as `a:_`, `e:_`, `t_`, `r-`; no repair inferred. |
| Other unsupported ASCII sequences | 21 | 17 | Includes opaque punctuation, backslash, malformed tokenization, and mixed token patterns. |
| **Total** | **1,014** | **116** | All remain preserved and fail-closed. |

Tier distribution of the 1,014 failed occurrences:

| Tier | Failed occurrences |
|---|---:|
| MAU | 276 |
| MAS | 263 |
| KAS-MAU | 239 |
| KAN-MAU | 236 |
| **Total** | **1,014** |

Most frequent unresolved strings are `? a_8` (428), `l {:_8 p` (201), `a_8` (138), and `{:_8` (59). These four strings account for 826 occurrences; the remaining 42 distinct strings account for 188 occurrences. They remain raw source labels.

## Marker inventory: separate markers from phonetic notation

The inspector counted **89,929 marker appearances across tier labels**. These are tier-level appearances, not deduplicated events; the same marker can be represented in aligned tiers.

| Raw marker | Appearances | Evidence-based classification |
|---|---:|---|
| `<p:>` | 77,835 | Pause/silence marker (CCOST paper and BAS) |
| `<usb>` | 7,252 | Speaker-produced but unclassifiable event; CCOST paper uses it for disfluencies (CCOST paper and BAS) |
| `<nib>` | 4,260 | Non-speech event/noise (BAS) |
| `<P>` | 394 | **Unresolved**; uppercase form is not interchangeable with `<p:>` |
| `<notProcessedChunk>` | 142 | MAUS dummy failure segment inserted when a chunk could not be processed; alignment/processing failure, not a speech phone (BAS FAQ) |
| `<:p>` | 22 | **Unresolved variant**; not normalized to `<p:>` without evidence |
| `<Fail>` | 16 | **Unresolved**; no failure semantics inferred |
| `<P:>` | 4 | **Unresolved**; case-sensitive distinct marker |
| `<usb><usb>` | 2 | Repeated marker sequence; preserve raw |
| `<p:><p:>` | 2 | Repeated marker sequence; preserve raw |

Only tag-only labels made exclusively of a documented marker may be classified as non-phonetic markers. Mixed forms such as `m O:_1<usb>`, `<usb>v`, `n<p:>`, `<p:>z`, and marker-plus-Thai transcript strings are not silently stripped or partially converted.

## What is and is not IPA

- The paper says the phonemic and phonetic tiers use **X-SAMPA**, not IPA. A successful conversion is a derived IPA candidate, with provenance, not a source IPA annotation.
- BAS documentation explicitly defines `ORT-MAU`, `KAN-MAU`, and `KAS-MAU`; their suffix semantics are now resolved. MAU remains the phone-level phonetic segmentation tier; MAS remains the phonemic syllable tier.
- `ORT-MAU` and `TRN` are orthographic/text tiers. Their Thai-script content is not IPA.
- `MAU` is phone-level; `MAS` is phonemic/syllabic. They must not be conflated.
- Unicode IPA-looking characters in failed labels are not automatically passed through as IPA. The label may be mixed, corrupted, or use another convention.
- The CCOST paper maps five toneme categories to `_1`–`_5` (Mid, Low, Falling, High, Rising). General BAS/MAUS documentation separately permits tone suffix numbers `_1`–`_9`. Therefore `_8` is syntactically allowed by generic MAUS notation but is not mapped to a CCOST category in the paper. Its meaning in these CCOST labels is unresolved; do not call it a sixth Thai tone or infer a replacement.
- `<notProcessedChunk>` is a documented MAUS processing-failure placeholder, not a phonetic value. No phonetic value is guessed for `<P>`, `<Fail>`, `<:p>`, `<P:>`, slash forms, or truncated labels.

## Acceptance and status

| Task | Status | Evidence / acceptance |
|---|---|---|
| Inspect 488 CCOST TextGrids | DONE_VERIFIED | CI parsed all 488 long-text files |
| Inventory observed tier names and counts | DONE_VERIFIED | Counts above; raw tier names preserved |
| Classify documented MAUS markers and chunk failure label | DONE_VERIFIED | CCOST paper + BAS FAQ: `<p:>`, `<usb>`, `<nib>`, `<notProcessedChunk>` |
| Separate orthography, markers, and X-SAMPA candidates | DONE_VERIFIED for the inventory | Source roles documented; mixed forms remain unsupported |
| Explain `-MAU` tier suffixes | DONE_VERIFIED | BAS tutorial explicitly defines ORT-MAU, KAN-MAU and KAS-MAU |
| Establish `_8` meaning in CCOST | BLOCKED | CCOST paper documents five mappings `_1`–`_5`; generic BAS/MAUS syntax allows `_1`–`_9`. `_8` has no established CCOST category mapping. Preserve and abstain pending source-specific evidence. |
| Resolve remaining 146 failed occurrences | PARTIAL/BLOCKED | 116 raw strings inventoried; specialist/curator review required |
| Promote converted labels to IPA gold | BLOCKED | Independent Thai review and adjudication still required |

**Do not promote any of these 1,014 occurrences to IPA or phoneme output.** The current adapter remains a conservative, partial candidate converter; source annotations are not independent gold and linguistic accuracy remains `NOT_MEASURED`.


## Adapter behavior change

The converter previously treated any tag-only angle-bracket string as a non-phonetic marker. That was too permissive: tag shape alone does not establish semantics. The adapter now skips only the three source-documented markers `<p:>`, `<nib>`, and `<usb>`. Unknown tag-only labels (`<Fail>`, `<P>`, `<P:>`, `<:p>`, `<notProcessedChunk>`) now raise the normal unsupported-label error instead of being silently omitted. Mixed tag-plus-text labels continue to fail closed. Regression tests cover this distinction.


## Primary-paper clarification (2026-11-05)

A closer reading of the published LREC 2026 paper, §3.3–3.4, resolves part—but not all—of the tier question:

- MAU = phonetic segment tier; phonetic variants are annotated there.
- MAS = phonemic syllable tier.
- KAN = canonical word pronunciation.
- KAS = canonical syllabified pronunciation.
- ORT = orthographic word; TRN = orthographic utterance transcript.
- The paper explicitly says phonemic and phonetic representations use X-SAMPA.
- The paper documents only _1 Mid, _2 Low, _3 Falling, _4 High, _5 Rising.

The paper does **not** define why the release's ORT-MAU, KAN-MAU, and KAS-MAU names carry -MAU, nor does it document _8 or the unresolved tag spellings. These remain questions for the named data curators. The base meaning of MAU is no longer unknown; the suffix/alias relationship remains unresolved.


## BAS cross-check — 2026-11-05

The BAS WebServices tutorial defines the exact tier labels present in this release: `ORT-MAU` (tokenized word segmentation based on MAUS), `KAN-MAU` (canonical word pronunciation encoded in X-SAMPA), and `KAS-MAU` (phonological syllable segmentation based on G2P). This resolves the `-MAU` suffix question without curator input. The BAS FAQ also explains `notProcessedChunk`: MAUS inserts a very short dummy segment when one or more chunks cannot be processed; likely causes include transcript/signal mismatch or a chunk too short for its expected phone sequence. Therefore `<notProcessedChunk>` is a processing/alignment failure marker, not a phonetic segment. It should be classified separately from the unresolved `<P>`, `<P:>`, `<:p>`, and `<Fail>` spellings.

Sources: [BAS WebServices tutorial](https://clarin.phonetik.uni-muenchen.de/BASWebServices/help/tutorial) · [BAS FAQ: chunkNotProcessed / notProcessedChunk](https://clarin.phonetik.uni-muenchen.de/BASWebServices/help/help_examples).


The public CCOST annotation manual was also checked directly from the Zenodo record. It describes the production workflow and MAUS pipeline but does not define `_8` or the four unresolved tag spellings. No public definition for those labels was found in the corpus paper, manual, BAS documentation, or the GitHub searches performed for this review.


### `_8` resolution — BAS tone inventory

The BAS WebServices FAQ states that generic MAUS tone notation uses numeric suffixes `_1`–`_9` attached to the syllable nucleus (and explicitly excludes `_0`). This is a generic syntax rule, not a language-specific tone inventory. The CCOST paper documents five Thai toneme mappings `_1`–`_5` (Mid, Low, Falling, High, Rising), but does not define `_8`. Thus `_8` is **not invalid under generic MAUS syntax**, yet it is **unmapped in the published CCOST convention**. It may be a corpus-specific code, annotation anomaly, or another use; the available evidence does not decide. Keep all 868 occurrences fail-closed and do not replace or convert them until their CCOST-specific meaning is established.

## Contextual review worklist — 2026-11-05

A machine-readable blind worklist is now generated by `scripts/build_ccost_review_worklist.py` and published by CI as `ccost-label-adjudication-worklist`. It scans only TextGrid members, includes all four unresolved marker spellings across tiers, preserves source labels and exact intervals, and adds overlapping cross-tier labels plus adjacent same-tier context. Expert decision fields are blank; no source value is corrected or inferred.

The `_8` count is a **tier-occurrence count**, not a count of independent speech tokens:

| Denominator | Count | Meaning |
|---|---:|---|
| Tier-level `_8` occurrences | 868 | All failing appearances across KAN-MAU, KAS-MAU, MAU and MAS |
| Exact file + interval groups | 397 | Distinct interval groups after aligned-tier duplicates are grouped |
| File + interval + raw-label events | 438 | Distinct raw-label events; one interval may have different raw labels in different tiers |
| Distinct raw strings | 22 | Unique literal forms containing `_8` |
| Files containing `_8` | 119 | CCOST TextGrid members with at least one occurrence |

Tier distribution: KAS-MAU 227; KAN-MAU 226; MAS 212; MAU 203. The most frequent strings remain `? a_8` (428), `l {:_8 p` (201), `a_8` (138), and `{:_8` (59). Do not divide 868 by 397 and call the result a rate; they are different grouping levels.

The four unresolved markers have a separate interval inventory. The previous whole-archive scan recorded `<P>` 394 appearances, `<P:>` 4, `<:p>` 22, and `<Fail>` 16. The new worklist records exact interval contexts and repeats; the marker count is not a unique-event count.

### Expert review boundary

- Text-only/canonical/phonemic label consistency can be reviewed from the supplied Thai orthographic and aligned TextGrid tiers.
- No audio is opened or supplied. The worklist cannot establish acoustic surface-tone contours, speaker-specific allophony, duration, or exact acoustic realization.
- A valid correction must cite positive cross-tier or source-convention evidence. The generic MAUS suffix range does not identify the CCOST-specific meaning of `_8`.
- Review status remains BLOCKED until two qualified independent Thai reviewers submit blind packets and a separate adjudicator records decisions. Reviewer candidates and public qualification evidence are listed in `reviewer-outreach-shortlist.md`; no one has been contacted or appointed.


## Worklist inventory reconciliation — all-tier scope (2026-11-05)

The CI worklist intentionally uses a broader scope than the earlier `inspect_ccost_textgrid.py` marker summary: it scans **every non-empty interval in every IntervalTier**, not only the declared phonetic tiers. Therefore its marker counts must not be conflated with the earlier inspector's phonetic-tier-only `bracket_marker_counts`.

The verified worklist artifact manifest reports the following independently:
- `_8`: 868 tier-level conversion failures; 397 exact file/interval groups; 438 file/interval/raw-label events; 22 distinct raw strings; 119 source files.
- All phonetic conversion failures: 1,450 tier-level occurrences. This includes `_8` and other unsupported forms; it is not a count of unique speech events.
- `<notProcessedChunk>`: 142 documented MAUS processing-failure intervals, kept separate from unknown symbols.
- Unresolved marker labels across **all tiers**: 821 intervals containing at least one marker; 871 total marker appearances. Per-marker interval counts are `<P>` 771, `<Fail>` 24, `<P:>` 4, `<:p>` 22; appearance counts are `<P>` 821, `<Fail>` 24, `<P:>` 4, `<:p>` 22. These are worklist all-tier counts. The earlier inspector counted `<P>` 394 and `<Fail>` 16 in phonetic tiers only; the two reports have different scope and are not contradictory.

The worklist preserves exact raw strings, file/tier/time provenance, overlapping labels from other tiers, adjacent same-tier context, and blank reviewer/adjudicator fields. The artifact is published as `ccost-label-adjudication-worklist` by the PR CI workflow. The generator, focused tests, exact-head CI worklist step and artifact are **DONE_VERIFIED on implementation checkpoint `47db8ac988836014663a435e08e2afe470342fe8`**: [Full CI run 42034879862](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42034879862) passed all three jobs; artifact [ccost-label-adjudication-worklist](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42034879862/artifacts/13418750385) was downloaded and inspected. It contains 1,975 rows; all 11 reviewer/adjudicator fields are blank; 868 `_8` occurrences are preserved, including `nia_8p`; `audio_members_read=0`. A subsequent workflow-only commit adds assertions for marker interval/appearance counts and is pending its own exact-head run.

No semantic interpretation is inferred for `<P>`, `<P:>`, `<:p>`, or `<Fail>`. The counts identify review targets, not meanings. `_8` is syntactically permitted by generic MAUS tone notation but unmapped in the CCOST paper's five-category scheme; its CCOST-specific meaning remains unknown.


## Exact-head continuation — cross-tier evidence and interval deduplication (2026-11-05)

This section supersedes earlier checkpoint-only statements above. The worklist and its current inventory were verified on Full CI run [42036060620](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42036060620), commit ebd1f0a55b2987c40725659b1524d26ad21abc0c. The run's test, wheel-install-smoke, and master-artifact jobs all succeeded. The test job log reports **394 passed, 1 skipped, 1,211 subtests passed**, Ruff passed, and 29 web/Python parity fixtures passed. Its uploaded worklist artifact was downloaded and inspected: 1,975 TSV rows, 488 source TextGrids, 11 expert/adjudicator fields blank, and audio_members_read=0.

### Marker inventory at three different denominators

The all-tier worklist has **821 tier-interval rows** containing at least one unresolved marker and **871 literal marker appearances**. These reduce to **398 exact file+interval groups** after aligned-tier duplicates are grouped. Per marker:

| Marker | Literal appearances | Tier-interval rows | Exact file+interval groups | Observed tier distribution |
|---|---:|---:|---:|---|
| <P> | 821 | 771 | 375 | ORT-MAU 198; KAN-MAU 198; KAS-MAU 198; TRN 177 |
| <P:> | 4 | 4 | 4 | MAS 4 |
| <:p> | 22 | 22 | 11 | MAU 11; MAS 11 (same exact intervals in both tiers) |
| <Fail> | 24 | 24 | 8 | ORT-MAU 8; KAN-MAU 8; KAS-MAU 8 (same exact intervals in all three tiers) |
| **Total** | **871** | **821** | **398** | Counts have different denominators; do not sum across columns |

The <P> appearance count exceeds its tier-interval-row count because some TRN labels contain multiple inline occurrences. The repeated aligned-tier forms of <Fail> and <:p> are evidence of structural duplication, **not proof of what the markers mean**. The generator now records per-marker unique interval-group counts and labels cross-tier context as exact_interval only when both boundaries match within 1 ns. CI asserts the group counts above.

### _8: source convention versus cross-tier evidence

Important correction: **_8 is not generically invalid MAUS syntax.** BAS's generic MAUS syntax permits numeric tone suffixes _1–_9 (not _0). The CCOST paper publishes a five-category Thai mapping only: _1 Mid, _2 Low, _3 Falling, _4 High, _5 Rising. Therefore these 868 cases are **unmapped in the published CCOST mapping**, not syntactically impossible under MAUS. Their intended CCOST-specific value remains unknown.

A new conservative exact-interval scan found **14 of the 397 _8 interval groups** with a different, mapped _1–_5 suffix in another phonetic tier at the exact same interval:

| Other tier and suffix | Exact-interval groups |
|---|---:|
| MAU _2 | 7 |
| MAS _2 | 4 |
| MAS _3 | 4 |
| KAN-MAU _3 | 1 |

This is useful review evidence, **not a correction rule**: canonical and realized tiers have different annotation roles, and exact interval coincidence alone does not establish which label is authoritative. The generator marks such context explicitly and leaves proposed_xsampa, decision, and adjudicator fields blank. CI asserts 14 groups and the tier/suffix distribution. The other 383 groups have no exact-interval mapped counterpart under this conservative test; they may still have non-exact overlapping or adjacent context.

### Audio availability and next gate

The official Zenodo record lists C-COST.zip as a **6.2 GB archive containing both WAV audio and TextGrid annotations**, under **CC BY-NC-SA 4.0**. The license permits sharing/adaptation for non-commercial purposes with attribution and the same license on derivatives. This means acoustic evidence is publicly deposited; it is not present in the owner-supplied TextGrid-only archive. Source: [CCOST Zenodo record, file inventory and license](https://zenodo.org/records/17366698).

No audio was downloaded or processed in this continuation. The web preview rejects the archive because it contains too many files, and the execution container has no outbound DNS/network access for selective range retrieval. Do not pull the entire 6.2 GB archive into routine CI. A future audio-backed review needs an opt-in, selective per-recording extraction path, a non-commercial-use check, speaker/recording metadata, time-interval registration, and a human phonetics panel. Until then, text-only canonical/cross-tier review is possible; acoustic tone-contour, duration and surface-realization claims remain blocked.

### Current acceptance status

- Marker inventory, interval grouping, exact-tier context and artifact generation: **DONE_VERIFIED** on the exact-head CI above.
- Marker semantics for <P>, <P:>, <:p>, <Fail>: **BLOCKED**; public search and the corpus paper/manual/BAS references did not define these CCOST-specific forms. Preserve verbatim.
- _8 inventory and cross-tier candidate discovery: **DONE_VERIFIED**; recovery of intended values: **BLOCKED** pending evidence-backed review. No automatic substitution.
- Independent Thai phonetic review/adjudication: **BLOCKED**; reviewer registry remains header-only, no reviewers have been contacted/appointed/consented, and independent IPA gold rows remain 0.
- Acoustic validation: **BLOCKED_PENDING_SELECTIVE_AUDIO_ACCESS_AND_NONCOMMERCIAL_SCOPE_CONFIRMATION**, not impossible: official audio exists in the licensed Zenodo archive but was not accessed.


## Latest exact-head verification — 2026-11-05 15:58 UTC

Full CI run [42039619729](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42039619729) passed on commit 43fa978d440bc654645a10430ac54962bd790582: test, wheel-install-smoke and master-artifact all SUCCESS. The test job log records **395 passed, 1 skipped, 1,211 subtests passed**, Ruff passed, and 29 web/Python parity fixtures passed. The dedicated FastThaiG2P Site API run [42039619784](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42039619784) and optional external smoke run [42039619715](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42039619715) also passed on the same HEAD.

The exact-head worklist artifact [13421040388](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42039619729/artifacts/13421040388) was downloaded and independently inspected: 1,975 records from 488 TextGrid files; all 11 reviewer/adjudicator fields blank; no audio member read. The manifest asserts 868 _8 tier occurrences, 397 _8 exact interval groups, 438 file/interval/raw-label events, 22 raw strings, 119 files; 14 exact-interval mapped-tone counterpart groups; 821 marker-bearing tier intervals, 871 marker appearances and 398 unique marker interval groups; 142 documented notProcessedChunk intervals. The per-marker group counts are <P> 375, <P:> 4, <:p> 11 and <Fail> 8. The downloaded TSV independently reproduces the 14-group counterpart distribution: MAU _2 7; MAS _2 4; MAS _3 4; KAN-MAU _3 1.

The added exact-interval relation and deduplicated summary counters are now DONE_VERIFIED on this exact HEAD. This remains inventory/context evidence only: no label is auto-corrected, no marker meaning is asserted, and no reviewer fields are populated.
