# CCOST text-only adapter and acquisition record

**Status: PARTIAL — converter and long-text TextGrid reader implemented; CCOST release files not yet inspected.**
**Scope:** text and phonetic annotation only. No WAV is needed, downloaded, extracted, opened, or bundled.

## What is actually published

The Zenodo v1.0 record (DOI 10.5281/zenodo.17366698) publishes wordlist.csv, sentences.txt, metadata, CCOST_manual.pdf, and a single 6.2 GB C-COST.zip described as containing both WAV files and Praat TextGrid annotations. The public file list does **not** expose a separate TextGrid-only archive. Its ZIP preview reports too many files. The 206-item wordlist can be previewed independently; it is not pronunciation gold. See the [Zenodo record](https://zenodo.org/records/17366698).

The LREC 2026 paper documents these tier names and meanings:
- ORT: orthographic word
- KAN: canonical word pronunciation
- KAS: canonical syllabified pronunciation
- MAU: phonetic segment
- MAS: phonemic syllable
- TRN: orthographic utterance transcript

The paper states that phonemic and phonetic labels use X-SAMPA and that numeric tone suffixes are _1 Mid, _2 Low, _3 Falling, _4 High, _5 Rising. Figure 2 publishes an example for น่าจะ: KAN `n a:_3 c a_2`; KAS `n a:_3 . c a_2`; MAU intervals `n`, `a:_3`, `c`, `a_2`; MAS syllable labels `na:_3`, `ca_2`. These published examples are now regression fixtures; they are not a substitute for inspecting the released TextGrid files. Native Thai research assistants corrected alignment, tone and segmental accuracy; the paper reports no formal inter-annotator agreement. The published tier map is a research specification, **not proof that every released TextGrid has exactly these tier names/values**. Source: [Pittayaporn et al., LREC 2026](https://aclanthology.org/2026.lrec-1.247/).

## Acquisition decision

Do not download the 6.2 GB mixed archive merely to extract text. The owner requirement is text-only. A request for a TextGrid-only export and the precise annotation manual is prepared in docs/external-review-and-source-requests.md, but has **not been sent** because this execution has no connected email action. Public curator contacts listed by the project's official ChulaSEAL page are:
- Pittayawat Pittayaporn — Pittayawat.P@chula.ac.th
- Sujinat Jitwiriyanont — Sujinat.J@chula.ac.th

If a TextGrid-only export is unavailable, the acceptable fallback is a curator-confirmed method for streaming/selectively extracting .TextGrid members without persisting WAV bytes, with a documented license basis and a verified file manifest. Do not assume that a ZIP containing both file types automatically authorizes selective redistribution; all extracted text remains CC BY-NC-SA 4.0. Keep source files outside this repository unless the license, attribution and ShareAlike obligations are handled explicitly.

## Converter contract

src/thai_ukrainian/adapters/xsampa.py is a strict X-SAMPA → IPA converter. It:
- uses longest-token matching for multi-character X-SAMPA symbols;
- preserves aspiration, length, syllabicity, non-syllabicity and the explicitly supported diacritics;
- interprets CCOST numeric _1–_5 suffixes as tone metadata, not as standard X-SAMPA tone symbols;
- retains original raw label, per-syllable X-SAMPA, IPA, tone number and tone category;
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
