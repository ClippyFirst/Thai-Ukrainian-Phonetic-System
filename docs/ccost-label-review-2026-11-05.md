# CCOST label and marker review — 2026-11-05

## Scope and evidence

This review covers the owner-supplied `CCOST textgrid.zip` only. The inspection workflow read the 488 Praat long-text `.TextGrid` members and did not extract, open, hash, or otherwise process audio. The archived machine report is the CI artifact [textgrid-archive-inspection, run 42018381197](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42018381197/artifacts/13410038957). Its SHA-256 artifact digest is `dd3b0f263fe72e17af7d6de1e429385286140fb55d1df0b6e3ba3a33c3925cc2`.

Primary sources:
- [CCOST LREC 2026 paper, §3.3–3.4](https://aclanthology.org/2026.lrec-1.247/): explicitly identifies X-SAMPA for phonemic/phonetic representations; defines only tone suffixes `_1`–`_5`; says disfluencies are marked `<usb>` and pauses `<p:>`; describes phonetic variants at MAU level.
- [CCOST Zenodo record and manual](https://zenodo.org/records/17366698): CC BY-NC-SA 4.0 and release documentation. I extracted/search-inspected the public `CCOST_manual.pdf`: it documents the RA workflow and the CHUNKPREP → G2P → MAUS → PHO2SYL pipeline, but is not a phonetic-symbol key; the extracted text contains no `_8` or definitions for `<P>`, `<P:>`, `<:p>`, or `<Fail>`.
- [BAS Partitur Format, MAU tier](https://www.phonetik.uni-muenchen.de/Bas/BasFormatseng.html): defines generic MAU labels `<nib>` (non-speech event), `<p:>` (pause), and `<usb>` (speaker event that cannot be classified, e.g. unintelligible words). The CCOST paper is the corpus-specific source for its X-SAMPA and tone conventions.

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
| Out-of-range tone suffix `_8` | 868 | 22 | BAS supports only tone suffixes `_1`–`_5`; `_8` is invalid/out of range under the documented convention. Its intended correction is unknown; do not call it a sixth tone or map it to IPA. |
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
- The only supported BAS tone suffixes are `_1`–`_5`; the CCOST paper maps these to Mid, Low, Falling, High, and Rising. `_8` is outside the supported range and is therefore an invalid/unrecognized suffix, not a sixth tone. The intended repair (if any) remains unknown.
- `<notProcessedChunk>` is a documented MAUS processing-failure placeholder, not a phonetic value. No phonetic value is guessed for `<P>`, `<Fail>`, `<:p>`, `<P:>`, slash forms, or truncated labels.

## Acceptance and status

| Task | Status | Evidence / acceptance |
|---|---|---|
| Inspect 488 CCOST TextGrids | DONE_VERIFIED | CI parsed all 488 long-text files |
| Inventory observed tier names and counts | DONE_VERIFIED | Counts above; raw tier names preserved |
| Classify documented MAUS markers and chunk failure label | DONE_VERIFIED | CCOST paper + BAS FAQ: `<p:>`, `<usb>`, `<nib>`, `<notProcessedChunk>` |
| Separate orthography, markers, and X-SAMPA candidates | DONE_VERIFIED for the inventory | Source roles documented; mixed forms remain unsupported |
| Explain `-MAU` tier suffixes | DONE_VERIFIED | BAS tutorial explicitly defines ORT-MAU, KAN-MAU and KAS-MAU |
| Classify 868 `_8` occurrences as out-of-range suffixes | DONE_VERIFIED | BAS tutorial limits tone suffixes to `_1`–`_5`; intended correction remains unresolved and fail-closed |
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

The BAS WebServices tutorial's glossary states that tone support is limited to five stages and encodes them with `_1` through `_5`. The CCOST paper supplies the language-specific mapping for those five suffixes. Therefore every observed `_8` sequence is classifiable as an **out-of-range/invalid tone suffix under the documented BAS convention**. This resolves the question of whether `_8` is a legitimate sixth tone: it is not. It does **not** reveal which valid tone (if any) was intended in the source. Keep all 868 occurrences fail-closed; no repair or IPA conversion is justified.

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
- A valid correction must cite positive cross-tier or source-convention evidence. `_8` being out of range does not identify which valid suffix was intended.
- Review status remains BLOCKED until two qualified independent Thai reviewers submit blind packets and a separate adjudicator records decisions. Reviewer candidates and public qualification evidence are listed in `reviewer-outreach-shortlist.md`; no one has been contacted or appointed.


## Worklist inventory reconciliation — all-tier scope (2026-11-05)

The CI worklist intentionally uses a broader scope than the earlier `inspect_ccost_textgrid.py` marker summary: it scans **every non-empty interval in every IntervalTier**, not only the declared phonetic tiers. Therefore its marker counts must not be conflated with the earlier inspector's phonetic-tier-only `bracket_marker_counts`.

The latest worklist CI gate asserts the following independently:
- `_8`: 868 tier-level conversion failures; 397 exact file/interval groups; 438 file/interval/raw-label events; 22 distinct raw strings; 119 source files.
- All phonetic conversion failures: 1,450 tier-level occurrences. This includes `_8` and other unsupported forms; it is not a count of unique speech events.
- `<notProcessedChunk>`: 142 documented MAUS processing-failure intervals, kept separate from unknown symbols.
- Unresolved marker labels across **all tiers**: 821 intervals, with appearances `<P>` 821, `<Fail>` 24, `<P:>` 4, and `<:p>` 22. These are worklist all-tier counts. The earlier inspector counted `<P>` 394 and `<Fail>` 16 in phonetic tiers only; the two reports have different scope and are not contradictory.

The worklist preserves exact raw strings, file/tier/time provenance, overlapping labels from other tiers, adjacent same-tier context, and blank reviewer/adjudicator fields. The artifact is published as `ccost-label-adjudication-worklist` by the PR CI workflow. Its generator and tests are **PARTIAL_PENDING_EXACT_HEAD_CI** until the exact latest PR-head run succeeds and the uploaded artifact is inspected. Do not mark the worklist verified based only on the presence of code or a workflow step.

No semantic interpretation is inferred for `<P>`, `<P:>`, `<:p>`, or `<Fail>`. The counts identify review targets, not meanings. `_8` remains out-of-range under the documented five-tone convention; intended original values remain unknown.
