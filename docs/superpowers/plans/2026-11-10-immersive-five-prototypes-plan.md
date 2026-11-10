# Immersive Five Prototype Directions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add five distinctive, interactive visual prototypes for the Thai–Ukrainian phonetic project without changing production pages.

**Architecture:** Add a standalone comparison page under `web/prototypes/round-2/`. Use scoped CSS and vanilla JavaScript in one self-contained HTML file, following the existing static-site approach. The page switches between five independently art-directed experiences and labels all illustrative demo results.

**Tech Stack:** HTML, CSS, vanilla JavaScript; no added dependencies.

**Spec:** `docs/superpowers/specs/2026-11-10-immersive-five-prototypes-design.md`

## Global Constraints
- Keep `main` unchanged; work only on `design/immersive-five-prototypes-2026-11-10`.
- This is a transcription aid, not a translator.
- Do not claim accuracy is measured or independently validated.
- Clearly label all mock/demo outputs as illustrative and not real engine results.
- Keep local-processing and privacy claims aligned with the actual service.
- Support keyboard, touch, mobile, and reduced-motion preferences.

## Review Focus
- A very long Thai string must wrap without clipping in every concept.
- Empty input must not reveal a fabricated result.
- Touch users must be able to access information without cursor hover.
- Reduced-motion users must retain the same information and navigation.
- Narrow viewports must not hide the active concept navigation or primary input.

---

### Task 1: Add the five-direction prototype comparison page

**Files:**
- Create: `web/prototypes/round-2/index.html`

**Interfaces:**
- Each concept section is keyed by a stable data attribute.
- Concept switcher changes the active scene and updates accessible pressed state.
- Example controls populate the associated Thai textarea.
- Demo action reveals only clearly labeled illustrative content; it does not call the production engine.

- [ ] **Step 1: Write the failing structural checks**
  - Check that the document contains exactly five concept roots with the required IDs.
  - Check that each concept has a Thai input, example action, and demo action.
  - Check for reduced-motion CSS, keyboard focus styling, and touch fallback.
  - Check that the disclaimer explicitly says demo values are not engine output.

- [ ] **Step 2: Run checks before implementation**
  - Expected: the target file does not exist and checks fail for missing file/content.

- [ ] **Step 3: Implement the standalone HTML/CSS/JS page**
  - Give each concept a distinct signature interaction: spotlight reveal, fluid field, constellation, portal navigation, knowledge graph.
  - Use transform/opacity/clip/mask effects where appropriate; avoid animating layout dimensions.
  - Keep semantic buttons, labels, live status, and keyboard-operable navigation.

- [ ] **Step 4: Run structural checks and static validation**
  - Verify five concept roots, all controls, truthful demo disclaimer, reduced-motion and responsive rules.
  - Check HTML parseability and JavaScript syntax.
  - Expected: all structural checks pass with no syntax errors.

- [ ] **Step 5: Commit**
  - Commit the prototype page and this spec/plan on the isolated design branch.

### Task 2: Verify repository isolation and deliverable

**Files:**
- Read: `web/prototypes/round-2/index.html`
- Read: `docs/superpowers/specs/2026-11-10-immersive-five-prototypes-design.md`
- Read: `docs/superpowers/plans/2026-11-10-immersive-five-prototypes-plan.md`

- [ ] **Step 1: Verify branch and changed paths**
  - Expected: only the new prototype and planning documents changed; `main` is untouched.

- [ ] **Step 2: Verify prototype source**
  - Expected: all five directions, input controls, accessible states, disclaimers, and reduced-motion support are present.

- [ ] **Step 3: Provide the exact branch preview link**
  - State clearly that the engine is not connected and that GitHub Pages does not publish an unmerged branch.
