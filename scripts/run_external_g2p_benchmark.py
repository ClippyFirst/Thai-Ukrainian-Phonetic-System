#!/usr/bin/env python3
"""Run optional external Thai G2P engines against the challenge JSONL.

This script is intentionally separate from the production runtime. It records
raw candidate output and timing; it only scores exact IPA matches for rows
with independently adjudicated gold_phonemic_ipa values.
"""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import sys
import time
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "benchmark" / "thai_g2p_challenge.jsonl"


def package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def load_rows(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict) or not isinstance(row.get("input"), str):
            raise ValueError(f"{path}:{line_number}: expected object with string 'input'")
        rows.append(row)
    if not rows:
        raise ValueError(f"{path}: challenge corpus contains no records")
    return rows


def candidate_thaiphon() -> tuple[Callable[[str], str], dict[str, Any]]:
    import thaiphon

    return (
        lambda text: thaiphon.transcribe_sentence(text, scheme="ipa"),
        {
            "package": "thaiphon",
            "version": getattr(thaiphon, "__version__", None) or package_version("thaiphon"),
            "configuration": {"scheme": "ipa", "api": "transcribe_sentence"},
            "optional_lexicon_installed": package_version("thaiphon-data-volubilis") is not None,
        },
    )


def candidate_fastthaig2p() -> tuple[Callable[[str], str], dict[str, Any]]:
    from fastthaig2p import G2P

    engine = G2P()
    return (
        engine.convert,
        {
            "package": "FastThaiG2P",
            "version": package_version("fastthaig2p"),
            "configuration": {"api": "G2P.convert", "default_dictionary_and_fallback": True},
            "source_commit": "c4759eef7df03e11fcbb9aa83efe8cf21709fd2f",
        },
    )


CANDIDATES = {
    "thaiphon": candidate_thaiphon,
    "fastthaig2p": candidate_fastthaig2p,
}


def normalized_ipa(value: str | None) -> str | None:
    if value is None:
        return None
    # Conservative normalization only: trim outer whitespace. Do not strip
    # tone, length, syllable dots, or tie bars because those are scoreable data.
    return value.strip()


def strip_tone_symbols_diagnostic(value: str | None) -> str | None:
    """Remove only IPA tone letters for diagnostic decomposition, never for scoring."""
    if value is None:
        return None
    return value.translate(str.maketrans("", "", "˥˦˧˨˩"))


def build_inter_engine_diagnostic(outputs: list[dict[str, Any]]) -> dict[str, Any]:
    """Compare engine outputs per input without treating agreement as accuracy."""
    grouped: dict[str, list[str]] = {}
    for row in outputs:
        raw = row.get("raw_output")
        ident = row.get("record_id")
        if ident is None or not isinstance(raw, str) or row.get("error") is not None:
            continue
        grouped.setdefault(str(ident), []).append(raw.strip())

    comparable_inputs = 0
    pair_count = 0
    exact_pairs = 0
    tone_stripped_pairs = 0
    tone_only_pairs = 0
    non_tone_pairs = 0
    for values in grouped.values():
        if len(values) < 2:
            continue
        comparable_inputs += 1
        for i in range(len(values)):
            for j in range(i + 1, len(values)):
                pair_count += 1
                exact = values[i] == values[j]
                tone_equal = strip_tone_symbols_diagnostic(values[i]) == strip_tone_symbols_diagnostic(values[j])
                exact_pairs += int(exact)
                tone_stripped_pairs += int(tone_equal)
                tone_only_pairs += int(not exact and tone_equal)
                non_tone_pairs += int(not exact and not tone_equal)
    return {
        "comparable_inputs": comparable_inputs,
        "engine_pairs_compared": pair_count,
        "exact_agreement_pairs": exact_pairs,
        "tone_stripped_agreement_pairs_diagnostic_only": tone_stripped_pairs,
        "tone_only_disagreements_diagnostic_only": tone_only_pairs,
        "non_tone_or_format_disagreements_requiring_review": non_tone_pairs,
        "exact_agreement_rate": exact_pairs / pair_count if pair_count else None,
        "tone_stripped_agreement_rate_diagnostic_only": tone_stripped_pairs / pair_count if pair_count else None,
        "interpretation": "Inter-engine agreement is not accuracy. Tone-stripped results are a diagnostic decomposition only; raw outputs and tone-sensitive exact-match rules are unchanged.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "benchmark" / "runs" / "external-g2p-latest.jsonl")
    parser.add_argument("--engine", choices=[*CANDIDATES, "all"], default="all")
    args = parser.parse_args()

    rows = load_rows(args.input)
    selected = list(CANDIDATES) if args.engine == "all" else [args.engine]
    outputs: list[dict[str, Any]] = []
    errors: list[str] = []

    for name in selected:
        try:
            transcribe, metadata = CANDIDATES[name]()
        except Exception as exc:  # optional dependencies are deliberately non-fatal
            errors.append(f"{name}: unavailable: {type(exc).__name__}: {exc}")
            continue

        for row in rows:
            started = time.perf_counter()
            try:
                raw = transcribe(row["input"])
                error = None
            except Exception as exc:  # retain failure rows instead of silently dropping them
                raw = None
                error = f"{type(exc).__name__}: {exc}"
            elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
            gold = normalized_ipa(row.get("gold_phonemic_ipa"))
            candidate = normalized_ipa(raw)
            outputs.append({
                "record_id": row.get("id"),
                "input": row["input"],
                "stratum": row.get("stratum"),
                "engine": name,
                "engine_metadata": metadata,
                "raw_output": raw,
                "elapsed_ms": elapsed_ms,
                "error": error,
                "gold_status": row.get("lexical_attestation_status", "not_adjudicated"),
                "exact_raw_string_match_diagnostic_only": (candidate == gold) if gold is not None and candidate is not None else None,
            })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as stream:
        for item in outputs:
            stream.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")

    inter_engine_diagnostic = build_inter_engine_diagnostic(outputs)
    summary = {
        "input": str(args.input),
        "inter_engine_diagnostic": inter_engine_diagnostic,
        "output": str(args.output),
        "candidate_rows": len(rows),
        "engines_requested": selected,
        "engines_run": sorted({item["engine"] for item in outputs}),
        "output_rows": len(outputs),
        "gold_labeled_rows": sum(row.get("gold_phonemic_ipa") is not None for row in rows),
        "raw_string_diagnostic_rows": sum(item["exact_raw_string_match_diagnostic_only"] is not None for item in outputs),
        "errors": errors,
        "interpretation": "Raw candidate outputs only. Raw-string equality is diagnostic, not a fair accuracy score: candidate IPA conventions and segmentation differ. Adjudicate gold, document engine-specific normalization, then score features separately.",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    successful_outputs = sum(item["error"] is None for item in outputs)
    # A run where every engine failed to initialize or transcribe is not a
    # successful smoke test, even if failure rows were written for inspection.
    return 0 if successful_outputs else (2 if errors or outputs else 0)


if __name__ == "__main__":
    sys.exit(main())
