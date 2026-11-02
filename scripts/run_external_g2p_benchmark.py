#!/usr/bin/env python3
"""Run optional external Thai G2P engines against the challenge JSONL.

This script is intentionally separate from the production runtime. It records
raw candidate output and timing; it only scores exact IPA matches for rows
with independently adjudicated gold_phonemic_ipa values.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import statistics
import subprocess
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


class CandidateAbstention(RuntimeError):
    """A candidate deliberately withholds a result for this input."""


def candidate_clippyfirst() -> tuple[Callable[[str], str], dict[str, Any]]:
    from thai_ukrainian.text import analyze_text_with_word_segmentation

    def transcribe(text: str) -> str:
        tokens = analyze_text_with_word_segmentation(text)
        ipa_words: list[str] = []
        for token in tokens:
            if token.get("kind") != "thai":
                continue
            syllables = token.get("syllables") or []
            if token.get("segmentation_status") == "unresolved" or not syllables:
                raise CandidateAbstention(
                    f"conservative ClippyFirst abstention for token {token.get('input')!r}"
                )
            ipa_syllables = []
            for syllable in syllables:
                # Consume the same typed IPA boundary as the Ukrainian adapter.
                typed_ipa = syllable.get("phonetic_result")
                if not isinstance(typed_ipa, dict) or typed_ipa.get("status") != "SUPPORTED":
                    raise CandidateAbstention(
                        f"ClippyFirst typed IPA is not supported for token {token.get('input')!r}"
                    )
                ipa = typed_ipa.get("phonemic_ipa")
                tone = typed_ipa.get("tone_contour_ipa")
                if not isinstance(ipa, str) or not ipa or not isinstance(tone, str) or not tone:
                    raise CandidateAbstention(
                        f"ClippyFirst withheld segmental IPA or tone for token {token.get('input')!r}"
                    )
                ipa_syllables.append(ipa + tone)
            ipa_words.append("/" + ".".join(ipa_syllables) + "/")
        if not ipa_words:
            raise CandidateAbstention("ClippyFirst produced no Thai IPA tokens")
        return " ".join(ipa_words)

    return transcribe, {
        "package": "ClippyFirst",
        "version": "in-repository",
        "configuration": {
            "api": "analyze_text_with_word_segmentation",
            "phonemic_ipa": True,
            "typed_ipa_contract": "PhoneticResult (segmental IPA plus separate tone contour)",
            "policy": "conservative; abstain unless every Thai token has complete IPA and tone",
            "word_segmentation": "pinned ClippyFirst dictionary maximum matching",
        },
        "source_commit": "runtime-at-benchmark-commit",
    }


def candidate_fastthaig2p() -> tuple[Callable[[str], str], dict[str, Any]]:
    from thai_ukrainian.adapters.fastthaig2p import FastThaiG2PAdapter

    adapter = FastThaiG2PAdapter()
    return adapter.convert, adapter.metadata()


CANDIDATES = {
    "clippyfirst": candidate_clippyfirst,
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


def strip_ipa_delimiter_slashes_diagnostic(value: str | None) -> str | None:
    """Remove IPA /.../ transcription delimiters only; never used for scoring."""
    if value is None:
        return None
    return value.replace("/", "").strip()


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
        if ident is None or not isinstance(raw, str) or not raw.strip() or row.get("error") is not None:
            continue
        grouped.setdefault(str(ident), []).append(raw.strip())

    comparable_inputs = 0
    pair_count = 0
    exact_pairs = 0
    slash_stripped_pairs = 0
    slash_only_pairs = 0
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
                slash_equal = strip_ipa_delimiter_slashes_diagnostic(values[i]) == strip_ipa_delimiter_slashes_diagnostic(values[j])
                tone_equal = strip_tone_symbols_diagnostic(strip_ipa_delimiter_slashes_diagnostic(values[i])) == strip_tone_symbols_diagnostic(strip_ipa_delimiter_slashes_diagnostic(values[j]))
                exact_pairs += int(exact)
                slash_stripped_pairs += int(slash_equal)
                slash_only_pairs += int(not exact and slash_equal)
                tone_stripped_pairs += int(tone_equal)
                tone_only_pairs += int(not slash_equal and tone_equal)
                non_tone_pairs += int(not tone_equal)
    return {
        "comparable_inputs": comparable_inputs,
        "engine_pairs_compared": pair_count,
        "exact_agreement_pairs": exact_pairs,
        "slash_delimiter_stripped_agreement_pairs_diagnostic_only": slash_stripped_pairs,
        "slash_only_format_disagreements_diagnostic_only": slash_only_pairs,
        "slash_and_tone_stripped_agreement_pairs_diagnostic_only": tone_stripped_pairs,
        "tone_only_disagreements_after_slash_stripping_diagnostic_only": tone_only_pairs,
        "remaining_mismatches_after_limited_diagnostics": non_tone_pairs,
        "exact_agreement_rate": exact_pairs / pair_count if pair_count else None,
        "slash_delimiter_stripped_agreement_rate_diagnostic_only": slash_stripped_pairs / pair_count if pair_count else None,
        "slash_and_tone_stripped_agreement_rate_diagnostic_only": tone_stripped_pairs / pair_count if pair_count else None,
        "interpretation": "Inter-engine agreement is not accuracy. Slash-delimiter and tone-stripped results are separate diagnostics only; raw outputs and tone-sensitive exact-match rules are unchanged.",
    }


def has_usable_output(item: dict[str, Any]) -> bool:
    """Count only non-empty string outputs without a recorded per-input error."""
    raw = item.get("raw_output")
    return item.get("error") is None and isinstance(raw, str) and bool(raw.strip())


def build_pairwise_engine_diagnostic(outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Compare each engine pair on shared successful inputs; not an accuracy metric."""
    grouped: dict[str, dict[str, str]] = {}
    for row in outputs:
        ident, engine, raw = row.get("record_id"), row.get("engine"), row.get("raw_output")
        if ident is None or not isinstance(engine, str) or not isinstance(raw, str) or not raw.strip() or row.get("error") is not None:
            continue
        grouped.setdefault(str(ident), {})[engine] = raw.strip()
    names = sorted({engine for group in grouped.values() for engine in group})
    report = []
    for i, engine_a in enumerate(names):
        for engine_b in names[i + 1:]:
            pairs = [(group[engine_a], group[engine_b]) for group in grouped.values() if engine_a in group and engine_b in group]
            raw_matches = sum(a == b for a, b in pairs)
            slash_matches = sum(strip_ipa_delimiter_slashes_diagnostic(a) == strip_ipa_delimiter_slashes_diagnostic(b) for a, b in pairs)
            tone_matches = sum(strip_tone_symbols_diagnostic(strip_ipa_delimiter_slashes_diagnostic(a)) == strip_tone_symbols_diagnostic(strip_ipa_delimiter_slashes_diagnostic(b)) for a, b in pairs)
            report.append({
                "engine_a": engine_a, "engine_b": engine_b, "comparable_inputs": len(pairs),
                "raw_exact_matches": raw_matches,
                "slash_delimiter_stripped_matches_diagnostic_only": slash_matches,
                "slash_and_tone_stripped_matches_diagnostic_only": tone_matches,
                "remaining_mismatches_after_limited_diagnostics": len(pairs) - tone_matches,
                "raw_exact_agreement_rate": raw_matches / len(pairs) if pairs else None,
                "slash_and_tone_stripped_agreement_rate_diagnostic_only": tone_matches / len(pairs) if pairs else None,
            })
    return report

def _percentile(values: list[float], percentile: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, int((len(ordered) * percentile + 0.999999)) - 1))
    return round(ordered[index], 3)


def summarize_per_engine(outputs: list[dict[str, Any]], selected: list[str]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for name in selected:
        engine_rows = [item for item in outputs if item["engine"] == name]
        failed = [item for item in engine_rows if item.get("outcome", "error" if item.get("error") else "success") == "error"]
        abstained = [item for item in engine_rows if item.get("outcome") == "abstain"]
        successful = sum(has_usable_output(item) for item in engine_rows)
        latencies = [float(item["elapsed_ms"]) for item in engine_rows if isinstance(item.get("elapsed_ms"), (int, float))]
        summary[name] = {
            "output_rows": len(engine_rows),
            "successful_outputs": successful,
            "coverage": successful / len(engine_rows) if engine_rows else None,
            "abstained_outputs": len(abstained),
            "runtime_failures": len(failed),
            "failed_outputs": len(failed),
            "empty_outputs_without_error": sum(item.get("error") is None and (not isinstance(item.get("raw_output"), str) or not item["raw_output"].strip()) for item in engine_rows),
            "latency_ms": {
                "median": round(statistics.median(latencies), 3) if latencies else None,
                "p95": _percentile(latencies, 0.95),
                "n": len(latencies),
            },
            "failure_examples": [{"record_id": item.get("record_id"), "input": item.get("input"), "error": item.get("error")} for item in failed[:5]],
            "abstention_examples": [{"record_id": item.get("record_id"), "input": item.get("input"), "reason": item.get("error")} for item in abstained[:5]],
        }
    return summary


def repository_revision() -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


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
            outcome = "success"
            try:
                raw = transcribe(row["input"])
                error = None
            except CandidateAbstention as exc:
                raw = None
                error = f"{type(exc).__name__}: {exc}"
                outcome = "abstain"
            except Exception as exc:  # retain failure rows instead of silently dropping them
                raw = None
                error = f"{type(exc).__name__}: {exc}"
                outcome = "error"
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
                "outcome": outcome,
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
        f"{name}: {details['runtime_failures']} per-input runtime failures"
        for name, details in per_engine.items()
        if details["runtime_failures"]
    ]
    abstention_summaries = [
        f"{name}: {details['abstained_outputs']} conservative abstentions"
        for name, details in per_engine.items()
        if details["abstained_outputs"]
    ]
    corpus_bytes = args.input.read_bytes()
    summary = {
        "report_type": "SAME_INPUT_G2P_COMPARISON_DIAGNOSTIC_NOT_ACCURACY",
        "input": str(args.input),
        "corpus_sha256": hashlib.sha256(corpus_bytes).hexdigest(),
        "repository_commit": repository_revision() or __import__("os").environ.get("GITHUB_SHA"),
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inter_engine_diagnostic": inter_engine_diagnostic,
        "pairwise_engine_diagnostic": build_pairwise_engine_diagnostic(outputs),
        "output": str(args.output),
        "candidate_rows": len(rows),
        "engines_requested": selected,
        "engines_run": sorted({item["engine"] for item in outputs}),
        "output_rows": len(outputs),
        "per_engine": per_engine,
        "gold_labeled_rows": sum(row.get("gold_phonemic_ipa") is not None for row in rows),
        "accuracy_status": "NOT_MEASURED_BY_THIS_SMOKE_RUNNER; use benchmark_ipa.py only after the independent adjudication gate",
        "raw_string_diagnostic_rows": sum(item["exact_raw_string_match_diagnostic_only"] is not None for item in outputs),
        "errors": errors + per_input_failure_summaries,
        "abstentions": abstention_summaries,
        "interpretation": "All engines receive the same frozen input rows. Coverage, abstention and latency are engineering diagnostics; raw-string equality and inter-engine agreement are not accuracy. Gold is required for accuracy. No IPA normalization is applied for scoring.",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    successful_outputs = sum(has_usable_output(item) for item in outputs)
    # A run where every engine failed to initialize or transcribe is not a
    # successful smoke test, even if failure rows were written for inspection.
    return 0 if successful_outputs else (2 if errors or outputs else 0)


if __name__ == "__main__":
    sys.exit(main())
