#!/usr/bin/env python3
"""Extract pinned FastThaiG2P normalizer maps as browser data (no runtime Python)."""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

CONSTANTS = (
    "THAI_DIGITS", "THAI_NUMERAL_MAP", "LETTER_TO_THAI", "ABBREVIATIONS",
    "SYMBOLS", "ENGLISH_ABBREVS", "UNITS", "_EMAIL_WORDS",
)


def extract(source: Path) -> dict:
    path = source / "fastthaig2p" / "normalizer.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in CONSTANTS:
                    values[target.id] = ast.literal_eval(node.value)
    missing = set(CONSTANTS) - values.keys()
    if missing:
        raise SystemExit(f"Upstream normalizer constants changed: {sorted(missing)}")
    return {
        "schema_version": 1,
        "upstream_commit": "4e82a291b4cf2876326744c6580121e9986ad354",
        "THAI_DIGITS": values["THAI_DIGITS"],
        "THAI_NUMERAL_MAP": values["THAI_NUMERAL_MAP"],
        "LETTER_TO_THAI": values["LETTER_TO_THAI"],
        "ABBREVIATIONS": values["ABBREVIATIONS"],
        "SYMBOLS": values["SYMBOLS"],
        "ENGLISH_ABBREVS": values["ENGLISH_ABBREVS"],
        "UNITS": values["UNITS"],
        "EMAIL_WORDS": values["_EMAIL_WORDS"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    data = extract(args.source)
    data_path = args.source / "fastthaig2p" / "data" / "normalizer-data.json"
    data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")

    project = args.source / "pyproject.toml"
    project_text = project.read_text(encoding="utf-8")
    fallback = '"data/fallback" = "fastthaig2p/data/fallback"'
    include = '"data/normalizer-data.json" = "fastthaig2p/data/normalizer-data.json"'
    if include not in project_text:
        if fallback not in project_text:
            raise SystemExit("FastThaiG2P wheel force-include configuration changed")
        project_text = project_text.replace(fallback, fallback + "\\n" + include, 1)
        project.write_text(project_text, encoding="utf-8")
    print(json.dumps({"data_file": str(data_path), "map_count": len(CONSTANTS)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
