#!/usr/bin/env python3
"""Probe repeatability of pinned Goruut outputs; this is not an accuracy benchmark."""
from __future__ import annotations
import argparse, json, sys, time, urllib.error, urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.run_external_g2p_benchmark import load_rows
DEFAULT_INPUT = ROOT / "data" / "benchmark" / "thai_g2p_challenge.jsonl"
GORUUT_COMMIT = "b224bde02151f8f86d0fe260804e4ca743bda620"

def query(url: str, language: str, text: str) -> dict[str, Any]:
    payload = json.dumps({"Language": language, "Sentence": text}).encode("utf-8")
    request = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=20) as response:
        value = json.loads(response.read().decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object, got {type(value).__name__}")
    return value

def summarize_case(record_id: str, text: str, attempts: list[dict[str, Any]]) -> dict[str, Any]:
    outputs = [a["phonetic_output"] for a in attempts if a.get("phonetic_output")]
    variants = sorted(set(outputs))
    return {"record_id": record_id, "input": text, "attempts": attempts,
            "successful_nonempty_calls": len(outputs), "unique_nonempty_outputs": len(variants),
            "varies_across_repetitions": len(variants)>1, "distinct_outputs": variants,
            "status": "NO_NONEMPTY_OUTPUT" if not outputs else "VARIABLE_OUTPUT" if len(variants)>1 else "REPEATED_OUTPUT_STABLE_IN_THIS_SAMPLE"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--language", default="Thai")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts" / "goruut-repeatability.json")
    args = parser.parse_args()
    if args.repeats < 2:
        parser.error("--repeats must be at least 2")
    rows = load_rows(args.input)
    cases, all_attempts = [], []
    for row in rows:
        attempts = []
        for index in range(args.repeats):
            started = time.perf_counter()
            try:
                response = query(args.url, args.language, row["input"])
                words = response.get("Words")
                if not isinstance(words, list):
                    raise ValueError("response has no Words list")
                phones = [word.get("Phonetic") for word in words if isinstance(word, dict)]
                if len(phones) != len(words) or any(not isinstance(phone, str) for phone in phones):
                    raise ValueError("response contains missing/non-string Phonetic field")
                attempt = {"repeat_index": index + 1, "phonetic_output": " ".join(phones) if phones else None,
                           "word_outputs": phones, "randomization_words_count": response.get("RandomizationWordsCount"),
                           "randomization_words_choices": response.get("RandomizationWordsChoices"),
                           "elapsed_ms": round((time.perf_counter()-started)*1000, 3), "error": None}
            except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
                attempt = {"repeat_index": index + 1, "phonetic_output": None, "word_outputs": [],
                           "randomization_words_count": None, "randomization_words_choices": None,
                           "elapsed_ms": round((time.perf_counter()-started)*1000, 3),
                           "error": f"{type(exc).__name__}: {exc}"}
            attempts.append(attempt); all_attempts.append(attempt)
        cases.append(summarize_case(row["id"], row["input"], attempts))
    comparable = [c for c in cases if c["successful_nonempty_calls"] >= 2]
    variable = [c for c in comparable if c["varies_across_repetitions"]]
    report = {"schema_version":"1.0","engine":"Goruut","upstream_commit":GORUUT_COMMIT,"language":args.language,
              "input_count":len(rows),"repeats_per_input":args.repeats,"attempt_count":len(all_attempts),
              "successful_nonempty_calls":sum(bool(a.get("phonetic_output")) and a.get("error") is None for a in all_attempts),
              "no_output_calls":sum(a.get("phonetic_output") is None and a.get("error") is None for a in all_attempts),
              "error_calls":sum(a.get("error") is not None for a in all_attempts),
              "inputs_with_at_least_two_nonempty_outputs":len(comparable),"inputs_with_multiple_distinct_outputs":len(variable),
              "observed_repeatability_rate":1-len(variable)/len(comparable) if comparable else None,
              "interpretation":"Repeatability diagnostic only, not accuracy. Stable output can still be wrong; variable output requires investigation of homonyms/randomization and API configuration.",
              "cases":cases}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:report[k] for k in ("engine","upstream_commit","language","input_count","repeats_per_input","attempt_count","successful_nonempty_calls","no_output_calls","error_calls","inputs_with_at_least_two_nonempty_outputs","inputs_with_multiple_distinct_outputs","observed_repeatability_rate")},ensure_ascii=False,indent=2))
    print(f"Repeatability report: {args.output}")
    return 0 if report["successful_nonempty_calls"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
