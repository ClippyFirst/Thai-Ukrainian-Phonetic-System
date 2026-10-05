# Web service architecture

## Data flow

Thai input → browser adapter → generated research runtime → graphemic analysis → syllable/phonology/tone → broad IPA → surface IPA → Ukrainian candidates → practical orthography → presentation model → Service UI.

The System page consumes documentation metadata only and contains no conversion rules.

## Source of truth

Authoritative registries remain under data/thai and the Python package. Browser artefacts are generated. A generated manifest should record source version/commit, generator version, source hashes and generated hashes.

## Runtime policy

Preferred: compile the deterministic research rules into a browser-safe runtime. A fallback backend adapter is acceptable only if fully documented; it must not be presented as static offline equivalence.

## Structured result contract

A result may contain: input; Thai decomposition; tone; phonemic IPA; conservative surface IPA; Ukrainian feature candidates; Ukrainian orthographic candidates; selected candidate; warnings; evidence/status metadata.

Statuses include analyzed, invalid:tone-combination, unresolved, unsupported and analysis-dependent families.

Presentation never infers missing linguistic data.

## Pages and deployment

/ — Service
/system.html — System

Primary deployment target: GitHub Pages/static hosting, only after browser/reference parity is demonstrated.

## QA

Automated: build, unit tests, browser smoke tests, Python↔browser parity, accessibility assertions and deterministic generated-artifact checks.

Manual: desktop/mobile, keyboard-only, result announcement, unresolved input, copy controls and System-page readability.

UI quality cannot upgrade an analysis-dependent rule into an empirical fact.
