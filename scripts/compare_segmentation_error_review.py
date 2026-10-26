#!/usr/bin/env python3
"""Compare dictionary and TUD segmentation errors on identical Wisesight rows.

This is a reproducible triage report against source-annotated labels, not
independent expert adjudication or a release-quality accuracy benchmark.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "data" / "benchmark" / "segmentation-gold.tsv"
SOURCE_ID = "WISESIGHT1000-C1D063649ABC"


def boundary_offsets(tokens: list[str]) -> set[int]:
    offsets: set[int] = set()
    cursor = 0
    for token, next_token in zip(tokens, tokens[1:]):
        cursor += len(token)
        if not token.isspace() and not next_token.isspace():
            offsets.add(cursor)
    return offsets


def segment_tud_preserving(text: str, counts: dict[str, int], penalty: float) -> list[str]:
    """Apply the TUD model only to Thai runs, copying other runs unchanged."""
    from thai_ukrainian.text import _kind
    from train_tud_word_segmenter import segment

    if not text:
        return []
    output: list[str] = []
    start = 0
    previous_kind = _kind(text[0])
    for index, char in enumerate(text[1:], 1):
        kind = _kind(char)
        if kind != previous_kind:
            chunk = text[start:index]
            output.extend(segment(chunk, counts, penalty) if previous_kind == "thai" else [chunk])
            start, previous_kind = index, kind
    chunk = text[start:]
    output.extend(segment(chunk, counts, penalty) if previous_kind == "thai" else [chunk])
    if "".join(output) != text:
        raise AssertionError("TUD segmentation must preserve the source text exactly")
    return output


def score_engine(
    rows: list[dict[str, str]],
    segmenter: Callable[[str], list[str]],
    examples_per_error: int,
) -> dict:
    fp = fn = gold_total = pred_total = tp = exact = 0
    false_split_examples: list[dict] = []
    false_merge_examples: list[dict] = []
    for row in rows:
        text = row["text"]
        gold_tokens = json.loads(row["gold_tokens_json"])
        predicted = segmenter(text)
        if not predicted or "".join(predicted) != text:
            raise ValueError(f"prediction does not reconstruct input: {row['id']}")
        gold_b, pred_b = boundary_offsets(gold_tokens), boundary_offsets(predicted)
        splits, merges = sorted(pred_b - gold_b), sorted(gold_b - pred_b)
        tp += len(gold_b & pred_b)
        fp += len(splits)
        fn += len(merges)
        gold_total += len(gold_b)
        pred_total += len(pred_b)
        exact += int(gold_tokens == predicted)

        def contexts(offsets: list[int]) -> list[dict[str, object]]:
            return [
                {
                    "offset_codepoints": offset,
                    "left_context": text[max(0, offset - 12):offset],
                    "right_context": text[offset:min(len(text), offset + 12)],
                }
                for offset in offsets
            ]

        base = {
            "id": row["id"],
            "text_excerpt": text[:180],
            "gold_tokens": gold_tokens,
            "predicted_tokens": predicted,
            "false_split_offsets_codepoints": splits,
            "false_merge_offsets_codepoints": merges,
            "false_split_contexts": contexts(splits),
            "false_merge_contexts": contexts(merges),
        }
        if splits:
            false_split_examples.append({**base, "error_count": len(splits)})
        if merges:
            false_merge_examples.append({**base, "error_count": len(merges)})

    precision = tp / pred_total if pred_total else None
    recall = tp / gold_total if gold_total else None
    f1 = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else None
    order = lambda item: (-int(item["error_count"]), str(item["id"]))
    return {
        "metrics": {
            "gold_boundary_count": gold_total,
            "predicted_boundary_count": pred_total,
            "true_positive_boundary_count": tp,
            "false_split_count": fp,
            "false_merge_count": fn,
            "boundary_precision": precision,
            "boundary_recall": recall,
            "boundary_f1": f1,
            "exact_sequence_count": exact,
            "exact_sequence_rate": exact / len(rows) if rows else None,
        },
        "false_split_examples": sorted(false_split_examples, key=order)[:examples_per_error],
        "false_merge_examples": sorted(false_merge_examples, key=order)[:examples_per_error],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tud-model", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("/tmp/thai-segmentation-comparative-error-review.json"))
    parser.add_argument("--examples-per-error", type=int, default=8)
    args = parser.parse_args()
    if not 1 <= args.examples_per_error <= 100:
        parser.error("--examples-per-error must be between 1 and 100")
    model = json.loads(args.tud_model.read_text(encoding="utf-8"))
    if model.get("model_id") != "clippyfirst-tud-unigram-viterbi-v1" or model.get("source_license") != "CC-BY-SA-4.0":
        raise ValueError("unexpected TUD model identity or license")
    counts, penalty = model.get("word_counts"), model.get("token_penalty")
    if not isinstance(counts, dict) or not counts or not isinstance(penalty, (int, float)):
        raise ValueError("invalid TUD model counts or token penalty")

    with GOLD.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    if len(rows) != 993:
        raise ValueError(f"pinned Wisesight snapshot must contain 993 rows, found {len(rows)}")
    seen: set[str] = set()
    for row in rows:
        if not row.get("id") or row["id"] in seen:
            raise ValueError(f"gold IDs must be non-empty and unique: {row.get('id')!r}")
        seen.add(row["id"])
        if (row.get("source_id") != SOURCE_ID or row.get("license") != "CC0-1.0"
                or row.get("gold_status") != "SOURCE_ANNOTATED" or row.get("split") != "test"):
            raise ValueError(f"unexpected evidence provenance for {row['id']!r}")
        tokens = json.loads(row["gold_tokens_json"])
        if not isinstance(tokens, list) or any(not isinstance(t, str) or not t for t in tokens):
            raise ValueError(f"invalid gold token array for {row['id']!r}")
        if "".join(tokens) != row["text"]:
            raise ValueError(f"gold tokens do not reconstruct source text for {row['id']!r}")

    from thai_ukrainian.segmentation import segment_text_preserving

    dictionary = score_engine(rows, lambda text: list(segment_text_preserving(text)), args.examples_per_error)
    tud = score_engine(rows, lambda text: segment_tud_preserving(text, counts, float(penalty)), args.examples_per_error)
    report = {
        "report_type": "COMPARATIVE_SEGMENTATION_ERROR_TRIAGE_NOT_GOLD_ADJUDICATION",
        "dataset": {
            "name": "PyThaiNLP Wisesight word-tokenization labels",
            "rows_total": len(rows),
            "rows_source_annotated": len(rows),
            "rows_expert_adjudicated": 0,
            "source_id": SOURCE_ID,
            "license": "CC0-1.0",
            "upstream_commit": "c1d063649abc3a6870b5fd1aae26cd1c64bdde7b",
            "split": "test",
            "same_rows_for_both_engines": True,
        },
        "models": {
            "dictionary_max_match": {
                "model_id": "clippyfirst-dictionary-max-match-v1",
                "evidence_grade": "DICTIONARY_BASELINE_NOT_GOLD",
                **dictionary,
            },
            "tud_unigram_viterbi": {
                "model_id": model["model_id"],
                "source_commit": model.get("source_commit"),
                "source_license": model["source_license"],
                "token_penalty": penalty,
                "training_vocabulary_size": len(counts),
                "evidence_grade": "RESEARCH_MODEL_NOT_GOLD",
                **tud,
            },
        },
        "method": {
            "offset_unit": "Unicode code points in original source text",
            "boundary_policy": "exclude boundaries touching whitespace-only tokens",
            "mixed_text_policy": "non-Thai runs are copied unchanged; both engines preserve the full original text",
            "example_order": "descending error count, then stable row ID",
            "caveats": [
                "All 993 labels are SOURCE_ANNOTATED, not independently expert-adjudicated.",
                "Both engines are scored on the same rows and the same lexical-boundary policy; their metrics are not proof of linguistic correctness.",
                "TUD model is trained on CC BY-SA 4.0 source data; preserve attribution/share-alike for derived artifacts.",
                "A disagreement with source tokenization is a review candidate, not automatically a model error.",
                "This report does not establish pronunciation, IPA, Ukrainian target quality, or production readiness.",
            ],
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({name: value["metrics"] for name, value in report["models"].items()}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
