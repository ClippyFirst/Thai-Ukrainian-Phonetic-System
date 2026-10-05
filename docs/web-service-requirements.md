# Web service requirements — Thai → Ukrainian

## 1. Product definition

The web layer is the public-facing application of the research repository. It exposes the Thai → Ukrainian analysis pipeline without replacing the research core or inventing a second linguistic model.

The product has exactly two primary pages:
1. **Service** — interactive Thai input and results.
2. **System** — explanation of the author's Ukrainian practical transcription system and its evidence/method.

The service is not a translator. It analyses Thai orthography and presents pronunciation and Ukrainian rendering.

## 2. Reference product

The Chinese project ClippyFirst/chinese-for-ukrainians is the UX reference for information architecture and interaction density:
- one focused working surface;
- immediate input → result;
- copyable results;
- local-first/static architecture where possible;
- restrained typographic UI rather than a marketing landing page;
- a separate explanatory documentation page.

Reuse the interaction philosophy, not Chinese linguistic semantics.

## 3. Page A — Service

Required:
- header/project identity;
- Thai input;
- example input;
- clear action;
- analysis status;
- Thai orthographic decomposition;
- broad/phonological IPA;
- conservative surface IPA when available;
- Ukrainian phonetic/phonological candidate;
- Ukrainian practical orthographic candidate;
- uncertainty/warnings;
- independent copy controls;
- link to System;
- GitHub/source link;
- accessible live status.

Results must distinguish source Thai text, analysis, IPA, Ukrainian candidate and practical Ukrainian orthography. Unsupported or unresolved input must never become a confident-looking answer.

## 4. Page B — System

Explain in Ukrainian:
- what the system is;
- why it is practical transcription rather than character substitution;
- the full pipeline;
- Thai phonological evidence;
- IPA as intermediate representation;
- Ukrainian target constraints;
- candidate selection;
- tones;
- consonant classes;
- complex onsets;
- special orthography;
- established vs analysis-dependent rules;
- comparison with existing practice;
- limitations/evidence gates;
- reproducibility and citation.

This is a research explanation, not a second converter.

## 5. Visual identity

The visual language must be recognisably Thai but functional and typographic.

Palette derived from the Thai national flag:
- deep blue as the main structural/interactive colour;
- red as a restrained accent;
- white as the dominant field;
- neutral dark/light UI surfaces.

Do not turn the interface into a flag collage.

Avoid generic AI gradients, excessive glassmorphism, decorative Thai stereotypes, ornamental imagery without justification, noisy dashboards and excessive rounded cards.

The Chinese reference's restrained editorial/typographic character should remain visible.

## 6. Interaction

- no account;
- no server for ordinary conversion if the research core can be safely compiled to the browser;
- no telemetry by default;
- independent copy controls;
- Unicode Thai input;
- keyboard accessible;
- responsive desktop/mobile;
- clear success vs unresolved states;
- uncertainty is explained rather than hidden.

## 7. Linguistic correctness

The browser must not create an independent source of truth.

Preferred:
Thai source data/rules → generated browser data/runtime → UI.

If a browser implementation duplicates Python rules, it must have parity tests against the Python reference.

Preserve evidence-gated semantics:
- no empirical accuracy claim without a gold corpus;
- no claim of an official Ukrainian standard;
- no invented word segmentation;
- no silent fallback to /a/;
- no unsupported complex cluster;
- no silent dropping of unsupported characters;
- tone uncertainty remains visible.

## 8. Accessibility

Target WCAG 2.2 AA where practical:
semantic landmarks, labels, visible focus, keyboard operation, sufficient contrast, aria-live for results/errors, reduced-motion support, no colour-only meaning and announced copy confirmation.

## 9. Performance/security

Target a static first load, no external runtime dependency for core conversion, deterministic output, small initial bundle and lazy loading for large generated data.

Ordinary conversion must keep user text in the browser. Use restrictive CSP, no third-party analytics, no remote fonts unless justified, safe text rendering and safe external-link attributes.

## 10. Release gates

Release-ready means:
1. research-core tests pass;
2. browser build succeeds;
3. browser/reference parity tests pass;
4. representative Thai examples cover ordinary syllables, tones, clusters, ห นำ, preposed vowels and unresolved/special cases;
5. accessibility checks pass;
6. production build is deterministic;
7. System page matches current methodology;
8. UI contains no unsupported empirical claims;
9. static deployment is reproducible;
10. a release commit can be archived independently for DOI/Zenodo.

## 11. Acceptance probes

At minimum:
กา, กาน, กรา, กล้า, คน, เกะ, เก, เกีย, เกา, เกียว, แล้ว, เร็ว, เลย, ขาย, หงา, ไหม, ไหว้, แสดง.

Malformed repeated tone/vowel cases must also be tested.

These are regression probes, not corpus-accuracy claims.
