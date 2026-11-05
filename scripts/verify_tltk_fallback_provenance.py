#!/usr/bin/env python3
"""Verify the pinned FastThaiG2P TLTK-derived fallback asset transformations."""
from __future__ import annotations

import argparse
import bz2
import hashlib
import json
from pathlib import Path

PAIRS = {
    "PhSTrigram.sts": ("data/fallback/PhSTrigram.sts", "tltk/PhSTrigram.sts", "identical"),
    "sylrule.lts": ("data/fallback/sylrule.lts", "tltk/sylrule.lts", "identical"),
    "sylseg.3g": ("data/fallback/sylseg.3g", "tltk/sylseg.3g", "identical"),
    "thaisyl.dict": ("data/fallback/thaisyl.dict", "tltk/thaisyl.dict", "identical"),
    "thdict": ("data/fallback/thdict", "tltk/thdict", "identical"),
    "sylform_var.pkl": ("data/fallback/sylform_var.pkl", "tltk/sylform_var.pklz", "bzip2_decompressed"),
}
EXPECTED_FASTTHAIG2P_COMMIT = "4e82a291b4cf2876326744c6580121e9986ad354"
EXPECTED_TLTK_FILE_COMMIT = "0cef4bcfbdd675f589783dd4134b87b9bb9fbb93"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify(fast_root: Path, tltk_root: Path) -> dict:
    fast_source = (fast_root / "fastthaig2p/_th2ipa.py").read_text(encoding="utf-8")
    if "Thai Language Toolkit : version  1.3.8" not in fast_source:
        raise SystemExit("Vendored FastThaiG2P parser no longer identifies TLTK 1.3.8")
    setup_source = (tltk_root / "setup.py").read_text(encoding="utf-8")
    repository_license = (tltk_root / "LICENSE").read_text(encoding="utf-8")
    module_license = (tltk_root / "LICENSE.txt").read_text(encoding="utf-8")
    package_metadata = (tltk_root / "PKG-INFO").read_text(encoding="utf-8")
    if "version='1.9.1'" not in setup_source:
        raise SystemExit("Pinned TLTK repository setup.py version changed")
    if "GNU LESSER GENERAL PUBLIC LICENSE" not in repository_license:
        raise SystemExit("Pinned TLTK repository LICENSE no longer identifies LGPL-3.0")
    if "Redistribution and use in source and binary forms" not in module_license:
        raise SystemExit("Pinned TLTK LICENSE.txt no longer contains the BSD-style module notice")
    if "Version: 1.1.7" not in package_metadata or "License: GPLv3" not in package_metadata:
        raise SystemExit("Pinned TLTK PKG-INFO no longer matches the recorded stale metadata")
    records = []
    for name, (fast_rel, tltk_rel, transform) in PAIRS.items():
        fast_bytes = (fast_root / fast_rel).read_bytes()
        tltk_bytes = (tltk_root / tltk_rel).read_bytes()
        transformed = bz2.decompress(tltk_bytes) if transform == "bzip2_decompressed" else tltk_bytes
        if fast_bytes != transformed:
            raise SystemExit(f"TLTK fallback asset transformation mismatch: {name}")
        records.append({
            "asset": name,
            "fastthaig2p_path": fast_rel,
            "tltk_path": tltk_rel,
            "transform": transform,
            "fastthaig2p_sha256": digest(fast_bytes),
            "tltk_source_sha256": digest(tltk_bytes),
            "transformed_sha256": digest(transformed),
            "verified": True,
        })
    return {
        "fastthaig2p_commit": EXPECTED_FASTTHAIG2P_COMMIT,
        "tltk_file_last_change_commit": EXPECTED_TLTK_FILE_COMMIT,
        "fastthaig2p_vendored_parser_header_version": "1.3.8",
        "fastthaig2p_vendored_parser_header_license": "BSD-3-Clause",
        "pinned_tltk_repository_setup_version": "1.9.1",
        "pinned_tltk_repository_root_license": "LGPL-3.0",
        "pinned_tltk_module_license_txt": "BSD-3-Clause-style notice",
        "pinned_tltk_pkg_info": {
            "version": "1.1.7",
            "license": "GPLv3",
            "status": "STALE_METADATA_RELATIVE_TO_SETUP_PY_1_9_1",
        },
        "license_scope": "AMBIGUOUS_RETAIN_BOTH_LGPL_AND_BSD_NOTICES_PENDING_FILE_LEVEL_REVIEW",
        "assets": records,
        "verified_assets": len(records),
        "status": "BYTE_OR_BZIP2_DECOMPRESSION_TRANSFORM_VERIFIED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fastthaig2p", type=Path, required=True)
    parser.add_argument("--tltk", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    report = verify(args.fastthaig2p, args.tltk)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
