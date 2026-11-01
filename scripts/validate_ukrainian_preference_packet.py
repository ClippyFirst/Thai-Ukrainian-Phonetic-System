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
    validate_ukrainian_independent_pair,
    validate_ukrainian_review_packet,
)


def read_tsv(
    path: Path, required: tuple[str, ...] | list[str], *, exact: bool = True
) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        fields = set(reader.fieldnames or [])
        missing = set(required) - fields
        unexpected = fields - set(required)
        if missing or (exact and unexpected):
            raise ValueError(
                f"{path}: columns mismatch; missing={sorted(missing)}, unexpected={sorted(unexpected)}"
            )
        return [{key: (value or "") for key, value in row.items()} for row in reader]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--mode", choices=("blind", "review", "pair"), default="blind")
    parser.add_argument("--reviewer-id", default="")
    parser.add_argument("--reviewer-b-packet", type=Path)
    parser.add_argument(
        "--source", type=Path, default=Path("data/benchmark/source-attested-ipa.tsv")
    )
    args = parser.parse_args()
    try:
        packet = read_tsv(args.packet, UKRAINIAN_PREFERENCE_FIELDS)
        if args.mode == "blind":
            source = read_tsv(
                args.source,
                ("id", "thai", "phonemic_ipa", "source_id", "source_url", "license"),
                exact=False,
            )
            result = validate_ukrainian_blind_packet(packet, source)
        elif args.mode == "review":
            result = validate_ukrainian_review_packet(
                packet, [row["id"] for row in read_tsv(
                    args.source,
                    ("id", "thai", "phonemic_ipa", "source_id", "source_url", "license"),
                    exact=False,
                )], args.reviewer_id
            )
        else:
            if args.reviewer_b_packet is None:
                raise ValueError("--reviewer-b-packet is required in pair mode")
            reviewer_b = read_tsv(args.reviewer_b_packet, UKRAINIAN_PREFERENCE_FIELDS)
            result = validate_ukrainian_independent_pair(packet, reviewer_b)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"error: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
