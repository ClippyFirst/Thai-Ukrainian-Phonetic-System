# Web service architecture

## Goal

Expose the Thai → Ukrainian research engine as a browser service while retaining a single linguistic source of truth.

## Architecture

Thai input
→ browser adapter
→ generated research data/runtime
→ Thai graphemic analysis
→ syllable + phonology + tone
→ broad IPA
→ surface IPA when supported
→ Ukrainian feature candidates
→ Ukrainian practical orthographic candidates
→ presentation model
→ Service UI

The System page consumes documentation metadata only; it contains no conversion rules.

## Logical layout

web/
  index.html
  system.html
  src/
    app.js
    styles.css
    ui.js
    adapter.js
  generated/
  tests/

Authoritative linguistic data remain under data/thai/ and the Python package. Browser artefacts are derived.

## Single source of truth

A generated manifest should record source version/commit, generator version, source hashes and generated artefact hashes. The UI must never maintain a hand-edited duplicate mapping table.

## Runtime

Preferred: compile the deterministic research rules into a browser-safe runtime.

Fallback: if a complete browser port would duplicate or distort the research implementation, use a documented API adapter and do not claim static offline equivalence.

## Error model

The UI consumes structured statuses:
- analyzed
- invalid:tone-combination
- unresolved
- unsupported
- analysis-dependent

Warnings are first-class data.

## Presentation contract

Each result may expose:
input; Thai decomposition; tone; phonemic IPA; conservative surface IPA; Ukrainian feature candidates; Ukrainian orthographic candidates; selected candidate; warnings; evidence/status metadata.

Presentation components never infer missing linguistic data.

## Pages

/ — Service
/system.html — System

## Deployment

Primary target: GitHub Pages/static hosting.

No server is required only if browser parity is achieved. Otherwise deployment must explicitly state its backend requirement.

## QA

Automated:
build, unit tests, browser smoke tests, Python↔browser parity fixtures, accessibility assertions and deterministic generated-artifact checks.

Manual:
desktop, mobile, keyboard-only, screen-reader result announcement, unresolved input, copy controls and System-page readability.

## Research boundary

Website presentation quality cannot turn an analysis-dependent rule into an empirical fact.
