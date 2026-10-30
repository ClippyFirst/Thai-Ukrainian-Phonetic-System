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
