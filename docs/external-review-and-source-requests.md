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

## 2. CCOST annotation-tier and label clarification request

### Public author/curator contacts

The published LREC 2026 paper lists these author contacts:
- Cathryn Yang: cathryn_yang@sil.org
- James Kirby: jkirby@phonetik.uni-muenchen.de
- Pittayawat Pittayaporn: pittiyawat.p@chula.ac.th (paper spelling; ChulaSEAL's official page lists Pittayawat.P@chula.ac.th)
- Sujinat Jitwiriyanont: sujinat.j@chula.ac.th (paper spelling; ChulaSEAL's official page lists Sujinat.J@chula.ac.th)

The Zenodo record identifies Pittayawat Pittayaporn and Sujinat Jitwiriyanont as data curators and Cathryn Yang and James Kirby as data managers. These contacts are taken from the paper and institutional pages; no message has been sent by this workflow.

### Copy-ready request

**To:** Pittayawat Pittayaporn; Sujinat Jitwiriyanont; Cathryn Yang; James Kirby  
**Subject:** CCOST v1.0 TextGrid clarification: -MAU tiers, _8 labels and MAUS markers

Dear CCOST team,

We are reviewing the public CCOST v1.0 TextGrid annotations for a research prototype on Thai-to-Ukrainian phonetic transcription. We have read the LREC 2026 paper and inspected all 488 TextGrid files in our supplied text-only archive. We have not changed source labels or inferred pronunciations for unsupported forms.

The paper (§3.3–3.4) describes ORT, KAN, KAS, MAU, MAS, and TRN; it defines MAU as the phonetic-segment tier, MAS as the phonemic-syllable tier, and says phonetic/phonemic labels use X-SAMPA. The release we inspected instead contains ORT-MAU, KAN-MAU, and KAS-MAU alongside MAU, MAS, and TRN.

Could you please clarify:

1. **Tier names:** Why do ORT-MAU, KAN-MAU, and KAS-MAU carry the -MAU suffix? Are these export aliases for ORT, KAN, and KAS, additional MAUS-generated tiers, or a distinct tier family? Should downstream users treat them as semantically equivalent to the unsuffixed names?
2. **_8 labels:** The paper documents only _1–_5 for Mid, Low, Falling, High, and Rising tones. We found 868 failed-conversion occurrences containing _8 across 22 distinct raw strings (including ? a_8, l {:_8 p, a_8, and {:_8). What does _8 encode in this release? Is it a MAUS/X-SAMPA convention, an unknown/unclassifiable event, an alignment artifact, or a transcription error? Should it be retained as an opaque marker or excluded from phonetic interpretation?
3. **-MAU spelling and segmentation:** Are slash forms such as r/ and compound forms intended to represent alternatives, boundaries, or multiple phones? Is there a release-specific X-SAMPA inventory or mapping table?
4. **Tag spellings:** The paper documents <usb> for disfluencies and <p:> for pauses; BAS documentation also defines <nib> as a non-speech event. We also found <P>, <P:>, <:p>, <Fail>, and <notProcessedChunk>. What do these exact, case-sensitive forms mean? Are they all MAUS/BAS control markers, and if so, which should be treated as non-phonetic?
5. **Mixed labels:** We found labels combining tags with phonetic material or Thai text (for example marker-plus-phone and marker-plus-transcript strings). Should these be preserved as complete raw events, split into aligned components, or interpreted using a specific escape/serialization rule?
6. **Unicode-looking strings:** Some failed labels contain IPA-like Unicode symbols (ɹ, ɾ, tʃ, ʔ, nˠ) despite the paper specifying X-SAMPA. Are these intentional release annotations, post-processing artifacts, or malformed entries?

We recorded 1,014 tier-level failed-conversion occurrences across 116 distinct raw strings. These are not necessarily 1,014 unique speech events because aligned tiers can repeat the same event. We can provide a compact CSV of distinct labels, counts, tier names, and representative file/interval identifiers if useful.

Until we receive clarification, our adapter preserves all raw strings, converts only explicitly supported X-SAMPA forms, and fails closed on unresolved markers and mixed labels. We will not interpret _8 as a sixth tone or silently strip unknown tags.

Thank you for maintaining this valuable resource. Any pointer to a corrected manual, release note, or canonical MAUS export specification would also be very helpful.

Best regards,  
[Project contact]

### Contact and delivery status

**PREPARED — NOT SENT.** Public email addresses are verified from the paper/institutional sources. The connected tools available in this session include GitHub but no email-sending action, so no outbound message has been transmitted and no curator response has been received. Send the request from the project owner's email account; record the sent date, message ID, and any reply before changing blocked labels to verified.

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

The official dataset card also links the full-session WAV archive [wav.zip](https://drive.google.com/file/d/1ofw99Y5W1p8f1DSaIbJkS0xWtuTI2Hrc/view) and TextGrid archive [textgrid.zip](https://drive.google.com/file/d/14fMv_X_8sGDPGbnU-hpJ85Mug43AHlgO/view). Both Google Drive links resolve, but the file pages require sign-in/automated retrieval is blocked in this environment. The archives have not been downloaded or inspected; do not infer tier contents or audio-to-row alignment from filenames alone.

**Copy-ready request to dataset maintainer**

**Subject:** LOTUSDIS: immutable dataset revision and audio row provenance for phonetic annotation

Dear LOTUSDIS maintainers,

We are preparing a small, research-only human phonetic annotation sample from the public `nectec/LOTUSDIS` dataset. We resolved the 14 October 2025 audio-upload revision as `45145d7ca2286498a31958b35628ab3c1969f808` using the Hugging Face Hub commits API and recorded the Hub-reported metadata for all 24 Parquet shards. Could you confirm that this is the intended immutable snapshot and clarify how the `audio`, `speaker_id`, `mic` and `duration` fields map to original recording/session identifiers?

The dataset viewer exposes temporary signed audio URLs for rows, but our environment could not retrieve the audio bytes. We therefore have not registered an audio asset or claimed a per-WAV hash. Could you point us to a stable revision-pinned audio-object URI or canonical manifest, and clarify whether the row index plus Parquet shard is a stable identifier for an audio item?

We intend to select only a clean near-field single-speaker interval and retain the exact revision, Parquet shard/row identity, independently computed audio-object hash, speaker pseudonym, microphone/channel and interval timestamps. We will not treat transcripts as phonetic gold.

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
- The owner-supplied CCOST TextGrid-only ZIP has been structurally inspected: 488/488 files parse, with actual release tiers inventoried. The owner-supplied LOTUSDIS TextGrid ZIP has 90/90 parseable transcript files. No audio member was read or extracted. Remaining CCOST source questions concern provisional `-MAU` tier aliases, `_8`, Unicode IPA-looking forms and annotation tags; these require curator/manual clarification. LOTUSDIS audio/Parquet acquisition and acoustic provenance are DEFERRED / OUT OF SCOPE by owner decision.
- No reviewer may be registered as verified and no annotation may be fabricated to make the evaluation gate pass.


## 2A. CCOST release-tier and label clarification — prepared, not sent

**Status: PREPARED — NOT SENT.** The owner has supplied a TextGrid-only ZIP containing 488 `.TextGrid` files; CI parses all 488. The earlier request for a TextGrid-only export is superseded. This follow-up asks only for clarification of observed release-tier and label conventions.

**Subject:** Clarification of CCOST TextGrid tier aliases and observed annotation labels

Dear Pittayawat Pittayaporn, Cathryn Yang, Sujinat Jitwiriyanont and James Kirby,

We are conducting non-commercial research on Thai phonetic transcription using the CCOST v1.0 release (Zenodo DOI 10.5281/zenodo.17366698). We have obtained a TextGrid-only export and deliberately excluded audio from our workflow.

Our structural inventory contains 488 TextGrid files, matching the total recording-file count in Table 1 of the LREC 2026 paper. The files use tiers named `ORT-MAU`, `KAN-MAU`, `KAS-MAU`, `MAU`, `MAS` and `TRN`, rather than the shorter published names ORT/KAN/KAS/MAU/MAS/TRN. Could you confirm whether the `-MAU` suffixes are release-specific aliases for the corresponding orthographic/canonical tiers?

We also ran a full fail-closed inventory of the phonetic tiers. It recorded 1,014 conversion-failure occurrences across 116 distinct raw label strings: 868 occurrences contain an undocumented `_8` sequence (22 distinct strings); 58 are slash/alternative forms; 26 mix a MAUS marker with phonetic or text material; 17 are non-ASCII phonetic-looking forms; 10 contain Thai script or mixed Thai/phonetic text; 14 are truncated/malformed; and 21 are other unsupported ASCII sequences. Failures occur in MAU (276), MAS (263), KAS-MAU (239), and KAN-MAU (236). These are tier-level occurrences, not 1,014 unique speech events. We preserve every raw label and do not guess conversions.

We also observed labels that are not explained by the paper's five-tone table:

1. `_8` tone suffixes (for example `? a_8`, `a_8` and `{:_8`), although the paper documents only `_1`–`_5` for Mid/Low/Falling/High/Rising. What does `_8` mean, and should these labels be treated as unknown/unspecified rather than lexical tone?
2. Unicode IPA-looking tokens in MAU (for example `ɹ`, `ɾ`, `tʃ`, `ʔ`) and unusual forms such as `r/`. Are these intentionally IPA rather than X-SAMPA, and is there a canonical conversion table?
3. We understand from the paper and BAS format documentation that `<p:>` denotes pause, `<usb>` is used for speaker-produced disfluency/unintelligible events, and `<nib>` denotes a non-speech event/noise. Could you confirm these meanings for the CCOST release and explain the distinct observed tags `<notProcessedChunk>`, `<Fail>`, `<P>`, `<:p>` and `<P:>`? Should the latter be treated as errors/unknown markers? We also observe mixed marker-plus-Thai-text and marker-plus-phone labels; should these be preserved as raw events rather than parsed as phonetic segments?
4. Is the supplied 488-file TextGrid set complete for the v1.0 recording manifest, or are any sessions/files intentionally absent?
5. Is the published `CCOST_manual.pdf` the current authoritative manual for the released tier schema, and is there a more detailed MAUS/PHO2SYL label inventory?

We preserve all raw labels and tier names, fail closed on unsupported notation, and do not promote CCOST annotations to independently adjudicated gold. We will retain CC BY-NC-SA 4.0 attribution and ShareAlike conditions.

The LREC 2026 paper lists these author contacts: cathryn_yang@sil.org, jkirby@phonetik.uni-muenchen.de, pittiyawat.p@chula.ac.th, sujinat.j@chula.ac.th.

Thank you for your guidance.

Best regards,
[Project contact]
