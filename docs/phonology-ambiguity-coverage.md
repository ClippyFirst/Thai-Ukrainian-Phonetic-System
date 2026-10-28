# Thai phonology completeness and ambiguous-reading audit

**Audit date:** 2026-10-28  
**Scope:** Standard Thai orthography, syllable-level phonology and IPA handoff.  
**Status:** PARTIAL — core productive rules are implemented, but lexical reading, syllabification, connected speech and acoustic realization are not exhaustive.  
**Evidence policy:** A source-attested dictionary reading is not independent IPA gold. No accuracy claim is made here.

## Findings

| Domain | Current behavior | Evidence / examples | State and safe next action |
|---|---|---|---|
| Consonant classes, tone marks, live/dead syllables, vowel quantity | Explicit rule table in `data/thai/tone_rules.csv`; tone-bearing consonant is distinct from written onset. New `tests/test_tone_rule_coverage.py` asserts all 15 canonical conditions, unique keys, runtime lookup parity and restricted mai-tri/chattawa use. | Tingsabadh & Abramson, *Thai* (1993), [JIPA DOI](https://doi.org/10.1017/S0025100300004746); [NEC/Unicode Thai script reference](https://r12a.github.io/scripts/thai/th). | DONE_VERIFIED as a deterministic rule implementation; not proof of correct syllabification on arbitrary text. |
| Initial clusters | Strict licensed cluster inventory; arbitrary adjacent consonants are not accepted as a cluster. | [Thai orthography notes](https://r12a.github.io/scripts/thai/th) documents restricted onset clusters. | PARTIAL: cluster inventory and loanword/rare forms require systematic source-backed coverage. Keep fail-closed for unlicensed sequences. |
| Final consonants | Onset and coda values differ; final stops are represented unreleased in surface IPA. | JIPA 1993; project contextual-phonology note. | PARTIAL: phonemic coda inventory is implemented; connected-speech and phonetic variation are not modeled exhaustively. |
| `ห นำ` and `อ นำ` | `ห นำ` has a structural path; `อย่า/อยู่/อย่าง/อยาก` are lexicalized; the rule must not generalize to arbitrary sequences. | Official OBEC teaching guide: [source PDF](https://academic.obec.go.th/web/images/document/1650944942_d_1.pdf), printed p. 275. | PARTIAL: broaden only with a documented construction and regression fixtures. |
| `ทร` | Exact lexical families such as `ทราบ` can be normalized by a known lexical reading; source-pinned compound `ทะเลทราย` is segmented as `ทะ|เล|ซาย` for the sand sense; isolated `ทราย` remains analysis-dependent. | Royal Institute journal, [เรื่องยุ่ง ๆ เกี่ยวกับอักษรควบ](https://www.orst.go.th/FILEROOM/CABROYINWEB/DRAWER004/GENERAL/DATA0000/00000630.FLP/html/49/); [Thai Wiktionary ทราย, revision 5775733](https://th.wiktionary.org/w/index.php?title=ทราย&oldid=5775733) records the common sand reading /saːj˧/; the Royal Institute source distinguishes the deer-name sense with a true cluster. The exact compound [ทะเลทราย, revision 87239667](https://en.wiktionary.org/w/index.php?title=ทะเลทราย&oldid=87239667) safely resolves the sand sense as ทะ-เล-ซาย. | PARTIAL, intentionally fail-closed. Do **not** apply /s/ to every `ทร` or add a context-free `ทราย` override without a sense/context contract. |
| `จร/สร/ศร/ซร` | These sequences are flagged as special orthography rather than automatically interpreted as a true /r/ cluster; a few established words have source-backed lexical normalization. | Project rule registry cites Royal Institute material; examples include `จริง`, `สร้าง`, `ศรี`, `เศร้า`, `ไซร้`. | PARTIAL: lexical exceptions are not a complete lexicon. Unknown forms must remain unresolved. |
| `รร` | Special orthography is detected; lexical segmentation is available for documented forms such as `สรรพคุณ`, `สรรพสินค้า`, `สรรพนาม`. | Official OBEC resource [การอ่านพยางค์ที่มี รร](https://academic.obec.go.th/images/document/1649041534_d_1.pdf), p. 29. | PARTIAL: `รร` has several context-sensitive readings; no single global replacement is justified. |
| `ฤ/ฤๅ/ฦ/ฦๅ` | Registered as analysis-dependent special vowel letters; generic forms do not receive a guessed IPA. Selected words use lexical syllabification. | Official OBEC/IPST guide [PDF](https://academic.obec.go.th/images/document/1649040986_d_1.pdf), p. 5. | PARTIAL: resolve per lexical item, not by treating the teaching guide's broad correspondences as universal IPA rules. |
| `์` and silent letters | Thanthakhat is recognized as a special construction; scope is not guessed from the mark alone. | Royal Institute orthography references in `data/thai/sources.csv`. | PARTIAL: add exact lexical rules only when the deleted span and word reading are source-attested. |
| Tone contours and surface phonetics | Tone category is stored separately from segmental IPA; surface IPA is withheld when evidence is absent. | JIPA 1993; [Thai script/phonology notes](https://r12a.github.io/scripts/thai/th). | PARTIAL: the engine's canonical tone contours are categorical encodings, not measured speaker-specific F0 trajectories. |
| Lexical segmentation and connected speech | Conservative endpoint withholds output when segmentation is unknown; opt-in dictionary segmentation has separate evidence grades. | Repository's source registries and segmentation benchmark docs. | PARTIAL: dictionary boundaries do not prove pronunciation; connected-speech sandhi/reduction remain outside deterministic core. |

## Regression contract added by this audit

1. Every registered ambiguity family must return an analysis-dependent/withheld result for a representative unlisted form.
2. Source-backed lexical readings may resolve only their exact listed forms.
3. A known lexical reading must not be promoted to a productive spelling rule.
4. Context-specific compound `ทะเลทราย` must resolve to `ทะ|เล|ซาย` in both Python and browser, while isolated `ทราย` remains unresolved.
4. Thai practical output must continue to be derived through the typed IPA adapter.
5. A dictionary IPA entry is labelled `SOURCE_ATTESTED_NOT_GOLD`; it must not enter the adjudicated-gold denominator.
6. An unresolved ambiguity is a valid safe result, not a coverage failure to be patched with a guessed pronunciation.

## Highest-value next research tasks

- Build a source-pinned contrast set for productive onset clusters vs. false clusters, including word/sense-specific `ทร`.
- Expand the `รร`, `ฤ`, silent-letter and loanword matrices using official Thai education/reference sources, preserving exact word boundaries and source revisions.
- Review coda /p t k/ and short open syllables separately at phonemic vs. surface-phonetic levels.
- Obtain independent Thai-speaker/phonetics adjudication for IPA and Ukrainian target forms before reporting accuracy.
- Audit all registered vowel patterns against the structural generator and all browser/Python implementations; do not infer completeness from a passing fixture suite alone.

## Overall verdict

**Core deterministic rules: implemented; edge-case coverage: partial; lexical pronunciation coverage: partial; connected-speech model: deferred; independent IPA accuracy: not measured.** The current design correctly prefers uncertainty over a fabricated pronunciation. This audit does not certify the engine as complete or release-ready.


## Verification closure (2026-10-28)

- Exact code head `7a47e1f86862f33bb8eadfb34de75aeba5fd3809`: [CI 40645028725](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40645028725) passed 209 Python tests, browser parity/UI contracts, benchmark and diagnostic gates, and the master artifact (351,780 structural rows, 41 vowels).
- [Web static validation 40645028587](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/40645028587) passed.
- The code/test work is verified; the project remains a partial linguistic prototype because independent IPA/UA gold, exhaustive lexical exceptions and connected speech remain open.
