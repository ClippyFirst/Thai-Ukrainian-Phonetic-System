# Website UX and visual system

**Status (2026-11-06):** merged to `main` through PR [#211](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/211), squash commit `476cb6ed0e4421ab02bb564ff232c99b6c19e008`. Exact-head checks on `8200255df8d7c2cfb4f8aa30d218785e9a625b08` passed: Full CI 42117563464, Web Static 42117563510, Site API 42117563500, Pyodide compatibility 42117563482. Post-merge Pages workflow [42120159047](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42120159047) was still `in_progress` when checked; independent live-page confirmation and manual accessibility/performance acceptance remain open.

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

## Optional RTGS result

The primary result remains the provisional Ukrainian IPA adaptation, with external IPA beside it. A separate RTGS romanization is discoverable directly below as a collapsed native disclosure; it is dynamically imported only when the user opens it. The pinned CC0 word list is shared with the primary native tokenizer and may already be cached or fetched during the main analysis; the RTGS loader still validates the same-origin manifest, version, size and SHA-256. This keeps the additional capability visible without competing with the primary task or loading the optional RTGS module for users who do not request it. RTGS is labelled as a separate romanization method and never feeds the IPA → Ukrainian adapter.

## Interaction contracts

- Selecting a sample fills the input; it does not launch analysis automatically.
- Editing input clears the old result to prevent mismatched text/output.
- A result from an in-flight request is discarded if the input changed before it returned.
- The analyze button is disabled and relabelled while the worker is running.
- The status region reports startup, download, analysis, success and failure without moving focus.
- Copy controls copy the exact displayed string and show a short confirmation.
- Advanced detail remains inside a native details/summary disclosure.
- RTGS is an explicit, collapsed secondary result; it loads only on expansion, uses same-origin integrity-checked assets, and discards results if the input changes while loading.

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

Reviewed snapshots: UI UX Pro Max `b7d5353e0130feb8c5574ef1251f8a1db1873ccb`; Superpowers `22f0b463e7a5e579904dd6211a520321035526f7`; Matt Pocock skills `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`; Ponytail `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846`; Unlazy `16671491f6679ad9378f52604d3bc2415b4120c7`.

These are reviewed upstream references, not vendored code or installed runtime dependencies. UI UX Pro Max's React/Tailwind/shadcn-specific recommendations were not imported because this service is deliberately static HTML/CSS/JS with no framework. Its hierarchy, interaction, accessibility and responsive-design principles were selectively applied.

## Acceptance checklist

- [x] The first viewport's purpose, three-step explanation and input workbench are present in source; static document contract passes. Manual visual review remains open.
- [x] Sample selection, explicit analysis, input clearing, keyboard shortcut, status and fail-closed output are covered by the UI contract. Actual browser clipboard interaction remains unverified manually.
- [x] Editing input invalidates prior output; a delayed stale Worker response is explicitly tested and discarded.
- [x] Ukrainian candidate and external IPA are separate, named result panels; automated UI contract passes.
- [x] Word/syllable, tone, length, warnings and provenance remain in native progressive disclosure; automated UI contract passes.
- [ ] Manual keyboard-only and screen-reader review on the deployed UI, including focus order and announcement quality.
- [ ] Visual reflow review at narrow mobile widths and 200%/400% zoom; source contains responsive breakpoints, but no visual viewport capture was available in this run.
- [x] Static source contrast contract checks 14 selected text pairs against 4.5:1 and the Thai input border against 3:1. This is not a complete contrast audit or WCAG conformance claim.
- [x] Pages/Pyodide worker, same-origin asset and privacy contract preserved; exact-head Pyodide compatibility and Chromium Worker checks pass.
- [x] Exact candidate commit CI, Web Static, Site API and Pyodide compatibility checks pass (see validation matrix).

**Remaining manual acceptance:** keyboard and assistive-technology review, real viewport/zoom reflow, actual clipboard interaction, and deployed mobile cold/warm performance. No WCAG 2.2 AA conformance claim is made.