#!/usr/bin/env python3
"""Evidence-gated word-segmentation benchmark; standard library only.

Gold TSV: id, text, gold_tokens_json, gold_status, source_id, license, split
Prediction TSV: id, engine, predicted_tokens_json, status, version

Only ADJUDICATED gold rows enter denominators. Token arrays must concatenate
exactly to the NFC-normalized source text; whitespace is never silently dropped.
"""
from __future__ import annotations

import argparse
import csv
import json
import unicodedata
from collections import defaultdict
from pathlib import Path

GOLD_FIELDS = ["id", "text", "gold_tokens_json", "gold_status", "source_id", "license", "split"]
PRED_FIELDS = ["id", "engine", "predicted_tokens_json", "status", "version"]


def read_tsv(path: Path, required: list[str]) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        missing = set(required) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path}: missing columns: {', '.join(sorted(missing))}")
        rows = list(reader)
    return [{key: (value or "") for key, value in row.items()} for row in rows]


def normalize(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def parse_tokens(raw: str, *, row_id: str, field: str) -> list[str]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{field} for row {row_id!r} must be a JSON array") from exc
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f"{field} for row {row_id!r} must be a non-empty-string JSON array")
    return value


def boundaries(text: str, tokens: list[str], *, row_id: str, field: str) -> set[int]:
    text = normalize(text)
    joined = normalize("".join(tokens))
    if joined != text:
        raise ValueError(
            f"{field} for row {row_id!r} does not concatenate to NFC text; "
            "do not silently normalize, drop whitespace, or rewrite source text"
        )
    offsets: set[int] = set()
    cursor = 0
    for token in tokens[:-1]:
        cursor += len(normalize(token))
        offsets.add(cursor)
    return offsets


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("segmentation-benchmark.json"))
    args = parser.parse_args()

    gold_rows = read_tsv(args.gold, GOLD_FIELDS)
    prediction_rows = read_tsv(args.predictions, PRED_FIELDS)
    gold: dict[str, dict[str, object]] = {}
    for row in gold_rows:
        row_id = row["id"]
        if not row_id or row_id in gold:
            raise ValueError(f"gold IDs must be non-empty and unique: {row_id!r}")
        if row["gold_status"] == "ADJUDICATED":
            for field in ("source_id", "license", "split"):
                if not row[field].strip():
                    raise ValueError(f"ADJUDICATED gold row {row_id!r} requires {field}")
            tokens = parse_tokens(row["gold_tokens_json"], row_id=row_id, field="gold_tokens_json")
            gold[row_id] = {
                "text": normalize(row["text"]),
                "tokens": tokens,
                "boundaries": boundaries(row["text"], tokens, row_id=row_id, field="gold_tokens_json"),
                "source_id": row["source_id"].strip(),
                "license": row["license"].strip(),
                "split": row["split"].strip(),
            }

    predictions: dict[str, dict[str, dict[str, object]]] = defaultdict(dict)
    for row in prediction_rows:
        if not row["id"].strip() or not row["engine"].strip():
            raise ValueError("prediction id and engine must be non-empty")
        engine, row_id = row["engine"].strip(), row["id"].strip()
        if row_id in predictions[engine]:
            raise ValueError(f"prediction (engine,id) must be unique: {(engine, row_id)!r}")
        if row_id not in {r["id"] for r in gold_rows}:
            raise ValueError(f"prediction references unknown gold id: {row_id!r}")
        tokens: list[str] = []
        predicted_boundaries: set[int] = set()
        if row["predicted_tokens_json"].strip():
            tokens = parse_tokens(row["predicted_tokens_json"], row_id=row_id, field="predicted_tokens_json")
            predicted_boundaries = boundaries(
                next(r["text"] for r in gold_rows if r["id"] == row_id),
                tokens, row_id=row_id, field="predicted_tokens_json",
            )
        predictions[engine][row_id] = {
            "tokens": tokens,
            "boundaries": predicted_boundaries,
            "status": row["status"],
            "version": row["version"],
        }

    engine_names = sorted(predictions)
    eligible_ids = set(gold)
    report: dict[str, object] = {
        "schema_version": "1.0",
        "method": {
            "gold_gate": "gold_status == ADJUDICATED with source_id, license, split and valid tokenization",
            "normalization": "Unicode NFC only; token concatenation must equal normalized source text exactly",
            "boundary_units": "Python Unicode code-point offsets, excluding the final text boundary",
            "missing_predictions": "eligible gold rows remain in denominator; missing/empty tokenization contributes no predicted boundaries",
            "exact_sequence": "all token strings and boundaries must match the adjudicated sequence",
            "accuracy_claim": "descriptive only for the supplied adjudicated rows",
        },
        "gold": {
            "rows_total": len(gold_rows),
            "rows_adjudicated": len(gold),
            "status": "MEASURED_ON_ADJUDICATED_ROWS" if gold else "NOT_MEASURED",
        },
        "engines": {},
    }
    engines: dict[str, object] = {}
    for engine in engine_names:
        by_id = predictions[engine]
        tp = fp = fn = exact = covered = 0
        for row_id, reference in gold.items():
            prediction = by_id.get(row_id)
            if prediction and prediction["tokens"]:
                covered += 1
                predicted_set = prediction["boundaries"]
                gold_set = reference["boundaries"]
                tp += len(predicted_set & gold_set)
                fp += len(predicted_set - gold_set)
                fn += len(gold_set - predicted_set)
                exact += int(prediction["tokens"] == reference["tokens"])
            else:
                fn += len(reference["boundaries"])
        precision = tp / (tp + fp) if tp + fp else (1.0 if tp + fn == 0 and gold else 0.0)
        recall = tp / (tp + fn) if tp + fn else (1.0 if gold else None)
        f1 = (2 * precision * recall / (precision + recall)) if precision + recall else 0.0
        engines[engine] = {
            "status": "MEASURED" if gold else "NOT_MEASURED_NO_ADJUDICATED_GOLD",
            "n_adjudicated_gold_rows": len(gold),
            "nonempty_predictions": covered,
            "coverage": covered / len(gold) if gold else None,
            "exact_sequence_matches": exact,
            "exact_sequence_rate": exact / len(gold) if gold else None,
            "boundary_tp": tp, "boundary_fp": fp, "boundary_fn": fn,
            "boundary_precision": precision if gold else None,
            "boundary_recall": recall,
            "boundary_f1": f1 if gold else None,
        }
    report["engines"] = engines
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
