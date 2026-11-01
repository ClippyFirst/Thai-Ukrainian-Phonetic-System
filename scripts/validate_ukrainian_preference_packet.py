#!/usr/bin/env python3
"""Validate the candidate-blind Ukrainian preference packet against source-attested IPA."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from thai_ukrainian.adjudication import (
    UKRAINIAN_PREFERENCE_FIELDS,
    validate_ukrainian_blind_packet,
)


def read_tsv(path: Path, required: tuple[str, ...] | list[str]) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        missing = set(required) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path}: missing columns: {', '.join(sorted(missing))}")
        if "engine_candidate" in (reader.fieldnames or []):
            raise ValueError(f"{path}: blind preference packet must not expose engine_candidate")
        return [{key: (value or "") for key, value in row.items()} for row in reader]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument(
        "--source", type=Path, default=Path("data/benchmark/source-attested-ipa.tsv")
    )
    args = parser.parse_args()
    try:
        packet = read_tsv(args.packet, UKRAINIAN_PREFERENCE_FIELDS)
        source = read_tsv(
            args.source,
            ("id", "thai", "phonemic_ipa", "source_id", "source_url", "license"),
        )
        result = validate_ukrainian_blind_packet(packet, source)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"error: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
