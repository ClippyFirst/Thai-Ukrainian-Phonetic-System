# FastThaiG2P website integration

**Decision (2026-11-04):** the public website uses FastThaiG2P as its single pronunciation engine. The site displays a Ukrainian practical rendering from FastThaiG2P's IPA, but labels that rendering as provisional until independent phonetic and Ukrainian-native review is complete.

## Runtime contract

- Upstream engine: `awslabs/FastThaiG2P` at immutable commit `4e82a291b4cf2876326744c6580121e9986ad354`.
- Python dependency set: FastThaiG2P plus PyThaiNLP `5.4.0` and FastAPI `0.117.1`.
- Entry point: `src/index.py`; FastAPI serves both the same-origin API and the `web/` static assets.
- API: `POST /api/analyze` and `GET /api/health`.
- The browser has no second G2P implementation and makes no fallback call. Incomplete upstream IPA is a visible error.

## IPA and Ukrainian boundary

FastThaiG2P's output is not independently adjudicated as phonemic or broad-surface IPA. The adapter therefore retains segmental IPA in `PhoneticResult.external_ipa` and leaves `phonemic_ipa` and `broad_surface_ipa` unset. A result with supported symbols is marked `PROVISIONAL`; the existing IPA→Ukrainian mapping may produce a candidate only from that separate external IPA field. Unsupported symbols still withhold output.

The UI shows:
- raw FastThaiG2P IPA, including syllable separators and tone notation;
- Ukrainian practical candidate;
- tone, vowel length, word/syllable groups and engine provenance;
- an explicit notice that the Ukrainian candidate is provisional and not expert-validated.

This is not an accuracy claim. The 42-item challenge contains no independently adjudicated IPA gold. Existing cross-engine agreement and coverage diagnostics remain comparator evidence only.

## License and provenance gate

The pinned upstream software declares Apache-2.0. That does not automatically settle the rights and attribution for all dictionary/fallback data shipped inside the package. Upstream documentation describes a mixed dictionary containing manual overrides, Wiktionary-derived entries and LLM-generated entries; the fallback parser also carries its own BSD-3-Clause notice.

Before public production deployment, verify the exact pinned package's bundled data files, provenance, applicable terms and attribution/share-alike obligations. Do not copy its dictionary or fallback data into this repository. This integration pins and installs the upstream package as a dependency; it does not claim that all bundled data is independently cleared for redistribution or commercial use.

## Deployment gate

GitHub Pages is static-only and cannot execute this Python application. The FastAPI app is intended for Vercel's Python runtime, which recognizes `src/index.py` as an application entrypoint. Vercel's documentation confirms Python runtime support and the `src/index.py` FastAPI entrypoint convention ([Python runtime](https://vercel.com/docs/functions/runtimes/python), [FastAPI on Vercel](https://vercel.com/docs/frameworks/backend/fastapi)).

At the time of this branch, the linked Vercel account has no project linked to this repository. Creating/connecting a Vercel project and changing the public deployment/domain are external deployment actions; they are intentionally not performed in this implementation branch. Until a project is connected and a preview deployment passes the site/API smoke tests, the existing GitHub Pages deployment must remain unchanged and this branch must not be merged into `main`.

## Verification

Run:

```bash
python -m pip install -e ".[dev,fastthaig2p]"
python -m pytest -q tests/test_fastthaig2p_adapter.py tests/test_fastthaig2p_site_api.py
node web/tests/ui-contract.test.mjs
node web/tests/accessibility-contract.test.mjs
node web/tests/ipa-ua.test.mjs
```

The dedicated GitHub Actions workflow runs the pinned upstream smoke test and these targeted checks. Local execution in a connector-only environment is not claimed.
