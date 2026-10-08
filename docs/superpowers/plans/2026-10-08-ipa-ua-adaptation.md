# IPA → Ukrainian adaptation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a deterministic, auditable IPA → Ukrainian practical-adaptation layer whose canonical invariant is `kʰaː → ка`.

**Architecture:** Parse IPA into structured segments/features, generate candidates from a machine-readable Ukrainian adaptation registry, then rank candidates using deterministic contextual rules. The layer is independent of Thai orthography and keeps source IPA unchanged while explicitly recording neutralized features.

**Tech Stack:** Python 3.14; existing repository test framework; JSON/CSV registries; browser JavaScript parity fixtures; GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-08-ipa-ua-adaptation-design.md`

## Global Constraints

- IPA → UA must not inspect Thai graphemes or Thai-specific orthographic rules.
- `kʰaː → ка` is a mandatory regression invariant.
- Aspiration and vowel length are preserved upstream and may be neutralized only in the Ukrainian adaptation layer.
- No unresolved/invalid source may produce fabricated Ukrainian output.
- Tone remains separate from segmental Ukrainian rendering.
- Candidate ranking is deterministic and is not presented as calibrated probability.
- Ukrainian target inventory must use the shared inventory architecture or a pinned generated snapshot.
- Python and browser semantics must agree.
- Generated artifacts must be reproducible and CI-verified.

## Review Focus

1. **Aspirated + long vowel:** `kʰaː` must become `ка`, while audit metadata records aspiration and length as neutralized.
2. **Unknown IPA:** malformed or unknown IPA must return a withheld/invalid result rather than a guessed Ukrainian letter.
3. **Context-sensitive IPA:** the same segment may require different candidates in onset/coda or adjacent-glide contexts.
4. **IPA normalization:** combining marks and modifier sequences must parse identically to canonical precomposed/normalized forms.
5. **Orthography leakage:** two Thai spellings producing the same IPA must produce the same Ukrainian result when metadata is equivalent.

### Task 1: Establish the IPA → UA data contract

**Files:**
- Create: `data/ukrainian/ipa_adaptation.json`
- Create: `src/thai_ukrainian/ipa_ua.py`
- Test: `tests/test_ipa_ua.py`

**Interfaces:**
- Produces `parse_ipa(text: str) -> ParsedIPA`.
- Produces `adapt_ipa(parsed: ParsedIPA, context: AdaptationContext | None = None) -> AdaptationResult`.
- `AdaptationResult) exposes `status`, `source_ipa`, `candidates`, `selected`, `preserved_features`, `neutralized_features`, and `rules_applied`.

- [ ] **Step 1: Write failing tests** for `kʰaː`, `ka`, `kʰa`, malformed IPA, and an unknown IPA symbol.
- [ ] **Step 2: Run the focused tests** and verify they fail because the new parser/adapter contract does not exist.
- [ ] **Step 3: Implement the minimal structured parser and result dataclasses.** Normalize IPA modifiers; represent `kʰ` and `aː` as base segment + features rather than substring replacements.
- [ ] **Step 4: Add the minimal registry entries** needed for the canonical stop/vowel tests: `k`, aspirated `kʰ`, `a`, long `aː`.
- [ ] **Step 5: Implement deterministic adaptation** so `kʰaː`, `kʰa`, and `kaː` all yield `ка`, with explicit neutralization metadata.
- [ ] **Step 6: Run focused tests** and verify PASS.
- [ ] **Step 7: Commit** with `feat: add IPA to Ukrainian adaptation core`.

### Task 2: Expand the adaptation registry and feature model

**Files:**
- Modify: `data/ukrainian/ipa_adaptation.json`
- Modify: `src/thai_ukrainian/ipa_ua.py`
- Test: `tests/test_ipa_ua_inventory.py`

**Interfaces:**
- Registry records declare source pattern, Ukrainian candidate, preserved/neutralized features, context constraints, evidence status, priority, and rule ID.
- Feature parser exposes consonant place/manner/voicing/aspiration and vowel height/backness/rounding/length.

- [ ] **Step 1: Add failing inventory tests** for p/pʰ, t/tʰ, affricates, fricatives, nasals including `ŋ`, liquids, glides, core vowels, long/short pairs, and diphthong/glide structures.
- [ ] **Step 2: Run inventory tests** and confirm unsupported patterns fail rather than silently fall back.
- [ ] **Step 3: Expand the registry** with evidence/status fields and only candidates licensed by the Ukrainian adaptation policy.
- [ ] **Step 4: Implement feature extraction** independent of Thai identity.
- [ ] **Step 5: Add explicit aspiration-neutralization rules** for `pʰ → п`, `tʰ → т`, `kʰ → к`; keep `tɕʰ` separate.
- [ ] **Step 6: Add explicit vowel-length neutralization** without collapsing the source IPA representation.
- [ ] **Step 7: Run inventory tests and full Python tests**; commit `feat: expand IPA adaptation registry`.

### Task 3: Candidate generation and deterministic ranking

**Files:**
- Modify: `src/thai_ukrainian/ipa_ua.py`
- Test: `tests/test_ipa_ua_ranking.py`

**Interfaces:**
- `generate_candidates(parsed: ParsedIPA, context: AdaptationContext) -> list[Candidate]`.
- `rank_candidates(candidates: list[Candidate], context: AdaptationContext) -> list[Candidate]`.

- [ ] **Step 1: Write failing ranking tests** proving context-sensitive candidates are ordered deterministically and unsupported visual lookalikes are excluded.
- [ ] **Step 2: Implement finite candidate generation** from registry entries only.
- [ ] **Step 3: Implement deterministic ranking** using Ukrainian plausibility, salient-feature preservation, phonotactic legality, context, evidence strength, and minimum unnecessary material in the declared order.
- [ ] **Step 4: Expose ranking/audit metadata** without presenting the score as empirical probability.
- [ ] **Step 5: Add negative tests** for malformed IPA, contradictory metadata, and unknown symbols.
- [ ] **Step 6: Run focused + full tests**; commit `feat: add deterministic IPA candidate ranking`.

### Task 4: Integrate with the existing word/syllable analysis model

**Files:**
- Modify: `src/thai_ukrainian/models.py`
- Modify: `src/thai_ukrainian/ipa_ua.py`
- Modify: existing analysis integration module(s) identified by tests/search
- Test: `tests/test_ipa_ua_integration.py`

- [ ] **Step 1: Write failing integration tests** for Thai analyses whose IPA is `kʰaː` and for invalid/unresolved analyses.
- [ ] **Step 2: Integrate IPA → UA only after valid IPA exists.**
- [ ] **Step 3: Populate existing candidate/output fields from the new adapter rather than a second mapping implementation.**
- [ ] **Step 4: Remove or quarantine legacy direct IPA/Thai → UA substitution logic that conflicts with the new adapter.**
- [ ] **Step 5: Ensure null source IPA cannot become `?` and cannot generate Ukrainian output.**
- [ ] **Step 6: Verify end-to-end `kʰaː → ка` and invalid-status behavior; commit `refactor: integrate IPA-first Ukrainian adaptation`.

### Task 5: Context, tone separation, and adversarial regressions

**Files:**
- Modify: `src/thai_ukrainian/ipa_ua.py`
- Test: `tests/test_ipa_ua_adversarial.py`
- Test: relevant existing Thai → IPA regression suite

- [ ] **Step 1: Add failing tests** for onset/coda, syllable boundaries, adjacent glides, tone metadata, and two Thai spellings yielding equivalent IPA.
- [ ] **Step 2: Implement context constraints solely from IPA/structured metadata.**
- [ ] **Step 3: Assert tone never changes segmental candidate selection unless a declared adaptation rule explicitly requires a phonetic-context interaction.**
- [ ] **Step 4: Add regression tests ensuring Thai spelling identity is unavailable to the adapter.
- [ ] **Step 5: Run adversarial suite and full suite; commit `test: harden IPA Ukrainian adaptation boundaries`.

### Task 6: Browser parity and generated fixtures

**Files:**
- Modify/create: `web/src/engine.js` adaptation layer
- Modify/create: `web/tests/fixtures.json`
- Modify/create: `scripts/generate_web_fixtures.py`
- Test: browser parity workflow/tests

- [ ] **Step 1: Add failing parity fixtures** for `kʰaː`, aspiration/length neutralization, unknown IPA, and candidate audit metadata.
- [ ] **Step 2: Port the same registry semantics into browser-safe generated data/code; do not create a second hand-maintained inventory.
- [ ] **Step 3: Generate fixtures from Python reference implementation.
- [ ] **Step 4: Run browser parity checks and verify semantic equality.
- [ ] **Step 5: Commit `test: enforce Python browser IPA adaptation parity`.

### Task 7: Shared Ukrainian inventory integration and documentation

**Files:**
- Modify: adapter data/loader as needed
- Create/modify: `docs/ipa-to-ukrainian.md`
- Modify: `README.md`
- Test: `tests/test_ipa_ua_provenance.py`

- [ ] **Step 1: Add failing provenance tests** requiring every non-trivial mapping to have rule ID/evidence status and the Ukrainian inventory source to be declared.
- [ ] **Step 2: Connect the adapter to the shared Ukrainian inventory or a pinned generated snapshot without duplicating the canonical inventory manually.
- [ ] **Step 3: Document the three-layer distinction: Thai pronunciation, IPA, Ukrainian practical rendering.
- [ ] **Step 4: Document `kʰaː → ка` as the canonical worked example.
- [ ] **Step 5: Document limitations and non-normative status.
- [ ] **Step 6: Run provenance tests and documentation consistency checks; commit `docs: document IPA Ukrainian adaptation provenance`.

### Task 8: Full verification and release gate

**Files:**
- Modify: CI/config only if required
- Modify: generated artifacts only through their generators
- Test: complete repository suite

- [ ] **Step 1: Regenerate all derived artifacts from source registries.
- [ ] **Step 2: Run the complete Python test suite.
- [ ] **Step 3: Run browser parity tests.
- [ ] **Step 4: Run generated-tree cleanliness checks.
- [ ] **Step 5: Verify no legacy direct IPA → UA implementation remains active.
- [ ] **Step 6: Verify the upstream Thai → IPA output for canonical examples is unchanged.
- [ ] **Step 7: Record final test/CI results and commit `chore: verify IPA Ukrainian adaptation release gate`.

## Self-review

- Spec coverage: all 20 specification sections map to Tasks 1–8; no requirement is intentionally left without an owner.
- Step scan: each task has a test-first boundary and a separately verifiable outcome.
- Type consistency: parser, result, candidate, and context interfaces are defined before consumers.
- Review focus: all five high-risk failure modes are pinned to Tasks 1, 2, 3, 5, and 6.
- Proportion: the plan fixes interfaces and tests but leaves implementation bodies to the executor.
