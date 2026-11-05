#!/usr/bin/env python3
"""Export explicitly selected orthographic TextGrid intervals as provenance-rich JSONL.

Only .TextGrid members are read from ZIP archives. Audio and all other members are
skipped; source labels are preserved verbatim and are not promoted to gold.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from collections import Counter
from pathlib import Path
from typing import Iterator

from thai_ukrainian.adapters.ccost import parse_textgrid_long

MAX_TEXTGRID_MEMBER_BYTES = 8 * 1024 * 1024
MAX_ARCHIVE_TEXTGRID_BYTES = 1024 * 1024 * 1024
MAX_COMPRESSION_RATIO = 1000

SOURCE_METADATA = {
    "CCOST textgrid.zip": {
        "source": "CCOST",
        "source_version": "Zenodo v1.0; DOI 10.5281/zenodo.17366698",
        "license": "CC-BY-NC-SA-4.0",
        "attribution": (
            "Pittayaporn, Yang, Jitwiriyanont, and Kirby (2026), "
            "The Chulalongkorn Corpus of Spoken Thai"
        ),
        "source_url": "https://zenodo.org/records/17366698",
    },
    "nectecLOTUSDIS textgrid.zip": {
        "source": "LOTUSDIS",
        "source_version": "Researcher-supplied TextGrid export; upstream snapshot not pinned",
        "license": "CC-BY-SA-4.0",
        "attribution": (
            "Tipaksorn, Thatphithakkul, Chunwijitra, and Thangthai (2025), LOTUSDIS"
        ),
        "source_url": "https://github.com/CAI-NECTEC/LOTUSDIS",
    },
}


def iter_textgrid_members(path: Path) -> Iterator[tuple[str, bytes]]:
    """Yield TextGrid bytes only; never extract or read non-TextGrid ZIP members."""
    if path.is_dir():
        for candidate in sorted(path.rglob("*")):
            if candidate.is_file() and candidate.suffix.lower() == ".textgrid":
                if candidate.stat().st_size > MAX_TEXTGRID_MEMBER_BYTES:
                    raise ValueError(f"TextGrid exceeds 8 MiB safety limit: {candidate}")
                yield str(candidate), candidate.read_bytes()
        return

    if path.suffix.lower() == ".textgrid":
        if path.stat().st_size > MAX_TEXTGRID_MEMBER_BYTES:
            raise ValueError(f"TextGrid exceeds 8 MiB safety limit: {path}")
        yield path.name, path.read_bytes()
        return

    if path.suffix.lower() != ".zip":
        raise ValueError(f"expected a .TextGrid file, directory, or ZIP archive: {path}")

    with zipfile.ZipFile(path) as archive:
        members = [item for item in archive.infolist() if not item.is_dir()]
        selected = [
            item for item in members if Path(item.filename).suffix.lower() == ".textgrid"
        ]
        total_size = sum(item.file_size for item in selected)
        if total_size > MAX_ARCHIVE_TEXTGRID_BYTES:
            raise ValueError(
                f"aggregate TextGrid data exceeds 1 GiB safety limit: {path}"
            )
        for item in selected:
            if item.file_size > MAX_TEXTGRID_MEMBER_BYTES:
                raise ValueError(f"TextGrid member exceeds 8 MiB safety limit: {item.filename}")
            if item.compress_size and item.file_size / item.compress_size > MAX_COMPRESSION_RATIO:
                raise ValueError(
                    f"TextGrid member exceeds compression-ratio safety limit: {item.filename}"
                )
            yield f"{path.name}:{item.filename}", archive.read(item)


def source_metadata(path: Path) -> dict[str, str]:
    metadata = SOURCE_METADATA.get(path.name)
    if metadata is None:
        raise ValueError(
            f"no verified source/license metadata for {path.name!r}; "
            "add a source-specific record before exporting"
        )
    return metadata


def export_records(
    paths: list[Path],
    exact_tiers: set[str],
    tier_prefixes: tuple[str, ...],
) -> tuple[list[dict], dict]:
    if not exact_tiers and not tier_prefixes:
        raise ValueError("select at least one --tier or --tier-prefix")

    records: list[dict] = []
    files_seen = 0
    selected_tiers: Counter[str] = Counter()
    source_counts: Counter[str] = Counter()

    for path in paths:
        metadata = source_metadata(path)
        for member_name, raw in iter_textgrid_members(path):
            grid = parse_textgrid_long(raw.decode("utf-8-sig"))
            files_seen += 1
            for tier in grid.tiers:
                if tier.name not in exact_tiers and not tier.name.startswith(tier_prefixes):
                    continue
                if tier.kind != "IntervalTier":
                    raise ValueError(
                        f"selected tier is not an IntervalTier: {member_name}:{tier.name}"
                    )
                selected_tiers[tier.name] += 1
                for interval_index, interval in enumerate(tier.intervals):
                    if not interval.text.strip():
                        continue
                    identity = (
                        f"{metadata['source']}\0{member_name}\0{tier.name}\0{interval_index}"
                    )
                    record = {
                        "id": hashlib.sha256(identity.encode("utf-8")).hexdigest(),
                        "text": interval.text,
                        "start": interval.xmin,
                        "end": interval.xmax,
                        "source": metadata["source"],
                        "source_version": metadata["source_version"],
                        "source_file": member_name,
                        "tier": tier.name,
                        "interval_index": interval_index,
                        "annotation_role": (
                            "orthographic_transcript"
                            if tier.name in {"ORT-MAU", "TRN"}
                            or tier.name.startswith("Hijack_")
                            else "explicitly_selected_textgrid_tier"
                        ),
                        "license": metadata["license"],
                        "attribution": metadata["attribution"],
                        "source_url": metadata["source_url"],
                        "evidence_grade": "SOURCE_ANNOTATED_NOT_GOLD",
                    }
                    records.append(record)
                    source_counts[metadata["source"]] += 1

    summary = {
        "files_parsed": files_seen,
        "records_exported": len(records),
        "records_by_source": dict(sorted(source_counts.items())),
        "selected_tier_file_counts": dict(sorted(selected_tiers.items())),
        "audio_read": False,
        "gold_promoted": False,
    }
    return records, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument(
        "--tier",
        action="append",
        default=[],
        help="Exact tier name to export; may be repeated.",
    )
    parser.add_argument(
        "--tier-prefix",
        action="append",
        default=[],
        help="Tier-name prefix to export; may be repeated.",
    )
    parser.add_argument("--output", type=Path, required=True, help="Output JSONL path")
    args = parser.parse_args()

    records, summary = export_records(
        args.paths, set(args.tier), tuple(args.tier_prefix)
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as stream:
        for record in records:
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps({"output": str(args.output), **summary}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
