# CCOST text-only adapter and acquisition record

**Status: PARTIAL — supplied release TextGrids are structurally parsed; X-SAMPA coverage and release-tier semantics still need review.**
**Scope:** orthographic and phonetic annotations only. No WAV/audio member is present in the supplied CCOST ZIP; the CI inspector reads only `.TextGrid` members.

## Supplied archive and observed release schema

The repository owner supplied `CCOST textgrid.zip` on branch `docs/repository-audit-2026-11-04`. It contains 488 `.TextGrid` members (18,376,603 compressed bytes; 149,676,102 uncompressed TextGrid bytes); all 488 parse as Praat long-text TextGrid. The 488-file count matches the sum of recording files in Table 1 of Pittayaporn et al., LREC 2026. The branch Git blob SHA-1 is `3b1e3978c2b3a232dce4fdcfd137bb572ce5467f`; this pins the supplied branch file, not an upstream publisher checksum.

The paper describes these tier roles: ORT (orthographic word), KAN (canonical word pronunciation), KAS (canonical syllabified pronunciation), MAU (phonetic segment), MAS (phonemic syllable), and TRN (orthographic utterance transcript). The supplied release files use these exact names:

| Observed tier | Non-empty labels | Project interpretation |
|---|---:|---|
| `ORT-MAU` | 133,344 | Orthographic word tier; provisional alias of ORT |
| `KAN-MAU` | 133,338 | Canonical word pronunciation; provisional alias of KAN |
| `KAS-MAU` | 133,340 | Canonical syllabified pronunciation; provisional alias of KAS |
| `MAU` | 445,723 | Phone-level surface tier |
| `MAS` | 195,288 | Phonemic syllable tier |
| `TRN` | 12,090 | Orthographic utterance transcript |

The `-MAU` suffix is an observed release-tier naming convention. The mapping to the paper's published roles is a provisional project decision, not a confirmed statement from the curators. Preserve the raw tier names in provenance.

## Source tone and marker evidence

The LREC 2026 paper explicitly states that phonemic and phonetic labels use X-SAMPA and defines only `_1` Mid, `_2` Low, `_3` Falling, `_4` High and `_5` Rising. It reports manual correction by trained native Thai research assistants but no formal inter-annotator agreement. Generic BAS documentation describes a broader 1–9 tone-number facility; that generic facility does not override CCOST's corpus-specific five-tone mapping. Therefore observed `_8` labels are not interpreted as a sixth tone or converted by guesswork.

Actual files contain tag-only labels such as `<p:>`, `<nib>`, `<usb>`, `<notProcessedChunk>`, `<Fail>` and `<P>`. The paper explicitly documents `<usb>` for disfluencies and `<p :>` for pauses; other tags remain opaque until their release-specific meaning is confirmed. Mixed tag-plus-transcript labels are not discarded as control markers; they remain unsupported for phonetic conversion.

Other unsupported labels include Unicode IPA-looking forms (`ɹ`, `ɾ`, `tʃ`, `ʔ`), unusual ASCII sequences such as `r/`, and a Thai-script token. The paper describes phonetic variation and code-mixed items at MAU level, but it does not provide a complete conversion table for every observed label. Keep these cases fail-closed pending manual/curator evidence.

## Text-only export

To create a local JSONL containing orthographic intervals only (no phonetic tiers, no audio), run:

    python scripts/export_textgrid_text.py "CCOST textgrid.zip" --tier ORT-MAU --tier TRN --output /tmp/ccost-orthographic-text.jsonl

The exporter preserves interval times, raw label text, source file, tier, source version, CC BY-NC-SA 4.0 license, attribution and `SOURCE_ANNOTATED_NOT_GOLD` status. It does not write derived corpus rows into the repository. Keep the output under the source license and do not call it gold.

## Curator follow-up

The prior need to obtain a TextGrid-only archive is satisfied for the supplied 488-file export. A curator response is still useful to confirm the `-MAU` tier aliases and explain `_8`, non-ASCII variants and opaque markers. The prepared request in `docs/external-review-and-source-requests.md` has not been sent because no email action is connected.

Primary references: [CCOST Zenodo record](https://zenodo.org/records/17366698), [Pittayaporn et al., LREC 2026](https://aclanthology.org/2026.lrec-1.247/), and [BAS tone/X-SAMPA help](https://clarin.phonetik.uni-muenchen.de/BASWebServices/help/help_examples).
## Converter contract

src/thai_ukrainian/adapters/xsampa.py is a strict X-SAMPA → IPA converter. It:
- uses longest-token matching for multi-character X-SAMPA symbols;
- preserves aspiration, length, syllabicity, non-syllabicity and the explicitly supported diacritics;
- interprets CCOST numeric _1–_5 suffixes as tone metadata, not as standard X-SAMPA tone symbols;
- retains original raw label, per-syllable X-SAMPA, IPA, tone number and tone category;
- normalizes IPA to canonical NFD so combining phonetic diacritics remain explicit;
- treats spaces as token separators only (not inferred syllable boundaries); explicit periods and CCOST tone suffixes close syllables;
- raises XSampaConversionError for unknown symbols, malformed suffixes, non-ASCII input and unsupported notation; no best-effort substitution.

The symbol map is a declared subset of the standard X-SAMPA inventory, not an assertion that all listed symbols occur in CCOST. Mapping is grounded in Wells's X-SAMPA scheme and the [eSpeak-NG X-SAMPA reference table](https://github.com/espeak-ng/espeak-ng/blob/master/docs/phonemes/xsampa.md). The implementation intentionally omits ambiguous/context-dependent modifiers until the CCOST manual and real tier labels establish their meaning. Before using the adapter on the corpus, inspect actual MAU, MAS, KAS and KAN labels and extend the map only with source/manual evidence and tests.

src/thai_ukrainian/adapters/ccost.py reads Praat **long-text** TextGrid files and preserves tier name, interval boundaries and label text. It never accesses the paired audio. It maps KAN/KAS/MAS into provisional phonemic PhoneticResult values and preserves MAU as phone-level surface IPA that cannot directly drive syllable-level Ukrainian adaptation. Source annotations are not independently adjudicated gold.

## Run against the supplied files

The owner-supplied `CCOST textgrid.zip` is already present on this branch. Inspect its actual release tiers and labels with:

    python scripts/inspect_ccost_textgrid.py "CCOST textgrid.zip" --output /tmp/ccost-textgrid-report.json

To export orthographic word and utterance intervals only:

    python scripts/export_textgrid_text.py "CCOST textgrid.zip" --tier ORT-MAU --tier TRN --output /tmp/ccost-orthographic-text.jsonl

The inspector and exporter read only `.TextGrid` members; no WAV is required. The JSONL exporter preserves raw labels, interval bounds, source/tier, license, attribution and `SOURCE_ANNOTATED_NOT_GOLD`. Do not commit the generated data by default.

## Verification and acceptance gates

- Exact-head CI parsed all 488 supplied CCOST TextGrids and all 90 supplied LOTUSDIS TextGrids. The 488 CCOST file count matches the recording-file total in LREC 2026 Table 1.
- The supplied release uses `ORT-MAU`, `KAN-MAU`, `KAS-MAU`, `MAU`, `MAS`, `TRN`. The `-MAU` aliases are provisional project mappings; curator confirmation remains desirable.
- The declared X-SAMPA subset converts deterministically, but 1,014 phonetic-tier labels remain unsupported. `_8`, Unicode IPA-looking forms, unusual sequences and mixed tag-plus-text labels fail closed; do not infer mappings.
- Final exact-head CI [42015757949](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42015757949) passed: 385 Python tests passed, 1 skipped, 1,206 subtests; Ruff, wheel-install smoke, master-artifact, archive inspection, 178,377-record orthographic export, SHA-256 manifest validation and license-notice artifact upload passed.
- Before promoting any corpus record: pin the source version and file identity; record tier and interval; preserve raw source labels; convert deterministically; retain tone/length/boundaries; independently review a stratified sample; keep source annotations separate from adjudicated gold.
- MAU phone intervals must not be treated as a phonemic syllable. MAS is the phonemic syllable tier. KAS is canonical syllabified pronunciation. KAN is canonical word pronunciation. Do not merge them without an explicit alignment contract.

**Current status:** TextGrid structure and text-only export are DONE_VERIFIED for supplied files. CCOST `-MAU` semantics and X-SAMPA coverage remain PARTIAL pending source/curator evidence. Independent phonetic gold remains BLOCKED; linguistic accuracy remains `NOT_MEASURED`; no CCOST IPA rows have been promoted to gold.


## Evidence-based label review — 2026-11-05

A full occurrence-level review is recorded in [CCOST label and marker review](ccost-label-review-2026-11-05.md). The CI inspection report [artifact](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42018381197/artifacts/13410038957) contains the 1,014 failed conversion occurrences.

Key corrections and confirmed findings:
- The CCOST paper §3.3 explicitly identifies X-SAMPA for its phonemic/phonetic tiers and defines only `_1` Mid, `_2` Low, `_3` Falling, `_4` High, `_5` Rising. It does **not** define `_8`.
- The 1,014 failures are 1,014 tier-level occurrences and 116 distinct raw strings, not 1,014 distinct symbols. They comprise 868 `_8` cases, 58 slash/alternative forms, 26 mixed-marker cases, 17 non-ASCII phonetic-looking forms, 10 Thai/mixed text cases, 14 truncated/malformed tokens, and 21 other unsupported ASCII sequences.
- CCOST and BAS sources define `<p:>` as pause, `<usb>` as a speaker event/disfluency/unintelligible event, and `<nib>` as a non-speech event/noise. They are not IPA. `<P>`, `<P:>`, `<:p>`, `<Fail>`, and `<notProcessedChunk>` remain unresolved and distinct.
- The observed `ORT-MAU`, `KAN-MAU`, and `KAS-MAU` tier names are real, but their `-MAU` alias semantics remain provisional until confirmed by the corpus curator.
- Unicode IPA-looking forms are not accepted as IPA by appearance alone. Mixed marker-plus-phone/text labels remain raw and fail-closed.
- No parser mapping was broadened and no unsupported label was guessed. The adapter remains PARTIAL; source annotations are not gold.
