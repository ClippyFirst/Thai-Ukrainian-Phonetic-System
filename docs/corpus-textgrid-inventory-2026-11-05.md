## Latest exact-head repository verification — 2026-11-05

- Branch: `docs/repository-audit-2026-11-04`; documentation checkpoint HEAD: `45bbd7386ede98c6fa63b015c9c7a303c436e699`; implementation checkpoint: `f9b6baf1ad3c55057051ff5652ac7827a06fd7c1`; base `main`: `56fba86b4b8be2fe4e67284355e9928108527387`; comparison at this checkpoint: **137 commits ahead, 0 behind**.
- PR [#210](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/210) is **OPEN, not merged**, targets `main`, and is mergeable. No mainline change, force-push, branch deletion or release was made.
- Exact-head Full CI [run 42018381197](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42018381197) succeeded on the documentation checkpoint HEAD. Jobs `test`, `wheel-install-smoke`, and `master-artifact` all passed. The test job reports **385 passed, 1 skipped, 1,206 subtests passed**; Ruff passed; 29 Python/browser parity fixtures passed; generated-artifact drift checks, source/reviewer packet validators, archive inspection, JSONL export, and artifact upload passed.
- The one skip is `tests/test_fastthaig2p_site_api.py` in the generic environment because FastAPI is optional and absent there. Dedicated FastThaiG2P Site API [run 42018381263](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42018381263) passed; optional external Thai G2P smoke [run 42018381361](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42018381361) passed.
- CI re-inspected 578/578 supplied TextGrid files and verified 178,377 orthographic JSONL rows (CCOST 145,434; LOTUSDIS 32,943). The current `textgrid-text-only-jsonl` artifact is [available from run 42018381197](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42018381197/artifacts/13411240199), 12,609,560 bytes, artifact digest `sha256:260ff20858e588f78152fdfb01d969f7160fbfc530ed2a8945758f80ee3c0fcb`. It contains text-only exports, manifest and notices; no audio is read or included.
- Linguistic status is unchanged: independent IPA gold rows **0**; accuracy **NOT_MEASURED**. The CCOST adapter remains PARTIAL with 1,014 unsupported labels; `_8`, Unicode IPA-looking strings, unusual sequences and mixed marker/text labels remain fail-closed.
- Current blockers: CCOST curator clarification of `-MAU` aliases and unsupported labels; two qualified independent Thai reviewers plus adjudicator; independent Ukrainian-native target review; hands-on accessibility review; FastThaiG2P bundled-data rights and Python-host preview. Global TIMIT and audio tasks remain DEFERRED/EXCLUDED by owner decision.
- Local tests were not run in this connector-only session. The exact-head GitHub Actions evidence above is the verification record; no local checkout or local test execution is claimed.
- Readiness: **ENGINEERING_VERIFIED_RESEARCH_PROTOTYPE_NOT_RELEASE_READY**. Software/packaging/CI gates pass, but independent linguistic and human accessibility gates remain unmet.

## Exact-head verification

On final workflow checkpoint `824c09098d2869256ab8206324b3e1fa1d6d6d81`: [CI run 42015757949](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42015757949) passed all jobs.

- Python: **385 passed, 1 skipped, 1,206 subtests passed**.
- Ruff: passed.
- Wheel-install smoke: passed.
- Master artifact: passed.
- Actual TextGrid inspection: 578/578 parse; no file-level parse errors.
- Actual orthographic export: 178,377 rows; source counts and license/evidence metadata assertions passed. The `textgrid-text-only-jsonl` artifact includes both JSONLs, a valid SHA-256 manifest and the third-party corpus notice.
- FastThaiG2P Site API: [42015757883](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42016775080) passed.
- Optional external Thai G2P smoke: [42015757971](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42016775087) passed.
- The one skipped test is optional FastAPI-dependent coverage in the generic Python test environment; the dedicated Site API workflow passed.

## Task ledger

| Task | Status | Evidence / remaining acceptance |
|---|---|---|
| Inventory supplied ZIPs without reading audio | DONE_VERIFIED | 488 CCOST + 90 LOTUSDIS TextGrid members; one `.DS_Store` metadata member skipped |
| Parse supplied TextGrid files | DONE_VERIFIED | 578/578 parse; long-text only |
| Export selected orthographic transcript intervals | DONE_VERIFIED | 178,377 provenance-rich JSONL records in CI; output not committed |
| LOTUSDIS source role | DONE_VERIFIED for supplied sample | Transcript-only interval tiers; no phonetic tiers observed |
| CCOST `-MAU` tier aliases | PARTIAL | Implemented provisional mapping; curator confirmation desirable |
| CCOST X-SAMPA coverage | PARTIAL | 1,014 labels unsupported; preserve and review, do not guess |
| Independent phonetic IPA gold | BLOCKED | Requires two qualified independent Thai reviewers and separate adjudication; current gold rows 0 |
| Audio acquisition/acoustic validation | DEFERRED / OUT OF SCOPE | Explicit owner decision |
| Global TIMIT Thai | DEFERRED / EXCLUDED | Explicit owner decision; do not pursue LDC access |

## License notices and primary references

- File-specific attribution and license terms: [third-party corpus notices](../data/THIRD-PARTY-CORPUS-NOTICES.md).
- [CCOST Zenodo record](https://zenodo.org/records/17366698), DOI 10.5281/zenodo.17366698.
- [Pittayaporn et al., “The Chulalongkorn Corpus of Spoken Thai”, LREC 2026](https://aclanthology.org/2026.lrec-1.247/).
- [NECTEC LOTUSDIS dataset card](https://huggingface.co/datasets/nectec/LOTUSDIS), license CC BY-SA 4.0.
- [Tipaksorn et al., “LOTUSDIS: A Thai far-field meeting corpus for robust conversational ASR”](https://arxiv.org/abs/2509.18722).