# Web service requirements — Thai → Ukrainian

## Product

The website is the public application of the research repository, not a second linguistic model. It has two primary pages: Service and System. The live website uses **FastThaiG2P as its sole Thai pronunciation/G2P engine**.

The Service analyses Thai text and presents FastThaiG2P IPA plus a provisional Ukrainian practical adaptation. It is not a semantic translator.

## Service page

Required: Thai input, examples, clear action, structured status, FastThaiG2P IPA, word/syllable boundaries, tone and vowel length metadata, provisional Ukrainian candidate, warnings, copy controls, System/GitHub links, accessible live result status.

Incomplete upstream IPA must remain visibly distinct from a complete result. Unsupported IPA symbols must withhold the affected Ukrainian candidate. The client must never silently fall back to the former browser engine, RTGS renderer or an orthography-derived heuristic.

## System page

Explain in Ukrainian: purpose; FastThaiG2P as the only site G2P engine; external IPA and the provisional typed-IPA boundary; IPA→Ukrainian adaptation; tones/length; evidence and uncertainty; package/data licensing limits; API hosting; limitations and reproducibility.

## Visual identity

Use a functional Thai visual identity derived from the national flag: deep blue as the structural colour, restrained red accent, white dominant field, neutral text/surfaces. Avoid flag collage, generic AI gradients, excessive glassmorphism, decorative stereotypes, noisy dashboards and excessive rounded cards. Preserve the restrained editorial/typographic character of the Chinese reference project.

## Engineering

The public site is a FastAPI application in `src/index.py`, serving the static `web/` UI and same-origin `/api/analyze` endpoint. The browser is a presentation client; it does not execute a second G2P model. The FastThaiG2P and PyThaiNLP dependencies are pinned. CSP allows same-origin API connections only.

GitHub Pages is static-only and cannot host this Python API. The combined UI/API app must be deployed to a Python-capable host (intended target: Vercel) before the website branch can replace the current Pages deployment. No external Vercel project is created by repository code.

No account or telemetry is introduced by this integration. Thai text is sent to the same-origin API for processing; the UI explicitly tells users not to enter confidential text. Use safe text rendering and explicit unresolved states.

Target WCAG 2.2 AA where practical; static checks do not replace manual keyboard, screen-reader, zoom/reflow and device testing.

## Research gates

The site must not claim corpus accuracy without independent gold, must not claim an official Ukrainian standard, must not mislabel unadjudicated FastThaiG2P IPA as phonemic/broad-surface IPA, and must not silently guess unsupported output. Ukrainian candidates from external IPA remain `PROVISIONAL` pending independent Thai and Ukrainian review.

The upstream package software license does not automatically clear all bundled dictionary/fallback data. Verify exact data provenance, terms and required attribution before public production deployment.

## Release gates

Pinned dependency installation and upstream smoke pass; typed external-IPA and provisional adapter tests pass; FastAPI API tests pass; UI fail-closed tests pass; full repository CI and Web Static pass on exact head; Vercel preview serves static assets and API at one origin; CSP, cold start, error paths and manual accessibility are verified; upstream data rights are documented; System documentation matches implementation; production cutover is explicitly planned.

## Acceptance probes

กา, กาน, กรา, กล้า, คน, เกะ, เก, เกีย, เกา, เกียว, แล้ว, เร็ว, เลย, ขาย, หงา, ไหม, ไหว้, แสดง, plus malformed repeated tone/vowel cases. Also test the previously pinned external Bangkok challenge entry against FastThaiG2P.

These probes are regression fixtures, not corpus-accuracy evidence.
