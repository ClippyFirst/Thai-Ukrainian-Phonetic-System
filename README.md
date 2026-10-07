# Thai → Ukrainian Phonetic-Graphemic Correspondence System

Research-oriented, machine-readable reference implementation for mapping contemporary Standard Thai orthography through graphemic structure, phonology and IPA into a Ukrainian phonetic/phonological target.

## Research pipeline

**Primary:** Thai orthography → structural orthographic analysis → syllable structure → Thai phonology → Ukrainian adaptation.

**Independent audit:** Thai phonology → phonemic IPA → conservative surface IPA.

IPA is not required as the intermediate string for Ukrainian output. Context-dependent graphemes are resolved by the machine-readable orthographic-rule registry before phonological and Ukrainian layers are applied.

The layers are intentionally separated. This is **not RTGS** and not a Thai-character → Ukrainian-character substitution table.

## Scope

Primary scope: contemporary Standard Thai with a Bangkok/central-standard reference where the evidence permits.

The model distinguishes:

- grapheme vs phoneme;
- consonant class vs phonetic realization;
- vowel sign vs vowel nucleus;
- tone mark vs phonological tone;
- orthographic order vs phonological order;
- structural combinations vs valid orthography vs phonotactic possibility vs attestation;
- phonemic/broad IPA vs narrower surface phonetics;
- Ukrainian candidate ranking vs a calibrated probability or a unique orthographic answer.

## Implemented

- 44 Thai consonant graphemes with class and positional data.
- Vowel-sign parsing including interleaved Thai spelling and a machine-declared glide/rime registry.
- Conservative complex-onset licensing: arbitrary consonant adjacency is not promoted to a Thai cluster without structural evidence.
- Live/dead syllable classification and explicit tone-bearing consonant-class selection for clusters.
- Five-tone engine with explicit invalid combinations.
- ห นำ handling as an explicit orthographic/phonological transformation.
- Broad phonological and conservative surface-phonetic layers with explicit syllable-internal positional IPA.
- Feature-distance Ukrainian candidate generation using the canonical Ukrainian target snapshot.
- Evidence/provenance registry.
- Machine-readable tone-rule registry consumed by the tone engine.
- Explicit special-orthography analysis layer for lexical/context-dependent constructions.
- Machine-readable context-dependent orthographic rule registry, including role classification for อ.
- Publication-ready orthographic correspondence table generated from the same rule registry used by the parser.
- External lexicon adapter for evidence-backed syllable segmentation.
- Project-defined Ukrainian orthographic candidate layer with tone kept separate.
- Generated source→parser→derived consistency manifest enforced by CI.
- Structural combinatorial-space accounting.
- Machine-readable analysis and corpus-record schemas.
- Deterministic JSONL evaluation API and CLI.
- Explicit word model with standalone / initial / medial / final syllable positions.
- Positional regression tests and a documented segmentation boundary.
- Separate generated Thai-consonant and Thai-vowel correspondence tables exposing phonemic IPA, conservative surface IPA, position/context, and Ukrainian candidates derived from IPA.
- Adversarial rejection of non-conforming consonant sequences such as แสดง when supplied as one syllable.
- Adversarial rejection of multiple tone marks, unconsumed vowel signs and unsupported symbols instead of silently dropping them.
- Regression, negative-input and generated-artifact tests.
- GitHub Actions CI that regenerates derived artifacts and verifies a clean tree.
- Citation metadata, license and research release protocol.

## Current release status

**v0.5.0 — research-ready IPA-audit layer with conservative positional surface phonetics.**

The repository is suitable as a transparent research foundation and reference implementation. The completion branch adds machine-readable tone rules, special-orthography analysis, external lexical segmentation support, a Ukrainian orthographic candidate layer, and source→parser→derived consistency checks. The current development branch is CI-verified; the pull request remains the review boundary until the branch is merged.

It is **not** yet an empirically validated benchmark. No corpus accuracy percentage is claimed because a declared gold corpus has not been processed by CI.

### Evidence-gated limitations

- arbitrary Thai text still requires an external lexical segmentation source; the software does not invent word boundaries;
- special orthography is represented conservatively as explicit analysis-dependent alternatives where lexical evidence is required;
- connected-speech narrow phonetics still requires acoustic/phonetic evidence;
- corpus-calibrated probabilities still require a gold dataset;
- Ukrainian orthographic candidates are project-specific and not an official normative standard.

These are evidence gates, not hidden software gaps.

## Quantitative accounting

The generated syllable-space report gives a **structural upper bound**, not the number of Thai syllables:

- initial grapheme options: 44;
- declared vowel/rime records: 40;
- structural coda grapheme options used by the generator: 38;
- tone-mark states: 5;
- combined structural upper bound: 351,780.

This must not be interpreted as a count of valid, lexical or corpus-attested Thai syllables.

## Word and positional model

The reference implementation can analyze an explicitly segmented word with `analyze_word_syllables(["กา", "นา", "มา"])`. It preserves syllable index and position without pretending that Thai orthography alone provides universal word segmentation. See `docs/word-and-position-model.md`.

## Evidence and validation

Core evidence includes Royal Institute of Thailand materials, Tingsabadh & Abramson (1993), corpus-based Thai phoneme-distribution work, CCOST and Thai G2P resources. Third-party corpora are not redistributed.

See:

- Research protocol: docs/research-protocol.md
- Corpus validation: docs/corpus-validation.md
- Evidence registry: docs/evidence.md
- Final audit: docs/final-audit.md

## User interface

The research core is also available as an installable `thai-ua` CLI with single-input analysis, TXT/CSV/TSV/XLSX batch processing and a local JSON API. Excel support is optional: `pip install -e ".[excel]"`.

Examples:

```powershell
thai-ua analyze "กา"
thai-ua batch words.csv -c thai -o results.xlsx
thai-ua serve
```

See `docs/cli-batch-api.md` for the complete CLI and API reference.

## Reproducibility

From a clean Python environment:

~~~bash
pip install -e .
python scripts/generate_derived.py
python scripts/generate_syllable_space.py
python -m unittest discover -s tests -v
~~~

For an external gold JSONL corpus:

~~~bash
python scripts/evaluate_corpus.py path/to/records.jsonl
~~~

The evaluator reports numerators and denominators explicitly and excludes missing gold fields from the relevant metric.


## Web service

The repository includes a static two-page web application under `web/`:

- `web/index.html` — public Service interface for Thai analysis;
- `web/system.html` — methodology and evidence page;
- `web/src/engine.js` — browser-safe implementation of the declared analysis pipeline;
- `web/tests/fixtures.json` — versioned parity probes;
- `scripts/generate_web_fixtures.py` — generates the authoritative fixture values from the Python core.

The web CI gate compares the browser engine against the Python reference on the same probes before the Pages artifact is eligible for deployment. GitHub Pages is a static presentation/deployment layer; it does not run the Python package server-side.

## Research workspace

- Notion: https://app.notion.com/p/3ec40df389698138be8beb43b78971a2?pvs=204
- Lucid: https://lucid.app/lucidchart/bd12788f-bec1-4f10-a01d-0def1efea509/view

## Citation

Use the repository's CITATION.cff. The software is released under the MIT License.

## Final principle

A result is only called **empirical** when it has a named/versioned evidence source and an explicit evaluation denominator. Structural generation, heuristic candidate ranking and documented linguistic rules are valuable research components, but they are not substitutes for corpus validation.


## Master correspondence table

The repository can deterministically generate an exhaustive structural Thai → Ukrainian master table using the IPA-first pipeline. It contains 351,780 structural rows from 44 initial graphemes, 41 vowel/rime records, 38 coda options plus open syllables, and 5 tone-mark states. The downloadable generated artifacts are attached to the **master-artifact** CI job; see `docs/master-correspondence-table.md` for semantics and limitations.
