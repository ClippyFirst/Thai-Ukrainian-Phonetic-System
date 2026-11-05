# Third-party corpus data notices

The corpus archives below retain their own source licenses. They are not relicensed by the repository's root license. Any extracted or adapted labels must retain the applicable attribution and license terms.

## CCOST — Chulalongkorn Corpus of Spoken Thai

- Authors: Pittayawat Pittayaporn, Cathryn Yang, Sujinat Jitwiriyanont, and James Kirby.
- Dataset: [CCOST v1.0, Zenodo DOI 10.5281/zenodo.17366698](https://zenodo.org/records/17366698).
- Paper: [Pittayaporn et al. (2026), LREC 2026](https://aclanthology.org/2026.lrec-1.247/).
- Declared license: **CC BY-NC-SA 4.0** — attribution, non-commercial use, and ShareAlike apply. See the [license deed](https://creativecommons.org/licenses/by-nc-sa/4.0/).
- Repository file: `CCOST textgrid.zip`, owner-supplied TextGrid-only export, 488 `.TextGrid` members. The archive is not the upstream 6.2 GB mixed C-COST.zip and no upstream checksum/manifest was supplied. Its Git blob SHA-1 is `3b1e3978c2b3a232dce4fdcfd137bb572ce5467f`; this pins only the branch copy.
- No WAV/audio member is present in this supplied ZIP. The CI inspector reads only TextGrid members. Source labels are retained as source annotations and are not project gold.
- Project changes: the archive was supplied by the repository owner; no TextGrid label content was intentionally edited. Derived text exports preserve raw labels and must be distributed only under CC BY-NC-SA 4.0 with attribution and non-commercial ShareAlike conditions.

## LOTUSDIS — Thai far-field meeting corpus

- Authors: Pattara Tipaksorn, Sumonmas Thatphithakkul, Vataya Chunwijitra, and Kwanchiva Thangthai.
- Dataset: [NECTEC LOTUSDIS dataset card](https://huggingface.co/datasets/nectec/LOTUSDIS); paper [Tipaksorn et al. (2025)](https://arxiv.org/abs/2509.18722).
- Declared license: **CC BY-SA 4.0** — attribution and ShareAlike apply. See the [license deed](https://creativecommons.org/licenses/by-sa/4.0/).
- Repository file: `nectecLOTUSDIS textgrid.zip`, owner-supplied export with 90 `.TextGrid` members and one `textgrid/.DS_Store` metadata entry (6,148 uncompressed bytes). Its Git blob SHA-1 is `50518e9a54e0986935e7b1cff122eb43c0b9edbd`; this pins only the branch copy, not the upstream dataset snapshot.
- The TextGrid inspector/exporter reads only `.TextGrid` members. The `.DS_Store` metadata entry is deliberately not read. No recognized audio-extension member is present; the inspector does not open any non-TextGrid member. No audio bytes were read or extracted.
- The 90 parsed TextGrids contain recording-named orthographic transcript IntervalTiers. No phone/phoneme/toneme/IPA tiers were observed. These are conversational text context, not phonetic gold.
- Derived transcript exports must retain CC BY-SA 4.0 attribution and ShareAlike conditions.

## Use boundary

- The file-level licenses above are separate from the repository's root code license.
- CCOST's non-commercial restriction must be respected. Do not use CCOST-derived content commercially without separate permission.
- Do not infer audio absence from an extensionless ZIP member. The current exporter is safe because it reads only members whose suffix is `.TextGrid`.
- Do not describe either corpus's source annotations as independent expert gold. Any evaluation gold requires the project's independent blinded review and adjudication protocol.


## FastThaiG2P — optional software dependency

- Upstream: [awslabs/FastThaiG2P](https://github.com/awslabs/FastThaiG2P), pinned by this project to commit `4e82a291b4cf2876326744c6580121e9986ad354` in `pyproject.toml`.
- Upstream source code license: **Apache-2.0**. The upstream `NOTICE` attributes copyright to Amazon.com, Inc. or its affiliates. Retain the full license and relevant NOTICE if redistributing covered code.
- Vendored `fastthaig2p/_th2ipa.py` contains a separate **3-clause BSD** notice for the TLTK-derived parser, copyright Dept. of Linguistics, Chulalongkorn University (2018). Preserve its file-level copyright, conditions, and disclaimer if copied.
- **Bundled data is mixed provenance:** upstream documents a merged 62k dictionary containing Wiktionary/kaikki-derived entries, model-generated entries, and manual overrides, plus TLTK fallback data. kaikki.org states Wiktionary-derived data is available under CC BY-SA and GFDL. The upstream data README does not provide complete per-entry or per-file rights for every generated/manual/fallback asset.
- This repository uses FastThaiG2P as an optional external dependency and does not copy its dictionary or fallback data into project corpus assets. The full bundled-data redistribution rights are **not cleared** by the Apache-2.0 source license alone. Do not bulk-copy or redistribute those assets until component-level provenance and terms are confirmed.
- Detailed review: [FastThaiG2P license and bundled-data review](../docs/fastthaig2p-license-review-2026-11-05.md).
