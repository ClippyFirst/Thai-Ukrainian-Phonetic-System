#!/usr/bin/env python3
"""Inspect text-only Praat TextGrid files, including TextGrid members inside ZIPs.

ZIP handling reads only the central directory and selected .TextGrid member bytes.
Other members (including WAV/audio) are listed by metadata only and never extracted,
opened, hashed, or copied.
"""
from __future__ import annotations

import argparse
import json
import zipfile
from collections import Counter
from pathlib import Path

from thai_ukrainian.adapters.ccost import CCOST_PHONETIC_TIERS, is_ccost_nonphonetic_label, parse_textgrid_long
from thai_ukrainian.adapters.xsampa import XSampaConversionError, convert_xsampa_label

TEXTGRID_SUFFIXES = (".textgrid",)
AUDIO_SUFFIXES = {".wav", ".wave", ".mp3", ".flac", ".ogg", ".m4a", ".aiff", ".aif"}
MAX_TEXTGRID_MEMBER_BYTES = 8 * 1024 * 1024
MAX_ARCHIVE_TEXTGRID_BYTES = 1024 * 1024 * 1024
MAX_COMPRESSION_RATIO = 1000


def inspect(paths: list[Path], sample_limit: int = 5) -> dict:
    files: list[dict] = []
    failures: list[dict] = []
    archives: list[dict] = []
    tier_counts: Counter[str] = Counter()
    converted_counts: Counter[str] = Counter()
    marker_counts: Counter[tuple[str, str]] = Counter()

    def inspect_text(name: str, raw: bytes) -> None:
        try:
            text = raw.decode("utf-8-sig")
            grid = parse_textgrid_long(text)
            entry = {"file": name, "duration": grid.xmax - grid.xmin, "tiers": {}}
            for tier in grid.tiers:
                labels = [item.text for item in tier.intervals if item.text.strip()]
                tier_counts[tier.name] += len(labels)
                entry["tiers"][tier.name] = {
                    "kind": tier.kind,
                    "interval_count": len(tier.intervals),
                    "nonempty_labels": len(labels),
                    "samples": labels[:sample_limit],
                }
                if tier.name in CCOST_PHONETIC_TIERS:
                    for interval in tier.intervals:
                        label = interval.text.strip()
                        if not label:
                            continue
                        if is_ccost_nonphonetic_label(label):
                            marker_counts[(tier.name, label)] += 1
                            continue
                        try:
                            convert_xsampa_label(label)
                            converted_counts[tier.name] += 1
                        except XSampaConversionError as exc:
                            failures.append({
                                "file": name,
                                "tier": tier.name,
                                "interval": [interval.xmin, interval.xmax],
                                "raw_label": label,
                                "error": str(exc),
                            })
            files.append(entry)
        except (UnicodeError, ValueError) as exc:
            failures.append({"file": name, "error": f"{type(exc).__name__}: {exc}"})

    for path in sorted(paths):
        if path.is_dir():
            for candidate in sorted(path.rglob("*")):
                if candidate.is_file() and candidate.suffix.lower() in TEXTGRID_SUFFIXES:
                    try:
                        inspect_text(str(candidate), candidate.read_bytes())
                    except OSError as exc:
                        failures.append({"file": str(candidate), "error": f"{type(exc).__name__}: {exc}"})
            continue
        if not path.is_file():
            failures.append({"file": str(path), "error": "path does not exist"})
            continue
        if not zipfile.is_zipfile(path):
            if path.suffix.lower() in TEXTGRID_SUFFIXES:
                try:
                    inspect_text(str(path), path.read_bytes())
                except OSError as exc:
                    failures.append({"file": str(path), "error": f"{type(exc).__name__}: {exc}"})
            else:
                failures.append({"file": str(path), "error": "expected a TextGrid file or ZIP archive"})
            continue

        archive_report = {
            "archive": path.name,
            "members_total": 0,
            "textgrid_member_count": 0,
            "textgrid_uncompressed_bytes": 0,
            "textgrid_members": [],
            "extension_counts": {},
            "non_textgrid_members_skipped": 0,
            "audio_members_skipped": 0,
        }
        try:
            with zipfile.ZipFile(path) as archive:
                members = [info for info in archive.infolist() if not info.is_dir()]
                textgrid_infos = [
                    info for info in members
                    if Path(info.filename).suffix.lower() in TEXTGRID_SUFFIXES
                ]
                extension_counts = Counter(
                    Path(info.filename).suffix.lower() or "[no extension]" for info in members
                )
                total_textgrid_bytes = sum(info.file_size for info in textgrid_infos)
                archive_report.update({
                    "members_total": len(members),
                    "textgrid_member_count": len(textgrid_infos),
                    "textgrid_uncompressed_bytes": total_textgrid_bytes,
                    "textgrid_members": [info.filename for info in textgrid_infos],
                    "extension_counts": dict(sorted(extension_counts.items())),
                    "non_textgrid_members_skipped": len(members) - len(textgrid_infos),
                    "audio_members_skipped": sum(
                        Path(info.filename).suffix.lower() in AUDIO_SUFFIXES for info in members
                    ),
                })
                if total_textgrid_bytes > MAX_ARCHIVE_TEXTGRID_BYTES:
                    failures.append({
                        "file": path.name,
                        "error": (
                            f"aggregate TextGrid data is {total_textgrid_bytes} bytes; "
                            f"limit is {MAX_ARCHIVE_TEXTGRID_BYTES} bytes"
                        ),
                    })
                    archives.append(archive_report)
                    continue

                for info in textgrid_infos:
                    if info.file_size > MAX_TEXTGRID_MEMBER_BYTES:
                        failures.append({
                            "file": f"{path.name}:{info.filename}",
                            "error": "TextGrid member exceeds 8 MiB safety limit",
                        })
                        continue
                    if info.compress_size and info.file_size / info.compress_size > MAX_COMPRESSION_RATIO:
                        failures.append({
                            "file": f"{path.name}:{info.filename}",
                            "error": "TextGrid member exceeds compression-ratio safety limit",
                        })
                        continue
                    try:
                        inspect_text(f"{path.name}:{info.filename}", archive.read(info))
                    except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
                        failures.append({
                            "file": f"{path.name}:{info.filename}",
                            "error": f"{type(exc).__name__}: {exc}",
                        })
        except (OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
            failures.append({"file": str(path), "error": f"{type(exc).__name__}: {exc}"})
        archives.append(archive_report)

    return {
        "schema_version": "1.2",
        "source": "researcher-supplied TextGrid text; non-TextGrid ZIP members were not read",
        "files_inspected": len(files),
        "files": files,
        "archives": archives,
        "tier_nonempty_label_counts": dict(sorted(tier_counts.items())),
        "converted_label_counts": dict(sorted(converted_counts.items())),
        "bracket_marker_counts": {
            f"{tier}:{label}": count
            for (tier, label), count in sorted(marker_counts.items())
        },
        "failures": failures,
        "limitations": [
            "TextGrid labels are source annotations, not independent project gold.",
            "ZIP inspection reads only .TextGrid members; audio members are skipped and never extracted or opened.",
            "Successful conversion does not establish released-tier completeness or linguistic correctness.",
            "Only Praat long-text TextGrid is supported; short/binary formats are rejected.",
            "Unknown X-SAMPA labels are reported and are not guessed.",
            "Unrecognized tier names are inventoried but are not assumed to be phonetic tiers.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="TextGrid file(s), ZIP archive(s), or directories")
    parser.add_argument("--sample-limit", type=int, default=5)
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    parser.add_argument("--quiet", action="store_true", help="Do not print the full JSON report")
    parser.add_argument("--report-only", action="store_true", help="Return success even when labels need review")
    args = parser.parse_args()
    if args.sample_limit < 0:
        parser.error("--sample-limit must be non-negative")
    report = inspect(args.paths, args.sample_limit)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    if not args.quiet:
        print(rendered, end="")
    return 0 if args.report_only or not report["failures"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
