#!/usr/bin/env python3
from __future__ import annotations

import json
import sys

from thai_ukrainian.evaluation import evaluate_file


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: python scripts/evaluate_corpus.py RECORDS.jsonl", file=sys.stderr)
        return 2
    try:
        result = evaluate_file(argv[0])
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
