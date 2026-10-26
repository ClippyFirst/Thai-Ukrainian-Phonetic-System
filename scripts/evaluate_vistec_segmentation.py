#!/usr/bin/env python3
"""Evaluate the pinned VISTEC-TP-TH-2021 word-boundary annotations.

The upstream submissionText field contains pipe-delimited annotated tokens and
NER/misspelling markup. This adapter strips only the documented annotation tags,
keeps the resulting annotated text unchanged, and verifies exact reconstruction.
The dataset is source-annotated, not independently re-adjudicated gold.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "VISTEC-TP-TH-2021-215a7dc3d384f20eb56af1cbc41fb32b7f8df57c"
SOURCE_COMMIT = "215a7dc3d384f20eb56af1cbc41fb32b7f8df57c"
SOURCE_BLOB_SHA1 = "edfcb85907a604c5e30643065ac4975862a0fe90"
SOURCE_LICENSE = "CC-BY-SA-3.0"
EXPECTED_ROWS = 49997
TAG_RE = re.compile(r"</?(?:ne|msp)\b[^>]*>")


def parse_submission_text(value: str, *, row_id: str = "fixture") -> tuple[str, list[str]]:
    if not isinstance(value, str) or not value:
        raise ValueError(f"empty submissionText for {row_id}")
    tokens = [TAG_RE.sub("", part) for part in value.split("|")]
    tokens = [token for token in tokens if token != ""]
    text = "".join(tokens)
    if not text:
        raise ValueError(f"submissionText contains no text for {row_id}")
    if "|" in text or TAG_RE.search(text):
        raise ValueError(f"annotation markup was not fully removed for {row_id}")
    if "".join(tokens) != text:
        raise AssertionError(f"source reconstruction failed for {row_id}")
    return text, tokens


def git_blob_sha1(path: Path) -> str:
    """Compute Git's SHA-1 blob object ID without requiring a local Git checkout."""
    size = path.stat().st_size
    digest = hashlib.sha1()
    digest.update(f"blob {size}\\0".encode("ascii"))
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_benchmark_files(source_csv: Path, gold_path: Path, predictions_path: Path,
                          tud_model: dict, *, expected_rows: int = EXPECTED_ROWS,
                          expected_blob_sha1: str | None = SOURCE_BLOB_SHA1) -> int:
    if (tud_model.get("model_id") != "clippyfirst-tud-unigram-viterbi-v1"
            or tud_model.get("source_license") != "CC-BY-SA-4.0"):
        raise ValueError("unexpected TUD model identity or license")
    counts, penalty = tud_model.get("word_counts"), tud_model.get("token_penalty")
    if not isinstance(counts, dict) or not counts or not isinstance(penalty, (int, float)):
        raise ValueError("invalid TUD model counts or token penalty")

    if expected_blob_sha1 is not None and git_blob_sha1(source_csv) != expected_blob_sha1:
        raise ValueError("VISTEC CSV Git blob SHA-1 does not match the pinned source snapshot")

    from thai_ukrainian.segmentation import segment_text_preserving
    from compare_segmentation_error_review import segment_tud_preserving

    with source_csv.open("r", encoding="utf-8-sig", newline="") as src:
        reader = csv.DictReader(src)
        if "submissionText" not in (reader.fieldnames or []):
            raise ValueError("pinned VISTEC CSV must contain submissionText")
        with gold_path.open("w", encoding="utf-8", newline="") as gold_file, predictions_path.open(
            "w", encoding="utf-8", newline=""
        ) as pred_file:
            gold_writer = csv.DictWriter(gold_file, fieldnames=[
                "id", "text", "gold_tokens_json", "gold_status", "source_id", "license", "split"
            ], delimiter="\t", lineterminator="\n")
            pred_writer = csv.DictWriter(pred_file, fieldnames=[
                "id", "engine", "predicted_tokens_json", "status", "version"
            ], delimiter="\t", lineterminator="\n")
            gold_writer.writeheader()
            pred_writer.writeheader()
            count = 0
            for row_number, source_row in enumerate(reader, 1):
                row_id = f"VISTEC-TP-TH-2021-{row_number:05d}"
                text, gold_tokens = parse_submission_text(source_row.get("submissionText", ""), row_id=row_id)
                dictionary_tokens = list(segment_text_preserving(text))
                tud_tokens = list(segment_tud_preserving(text, counts, float(penalty)))
                for engine, tokens in (("dictionary_max_match", dictionary_tokens),
                                       ("tud_unigram_viterbi", tud_tokens)):
                    if not tokens or "".join(tokens) != text:
                        raise ValueError(f"{engine} failed exact reconstruction for {row_id}")
                gold_writer.writerow({
                    "id": row_id, "text": text,
                    "gold_tokens_json": json.dumps(gold_tokens, ensure_ascii=False),
                    "gold_status": "SOURCE_ANNOTATED", "source_id": SOURCE_ID,
                    "license": SOURCE_LICENSE, "split": "external_test",
                })
                for engine, tokens, version in (
                    ("dictionary_max_match", dictionary_tokens, "clippyfirst-dictionary-max-match-v1"),
                    ("tud_unigram_viterbi", tud_tokens, "clippyfirst-tud-unigram-viterbi-v1"),
                ):
                    pred_writer.writerow({
                        "id": row_id, "engine": engine,
                        "predicted_tokens_json": json.dumps(tokens, ensure_ascii=False),
                        "status": "ok", "version": version,
                    })
                count += 1
    if count != expected_rows:
        raise ValueError(f"pinned VISTEC row count mismatch: expected {expected_rows}, got {count}")
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, required=True, help="VISTEC CSV at the pinned source revision")
    parser.add_argument("--tud-model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-rows", type=int, default=EXPECTED_ROWS)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="vistec-segmentation-") as directory:
        work = Path(directory)
        gold = work / "vistec-gold.tsv"
        predictions = work / "vistec-predictions.tsv"
        model = json.loads(args.tud_model.read_text(encoding="utf-8"))
        rows = write_benchmark_files(args.csv, gold, predictions, model, expected_rows=args.expected_rows)
        subprocess.run([
            sys.executable, str(ROOT / "scripts/evaluate_segmentation.py"),
            "--gold", str(gold), "--predictions", str(predictions), "--output", str(args.output)
        ], check=True)
    report = json.loads(args.output.read_text(encoding="utf-8"))
    report["external_corpus"] = {
        "name": "VISTEC-TP-TH-2021",
        "source_url": "https://github.com/mrpeerat/OSKut/tree/215a7dc3d384f20eb56af1cbc41fb32b7f8df57c/VISTEC-TP-TH-2021",
        "source_commit": SOURCE_COMMIT,
        "source_git_blob_sha1": SOURCE_BLOB_SHA1,
        "source_id": SOURCE_ID,
        "license": SOURCE_LICENSE,
        "rows": rows,
        "annotation_field": "submissionText",
        "annotation_convention": "pipe-delimited word tokens with <ne> and <msp...> markup stripped; text is reconstructed from annotated submissionText, not raw questionText",
        "evidence_grade": "SOURCE_ANNOTATED_NOT_EXPERT_ADJUDICATED",
        "training_or_tuning_use": False,
        "caveats": [
            "This is a separate source corpus/domain from Wisesight and TUD, but its annotations are not independent expert re-adjudication by this project.",
            "Do not compare these source-label metrics directly with Wisesight without accounting for annotation conventions and domain.",
            "The dataset is CC BY-SA 3.0; preserve attribution and share-alike obligations for derivative data/artifacts.",
            "The annotation source text is submissionText after removing documented markup, not the original questionText field."
        ]
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "rows": rows,
                      "evidence_grade": "SOURCE_ANNOTATED_NOT_EXPERT_ADJUDICATED",
                      "engines": report["engines"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
