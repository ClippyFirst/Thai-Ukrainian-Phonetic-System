# Thai romanization integration research

**Status:** DONE_VERIFIED for the RTGS implementation and deployment; PARTIAL for linguistic coverage. Exact-head CI, static validation and post-deploy Pages checks passed. Full PyThaiNLP tokenizer/dictionary parity, manual browser visual review and independent linguistic gold remain open.

## Decision and pipeline boundary

RTGS (Royal Thai General System of Transcription) is displayed as a parallel Latin reference, never as input to Ukrainian adaptation. The main route remains:

`Thai orthography → structural analysis → source phonology → IPA/typed result → Ukrainian adaptation → Ukrainian practical orthography`

RTGS is lossy: it does not encode tone and does not reliably preserve vowel length or all phonemic distinctions. It is not English pronunciation spelling. RTGS `ph`, `th`, and `kh` represent aspirated Thai stops, not English /f/, /θ/, or English letter-name values.

ISO 11940 is a separate reversible orthographic transliteration scheme, not pronunciation transcription. If added later, it must have its own explicitly orthographic panel.

## Implementation and provenance

- Upstream: PyThaiNLP `v5.4.0`, `pythainlp/transliterate/royin.py`, immutable release commit `7f26adf5ce09c3d77c39ca2ef86f7138e9071088`.
- Source: https://github.com/PyThaiNLP/pythainlp/blob/v5.4.0/pythainlp/transliterate/royin.py
- API docs: https://pythainlp.org/docs/5.4.0/api/transliterate.html
- License: Apache-2.0; attribution and license text are in `THIRD_PARTY_NOTICES.md` and `licenses/Apache-2.0-PyThaiNLP.txt`.
- The browser implementation ports per-token vowel rules, consonant mapping, normalization, `รร` handling and the upstream syllable-separator rule.
- The site has no runtime Python dependency, model download, API call or network request. PyThaiNLP 5.4.0 is a CI-only oracle.

## Reviewed correction layer and abstentions

The upstream algorithm is a useful reference, not a complete standards implementation. A focused output review exposed predictable rule-engine failures, so ClippyFirst applies a finite, source-backed correction layer rather than treating every upstream output as authoritative.

| Input | ClippyFirst RTGS output | Evidence / reason |
|---|---|---|
| `จริง` / `สามารถ` | `ching` / `samat` | UK BGN/PCGN Thai romanization reference documents these conventional forms. |
| `สร้าง` / `ศรี` / `เศร้า` / `ไซร้` | `sang` / `si` / `sao` / `sai` | Royal Institute discussion of non-compositional clusters: https://www.orst.go.th/FILEROOM/CABROYINWEB/DRAWER004/GENERAL/DATA0000/00000630.FLP/html/49/ |
| `ทรง` / `ทราม` / `ทราบ` / `ทรัพย์` / `แทรก` | `song` / `sam` / `sap` / `sap` / `saek` | Same Royal Institute lexical-scope reference; `ทราม` is additionally pinned to English Wiktionary revision 88637433 (`/saːm˧/`, CC BY-SA 4.0): https://en.wiktionary.org/w/index.php?title=ทราม&oldid=88637433. These are lexical cases, not a productive `ทร → s` rule. |
| `สวัสดี` / `พัฒนา` / `ฤทธิ์` / `ฤๅ` / `อักษร` / `ยูเครน` | `sawatdi` / `phatthana` / `rit` / `rue` / `akson` / `yukhren` | Word-level Royal Institute romanization fields: [สวัสดี](https://th.wiktionary.org/wiki/สวัสดี), [พัฒนา](https://th.wiktionary.org/wiki/พัฒนา), [ฤทธิ์](https://th.wiktionary.org/wiki/ฤทธิ์), [ฤๅ](https://th.wiktionary.org/wiki/ฤๅ), [อักษร](https://th.wiktionary.org/wiki/อักษร), [ยูเครน](https://th.wiktionary.org/wiki/ยูเครน). |
| `รถไฟ` / `ผลไม้` | `rotfai` / `phonlamai` | Word-level forms: [รถไฟ](https://th.wiktionary.org/wiki/รถไฟ); Royal Institute form for `น้ำผลไม้` is `nam-phon-la-mai`: https://th.wiktionary.org/wiki/น้ำผลไม้. |
| `ใหม่` / `ไหม` / `เหงา` / `ให้` | `mai` / `mai` / `ngao` / `hai` | ClippyFirst correction for preposed vowels in `ห นำ` clusters; compare [W3C Thai Layout Requirements](https://www.w3.org/TR/2026/DNOTE-thai-lreq-20260315/) and [r12a Thai script notes](https://r12a.github.io/scripts/thai/block.html). |
| `ใกล้` / `ใคร` | `klai` / `khrai` | Added the two-consonant `ใ**` pattern, analogous to the existing `ไ**` pattern, so the vowel does not swallow the onset cluster. |

These 25 lexical/orthographic corrections are separately tested; they are not counted as exact parity with PyThaiNLP. The correction list is finite and does not imply standards-level completeness.

The following cases explicitly abstain rather than produce a plausible-looking unsupported result: unreviewed initial `ทร` tokens (e.g. `ทราย`), repetition/abbreviation marks `ๆ` and `ฯ`, unsupported letter `ฦ`, and the unreviewed long proper-name token `สตรีเศรษฐบุตรบำเพ็ญ`.

## Parity corpus and evidence

`docs/research/rtgs-parity-corpus.json` contains 66 normal token inputs, five explicit abstention cases and pre-segmented token sequences. `scripts/test_rtgs_parity.py` compares the browser implementation with private per-token `_romanize` and `_should_add_syllable_separator` functions from pinned PyThaiNLP 5.4.0, except the 25 documented correction cases which are checked against their reviewed outputs.

- Focused `node web/tests/rtgs-reference.test.mjs` and `python scripts/test_rtgs_parity.py` passed in exact-head CI [40691939835](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40691939835) on `13d89d6f9b8a85b3ba85612e738a583a9c81ca0f`; both `test` and `master-artifact` jobs passed.
- Latest-head web static validation [40691940070](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40691940070) — PASS.
- RTGS Pages deployment [40692707861](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40692707861) passed and verified the published module/panel. After the public guidance update, Pages deployment [40694421367](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40694421367) also passed and verified the served homepage, system page and RTGS module.

This verifies implementation parity for declared inputs and repository regression tests, not full PyThaiNLP `newmm` tokenizer/dictionary parity, correctness for every sentence/proper name, independent Thai IPA adjudication, or Ukrainian target-transcription accuracy. The website uses ClippyFirst token boundaries; phrase spacing can differ from PyThaiNLP's full text API.

## Open PR reconciliation

- **PR #111** (`feat: pin Thai ทร lexical exception and guard ambiguity`) remains open and was not merged or cherry-picked. Its source-backed lexical cases informed only this separate RTGS correction layer; no IPA engine, text lexicon or branch changes from that PR were copied.
- **PR #112** (`docs(site): audit public guidance and evidence status`) was not merged blindly. Its homepage/system copy and UI-contract changes were ported alongside the live RTGS implementation through PR #116, merged as `f4cc4d061c529fc5aec094af896dea5aaec9378f`. The structured public-content audit register is maintained in `docs/final-audit.md`; PR #112 is now superseded and should be closed after this closeout update is merged.
- Recently merged PR #110 and earlier Thai IPA/lexicon work are preserved because this branch is based on current `main` at `d39fc9e2c40db4a9f760069099c1f45973d592c8`.

## Acceptance gates

1. [x] Pin upstream source and include license attribution.
2. [x] Implement an offline browser adapter, separated from IPA → Ukrainian.
3. [x] Add reviewed lexical/orthographic corrections and explicit abstentions for unsupported cases.
4. [x] Add 66-token parity corpus and CI comparison against pinned PyThaiNLP 5.4.0.
5. [x] Focused RTGS tests and latest-head static validation pass; latest full CI `test` job passes.
6. [x] Latest-head `master-artifact` job completes successfully (CI [40691939835](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40691939835)).
7. [x] Confirm deployed website behavior through the post-deploy contract in [40692707861](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40692707861) and [40694421367](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40694421367).
8. [ ] Complete manual browser visual review across viewport sizes/devices; automated served-content checks are not visual QA.
8. [ ] Decide whether to bundle a Thai word tokenizer/dictionary only after separate browser compatibility, provenance and license review.

## Remaining independent research gaps

- Independent Thai IPA adjudication and Ukrainian target-form review remain separate research requirements; RTGS parity does not resolve them.
- If full PyThaiNLP behavior is required, tokenizer and dictionary provenance/licensing must be inspected separately and parity measured on a reviewed sentence corpus.
- No general accuracy claim should be inferred from passing algorithm parity.
