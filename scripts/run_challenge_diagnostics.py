#!/usr/bin/env python3
"""Run the authored engine on the challenge set without claiming accuracy.

This is a reproducible runtime/abstention diagnostic. The challenge records do
not contain adjudicated gold, so this report intentionally emits no accuracy
or correctness score.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from thai_ukrainian.text import analyze_text

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "benchmark" / "thai_g2p_challenge.jsonl"
DEFAULT_OUTPUT = ROOT / "reports" / "challenge-runtime-diagnostics.json"


def load_challenge(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    with path.open("r", encoding="utf-8") as stream:
        for line_no, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
                raise ValueError(f"{path}:{line_no}: each record needs a non-empty string id")
            if row["id"] in seen:
                raise ValueError(f"{path}:{line_no}: duplicate id {row['id']!r}")
            if not isinstance(row.get("input"), str) or not row["input"]:
                raise ValueError(f"{path}:{line_no}: each record needs a non-empty string input")
            seen.add(row["id"])
            rows.append(row)
    return rows


def build_report(path: Path = DEFAULT_INPUT) -> dict[str, Any]:
    challenge = load_challenge(path)
    segmentation_counts: Counter[str] = Counter()
    analysis_counts: Counter[str] = Counter()
    details: list[dict[str, Any]] = []
    output_count = 0
    abstained_count = 0

    for row in challenge:
        tokens = analyze_text(row["input"])
        thai_tokens = [token for token in tokens if token.get("kind") == "thai"]
        syllables = [
            syllable
            for token in thai_tokens
            for syllable in token.get("syllables", [])
        ]
        segmentation = (
            thai_tokens[0].get("segmentation_status", "not_applicable")
            if len(thai_tokens) == 1
            else "multiple_or_no_thai_tokens"
        )
        segmentation_counts[segmentation] += 1
        for syllable in syllables:
            analysis_counts[str(syllable.get("status", "missing-status"))] += 1

        emitted = bool(syllables) and all(
            bool(syllable.get("phonemic_ipa"))
            and bool(syllable.get("ukrainian_transliteration"))
            for syllable in syllables
        ) and all(token.get("segmentation_status") != "unresolved" for token in thai_tokens)
        if emitted:
            output_count += 1
        else:
            abstained_count += 1

        details.append({
            "id": row["id"],
            "input": row["input"],
            "stratum": row.get("stratum"),
            "segmentation_status": segmentation,
            "token_count": len(tokens),
            "syllable_count": len(syllables),
            "analysis_statuses": [s.get("status") for s in syllables],
            "phonemic_ipa": [s.get("phonemic_ipa") for s in syllables],
            "surface_ipa": [s.get("phonetic_ipa") for s in syllables],
            "tone_categories": [
                (s.get("tone") or {}).get("tone") if isinstance(s.get("tone"), dict) else None
                for s in syllables
            ],
            "vowel_lengths": [s.get("vowel_length") for s in syllables],
            "ukrainian_outputs": [s.get("ukrainian_transliteration") for s in syllables],
            "warnings": [warning for token in tokens for warning in token.get("warnings", [])],
            "engine_output_emitted": emitted,
        })

    return {
        "schema_version": "1.0",
        "evaluation_kind": "runtime_diagnostic_not_accuracy_benchmark",
        "gold_status": "NOT_ADJUDICATED",
        "input_path": path.as_posix(),
        "summary": {
            "challenge_inputs": len(challenge),
            "inputs_with_engine_output": output_count,
            "inputs_abstained_or_without_complete_output": abstained_count,
            "segmentation_status_counts": dict(sorted(segmentation_counts.items())),
            "syllable_analysis_status_counts": dict(sorted(analysis_counts.items())),
        },
        "limitations": [
            "The challenge set has no independently adjudicated IPA or word-boundary gold.",
            "Output presence, parser status, and external-engine agreement are not correctness measures.",
            "Abstention is reported explicitly and is not counted as a pronunciation error.",
            "This hand-picked adversarial set is not a representative estimate of Thai coverage.",
        ],
        "records": details,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    try:
        report = build_report(args.input)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Diagnostic report written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
