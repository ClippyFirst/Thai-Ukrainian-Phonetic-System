#!/usr/bin/env python3
"""Evidence-gated IPA benchmark; only independently double-reviewed gold is scored."""
from __future__ import annotations

import argparse
import csv
import json
import unicodedata
from collections import defaultdict
from pathlib import Path

GOLD_FIELDS = [
    "id", "text", "gold_ipa", "gold_status", "profile", "source_id", "source_url",
    "license", "transcription_level", "reviewer_a_id", "reviewer_b_id",
    "reviewer_a_ipa", "reviewer_b_ipa", "adjudicator_id", "adjudication_outcome",
    "adjudication_record_id", "adjudication_notes",
]
PRED_FIELDS = ["id", "engine", "raw_output", "ipa", "status", "version"]
TRANSCRIPTION_LEVELS = {"BROAD_PHONEMIC", "BROAD_SURFACE"}
ADJUDICATION_OUTCOMES = {"AGREEMENT", "RESOLVED_DISAGREEMENT"}


def read_tsv(path: Path, required: list[str]) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        missing = set(required) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path}: missing columns: {', '.join(sorted(missing))}")
        return [{key: (value or "") for key, value in row.items()} for row in reader]


def norm(value: str) -> str:
    return unicodedata.normalize("NFC", value.strip())


def distance(a: str, b: str) -> int:
    """Levenshtein distance over Unicode code points, not IPA feature classes."""
    previous = list(range(len(b) + 1))
    for i, char_a in enumerate(a, 1):
        current = [i]
        for j, char_b in enumerate(b, 1):
            current.append(min(
                current[-1] + 1,
                previous[j] + 1,
                previous[j - 1] + (char_a != char_b),
            ))
        previous = current
    return previous[-1]


def validate_gold_row(row: dict[str, str]) -> None:
    ident = row["id"]
    if not norm(row["gold_ipa"]):
        raise ValueError(f"ADJUDICATED gold row {ident!r} requires non-empty gold_ipa")
    required = (
        "source_id", "source_url", "license", "profile", "transcription_level",
        "reviewer_a_id", "reviewer_b_id", "reviewer_a_ipa", "reviewer_b_ipa",
        "adjudicator_id", "adjudication_outcome", "adjudication_record_id",
        "adjudication_notes",
    )
    missing = [field for field in required if not row[field].strip()]
    if missing:
        raise ValueError(
            f"ADJUDICATED gold row {ident!r} requires provenance: {', '.join(missing)}"
        )
    if row["reviewer_a_id"].strip() == row["reviewer_b_id"].strip():
        raise ValueError(f"ADJUDICATED gold row {ident!r} requires two distinct reviewers")
    if row["transcription_level"] not in TRANSCRIPTION_LEVELS:
        raise ValueError(f"ADJUDICATED gold row {ident!r} has unsupported transcription_level")
    outcome = row["adjudication_outcome"]
    if outcome not in ADJUDICATION_OUTCOMES:
        raise ValueError(f"ADJUDICATED gold row {ident!r} has invalid adjudication_outcome")
    labels_agree = norm(row["reviewer_a_ipa"]) == norm(row["reviewer_b_ipa"])
    if outcome == "AGREEMENT" and not labels_agree:
        raise ValueError(f"ADJUDICATED gold row {ident!r}: AGREEMENT requires matching reviewer IPA")
    if outcome == "RESOLVED_DISAGREEMENT" and labels_agree:
        raise ValueError(
            f"ADJUDICATED gold row {ident!r}: RESOLVED_DISAGREEMENT requires differing reviewer IPA"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("benchmark-report.json"))
    args = parser.parse_args()
    gold_rows = read_tsv(args.gold, GOLD_FIELDS)
    prediction_rows = read_tsv(args.predictions, PRED_FIELDS)
    gold: dict[str, dict[str, str]] = {}
    for row in gold_rows:
        if not row["id"] or row["id"] in gold:
            raise ValueError(f"gold IDs must be non-empty and unique: {row['id']!r}")
        gold[row["id"]] = row
    for row in gold_rows:
        if row["gold_status"] == "ADJUDICATED":
            validate_gold_row(row)
    eligible = {
        ident: row for ident, row in gold.items()
        if row["gold_status"] == "ADJUDICATED" and norm(row["gold_ipa"])
    }
    predictions: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    unknown_ids = []
    for row in prediction_rows:
        if not row["engine"] or not row["id"]:
            raise ValueError("prediction engine and id must be non-empty")
        engine = row["engine"]
        if row["id"] in predictions[engine]:
            raise ValueError(f"prediction (engine,id) must be unique: {(engine, row['id'])!r}")
        predictions[engine][row["id"]] = row
        if row["id"] not in gold:
            unknown_ids.append({"engine": engine, "id": row["id"]})
    report = {
        "schema_version": "1.1",
        "method": {
            "gold_gate": (
                "ADJUDICATED, non-empty IPA, two distinct reviewer IDs and raw labels, "
                "adjudicator, outcome, transcription level, source/license and adjudication record"
            ),
            "normalization": "Unicode NFC plus outer whitespace trim only",
            "exact_match": "strict full-string IPA match; tone, length and syllable separators remain significant",
            "cer": "Levenshtein over Unicode code points; not articulatory/feature-weighted",
            "missing_predictions": "every eligible gold row is in each engine's denominator; absent/empty IPA counts as missing",
            "accuracy_claim": "descriptive only for supplied independently reviewed rows; no generalization claim",
        },
        "gold": {
            "rows_total": len(gold),
            "rows_adjudicated": len(eligible),
            "accuracy_status": "MEASURED_ON_ADJUDICATED_SUBSET" if eligible else "NOT_MEASURED",
        },
        "unknown_prediction_ids": unknown_ids,
        "engines": {},
    }
    for engine in sorted(predictions):
        rows = []
        for ident, reference in eligible.items():
            prediction = predictions[engine].get(ident)
            ref = norm(reference["gold_ipa"])
            predicted = norm(prediction["ipa"]) if prediction else ""
            rows.append({
                "id": ident,
                "profile": reference["profile"],
                "transcription_level": reference["transcription_level"],
                "exact_match": bool(predicted) and predicted == ref,
                "missing_prediction": not bool(predicted),
                "prediction_row_present": prediction is not None,
                "edit_distance": distance(ref, predicted) if predicted else len(ref),
                "reference_codepoints": len(ref),
                "raw_output_present": bool(prediction and prediction["raw_output"]),
                "status": prediction["status"] if prediction else "MISSING_ROW",
                "version": prediction["version"] if prediction else "",
            })
        count = len(rows)
        edits = sum(row["edit_distance"] for row in rows)
        codepoints = sum(row["reference_codepoints"] for row in rows)
        report["engines"][engine] = {
            "n_adjudicated_gold_rows": count,
            "exact_matches": sum(row["exact_match"] for row in rows),
            "exact_match_rate": sum(row["exact_match"] for row in rows) / count if count else None,
            "missing_predictions": sum(row["missing_prediction"] for row in rows),
            "missing_prediction_rate": sum(row["missing_prediction"] for row in rows) / count if count else None,
            "codepoint_cer": edits / codepoints if codepoints else None,
            "profiles": sorted({row["profile"] for row in rows if row["profile"]}),
            "transcription_levels": sorted({row["transcription_level"] for row in rows}),
            "versions": sorted({row["version"] for row in predictions[engine].values() if row["version"]}),
            "rows": rows,
            "status": "SCORED" if count else "NOT_MEASURED_NO_ADJUDICATED_GOLD",
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "gold_adjudicated": len(eligible),
        "engines": {
            key: {
                "n": value["n_adjudicated_gold_rows"],
                "status": value["status"],
                "missing": value["missing_predictions"],
            }
            for key, value in report["engines"].items()
        },
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
