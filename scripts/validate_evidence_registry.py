#!/usr/bin/env python3
"""Validate the machine-readable source and reviewer evidence registries."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from thai_ukrainian.evidence_registry import load_audio_asset_registry, load_reviewer_registry, load_source_registry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, default=Path("data/benchmark/source-registry.tsv"))
    parser.add_argument("--reviewers", type=Path, default=Path("data/benchmark/reviewer-qualifications.tsv"))
    parser.add_argument("--audio-assets", type=Path, default=Path("data/benchmark/audio-assets.tsv"))
    args = parser.parse_args()
    sources = load_source_registry(args.sources)
    reviewers = load_reviewer_registry(args.reviewers)
    audio_assets = load_audio_asset_registry(args.audio_assets, sources)
    print(json.dumps({
        "source_records": len(sources),
        "verified_source_records": sum(row["verification_status"] == "VERIFIED" for row in sources.values()),
        "blocked_source_records": sum(row["verification_status"] == "BLOCKED" for row in sources.values()),
        "verified_reviewer_records": sum(row["verification_status"] == "VERIFIED" for row in reviewers.values()),
        "audio_asset_records": len(audio_assets),
        "verified_audio_asset_records": sum(row["verification_status"] == "VERIFIED" for row in audio_assets.values()),
        "reviewer_registry_status": "READY" if reviewers else "VALID_EMPTY_NO_REVIEWERS_VERIFIED",
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
