# Web UX and accessibility audit — 2026-10-08

## Scope

This is a **static/code-level audit** of the two-page research service:

- \`web/index.html\` — Service;
- \`web/system.html\` — System;
- \`web/src/app.js\` — interaction and result rendering;
- \`web/src/styles.css\` — visual and responsive layer.

A screenshot-based browser audit is intentionally not claimed because the required browser capture surface was unavailable in this execution environment.

## Product contract

The interface has one primary job: accept Thai orthographic input and expose a transparent analysis chain without disguising uncertainty as a successful transliteration.

The UI therefore follows four product rules:

1. deterministic results are visually distinct from unresolved/analysis-dependent/invalid results;
2. the input contract is explicit: a single syllable or explicitly space-separated syllables;
3. the browser is a presentation/runtime layer, not an independent linguistic source of truth;
4. the System page explains why an apparently incomplete result can be scientifically preferable to a guessed one.

## Closed UX findings

### 1. Input affordance

**Closed.** The textarea now has an explicit visible label, Thai language metadata, spellcheck/autocomplete suppression, a concise segmentation hint, and a documented Ctrl/⌘ + Enter shortcut.

### 2. Examples

**Closed.** Example buttons are real buttons with explicit \`type="button"\`, keyboard focus, and immediate analysis. The examples intentionally include both ordinary and adversarial constructions.

### 3. Result hierarchy

**Closed.** Results now have semantic headings, a stable per-result title, a large Thai source string, a human-readable status description and the machine status code.

### 4. Uncertainty communication

**Closed.** Non-deterministic states no longer resemble empty successful results. They receive a dedicated explanation panel and retain the research-core warning.

### 5. Copy interaction

**Closed.** Copy controls are real buttons, use the Clipboard API when available, and provide immediate textual feedback.

### 6. Responsive behaviour

**Closed at code level.** The two-column data and status grids collapse to one column on small screens; navigation wraps rather than overflowing; large Thai text scales down.

### 7. Keyboard and focus

**Closed at code level.** Interactive elements have explicit visible focus treatment. The main input supports keyboard analysis without requiring a pointer.

### 8. Reduced motion

**Closed at code level.** The stylesheet disables transitions/scroll animation under \`prefers-reduced-motion: reduce\`.

## Research-integrity checks

The UI does not claim:

- corpus accuracy;
- automatic lexical segmentation;
- an official Ukrainian transliteration standard;
- deterministic pronunciation for evidence-gated special orthography.

The Service and System pages use the same v0.5.1 release label.

## Remaining evidence limits

A static audit cannot establish:

- actual visual rendering at multiple viewport sizes;
- screen-reader output in a real browser;
- keyboard traversal order as experienced by assistive technology;
- clipboard behaviour under browser permissions;
- GitHub Pages deployment availability;
- font rendering quality for all Thai/Ukrainian environments.

These require browser/device execution. They are not silently converted into a “PASS”.

## Verdict

**Static product quality: release-ready.**

The remaining uncertainty is environmental rather than an identified UI defect. The repository should retain the explicit distinction between static accessibility evidence and a future screenshot/browser audit.
