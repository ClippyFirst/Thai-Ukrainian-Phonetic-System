# User-supplied TextGrid archive inventory — 2026-11-05

**Status:** DONE_VERIFIED for structural parsing and the explicit orthographic JSONL export. This is a source-annotation inventory, not linguistic validation or gold-data promotion.

## Safety and provenance boundary

- Both archives were supplied by the repository owner on `docs/repository-audit-2026-11-04`.
- CI reads ZIP central-directory metadata and only bytes of `.TextGrid` members. It never extracts, opens, hashes or copies audio members.
- `CCOST textgrid.zip` contains 488 `.TextGrid` members and no other members. `nectecLOTUSDIS textgrid.zip` contains 90 `.TextGrid` members plus one `textgrid/.DS_Store` entry (6,148 uncompressed bytes), which is skipped without reading its contents. No recognized audio-extension member is present in either archive.
- Git blob SHA-1 values pin the exact files committed to this branch; they are not upstream publisher checksums and do not prove byte identity with an upstream release archive.

## Archive inventory

| Archive | Git blob SHA-1 | ZIP bytes | Members | TextGrid members | Parsed | TextGrid bytes uncompressed | Other members skipped |
|---|---|---:|---:|---:|---:|---:|---:|
| `CCOST textgrid.zip` | `3b1e3978c2b3a232dce4fdcfd137bb572ce5467f` | 18,376,603 | 488 | 488 | 488 | 149,676,102 | 0 |
| `nectecLOTUSDIS textgrid.zip` | `50518e9a54e0986935e7b1cff122eb43c0b9edbd` | 1,527,911 | 91 | 90 | 90 | 8,245,774 | 1 `.DS_Store` |

All 578/578 TextGrid files parse with the Praat long-text reader, including multiline quoted labels and doubled-quote escaping. The 488 CCOST files match the total number of recording files summed from Table 1 of the LREC 2026 paper. The LOTUSDIS `.DS_Store` entry is metadata by filename and was not read.

## CCOST: observed release tiers and adapter status

The LREC 2026 paper documents ORT (orthographic word), KAN (canonical word pronunciation), KAS (canonical syllabified pronunciation), MAU (phonetic segment), MAS (phonemic syllable), and TRN (orthographic utterance transcript). It specifies X-SAMPA for phonemic/phonetic labels and only five tone suffixes: `_1` Mid, `_2` Low, `_3` Falling, `_4` High, `_5` Rising.

| Observed tier | Non-empty labels | Current interpretation |
|---|---:|---|
| `ORT-MAU` | 133,344 | Orthographic-word tier; provisional alias of published ORT |
| `KAN-MAU` | 133,338 | Canonical word pronunciation; provisional alias of published KAN |
| `KAS-MAU` | 133,340 | Canonical syllabified pronunciation; provisional alias of published KAS |
| `MAU` | 445,723 | Phone-level surface tier |
| `MAS` | 195,288 | Phonemic syllable tier |
| `TRN` | 12,090 | Orthographic utterance transcript |

The `-MAU` alias mapping is a provisional project decision based on the observed release tier names and the paper's tier roles; curator confirmation is still desirable. Exact raw tier names remain in provenance.

Successfully converted source-label counts:

| Tier | Converted labels |
|---|---:|
| `KAN-MAU` | 130,080 |
| `KAS-MAU` | 130,076 |
| `MAS` | 153,103 |
| `MAU` | 403,487 |

After tightening marker recognition to accept only labels consisting entirely of angle-bracket tags, **1,014 labels remain unsupported** across the four phonetic tiers. The previous 1,002 count was superseded: 12 mixed tag-plus-Thai-text labels had been incorrectly treated as tag-only markers. They are now surfaced as unsupported instead of silently discarded.

The largest unsupported groups include `? a_8` (144 occurrences each in KAN-MAU, KAS-MAU and MAS), `a_8` (137 in MAU), `l {:_8 p`, `{:_8`, and `r/`. Other outliers include Unicode IPA-looking forms (`ɹ`, `ɾ`, `tʃ`, `ʔ`) and a Thai-script token. The CCOST paper defines only `_1`–`_5`; `_8` is not guessed as a sixth lexical tone. Unicode IPA-looking labels and unusual ASCII sequences are not silently normalized.

Pure tag-only labels are counted separately as opaque markers. The paper explicitly identifies `<usb>` as a disfluency label and `<p :>` as a pause label; other tags (for example `<nib>`, `<notProcessedChunk>`, `<Fail>` and `<P>`) are preserved as opaque until their exact release-specific semantics are confirmed. Mixed tag-plus-transcript labels are not treated as markers.

**Interpretation:** CCOST is an accessible and structurally parseable primary phonetic-text candidate. The X-SAMPA adapter remains PARTIAL, and source labels are not independent project gold. No Ukrainian output or accuracy claim is promoted from this inventory.

## LOTUSDIS: transcript-only role

All 90 supplied TextGrid files parse. Each has one recording-named IntervalTier (for example `Hijack_S..._T..._Con123`) containing time-aligned conversational transcript intervals. There are 32,943 non-empty transcript intervals. No phone, phoneme, toneme, IPA or X-SAMPA tiers were observed.

The official LOTUSDIS dataset card declares CC BY-SA 4.0 and describes sentence text, speaker ID, microphone ID and duration alongside audio. The supplied TextGrid intervals are orthographic conversational context only—useful for vocabulary, disfluencies, code-switching and orthographic robustness, but not phonetic gold.

## Explicit orthographic export

`scripts/export_textgrid_text.py` exports only explicitly selected orthographic tiers, preserving raw text, interval bounds, source file, tier, source version, archive Git blob SHA-1, license, attribution and `SOURCE_ANNOTATED_NOT_GOLD` evidence grade.

CI executed:

    python scripts/export_textgrid_text.py "CCOST textgrid.zip" "nectecLOTUSDIS textgrid.zip" --tier ORT-MAU --tier TRN --tier-prefix Hijack_ --output /tmp/textgrid-orthographic-text.jsonl

Verified output: **178,377 records** — 145,434 CCOST (`ORT-MAU` + `TRN`) and 32,943 LOTUSDIS transcript intervals. The JSONL is temporary in CI/local output and is not committed as derived corpus data. No audio is read; no gold is promoted.

## Exact-head verification

On implementation checkpoint `1dc252c517343fd6277badaa1625c095bd3a63d9`: [CI run 42014178666](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42014178666) passed all jobs.

- Python: **385 passed, 1 skipped, 1,206 subtests passed**.
- Ruff: passed.
- Wheel-install smoke: passed.
- Master artifact: passed.
- Actual TextGrid inspection: 578/578 parse; no file-level parse errors.
- Actual orthographic export: 178,377 rows; source counts and license/evidence metadata assertions passed.
- FastThaiG2P Site API: [42014178630](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42014178630) passed.
- Optional external Thai G2P smoke: [42014178504](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42014178504) passed.
- The one skipped test is optional FastAPI-dependent coverage in the generic Python test environment; the dedicated Site API workflow passed.

## Task ledger

| Task | Status | Evidence / remaining acceptance |
|---|---|---|
| Inventory supplied ZIPs without reading audio | DONE_VERIFIED | 488 CCOST + 90 LOTUSDIS TextGrid members; one `.DS_Store` metadata member skipped |
| Parse supplied TextGrid files | DONE_VERIFIED | 578/578 parse; long-text only |
| Export selected orthographic transcript intervals | DONE_VERIFIED | 178,377 provenance-rich JSONL records in CI; output not committed |
| LOTUSDIS source role | DONE_VERIFIED for supplied sample | Transcript-only interval tiers; no phonetic tiers observed |
| CCOST `-MAU` tier aliases | PARTIAL | Implemented provisional mapping; curator confirmation desirable |
| CCOST X-SAMPA coverage | PARTIAL | 1,014 labels unsupported; preserve and review, do not guess |
| Independent phonetic IPA gold | BLOCKED | Requires two qualified independent Thai reviewers and separate adjudication; current gold rows 0 |
| Audio acquisition/acoustic validation | DEFERRED / OUT OF SCOPE | Explicit owner decision |
| Global TIMIT Thai | DEFERRED / EXCLUDED | Explicit owner decision; do not pursue LDC access |

## License notices and primary references

- File-specific attribution and license terms: [third-party corpus notices](../data/THIRD-PARTY-CORPUS-NOTICES.md).
- [CCOST Zenodo record](https://zenodo.org/records/17366698), DOI 10.5281/zenodo.17366698.
- [Pittayaporn et al., “The Chulalongkorn Corpus of Spoken Thai”, LREC 2026](https://aclanthology.org/2026.lrec-1.247/).
- [NECTEC LOTUSDIS dataset card](https://huggingface.co/datasets/nectec/LOTUSDIS), license CC BY-SA 4.0.
- [Tipaksorn et al., “LOTUSDIS: A Thai far-field meeting corpus for robust conversational ASR”](https://arxiv.org/abs/2509.18722).