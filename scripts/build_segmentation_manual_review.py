#!/usr/bin/env python3
"""Build a human-review TSV from comparative segmentation triage and pinned source rows.

Heuristic strata are sampling hints only; this script never adjudicates labels.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "data/benchmark/segmentation-gold.tsv"

def strata(text: str, dictionary: list[str], tud: list[str]) -> list[str]:
    tags = []
    if re.search(r"\d", text) or re.search(r"\b(?:19|20)\d{2}\b", text):
        tags.append("NUMERIC_OR_DATE_CANDIDATE")
    if re.search(r"https?://|www\.|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text, re.I):
        tags.append("URL_OR_EMAIL_CANDIDATE")
    if re.search(r"[A-Za-z]", text) and re.search(r"[\u0E00-\u0E7F]", text):
        tags.append("MIXED_LATIN_THAI_CANDIDATE")
    elif re.search(r"[A-Za-z]", text):
        tags.append("LATIN_OR_BRAND_CANDIDATE")
    if re.search(r"[!?,.:;()\[\]{}‘’“”\"'…]", text):
        tags.append("PUNCTUATION_OR_QUOTING_CANDIDATE")
    if len(re.findall(r"[\u0E00-\u0E7F]", text)) >= 80:
        tags.append("LONG_THAI_SEQUENCE_CANDIDATE")
    if dictionary != tud:
        tags.append("ENGINE_DISAGREEMENT")
    if not tags:
        tags.append("GENERAL_REVIEW")
    return tags

def build(report: dict, gold_path: Path) -> list[dict]:
    if report.get("report_type") != "COMPARATIVE_SEGMENTATION_ERROR_TRIAGE_NOT_GOLD_ADJUDICATION":
        raise ValueError("unexpected report type")
    ds = report.get("dataset", {})
    if ds.get("rows_expert_adjudicated") != 0 or ds.get("rows_source_annotated") != 993:
        raise ValueError("expected the pinned 993-row source-annotated dataset")
    candidates = {}
    for model_id, model in report["models"].items():
        for kind in ("false_split_examples", "false_merge_examples"):
            for example in model.get(kind, []):
                row = candidates.setdefault(example["id"], {"id": example["id"], "evidence": set(), "predictions": {}})
                row["evidence"].add(model_id + ":" + kind)
                row["predictions"][model_id] = example["predicted_tokens"]
    required = {"dictionary_max_match", "tud_unigram_viterbi"}
    candidates = {k:v for k,v in candidates.items() if required <= set(v["predictions"])}
    with gold_path.open(encoding="utf-8-sig", newline="") as f:
        source = {row["id"]: row for row in csv.DictReader(f, delimiter="\t")}
    rows = []
    for row_id, candidate in sorted(candidates.items()):
        if row_id not in source:
            raise ValueError(f"triage ID missing from pinned source: {row_id}")
        original = source[row_id]
        text = original["text"]
        gold_tokens = json.loads(original["gold_tokens_json"])
        dictionary = candidate["predictions"]["dictionary_max_match"]
        tud = candidate["predictions"]["tud_unigram_viterbi"]
        if "".join(gold_tokens) != text or "".join(dictionary) != text or "".join(tud) != text:
            raise ValueError(f"lossless reconstruction failed for {row_id}")
        rows.append({
            "id": row_id, "text": text, "gold_tokens_json": json.dumps(gold_tokens, ensure_ascii=False),
            "dictionary_tokens_json": json.dumps(dictionary, ensure_ascii=False),
            "tud_tokens_json": json.dumps(tud, ensure_ascii=False),
            "triage_sources": ";".join(sorted(candidate["evidence"])),
            "sampling_strata": ";".join(strata(text, dictionary, tud)),
            "gold_status": "SOURCE_ANNOTATED", "human_decision": "", "reviewer_id": "",
            "decision_rationale": "", "adjudicated": "NO",
        })
    if not rows:
        raise ValueError("no row has error examples from both systems; refusing empty review set")
    return rows

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--gold", type=Path, default=GOLD)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    rows = build(json.loads(a.report.read_text(encoding="utf-8")), a.gold)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    with a.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    print(json.dumps({"output": str(a.output), "review_rows": len(rows), "adjudicated": 0,
                      "status": "SAMPLING_CANDIDATES_NOT_ADJUDICATED"}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
