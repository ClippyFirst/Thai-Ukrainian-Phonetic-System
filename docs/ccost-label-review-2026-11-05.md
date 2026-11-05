# CCOST label and marker review — 2026-11-05

## Scope and evidence

This review covers the owner-supplied `CCOST textgrid.zip` only. The inspection workflow read the 488 Praat long-text `.TextGrid` members and did not extract, open, hash, or otherwise process audio. The archived machine report is the CI artifact [textgrid-archive-inspection, run 42018381197](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42018381197/artifacts/13410038957). Its SHA-256 artifact digest is `dd3b0f263fe72e17af7d6de1e429385286140fb55d1df0b6e3ba3a33c3925cc2`.

Primary sources:
- [CCOST LREC 2026 paper, §3.3–3.4](https://aclanthology.org/2026.lrec-1.247/): explicitly identifies X-SAMPA for phonemic/phonetic representations; defines only tone suffixes `_1`–`_5`; says disfluencies are marked `<usb>` and pauses `<p:>`; describes phonetic variants at MAU level.
- [CCOST Zenodo record and manual](https://zenodo.org/records/17366698): CC BY-NC-SA 4.0 and release documentation. The downloadable RA manual is a workflow guide; it does not provide a complete phonetic-symbol dictionary for every observed label.
- [BAS Partitur Format, MAU tier](https://www.phonetik.uni-muenchen.de/Bas/BasFormatseng.html): defines generic MAU labels `<nib>` (non-speech event), `<p:>` (pause), and `<usb>` (speaker event that cannot be classified, e.g. unintelligible words). The CCOST paper is the corpus-specific source for its X-SAMPA and tone conventions.

## Observed release tier names

All 488 files parsed. The release uses six non-empty tier names:

| Observed tier | Non-empty labels | Interpretation |
|---|---:|---|
| `ORT-MAU` | 133,344 | Orthographic tier; mapping to published ORT is provisional |
| `KAN-MAU` | 133,338 | Canonical word-pronunciation tier; mapping to published KAN is provisional |
| `KAS-MAU` | 133,340 | Canonical syllabified-pronunciation tier; mapping to published KAS is provisional |
| `MAU` | 445,723 | Phone-level phonetic segmentation |
| `MAS` | 195,288 | Phonemic syllable tier |
| `TRN` | 12,090 | Orthographic utterance transcript |

The suffix `-MAU` is confirmed as part of the supplied file's tier names, but neither the paper nor the inspected RA manual defines its exact semantics. The three aliases therefore remain a project mapping, not a curator-confirmed equivalence. Preserve the raw tier names and do not normalize them destructively.

## Exact failure inventory

The inspector recorded **1,014 failed conversion occurrences**, representing **116 distinct raw label strings**. Occurrences are tier-level failures; the same interval/label may appear in multiple tiers, so 1,014 is not a count of unique underlying speech events.

| Failure class | Occurrences | Distinct raw strings | Interpretation / action |
|---|---:|---:|---|
| Undocumented `_8` sequence | 868 | 22 | Not among CCOST's documented `_1`–`_5` tone suffixes. Do not call it a sixth tone or map it to IPA. |
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
| `<notProcessedChunk>` | 142 | **Unresolved**; do not assume it is a phonetic segment or a harmless control marker |
| `<:p>` | 22 | **Unresolved variant**; not normalized to `<p:>` without evidence |
| `<Fail>` | 16 | **Unresolved**; no failure semantics inferred |
| `<P:>` | 4 | **Unresolved**; case-sensitive distinct marker |
| `<usb><usb>` | 2 | Repeated marker sequence; preserve raw |
| `<p:><p:>` | 2 | Repeated marker sequence; preserve raw |

Only tag-only labels made exclusively of a documented marker may be classified as non-phonetic markers. Mixed forms such as `m O:_1<usb>`, `<usb>v`, `n<p:>`, `<p:>z`, and marker-plus-Thai transcript strings are not silently stripped or partially converted.

## What is and is not IPA

- The paper says the phonemic and phonetic tiers use **X-SAMPA**, not IPA. A successful conversion is a derived IPA candidate, with provenance, not a source IPA annotation.
- `ORT-MAU` and `TRN` are orthographic/text tiers. Their Thai-script content is not IPA.
- `MAU` is phone-level; `MAS` is phonemic/syllabic. They must not be conflated.
- Unicode IPA-looking characters in failed labels are not automatically passed through as IPA. The label may be mixed, corrupted, or use another convention.
- The only source-documented tone suffixes are `_1` Mid, `_2` Low, `_3` Falling, `_4` High, and `_5` Rising. `_8` stays unresolved.
- No phonetic value is guessed for `<P>`, `<Fail>`, `<notProcessedChunk>`, `<:p>`, `<P:>`, slash forms, or truncated labels.

## Acceptance and status

| Task | Status | Evidence / acceptance |
|---|---|---|
| Inspect 488 CCOST TextGrids | DONE_VERIFIED | CI parsed all 488 long-text files |
| Inventory observed tier names and counts | DONE_VERIFIED | Counts above; raw tier names preserved |
| Classify documented MAUS markers | DONE_VERIFIED | CCOST paper + BAS format definitions |
| Separate orthography, markers, and X-SAMPA candidates | DONE_VERIFIED for the inventory | Source roles documented; mixed forms remain unsupported |
| Explain every `-MAU` alias | BLOCKED | Requires corpus curator confirmation |
| Resolve 868 `_8` occurrences | BLOCKED | No source definition; curator/manual clarification required |
| Resolve remaining 146 failed occurrences | PARTIAL/BLOCKED | 116 raw strings inventoried; specialist/curator review required |
| Promote converted labels to IPA gold | BLOCKED | Independent Thai review and adjudication still required |

**Do not promote any of these 1,014 occurrences to IPA or phoneme output.** The current adapter remains a conservative, partial candidate converter; source annotations are not independent gold and linguistic accuracy remains `NOT_MEASURED`.
