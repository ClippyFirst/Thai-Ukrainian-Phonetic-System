#!/usr/bin/env python3
"""Run the authored engine on the challenge set without claiming accuracy.

This is a reproducible runtime/abstention diagnostic. The challenge records do
not contain adjudicated gold, so this report intentionally emits no accuracy
or correctness score.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from thai_ukrainian.text import analyze_text, analyze_text_with_word_segmentation

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "benchmark" / "thai_g2p_challenge.jsonl"
DEFAULT_OUTPUT = ROOT / "reports" / "challenge-runtime-diagnostics.json"


def load_challenge(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    with path.open("r", encoding="utf-8") as stream:
        for line_no, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
                raise ValueError(f"{path}:{line_no}: each record needs a non-empty string id")
            if row["id"] in seen:
                raise ValueError(f"{path}:{line_no}: duplicate id {row['id']!r}")
            if not isinstance(row.get("input"), str) or not row["input"]:
                raise ValueError(f"{path}:{line_no}: each record needs a non-empty string input")
            seen.add(row["id"])
            rows.append(row)
    if not rows:
        raise ValueError(f"{path}: challenge set is empty; refusing to emit a vacuous diagnostic")
    return rows


def _emits_complete_output(tokens: list[dict[str, Any]]) -> bool:
    thai_tokens = [token for token in tokens if token.get("kind") == "thai"]
    syllables = [syllable for token in thai_tokens for syllable in token.get("syllables", [])]
    return bool(thai_tokens) and bool(syllables) and all(
        bool(syllable.get("phonemic_ipa"))
        and bool(syllable.get("ukrainian_transliteration"))
        for syllable in syllables
    ) and all(token.get("segmentation_status") != "unresolved" for token in thai_tokens)


def _coordination_cluster(row: dict[str, Any], emitted: bool, syllables: list[dict[str, Any]],
                          word_segmented_emitted: bool) -> str:
    if emitted:
        return "OUTPUT_AVAILABLE_NOT_GOLD"
    if row.get("stratum") in {"ฤ-series", "ฦ-series"}:
        return "SPECIAL_VOWEL_NEEDS_LEXICAL_CONTEXT"
    statuses = {str(item.get("status")) for item in syllables}
    if any(status.startswith("analysis-dependent:special-orthography") for status in statuses):
        if "ทร" in row.get("input", ""):
            return "CONTEXTUAL_THR_HOMOGRAPH_OR_CLUSTER"
        if "รร" in row.get("input", ""):
            return "CONTEXTUAL_RR_READING"
        return "SPECIAL_ORTHOGRAPHY_NEEDS_LEXICAL_EVIDENCE"
    if row.get("stratum") == "invalid-input":
        return "EXPECTED_INVALID_OR_MALFORMED_ABSTENTION"
    if word_segmented_emitted:
        return "CONSERVATIVE_ENDPOINT_ABSTENTION_WORD_SEGMENTED_PATH_AVAILABLE"
    if str(row.get("stratum", "")).startswith("article-style"):
        return "CONTINUOUS_TEXT_WORD_BOUNDARY_GAP"
    if row.get("stratum") == "loanword":
        return "LOANWORD_LEXICAL_COVERAGE_GAP"
    if row.get("stratum") == "false-cluster":
        return "FALSE_CLUSTER_LEXICAL_EXCEPTION_GAP"
    if row.get("stratum") == "rr-series":
        return "RR_LEXICAL_READING_GAP"
    return "UNRESOLVED_SEGMENTATION_OR_PHONOLOGY_REVIEW"


def build_report(path: Path = DEFAULT_INPUT) -> dict[str, Any]:
    challenge = load_challenge(path)
    segmentation_counts: Counter[str] = Counter()
    analysis_counts: Counter[str] = Counter()
    details: list[dict[str, Any]] = []
    output_count = 0
    abstained_count = 0
    word_segmented_output_count = 0

    for row in challenge:
        tokens = analyze_text(row["input"])
        thai_tokens = [token for token in tokens if token.get("kind") == "thai"]
        syllables = [
            syllable
            for token in thai_tokens
            for syllable in token.get("syllables", [])
        ]
        segmentation = (
            thai_tokens[0].get("segmentation_status", "not_applicable")
            if len(thai_tokens) == 1
            else "multiple_or_no_thai_tokens"
        )
        segmentation_counts[segmentation] += 1
        for syllable in syllables:
            analysis_counts[str(syllable.get("status", "missing-status"))] += 1

        emitted = _emits_complete_output(tokens)
        word_segmented_tokens = analyze_text_with_word_segmentation(row["input"])
        word_segmented_syllables = [
            syllable
            for token in word_segmented_tokens
            if token.get("kind") == "thai"
            for syllable in token.get("syllables", [])
        ]
        word_segmented_emitted = _emits_complete_output(word_segmented_tokens)
        if word_segmented_emitted:
            word_segmented_output_count += 1
        if emitted:
            output_count += 1
        else:
            abstained_count += 1
        coordination_cluster = _coordination_cluster(
            row, emitted, syllables, word_segmented_emitted
        )

        details.append({
            "id": row["id"],
            "input": row["input"],
            "stratum": row.get("stratum"),
            "segmentation_status": segmentation,
            "token_count": len(tokens),
            "syllable_count": len(syllables),
            "analysis_statuses": [s.get("status") for s in syllables],
            "phonemic_ipa": [s.get("phonemic_ipa") for s in syllables],
            "surface_ipa": [s.get("phonetic_ipa") for s in syllables],
            "tone_categories": [
                (s.get("tone") or {}).get("tone") if isinstance(s.get("tone"), dict) else None
                for s in syllables
            ],
            "vowel_lengths": [s.get("vowel_length") for s in syllables],
            "ukrainian_outputs": [s.get("ukrainian_transliteration") for s in syllables],
            "warnings": [warning for token in tokens for warning in token.get("warnings", [])],
            "engine_output_emitted": emitted,
            "word_segmented_output_emitted": word_segmented_emitted,
            "word_segmented_token_count": sum(token.get("kind") == "thai" for token in word_segmented_tokens),
            "word_segmented_syllable_count": len(word_segmented_syllables),
            "word_segmented_statuses": [
                token.get("word_segmentation_status")
                for token in word_segmented_tokens if token.get("kind") == "thai"
            ],
            "word_segmented_methods": sorted({
                str(token.get("word_segmentation_method"))
                for token in word_segmented_tokens
                if token.get("kind") == "thai" and token.get("word_segmentation_method")
            }),
            "word_segmented_evidence_grades": sorted({
                str(token.get("word_segmentation_evidence_grade"))
                for token in word_segmented_tokens
                if token.get("kind") == "thai" and token.get("word_segmentation_evidence_grade")
            }),
            "coordination_cluster": coordination_cluster,
        })

    return {
        "schema_version": "1.0",
        "evaluation_kind": "runtime_diagnostic_not_accuracy_benchmark",
        "gold_status": "NOT_ADJUDICATED",
        "input_file": path.name,
        "summary": {
            "challenge_inputs": len(challenge),
            "inputs_with_engine_output": output_count,
            "inputs_abstained_or_without_complete_output": abstained_count,
            "inputs_with_word_segmented_output": word_segmented_output_count,
            "inputs_without_word_segmented_output": len(challenge) - word_segmented_output_count,
            "coordination_cluster_counts": dict(sorted(Counter(
                record["coordination_cluster"] for record in details
            ).items())),
            "segmentation_status_counts": dict(sorted(segmentation_counts.items())),
            "syllable_analysis_status_counts": dict(sorted(analysis_counts.items())),
        },
        "limitations": [
            "The challenge set has no independently adjudicated IPA or word-boundary gold.",
            "Output presence, parser status, and external-engine agreement are not correctness measures.",
            "Abstention is reported explicitly and is not counted as a pronunciation error.",
            "The opt-in dictionary-word-segmented path is reported separately; it does not replace the conservative endpoint or prove word-boundary correctness.",
            "coordination_cluster labels are workflow triage categories, not adjudicated error labels or accuracy outcomes.",
            "This hand-picked adversarial set is not a representative estimate of Thai coverage.",
        ],
        "records": details,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    try:
        report = build_report(args.input)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Diagnostic report written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
