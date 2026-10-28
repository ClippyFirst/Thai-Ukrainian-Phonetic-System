# Thai romanization integration research

**Status:** PARTIAL / ENGINEERING CI PASS — the offline browser port, reviewed correction layer and pinned-reference parity test pass in CI. Full tokenizer parity and website visual/deployment review are still open.

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

The upstream algorithm is a useful reference, not a complete standards implementation. A focused output review exposed predictable rule-engine failures, so ClippyFirst applies a small, source-attested correction layer rather than treating every upstream output as authoritative.

| Input | ClippyFirst RTGS output | Evidence / reason |
|---|---|---|
| `จริง` | `ching` | UK BGN/PCGN Thai romanization reference documents the conventional `จริง → ching` form. |
| `สามารถ` | `samat` | UK BGN/PCGN reference documents the conventional form. |
| `สวัสดี` | `sawatdi` | Royal Institute romanization: [Thai Wiktionary entry](https://th.wiktionary.org/wiki/สวัสดี). |
| `พัฒนา` | `phatthana` | Royal Institute romanization: [Thai Wiktionary entry](https://th.wiktionary.org/wiki/พัฒนา). |
| `ฤทธิ์` | `rit` | Royal Institute romanization: [Thai Wiktionary entry](https://th.wiktionary.org/wiki/ฤทธิ์). |
| `ฤๅ` | `rue` | Royal Institute romanization: [Thai Wiktionary entry](https://th.wiktionary.org/wiki/ฤๅ). |
| `อักษร` | `akson` | Royal Institute romanization: [Thai Wiktionary entry](https://th.wiktionary.org/wiki/อักษร). |
| `ยูเครน` | `yukhren` | Royal Institute romanization: [Thai Wiktionary entry](https://th.wiktionary.org/wiki/ยูเครน). |
| `ทราบ` / `ทรัพย์` / `แทรก` | `sap` / `sap` / `saek` | Word-level Royal Institute forms: [ทราบ](https://th.wiktionary.org/wiki/ทราบ), [ทรัพย์](https://th.wiktionary.org/wiki/ทรัพย์), [แทรก](https://th.wiktionary.org/wiki/แทรก). Unknown initial `ทร` tokens abstain rather than extrapolate. |
| `รถไฟ` | `rotfai` | Reviewed word-level RTGS form: [ThaiRoots reference](https://www.thairoots.com/). |
| `ผลไม้` | `phonlamai` | Royal Institute form for `น้ำผลไม้` is `nam-phon-la-mai`; see [Thai Wiktionary entry](https://th.wiktionary.org/wiki/น้ำผลไม้). |
| `ใหม่` / `ไหม` / `เหงา` / `ให้` | `mai` / `mai` / `ngao` / `hai` | ClippyFirst correction for preposed vowels in `ห นำ` clusters; compare [W3C Thai Layout Requirements](https://www.w3.org/TR/2026/DNOTE-thai-lreq-20260315/) and [r12a Thai script notes](https://r12a.github.io/scripts/thai/block.html). |
| `ใกล้` / `ใคร` | `klai` / `khrai` | Added the two-consonant `ใ**` pattern, analogous to the existing `ไ**` pattern; the vowel is not allowed to swallow the onset cluster. |

These lexical/orthographic corrections are separately tested; they are not counted as exact parity with PyThaiNLP. The project-maintained correction list is intentionally finite and does not imply standards-level completeness.

The following cases explicitly abstain instead of producing a plausible-looking but unsupported result: unreviewed initial `ทร` tokens (e.g. `ทราย`), repetition/abbreviation marks `ๆ` and `ฯ`, unsupported letter `ฦ`, and the unreviewed long proper-name token `สตรีเศรษฐบุตรบำเพ็ญ`.

## Parity corpus and what it proves

`docs/research/rtgs-parity-corpus.json` contains 60 normal token inputs, five explicit abstention cases and pre-segmented token sequences. `scripts/test_rtgs_parity.py` compares the browser implementation with private per-token `_romanize` and `_should_add_syllable_separator` functions from pinned PyThaiNLP 5.4.0, except the 19 documented correction cases which are checked against their reviewed outputs.

**Verified on commit `e3bbdf285f95d835bc1e9674dce11b6780e564f2`:**
- `node web/tests/rtgs-reference.test.mjs` — PASS.
- `python scripts/test_rtgs_parity.py` — PASS.
- Full repository CI run [40683075009](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40683075009) — PASS.
- Web static validation [40683074832](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40683074832) — PASS.

This verifies implementation parity for the declared inputs and the repository's existing CI suite, not:
- parity with PyThaiNLP's `newmm` tokenizer/dictionary or full `romanize(text)`;
- correctness for every Thai sentence or proper name;
- independent Thai IPA adjudication or Ukrainian target-transcription accuracy.

The website uses ClippyFirst's token boundaries. Phrase spacing and separator behavior can therefore differ from PyThaiNLP's full text API. The UI states this limitation.

## Acceptance gates

1. [x] Pin upstream source and include license attribution.
2. [x] Implement an offline browser adapter, separated from IPA → Ukrainian.
3. [x] Add reviewed lexical/orthographic corrections and explicit abstentions for unsupported cases.
4. [x] Add 60-token parity corpus and CI comparison against pinned PyThaiNLP 5.4.0.
5. [x] Focused RTGS tests, full repository CI and static validation pass on the implementation commit.
6. [ ] Complete a browser visual review and confirm the deployed website behavior before promoting the feature out of draft.
7. [ ] Decide whether to bundle a Thai word tokenizer/dictionary only after separate browser compatibility, provenance and license review.

## Remaining independent research gaps

- Independent Thai IPA adjudication and Ukrainian target-form review remain separate research requirements; RTGS parity does not resolve them.
- If full PyThaiNLP behavior is required, tokenizer and dictionary provenance/licensing must be inspected separately and parity measured on a reviewed sentence corpus.
- No general accuracy claim should be inferred from passing algorithm parity.
