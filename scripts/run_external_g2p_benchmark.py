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
import urllib.error
import urllib.request
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

GORUUT_COMMIT = "b224bde02151f8f86d0fe260804e4ca743bda620"


def parse_goruut_response(body: Any) -> str:
    """Extract raw per-word phonetic strings without phone-symbol rewriting."""
    words = body.get("Words") if isinstance(body, dict) else None
    if not isinstance(words, list) or not words:
        raise ValueError(f"Goruut returned no Words array: {body!r}")
    phones = [word.get("Phonetic") for word in words if isinstance(word, dict)]
    if len(phones) != len(words) or any(not isinstance(phone, str) for phone in phones):
        raise ValueError(f"Goruut response has missing/non-string Phonetic fields: {body!r}")
    return " ".join(phones)


def candidate_goruut(url: str, language: str) -> tuple[Callable[[str], str], dict[str, Any]]:
    """Query a separately built, pinned Goruut HTTP service; never a runtime dependency."""
    if not url:
        raise ValueError("Goruut requires --goruut-url pointing at a running pinned service")

    def transcribe(text: str) -> str:
        payload = json.dumps({"Language": language, "Sentence": text}).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                body = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Goruut request failed: {type(exc).__name__}: {exc}") from exc
        # Preserve each engine-produced word string; spaces mark response word boundaries.
        return parse_goruut_response(body)

    return transcribe, {
        "package": "Goruut",
        "version": GORUUT_COMMIT,
        "source_commit": GORUUT_COMMIT,
        "configuration": {
            "api": "/tts/phonemize/sentence",
            "language": language,
            "raw_output_representation": "space-joined Word.Phonetic fields; individual phone strings unchanged",
        },
        "license_note": "Goruut repository reports MIT; per-language dictionary/model data provenance remains separately unreviewed.",
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


def has_usable_output(item: dict[str, Any]) -> bool:
    """Count only non-empty string outputs without a recorded per-input error."""
    raw = item.get("raw_output")
    return item.get("error") is None and isinstance(raw, str) and bool(raw.strip())


def summarize_per_engine(outputs: list[dict[str, Any]], selected: list[str]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for name in selected:
        engine_rows = [item for item in outputs if item["engine"] == name]
        failed = [item for item in engine_rows if item.get("error") is not None]
        summary[name] = {
            "output_rows": len(engine_rows),
            "successful_outputs": sum(has_usable_output(item) for item in engine_rows),
            "failed_outputs": len(failed),
            "empty_outputs_without_error": sum(item.get("error") is None and (not isinstance(item.get("raw_output"), str) or not item["raw_output"].strip()) for item in engine_rows),
            "failure_examples": [{"record_id": item.get("record_id"), "input": item.get("input"), "error": item.get("error")} for item in failed[:5]],
        }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "benchmark" / "runs" / "external-g2p-latest.jsonl")
    parser.add_argument("--engine", choices=[*CANDIDATES, "goruut", "all"], default="all")
    parser.add_argument("--goruut-url", default="", help="Optional URL of a running pinned Goruut service.")
    parser.add_argument("--goruut-language", default="Thai", help="Goruut's upstream language label.")
    args = parser.parse_args()

    if args.engine == "goruut" and not args.goruut_url:
        parser.error("--engine goruut requires --goruut-url")
    rows = load_rows(args.input)
    selected = list(CANDIDATES) if args.engine == "all" else [args.engine]
    if args.engine == "all" and args.goruut_url:
        selected.append("goruut")
    outputs: list[dict[str, Any]] = []
    errors: list[str] = []

    for name in selected:
        try:
            transcribe, metadata = (candidate_goruut(args.goruut_url, args.goruut_language) if name == "goruut" else CANDIDATES[name]())
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
    per_engine = summarize_per_engine(outputs, selected)
    per_input_failure_summaries = [
        f"{name}: {details['failed_outputs']} per-input failures"
        for name, details in per_engine.items()
        if details["failed_outputs"]
    ]
    summary = {
        "input": str(args.input),
        "inter_engine_diagnostic": inter_engine_diagnostic,
        "output": str(args.output),
        "candidate_rows": len(rows),
        "engines_requested": selected,
        "engines_run": sorted({item["engine"] for item in outputs}),
        "output_rows": len(outputs),
        "per_engine": per_engine,
        "gold_labeled_rows": sum(row.get("gold_phonemic_ipa") is not None for row in rows),
        "raw_string_diagnostic_rows": sum(item["exact_raw_string_match_diagnostic_only"] is not None for item in outputs),
        "errors": errors + per_input_failure_summaries,
        "interpretation": "Raw candidate outputs only. Per-engine failures and empty outputs are explicit. Raw-string equality and inter-engine agreement are diagnostic, not accuracy: candidate IPA conventions and segmentation differ. Adjudicate gold, document engine-specific normalization, then score features separately.",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    successful_outputs = sum(has_usable_output(item) for item in outputs)
    # A run where every engine failed to initialize or transcribe is not a
    # successful smoke test, even if failure rows were written for inspection.
    return 0 if successful_outputs else (2 if errors or outputs else 0)


if __name__ == "__main__":
    sys.exit(main())
