# User-supplied TextGrid archive inventory — 2026-11-05

**Status:** complete structural inventory of both supplied ZIPs; no audio members were read or extracted. This is a text/annotation inventory, not a linguistic validation or gold-data promotion.

## Safety and provenance boundary

- The archives were supplied by the repository owner on `docs/repository-audit-2026-11-04`.
- The CI inspector reads ZIP central-directory metadata and only the bytes of members ending in `.TextGrid`. It never extracts, opens, hashes or copies audio members.
- The CCOST archive contains only 488 `.TextGrid` members. The LOTUSDIS archive contains 90 `.TextGrid` members and one member without a filename extension. No member with a recognized audio extension was present in either archive.
- Git blob SHA-1 values below pin the exact files committed to this repository branch; they are not upstream publisher checksums and do not prove that the user-supplied exports are byte-identical to a publisher's archive.

## Archive inventory

| Archive in repository | Git blob SHA-1 | ZIP bytes | File members | TextGrid members | Parsed | Uncompressed TextGrid bytes | Audio members |
|---|---|---:|---:|---:|---:|---:|---:|
| `CCOST textgrid.zip` | `3b1e3978c2b3a232dce4fdcfd137bb572ce5467f` | 18,376,603 | 488 | 488 | 488 | 149,676,102 | 0 |
| `nectecLOTUSDIS textgrid.zip` | `50518e9a54e0986935e7b1cff122eb43c0b9edbd` | 1,527,911 | 91 | 90 | 90 | 8,245,774 | 0 |

All 578 TextGrid files parse with the repository's Praat long-text reader after adding support for multiline quoted interval labels and doubled-quote escaping. The one LOTUSDIS member without an extension is counted as non-TextGrid metadata and is not read by the inspector.

## CCOST: observed release tiers and adapter status

The LREC 2026 paper documents six annotation roles: ORT (orthographic word), KAN (canonical word pronunciation), KAS (canonical syllabified pronunciation), MAU (phonetic segment), MAS (phonemic syllable), and TRN (orthographic utterance transcript). It specifies X-SAMPA for phonemic/phonetic labels and only five tone suffixes: `_1` Mid, `_2` Low, `_3` Falling, `_4` High, `_5` Rising.

The supplied release files use these actual tier names:

| Observed tier | Non-empty labels | Current interpretation |
|---|---:|---|
| `ORT-MAU` | 133,344 | Orthographic-word tier; provisional alias of published ORT |
| `KAN-MAU` | 133,338 | Canonical word pronunciation; provisional alias of published KAN |
| `KAS-MAU` | 133,340 | Canonical syllabified pronunciation; provisional alias of published KAS |
| `MAU` | 445,723 | Phone-level surface tier |
| `MAS` | 195,288 | Phonemic syllable tier |
| `TRN` | 12,090 | Orthographic utterance transcript |

The `-MAU` alias mapping is grounded in the observed tier labels and the published tier descriptions, but it is still a **provisional project mapping** pending curator confirmation. The code recognizes `KAN-MAU` and `KAS-MAU` as phonetic inputs, `ORT-MAU` as orthographic, and preserves the exact raw tier name in provenance.

Current deterministic conversion counts after alias support:

| Tier | Successfully converted labels |
|---|---:|
| `KAN-MAU` | 130,080 |
| `KAS-MAU` | 130,076 |
| `MAS` | 153,103 |
| `MAU` | 403,487 |

There are **1,002 remaining unsupported labels** across the four phonetic tiers. The largest groups contain `_8` suffixes (for example `? a_8`, `a_8`, `l {:_8 p`, `{:_8`), which are not part of the published `_1`–`_5` tone mapping. Other outliers include `r/`, Unicode IPA-looking forms such as `ɹ`, `ɾ`, `tʃ`, `ʔ`, and a Thai-script token. These are deliberately not guessed or silently normalized.

Angle-bracket annotation/control tokens are excluded from X-SAMPA conversion and counted separately; their original labels remain in the source TextGrid. The paper explicitly identifies `<usb>` as a disfluency label and `<p :>` as a pause label. Other observed markers (for example `<nib>`, `<notProcessedChunk>`, `<Fail>`, and `<P>`) are retained as opaque markers until their exact release-specific semantics are confirmed.

**Interpretation:** CCOST is now an accessible, parseable primary phonetic-text candidate. It is not yet a complete converter input and its source labels are not independent project gold. No Ukrainian output or accuracy claim is promoted from this inventory.

## LOTUSDIS: transcript-only role

All 90 supplied TextGrid files parse. Each parsed file contains one interval tier named with a recording/session identifier (for example, `Hijack_S..._T..._Con123`). The tier contains time-aligned conversational transcript intervals with speaker-related and annotation markers. The archive does not expose phone, phoneme, toneme, IPA or X-SAMPA tiers.

The official LOTUSDIS dataset card describes sentence text, speaker ID, microphone ID and duration alongside audio, and declares CC BY-SA 4.0. The supplied TextGrid export is therefore classified as **orthographic conversational transcript context only**: useful for vocabulary, disfluencies, code-switching and robustness analysis, but not a phonetic gold source.

## Verification

Exact-head CI on implementation commit `9214e7a03c3fbd8652e705f7d027197bba644c7f`:

- Python: **383 passed, 1 skipped, 1,206 subtests passed**.
- Ruff: passed.
- Wheel-install smoke: passed.
- Master artifact: passed.
- FastThaiG2P Site API: passed.
- Optional external Thai G2P smoke: passed.
- TextGrid archive inspection artifact: `textgrid-archive-inspection` (CI run 42011279020).

The one skipped test is the optional FastAPI-dependent test in the generic Python test environment; the dedicated site API workflow passed.

## Task ledger

| Task | Status | Evidence / remaining acceptance |
|---|---|---|
| Inventory supplied ZIPs without audio | DONE_VERIFIED | 488 CCOST + 90 LOTUSDIS TextGrid members; zero recognized audio members |
| Parse actual TextGrid files | DONE_VERIFIED | 578/578 parse after multiline quoted-label support |
| LOTUSDIS source role | DONE_VERIFIED | Transcript-only interval tiers; no phonetic tiers observed |
| CCOST `-MAU` tier aliases | PARTIAL | Implemented from observed data and published tier roles; curator confirmation still desirable |
| CCOST X-SAMPA coverage | PARTIAL | 1,002 labels remain unsupported; preserve and review, do not guess |
| Independent phonetic IPA gold | BLOCKED | Requires two qualified independent Thai reviewers and separate adjudication; current gold rows remain 0 |
| Audio acquisition/acoustic validation | DEFERRED / OUT OF SCOPE | Explicit owner decision |
| Global TIMIT Thai | DEFERRED / EXCLUDED | Explicit owner decision; do not pursue LDC access |

## Primary references

- [CCOST Zenodo record](https://zenodo.org/records/17366698), DOI 10.5281/zenodo.17366698.
- [Pittayaporn et al., “The Chulalongkorn Corpus of Spoken Thai”, LREC 2026](https://aclanthology.org/2026.lrec-1.247/).
- [NECTEC LOTUSDIS dataset card](https://huggingface.co/datasets/nectec/LOTUSDIS), license CC BY-SA 4.0.
- [Tipaksorn et al., “LOTUSDIS: A Thai far-field meeting corpus for robust conversational ASR”](https://arxiv.org/abs/2509.18722).
