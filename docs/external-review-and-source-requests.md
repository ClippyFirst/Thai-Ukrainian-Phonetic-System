# External review and source-clarification request pack

**Status: PREPARED — NOT SENT.** This document records public institutional contact routes and copy-ready requests. No person has been contacted, consented, or registered. Do not mark a reviewer VERIFIED until qualification, conflicts, scope, consent and identity evidence are checked.

## 1. Thai phonetics and segmentation reviewers

### Recommended first-pass invitations

| Candidate | Publicly documented relevance | Public contact route | Conflict note |
|---|---|---|---|
| Chutamanee Onsuwan, Ph.D. | Thammasat profile documents a PhD dissertation on temporal relations between consonants and vowels in Thai syllables and expertise in laboratory phonetics/speech science. | [Official Thammasat faculty profile](https://arts.tu.ac.th/th/teacherlarts/cmukv6znk0052pm61l213msd6) — use its institutional contact route. | No project relationship known from the public profile; verify directly. |
| Lena Maluleem, Ph.D. | Kasetsart profile lists phonetics/phonology, prosody and experimental linguistics. | `lena.m@ku.th`; [official profile](https://ling.human.ku.ac.th/index.php/lyna_cv/). | No project relationship known from the public profile; verify directly. |
| Rungpat Roengpitya | Mahidol profile documents Standard Thai tone research and perception of Thai word-final stops; confirm whether the proposed vowel-length and segmentation scope fits current expertise. | [Official Mahidol profile](https://murex.mahidol.ac.th/en/persons/rungpat-roengpitya/). | No project relationship known from the public profile; verify directly. |

**Suggested independent pair:** invite Chutamanee Onsuwan and Lena Maluleem first, subject to their explicit confirmation of Standard Thai competence, phonemic IPA, lexical reading, word/syllable segmentation, tone and vowel-length expertise. Rungpat Roengpitya is a potential reserve or adjudicator only after confirming the exact scope. Do not infer native-speaker status or dialect competence from institutional affiliation.

### Copy-ready invitation

**Subject:** Invitation: independent blind review of Standard Thai phonetics and segmentation (research project)

Dear Dr [Surname],

I am working on a research prototype for Thai-to-Ukrainian phonetic transcription. We are preparing a small, blind evaluation set and are seeking two independent qualified reviewers, followed by a separate adjudicator.

The first-pass task is to annotate Thai lexical readings, orthographic validity, word and syllable boundaries, broad phonemic IPA, tone categories/contours, vowel length and uncertainty. The base packet contains 42 short prompts plus a separate six-item regression supplement. It contains no engine predictions or prefilled labels. We would provide the annotation guide, a separate reviewer copy, the expected time commitment and the proposed compensation/credit arrangements before any commitment.

Could you let us know whether this task falls within your expertise and whether you might be interested? If so, please indicate:
- your competence in Standard Thai and any relevant dialect scope;
- experience with Thai phonetics/phonology, IPA and segmentation;
- any conflicts of interest (including prior involvement with the project, engine or source datasets);
- availability, preferred compensation and whether you prefer named or pseudonymous acknowledgement.

Each reviewer would submit independently; the original annotations would be frozen before comparison. A third person would adjudicate disagreements. We would not expose engine output before first-pass submissions are frozen.

Thank you for considering this request.

Best regards,
[Project contact]

### Reviewer qualification and acceptance checklist

Before adding a row to `data/benchmark/reviewer-qualifications.tsv`:
1. Confirm identity and permission to retain the qualification evidence reference.
2. Record self-declared Thai proficiency, Standard Thai/dialect scope, and relevant phonetics/phonology experience.
3. Verify relevant public qualifications or publications; distinguish verified evidence from self-report.
4. Ask about prior involvement with CCOST, the project, the engine, or other reviewer submissions.
5. Agree on annotation scope, guide version, deadlines, compensation and attribution/privacy preference.
6. Issue separate blind copies. Do not share model outputs or another reviewer's labels.
7. Freeze both original submissions before any reconciliation.
8. Appoint a separate adjudicator; preserve disagreements, abstentions and written rationales.

## 2. CCOST A–D clarification request

### Public curator contacts

Zenodo lists Pittayawat Pittayaporn and Sujinat Jitwiriyanont as CCOST data curators. Chulalongkorn's official faculty pages publish these institutional contacts:
- Pittayawat Pittayaporn: `Pittayawat.P@chula.ac.th` ([official ChulaSEAL people page](https://www.arts.chula.ac.th/chulaseal/people/)).
- Sujinat Jitwiriyanont: `Sujinat.J@chula.ac.th` ([official ChulaSEAL people page](https://www.arts.chula.ac.th/chulaseal/people/)).

These are source-curator contacts, not independent reviewers for a CCOST-derived benchmark. Any review by a CCOST author must disclose that relationship and must not be counted as independent validation of CCOST's own annotations.

### Copy-ready clarification request

**Subject:** Clarification request: 206-item CCOST word list and randomized orders A–D

Dear Professor Pittayaporn and Dr Jitwiriyanont,

We are auditing the public CCOST v1.0 release (Zenodo DOI 10.5281/zenodo.17366698) for a research evaluation of Thai phonetic transcription.

The Zenodo record describes a 206-item monosyllabic word list. We verified the published `wordlist.csv` preview against its MD5 checksum (`e62f500d87b4ff8c6deb4c4595854d34`). Each of columns A, B, C and D contains 206 rows and 206 unique forms, with no within-column duplicates. However, the sets are not identical: B, C and D each differ from A by two missing and two additional forms, producing a 208-form union.

Could you clarify:
1. Are A–D intended to be four randomized presentation orders of exactly the same 206 lexical items?
2. If yes, which order(s) contain the erroneous substitutions, and is there a corrected CSV or erratum?
3. If the sets are intentionally different, what is the intended interpretation of the differing items and the 206-item count in the record/paper?
4. Is there a preferred citation/version note for researchers using the word-list file?

We have not silently merged, corrected or generated a scoreable packet from these lists. We will preserve the source version and document any correction or clarification you provide.

Thank you for your help.

Best regards,
[Project contact]

## 3. LOTUSDIS data-provider clarification request

The immutable Hub revision for the 14 October 2025 audio upload is now resolved from the official Hugging Face commits API: `45145d7ca2286498a31958b35628ab3c1969f808`. At that revision, the Hub tree API enumerates 24 Parquet shards (17 train, 3 validation, 4 test; 13,180,732,521 bytes total). Per-shard sizes, LFS SHA-256 values, Git blob SHA-1 values, Xet hashes and the commit that last wrote each shard are recorded in `data/benchmark/lotusdis-parquet-shards.tsv`.

**Hash evidence boundary:** the LFS SHA-256 values are copied from Hugging Face's repository tree metadata. The Parquet bytes were not downloaded, so those values are provider-reported object digests, not locally recomputed checksums. The dataset viewer's first-row preview confirms the schema (`audio` at 16 kHz, `sentence`, `speaker_id`, `mic`, `duration`) and one sample metadata record (train row 0: speaker `M01`, microphone `con123`, duration 2.59 s). Its temporary signed audio URL could not be retrieved as bytes in this execution environment. Accordingly, `data/benchmark/audio-assets.tsv` remains header-only: no individual WAV hash, stable audio asset URI, clean interval, or overlap status has been registered. This is source/snapshot provenance progress, not acoustic validation.

**Copy-ready request to dataset maintainer**

**Subject:** LOTUSDIS: immutable dataset revision and audio row provenance for phonetic annotation

Dear LOTUSDIS maintainers,

We are preparing a small, research-only human phonetic annotation sample from the public `nectec/LOTUSDIS` dataset. Before selecting any audio, could you confirm the full immutable dataset revision corresponding to the 14 October 2025 audio upload (the Hub history currently displays prefix `45145d7`) and clarify how the `audio`, `speaker_id`, `mic` and `duration` fields map to original recording/session identifiers?

We intend to select only a clean near-field single-speaker interval and retain the exact revision, Parquet shard/row identity, object hash, speaker pseudonym, microphone/channel and interval timestamps. We will not treat transcripts as phonetic gold.

If there is a canonical manifest or stable per-recording audio URI scheme, please point us to it.

Best regards,
[Project contact]

## 4. WCAG 2.2 AA hands-on verification protocol

**Status: NOT RUN.** Static source assertions and selected color-pair calculations are not manual conformance evidence. Firecrawl browser credits were exhausted at the time of this run, and no local browser/assistive-technology session was available. Do not mark any criterion passed until a tester records the actual build, browser, OS, assistive technology, steps and observed result.

### Required environments

- Desktop keyboard-only: current Firefox and Chromium-based browser, Windows or Linux.
- Screen reader: NVDA + Firefox and NVDA + Chromium on Windows; VoiceOver + Safari on macOS/iOS where available.
- Mobile: TalkBack + Chrome on Android and VoiceOver + Safari on iOS.
- Zoom/reflow: browser zoom to 200% and 400%; explicitly verify 320 CSS px reflow.
- Test both `web/index.html` and `web/system.html`, including dynamic result states, errors, disclosures and copy controls.

### Test cases and evidence

| WCAG criterion | Manual action | Pass condition |
|---|---|---|
| 2.1.1 Keyboard | Use Tab, Shift+Tab, Enter, Space and arrow keys through every control and disclosure. | Every operation is available without a pointer; no hidden keyboard-only action. |
| 2.1.2 No Keyboard Trap | Enter and leave every control/disclosure region. | Focus can always move away using the keyboard. |
| 2.4.3 Focus Order | Traverse both pages in reading/operation order. | Focus order preserves meaning and operability. |
| 2.4.7 Focus Visible | Inspect each focused control at normal and high zoom. | Keyboard focus indicator is visible. |
| 2.4.11 Focus Not Obscured (Minimum) | Focus controls near sticky headers, notices and page edges. | Focused component is not entirely hidden by author-created content. |
| 2.5.8 Target Size (Minimum) | Measure pointer targets for buttons, links and disclosure controls. | Target is at least 24×24 CSS px or meets a documented WCAG exception/spacing rule. |
| 1.4.10 Reflow | Test at 320 CSS px width / 400% zoom. | No loss of information or functionality and no two-dimensional scrolling except permitted content. |
| 1.4.12 Text Spacing | Apply WCAG text-spacing overrides (line height 1.5×, paragraph spacing 2×, letter spacing 0.12× font size, word spacing 0.16×). | No clipping, overlap or loss of functionality/content. |
| 1.4.11 Non-text Contrast | Inspect control boundaries, focus indicators and meaningful graphics against adjacent colors. | At least 3:1 where the criterion applies. |
| 3.3.1 Error Identification | Submit empty/invalid Thai input and inspect validation feedback. | Error is identified in text and associated with the field. |
| 3.3.2 Labels or Instructions | Navigate input controls with screen reader. | Purpose and required format are announced. |
| 4.1.2 Name, Role, Value | Inspect textarea, selectors, range input, buttons and disclosures using accessibility tree/screen reader. | Correct accessible name, role and current value/state. |
| 4.1.3 Status Messages | Run analysis and trigger errors without moving focus. | Meaningful status/result changes are announced without requiring focus movement. |

### Result record template

For each criterion and page, record: `test_id`, commit SHA, URL, date/time, tester, OS/version, browser/version, AT/version, viewport, zoom, exact steps, expected result, observed result, PASS/FAIL/NOT_TESTED, screenshot/video or redacted evidence reference, defect ID, fix commit and retest result. Keep `NOT_TESTED` distinct from `PASS`.

## 5. Current hard blockers

- No email/messaging connector is available in this execution context; no outbound invitation or curator request has been sent. This file is a prepared request pack, not evidence of contact.
- Firecrawl has `0` remaining credits in the current billing period, so live browser interaction and manual screen-reader testing could not be performed.
- No CCOST 6.2 GB archive bytes have been inspected. LOTUSDIS is now pinned to an immutable Hub revision and its 24 Parquet shard metadata is recorded, but the Parquet/audio bytes were not downloaded; provider-reported LFS hashes were not independently recomputed, and no individual WAV hash or clean interval is registered.
- No reviewer may be registered as verified and no annotation may be fabricated to make the evaluation gate pass.
