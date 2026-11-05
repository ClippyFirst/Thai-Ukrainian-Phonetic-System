# Beta release scope and operational checklist

**Decision date:** 2026-11-05  
**Owner decision:** prepare a beta release; external Thai-phonetics and Ukrainian-native review are not beta acceptance gates.

## Beta contract

This is a usable, evidence-labelled beta of a research-oriented Thai-to-Ukrainian reading aid. It is not a validated pronunciation standard, a translation service, or a corpus-accuracy benchmark.

- Keep the website's sole G2P path: FastThaiG2P → raw external IPA → typed provisional IPA boundary → Ukrainian adaptation.
- Keep unsupported/incomplete IPA fail-closed. Do not infer missing segments, syllable boundaries, tone categories, or Ukrainian spellings to improve apparent coverage.
- Label the Ukrainian output as a **provisional practical candidate**. Preserve raw IPA and source-engine provenance.
- Do not claim independent linguistic accuracy. Current independent IPA gold remains 0 and accuracy remains NOT_MEASURED.
- No audio acquisition, audio processing, acoustic validation, or narrow connected-speech claims. These remain outside the text-only beta scope.
- CCOST/LOTUSDIS annotations remain source-annotated data, not independent gold. Corpus use remains subject to each source's terms and attribution.
- Do not bulk-vendor mixed FastThaiG2P dictionary/fallback data unless exact component-level provenance and notices are preserved. The pinned optional dependency path is separate from redistribution.

## Owner-approved beta gate changes

| Work item | Beta status | Meaning |
|---|---|---|
| Two independent Thai reviewers plus adjudicator | DEFERRED | Not required to publish a clearly labelled beta; do not claim expert-validated Thai IPA. |
| Independent Ukrainian-native target-form review | DEFERRED | Not required for beta; Ukrainian output remains project-defined and provisional, not normative. |
| Acoustic/narrow phonetic validation | DEFERRED / OUT OF SCOPE | No audio is requested or processed. |
| Manual accessibility certification | DEFERRED as a certification gate | Source-level and automated checks remain required; unresolved manual checks must be disclosed, not described as passed. |
| CCOST unknown labels (_8, <P>, <P:>, <:p>, <Fail>) | PARTIAL / fail-closed | Keep raw values and abstain; beta may proceed without inventing semantics. |
| CCOST controlled-wordlist discrepancy | DEFERRED unless it affects a shipped runtime path | Do not promote unresolved research rows into runtime data. |
| FastThaiG2P component-level vendoring | DEFERRED | Continue using the pinned optional dependency; do not copy unreviewed mixed assets into the distribution. |

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

These are manual verification tasks, not evidence of failure. Do not claim WCAG conformance or certification until the checks are executed and recorded. The beta can ship with this limitation stated if all automated repository gates pass.

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

- [ ] Exact-head Full CI passes on the candidate commit.
- [ ] Dedicated FastThaiG2P Site API workflow passes.
- [ ] Optional external G2P smoke passes, or its unavailability is explicitly recorded.
- [ ] Python/browser parity and generated-artifact drift gates pass.
- [ ] Dependency pins, license notices and corpus attribution are present.
- [ ] Beta UI clearly states provisional status, privacy caution, and unsupported-input behavior.
- [x] A feedback path and a simple issue-triage procedure are published: website footer links to the GitHub Beta feedback form at .github/ISSUE_TEMPLATE/beta-feedback.yml; it asks for minimal reproduction context and explicitly prohibits personal/confidential data and audio.
- [ ] Python-capable hosting preview and same-origin API behavior are verified before public site cutover.
- [ ] Manual accessibility limitations are disclosed; no unsupported WCAG conformance claim is made.
- [ ] Release notes identify known linguistic and corpus limitations.

## Current readiness statement

**BETA_CANDIDATE_ENGINEERING_VERIFIED; PUBLIC_DEPLOYMENT_NOT_YET_VERIFIED.** Existing exact-head CI on 5a7f6888420009e288f6b43332bd0dd4b560fddd passed (Full CI, Site API, optional external G2P smoke). This is an engineering verification result, not linguistic validation and not proof that a Python-capable public hosting preview is ready. No release tag or production cutover is made by this document.
