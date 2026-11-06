#!/usr/bin/env python3
"""Build a deterministic, browser-consumable data pack for the pinned TLTK OOV parser.

The runtime port remains JavaScript. This build-time extractor only decodes the
pinned CP874 text tables and Python pickle containers into source-auditable JSON,
then gzip-compresses the result for lazy same-origin delivery on an OOV request.
"""
from __future__ import annotations

import argparse
import ast
import gzip
import hashlib
import json
import pickle
from pathlib import Path
from typing import Any

FASTTHAIG2P_COMMIT = "4e82a291b4cf2876326744c6580121e9986ad354"
TLTK_COMMIT = "0cef4bcfbdd675f589783dd4134b87b9bb9fbb93"
# sylform_var.pkl is loaded by TLTK module initialisation but static call-graph
# inspection found no reads of SYLVAR from g2p() -> sylparse() -> wordparse().
# It is therefore provenance-verified separately but intentionally omitted
# from the browser OOV payload.
ASSET_NAMES = (
    "sylrule.lts",
    "thaisyl.dict",
    "PhSTrigram.sts",
    "sylseg.3g",
    "thdict",
)


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def read_cp874(path: Path) -> list[str]:
    return path.read_bytes().decode("cp874").splitlines()


def load_pickle(path: Path) -> Any:
    with path.open("rb") as source:
        return pickle.load(source)


def parse_syllable_patterns(path: Path) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for line_number, line in enumerate(read_cp874(path), 1):
        if not line or line.startswith("#"):
            continue
        fields = line.split(",")
        if len(fields) < 3:
            raise ValueError(f"{path}:{line_number}: expected at least three comma-separated fields")
        pattern, pronunciation, tone_flag = fields[:3]
        records.append({
            "pattern": pattern,
            "pronunciation": pronunciation,
            "tone_flag": tone_flag,
        })
    if not records:
        raise ValueError(f"No syllable patterns found in {path}")
    return records


def parse_syllable_dictionary(path: Path) -> list[list[str]]:
    records: list[list[str]] = []
    for line_number, line in enumerate(read_cp874(path), 1):
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t", 1)
        if len(fields) != 2:
            raise ValueError(f"{path}:{line_number}: expected syllable<TAB>pronunciation")
        records.append([fields[0], fields[1]])
    if not records:
        raise ValueError(f"No syllable dictionary records found in {path}")
    return records


def parse_phone_trigrams(path: Path) -> list[list[Any]]:
    records: list[list[Any]] = []
    for line_number, raw_line in enumerate(read_cp874(path), 1):
        line = raw_line.rstrip().replace("<w>", "|")
        if not line:
            continue
        try:
            encoded, count_text = line.rsplit("\t", 1)
            form_sequence, phone = encoded.split("/", 1)
            forms = form_sequence.split("-")
            if len(forms) != 3:
                raise ValueError("expected three syllable-form fields")
            count = float(count_text)
        except (ValueError, TypeError) as error:
            raise ValueError(f"{path}:{line_number}: invalid phone trigram row: {error}") from error
        records.append([forms[0], forms[1], forms[2], phone, count])
    if not records:
        raise ValueError(f"No phone trigram records found in {path}")
    return records


def parse_trigram_counts(path: Path) -> list[list[Any]]:
    value = load_pickle(path)
    if not isinstance(value, dict):
        raise TypeError(f"{path}: expected a pickled dictionary")
    records: list[list[Any]] = []
    for key, count in value.items():
        if not isinstance(key, tuple) or len(key) != 3:
            raise TypeError(f"{path}: expected three-part tuple keys, got {type(key).__name__}")
        if not all(isinstance(part, str) for part in key):
            raise TypeError(f"{path}: trigram key parts must be strings")
        if not isinstance(count, (int, float)):
            raise TypeError(f"{path}: trigram counts must be numeric")
        records.append([key[0], key[1], key[2], count])
    records.sort(key=lambda row: (row[0], row[1], row[2]))
    if not records:
        raise ValueError(f"No syllable trigram counts found in {path}")
    return records


def parse_word_dictionary(path: Path) -> list[str]:
    value = load_pickle(path)
    if isinstance(value, dict):
        words = value.keys()
    elif isinstance(value, (set, list, tuple)):
        words = value
    else:
        raise TypeError(f"{path}: expected a dictionary, set, list or tuple")
    normalized = sorted({word for word in words if isinstance(word, str) and word})
    if not normalized:
        raise ValueError(f"No string words found in {path}")
    return normalized


def parse_parser_constants(path: Path) -> dict[str, Any]:
    """Extract only literal pronunciation tables from the pinned BSD parser source."""
    module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    function = next(
        (node for node in module.body if isinstance(node, ast.FunctionDef) and node.name == "read_sylpattern"),
        None,
    )
    if function is None:
        raise ValueError(f"{path}: read_sylpattern() was not found")
    stable_base: dict[str, dict[str, str]] = {}
    allowed_clusters: dict[str, str] = {}
    english_abbreviations: list[str] | None = None
    for node in ast.walk(function):
        if not isinstance(node, ast.Assign):
            continue
        value = node.value
        for target in node.targets:
            if isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name):
                key = target.slice.value if isinstance(target.slice, ast.Constant) else None
                if target.value.id == "stable" and key in {"X", "Y"}:
                    stable_base[key] = ast.literal_eval(value)
                elif target.value.id == "AK" and isinstance(key, str):
                    allowed_clusters[key] = ast.literal_eval(value)
            elif isinstance(target, ast.Name) and target.id == "EngAbbr":
                english_abbreviations = ast.literal_eval(value)
    if set(stable_base) != {"X", "Y"} or not allowed_clusters or not english_abbreviations:
        raise ValueError(f"{path}: required stable/AK/EngAbbr literal tables were not extracted")
    return {
        "stable_base": stable_base,
        "stable_aliases": {
            "A": "X", "K": "X", "C": "X", "R": "X", "G": "X", "E": "X",
            "D": "Y", "Z": "Y", "H": "Y", "F": "Y",
        },
        "allowed_clusters": allowed_clusters,
        "english_abbreviations": english_abbreviations,
    }


def build(fallback_dir: Path, parser_source: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    source_files = {name: fallback_dir / name for name in ASSET_NAMES}
    missing = [str(path) for path in source_files.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing pinned TLTK fallback assets: " + ", ".join(missing))

    parser_constants = parse_parser_constants(parser_source)
    data = {
        "schema_version": 1,
        "parser_source_sha256": sha256(parser_source.read_bytes()),
        "parser_constants": parser_constants,
        "fastthaig2p_commit": FASTTHAIG2P_COMMIT,
        "tltk_source_commit": TLTK_COMMIT,
        "tltk_package_version": "1.9.1",
        "tltk_package_license": "BSD-3-Clause",
        "syllable_patterns": parse_syllable_patterns(source_files["sylrule.lts"]),
        "syllable_dictionary": parse_syllable_dictionary(source_files["thaisyl.dict"]),
        "phone_trigrams": parse_phone_trigrams(source_files["PhSTrigram.sts"]),
        "syllable_trigrams": parse_trigram_counts(source_files["sylseg.3g"]),
        "word_dictionary": parse_word_dictionary(source_files["thdict"]),
    }
    source_manifest = {
        name: {
            "size_bytes": source_files[name].stat().st_size,
            "sha256": sha256(source_files[name].read_bytes()),
        }
        for name in ASSET_NAMES
    }
    report = {
        "schema_version": 1,
        "fastthaig2p_commit": FASTTHAIG2P_COMMIT,
        "tltk_source_commit": TLTK_COMMIT,
        "tltk_package_version": "1.9.1",
        "tltk_package_license": "BSD-3-Clause",
        "source_assets": source_manifest,
        "excluded_assets": {
            "sylform_var.pkl": "Loaded by TLTK initial() but not read anywhere in the g2p() -> sylparse() -> wordparse() call path; excluded from the browser OOV data pack."
        },
        "record_counts": {
            "syllable_patterns": len(data["syllable_patterns"]),
            "syllable_dictionary": len(data["syllable_dictionary"]),
            "phone_trigrams": len(data["phone_trigrams"]),
            "syllable_trigrams": len(data["syllable_trigrams"]),
            "word_dictionary": len(data["word_dictionary"]),
            "allowed_cluster_initials": len(parser_constants["allowed_clusters"]),
            "english_abbreviations": len(parser_constants["english_abbreviations"]),
        },
        "note": (
            "Build-time pickle decoding only. Browser runtime receives JSON, "
            "never Python pickle or executable Python modules."
        ),
    }
    return data, report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fallback-dir", type=Path, required=True)
    parser.add_argument("--parser-source", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    data, report = build(args.fallback_dir, args.parser_source)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    compressed = gzip.compress(payload, compresslevel=9, mtime=0)
    manifest = {
        "schema_version": 1,
        "engine": "ClippyFirst browser-native TLTK OOV adapter data",
        "fastthaig2p_commit": FASTTHAIG2P_COMMIT,
        "tltk_source_commit": TLTK_COMMIT,
        "tltk_package_version": "1.9.1",
        "license": "BSD-3-Clause",
        "path": "tltk-oov-data.json.gz",
        "compressed_size_bytes": len(compressed),
        "compressed_sha256": sha256(compressed),
        "uncompressed_size_bytes": len(payload),
        "uncompressed_sha256": sha256(payload),
        "record_counts": report["record_counts"],
    }
    (args.output_dir / "tltk-oov-data.json.gz").write_bytes(compressed)
    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (args.output_dir / "source-provenance.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
