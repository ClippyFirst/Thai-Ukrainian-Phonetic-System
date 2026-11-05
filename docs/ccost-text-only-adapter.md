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

## Run against curator-supplied files

After obtaining and locally storing only TextGrid text files under the CC BY-NC-SA 4.0 terms:

    python scripts/inspect_ccost_textgrid.py /path/to/textgrids --output /tmp/ccost-textgrid-report.json

The script reports tier names, interval counts, a small sample of labels, successful conversion counts and unsupported labels. It does not bundle source files or output a gold dataset. If the archive uses Praat short-text or binary TextGrid, this parser will fail closed; add a separately tested reader only after confirming the actual encoding.

## Verification and acceptance gates

- Automated tests cover standard X-SAMPA multi-character tokens, Thai-relevant symbols, aspiration, vowel length, tone suffixes, syllable boundaries, unknown-symbol rejection, TextGrid tier extraction and the IPA → Ukrainian provisional adapter.
- CI can verify converter behavior on synthetic fixtures. It cannot establish compatibility with actual CCOST TextGrids until a lawful text-only sample is obtained and inspected.
- Before promoting any corpus record: pin Zenodo version and source file hash; record tier and interval; preserve raw X-SAMPA; convert deterministically; retain tone/length/boundaries; independently review a stratified sample; keep source annotations separate from adjudicated gold.
- MAU phone intervals must not be treated as a phonemic syllable. MAS is the phonemic syllable tier. KAS is canonical syllabified pronunciation. KAN is canonical word pronunciation. Do not merge them without an explicit alignment contract.

**Current status:** implementation is testable; actual CCOST TextGrid compatibility remains BLOCKED on access to text-only files / curator confirmation. Linguistic accuracy remains NOT_MEASURED; no CCOST IPA rows have been imported or promoted to gold.
