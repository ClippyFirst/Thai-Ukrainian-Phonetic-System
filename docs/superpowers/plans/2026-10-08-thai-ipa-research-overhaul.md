# Thai → IPA Research Overhaul Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current Thai→IPA implementation with a single evidence-traceable, non-fabricating IPA layer covering Standard Thai segmental structure, tone categories, contextual phonetics, and high-risk orthographic cases, while leaving Ukrainian rendering unchanged.

**Architecture:** CSV registries remain the machine-readable source of truth for consonant/vowel/tone facts. Python resolves orthography into a structured analysis, then composes conservative phonemic IPA and a separately documented conservative surface IPA; browser code consumes generated/parity data rather than maintaining independent IPA tables. Unresolved, invalid, and evidence-dependent cases never receive placeholder or invented IPA.

**Tech Stack:** Python 3.x, pytest, CSV registries, existing browser JavaScript/CSS, GitHub Actions, generated CSV/JSON artifacts.

**Spec:** `docs/superpowers/specs/2026-10-08-thai-ipa-overhaul-design.md`

## Global Constraints

- Scope is Thai → IPA; Ukrainian adaptation/ranking is not redesigned.
- Adopt Standard Thai/Bangkok-oriented evidence; no dialect-specific claims.
- Phonemic/broad IPA and conservative surface IPA are separate outputs.
- Tone category and phonetic contour are separate semantic concepts.
- No `?`, empty-string, or guessed symbol may represent missing IPA.
- No duplicated production IPA inventory may exist outside authoritative registries/rules.
- Invalid/unresolved analyses return null IPA fields.
- Analysis-dependent output requires an explicit evidence-backed interpretation; otherwise IPA is withheld.
- Every changed rule must have regression coverage.
- Python and browser semantic parity is a release gate.
- Generated artifacts must be reproducible.

## Review Focus

- Carrier `อ`: do not automatically turn the orthographic carrier into a phonemic /ʔ/ segment in every vowel-initial syllable.
- Final obstruents: preserve phonemic coda neutralization while allowing only explicitly supported conservative surface unreleased notation.
- Diphthongs and vowel+glide sequences: do not collapse phonemic diphthongs into a general triphthong inventory or conflate them with final glides.
- Tone contours: never present one speaker/context-dependent F0 contour as a universally exact narrow transcription.
- Lexically/contextually underdetermined spellings: return an explicit analysis-dependent/unresolved state instead of fabricating a pronunciation.

### Task 1: Establish the evidence-backed IPA registry contract

**Files:**
- Modify: `data/thai/consonants.csv`
- Modify: `data/thai/vowels.csv`
- Modify: `data/thai/tone_rules.csv`
- Create: `data/thai/ipa_sources.csv`
- Create: `tests/test_ipa_registry.py`

**Interfaces:**
- Consumes: existing CSV registries and the adopted Standard Thai evidence base.
- Produces: validated machine-readable segmental/tone IPA records with stable IDs and source/evidence metadata.

- [ ] **Step 1: Write failing registry tests** for: 44 consonant grapheme records; onset/coda fields; carrier semantics; nine monophthong qualities with length contrast; adopted diphthong inventory; no generic triphthong inventory; tone rule coverage; every IPA value non-empty and Unicode-valid; every record has a source/evidence status.
- [ ] **Step 2: Run the focused registry tests and verify they fail** against the current duplicated/under-specified data.
- [ ] **Step 3: Implement the registry contract** by adding source IDs, explicit IPA role/level metadata where needed, correcting only evidence-backed vowel/tone/consonant values, and documenting analysis-dependent records rather than forcing them into deterministic IPA.
- [ ] **Step 4: Run the focused registry tests and verify they pass.**
- [ ] **Step 5: Commit** as `feat(thai): formalize evidence-backed IPA registries`.

### Task 2: Remove duplicated IPA logic and make Python IPA status-safe

**Files:**
- Modify: `src/thai_ukrainian/inventory.py`
- Modify: `src/thai_ukrainian/phonology.py`
- Modify: `src/thai_ukrainian/models.py`
- Modify: `src/thai_ukrainian/tone.py`
- Create/modify: `tests/test_phonology_ipa.py`
- Create/modify: `tests/test_status_ipa_contract.py`

**Interfaces:**
- Consumes: Task 1 registries.
- Produces: `SyllableAnalysis.phonemic_ipa: str | None`, `SyllableAnalysis.phonetic_ipa: str | None`, and word-level IPA properties that return `None` when any required syllable IPA is unavailable.

- [ ] **Step 1: Write failing tests** proving no production `ONSET_IPA` duplicate exists, unknown consonants cannot become `?`, `อ` carrier is not blindly emitted as /ʔ/, and invalid/unresolved/analysis-dependent syllables have null IPA.
- [ ] **Step 2: Run focused tests and verify failure.**
- [ ] **Step 3: Refactor** `phonology.py` to consume `Consonant.onset_ipa/coda_ipa` from the registry; make carrier/zero-onset handling explicit; preserve ห นำ tone-class behavior without emitting silent ห; replace word-level `?` fallbacks with nullable output; centralize status gating.
- [ ] **Step 4: Tighten tone resolution** so the returned tone category is registry-backed and its contour representation is labeled as a phonetic/broad convention rather than an exact acoustic measurement.
- [ ] **Step 5: Run focused tests and verify pass.**
- [ ] **Step 6: Commit** as `refactor(thai): make IPA generation registry-driven and non-fabricating`.

### Task 3: Implement the complete conservative surface-IPA layer

**Files:**
- Modify: `src/thai_ukrainian/contextual.py`
- Modify: `src/thai_ukrainian/phonology.py`
- Modify: `tests/test_phonology_ipa.py`
- Create/modify: `tests/test_surface_ipa.py`

**Interfaces:**
- Consumes: validated segmental registry and Task 2 semantic model.
- Produces: conservative surface IPA only for documented deterministic positional effects.

- [ ] **Step 1: Write failing tests** for final `p/t/k` conservative unreleased notation, final nasal/glide behavior, vowel context handling, and preservation of onset aspiration/contrast.
- [ ] **Step 2: Run and verify failure.**
- [ ] **Step 3: Implement only evidence-backed surface rules**; do not add speaker-specific /r/, tone peak timing, optional glottalization, or other variable realizations as deterministic output.
- [ ] **Step 4: Verify broad and surface outputs remain distinct and source-traceable.**
- [ ] **Step 5: Run focused tests and verify pass.**
- [ ] **Step 6: Commit** as `feat(thai): add conservative surface IPA rules`.

### Task 4: Harden orthography → IPA edge cases

**Files:**
- Modify: `src/thai_ukrainian/orthography.py`
- Modify: `src/thai_ukrainian/api.py`
- Modify: `web/src/engine.js`
- Modify: `web/src/data.js`
- Modify: `web/src/vowels.js`
- Create/modify: `tests/test_ipa_edge_cases.py`
- Create/modify: `web/tests/fixtures.python.json` or its generator
- Modify: `web/tests/*.test.js` as applicable

**Interfaces:**
- Consumes: Tasks 1–3.
- Produces: deterministic parity behavior for ordinary syllables and explicit non-deterministic statuses for ambiguous/special orthography.

- [ ] **Step 1: Write failing tests** for `กา กาน กาล กรา กล้า คน เกะ เก เกา ไกล ใกล้ ไก่ หงา ไหม ไหว้ อย่า`, special `รร ทร จร สร ศร ซร ฤ ฤๅ ฦ ฦๅ ์`, carrier `อ`, invalid `ค๊า`, punctuation/unsupported input, obsolete consonants, coda licensing, and false clusters such as `จริง`.
- [ ] **Step 2: Run and verify failures for every currently incorrect semantic case.**
- [ ] **Step 3: Implement the minimal rule/data changes**: preposed vowels are structural, not linear; ห นำ affects tone class without a spoken ห; carrier semantics are explicit; special orthography remains analysis-dependent unless a deterministic lexical rule is evidenced; invalid tone/coda combinations emit no IPA.
- [ ] **Step 4: Regenerate normalized parity fixtures and assert Python/browser equality for status, segmentation, tone, IPA, and evidence metadata.**
- [ ] **Step 5: Run Python and browser focused suites and verify pass.**
- [ ] **Step 6: Commit** as `fix(thai): harden orthographic-to-IPA edge cases`.

### Task 5: Rebuild generated master artifacts from the IPA-first pipeline

**Files:**
- Modify: `scripts/generate_master_table.py`
- Modify: `tests/test_master_table.py`
- Modify: `data/derived/thai_ukrainian_master.csv`
- Modify: `data/derived/thai_ukrainian_master_2col.csv`
- Modify: `data/derived/thai_consonant_correspondence.csv`
- Modify: `data/derived/thai_vowel_correspondence.csv`
- Modify: `data/derived/thai_orthographic_correspondence.csv`

**Interfaces:**
- Consumes: Tasks 1–4.
- Produces: reproducible artifacts where actual parser IPA is distinguished from constructed structural expectations.

- [ ] **Step 1: Add failing assertions** that generated analyzed rows contain actual IPA, non-analyzed rows contain null/empty actual IPA, no generated actual IPA contains `?`, and `ukrainian_from_ipa` is derived only from actual phonemic IPA.
- [ ] **Step 2: Run and verify failure if current artifact semantics violate the new contract.**
- [ ] **Step 3: Update generation and expected cardinality/status accounting without changing the structural Cartesian product solely to hide parser disagreements.**
- [ ] **Step 4: Regenerate all derived artifacts.**
- [ ] **Step 5: Run artifact/master-table tests and verify pass.**
- [ ] **Step 6: Commit** as `chore(thai): regenerate IPA-first master artifacts`.

### Task 6: Documentation and scientific provenance

**Files:**
- Modify: `README.md`
- Modify: `docs/thai-vowels.md`
- Modify: `docs/master-correspondence-table.md`
- Modify: `docs/repository-audit-2026-10-05.md`
- Modify/create: `docs/thai-ipa-methodology.md`
- Modify: `docs/evidence-sources.md`
- Modify: `CITATION.cff` only if bibliographic additions require it

**Interfaces:**
- Consumes: final implementation and evidence registry.
- Produces: a reproducible scientific account of what the engine does and does not claim.

- [ ] **Step 1: Write documentation acceptance checks** for: adopted Standard Thai inventory; broad vs surface IPA; five tone categories vs realization; vowel/diphthong policy; coda neutralization; carrier semantics; status semantics; analysis-dependent cases; primary/secondary source provenance.
- [ ] **Step 2: Implement the methodology document and synchronize existing docs.**
- [ ] **Step 3: Add the primary JIPA Thai source plus relevant acoustic/phonological/G2P literature, including explicit limitations where full-text evidence was unavailable.
- [ ] **Step 4: Run documentation/static consistency checks and verify pass.**
- [ ] **Step 5: Commit** as `docs(thai): document IPA methodology and evidence boundaries`.

### Task 7: Full verification, browser parity, review, and release gate

**Files:**
- Modify: CI/test configuration only if required by actual failures.
- Modify: `docs/superpowers/...` ledger/review artifacts.

**Interfaces:**
- Consumes: all previous tasks.
- Produces: green Python tests, browser static/parity tests, generated-artifact verification, and a final reviewable PR.

- [ ] **Step 1: Run the complete Python suite.**
- [ ] **Step 2: Run the complete browser/static/parity suite.**
- [ ] **Step 3: Regenerate artifacts and confirm a clean reproducibility diff.**
- [ ] **Step 4: Run GitHub Actions and wait for all required checks to finish; investigate any failure rather than weakening tests.
- [ ] **Step 5: Perform the Superpowers final whole-branch review against the spec and this plan; Critical/Important findings require RED→GREEN fixes and a fresh full-suite run.
- [ ] **Step 6: Update Notion with final evidence, implementation status, limitations, test status, and PR link.
- [ ] **Step 7: Commit final verification/documentation changes** as `chore(thai): verify research-grade IPA overhaul`.

## Acceptance Criteria

1. Every emitted IPA symbol is traceable to a registry or explicitly documented phonological/surface rule.
2. No duplicated consonant/vowel IPA inventory remains in production code.
3. No output API uses `?` as missing IPA.
4. Invalid, unresolved, and unsupported analyses cannot emit fabricated IPA.
5. Analysis-dependent cases are explicitly labeled and do not silently become deterministic.
6. Carrier `อ`, ห นำ, final neutralization, clusters, preposed vowels, special orthography, and invalid tone combinations are tested.
7. Phonemic/broad IPA and conservative surface IPA are distinct.
8. Tone category is not presented as a universal speaker-independent narrow F0 contour.
9. Python and browser results are semantically equivalent for the parity fixture set.
10. Generated master artifacts remain reproducible and retain structural-vs-attested distinctions.
11. Documentation and Notion match the implementation and evidence limits.
12. Required CI checks are green before merge; GitHub Pages activation is not claimed unless independently verified.
