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

kaikki.org explicitly states that its Wiktionary-extracted data is available under **CC BY-SA and GFDL**. The FastThaiG2P data README does not provide per-entry attribution/rights metadata sufficient to prove that the merged `ipa.json`, word list, or generated/manual subset can all be relicensed solely under Apache-2.0. The generated entries and manual overrides do not have a separate rights grant described in the inspected data README. The TLTK fallback data files also need file-level notice/provenance confirmation before this project republishes them independently.

### 4. Project-specific conclusion

| Use | Finding |
|---|---|
| Depend on pinned FastThaiG2P code as an optional external package | **Permissible under the upstream Apache-2.0 grant**, while retaining its dependency identity and notices |
| Copy FastThaiG2P source into this repository | **Not done**; if ever done, preserve Apache LICENSE/NOTICE and the TLTK BSD-3 file notice |
| Copy or redistribute the full upstream IPA dictionary, word list, or fallback data in this repository | **Not cleared** by this review; mixed provenance and per-file terms must be resolved first |
| Promote FastThaiG2P IPA output to project gold | **Not permitted by evidence quality**; generated/lexical candidates remain provisional and require independent review |
| Use a small number of outputs internally for comparison | Keep source/version and method provenance; do not present them as ground truth |

The project's existing optional dependency remains pinned to the reviewed commit. No FastThaiG2P dictionary or fallback data has been copied into project corpus assets by this change. Do not redistribute a FastThaiG2P-derived bulk lexicon or claim that every bundled data asset is Apache-2.0-only.

## Required follow-up

1. Ask the FastThaiG2P maintainer for a component-level license/provenance statement for the merged runtime dictionary, generated entries, manual overrides, and each TLTK fallback data file.
2. Record the source snapshot and attribution for the 13k Wiktionary-derived subset; retain CC BY-SA/GFDL obligations as applicable.
3. Keep generated IPA and manual overrides separate from the Wiktionary subset in any future project dataset.
4. Preserve Apache LICENSE/NOTICE and TLTK BSD-3 notices if any source or fallback component is vendored.
5. Until that evidence exists, use FastThaiG2P only as the optional upstream dependency; do not copy its bundled datasets into the repository or release artifacts.

**Status:** source-code license verified; full bundled-data redistribution rights **PARTIAL / BLOCKED on per-component provenance**.
