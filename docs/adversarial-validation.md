# Adversarial validation

This document records deliberately difficult Thai inputs used to test failure modes of the parser. These are regression probes, not a gold corpus.

| Probe | Expected property |
|---|---|
| `กา` | explicit long vowel, open live syllable, /kaː/ |
| `กาน` | final น is coda and makes syllable live |
| `กรา` | กร remains a two-consonant onset cluster; no coda |
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
| `หงา` | ห นำ changes effective onset while retaining high-class tone environment |
| `ข๊า` | invalid high-class + mai tri combination is represented as structured invalid input, not a crash |
| `รร` forms | warning/unresolved pathway rather than silent universal guessing |
| thanthakhat forms | warning/unresolved pathway rather than silent universal guessing |

## What these probes test

1. **Longest-match precedence** — a specific rime must not be truncated by a generic preposed-vowel rule.
2. **Terminal glide ownership** — a glide belonging to the nucleus must not be counted again as a coda.
3. **Implicit-vowel epistemic safety** — unknown vowel quality must remain unknown until lexical/morphological evidence is available.
4. **Cluster/coda separation** — consonant sequences are not classified solely by their Unicode order.
5. **Tone robustness** — invalid combinations must be surfaced as data errors without crashing the general analysis API.
6. **Contextual orthography** — ห นำ is treated as an explicit transformation, not ordinary segment concatenation.

These probes do not establish empirical accuracy. A corpus benchmark still requires an external, named and versioned gold resource.
