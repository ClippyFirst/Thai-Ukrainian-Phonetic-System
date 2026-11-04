# Web service architecture

## Production site runtime

The website uses **FastThaiG2P as its sole Thai pronunciation/G2P engine**. The browser does not run the ClippyFirst grapheme-to-phonology engine, RTGS renderer, heuristic fallback, or a second pronunciation engine.

Data flow:

`Thai text → same-origin FastAPI endpoint → pinned FastThaiG2P → raw external IPA → typed external-IPA boundary → existing IPA → Ukrainian adapter → provisional Ukrainian practical spelling → browser presentation`.

The FastThaiG2P output is retained as raw IPA. Because its mixed dictionary/OOV output has not been independently adjudicated as phonemic or broad-surface IPA, it is represented in `PhoneticResult.external_ipa`; it is never mislabeled as either canonical IPA layer. The Ukrainian adapter may consume this field only when the typed result is explicitly `PROVISIONAL`. Unknown symbols and incomplete/passthrough output remain fail-closed.

The Ukrainian result is explicitly provisional, not expert-validated and not an official Ukrainian transcription standard. Tone and vowel length remain separately visible in IPA/metadata and may be neutralized in Ukrainian practical spelling.

## API and hosting

- `src/index.py` exports the FastAPI application and serves `web/` static assets.
- `POST /api/analyze` accepts JSON `{"text":"..." }` and returns the pinned FastThaiG2P IPA, provisional Ukrainian output, word/syllable groups, tone, length, provenance and warnings.
- `GET /api/health` identifies the active engine.
- `requirements.txt` pins FastAPI, PyThaiNLP and FastThaiG2P at an immutable upstream commit.
- The browser calls only same-origin `/api/analyze`; CSP allows same-origin connections only.

The GitHub Pages deployment is static-only and cannot execute this Python API. The new combined FastAPI/static application must be deployed to a Python-capable host (the implementation targets Vercel's Python runtime) before this branch can replace the currently published GitHub Pages site. No Vercel project is currently linked to this repository; project creation/connection and production-domain cutover remain external deployment actions and are not performed by this code change.

## Failure policy

- No fallback to the previous browser engine, RTGS, orthographic heuristics or another G2P provider.
- Incomplete upstream IPA returns an explicit API error; the UI shows the error instead of inventing a partial Ukrainian string.
- Unsupported IPA symbols withhold the affected Ukrainian candidate.
- Every displayed Ukrainian result carries a provisional warning and pinned engine provenance.

## QA

Automated: pinned upstream smoke test, typed external-IPA tests, provisional IPA→Ukrainian adapter tests, API contract tests, UI fail-closed tests, static accessibility checks and the repository's existing Python/browser regression suite.

Manual: desktop/mobile, keyboard-only, screen-reader result announcements, API failure, unsupported IPA, cold-start latency, and hosting/deployment verification.

UI quality cannot upgrade an unadjudicated external IPA result into phonetic gold.
