#!/usr/bin/env python3
"""Create a deterministic, evidence-graded false-split/false-merge review.

The input is the pinned CC0 Wisesight source-annotated segmentation set. This
report is a triage aid, not independent expert-adjudicated segmentation gold.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "data" / "benchmark" / "segmentation-gold.tsv"
SOURCE_ID = "WISESIGHT1000-C1D063649ABC"
ENGINE = "clippyfirst-dictionary-max-match"
VERSION = "clippyfirst-dictionary-max-match-v1"


def boundary_offsets(tokens: list[str]) -> set[int]:
    """Match the benchmark contract: ignore boundaries touching whitespace."""
    offsets: set[int] = set()
    cursor = 0
    for token, next_token in zip(tokens, tokens[1:]):
        cursor += len(token)
        if not token.isspace() and not next_token.isspace():
            offsets.add(cursor)
    return offsets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("/tmp/thai-segmentation-error-review.json"))
    parser.add_argument("--examples-per-error", type=int, default=12)
    args = parser.parse_args()
    if args.examples_per_error < 1 or args.examples_per_error > 100:
        parser.error("--examples-per-error must be between 1 and 100")

    from thai_ukrainian.segmentation import segment_text_preserving

    with GOLD.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    if len(rows) != 993:
        raise ValueError(f"pinned Wisesight snapshot must contain 993 rows, found {len(rows)}")

    seen: set[str] = set()
    false_split_total = false_merge_total = gold_boundary_total = predicted_boundary_total = 0
    exact_sequence_count = 0
    split_examples: list[dict[str, object]] = []
    merge_examples: list[dict[str, object]] = []

    for row in rows:
        row_id = row.get("id", "")
        if not row_id or row_id in seen:
            raise ValueError(f"gold IDs must be non-empty and unique: {row_id!r}")
        seen.add(row_id)
        if (row.get("source_id") != SOURCE_ID or row.get("license") != "CC0-1.0"
                or row.get("gold_status") != "SOURCE_ANNOTATED" or row.get("split") != "test"):
            raise ValueError(f"unexpected evidence provenance for {row_id!r}")
        text = row["text"]
        gold_tokens = json.loads(row["gold_tokens_json"])
        if not isinstance(gold_tokens, list) or any(not isinstance(t, str) or not t for t in gold_tokens):
            raise ValueError(f"invalid gold token array for {row_id!r}")
        if "".join(gold_tokens) != text:
            raise ValueError(f"gold tokens do not reconstruct source text for {row_id!r}")
        predicted_tokens = segment_text_preserving(text)
        if not predicted_tokens or "".join(predicted_tokens) != text:
            raise ValueError(f"prediction does not reconstruct source text for {row_id!r}")

        gold = boundary_offsets(gold_tokens)
        predicted = boundary_offsets(predicted_tokens)
        false_splits = sorted(predicted - gold)
        false_merges = sorted(gold - predicted)
        gold_boundary_total += len(gold)
        predicted_boundary_total += len(predicted)
        false_split_total += len(false_splits)
        false_merge_total += len(false_merges)
        exact_sequence_count += int(gold_tokens == predicted_tokens)

        base = {
            "id": row_id,
            "text_excerpt": text[:180],
            "gold_tokens": gold_tokens,
            "predicted_tokens": predicted_tokens,
            "false_split_offsets_codepoints": false_splits,
            "false_merge_offsets_codepoints": false_merges,
            "gold_boundary_count": len(gold),
            "predicted_boundary_count": len(predicted),
        }
        if false_splits:
            split_examples.append({**base, "error_count": len(false_splits)})
        if false_merges:
            merge_examples.append({**base, "error_count": len(false_merges)})

    precision_denominator = false_split_total + (gold_boundary_total - false_merge_total)
    recall_denominator = gold_boundary_total
    precision = (false_split_total + gold_boundary_total - false_merge_total) / precision_denominator if precision_denominator else None
    recall = (gold_boundary_total - false_merge_total) / recall_denominator if recall_denominator else None
    # Standard boundary counts: TP = predicted boundaries not false splits.
    true_positive = predicted_boundary_total - false_split_total
    precision = true_positive / predicted_boundary_total if predicted_boundary_total else None
    recall = true_positive / gold_boundary_total if gold_boundary_total else None
    f1 = 2 * precision * recall / (precision + recall) if precision is not None and recall is not None and precision + recall else 0.0 if precision is not None and recall is not None else None

    order = lambda item: (-int(item["error_count"]), str(item["id"]))
    report = {
        "report_type": "SEGMENTATION_ERROR_TRIAGE_NOT_GOLD_ADJUDICATION",
        "dataset": {
            "name": "PyThaiNLP Wisesight word-tokenization labels",
            "rows_total": len(rows),
            "rows_source_annotated": len(rows),
            "rows_expert_adjudicated": 0,
            "source_id": SOURCE_ID,
            "license": "CC0-1.0",
            "upstream_commit": "c1d063649abc3a6870b5fd1aae26cd1c64bdde7b",
            "split": "test",
        },
        "engine": {"name": ENGINE, "version": VERSION},
        "metrics": {
            "gold_boundary_count": gold_boundary_total,
            "predicted_boundary_count": predicted_boundary_total,
            "false_split_count": false_split_total,
            "false_merge_count": false_merge_total,
            "true_positive_boundary_count": true_positive,
            "boundary_precision": precision,
            "boundary_recall": recall,
            "boundary_f1": f1,
            "exact_sequence_count": exact_sequence_count,
            "exact_sequence_rate": exact_sequence_count / len(rows),
        },
        "false_split_examples": sorted(split_examples, key=order)[:args.examples_per_error],
        "false_merge_examples": sorted(merge_examples, key=order)[:args.examples_per_error],
        "method": {
            "offset_unit": "Unicode code points in the original text",
            "boundary_policy": "exclude boundaries touching whitespace-only tokens",
            "example_order": "descending error count, then stable row ID",
            "caveats": [
                "Source labels are SOURCE_ANNOTATED, not independently expert-adjudicated.",
                "Examples are diagnostic triage, not a claim that every discrepancy is an engine error.",
                "No data from this report is used to train or tune the segmenter.",
                "Wisesight is test-only; do not use it to build the runtime lexicon.",
            ],
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "metrics": report["metrics"], "evidence_grade": report["dataset"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
