# Adversarial validation

These probes target failure modes that can silently produce plausible but wrong Thai analyses. They are regression probes, not a gold corpus.

| Probe | Expected property |
|---|---|
| `กา` | explicit long vowel, open live syllable, /kaː/ |
| `กาน` | final น is coda and makes syllable live |
| `กรา` | กร is a licensed complex onset; no coda |
| `กล้า` | licensed complex onset; tone uses the first consonant class |
| `ก` | implicit-vowel case is unresolved; no invented IPA |
| `คน` | implicit-vowel case remains unresolved rather than being guessed as /a/; น remains structurally visible as coda |
| `เกะ` / `เก` | short/long preposed เ patterns are distinguished |
| `เกีย` | /iaː/ is recognized |
| `เกา` | /aw/ is recognized before generic เ- |
| `เกียว` | /iaw/ is recognized before generic เ-ีย |
| `แล้ว` | /ɛːw/ is recognized and ว is not duplicated as a coda |
| `เร็ว` | /ew/ is recognized and ว is not duplicated as a coda |
| `เลย` | /ɤːj/ is recognized and ย is not duplicated as a coda |
| `ขาย` | /aːj/ nucleus; ย is not treated as coda |
| `หงา` | ห นำ changes effective onset while retaining its high-class tone environment |
| `ข๊า` | invalid high-class + mai tri combination is structured, not a crash |
| `แสดง` | not forced into a fictitious /sd-/ complex onset; lexical/syllabic segmentation is required |
| `กาอ` | carrier อ is not silently accepted as a final coda |
| `รร` forms | unresolved/context-dependent pathway rather than universal guessing |
| thanthakhat forms | silent-letter evidence is preserved rather than erased blindly |

## What these probes test

1. Longest-match precedence.
2. Terminal-glide ownership.
3. Implicit-vowel epistemic safety.
4. Complex-onset licensing rather than “two consonants = cluster”.
5. Tone robustness and invalid-combination handling.
6. Contextual orthography such as ห นำ.
7. Separation of written onset class from tone-bearing class.
8. Source-model consistency between parser-recognized rimes and the declared vowel registry.

Standard Thai descriptions restrict complex onsets; the parser therefore refuses to manufacture a complex onset from arbitrary adjacent consonants. See the cited phonetic/orthographic sources in the project evidence registry.

These probes do not establish empirical accuracy. A corpus benchmark still requires an external, named and versioned gold resource.


## Three-profile fallback regression — 2026-11-01

The regression from the reported 1/3 output is now included in the main research branch and runs in CI after generating the browser word dictionary. Ten hand-written mixed Thai/mixed-script cases plus the 42 frozen challenge inputs are exercised across strict, soft and super-soft profiles (52 inputs × 3 profiles = 156 profile/input combinations). Six focused forms receive additional strict/super-soft checks: five unreferenced forms must be withheld in strict mode, while `เพิ่ง` uses a pinned source-attested one-syllable override with short /ɤ/, falling tone and explicit NOT_GOLD provenance. The suite also checks positive use of the heuristic fallback, all source-attested lexical controls, exact IPA→Ukrainian adapter equality and RTGS numeric passthrough. These remain runtime/evidence-contract tests, not independent pronunciation gold.

A structurally provisional orthographic fallback no longer carries computed tone, tone contour or surface IPA into the result as if confirmed. Segmental IPA remains a provisional candidate and continues through the existing IPA adapter. This is a conservative uncertainty fix, not a claim that the fallback IPA is correct Thai pronunciation.

Exact push CI [41337529189](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41337529189) passed all three jobs; Web Static [41337815975](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41337815975) passed. PR #181's implementation/test/CI changes were ported into PR #182 and #181 was closed as superseded; its branch was retained.
