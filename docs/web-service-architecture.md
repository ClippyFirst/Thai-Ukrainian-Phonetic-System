# Web service architecture

## Deployed product

The public website is a static GitHub Pages application. Thai analysis runs locally in the visitor's browser through a module Web Worker that initializes the self-hosted Pyodide runtime and invokes the shared Python FastThaiG2P service.

The public site does not call a remote API, FastAPI endpoint, CDN-hosted runtime, Vercel function, or a second JavaScript pronunciation engine.

## Runtime flow

Browser UI (web/index.html + web/src/app.js)
  → Thai text via Worker.postMessage
  → module Web Worker (web/src/fastthaig2p-worker.js)
  → self-hosted Pyodide 0.29.5 + pinned wheels
  → thai_ukrainian.fastthaig2p_service
  → FastThaiG2P adapter
  → typed external-IPA result and provenance
  → IPA-to-Ukrainian provisional adaptation
  → worker result message and escaped DOM rendering

- web/index.html is the public service entry point.
- web/src/app.js owns input interaction, worker requests, status messages, safe result rendering, copy controls and progressive disclosure.
- web/src/fastthaig2p-worker.js owns Pyodide startup, same-origin runtime/wheel loading, manifest and SHA-256 checks, package installation and worker message transport.
- src/thai_ukrainian/fastthaig2p_service.py is the shared transport-neutral analysis function called by both the browser worker and the optional FastAPI reference wrapper.
- src/index.py and FastAPI remain useful for local/API testing, but are not part of the deployed Pages request path.
- web/src/engine.js and RTGS renderers remain research/reference code. They are not site fallbacks.

## Data and privacy contract

- Thai text is sent from the page to a same-origin module worker using postMessage; it is not sent to a server.
- Runtime assets and pinned wheels are served from the Pages origin. The worker checks the committed bundle manifest and package hashes before installing the local wheels.
- Content Security Policy is restrictive and allows only same-origin scripts, styles, workers and connections plus the WebAssembly execution capability required by Pyodide.
- No account, analytics, telemetry, or user-text persistence is introduced by the website.
- Dynamic output is inserted only after escaping untrusted values. Unsupported or incomplete IPA is withheld; no legacy-engine or RTGS fallback is allowed.

## Output contract

The website uses FastThaiG2P as its sole pronunciation/G2P engine. Its IPA is retained as unclassified external IPA until independently adjudicated; it must not be relabelled as canonical phonemic or broad-surface IPA. The Ukrainian string is a provisional practical adaptation of that IPA, not an official Ukrainian standard or expert-validated transcription.

The result view preserves:
- complete raw IPA and segmental IPA where supplied;
- word and syllable grouping;
- tone and tone-IPA metadata;
- vowel length;
- engine/upstream provenance;
- warnings and explicit provisional status.

The UI must not imply that Ukrainian spelling retains every Thai tone or length distinction.

## Failure and interaction policy

- Empty input produces a clear inline prompt.
- Worker startup, download and analysis progress are announced through one polite status region.
- Incomplete upstream IPA produces an explicit error; the site does not switch engines.
- Editing the input invalidates the previously displayed result so that old output cannot be mistaken for the new text.
- Selecting an example fills the input; the visitor explicitly starts analysis.
- If the input changes while an analysis is in flight, the returned result is discarded and the visitor is asked to rerun it.
- Copy actions provide visible confirmation and retain accessible names.
- Keyboard operation, visible focus, reduced-motion preferences, responsive reflow and high-contrast mode are preserved.

## Verification

The public workflow is defined in .github/workflows/pages.yml; browser and UI contracts are in web/tests/. The Pyodide compatibility workflow validates CPython parity and the real worker in Chromium. Static UI checks do not establish WCAG 2.2 AA conformance; manual keyboard, screen-reader, zoom/reflow and mobile testing remain separate evidence gates.

Current live publication: https://clippyfirst.github.io/Thai-Ukrainian-Phonetic-System/.