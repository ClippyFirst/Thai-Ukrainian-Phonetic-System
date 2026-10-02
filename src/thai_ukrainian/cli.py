from __future__ import annotations

import argparse
import json
from pathlib import Path

from .batch import analyze_input, analyze_rows, load_batch, write_batch
from .server import serve


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="thai-ua",
        description="Thai → Ukrainian phonetic-graphemic research CLI.",
    )
    sub = parser.add_subparsers(dest="command")

    analyze = sub.add_parser("analyze", help="Analyze Thai text or a syllable.")
    analyze.add_argument("text", help="Thai text.")
    analyze.add_argument("--compact", action="store_true", help="Print compact JSON.")

    batch = sub.add_parser("batch", help="Analyze TXT, CSV/TSV or Excel input.")
    batch.add_argument("input", type=Path)
    batch.add_argument("-o", "--output", type=Path, required=True)
    batch.add_argument("-c", "--column", help="Input column for CSV/XLSX.")
    batch.add_argument("--sheet", help="Excel sheet name.")

    api = sub.add_parser("serve", help="Run the local JSON API.")
    api.add_argument("--host", default="127.0.0.1")
    api.add_argument("--port", type=int, default=8787)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "analyze":
        result = analyze_input(args.text)
        print(json.dumps(result, ensure_ascii=False, indent=None if args.compact else 2, default=str))
        return 0

    if args.command == "batch":
        rows = load_batch(args.input, args.column, args.sheet)
        results = analyze_rows(rows)
        write_batch(results, args.output)
        print(f"Processed {len(results)} rows -> {args.output}")
        return 0

    if args.command == "serve":
        serve(args.host, args.port)
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
