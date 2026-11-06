#!/usr/bin/env python3
"""Find one pinned FastThaiG2P token that requires its OOV rule fallback.

This emits a reproducible browser fixture from the same filtered wheel and
upstream source used by the Pyodide compatibility workflow. It is runtime
parity evidence, not linguistic gold.
"""
from __future__ import annotations

import argparse
import json
import pickle
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = Path("build/FastThaiG2P")
sys.path.insert(0, str(UPSTREAM))
sys.path.insert(0, str(ROOT / "src"))

from thai_ukrainian.fastthaig2p_adapter import FastThaiG2PAdapter
from thai_ukrainian.fastthaig2p_service import analyze_with_fastthaig2p


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    fallback_dictionary_path = UPSTREAM / "data/fallback/thdict"
    if not fallback_dictionary_path.is_file():
        raise SystemExit(f"Pinned TLTK fallback dictionary is missing: {fallback_dictionary_path}")

    engine = FastThaiG2PAdapter()
    with fallback_dictionary_path.open("rb") as source:
        fallback_words = pickle.load(source)
    candidates = sorted(
        (
            word for word in fallback_words
            if isinstance(word, str)
            and len(word) >= 3
            and all("\\u0e00" <= char <= "\\u0e7f" for char in word)
        ),
        key=lambda word: (len(word), word),
    )
    for word in candidates[:5000]:
        word = word.strip()
        if not word or word in engine._engine._ipa:
            continue
        try:
            output = engine.convert(word)
            if not output.complete_ipa or output.oov_rule_fallback_count < 1:
                continue
            result = analyze_with_fastthaig2p(word, engine=engine)
        except (ValueError, RuntimeError):
            continue
        if result["coverage"]["rule_fallback_tokens"] < 1:
            continue
        payload = {
            "upstream_commit": "4e82a291b4cf2876326744c6580121e9986ad354",
            "input": word,
            "raw_ipa": result["raw_ipa"],
            "result": result,
            "dictionary_hit_count": output.dictionary_hit_count,
            "rule_fallback_count": output.oov_rule_fallback_count,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(json.dumps({
            "input": word,
            "raw_ipa": result["raw_ipa"],
            "rule_fallback_count": output.oov_rule_fallback_count,
        }, ensure_ascii=False))
        return

    raise SystemExit("Could not find a complete pinned OOV fallback fixture in the upstream wordlist.")


if __name__ == "__main__":
    main()
