# Web service requirements — Thai → Ukrainian

## Product purpose

The website is the public browser interface to the research repository, not a semantic translator or a second linguistic model. It helps a visitor inspect FastThaiG2P IPA and a provisional Ukrainian practical adaptation.

## Hosting and runtime

- GitHub Pages is the only public hosting target.
- The application is static HTML/CSS/JavaScript. The existing FastThaiG2P Python service runs in self-hosted Pyodide 0.29.5 inside a same-origin module Web Worker.
- The browser sends text to the worker, not to a server/API. No Vercel, remote FastAPI endpoint, external CDN runtime or alternate JavaScript G2P engine is in the public path.
- Pinned runtime wheels and assets are integrity-checked against the committed manifest before use.
- No accounts, analytics, telemetry or persistence of user-entered text are introduced.

## Primary user journey

1. Understand immediately that the tool assists with reading Thai and does not translate meaning.
2. Paste Thai text or choose a sample.
3. Review the input and explicitly start analysis.
4. Receive progress feedback while the local engine starts and analyzes.
5. Read the Ukrainian candidate first, with the corresponding FastThaiG2P IPA alongside it.
6. Optionally expand word/syllable analysis, tone, vowel length, warnings and upstream provenance.
7. Copy the Ukrainian result or IPA.
8. Understand that the Ukrainian candidate is provisional and verify important words independently.

## Required service-page elements

- Ukrainian-language document, one descriptive H1, skip link, named primary navigation and visible form label.
- Thai input with example buttons, character count, clear action and explicit analyze action.
- Plain-language local-processing/privacy explanation.
- Progress, success, empty-input and failure states through a polite status region.
- Ukrainian candidate and raw IPA with separate copy controls.
- Word/syllable breakdown, tone, vowel length, warnings and engine provenance when returned.
- Provisional/uncertainty disclosure visible beside the result.
- Links to method, evidence, source code, feedback and third-party notices.

## System and legal pages

The System page explains the purpose, the single FastThaiG2P engine, browser/Pyodide execution, IPA-to-Ukrainian adaptation, evidence status, limitations and reproducibility. The legal-notices page discloses the project and third-party runtime/data licenses and attribution.

## Visual and interaction direction

Use a restrained editorial interface: white as the dominant surface, deep blue for structure and primary actions, restrained red for beta/uncertainty accents, neutral high-contrast text, generous spacing and clear typographic hierarchy. Keep the Thai text visually prominent. Prefer meaningful grouping and whitespace over decorative cards, generic gradients, excessive rounding, flag collage or decorative stereotypes.

The service should feel calm, precise and approachable. The Ukrainian candidate is the primary output; IPA is the supporting technical reference. Advanced detail is progressively disclosed rather than shown as a dense dashboard by default.

## Accessibility and responsive behavior

- Preserve keyboard navigation, a skip link, visible focus, programmatic labels and correct heading hierarchy.
- Interactive targets should be at least 44px high where practical, with adequate spacing.
- Maintain at least 4.5:1 text contrast for normal text and 3:1 for meaningful control boundaries/non-text indicators.
- Do not convey status by colour alone; pair status colour with text.
- Respect prefers-reduced-motion, forced-colors/high-contrast mode, browser zoom and text resizing.
- Reflow without horizontal scrolling at narrow widths; retain logical visual and screen-reader order.
- Announce progress and completion without moving focus or repeatedly interrupting the visitor.
- Static tests are not a substitute for hands-on keyboard, screen-reader, zoom/reflow and mobile checks.

## Linguistic and evidence boundaries

- Do not claim independent pronunciation accuracy: IPA gold remains 0 and accuracy remains NOT_MEASURED.
- Do not describe the Ukrainian candidate as an official standard or expert-validated transcription.
- Do not mislabel unadjudicated FastThaiG2P IPA as phonemic or broad-surface IPA.
- Do not silently guess unsupported output or fall back to the legacy research engine/RTGS.
- Do not imply that tone and vowel length are fully preserved in Ukrainian practical spelling.