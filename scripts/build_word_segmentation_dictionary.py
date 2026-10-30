#!/usr/bin/env python3
"""Rebuild the pinned Thai word dictionary from its exact upstream snapshot."""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_GIT_BLOB_SHA1 = "093dda8a35646281e71a8a434137cb5fac57882e"
EXPECTED_ENTRIES = 60963
DEFAULT_OUTPUT = ROOT / "data" / "thai" / "words_th_cc0.txt"


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def transform(source: bytes) -> list[str]:
    if git_blob_sha1(source) != EXPECTED_GIT_BLOB_SHA1:
        raise ValueError(
            "Source does not match the pinned PyThaiNLP Git blob "
            f"{EXPECTED_GIT_BLOB_SHA1}; refusing to regenerate from changed data."
        )
    text = source.decode("utf-8")
    words: list[str] = []
    seen: set[str] = set()
    for line in text.splitlines():
        word = line.rstrip()
        if not word or any(not ("\u0e00" <= char <= "\u0e7f") for char in word):
            continue
        if word not in seen:
            seen.add(word)
            words.append(word)
    if len(words) != EXPECTED_ENTRIES:
        raise ValueError(f"Expected {EXPECTED_ENTRIES} entries, generated {len(words)}")
    return words


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="Exact upstream words_th.txt snapshot")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    try:
        words = transform(args.source.read_bytes())
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(words) + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {len(words)} unique Thai-block entries to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
