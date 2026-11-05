# Website UX and visual system

**Status:** implementation brief and acceptance reference for the browser beta. This document describes the deployed Pages product, not a proposed second application.

## Design intent

The service should feel like a small, precise language tool: editorial rather than dashboard-like, friendly without being childish, and technical without exposing research complexity before it is useful.

The primary job is simple: enter Thai text, request analysis, read the Ukrainian candidate, and optionally inspect IPA and syllable detail. The interface should make that sequence obvious.

## Visual language

- Surface: white is dominant; pale neutral wash separates supporting regions.
- Structure: deep indigo/blue carries navigation, section hierarchy, focus and the primary action.
- Caution: muted red is reserved for beta and uncertainty states; never use colour alone to communicate them.
- Typography: system sans-serif for interface text; Thai-capable system fallback for the input; IPA-capable fallback stack for phonetic output. No remote font or icon dependency.
- Geometry: mostly square corners and fine borders; use spacing and rules rather than nested rounded cards.
- Composition: wide editorial hero with a compact three-stage explanation, followed by a single focused input workbench and a two-column result feature area that collapses to one column on small screens.

## Information hierarchy

1. Purpose: read Thai text in Ukrainian letters; explicitly say it is not translation.
2. Trust: local browser processing and a concise beta notice.
3. Action: Thai input, examples, character count, clear action and explicit analyze action.
4. Primary result: Ukrainian practical candidate, labelled provisional.
5. Technical evidence: raw FastThaiG2P IPA beside the candidate.
6. Progressive detail: word/syllable breakdown, tone, vowel length, warnings and engine provenance.
7. Support: method, evidence, feedback, GitHub and legal notices.

## Interaction contracts

- Selecting a sample fills the input; it does not launch analysis automatically.
- Editing input clears the old result to prevent mismatched text/output.
- A result from an in-flight request is discarded if the input changed before it returned.
- The analyze button is disabled and relabelled while the worker is running.
- The status region reports startup, download, analysis, success and failure without moving focus.
- Copy controls copy the exact displayed string and show a short confirmation.
- Advanced detail remains inside a native details/summary disclosure.

## Responsive rules

- Desktop: hero copy and the three-stage explainer sit side by side; Ukrainian and IPA results sit side by side.
- Tablet/mobile: hero and result regions stack; controls become full-width; helper text and character count wrap without clipping.
- No fixed-width page containers, horizontal content scrolling, hover-only interactions or disabled browser zoom.

## Engineering boundaries

- Keep the static Pages/Pyodide/Web Worker architecture.
- Do not add a framework, design-system runtime, CSS library, remote asset, icon package or font dependency for this redesign.
- Preserve the existing worker protocol, result schema, privacy contract, engine provenance, IPA labels, warning behavior and fail-closed handling.
- Keep rendering escaped; never interpolate raw Thai input or upstream output into HTML without the esc function.

## Adopted upstream practices

- UI UX Pro Max: accessibility and interaction first, then responsive composition, typography, colour and progressive disclosure. Product-specific editorial direction above takes precedence over generic style presets.
- Superpowers: define the intended user journey before implementation, test the interaction contract first, then implement a minimal vertical slice and verify the complete flow.
- Matt Pocock skills: preserve small interfaces and existing architecture; avoid installing a process framework or expanding scope without evidence.
- Ponytail: review correctness, security, load, missing tests, speed and unnecessary code; every finding must have a concrete failure case.
- Unlazy: use observable acceptance gates and report only evidence-backed completion. The repository's existing matrix and handoff remain canonical; no second gate system is installed.

References: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill, https://github.com/obra/superpowers, https://github.com/mattpocock/skills, https://github.com/DietrichGebert/ponytail, https://github.com/Leonxlnx/unlazy.

These are reviewed upstream references, not vendored code or installed runtime dependencies.

## Acceptance checklist

- [ ] The first viewport explains the tool and exposes the input without hunting.
- [ ] A visitor can select an example, edit input, run analysis and copy either output.
- [ ] Editing input cannot leave a stale result presented as current.
- [ ] Ukrainian candidate and IPA are visually distinct and correctly labelled.
- [ ] Word/syllable, tone, length, warning and provenance detail remain accessible.
- [ ] All actions work with keyboard only and have visible focus.
- [ ] Layout reflows at narrow viewport widths without horizontal scrolling.
- [ ] Text and control contrast checks pass; manual accessibility review is still recorded separately.
- [ ] The Pages/Pyodide worker and privacy contract are unchanged.
- [ ] CI passes on the exact candidate commit.