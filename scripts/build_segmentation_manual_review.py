#!/usr/bin/env python3
"""Build a deterministic, stratified human-review sample from pinned source rows.

This is a sampling aid, not an adjudicator. It deliberately includes both
high-disagreement cases and randomly selected controls; source annotations
remain source annotations until human reviewers independently decide otherwise.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "data/benchmark/segmentation-gold.tsv"
SOURCE_ID = "WISESIGHT1000-C1D063649ABC"
REQUIRED_MODELS = {"dictionary_max_match", "tud_unigram_viterbi"}


def strata(text: str, dictionary: list[str], tud: list[str]) -> list[str]:
    tags: list[str] = []
    if re.search(r"\\d", text):
        tags.append("NUMERIC_OR_DATE_CANDIDATE")
    if re.search(r"https?://|www\\.|[\\w.+-]+@[\\w.-]+\\.[A-Za-z]{2,}", text, re.I):
        tags.append("URL_OR_EMAIL_CANDIDATE")
    if re.search(r"[A-Za-z]", text) and re.search(r"[\\u0E00-\\u0E7F]", text):
        tags.append("MIXED_LATIN_THAI_CANDIDATE")
    elif re.search(r"[A-Za-z]", text):
        tags.append("LATIN_OR_BRAND_CANDIDATE")
    if re.search(r"[!?,.:;()\\[\\]{}‘’“”\\\"'…]", text):
        tags.append("PUNCTUATION_OR_QUOTING_CANDIDATE")
    if len(re.findall(r"[\\u0E00-\\u0E7F]", text)) >= 80:
        tags.append("LONG_THAI_SEQUENCE_CANDIDATE")
    if dictionary != tud:
        tags.append("ENGINE_DISAGREEMENT")
    if not tags:
        tags.append("GENERAL_REVIEW")
    return tags


def _rank(seed: str, row_id: str, stratum: str) -> str:
    return hashlib.sha256(f"{seed}:{row_id}:{stratum}".encode("utf-8")).hexdigest()


def build(
    report: dict,
    gold_path: Path,
    tud_model: dict,
    *,
    sample_per_stratum: int = 8,
    control_sample: int = 12,
    seed: str = "thai-segmentation-review-v1",
    dictionary_segmenter: Callable[[str], list[str]] | None = None,
    tud_segmenter: Callable[[str], list[str]] | None = None,
) -> list[dict]:
    if report.get("report_type") != "COMPARATIVE_SEGMENTATION_ERROR_TRIAGE_NOT_GOLD_ADJUDICATION":
        raise ValueError("unexpected report type")
    ds = report.get("dataset", {})
    expected_rows = ds.get("rows_total")
    if (not isinstance(expected_rows, int) or expected_rows < 1
            or ds.get("rows_expert_adjudicated") != 0
            or ds.get("rows_source_annotated") != expected_rows
            or ds.get("license") != "CC0-1.0" or ds.get("split") != "test"
            or ds.get("source_id") != SOURCE_ID):
        raise ValueError("expected a pinned, source-annotated, CC0 test dataset with no adjudicated rows")
    if not REQUIRED_MODELS.issubset(set(report.get("models", {}))):
        raise ValueError("comparative report must contain both required models")
    if (tud_model.get("model_id") != "clippyfirst-tud-unigram-viterbi-v1"
            or tud_model.get("source_license") != "CC-BY-SA-4.0"):
        raise ValueError("unexpected TUD model identity or license")
    counts, penalty = tud_model.get("word_counts"), tud_model.get("token_penalty")
    if not isinstance(counts, dict) or not counts or not isinstance(penalty, (int, float)):
        raise ValueError("invalid TUD model counts or token penalty")
    if sample_per_stratum < 1 or control_sample < 0:
        raise ValueError("sample_per_stratum must be positive and control_sample non-negative")

    if dictionary_segmenter is None:
        from thai_ukrainian.segmentation import segment_text_preserving
        dictionary_segmenter = lambda text: list(segment_text_preserving(text))
    if tud_segmenter is None:
        from compare_segmentation_error_review import segment_tud_preserving
        tud_segmenter = lambda text: list(segment_tud_preserving(text, counts, float(penalty)))

    with gold_path.open(encoding="utf-8-sig", newline="") as f:
        source_rows = list(csv.DictReader(f, delimiter="\\t"))
    if len(source_rows) != expected_rows:
        raise ValueError(f"source row count mismatch: expected {expected_rows}, got {len(source_rows)}")

    candidates: list[dict] = []
    seen: set[str] = set()
    for original in source_rows:
        row_id, text = original.get("id", ""), original.get("text", "")
        if not row_id or row_id in seen:
            raise ValueError(f"source IDs must be non-empty and unique: {row_id!r}")
        seen.add(row_id)
        if (original.get("source_id") != SOURCE_ID or original.get("license") != "CC0-1.0"
                or original.get("gold_status") != "SOURCE_ANNOTATED"
                or original.get("split") != "test"):
            raise ValueError(f"unexpected source provenance for {row_id!r}")
        gold = json.loads(original["gold_tokens_json"])
        dictionary = list(dictionary_segmenter(text))
        tud = list(tud_segmenter(text))
        for label, tokens in (("source annotation", gold), ("dictionary", dictionary), ("TUD", tud)):
            if not isinstance(tokens, list) or any(not isinstance(token, str) or not token for token in tokens):
                raise ValueError(f"invalid {label} tokens for {row_id}")
            if "".join(tokens) != text:
                raise ValueError(f"lossless reconstruction failed for {label}: {row_id}")
        tags = strata(text, dictionary, tud)
        candidates.append({
            "id": row_id, "text": text,
            "gold_tokens_json": json.dumps(gold, ensure_ascii=False),
            "dictionary_tokens_json": json.dumps(dictionary, ensure_ascii=False),
            "tud_tokens_json": json.dumps(tud, ensure_ascii=False),
            "sampling_strata": ";".join(tags),
            "gold_status": "SOURCE_ANNOTATED",
            "human_decision": "", "reviewer_id": "", "decision_rationale": "",
            "adjudicated": "NO",
        })

    # Choose a deterministic sample within every heuristic stratum, then add
    # a uniform control sample drawn from all rows. A row can satisfy many strata.
    selected: dict[str, set[str]] = {}
    by_id = {row["id"]: row for row in candidates}
    all_tags = sorted({tag for row in candidates for tag in row["sampling_strata"].split(";")})
    for tag in all_tags:
        members = [row for row in candidates if tag in row["sampling_strata"].split(";")]
        chosen = sorted(members, key=lambda row: _rank(seed, row["id"], tag))[:sample_per_stratum]
        for row in chosen:
            selected.setdefault(row["id"], set()).add(tag)
    controls = sorted(candidates, key=lambda row: _rank(seed, row["id"], "UNIFORM_CONTROL"))[:control_sample]
    for row in controls:
        selected.setdefault(row["id"], set()).add("UNIFORM_CONTROL")

    output: list[dict] = []
    for row_id in sorted(selected):
        row = dict(by_id[row_id])
        row["sampled_for"] = ";".join(sorted(selected[row_id]))
        output.append(row)
    if not output:
        raise ValueError("sample generation produced no rows")
    if any(row["gold_status"] != "SOURCE_ANNOTATED" or row["adjudicated"] != "NO"
           or row["human_decision"] or row["reviewer_id"] or row["decision_rationale"] for row in output):
        raise AssertionError("human adjudication fields must remain blank")
    return output


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--tud-model", type=Path, required=True)
    p.add_argument("--gold", type=Path, default=GOLD)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--sample-per-stratum", type=int, default=8)
    p.add_argument("--control-sample", type=int, default=12)
    p.add_argument("--seed", default="thai-segmentation-review-v1")
    a = p.parse_args()
    rows = build(json.loads(a.report.read_text(encoding="utf-8")),
                 a.gold, json.loads(a.tud_model.read_text(encoding="utf-8")),
                 sample_per_stratum=a.sample_per_stratum,
                 control_sample=a.control_sample, seed=a.seed)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    with a.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\\t", lineterminator="\\n")
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"output": str(a.output), "review_rows": len(rows),
                      "adjudicated": 0, "sampling": "DETERMINISTIC_STRATIFIED_PLUS_UNIFORM_CONTROLS",
                      "status": "SAMPLING_CANDIDATES_NOT_ADJUDICATED"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
