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

The pinned upstream repository includes an Apache-2.0 software LICENSE and an Amazon NOTICE. Its own `data/README.md` says the runtime dictionary is 62k words, with IPA merged from manual overrides, approximately 13k Wiktionary/kaikki entries and approximately 49k LLM-generated entries (Claude Opus 4.6 via Bedrock). The generated source file is gitignored upstream. The same README identifies fallback G2P data as vendored from TLTK; the vendored `_th2ipa.py` source carries a BSD-3-Clause notice and 2018 Chulalongkorn University copyright.

The upstream package build force-includes `data/dict.txt`, `data/ipa.json` and `data/fallback/` into the installed wheel. Its data README does not give a separate comprehensive license statement for all these runtime data assets. The software Apache-2.0 license and the TLTK source notice do not automatically resolve the rights/attribution of the manual, Wiktionary-derived, generated IPA and fallback data.

Before public production deployment, inspect the exact pinned wheel and bundled files, determine applicable terms for each source and record attribution/share-alike obligations. Do not copy its dictionary or fallback data into this repository. This integration pins and installs the upstream package as a dependency; it does not claim that all bundled data is independently cleared for redistribution or commercial use.

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


## Exact pinned upstream artifact review — 2026-11-04

The upstream repository was inspected at the exact runtime pin
`4e82a291b4cf2876326744c6580121e9986ad354`, not only at its moving default
branch:

- `LICENSE` is Apache License 2.0.
- `NOTICE` states: Copyright Amazon.com, Inc. or its affiliates.
- `data/README.md` says the runtime `dict.txt` and `ipa.json` comprise a
  62k-word dictionary; the merged IPA source is manual overrides, roughly 13k
  Wiktionary/kaikki entries and roughly 49k LLM-generated entries. The
  generated source JSON is gitignored upstream, but its merged output is
  included in the runtime `ipa.json`.
- The same data README identifies the fallback data directory as vendored
  from TLTK. The pinned `pyproject.toml` force-includes `data/dict.txt`,
  `data/ipa.json` and `data/fallback/` in the wheel.
- The pinned `fastthaig2p/_th2ipa.py` contains a BSD 3-Clause notice and
  2018 Chulalongkorn University copyright.
- The data README does not state one comprehensive license grant covering
  every runtime dictionary, generated IPA and fallback data asset. The
  software Apache-2.0 license and the vendored source-file BSD notice do not
  resolve the provenance/rights of every bundled data record.

**Disposition:** the data-rights gate remains BLOCKED. Obtain explicit
source-by-source rights and required attribution/share-alike terms before
production use. No dictionary, IPA JSON or fallback data was copied into this
repository.

## Vercel feasibility check — 2026-11-04

Official Vercel documentation confirms that its Python runtime supports
FastAPI and explicitly recognizes `src/index.py` as an application
entrypoint. The connected Vercel account currently has zero projects linked
to this repository. This verifies framework/entrypoint feasibility, not a
successful deployment.

The preview must still verify that the current FastAPI `StaticFiles` mount
serves the complete `web/` UI and assets alongside `/api/health` and
`/api/analyze`, with same-origin CSP, correct errors and acceptable cold
starts. Until that preview exists, the static GitHub Pages deployment must
remain unchanged.


## Additional source-license findings — 2026-11-04

The Wiktionary portion needs its own source-level treatment. FastThaiG2P's pinned data README identifies `sources/wiktionary_ipa.json` as roughly 13k entries parsed from a kaikki.org Thai Wiktionary dump. Wiktionary's published copyright terms state that entry text is available under CC BY-SA 4.0. A separate PyThaiNLP Thai G2P Wiktionary corpus declares CC BY-SA 3.0, but the available evidence does not establish that this separate corpus is the exact source file used by FastThaiG2P; do not substitute its license/version as provenance for the pinned package. The exact kaikki snapshot/revision and record-level attribution are still required.

The TLTK fallback has a similar source-identification gap. The vendored `_th2ipa.py` header identifies TLTK 1.3.8 and carries a BSD-3-Clause notice; PyPI's TLTK project history says the package license changed to BSD-3-Clause from 1.2.2 and describes commercial use. However, the current `attapol/tltk` repository root `LICENSE` contains LGPL-3 text while its `setup.py` declares BSD-3-Clause. FastThaiG2P does not pin the precise TLTK source revision for each bundled fallback data file. This conflicting repository/package evidence is not sufficient to make a definitive asset-by-asset conclusion.

**Updated disposition:** the TLTK code notice is identified, but fallback data rights remain unresolved until the upstream maintainer identifies the exact TLTK version/revision and confirms the terms covering the shipped data files. The Wiktionary subset needs its exact source snapshot and attribution. The generated IPA and manual overrides also need an explicit data-rights statement.

## Updated Vercel static-asset behavior — 2026-11-04

A newer Vercel platform change resolves the earlier uncertainty about whether this app must move its frontend into `public/`. Vercel's 2026-09-10 changelog states that FastAPI frontends and `StaticFiles` mounts are promoted to the Vercel CDN at build time; the original source directories remain in the function bundle unless explicitly excluded. It also preserves FastAPI route declaration order relative to a `StaticFiles` mount. This directly covers the app's existing `app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")` pattern, so a separate public-directory migration is not justified by the current evidence.

Primary platform reference: https://vercel-docs.vercel.sh/changelog/fastapi-frontends-and-static-files-served-from-the-cdn (2026-09-10). The older FastAPI deployment page still recommends `public/**` for generic static assets; the newer dated changelog specifically documents the FastAPI `StaticFiles` promotion behavior and is the more directly applicable source.

**Updated disposition:** static-asset architecture is platform-supported; it is no longer an independent design blocker. The hosting gate remains BLOCKED only because no Vercel project is connected and no preview deployment exists. Preview acceptance still requires checking the homepage, `/system.html`, all referenced JS/CSS/assets, `/api/health`, successful and failing `/api/analyze`, same-origin CSP, cold starts and the final function bundle size. Keep GitHub Pages unchanged until those live checks pass.


## Upstream lexical correction regression

The pinned FastThaiG2P commit is the merge commit of upstream [PR #3](https://github.com/awslabs/FastThaiG2P/pull/3), which corrected the dictionary IPA for `สวน` from the erroneous three-syllable `/sa˨˩.wa˦˥.na˦˥/` to `/sua̯n˩˩˦/`. A real-engine test now protects this exact pinned output and verifies that the adapter retains segmental IPA, the rising Chao tone contour and its explicitly provisional status. The PR's maintainer acceptance is source evidence for the upstream correction, not independent expert adjudication or general accuracy evidence. The real-engine regression passed in dedicated workflow [41872842606](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41872842606) on exact PR documentation head `32b8c3ed76a8bc65f7f35b5b632f96c40e7e1492`; the workflow also passed all 16 targeted Python tests, Ruff, the FastThaiG2P-only UI contract, static accessibility contract and IPA→Ukrainian regression.


## TLTK fallback-license evidence refinement — 2026-11-04

- Additional primary/package evidence narrows, but does not close, the TLTK part of the FastThaiG2P data-rights review. The TLTK project description states that the package license changed to New BSD (BSD-3-Clause) from version 1.2.2; it lists TLTK 1.3.8 as released 23 April 2021. PyPI's current project metadata also displays BSD-3-Clause. Sources: [PyPI project description and release history](https://pypi.org/project/tltk/) and [TLTK repository](https://github.com/attapol/tltk).
- PyPI explicitly labels its license metadata as **unverified**; the repository currently exposes both LGPL-3.0 and BSD-3-Clause license files, while its setup metadata says BSD-3-Clause. FastThaiG2P's vendored `_th2ipa.py` header identifies TLTK 1.3.8 and BSD-3-Clause, but the exact source commit/archive and file-by-file mapping for all six vendored fallback data assets have not been established.
- **Revised assessment:** BSD-3-Clause is the best-supported package-level declaration for TLTK 1.3.8 and the vendored parser source, so this is no longer accurately described as an entirely unresolved package-license claim. However, do not infer that every copied model/data file is independently cleared solely from the package metadata. The FastThaiG2P production data-rights gate remains **BLOCKED** because the larger runtime dictionary still mixes Wiktionary/kaikki-derived entries, generated IPA, manual overrides and fallback assets without a complete asset-level rights/attribution manifest. Exact upstream source revisions and data-specific terms are still required.

