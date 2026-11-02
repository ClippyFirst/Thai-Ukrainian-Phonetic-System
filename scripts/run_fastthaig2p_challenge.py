#!/usr/bin/env python3
"""Compare FastThaiG2P with ClippyFirst on the frozen 42-item Thai challenge.

This is an output/coverage diagnostic, not an accuracy benchmark: the challenge
currently has no independently adjudicated IPA labels.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import time
from pathlib import Path
from typing import Any

from thai_ukrainian.text import analyze_text

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "benchmark" / "thai_g2p_challenge.jsonl"
DEFAULT_OUTPUT = ROOT / "reports" / "fastthaig2p-challenge-comparison.json"
UPSTREAM_COMMIT = "4e82a291b4cf2876326744c6580121e9986ad354"
_WORD_IPA = re.compile(r"/([^/]+)/")
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


def parse_external_ipa(raw: str) -> list[str]:
    """Extract slash-delimited word groups and dot-delimited syllable strings.

    Keep the upstream raw string separately. This parser is intentionally
    lossless with respect to IPA symbols; it does not infer a ClippyFirst tone
    category or silently rewrite the upstream transcription.
    """
    syllables: list[str] = []
    for match in _WORD_IPA.finditer(raw):
        group = match.group(1).strip()
        if group:
            syllables.extend(part for part in group.split(".") if part)
    return syllables


def segmental_projection(ipa: str) -> str:
    """Remove only FastThaiG2P tone contour/sentinel and affricate tie-bar notation.

    This diagnostic projection aligns broad segment strings across the two
    engines; raw IPA is retained and tone is evaluated as a separate feature.
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


def run(input_path: Path = DEFAULT_INPUT) -> dict[str, Any]:
    try:
        from fastthaig2p import G2P
        from fastthaig2p.normalizer import normalize
    except ImportError as exc:
        raise RuntimeError(
            "FastThaiG2P is optional; install the pinned upstream commit "
            f"{UPSTREAM_COMMIT}"
        ) from exc

    challenge = load_challenge(input_path)
    external = G2P()
    records = []
    clippy_output_count = 0
    external_output_count = 0
    external_dictionary_tokens = 0
    external_oov_tokens = 0
    clippy_latencies = []
    external_latencies = []
    exact_syllable_pairs = 0
    exact_syllable_matches = 0
    comparable_records = 0

    for row in challenge:
        started = time.perf_counter()
        tokens = analyze_text(row["input"])
        clippy_ms = (time.perf_counter() - started) * 1000
        clippy_latencies.append(clippy_ms)
        thai_tokens = [t for t in tokens if t.get("kind") == "thai"]
        clippy_syllables = [
            s for token in thai_tokens for s in token.get("syllables", [])
        ]
        clippy_ipa = [str(s["phonemic_ipa"]) for s in clippy_syllables if s.get("phonemic_ipa")]
        clippy_complete = bool(clippy_syllables) and len(clippy_ipa) == len(clippy_syllables) and all(
            t.get("segmentation_status") != "unresolved" for t in thai_tokens
        )
        clippy_output_count += int(clippy_complete)

        # Inspect the pinned upstream token/dictionary boundary to distinguish
        # dictionary hits from rule-fallback tokens. This is a diagnostic only.
        normalized = normalize(row["input"])
        upstream_tokens = [
            token for token in external._tokenizer.tokenize(normalized) if token.strip()
        ]
        dict_hits = sum(bool(external._ipa.get(token)) for token in upstream_tokens)
        oov = len(upstream_tokens) - dict_hits
        external_dictionary_tokens += dict_hits
        external_oov_tokens += oov

        started = time.perf_counter()
        raw = external.convert(row["input"])
        external_ms = (time.perf_counter() - started) * 1000
        external_latencies.append(external_ms)
        external_syllables = parse_external_ipa(raw)
        external_complete = bool(external_syllables)
        external_output_count += int(external_complete)

        comparable = clippy_complete and external_complete and len(clippy_ipa) == len(external_syllables)
        if comparable:
            comparable_records += 1
            exact_syllable_pairs += len(clippy_ipa)
            exact_syllable_matches += sum(
                a == b for a, b in zip(clippy_ipa, external_syllables, strict=True)
            )

        records.append({
            "id": row["id"],
            "input": row["input"],
            "stratum": row.get("stratum"),
            "clippyfirst": {
                "complete_output": clippy_complete,
                "segmentation_statuses": [t.get("segmentation_status") for t in thai_tokens],
                "phonemic_ipa": clippy_ipa,
                "syllable_count": len(clippy_syllables),
                "elapsed_ms": round(clippy_ms, 6),
            },
            "fastthaig2p": {
                "raw_ipa": raw,
                "complete_output": external_complete,
                "syllable_ipa": external_syllables,
                "upstream_token_count": len(upstream_tokens),
                "dictionary_hit_count": dict_hits,
                "oov_rule_fallback_count": oov,
                "ipa_feature_inventory": summarize_ipa(external_syllables),
                "elapsed_ms": round(external_ms, 6),
            },
            "same_syllable_count": len(clippy_ipa) == len(external_syllables),
            "raw_exact_syllable_match_scored": bool(comparable),\n            "segmental_projection_matches": (\n                [segmental_projection(a) == segmental_projection(b) for a, b in zip(clippy_ipa, external_syllables, strict=True)]\n                if comparable else None\n            ),
        })

    return {
        "schema_version": "1.0",
        "report_type": "ENGINE_COMPARISON_DIAGNOSTIC_NOT_ACCURACY_BENCHMARK",
        "challenge": {
            "path": str(input_path.relative_to(ROOT)),
            "record_count": len(challenge),
            "gold_status": "NO_INDEPENDENTLY_ADJUDICATED_IPA",
        },
        "fastthaig2p": {
            "repository": "https://github.com/awslabs/FastThaiG2P",
            "upstream_commit": UPSTREAM_COMMIT,
            "api": "fastthaig2p.G2P.convert",
            "license": "Apache-2.0 for upstream software; dictionary/data provenance assessed separately",
        },
        "summary": {
            "challenge_inputs": len(challenge),
            "clippyfirst_complete_outputs": clippy_output_count,
            "fastthaig2p_nonempty_outputs": external_output_count,
            "fastthaig2p_dictionary_tokens": external_dictionary_tokens,
            "fastthaig2p_oov_rule_fallback_tokens": external_oov_tokens,
            "records_with_both_complete_and_equal_syllable_count": comparable_records,
            "exact_syllable_string_matches_on_comparable_records": exact_syllable_matches,
            "exact_syllable_string_pairs_compared": exact_syllable_pairs,
            "exact_syllable_agreement_rate": (
                exact_syllable_matches / exact_syllable_pairs if exact_syllable_pairs else None
            ),
            "clippyfirst_latency_ms": {
                "median": statistics.median(clippy_latencies),
                "p95": sorted(clippy_latencies)[max(0, int(0.95 * len(clippy_latencies)) - 1)],
            },
            "fastthaig2p_latency_ms": {
                "median": statistics.median(external_latencies),
                "p95": sorted(external_latencies)[max(0, int(0.95 * len(external_latencies)) - 1)],
            },
        },
        "limitations": [
            "The challenge has no independent IPA, tone, length, or boundary gold; no accuracy claim is possible.",
            "Raw exact syllable-string agreement is convention-sensitive; segmental projection removes only Chao tone marks, the tie bar and the upstream fallback sentinel 8. Both agreement values are inter-engine diagnostics, not correctness.",
            "ClippyFirst exposes phonemic IPA per syllable; FastThaiG2P emits slash-delimited IPA groups with Chao tone contours. Their conventions are not assumed equivalent.",
            "The report preserves FastThaiG2P raw IPA and does not feed it into the Ukrainian adapter.",
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
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    print(f"Comparison report written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
