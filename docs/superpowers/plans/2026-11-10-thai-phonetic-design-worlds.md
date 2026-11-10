# Five Distinct Thai Phonetic Design Concepts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the existing generic prototype gallery with five distinct, expressive, usable visual concepts for the Thai–Ukrainian phonetic reading service.

**Architecture:** Keep the existing single-file static gallery at `web/prototypes/index.html` so the current branch URL remains the review surface. Implement five isolated concept sections, shared accessible switcher behavior, and explicitly demo-only interactions in vanilla HTML/CSS/JS; no engine or production-page changes.

**Tech Stack:** Static HTML, CSS custom properties, vanilla JavaScript, inline SVG/CSS visuals; no dependencies or external network requests.

**Spec:** `docs/superpowers/specs/2026-11-10-thai-phonetic-design-worlds.md`

## Global Constraints
- Work only on `design/five-concepts-2026-11-10`; never modify `main`.
- Thai input remains local; this gallery does not submit input or call the transcription engine.
- Every example result is visibly marked as illustrative demo content.
- Preserve Thai → IPA → Ukrainian as the conceptual transformation; never imply direct orthographic substitution.
- Do not claim measured accuracy, expert validation, or measured audio.
- Support responsive layout, keyboard focus, and `prefers-reduced-motion`.

## Review Focus
- Long Thai text and mixed Thai/Latin punctuation remain readable and do not overflow.
- Narrow screens keep switcher, input, and results usable without horizontal scrolling.
- Reduced-motion users still understand the explanatory sequence without animated movement.
- Switching concepts does not leave multiple panels exposed or stale active controls.
- Demo interactions never imply the real engine ran or that output is validated.

---

### Task 1: Replace the prototype gallery

**Files:**
- Modify: `web/prototypes/index.html`

**Interfaces:**
- Consumes: existing static gallery URL and project truth from `web/index.html`, `web/transcription.html`, `web/system.html`.
- Produces: five independently styled `[data-concept]` sections and shared `[data-switch]` controls; each concept has `[data-example]`, `[data-analyze]`, `[data-clear]`, `[data-demo-result]` hooks.

- [ ] Step 1: Define manual acceptance checks for five concept identifiers, accessible switcher state, demo disclaimers, reduced-motion rules, and no network/form submission.
- [ ] Step 2: Confirm the current file fails the new concept-name and disclaimer checks (RED).
- [ ] Step 3: Replace the gallery with the five concepts and vanilla interactions.
- [ ] Step 4: Re-run structural checks and validate every selector/ID, unique concept, demo label, mobile breakpoint, reduced-motion block and absence of form submission/network calls (GREEN).
- [ ] Step 5: Commit the prototype update.

### Task 2: Document the handoff

**Files:**
- Create: `docs/superpowers/specs/2026-11-10-thai-phonetic-design-worlds.md`
- Create: `docs/superpowers/plans/2026-11-10-thai-phonetic-design-worlds.md`

**Interfaces:**
- Consumes: user-approved five visual directions and product constraints.
- Produces: durable design rationale and implementation/acceptance plan.

- [ ] Step 1: Add the approved design spec and implementation plan.
- [ ] Step 2: Verify both files are present on the design branch.
- [ ] Step 3: Commit documentation.

## Review Focus
- Treat this as a static visual decision artifact, not a production integration.
- If browser rendering cannot be inspected in this environment, report that limitation explicitly rather than claiming visual QA.
