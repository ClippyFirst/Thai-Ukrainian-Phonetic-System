#!/usr/bin/env python3
"""Evaluate the pinned dictionary segmenter on source-annotated Wisesight rows.

This is a held-out, source-annotated diagnostic. The upstream labels are not
independently re-adjudicated here, so the report must not be described as
expert-gold accuracy or phonetic accuracy.
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
SOURCE_ID = "WISESIGHT1000-C1D063649ABC"
ENGINE = "clippyfirst-dictionary-max-match"
VERSION = "clippyfirst-dictionary-max-match-v1"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("/tmp/wisesight1000-dictionary-segmentation.json"))
    args = parser.parse_args()

    # Package installation exposes the project module from src/.
    from thai_ukrainian.segmentation import segment_text_preserving

    with GOLD.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    if len(rows) != 993:
        raise ValueError(f"pinned Wisesight snapshot must contain 993 rows, found {len(rows)}")

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
                tokens = segment_text_preserving(row["text"])
                if not tokens or "".join(tokens) != row["text"]:
                    raise ValueError(f"dictionary segmenter failed exact reconstruction for {row.get('id')!r}")
                writer.writerow({
                    "id": row["id"],
                    "engine": ENGINE,
                    "predicted_tokens_json": json.dumps(tokens, ensure_ascii=False),
                    "status": "ok",
                    "version": VERSION,
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
        gold = report["gold"]
        engine = report["engines"][ENGINE]
        if gold["rows_total"] != 993 or gold["rows_source_annotated"] != 993 or gold["rows_adjudicated"] != 0:
            raise ValueError(f"source-gold accounting mismatch: {gold}")
        if gold["status"] != "MEASURED_ON_SOURCE_ANNOTATED_ROWS_NOT_EXPERT_ADJUDICATED":
            raise ValueError(f"gold evidence grade was not preserved: {gold}")
        if engine["n_gold_rows"] != 993 or engine["coverage"] != 1.0:
            raise ValueError(f"dictionary segmenter did not cover every test row: {engine}")
        if "not expert-adjudicated" not in report["method"]["accuracy_claim"]:
            raise ValueError("report lost the source-annotation caveat")
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
