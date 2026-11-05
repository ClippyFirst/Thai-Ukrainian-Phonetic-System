# FastThaiG2P license and bundled-data review — 2026-11-05

## Scope

The project pins FastThaiG2P in `pyproject.toml` to commit `4e82a291b4cf2876326744c6580121e9986ad354` through the optional `fastthaig2p` extra. This review checked the license, NOTICE, README, data README, package build configuration, and vendored TLTK parser at that exact upstream commit. It is a repository compliance review, not legal advice.

Primary sources:
- [Pinned FastThaiG2P LICENSE](https://github.com/awslabs/FastThaiG2P/blob/4e82a291b4cf2876326744c6580121e9986ad354/LICENSE)
- [Pinned FastThaiG2P NOTICE](https://github.com/awslabs/FastThaiG2P/blob/4e82a291b4cf2876326744c6580121e9986ad354/NOTICE)
- [Pinned FastThaiG2P README](https://github.com/awslabs/FastThaiG2P/blob/4e82a291b4cf2876326744c6580121e9986ad354/README.md)
- [FastThaiG2P data README](https://github.com/awslabs/FastThaiG2P/blob/4e82a291b4cf2876326744c6580121e9986ad354/data/README.md)
- [kaikki.org Thai Wiktionary data licensing](https://kaikki.org/thwiktionary/index.html)
- [CC BY-SA 4.0 deed](https://creativecommons.org/licenses/by-sa/4.0/)
- [GNU Free Documentation License](https://www.gnu.org/licenses/fdl-1.3.html)

## Findings

### 1. Upstream software source

- The pinned repository contains the full **Apache License 2.0** text.
- Its `NOTICE` contains: `Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.`
- Apache-2.0 permits commercial use, modification, and redistribution of the covered software, subject to its conditions. Redistribution of covered source/binaries must include the license, preserve applicable notices, mark modified files, and reproduce relevant NOTICE attributions.
- The project does not vendor FastThaiG2P source files into this repository; it declares a pinned optional Git dependency. Do not remove the upstream license/NOTICE from any future vendored copy.

### 2. Vendored TLTK parser

The pinned `fastthaig2p/_th2ipa.py` carries its own copyright and **3-clause BSD** notice:

- Copyright (c) 2018 Dept. of Linguistics, Chulalongkorn University.
- Source and binary redistribution are permitted if the specified copyright notice, conditions, and disclaimer are retained.
- The no-endorsement condition also applies.

This file-level BSD notice is separate from the top-level Apache license. The pinned source retains the notice in the file header. The upstream `data/README.md` also describes the fallback syllable parser data as vendored from TLTK; individual data-file provenance/licensing is not separately itemized there.

### 3. Bundled dictionary is mixed-provenance data, not just Apache-licensed code

The pinned upstream README and data README state that the runtime wheel includes:
- `data/dict.txt` — 62k word list;
- `data/ipa.json` — merged runtime IPA dictionary;
- `data/fallback/` — vendored TLTK syllable-parser data.

The build configuration force-includes these assets in the wheel. The merged dictionary sources are:
- approximately 13k Wiktionary-derived IPA entries extracted from the kaikki.org Thai dump;
- approximately 49k generated IPA entries produced with Claude Opus 4.6 via AWS Bedrock;
- manual overrides, with highest merge priority.

kaikki.org explicitly states that its Wiktionary-extracted data is available under **CC BY-SA and GFDL**. The data README documents a per-word `ipa_metadata.json` audit trail (`source`, `pos`, `origin`), and the merge script tags Wiktionary and generated entries separately. There is no per-entry `license` field, but source-category provenance is available for separating the components. The repository's Apache-2.0 grant appears to cover project-authored manual overrides and generated entries; Wiktionary-derived entries retain CC BY-SA/GFDL obligations. TLTK fallback files are listed as vendored and are included in TLTK's BSD-3-Clause package data; preserve the TLTK notices.

### 4. Project-specific conclusion

| Use | Finding |
|---|---|
| Depend on pinned FastThaiG2P code as an optional external package | **Permissible under the upstream Apache-2.0 grant**, while retaining its dependency identity and notices |
| Copy FastThaiG2P source into this repository | **Not done**; if ever done, preserve Apache LICENSE/NOTICE and the TLTK BSD-3 file notice |
| Copy or redistribute the upstream IPA dictionary, word list, or fallback data | **Permitted with component-appropriate terms and notices**: separate/attribute Wiktionary-derived material under CC BY-SA/GFDL; retain Apache-2.0 and TLTK BSD-3 notices for the corresponding components |
| Promote FastThaiG2P IPA output to project gold | **Not permitted by evidence quality**; generated/lexical candidates remain provisional and require independent review |
| Use a small number of outputs internally for comparison | Keep source/version and method provenance; do not present them as ground truth |

The project's existing optional dependency remains pinned to the reviewed commit. No FastThaiG2P dictionary or fallback data has been copied into project corpus assets by this change. Do not claim that every bundled data asset is Apache-2.0-only. A repackaged copy must preserve source separation/attribution and all applicable licenses; the current project does not vendor the dictionary.

## Required follow-up

1. Ask the FastThaiG2P maintainer for a component-level license/provenance statement for the merged runtime dictionary, generated entries, manual overrides, and each TLTK fallback data file.
2. Record the source snapshot and attribution for the 13k Wiktionary-derived subset; retain CC BY-SA/GFDL obligations as applicable.
3. Keep generated IPA and manual overrides separate from the Wiktionary subset in any future project dataset.
4. Preserve Apache LICENSE/NOTICE and TLTK BSD-3 notices if any source or fallback component is vendored.
5. The optional dependency and internal candidate outputs may continue to be used now. Vendoring is optional; if undertaken, package the source-separated data and notices rather than flattening it under Apache-2.0 alone.

**Status:** source-code license verified; data-use rights **PERMITTED WITH CONDITIONS**; project-side vendoring/repackaging is **PARTIAL / NOT IMPLEMENTED**.


## Follow-up rights check — 2026-11-05

The exact pinned files were re-opened through the GitHub connector. This confirms the following narrower position:

- The full top-level FastThaiG2P LICENSE is Apache-2.0; NOTICE attributes copyright to Amazon.com, Inc. or its affiliates.
- The vendored _th2ipa.py file carries a complete BSD-3-Clause notice for the TLTK-derived parser.
- The upstream data README explicitly says the runtime wheel force-includes dict.txt, ipa.json, and data/fallback/. It describes ipa.json as a merge of Wiktionary and generated IPA; source priorities are manual overrides, Wiktionary, then generated entries.
- TLTK's `setup.py` declares `BSD-3-Clause` and explicitly packages the fallback files (`sylrule.lts`, `thaisyl.dict`, `PhSTrigram.sts`, `sylseg.3g`, `sylform_var.pklz`, `thdict`); `LICENSE.txt` contains the corresponding BSD-3-Clause terms. Five FastThaiG2P fallback files have byte-identical Git blob hashes to the matching TLTK files; `sylform_var.pkl` is the uncompressed counterpart of TLTK's `.pklz` file (byte equivalence not checked). TLTK's repository also contains a separate LGPL-3.0 `LICENSE`, so the exact package/file scope should be kept visible rather than asserting that every repository file has one uniform license. The package metadata, `LICENSE.txt`, packaged-file list, and FastThaiG2P's own BSD header provide strong support for BSD-3-Clause coverage of the vendored fallback/parser components.
- The upstream README attributes about 13k IPA entries to kaikki/Wiktionary and about 49k to Claude Opus 4.6, with manual overrides as the highest-priority layer. The data README says `ipa_metadata.json` records a per-word `source`, `pos`, and `origin`; the merge script tags entries as `wiktionary` or `generated` and records the model for generated entries. This is useful source-category provenance, although the metadata schema has no explicit license field. kaikki states Wiktionary-extracted material is under CC BY-SA and GFDL. The upstream repository's Apache-2.0 grant appears to cover its own manual/generated project files absent a contrary file-specific notice; it does not erase the upstream Wiktionary terms for the extracted subset.

**Answer to the whole-dictionary question:** No single blanket license or complete rights statement for the entire bundled dictionary was found. It is not accurate to say that all 62k entries and all fallback data are simply Apache-2.0. The Wiktionary-derived portion carries upstream share-alike/attribution terms; the generated/manual portions and TLTK fallback assets need explicit provenance/rights clarification. The Apache-2.0 code license does not settle those data questions.

Primary references:
- [Pinned FastThaiG2P data README](https://github.com/awslabs/FastThaiG2P/blob/4e82a291b4cf2876326744c6580121e9986ad354/data/README.md)
- [TLTK upstream repository](https://github.com/attapol/tltk)
- [TLTK BSD-3 license file](https://github.com/attapol/tltk/blob/master/LICENSE.txt)
- [kaikki.org license statement](https://kaikki.org/thwiktionary/index.html)

This is a source-based compliance assessment, not a legal opinion. **Bulk redistribution is not categorically prohibited**: it is permissible only if the project preserves the Wiktionary-derived subset's CC BY-SA/GFDL obligations, attributes the source, and retains Apache-2.0/BSD-3 notices for the other components. This repository has not copied or repackaged that dataset.


## Public-source reconciliation — 2026-11-05

A deeper GitHub inspection refines (but does not reverse) the previous finding:

- FastThaiG2P `data/README.md` explicitly documents `ipa_metadata.json` as `{ipa, source, pos, origin, ...}` per word. `scripts/merge_ipa.py` records `source: wiktionary` or `source: generated` and stores `model: claude-opus-4.6` for generated entries. This means the upstream data has source-category audit metadata; the earlier wording that implied no per-entry source tracking was too broad. It still has no explicit per-entry license field.
- The upstream project has a top-level Apache-2.0 LICENSE and no separate restrictive license notice for its own manual overrides or generated entries. The best-supported reading is that those project-authored/generated assets are offered under the repository's Apache-2.0 grant. Do not claim that the Wiktionary-derived subset is thereby relicensed: its upstream CC BY-SA/GFDL terms remain relevant.
- The FastThaiG2P fallback data README says the files are vendored from TLTK. TLTK `setup.py` declares BSD-3-Clause and packages the same fallback assets; `LICENSE.txt` contains BSD-3-Clause. Five matching assets have identical Git blob hashes. The TLTK repository also contains a separate LGPL-3.0 `LICENSE`, so retain both upstream notices and avoid flattening the entire TLTK repository to one license.
- The paper itself is marked CC BY-NC-SA 4.0 on its public preprint page; that is the paper's license and must not be confused with the GitHub source-code license or treated as an automatic data license for the package.

**Operational decision:** using the pinned FastThaiG2P package as the project's optional external dependency, and using a limited number of its outputs internally as clearly labelled candidates, is allowed by the evidence currently available. This project already does so without copying the bundled dictionary into its own corpus. The unresolved issue is narrower: redistributing a copied/merged 62k dictionary as a standalone project asset requires preserving the Wiktionary-derived subset's attribution/ShareAlike obligations and making the component split and applicable notices explicit. That is a packaging/rights-evidence task, not a reason to disable the optional dependency or reject all use.

Primary source additions:
- [FastThaiG2P data README](https://github.com/awslabs/FastThaiG2P/blob/4e82a291b4cf2876326744c6580121e9986ad354/data/README.md)
- [FastThaiG2P merge script](https://github.com/awslabs/FastThaiG2P/blob/4e82a291b4cf2876326744c6580121e9986ad354/scripts/merge_ipa.py)
- [TLTK setup.py](https://github.com/attapol/tltk/blob/master/setup.py)
- [TLTK BSD license](https://github.com/attapol/tltk/blob/master/LICENSE.txt)
- [TLTK LGPL license](https://github.com/attapol/tltk/blob/master/LICENSE)
- [FastThaiG2P paper/preprint page](https://arxiv.org/abs/2608.12814).


## GitHub Pages browser-port follow-up — 2026-11-05

The browser bundle now applies the upstream per-entry source metadata instead of redistributing the merged dictionary as a single undifferentiated asset.

- CI retained exactly **13,144** `wiktionary` records and excluded **48,957** `generated` records. No manual or unknown-source rows were present in the pinned runtime metadata. The tokenizer wordlist was reduced to the 13,144 retained IPA keys.
- One runtime value (`สวน`) differs from its `ipa_metadata.json` snapshot. The source label remains Wiktionary; the current runtime IPA is preserved and the mismatch is recorded in the embedded provenance file rather than silently rewritten.
- The filtered FastThaiG2P wheel now embeds `browser-data-provenance.json` and `WIKTIONARY-ATTRIBUTION.md`. The attribution names Wiktionary contributors and Kaikki.org/Wiktextract, records the filtering/modification, and identifies CC BY-SA 4.0 for the derived Wiktionary subset. The generated and manual layers are not redistributed in this browser wheel.
- FastThaiG2P's vendored `_th2ipa.py` header explicitly identifies TLTK version 1.3.8 and carries a BSD-3-Clause notice. The TLTK 1.3.8 PyPI release page also identifies BSD-3-Clause. Five of six fallback data files have exact Git blob SHA matches with corresponding TLTK repository files. The remaining `sylform_var.pkl` differs from TLTK's `.pklz` file in size/format; the exact transformation is not independently reproduced.
- The TLTK repository's root LGPL-3.0 file and older GPLv3 package metadata remain disclosed alongside its BSD-3-Clause `LICENSE.txt`; they are not silently removed from the evidence. The public notice page explains this distinction.
- Ten third-party/project license and attribution notices are staged under `web/licenses/`. The bundle builder requires them, records their SHA-256/size in `bundle-manifest.json`, and the worker requires the full notice set. The Pages post-deploy smoke is configured to fetch and hash-check every notice.

Verification at code checkpoint `9894c80a4c47fe0b1e3b966ff4f6fb3dcaa2e124`:
- Pyodide parity and real Chromium worker smoke: [42073702543](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42073702543), SUCCESS.
- Full CI: [42073702565](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42073702565), SUCCESS.
- Web static validation: [42073702564](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42073702564), SUCCESS.
- Site API reference wrapper: [42073702559](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42073702559), SUCCESS.
- Optional external smoke: [42073702598](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/42073702598), SUCCESS.

**Current operational position:** the source-filtered ephemeral CI bundle and attribution notices are verified. `redistribution_approved` remains false; the Pages build refuses public packaging, and no live deployment or merge was performed. The remaining TLTK pickle transformation evidence is recorded as PARTIAL, not treated as resolved. This review remains a source-based compliance assessment, not legal advice.
