# Web service requirements — Thai → Ukrainian

## Product

The web layer is the public application of the research repository, not a second linguistic model. It has exactly two primary pages: Service and System.

The Service analyses Thai orthography and presents pronunciation plus Ukrainian project rendering. It is not a semantic translator.

## Service page

Required: Thai input, examples, clear action, structured status, orthographic decomposition, broad/phonological IPA, conservative surface IPA when available, Ukrainian candidate(s), practical Ukrainian candidate, warnings, copy controls, System/GitHub links, accessible live result status.

Unsupported, unresolved and analysis-dependent input must remain visibly distinct from successful analysis.

## System page

Explain in Ukrainian: purpose; practical transcription vs character substitution; full pipeline; Thai phonological evidence; IPA's audit role; Ukrainian target constraints; candidate selection; tones; consonant classes; clusters; special orthography; established vs analysis-dependent rules; comparisons; limitations; reproducibility and citation.

## Visual identity

Use a functional Thai visual identity derived from the national flag: deep blue as the structural colour, restrained red accent, white dominant field, neutral text/surfaces. Avoid flag collage, generic AI gradients, excessive glassmorphism, decorative stereotypes, noisy dashboards and excessive rounded cards. Preserve the restrained editorial/typographic character of the Chinese reference project.

## Engineering

Prefer a static, browser-local runtime generated from the Python research source. The browser must not become a second source of truth. If a browser port duplicates rules, Python↔browser parity fixtures are mandatory.

No account, no telemetry by default, Unicode Thai, keyboard access, responsive layout, safe text rendering and explicit unresolved states.

Target WCAG 2.2 AA where practical. Core conversion should have no third-party runtime dependency. Use restrictive CSP and no third-party analytics.

## Research gates

The site must not claim corpus accuracy without a gold corpus, must not claim an official Ukrainian standard, must not invent lexical segmentation, and must not silently guess or drop unsupported input.

## Release gates

Research tests pass; browser build passes; Python↔browser parity passes; representative Thai regression probes pass; accessibility is checked; production build is deterministic; System documentation matches the implementation; static deployment is reproducible; release can be archived independently for DOI/Zenodo.

## Acceptance probes

กา, กาน, กรา, กล้า, คน, เกะ, เก, เกีย, เกา, เกียว, แล้ว, เร็ว, เลย, ขาย, หงา, ไหม, ไหว้, แสดง, plus malformed repeated tone/vowel cases.

These probes are regression fixtures, not corpus-accuracy evidence.
