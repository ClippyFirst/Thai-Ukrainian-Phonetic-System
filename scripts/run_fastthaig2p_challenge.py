#!/usr/bin/env python3
"""Compare FastThaiG2P with ClippyFirst on the frozen 42-item Thai challenge.

This is an output/coverage diagnostic, not an accuracy benchmark: the challenge
currently has no independently adjudicated IPA labels.
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
import time
from pathlib import Path
from typing import Any

from thai_ukrainian.fastthaig2p_adapter import FastThaiG2PAdapter, UPSTREAM_COMMIT
from thai_ukrainian.text import analyze_text

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "benchmark" / "thai_g2p_challenge.jsonl"
DEFAULT_OUTPUT = ROOT / "reports" / "fastthaig2p-challenge-comparison.json"
_TONE_MARKS = set("˥˦˧˨˩")
_LENGTH_MARKS = set("ːˑ")
_SEGMENTAL_IGNORABLE = _TONE_MARKS | {"͡", "8"}


def load_challenge(path: Path) -> list[dict[str, Any]]:
    rows = []
    seen = set()
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            raise ValueError(f"{path}:{line_no}: expected object with string id")
        if row["id"] in seen or not isinstance(row.get("input"), str) or not row["input"]:
            raise ValueError(f"{path}:{line_no}: duplicate id or missing input")
        seen.add(row["id"])
        rows.append(row)
    if len(rows) != 42:
        raise ValueError(f"expected frozen 42-item challenge, found {len(rows)}")
    return rows


def segmental_projection(ipa: str) -> str:
    """Remove Chao tone, tie-bar and fallback sentinel for inter-engine comparison.

    This is a narrow comparison projection, not a rewrite of the source IPA.
    Raw IPA is retained; vowel length, glottal stops and other segments remain.
    """
    return "".join(ch for ch in ipa if ch not in _SEGMENTAL_IGNORABLE)


def summarize_ipa(syllables: list[str]) -> dict[str, int]:
    joined = "".join(syllables)
    return {
        "syllable_count": len(syllables),
        "tone_contour_codepoints": sum(ch in _TONE_MARKS for ch in joined),
        "vowel_length_marks": sum(ch in _LENGTH_MARKS for ch in joined),
        "aspiration_marks": joined.count("ʰ"),
        "unreleased_stop_marks": joined.count("̚"),
        "affricate_tie_bars": joined.count("͡"),
        "glottal_stops": joined.count("ʔ"),
    }


def _p95(values: list[float]) -> float:
    return sorted(values)[max(0, math.ceil(0.95 * len(values)) - 1)]


def run(input_path: Path = DEFAULT_INPUT) -> dict[str, Any]:
    challenge = load_challenge(input_path)
    external = FastThaiG2PAdapter()
    records = []
    clippy_output_count = 0
    external_nonempty_count = 0
    external_complete_count = 0
    external_passthrough_count = 0
    external_dictionary_tokens = 0
    external_oov_tokens = 0
    clippy_latencies = []
    external_latencies = []
    raw_exact_syllable_pairs = 0
    raw_exact_syllable_matches = 0
    segmental_pairs = 0
    segmental_matches = 0
    comparable_records = 0

    for row in challenge:
        started = time.perf_counter()
        tokens = analyze_text(row["input"])
        clippy_ms = (time.perf_counter() - started) * 1000
        clippy_latencies.append(clippy_ms)
        thai_tokens = [t for t in tokens if t.get("kind") == "thai"]
        clippy_syllables = [
            syllable for token in thai_tokens for syllable in token.get("syllables", [])
        ]
        clippy_ipa = [
            str(syllable["phonemic_ipa"])
            for syllable in clippy_syllables
            if syllable.get("phonemic_ipa")
        ]
        clippy_complete = (
            bool(clippy_syllables)
            and len(clippy_ipa) == len(clippy_syllables)
            and all(token.get("segmentation_status") != "unresolved" for token in thai_tokens)
        )
        clippy_output_count += int(clippy_complete)

        started = time.perf_counter()
        external_result = external.convert(row["input"])
        external_ms = (time.perf_counter() - started) * 1000
        external_latencies.append(external_ms)
        raw = external_result.raw_ipa
        external_syllables = list(external_result.syllable_ipa)
        external_nonempty = bool(raw.strip())
        external_complete = external_result.complete_ipa
        external_nonempty_count += int(external_nonempty)
        external_complete_count += int(external_complete)
        external_passthrough_count += int(bool(external_result.passthrough_text))
        dict_hits = external_result.dictionary_hit_count
        oov = external_result.oov_rule_fallback_count
        external_dictionary_tokens += dict_hits
        external_oov_tokens += oov

        comparable = (
            clippy_complete
            and external_complete
            and len(clippy_ipa) == len(external_syllables)
        )
        if comparable:
            comparable_records += 1
            raw_exact_syllable_pairs += len(clippy_ipa)
            raw_exact_syllable_matches += sum(
                left == right
                for left, right in zip(clippy_ipa, external_syllables, strict=True)
            )
            clippy_segmental = [segmental_projection(item) for item in clippy_ipa]
            external_segmental = [segmental_projection(item) for item in external_syllables]
            segmental_pairs += len(clippy_segmental)
            segmental_matches += sum(
                left == right
                for left, right in zip(clippy_segmental, external_segmental, strict=True)
            )

        records.append({
            "id": row["id"],
            "input": row["input"],
            "stratum": row.get("stratum"),
            "clippyfirst": {
                "complete_output": clippy_complete,
                "segmentation_statuses": [
                    token.get("segmentation_status") for token in thai_tokens
                ],
                "phonemic_ipa": clippy_ipa,
                "syllable_count": len(clippy_syllables),
                "elapsed_ms": round(clippy_ms, 6),
            },
            "fastthaig2p": {
                "raw_ipa": raw,
                "passthrough_text": external_result.passthrough_text,
                "complete_output": external_complete,
                "nonempty_output": external_nonempty,
                "syllable_ipa": external_syllables,
                "token_paths": [
                    {"token": item.token, "path": item.path}
                    for item in external_result.token_paths
                ],
                "upstream_token_count": len(external_result.token_paths),
                "dictionary_hit_count": dict_hits,
                "oov_rule_fallback_count": oov,
                "ipa_feature_inventory": summarize_ipa(external_syllables),
                "elapsed_ms": round(external_ms, 6),
            },
            "same_syllable_count": len(clippy_ipa) == len(external_syllables),
            "raw_exact_syllable_match_scored": bool(comparable),
            "segmental_projection_matches": (
                [
                    segmental_projection(left) == segmental_projection(right)
                    for left, right in zip(clippy_ipa, external_syllables, strict=True)
                ]
                if comparable else None
            ),
        })

    return {
        "schema_version": "1.1",
        "report_type": "ENGINE_COMPARISON_DIAGNOSTIC_NOT_ACCURACY_BENCHMARK",
        "challenge": {
            "path": str(input_path),
            "record_count": len(challenge),
            "gold_status": "NO_INDEPENDENTLY_ADJUDICATED_IPA",
        },
        "fastthaig2p": {
            "repository": "https://github.com/awslabs/FastThaiG2P",
            "upstream_commit": UPSTREAM_COMMIT,
            "adapter": "thai_ukrainian.fastthaig2p_adapter.FastThaiG2PAdapter",
            "api": "fastthaig2p.G2P.convert",
            "license": "Apache-2.0 upstream software; dictionary and fallback data provenance assessed separately",
        },
        "summary": {
            "challenge_inputs": len(challenge),
            "clippyfirst_complete_outputs": clippy_output_count,
            "fastthaig2p_nonempty_outputs": external_nonempty_count,
            "fastthaig2p_complete_ipa_outputs": external_complete_count,
            "fastthaig2p_passthrough_outputs": external_passthrough_count,
            "fastthaig2p_dictionary_tokens": external_dictionary_tokens,
            "fastthaig2p_oov_rule_fallback_tokens": external_oov_tokens,
            "records_with_both_complete_and_equal_syllable_count": comparable_records,
            "raw_exact_syllable_string_matches": raw_exact_syllable_matches,
            "raw_exact_syllable_string_pairs_compared": raw_exact_syllable_pairs,
            "raw_exact_syllable_agreement_rate": (
                raw_exact_syllable_matches / raw_exact_syllable_pairs
                if raw_exact_syllable_pairs else None
            ),
            "segmental_projection_matches": segmental_matches,
            "segmental_projection_pairs_compared": segmental_pairs,
            "segmental_projection_agreement_rate": (
                segmental_matches / segmental_pairs if segmental_pairs else None
            ),
            "clippyfirst_latency_ms": {
                "median": statistics.median(clippy_latencies),
                "p95": _p95(clippy_latencies),
            },
            "fastthaig2p_latency_ms": {
                "median": statistics.median(external_latencies),
                "p95": _p95(external_latencies),
            },
        },
        "limitations": [
            "The challenge has no independent IPA, tone, length, or boundary gold; no accuracy claim is possible.",
            "Raw exact syllable-string agreement is convention-sensitive; segmental projection removes only Chao tone marks, the tie bar and the upstream fallback sentinel 8. Both agreement values are inter-engine diagnostics, not correctness.",
            "ClippyFirst exposes phonemic IPA per syllable; FastThaiG2P emits slash-delimited IPA groups with Chao tone contours. Their conventions are not assumed equivalent.",
            "The adapter retains non-IPA passthrough text; such output is not counted as complete IPA and is not fed into the Ukrainian adapter.",
            "Dictionary-hit and OOV counts inspect private upstream fields pinned to the recorded commit and may need revision if the upstream API changes.",
            "Latency is measured in the same process but is not a controlled performance benchmark; initialization is excluded.",
            "The challenge set is adversarial and hand-picked, not a representative estimate of Thai coverage.",
        ],
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = run(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    print(f"Comparison report written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
