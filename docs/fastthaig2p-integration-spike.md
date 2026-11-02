# FastThaiG2P integration spike

Status: **OPTIONAL_ADAPTER_IMPLEMENTED; SAME-CORPUS_RUNTIME_DIAGNOSTIC_PENDING_CI; ACCURACY_NOT_MEASURED**

Date: 2026-11-02

## Scope and non-goals

This spike adds FastThaiG2P as an optional Python adapter and extends the existing external G2P runner to include the in-repository ClippyFirst engine on the same frozen 42-item challenge corpus. It does not add FastThaiG2P to the default runtime, browser bundle, or production request path. It does not make FastThaiG2P's IPA an authority or bypass the typed `PhoneticResult → Ukrainian adapter` boundary.

The adapter returns the upstream string unchanged. It does not strip tone, length, tie bars, syllable dots, word boundaries, or slashes. A separate ClippyFirst candidate uses the conservative text endpoint and records unsupported/unresolved inputs as abstentions rather than guessing.

## Reproducibility

- Upstream: [awslabs/FastThaiG2P](https://github.com/awslabs/FastThaiG2P)
- Pinned source commit: `c4759eef7df03e11fcbb9aa83efe8cf21709fd2f`
- Upstream package version at that commit: `0.1.0`
- Python: upstream requires Python 3.11 or newer.
- Runtime dependency: `pythainlp>=5.3.4`; TTS extras (ONNX/PyTorch) are not installed or used.
- Existing challenge: `data/benchmark/thai_g2p_challenge.jsonl`, 42 records, all phonemic/surface IPA gold fields null.
- Existing workflow: `.github/workflows/optional-external-g2p.yml`; it remains opt-in/triggered by selected file changes and uploads raw outputs plus a JSON summary.

## Layer-by-layer license and provenance register

| Layer | Evidence inspected | License / provenance | Integration treatment |
|---|---|---|---|
| FastThaiG2P Python code | Pinned upstream `LICENSE` and `NOTICE` | Apache-2.0; NOTICE attributes Amazon.com, Inc. or affiliates | Optional dependency only; no upstream source copied into ClippyFirst. Preserve upstream license/NOTICE when redistributing that dependency. |
| PyThaiNLP runtime | FastThaiG2P pinned `pyproject.toml` | PyThaiNLP software Apache-2.0; FastThaiG2P requires `pythainlp>=5.3.4` | Installed transitively by optional extra; no PyThaiNLP source copied. PyThaiNLP data/model assets are separately licensed and are not intentionally selected as the G2P dictionary. |
| FastThaiG2P word list and IPA dictionary | Pinned README and `data/README.md` | 62,112 dictionary keys; merged from manual overrides, Wiktionary-derived entries (~13k) and generated entries (~49k). The README does not provide a complete per-record license/provenance manifest in the inspected tree. | Do not copy or bundle `dict.txt`, `ipa.json`, `ipa_metadata.json` or source dumps in this repository. Use only through the upstream optional package while the source terms remain attached to that package. |
| Wiktionary-derived subset | Upstream README; NLP for Thai corpus catalogue | Wiktionary G2P source is listed as CC BY-SA 3.0 in the corpus catalogue; FastThaiG2P describes parsing a kaikki.org Thai dump but does not pin a per-row source manifest in its README. | Treat as share-alike source-derived data; do not claim the whole IPA dictionary is Apache-2.0 or independently gold. Exact row lineage remains incomplete. |
| Generated IPA subset | Pinned upstream README and data README | Approximately 49k entries generated with Claude Opus 4.6 via Bedrock; no distinct dataset license or full row-level provenance/validation record was found in the inspected files. | Provenance/license BLOCKED for redistribution; do not copy or treat as independent gold. |
| Manual overrides | Pinned upstream README and `data/sources/manual_overrides.json` | Upstream identifies these as hand-corrected entries; no separate data license/attribution statement found in inspected files. | Keep upstream; do not repackage or claim project authorship. |
| TLTK fallback source code | Pinned `fastthaig2p/_th2ipa.py` header | Explicit BSD 3-Clause notice, copyright Dept. of Linguistics, Chulalongkorn University (2018). | It is vendored by FastThaiG2P, not copied into ClippyFirst. If redistributed separately, preserve BSD notice and disclaimer. |
| TLTK fallback statistical/lexical data | Pinned `data/README.md` lists `sylseg.3g`, `thaisyl.dict`, `PhSTrigram.sts`, `thdict`, `sylform_var.pkl` | Described as vendored TLTK data; no separate per-file data license/provenance manifest was found in the inspected FastThaiG2P tree. TLTK software itself is BSD-3-Clause, but that alone does not establish every data file's rights. | Do not copy or redistribute these data files independently; retain as upstream package assets pending item-level confirmation. |
| ClippyFirst adapter and benchmark glue | New repository files | Original project code under repository MIT license; no FastThaiG2P implementation or dictionary copied. | Lazy optional import; no default runtime dependency. |

**License conclusion:** the FastThaiG2P software package itself is Apache-2.0 and can be consumed as an optional dependency alongside this MIT-licensed project. That conclusion does not relicense its dictionary, generated IPA, Wiktionary-derived records, or TLTK fallback data. The repository does not bundle those assets. The generated-data and fallback-data redistribution questions remain evidence-limited, not resolved.

Primary upstream references:
- https://github.com/awslabs/FastThaiG2P/tree/c4759eef7df03e11fcbb9aa83efe8cf21709fd2f
- https://github.com/awslabs/FastThaiG2P/blob/c4759eef7df03e11fcbb9aa83efe8cf21709fd2f/LICENSE
- https://github.com/awslabs/FastThaiG2P/blob/c4759eef7df03e11fcbb9aa83efe8cf21709fd2f/NOTICE
- https://nlpforthai.com/tasks/g2p/
- https://pypi.org/project/tltk/

## Comparable evaluation contract

All engines receive the exact same 42 source strings from the same JSONL corpus. The runner records raw outputs, version/commit/configuration, per-item elapsed time, initialization errors, per-input errors and conservative ClippyFirst abstentions. It reports per-engine coverage and latency diagnostics, plus pairwise raw-string/limited-format agreement.

No IPA normalization is used for accuracy. Slash removal and tone-stripped comparisons remain diagnostic only. The runner does not score this challenge because it contains **zero independently adjudicated IPA gold rows**. Inter-engine agreement is not accuracy; a larger coverage count is not evidence of better pronunciation.

ClippyFirst is measured using its existing conservative text-analysis path with dictionary word segmentation enabled. If any Thai token lacks a complete phonemic IPA result, that item is recorded as an abstention. The candidate does not create a grapheme-derived fallback or bypass the production IPA adapter.

## Results

The branch CI workflow is the execution source for the new same-corpus run. Until its artifact is inspected, results are **PENDING**. Local clone/test execution was unavailable in this session because the container could not resolve github.com. No test or benchmark pass is claimed here.

Acceptance criteria:
1. Optional adapter imports without FastThaiG2P installed; construction reports a clear optional-dependency error.
2. Adapter preserves upstream IPA exactly and rejects non-string inputs/results.
3. Same 42 records are passed to ClippyFirst, FastThaiG2P, thaiphon and (where its service starts) Goruut.
4. ClippyFirst abstentions are distinct from runtime errors.
5. Summary records coverage, median/p95 latency, pairwise agreement, corpus hash, Python/platform and engine pins.
6. Accuracy stays `NOT_MEASURED` while the independent gold count is zero.
7. CI runs adapter tests and uploads inspectable raw and summary artifacts.

## First optional CI attempt and correction — 2026-11-02

Optional workflow run [41431032031](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41431032031) completed successfully at the job level and uploaded artifact `thai-external-g2p-smoke` (artifact SHA-256 `d06f6a87d177a61780b3d58fc0bc74087f657ce8e0548c67bee4b20cd7275e8b`). Artifact inspection found an integration-environment defect: the workflow installed the external comparators but did not install the local src-layout ClippyFirst package. Therefore both `clippyfirst` and the wrapper-based `fastthaig2p` candidates failed initialization with `ModuleNotFoundError: No module named 'thai_ukrainian'`; only thaiphon and Goruut produced rows. This run is **not** a valid ClippyFirst/FastThaiG2P comparison.

The optional workflow was corrected to run `python -m pip install -e .` before installing the pinned comparators. A further correctness refinement routes ClippyFirst benchmark output through the typed `phonetic_result` object and appends its separate tone contour, rather than comparing segmental IPA without tone. The new PR-head workflow run must be inspected before reporting same-corpus coverage or latency. Accuracy remains NOT_MEASURED.

## Transcription-layer comparability refinement — 2026-11-02

FastThaiG2P's documented IPA convention includes unreleased final-stop diacritics (`̚`), while ClippyFirst explicitly separates phonemic IPA from conservative broad-surface IPA. To avoid conflating a layer mismatch with an error, the runner now emits two ClippyFirst profiles from the same typed `PhoneticResult`:
- `clippyfirst_phonemic`: `phonemic_ipa` + separate tone contour;
- `clippyfirst_surface`: `broad_surface_ipa` + separate tone contour.

FastThaiG2P remains its own upstream IPA convention; the broad-surface ClippyFirst profile is the closer representational comparison, not proof of identical phonetic scope. Both profiles preserve the typed adapter boundary and abstain when their selected IPA layer or tone is unavailable. The next optional workflow artifact will report both profiles side by side.

## First valid same-input run — 2026-11-02

- Optional workflow run: [41431679913](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41431679913), completed successfully.
- Artifact: `thai-external-g2p-smoke`, SHA-256 `ed6ed4a6e2eca2f87442d0c77062bfbe976a3d8bce763da0c6ffff4101e2dbd7`; 210 raw rows = 42 inputs × 5 candidate profiles.
- Frozen corpus SHA-256: `94d18b9f55c2be35d3d0b35811f53d306b9be6906ae4cc6ea2241d18ebadf6b8`; Python 3.12.15; Linux x86_64; checked-out PR merge commit `8276747a90cd3863dec6a44933efe5641025e28e` (workflow head branch commit `7900a7cc2e38bc69763f38273c97f73c6ebee2be)).
- Coverage and latency (single diagnostic run; median/p95 ms):
  - ClippyFirst phonemic: 28/42 (66.7%), 14 explicit abstentions, 0 runtime errors; 0.483 / 2.184.
  - ClippyFirst broad-surface: 23/42 (54.8%), 19 explicit abstentions, 0 runtime errors; 0.461 / 1.636.
  - FastThaiG2P: 42/42 (100%), 0 runtime errors; 0.032 / 2.109.
  - thaiphon 0.7.0: 42/42 (100%), 0 runtime errors; 0.174 / 0.889.
  - Goruut: 26/42 (61.9%), 16 per-input no-output failures; 0.496 / 0.690.
- Pairwise agreement with FastThaiG2P:
  - ClippyFirst phonemic: 12/28 raw exact (42.9%); 14/28 after slash and tone stripping (50.0%, diagnostic only).
  - ClippyFirst broad-surface: 9/23 raw exact (39.1%); 17/23 after slash and tone stripping (73.9%, diagnostic only). This higher tone-stripped agreement indicates that tone differences account for a material share of disagreements; it is not an accuracy score.
- Illustrative rows: `กา` and `กรรม` match exactly in ClippyFirst phonemic and FastThaiG2P (`/kaː˧/`, `/kam˧/`). For `บรรจุ`, ClippyFirst emits `/ban˧.tɕu˩/` while FastThaiG2P emits `/ban˧.t͡ɕuʔ˨˩/`; the latter matches the existing source-attested Wiktionary-derived IPA record more closely, but that record is not independent expert gold. For invalid challenge input `ข๊า`, FastThaiG2P returns `/kʰaː8˧/` (contains literal `8`), while conservative ClippyFirst abstains. Coverage therefore does not imply validity or correctness.
- Gold: **0 independently adjudicated rows**. Accuracy status: `NOT_MEASURED`. No engine is ranked for pronunciation accuracy.

This is an engineering comparison only. Latency is from one 42-item run and is not a stable performance benchmark; the challenge is intentionally adversarial and not a representative usage distribution. The new dual-profile runner's exact-head CI and fresh optional workflow run are still required after the latest branch updates.

## Exact-head verification — 2026-11-02

- Final spike branch head at this checkpoint: `84ca5c39e82e75db594a4a21152572a083d238db`.
- Exact-head main CI run [41432085958](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41432085958): all three jobs passed — `test`, `wheel-install-smoke`, `master-artifact`. Ruff reported “All checks passed”; pytest reported **326 passed, 1,169 subtests passed**. The complete existing repository checks, source/evidence validators, generated artifacts, browser tests, IPA adapter tests and wheel smoke completed successfully.
- Exact-head optional comparator run [41432085960](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41432085960): passed. Its install step successfully used `pip install -e ".[fastthaig2p]"`, validating the pinned optional extra itself.
- Final-head benchmark artifact SHA-256: `c93e2a97b635470dadbef3776009d0d181dc5fd0d9967a8b195bd3571c55bbb7`; 210 rows, 42 inputs × 5 profiles; corpus SHA-256 unchanged.
- Final-head median/p95 ms: ClippyFirst phonemic 0.487/2.199; ClippyFirst broad-surface 0.465/1.791; FastThaiG2P 0.030/2.116; thaiphon 0.180/0.889; Goruut 0.512/0.674. Coverage and pairwise agreement are unchanged from the first valid run.
- This verifies the optional adapter, report generation and engineering integration. It does **not** resolve independent-gold accuracy or item-level rights for upstream generated/manual/fallback data. No production runtime change was made.

## Final closeout run — 2026-11-02

- Latest branch head: `7d904b96b1790efeaa579b1552e2fbb41a5d2188` (documentation/audit closeout after code-bearing checkpoint `84ca5c39e82e75db594a4a21152572a083d238db`).
- Optional workflow [41432769499](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41432769499) passed on the latest branch head; the pinned optional extra was installed and all five profiles returned rows/explicit abstentions.
- Artifact SHA-256: `54fa65b4dada15bcf79d466441896435cee3df83e67f71b5236260f8337866c5`; 210 rows; corpus SHA-256 `94d18b9f55c2be35d3d0b35811f53d306b9be6906ae4cc6ea2241d18ebadf6b8`.
- Latest single-run median/p95 ms: ClippyFirst phonemic 0.479/2.701; ClippyFirst broad-surface 0.469/1.635; FastThaiG2P 0.032/2.203; thaiphon 0.169/0.884; Goruut 0.492/0.610. Coverage and pairwise agreement remain unchanged.
- Exact-head full CI on code-bearing checkpoint `84ca5c39e82e75db594a4a21152572a083d238db` passed all three jobs in [41432085958](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41432085958). A later documentation-only closeout commit is present on branch head `7d904b96b1790efeaa579b1552e2fbb41a5d2188`; CI run [41432769414](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/41432769414) is a subsequent documentation-head rerun and may still be in progress.
