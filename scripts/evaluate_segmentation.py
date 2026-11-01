#!/usr/bin/env python3
"""Evidence-gated word-segmentation benchmark; standard library only.

Gold TSV: id, text, gold_tokens_json, gold_status, source_id, license, split
Prediction TSV: id, engine, predicted_tokens_json, status, version

Only ADJUDICATED or SOURCE_ANNOTATED rows enter denominators; evidence grades
cannot be mixed in one report. Token arrays must concatenate exactly to the
NFC-normalized source text; whitespace is never silently dropped.
"""
from __future__ import annotations

import argparse
import csv
import json
import unicodedata
from collections import defaultdict
from pathlib import Path

from thai_ukrainian.evidence_registry import (
    load_reviewer_registry, load_source_registry,
    validate_reviewer_reference, validate_source_reference,
)

GOLD_FIELDS = ["id", "text", "gold_tokens_json", "gold_status", "source_id", "license", "split"]
PRED_FIELDS = ["id", "engine", "predicted_tokens_json", "status", "version"]
# Only a fully emitted prediction is scoreable. Error/abstention/partial rows
# remain in the input audit trail but cannot receive credit for stale tokens.
SCOREABLE_PREDICTION_STATUSES = {"ok"}
SCOREABLE_GOLD_STATUSES = {"ADJUDICATED", "SOURCE_ANNOTATED"}
ADJUDICATION_FIELDS = (
    "source_url", "segmentation_layer", "reviewer_a_id", "reviewer_b_id",
    "reviewer_a_qualification_ref", "reviewer_b_qualification_ref",
    "reviewer_a_tokens_json", "reviewer_b_tokens_json", "adjudicator_id",
    "adjudicator_qualification_ref", "adjudication_outcome", "adjudication_record_id",
    "adjudication_notes",
)


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
        raise ValueError(f"{field} for row {row_id!r} must be a JSON array of non-empty strings")
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
    for index, token in enumerate(tokens[:-1]):
        cursor += len(normalize(token))
        next_token = tokens[index + 1]
        # Explicit whitespace tokens reconstruct source text but are not lexical
        # word boundaries and must not affect segmentation precision/recall.
        if not normalize(token).isspace() and not normalize(next_token).isspace():
            offsets.add(cursor)
    return offsets


def validate_adjudicated_row(
    row: dict[str, str],
    source_registry: dict[str, dict[str, str]] | None = None,
    reviewer_registry: dict[str, dict[str, str]] | None = None,
) -> tuple[list[str], list[str]]:
    row_id = row["id"]
    missing = [field for field in ADJUDICATION_FIELDS if not row.get(field, "").strip()]
    if missing:
        raise ValueError(
            f"ADJUDICATED gold row {row_id!r} requires independent-review provenance: {', '.join(missing)}"
        )
    if row["segmentation_layer"] not in {"WORD", "SYLLABLE"}:
        raise ValueError(f"ADJUDICATED gold row {row_id!r} requires segmentation_layer WORD or SYLLABLE")
    if row["reviewer_a_id"].strip() == row["reviewer_b_id"].strip():
        raise ValueError(f"ADJUDICATED gold row {row_id!r} requires two distinct reviewers")
    if row["adjudicator_id"].strip() in {row["reviewer_a_id"].strip(), row["reviewer_b_id"].strip()}:
        raise ValueError(f"ADJUDICATED gold row {row_id!r} requires a distinct adjudicator")
    if source_registry is not None:
        validate_source_reference(row["source_id"], row["source_url"], row["license"],
                                  "WORD_SEGMENTATION_GOLD_INPUT", source_registry, row_id=row_id)
    if reviewer_registry is not None:
        for field in ("reviewer_a", "reviewer_b"):
            validate_reviewer_reference(row[f"{field}_id"], row[f"{field}_qualification_ref"], reviewer_registry,
                                        language="th", required_role="THAI_LINGUIST", row_id=row_id)
        validate_reviewer_reference(row["adjudicator_id"], row["adjudicator_qualification_ref"], reviewer_registry,
                                    language="th", required_role="THAI_LINGUIST_ADJUDICATOR", row_id=row_id)
    reviewer_a = parse_tokens(
        row["reviewer_a_tokens_json"], row_id=row_id, field="reviewer_a_tokens_json"
    )
    reviewer_b = parse_tokens(
        row["reviewer_b_tokens_json"], row_id=row_id, field="reviewer_b_tokens_json"
    )
    boundaries(row["text"], reviewer_a, row_id=row_id, field="reviewer_a_tokens_json")
    boundaries(row["text"], reviewer_b, row_id=row_id, field="reviewer_b_tokens_json")
    outcome = row["adjudication_outcome"]
    labels_agree = reviewer_a == reviewer_b
    if outcome == "AGREEMENT":
        if not labels_agree:
            raise ValueError(
                f"ADJUDICATED gold row {row_id!r}: AGREEMENT requires matching reviewer tokenizations"
            )
        if parse_tokens(row["gold_tokens_json"], row_id=row_id, field="gold_tokens_json") != reviewer_a:
            raise ValueError(
                f"ADJUDICATED gold row {row_id!r}: gold tokens must equal the agreed reviewer tokenization"
            )
    elif outcome == "RESOLVED_DISAGREEMENT":
        if labels_agree:
            raise ValueError(
                f"ADJUDICATED gold row {row_id!r}: RESOLVED_DISAGREEMENT requires differing reviewer tokenizations"
            )
    else:
        raise ValueError(f"ADJUDICATED gold row {row_id!r} has invalid adjudication_outcome")
    return reviewer_a, reviewer_b


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("segmentation-benchmark.json"))
    parser.add_argument("--source-registry", type=Path, default=Path("data/benchmark/source-registry.tsv"))
    parser.add_argument("--reviewer-registry", type=Path, default=Path("data/benchmark/reviewer-qualifications.tsv"))
    args = parser.parse_args()

    source_registry = load_source_registry(args.source_registry)
    reviewer_registry = load_reviewer_registry(args.reviewer_registry)
    gold_rows = read_tsv(args.gold, GOLD_FIELDS)
    prediction_rows = read_tsv(args.predictions, PRED_FIELDS)
    gold: dict[str, dict[str, object]] = {}
    seen_gold_ids: set[str] = set()
    for row in gold_rows:
        row_id = row["id"]
        if not row_id or row_id in seen_gold_ids:
            raise ValueError(f"gold IDs must be non-empty and unique: {row_id!r}")
        seen_gold_ids.add(row_id)
        if row["gold_status"] in SCOREABLE_GOLD_STATUSES:
            if not normalize(row["text"]):
                raise ValueError(f"ADJUDICATED gold row {row_id!r} requires non-empty text")
            for field in ("source_id", "license", "split"):
                if not row[field].strip():
                    raise ValueError(f"ADJUDICATED gold row {row_id!r} requires {field}")
            tokens = parse_tokens(row["gold_tokens_json"], row_id=row_id, field="gold_tokens_json")
            if row["gold_status"] == "ADJUDICATED":
                reviewer_a_tokens, reviewer_b_tokens = validate_adjudicated_row(
                    row, source_registry, reviewer_registry
                )
            else:
                validate_source_reference(
                    row["source_id"], row.get("source_url", ""), row["license"],
                    "WORD_SEGMENTATION_DIAGNOSTIC", source_registry,
                    row_id=row_id, require_url=False,
                )
                reviewer_a_tokens, reviewer_b_tokens = [], []
            gold[row_id] = {
                "text": normalize(row["text"]),
                "tokens": tokens,
                "boundaries": boundaries(row["text"], tokens, row_id=row_id, field="gold_tokens_json"),
                "source_id": row["source_id"].strip(),
                "license": row["license"].strip(),
                "split": row["split"].strip(),
                "gold_status": row["gold_status"].strip(),
                "source_url": row.get("source_url", "").strip() or source_registry[row["source_id"].strip()]["source_url"],
                "segmentation_layer": row.get("segmentation_layer", "").strip() or (
                    "WORD" if row["gold_status"] == "SOURCE_ANNOTATED" else ""
                ),
                "reviewer_a_id": row.get("reviewer_a_id", "").strip(),
                "reviewer_b_id": row.get("reviewer_b_id", "").strip(),
                "reviewer_a_tokens": reviewer_a_tokens,
                "reviewer_b_tokens": reviewer_b_tokens,
                "adjudicator_id": row.get("adjudicator_id", "").strip(),
                "adjudication_record_id": row.get("adjudication_record_id", "").strip(),
            }

    gold_statuses = {str(row["gold_status"]) for row in gold.values()}
    segmentation_layers = {str(row["segmentation_layer"]) for row in gold.values()}
    if len(segmentation_layers) > 1:
        raise ValueError("do not mix WORD and SYLLABLE segmentation rows in one report")
    if len(gold_statuses) > 1:
        raise ValueError(
            "do not mix ADJUDICATED and SOURCE_ANNOTATED rows in one report; "
            "run separate reports so evidence grades remain visible"
        )
    scored_gold_status = next(iter(gold_statuses), None)

    # Index once: VISTEC has ~50k rows and two predictions per row. Re-scanning
    # the entire gold list for every prediction made the evaluator quadratic.
    gold_rows_by_id = {row["id"]: row for row in gold_rows}
    gold_ids = set(gold_rows_by_id)
    predictions: dict[str, dict[str, dict[str, object]]] = defaultdict(dict)
    for row in prediction_rows:
        if not row["id"].strip() or not row["engine"].strip():
            raise ValueError("prediction id and engine must be non-empty")
        if not row["status"].strip() or not row["version"].strip():
            raise ValueError("prediction status and version must be non-empty")
        engine, row_id = row["engine"].strip(), row["id"].strip()
        if row_id in predictions[engine]:
            raise ValueError(f"prediction (engine,id) must be unique: {(engine, row_id)!r}")
        if row_id not in gold_ids:
            raise ValueError(f"prediction references unknown gold id: {row_id!r}")
        tokens: list[str] = []
        predicted_boundaries: set[int] = set()
        if row["predicted_tokens_json"].strip():
            tokens = parse_tokens(row["predicted_tokens_json"], row_id=row_id, field="predicted_tokens_json")
            if tokens and row["status"].strip().lower() in SCOREABLE_PREDICTION_STATUSES:
                predicted_boundaries = boundaries(
                    gold_rows_by_id[row_id]["text"],
                    tokens, row_id=row_id, field="predicted_tokens_json",
                )
        predictions[engine][row_id] = {
            "tokens": tokens,
            "boundaries": predicted_boundaries,
            "status": row["status"].strip().lower(),
            "version": row["version"],
        }

    engine_names = sorted(predictions)
    report: dict[str, object] = {
        "schema_version": "1.0",
        "method": {
            "gold_gate": "ADJUDICATED requires two distinct reviewers, raw tokenizations, adjudicator/outcome/record and source provenance; SOURCE_ANNOTATED retains its source-only evidence grade; evidence grades are never mixed",
            "gold_status": scored_gold_status or "NONE",
            "segmentation_layer": next(iter(segmentation_layers), None),
            "normalization": "Unicode NFC only; token concatenation must equal normalized source text exactly",
            "boundary_units": "Python Unicode code-point offsets, excluding the final text boundary",
            "missing_predictions": "eligible gold rows remain in denominator; missing/empty tokenization contributes no predicted boundaries",
            "scoreable_prediction_statuses": sorted(SCOREABLE_PREDICTION_STATUSES),
            "non_success_statuses": "Any status other than 'ok' is treated as abstention even if a token array is present; stale/partial output cannot score.",
            "exact_sequence": "all token strings and boundaries must match the adjudicated sequence",
            "accuracy_claim": (
                "descriptive only for independently adjudicated rows"
                if scored_gold_status == "ADJUDICATED"
                else "descriptive only for the supplied source-annotated labels; not expert-adjudicated"
                if scored_gold_status == "SOURCE_ANNOTATED"
                else "not measured; no scoreable gold rows"
            ),
        },
        "evidence_registries": {
            "source_records": len(source_registry),
            "verified_reviewer_records": sum(row["verification_status"] == "VERIFIED" for row in reviewer_registry.values()),
        },
        "gold": {
            "rows_total": len(gold_rows),
            "rows_adjudicated": sum(1 for row in gold.values() if row["gold_status"] == "ADJUDICATED"),
            "rows_source_annotated": sum(1 for row in gold.values() if row["gold_status"] == "SOURCE_ANNOTATED"),
            "status": (
                "MEASURED_ON_ADJUDICATED_ROWS" if scored_gold_status == "ADJUDICATED"
                else "MEASURED_ON_SOURCE_ANNOTATED_ROWS_NOT_EXPERT_ADJUDICATED"
                if scored_gold_status == "SOURCE_ANNOTATED"
                else "NOT_MEASURED"
            ),
        },
        "engines": {},
    }
    engines: dict[str, object] = {}
    for engine in engine_names:
        by_id = predictions[engine]
        tp = fp = fn = exact = covered = 0
        for row_id, reference in gold.items():
            prediction = by_id.get(row_id)
            if prediction and prediction["tokens"] and prediction["status"] in SCOREABLE_PREDICTION_STATUSES:
                covered += 1
                predicted_set = prediction["boundaries"]
                gold_set = reference["boundaries"]
                tp += len(predicted_set & gold_set)
                fp += len(predicted_set - gold_set)
                fn += len(gold_set - predicted_set)
                exact += int(prediction["tokens"] == reference["tokens"])
            else:
                fn += len(reference["boundaries"])
        precision = tp / (tp + fp) if tp + fp else None
        recall = tp / (tp + fn) if tp + fn else None
        # F1 is defined as 0 when either side has boundaries but there are
        # no true positives; it is undefined only when both gold and predicted
        # boundary sets are empty (zero denominator).
        f1_denominator = 2 * tp + fp + fn
        f1 = (2 * tp / f1_denominator) if f1_denominator else None
        engines[engine] = {
            "status": (
                "MEASURED_ON_ADJUDICATED_ROWS" if scored_gold_status == "ADJUDICATED"
                else "MEASURED_ON_SOURCE_ANNOTATED_ROWS_NOT_EXPERT_ADJUDICATED"
                if scored_gold_status == "SOURCE_ANNOTATED"
                else "NOT_MEASURED_NO_SCOREABLE_GOLD"
            ),
            "gold_status": scored_gold_status or "NONE",
            "n_gold_rows": len(gold),
            "n_adjudicated_gold_rows": sum(1 for row in gold.values() if row["gold_status"] == "ADJUDICATED"),
            "n_source_annotated_gold_rows": sum(1 for row in gold.values() if row["gold_status"] == "SOURCE_ANNOTATED"),
            "nonempty_predictions": covered,
            "non_success_status_rows": sum(
                1 for row_id in by_id
                if by_id[row_id]["status"] not in SCOREABLE_PREDICTION_STATUSES
            ),
            "coverage": covered / len(gold) if gold else None,
            "exact_sequence_matches": exact,
            "exact_sequence_rate": exact / len(gold) if gold else None,
            "boundary_tp": tp, "boundary_fp": fp, "boundary_fn": fn,
            "boundary_precision": precision if gold else None,
            "boundary_recall": recall if gold else None,
            "boundary_f1": f1 if gold else None,
        }
    report["engines"] = engines
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
