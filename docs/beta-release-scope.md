# Beta release scope and operational checklist

**Decision date:** 2026-11-05  
**Owner decision:** publish a clearly labelled research beta; external Thai-phonetics and Ukrainian-native review are not beta acceptance gates.

**Current publication:** live on GitHub Pages. The owner authorized research-project publication on 2026-11-05. This approval does not waive third-party license terms; the TLTK-derived fallback retains both BSD-3-Clause and LGPL-3.0 notices while exact file-level scope remains ambiguous.

## Beta contract

This is a usable, evidence-labelled beta of a research-oriented Thai-to-Ukrainian reading aid. It is not a validated pronunciation standard, a translation service, or a corpus-accuracy benchmark.

- Keep the website's sole G2P path: FastThaiG2P → raw external IPA → typed provisional IPA boundary → Ukrainian adaptation.
- Keep unsupported/incomplete IPA fail-closed. Do not infer missing segments, syllable boundaries, tone categories, or Ukrainian spellings to improve apparent coverage.
- Label the Ukrainian output as a **provisional practical candidate**. Preserve raw IPA and source-engine provenance.
- Do not claim independent linguistic accuracy. Current independent IPA gold remains 0 and accuracy remains NOT_MEASURED.
- No audio acquisition, audio processing, acoustic validation, or narrow connected-speech claims. These remain outside the text-only beta scope.
- CCOST/LOTUSDIS annotations remain source-annotated data, not independent gold. Corpus use remains subject to each source's terms and attribution.
- Build a source-filtered browser wheel from the pinned FastThaiG2P commit and Pyodide in CI; self-host all runtime assets on GitHub Pages. The build retains only per-entry Wiktionary IPA records, excludes generated/manual/unknown records, and preserves the upstream OOV fallback. It embeds attribution/provenance and produces a separately downloadable CC BY-SA dataset archive in the bundle. All six TLTK fallback asset transformations are source/transform verified. The owner-approved Pages bundle and transparent dataset ZIP are published and checked by the live post-deploy smoke; both TLTK notices remain disclosed because exact per-file license scope is not conclusively resolved.

## Owner-approved beta gate changes

| Work item | Beta status | Meaning |
|---|---|---|
| Two independent Thai reviewers plus adjudicator | DEFERRED | Not required to publish a clearly labelled beta; do not claim expert-validated Thai IPA. |
| Independent Ukrainian-native target-form review | DEFERRED | Not required for beta; Ukrainian output remains project-defined and provisional, not normative. |
| Acoustic/narrow phonetic validation | DEFERRED / OUT OF SCOPE | No audio is requested or processed. |
| Manual accessibility certification | DEFERRED as a certification gate | Source-level and automated checks remain required; unresolved manual checks must be disclosed, not described as passed. |
| CCOST unknown labels (_8, <P>, <P:>, <:p>, <Fail>) | PARTIAL / fail-closed | Keep raw values and abstain; beta may proceed without inventing semantics. |
| CCOST controlled-wordlist discrepancy | DEFERRED unless it affects a shipped runtime path | Do not promote unresolved research rows into runtime data. |
| FastThaiG2P browser runtime bundle | DONE_VERIFIED / PUBLISHED | Pages post-deploy smoke `42098396098`, Pyodide parity/Chromium worker `42098395877`, and main CI `42099035122` passed. Owner research-publication approval is recorded in the rights manifest; TLTK BSD/LGPL ambiguity remains disclosed and both notices are shipped. |

DEFERRED is a scope decision, not a pass. Reopen a deferred item before any claim of linguistic validation, official-standard status, corpus accuracy, or acoustic fidelity.

## Accessibility review: static evidence

The following source-level properties were inspected in web/index.html, web/system.html, web/src/app.js, and web/src/styles.css on the current work branch:

- Both pages declare lang="uk", have a viewport meta tag, a skip link to #main-content, a named primary navigation landmark, and a main landmark with a programmatic focus target.
- The Thai input has an explicit associated label, lang="th", and aria-describedby help text.
- The status region uses role="status", aria-live="polite", and aria-atomic="true"; result content is deliberately not announced as a large live region.
- Keyboard focus styling exists for buttons, links, textarea, select, and summary; the stylesheet includes responsive layouts at 760px and 420px.
- Interactive controls and navigation generally use 44px minimum heights; the primary action uses 48px.
- Reduced-motion preference is respected for smooth scrolling.
- A forced-colors media rule now uses system colors for visible focus, component boundaries, status markers, and the primary action.
- Contrast ratios calculated from authored CSS tokens: muted text #5e6070 on white 6.21:1; body text #505360 on white 7.64:1; primary blue #302d8b on white 11.21:1; red #9b263b on white 7.68:1; beta notice text #51474b on #fbf6f6 8.34:1. These sampled pairs exceed WCAG AA normal-text contrast (4.5:1). This is not a complete audit of every rendered state or CSS combination.

### Accessibility items not verified in this connector-only review

- Actual keyboard-only traversal and focus order in a browser.
- Screen-reader output for errors, result changes, copy feedback, and expandable syllable details.
- 200%/400% zoom, text-spacing overrides, narrow viewport/reflow and mobile assistive technology.
- Actual Windows High Contrast / forced-colors visual behavior in supported browsers (a source-level rule is present, but runtime rendering has not been inspected).
- Cross-browser rendering, touch target behavior and actual computed contrast for every dynamic result state.

These are manual verification tasks, not evidence of failure. Use [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) as the normative checklist; in particular, sampled text contrast is compared with SC 1.4.3 (4.5:1 for normal text). Do not claim WCAG conformance or certification until the checks are executed and recorded. The beta can ship with this limitation stated if all automated repository gates pass.

## Product and operations practices adopted from the reference skills repository

Reference: https://github.com/mfwarren/entrepreneur-claude-skills. Its README describes reusable skill packages with a consistent SKILL.md, README, examples and references structure, and categories including product strategy, landing pages, SOPs, automation, decision frameworks and founder productivity. It does **not** list a dedicated accessibility skill. Therefore:
- use its SOP-builder approach for repeatable beta triage and release procedures;
- use product-market-fit / market-research thinking to gather structured user feedback, not to invent demand or success metrics;
- use decision-frameworks to separate reversible beta decisions from claims that require stronger evidence;
- use landing-page/copywriting principles to make the beta notice, limitations and feedback path understandable;
- use WCAG criteria—not an entrepreneurship skill—as the accessibility standard.

No third-party skill files are copied into this repository.

## Beta operating loop

1. **Observe:** collect user-reported input/output pairs, browser/device context only when voluntarily supplied, and the exact visible warning/status. Do not collect sensitive text by default.
2. **Classify:** distinguish software defect, unsupported linguistic case, upstream FastThaiG2P behavior, UI/accessibility issue, and documentation/expectation mismatch.
3. **Prioritize:** fix correctness, data-loss, security/privacy, and blocking usability issues before cosmetic polish. Keep linguistic uncertainty as an abstention, not a bug to be guessed away.
4. **Change:** add a focused regression test and preserve Python/browser/API parity where relevant.
5. **Verify:** run exact-head CI, site API smoke and optional upstream smoke where applicable; inspect generated-artifact drift.
6. **Communicate:** update the known-limitations notice and this ledger. Do not convert user reports into gold labels without a separate provenance and review process.

## Beta release checklist

- [x] Exact-head Full CI passes on the candidate commit (run `42090379627`; latest documentation follow-up is undergoing a fresh exact-head run).
- [x] Dedicated FastThaiG2P Site API workflow passes (run `42090379612`).
- [x] Optional external G2P smoke passes (run `42090379819`).
- [x] Python/browser parity and generated-artifact drift gates pass (Full CI run `42090379627`; Pyodide run `42090379707`).
- [x] Dependency pins, license notices and corpus attribution are present.
- [x] Beta UI clearly states provisional status, privacy caution, and unsupported-input behavior.
- [x] A feedback path and a simple issue-triage procedure are published: website footer links to the GitHub Beta feedback form at .github/ISSUE_TEMPLATE/beta-feedback.yml; it asks for minimal reproduction context and explicitly prohibits personal/confidential data and audio.
- [x] FastThaiG2P Pyodide browser port passes CPython parity and real Chromium cold/warm worker smoke without API/CDN requests; live Pages deployment and post-deploy dataset/license hash smoke passed (`42098396098`, `42098395877`).
- [x] Owner-approved research-project redistribution is recorded in the bundle rights manifest; source filtering, transparent dataset archive, notices and live SHA-256 checks are verified. This approval does not waive third-party terms.
- [ ] Final per-file TLTK BSD/LGPL scope clarification; both notices remain published and disclosed while the exact scope is unresolved.
- [ ] Pyodide cold-start, warm-run and bundle-size budgets are measured on desktop and mobile.
- [x] Manual accessibility limitations are disclosed; no unsupported WCAG conformance claim is made.
- [x] Release notes identify known linguistic and corpus limitations.

## GitHub Pages-only hosting decision and port status (2026-11-05)

The owner selected a browser/WASM port of the existing FastThaiG2P engine. GitHub Pages is the sole hosting target; Vercel, remote API hosting and JavaScript engine replacement are out of scope. The port uses the shared Python service inside self-hosted Pyodide 0.29.5 and a same-origin Web Worker. The browser path does not call the FastAPI reference wrapper or any CDN.

The pinned FastThaiG2P dictionary is filtered by per-entry `ipa_metadata.json` source: 13,144 Wiktionary records are retained; 48,957 model-generated records and any manual/unknown records are excluded. The tokenizer list is reduced to those exact IPA keys. One stale metadata value (`สวน`) is disclosed while preserving the runtime IPA. The OOV fallback remains enabled. The browser wheel embeds source counts and attribution; the bundle builder also emits a transparent ZIP containing `dict.txt`, `ipa.json`, provenance, attribution, and the CC BY-SA 4.0 notice.

**Exact runtime evidence:** [Pyodide compatibility and Chromium worker — 42085653176](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42085653176) passed four CPython/Pyodide parity cases, cold/warm Chromium worker smoke, no API/CDN requests, source filtering, and all six TLTK fallback asset transformations. Five fallback assets are byte-identical to the pinned TLTK source; the sixth is byte-identical after bzip2 decompression. Ten third-party notices are staged and hashed. The transparent-dataset archive and its ZIP-member assertions passed on the exact branch head in [Pyodide workflow 42086644531](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42086644531). The deploy-time HTTP hash assertion is syntax-validated but cannot run until an authorized Pages deployment; Full CI and other PR checks remain queued. See [FastThaiG2P data provenance](fastthaig2p-data-provenance.md) and [Pyodide port status](fastthaig2p-pyodide-port.md).

**Public deployment is verified.** The owner-approved bundle manifest has `redistribution_approved=true`; the Pages post-deploy smoke verifies the site, worker assets, runtime manifest, four pinned wheels, transparent dataset ZIP, all ten license notices and their hashes. The TLTK file-level scope remains ambiguous; both BSD-3-Clause and LGPL-3.0 notices are preserved. Do not interpret the owner approval as a legal waiver or a claim that the ambiguity is resolved.

**Readiness:** `BETA_PUBLICATION_VERIFIED; LINGUISTIC_VALIDATION_NOT_DONE`. This is software-runtime evidence, not linguistic validation. Independent IPA gold remains 0, accuracy remains `NOT_MEASURED`, and Ukrainian forms remain provisional. Actual performance budgets and manual assistive-technology checks remain open. Production cutover remains false; the published product is a research beta.
