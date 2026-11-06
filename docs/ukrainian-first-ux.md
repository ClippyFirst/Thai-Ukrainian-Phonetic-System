# Ukrainian-first UX

**Status:** implementation in progress; see the latest validation-matrix and handoff entries for exact-head CI evidence.

## Product rule

Ukrainian is the default language for every user-facing interaction on the public service, not only for static page copy. This includes:
- input guidance, buttons, progress, success and empty states;
- validation, analysis, runtime, network and clipboard errors;
- warnings returned by Python packages or the G2P engine;
- dynamically rendered result labels and provenance captions;
- accessible names, status announcements, summaries and help text;
- the GitHub beta feedback form, including its categories, field labels, safety guidance and privacy confirmation.

Technical product names and notation (FastThaiG2P, Pyodide, Web Worker, IPA, RTGS) remain unchanged where they are proper names or established notation. Explain them in Ukrainian instead of translating the identifiers.

## Error-handling contract

The browser Worker sends a stable error `code` and a separate technical `diagnostic`. It does not forward an upstream `detail.message` or raw exception text as user copy.

The UI resolves the code through `web/src/messages.uk.js`:
- `ERROR_MESSAGES` maps known error codes to a stable public support ID and Ukrainian explanation;
- unknown codes use a generic Ukrainian message;
- diagnostics appear only in a collapsed disclosure after an error;
- the worker redacts the exact input string from exception diagnostics before posting them to the page;
- editing or clearing the input hides stale diagnostics.

Current error groups:
- `UA-LOAD-*`: runtime bundle download, configuration and integrity;
- `UA-ANALYSIS-*`: unsupported/incomplete IPA or inconsistent engine output;
- `UA-SYSTEM-*`: unexpected worker/runtime failure;
- `UA-CLIPBOARD-*`: clipboard permission or browser failure.

The support ID is safe to quote in a feedback report. The diagnostic panel is optional and intended for troubleshooting; it must not contain the text entered by the user.

## Warning localization

Warnings from the phonetic adapter may be technical or English. The result renderer maps known warning classes to Ukrainian explanations and uses a conservative generic Ukrainian warning for unrecognized strings. It never treats an unknown warning as evidence of correctness.

## Automated acceptance

The Web Static workflow runs:
- JavaScript syntax checks for the UI, localization catalog and Worker;
- `web/tests/ukrainian-first.test.mjs` to validate catalog language, stable unique IDs, generic fallback, and the boundary between user copy and diagnostics;
- `web/tests/ui-contract.test.mjs` to validate localized upstream errors/warnings, stale-result behavior and fail-closed handling;
- `web/tests/accessibility-contract.test.mjs` for static labels, landmarks, announcements, keyboard focus, contrast pairs and reduced-motion source contracts.

These tests are source-level contracts. They do not establish manual screen-reader usability, browser clipboard permission behavior, mobile performance, or WCAG conformance.

## Remaining product work

| Item | State | Acceptance |
|---|---|---|
| Central Ukrainian error catalog and code-only UI mapping | IMPLEMENTED_PENDING_CI | Exact-head Web Static and Full CI pass; test every known error branch in browser |
| Optional technical diagnostics with input redaction | IMPLEMENTED_PENDING_CI | Tests prove raw upstream message is not user copy and input is redacted |
| Localize warnings and provenance caption | IMPLEMENTED_PENDING_CI | UI contract proves no raw English warning/provenance caption is rendered |
| Audit every public page and all accessible text | TODO | Inventory all visible strings, aria labels, placeholders, titles, feedback form and third-party notices; retain English only for proper names/legal source titles |
| Manual mobile/keyboard/screen-reader/zoom acceptance | DEFERRED / NOT VERIFIED | Real-browser checks at narrow widths and 200%/400% zoom; keyboard-only and assistive-technology review |
| Privacy explanation page | TODO / EVIDENCE REQUIRED | Verify current GitHub Pages request/logging practices and explain local input processing, storage and telemetry accurately |
| User feedback workflow | IMPLEMENTED_PENDING_CI | GitHub beta feedback form is now Ukrainian; it warns against sharing private data and makes examples optional. Confirm the workflow and template render correctly. |
| Glossary and plain-language phonetics help | TODO | Ukrainian explanations of IPA, tones, vowel length, syllables and adaptation limitations, reviewed for linguistic accuracy |

## Out of scope for this UX change

This work does not change Thai phonological rules, IPA values, Ukrainian adaptation rules, corpus labels, evidence grades or accuracy claims. It does not add analytics, local storage, remote APIs, runtime dependencies or an English-language mode. Linguistic accuracy remains unmeasured and the Ukrainian output remains provisional.
