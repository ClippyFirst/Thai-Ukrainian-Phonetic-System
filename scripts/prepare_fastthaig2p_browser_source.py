#!/usr/bin/env python3
"""Prepare a source-attributed FastThaiG2P dictionary for browser distribution.

The upstream runtime ipa.json merges Wiktionary, manually supplied and
model-generated entries. This build step keeps only entries whose upstream
ipa_metadata.json source is Wiktionary or manual. Model-generated entries
are excluded from the public browser wheel because their redistribution
provenance is not established. The custom tokenizer dictionary is reduced
to exactly the retained IPA keys; OOV words continue through the upstream
rule-based fallback.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ALLOWED_SOURCES = {"wiktionary", "manual"}


def prepare_source(source_dir: Path) -> dict[str, Any]:
    data_dir = source_dir / "data"
    dict_path = data_dir / "dict.txt"
    ipa_path = data_dir / "ipa.json"
    metadata_path = data_dir / "ipa_metadata.json"

    for path in (dict_path, ipa_path, metadata_path):
        if not path.is_file():
            raise SystemExit(f"Required FastThaiG2P provenance input is missing: {path}")

    original_words = dict_path.read_text(encoding="utf-8").splitlines()
    original_ipa = json.loads(ipa_path.read_text(encoding="utf-8"))
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    retained: dict[str, str] = {}
    source_counts: dict[str, int] = {}
    metadata_ipa_mismatches: list[str] = []
    for word, record in metadata.items():
        source = record.get("source", "missing")
        source_counts[source] = source_counts.get(source, 0) + 1
        if source not in ALLOWED_SOURCES:
            continue
        ipa = original_ipa.get(word)
        if not isinstance(ipa, str) or not ipa.startswith("/") or not ipa.endswith("/"):
            raise SystemExit(f"Invalid or missing source-attributed IPA for {word!r}")
        if record.get("ipa") != ipa:
            # Keep the current runtime IPA but disclose that the audit snapshot is stale.
            # The source label remains the only provenance gate; do not invent a new source.
            metadata_ipa_mismatches.append(word)
        retained[word] = ipa

    if not retained:
        raise SystemExit("No source-attributed FastThaiG2P IPA entries remain after filtering")

    retained_words = [word for word in original_words if word in retained]
    if len(retained_words) != len(retained) or set(retained_words) != set(retained):
        missing_words = sorted(set(retained) - set(retained_words))[:10]
        raise SystemExit(f"Retained IPA keys do not match the tokenizer dictionary: {missing_words}")

    # Keep upstream word ordering for reproducible tokenizer behavior.
    filtered_ipa = {word: retained[word] for word in retained_words}
    dict_path.write_text("\n".join(retained_words) + "\n", encoding="utf-8")
    ipa_path.write_text(
        json.dumps(filtered_ipa, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    retained_counts = {
        source: count for source, count in source_counts.items()
        if source in ALLOWED_SOURCES
    }
    excluded_counts = {
        source: count for source, count in source_counts.items()
        if source not in ALLOWED_SOURCES
    }
    return {
        "upstream_commit": "4e82a291b4cf2876326744c6580121e9986ad354",
        "policy": "retain source=wiktionary or source=manual; exclude generated and unknown",
        "source_counts_before_filter": dict(sorted(source_counts.items())),
        "retained_counts": dict(sorted(retained_counts.items())),
        "excluded_counts": dict(sorted(excluded_counts.items())),
        "retained_entries": len(retained),
        "retained_dictionary_words": len(retained_words),
        "metadata_ipa_mismatch_count": len(metadata_ipa_mismatches),
        "metadata_ipa_mismatch_examples": metadata_ipa_mismatches[:20],
        "fallback": "upstream TLTK-derived rule fallback remains enabled",
        "linguistic_accuracy": "NOT_MEASURED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    report = prepare_source(args.source)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
