from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .api import analyze_syllable

REQUIRED = {"id", "thai", "source"}


def _validate_record(record: Any, index: int) -> dict:
    if not isinstance(record, dict):
        raise ValueError(f"Record {index} must be a JSON object.")
    missing = REQUIRED - set(record)
    if missing:
        raise ValueError(f"Record {index} is missing required fields: {sorted(missing)}")
    if not isinstance(record["id"], str) or not record["id"].strip():
        raise ValueError(f"Record {index} has an invalid id.")
    if not isinstance(record["thai"], str) or not record["thai"].strip():
        raise ValueError(f"Record {index} has an invalid thai field.")
    if not isinstance(record["source"], str) or not record["source"].strip():
        raise ValueError(f"Record {index} has an invalid source field.")
    return record


def load_records(path: str | Path) -> list[dict]:
    path = Path(path)
    records = []
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_no}: {exc.msg}") from exc
            records.append(_validate_record(value, line_no))
    return records


def _safe_accuracy(correct: int, total: int) -> float | None:
    return None if total == 0 else correct / total


def evaluate_records(records: list[dict]) -> dict:
    checked = [_validate_record(r, i) for i, r in enumerate(records, 1)]
    ipa_total = ipa_correct = tone_total = tone_correct = 0
    analyses = []

    for record in checked:
        analysis = analyze_syllable(record["thai"])
        analyses.append(analysis)
        if record.get("ipa") is not None:
            ipa_total += 1
            ipa_correct += int(analysis.phonemic_ipa == record["ipa"])
        if record.get("tone") is not None:
            tone_total += 1
            tone_correct += int(analysis.tone is not None and analysis.tone.tone == record["tone"])

    return {
        "status": "evaluated",
        "records_total": len(checked),
        "records_evaluable": len(analyses),
        "ipa_exact_correct": ipa_correct,
        "ipa_exact_total": ipa_total,
        "ipa_exact_accuracy": _safe_accuracy(ipa_correct, ipa_total),
        "tone_correct": tone_correct,
        "tone_total": tone_total,
        "tone_accuracy": _safe_accuracy(tone_correct, tone_total),
        "note": "Metrics are exact-match metrics over supplied gold fields; missing gold fields are excluded from that metric.",
    }


def evaluate_file(path: str | Path) -> dict:
    return evaluate_records(load_records(path))
