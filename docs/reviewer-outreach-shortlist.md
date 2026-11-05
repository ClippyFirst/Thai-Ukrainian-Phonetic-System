# Independent reviewer outreach shortlist

**Status:** research shortlist only. No one has been contacted, has agreed to review, or has been entered into `data/benchmark/reviewer-qualifications.tsv`. This list is not evidence of availability, native-speaker status, independence, or verified qualifications. Before inviting anyone, confirm language competence, current role, relevant expertise, conflicts of interest, scope, fee/compensation and permission to be credited or remain pseudonymous.

## Thai phonetics, phonology and segmentation

The Thai review requires two independent reviewers with demonstrated Standard Thai competence and experience in phonetics/phonology. A separate adjudicator should not be either first-pass reviewer.

| Potential reviewer | Publicly documented fit | Public institutional route |
|---|---|---|
| **Chutamanee Onsuwan, Ph.D.** | Thammasat faculty profile lists a PhD dissertation on temporal relations between consonants and vowels in Thai syllables; expertise includes laboratory phonetics, speech science and phonology; publications include Thai vowel duration and tone perception. | [Official Thammasat profile](https://arts.tu.ac.th/th/teacherlarts/cmukv6znk0052pm61l213msd6); use the faculty contact route. |
| **Lena Maluleem, Ph.D.** | Kasetsart Department of Linguistics profile lists phonetics/phonology, prosody and experimental linguistics; published work includes Thai compound stress. | [Official Kasetsart profile](https://ling.human.ku.ac.th/index.php/lyna_cv/); public institutional email: `lena.m@ku.th`. |
| **Rungpat Roengpitya** | Mahidol profile lists work on Standard Thai tones, cross-language perception of Japanese vowel-length contrasts, and perception of Thai word-final voiceless stops; the cited profile does not establish direct Thai vowel-length expertise. | [Official Mahidol profile](https://murex.mahidol.ac.th/en/persons/rungpat-roengpitya/); contact through the profile. |
| **Sujinat Jitwiriyanont, Ph.D.** | Chulalongkorn profile lists phonetics and acoustic phonetics; co-author of the 2026 CCOST corpus paper. | Public institutional email: `Sujinat.J@chula.ac.th`; [official ChulaSEAL people page](https://www.arts.chula.ac.th/chulaseal/people/). Disclose CCOST authorship if reviewing CCOST-derived labels. |
| **Pittayawat Pittayaporn, Ph.D.** | Chulalongkorn profile lists phonology and Southeast Asian linguistics; relevant Thai phonology publications and co-author/data curator of CCOST. | Public institutional email: `Pittayawat.P@chula.ac.th`; [official ChulaSEAL people page](https://www.arts.chula.ac.th/chulaseal/people/). Disclose CCOST authorship/curatorship if reviewing CCOST-derived labels. |

**Suggested initial pair:** invite Chutamanee Onsuwan and Lena Maluleem or Rungpat Roengpitya, subject to confirmation that each can independently review Standard Thai phonemic IPA, lexical readings, word/syllable boundaries and tone. Do not presume native status from names or affiliation; ask each reviewer to state their Thai proficiency and dialect/standard competence.

## Ukrainian practical transcription and phonetics

The Ukrainian task is conditional on supplied source IPA. It needs at least two independent Ukrainian-language reviewers who can assess practical transcription, Ukrainian phonotactics/orthography and readability. Thai expertise is not required for this layer; the IPA reference must remain visibly marked as source-attested, not gold.

| Potential reviewer | Publicly documented fit | Public institutional route |
|---|---|---|
| **Uliana Holovach, Ph.D.** | Associate professor at Ukrainian Catholic University; peer-reviewed work specifically addresses Ukrainian practical transcription of foreign proper names and distinguishes assimilated loans from unassimilated names. | [Official journal biography](https://lcmp.ukma.edu.ua/article/view/272362); public email: `holovatch@ucu.edu.ua`. |
| **Maksym O. Vakulenko, Ph.D.** | Linguist with documented research in Ukrainian phonetics, phonetic transcription and transliteration; 2025 peer-reviewed work addresses Ukrainian phonetic data and IPA. | [Peer-reviewed 2025 article](https://edizionicafoscari.unive.it/en/edizioni4/riviste/balcania-et-slavia/2025/1/movoznavchi-ta-didaktichni-aspekti-vikhodu-z-ukray/); [professional profile](https://ukrdiaspora.nauka.gov.ua/en/mentorship/d-r-maksim-vakulenko/). |
| **Erika Yesenova** | Senior lecturer at Uzhhorod National University; published specifically on practical transcription and transliteration of loanwords in the recipient language. | [UzhNU repository record](https://dspace.uzhnu.edu.ua/items/862027cb-dc7a-4b5b-a9fb-cca3bc28e107); [department staff/contact page](https://uzhnu.edu.ua/en/kafedra/kafedra-teorii-ta-praktyky-perekladu-2/staff). |

**Suggested initial pair:** invite Uliana Holovach and Maksym Vakulenko or Erika Yesenova. Confirm willingness to assess the project's declared *common-word practical transcription* scope; the cited work on proper names and loans is relevant methodological expertise, not an automatically binding rule for Thai.

## Review process and independence safeguards

1. Send the scope, versioned criteria and blind packet—not engine candidates, model rankings or another reviewer's annotations.
2. Ask for a short qualification statement: Thai/IPA competence and dialect for Thai reviewers; Ukrainian native/professional competence and practical-transcription experience for target reviewers.
3. Confirm conflicts, including prior contribution to the source corpus, project, engine, or any shared annotation.
4. Obtain two first-pass submissions independently. Freeze both originals before discussion.
5. A separate adjudicator resolves disagreements with a written rationale; preserve unresolved cases and abstentions.
6. Add a reviewer registry row only after the project owner verifies identity/qualification evidence and has permission to record it. Do not fabricate `VERIFIED` entries from this shortlist.
7. For acoustic tone or surface-phonetic claims, use licensed recordings with speaker/asset/time provenance; dictionary IPA and the CCOST wordlist alone are insufficient.

## Current evidence and blockers

- Thai blind packet: 42 frozen base prompts plus six supplemental user-regression prompts. The CCOST source preview has 206 rows per A-D order, but B/C/D each differ from A by two items; no scoreable CCOST review packet was generated pending curator clarification. Neither source contains expert phonetic labels.
- Ukrainian preference packet: seven source-attested IPA examples, including `เพิ่ง /pʰɤŋ˥˩/`. These are conditional review prompts, not IPA gold.
- Reviewer registry remains empty. No outreach has been sent and no human reviews have been received.
- CCOST wordlist preview was reconstructed byte-identically using the official MD5; exact A-D audit found a 2-item set mismatch per B/C/D versus A (208-item union), awaiting data-curator clarification. The 6.2 GB audio/TextGrid archive remains uninspected.


## Audio-source option for phonetic review

The source registry now includes `CORP-LOTUSDIS` (CC BY-SA 4.0) as an audio/transcript source for fresh human phonetic annotation. It is not an IPA/toneme gold set. For any acoustic review, the project owner must first pin the exact dataset revision and asset, verify a clean near-field non-overlap segment, and record speaker pseudonym, microphone/channel, time interval and file hash. No LOTUSDIS audio has been downloaded, sampled or sent to reviewers in this run. See [phonetic corpus selection](phonetic-corpus-selection.md).


## Contact-route verification — 2026-11-02

Official ChulaSEAL faculty pages publish institutional email addresses for CCOST curators Pittayawat Pittayaporn (`Pittayawat.P@chula.ac.th`) and Sujinat Jitwiriyanont (`Sujinat.J@chula.ac.th`). These routes are suitable for a wordlist clarification request, not for claiming an independent review of their own CCOST material. See `docs/external-review-and-source-requests.md` for a prepared message.

The shortlist remains **not contacted**. No outbound email facility was available in the execution environment; public contact details do not imply consent or availability.

## Thai expert qualification evidence refresh — 2026-11-05

The following candidates have current, publicly accessible institutional evidence relevant to the specific CCOST review. This improves qualification screening; it does **not** establish availability, consent, native-speaker status, conflict-free independence, or a completed review.

| Candidate | Publicly documented evidence | Potential role (unconfirmed) |
|---|---|---|
| **Chutamanee Onsuwan, Ph.D.** | Thammasat's official profile lists a Ph.D. dissertation on temporal relations between consonants and vowels in Thai syllables and expertise in laboratory phonetics, speech science and phonology; the profile also lists work on Thai vowel duration and tone perception. [Official profile](https://arts.tu.ac.th/th/teacherlarts/cmukv6znk0052pm61l213msd6) | First-pass reviewer for segmental, syllabic and phonetic interpretation |
| **Lena Maluleem, Ph.D.** | Kasetsart's official profile lists a Ph.D. in linguistics and research interests in phonetics/phonology, prosody and experimental linguistics; publications include Thai compound stress. [Official profile](https://ling.human.ku.ac.th/index.php/lyna_cv/) | Independent first-pass reviewer, subject to confirmation of Standard Thai IPA scope |
| **Rungpat Roengpitya** | Mahidol's official profile lists research on variation and quantification of Standard Thai tones, lexical tone awareness, Thai vowel-length perception and word-final stops. [Official profile](https://murex.mahidol.ac.th/en/persons/rungpat-roengpitya/) | Separate adjudicator or alternate reviewer, subject to confirmation of scope and independence |

A reasonable *proposed* panel is Onsuwan + Maluleem for blind first-pass annotation and Roengpitya as separate adjudicator. Do not record this as an appointment. Before use, verify each person's current role, Standard Thai competence, IPA/X-SAMPA familiarity, conflict statement, availability and permission to record qualification evidence. Keep reviewer registry rows empty until that verification is performed.

**Conflict boundary:** Pittayawat Pittayaporn and Sujinat Jitwiriyanont are CCOST paper authors/data curators. They may be useful for source-format clarification, but should not be counted as independent first-pass reviewers or the independent adjudicator for CCOST labels without a documented, defensible conflict assessment.

**Review scope boundary:** the supplied worklist supports text-based review of canonical/phonemic labels, marker semantics and cross-tier consistency. It does not support acoustic adjudication of surface tone contours, timing, or allophonic realization because audio is deliberately not opened or distributed in this project scope.

No contact has been made. No email has been sent. No reviewer has agreed to participate.


## Public-source candidate refresh for CCOST exception review — 2026-11-05

A focused search for Thai acoustic-phonetics and tone specialists found a stronger three-person *proposed* panel. These are public qualification leads only; no contact, consent, availability, conflict declaration or appointment is established.

| Candidate | Directly relevant public evidence | Proposed role, subject to acceptance |
|---|---|---|
| **Chutamanee Onsuwan, Ph.D.** | Official Thammasat profile documents a Ph.D. on temporal relations between consonants and vowels in Thai syllables and expertise in laboratory phonetics, speech science and phonology. Her publication record includes Thai tone perception and segmental timing. [Official Thammasat profile](https://arts.tu.ac.th/th/teacherlarts/cmukv6znk0052pm61l213msd6); [Thai stop/vowel timing study](https://sealang.net/sala/archives/pdf4/onsuwan2002temporal.pdf). | First-pass reviewer A |
| **Phanintra Teeranon, Ph.D.** | Public CV lists a Ph.D. in linguistics and phonetics coursework; peer-reviewed research directly examines acoustic and perceptual properties of Standard Thai tones, including comparisons with native Thai speakers and Praat F0 analysis. [CV](https://mfuth.academia.edu/PhanintraTeeranon/CurriculumVitae); [Thai tones acoustic/perceptual study](https://so03.tci-thaijo.org/index.php/JLC/article/view/240495); [2020 tone application study](https://asianonlinejournals.com/index.php/EDU/article/view/1701). | First-pass reviewer B |
| **Rungpat Roengpitya** | Mahidol profile lists work on Standard Thai tone variation, Thai children's lexical-tone awareness, vowel-length perception and word-final stops. Publications include acoustic work on Thai fricatives and phonetic realization of Khorat Thai tones. [Official Mahidol profile](https://murex.mahidol.ac.th/en/persons/rungpat-roengpitya/); [Khorat Thai tones](https://assta.org/proceedings/sst/2006/sst2006-76.pdf); [ICPhS acoustic study](https://www.internationalphoneticassociation.org/icphs-proceedings/ICPhS2011/OnlineProceedings/RegularSession/Roengpitya/Roengpitya.pdf). | Separate adjudicator |

**Why this panel is preferable:** all three have public evidence directly relevant to Thai phonetics/tones, and none is listed as a CCOST paper author or curator. This is not enough to certify independence: each must still disclose collaboration, supervision, financial and personal conflicts with CCOST authors, the project and each other. The project owner must verify identity, current role, Thai competence and consent before adding any reviewer registry entry.

**Conflict caution — Lena Maluleem:** her phonetics/phonology and Thai prosody credentials are relevant, but public publication metadata identifies Pittayawat Pittayaporn as her co-author on Thai prosody research, and her doctoral work was supervised by him. Since Pittayaporn is a CCOST co-author/data curator, treat this as a potential conflict for independent CCOST adjudication; do not assign her to the independent CCOST panel unless the conflict is disclosed and explicitly assessed. [Journal article](https://so04.tci-thaijo.org/index.php/TSDJ/article/view/261290); [Kasetsart profile](https://ling.human.ku.ac.th/index.php/lyna_cv/).

The CCOST authors/curators Pittayawat Pittayaporn and Sujinat Jitwiriyanont remain useful for source-format clarification but should not be counted as independent reviewers of their own corpus annotations.


## Official institutional qualification refresh — 2026-11-05

The proposed Thai panel has been rechecked against current public institutional pages rather than relying only on aggregator/CV mirrors. This is qualification screening, not contact or appointment.

| Candidate | Official institutional evidence | Relevant fit and caveat | Proposed role |
|---|---|---|---|
| **Chutamanee Onsuwan, Ph.D.** | [Thammasat official faculty profile](https://arts.tu.ac.th/th/teacherlarts/cmukv6znk0052pm61l213msd6) | Ph.D. dissertation on temporal relations between consonants and vowels in Thai syllables; expertise in laboratory phonetics, speech science and phonology; publication list includes Thai vowel-length and lexical-tone perception studies. | Blind first-pass reviewer A |
| **Phanintra Teeranon, Ph.D.** | [University of Phayao official staff profile](https://www.libarts.up.ac.th/employee/phanintra.te); public institutional email: phanintra.te@up.ac.th; [CV/publications](https://mfuth.academia.edu/PhanintraTeeranon/CurriculumVitae) | Associate Professor; Ph.D. in Linguistics; public CV lists phonetics coursework and acoustic/perceptual Thai tone research, including an acoustic/perceptual study of Standard Thai high tone and Thai-tone production/perception work. The official profile confirms current institutional affiliation/contact. | Blind first-pass reviewer B |
| **Rungpat Roengpitya** | [Mahidol official profile](https://murex.mahidol.ac.th/en/persons/rungpat-roengpitya/); public institutional email: rungpat.roe@mahidol.ac.th | Assistant Professor; official profile lists research on variation and quantification of Standard Thai tones, Thai lexical-tone awareness, Japanese vowel-length perception and Thai word-final stops. | Separate adjudicator candidate |

All three are not listed as authors of the CCOST LREC paper, but that alone does **not** establish independence. Before appointment, each must disclose prior collaboration, supervision, financial/personal interests and relationships with the other reviewers, the CCOST authors/curators and this project. Confirm Standard Thai competence, X-SAMPA/IPA familiarity, willingness, scope, compensation and permission to retain qualification evidence. The project has not contacted anyone, and no one has consented or been appointed. Keep reviewer-qualifications.tsv header-only until those checks are completed.
