#!/usr/bin/env python3
"""Run a reproducible no-automatic-word-segmentation baseline on Wisesight.

This is a segmentation diagnostic against upstream human source annotations,
not an expert-adjudicated gold benchmark and not a pronunciation benchmark.
"""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "data" / "benchmark" / "segmentation-gold.tsv"
SOURCE_ID = "WISIGHT1000-C1D063649ABC"
ENGINE_VERSION = "ClippyFirst-0.6.1-text-tokenizer-no-auto-word-segmentation"


def source_preserving_tokens(text: str) -> list[str]:
    """Mirror text.tokenize_text's character-kind runs but preserve whitespace.

    The production text tokenizer discards whitespace tokens. The benchmark
    adapter retains them so token strings concatenate exactly to the source;
    the scorer excludes whitespace-only boundaries from lexical word metrics.
    """
    from thai_ukrainian.text import _kind

    if not text:
        return []
    tokens: list[str] = []
    start = 0
    previous = _kind(text[0])
    for index, char in enumerate(text[1:], 1):
        kind = _kind(char)
        if kind != previous:
            tokens.append(text[start:index])
            start = index
            previous = kind
    tokens.append(text[start:])
    return tokens


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("/tmp/wisesight1000-segmentation-baseline.json"))
    args = parser.parse_args()

    with GOLD.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    if not rows:
        raise ValueError("Wisesight source-annotated gold file is empty")
    if len(rows) != 993:
        raise ValueError(f"pinned Wisesight snapshot must contain 993 records, found {len(rows)}")

    with tempfile.TemporaryDirectory() as directory:
        predictions_path = Path(directory) / "predictions.tsv"
        with predictions_path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(
                stream,
                fieldnames=["id", "engine", "predicted_tokens_json", "status", "version"],
                delimiter="\t",
            )
            writer.writeheader()
            for row in rows:
                if row.get("source_id") != SOURCE_ID or row.get("license") != "CC0-1.0":
                    raise ValueError(f"unexpected source provenance for {row.get('id')!r}")
                tokens = source_preserving_tokens(row["text"])
                if not tokens or "".join(tokens) != row["text"]:
                    raise ValueError(f"prediction adapter failed source reconstruction for {row.get('id')!r}")
                writer.writerow({
                    "id": row["id"],
                    "engine": "clippyfirst-text-tokenizer-baseline",
                    "predicted_tokens_json": json.dumps(tokens, ensure_ascii=False),
                    "status": "ok",
                    "version": ENGINE_VERSION,
                })

        args.output.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "evaluate_segmentation.py"),
                "--gold", str(GOLD),
                "--predictions", str(predictions_path),
                "--output", str(args.output),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            sys.stderr.write(result.stderr)
            return result.returncode
        report = json.loads(args.output.read_text(encoding="utf-8"))
        if report["gold"]["rows_total"] != 993 or report["gold"]["rows_source_annotated"] != 993:
            raise ValueError(f"source gold accounting mismatch: {report['gold']}")
        if report["gold"]["status"] != "MEASURED_ON_SOURCE_ANNOTATED_ROWS_NOT_EXPERT_ADJUDICATED":
            raise ValueError(f"gold evidence grade was not preserved: {report['gold']}")
        if report["engines"]["clippyfirst-text-tokenizer-baseline"]["n_gold_rows"] != 993:
            raise ValueError("baseline did not retain all source-annotated rows in its denominator")
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
