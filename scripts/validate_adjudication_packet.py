#!/usr/bin/env python3
"""Validate blank or completed independent Thai phonetic adjudication packets."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from thai_ukrainian.adjudication import (
    PACKET_FIELDS,
    validate_blind_packet,
    validate_independent_pair,
    validate_review_packet,
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        missing = set(PACKET_FIELDS) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path}: missing columns: {', '.join(sorted(missing))}")
        return [{key: (value or "") for key, value in row.items()} for row in reader]


def read_challenge(path: Path) -> list[dict[str, str]]:
    rows = []
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc.msg}") from exc
            rows.append({
                "id": str(value.get("id") or ""),
                "input": str(value.get("input") or ""),
                "stratum": str(value.get("stratum") or ""),
                "probe": str(value.get("probe") or ""),
            })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--challenge", type=Path, required=True)
    parser.add_argument("--mode", choices=("blind", "review", "pair"), default="blind")
    parser.add_argument("--reviewer-id", default="")
    parser.add_argument("--reviewer-b-packet", type=Path)
    args = parser.parse_args()
    try:
        rows = read_tsv(args.packet)
        challenge = read_challenge(args.challenge)
        if args.mode == "blind":
            result = validate_blind_packet(rows, challenge)
        elif args.mode == "review":
            result = validate_review_packet(rows, [row["id"] for row in challenge], args.reviewer_id)
        else:
            if args.reviewer_b_packet is None:
                raise ValueError("--reviewer-b-packet is required in pair mode")
            reviewer_b = read_tsv(args.reviewer_b_packet)
            result = validate_independent_pair(rows, reviewer_b)
            result["reviewer_a"] = validate_review_packet(
                rows, [row["id"] for row in challenge], result["reviewer_a_id"]
            )
            result["reviewer_b"] = validate_review_packet(
                reviewer_b, [row["id"] for row in challenge], result["reviewer_b_id"]
            )
    except (OSError, ValueError) as exc:
        parser.exit(1, f"error: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
