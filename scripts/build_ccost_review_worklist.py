#!/usr/bin/env python3
"""Build a context-rich, blind review worklist from CCOST TextGrid labels.

Only .TextGrid ZIP members are opened. Audio and all other members are skipped.
The output preserves source labels and supplies interval context; it never
proposes or infers a correction.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

from thai_ukrainian.adapters.ccost import (
    is_ccost_nonphonetic_label,
    CCOST_PHONETIC_TIERS,
    TextGridInterval,
    TextGridTier,
    parse_textgrid_long,
)
from thai_ukrainian.adapters.xsampa import XSampaConversionError, convert_xsampa_label

UNRESOLVED_MARKERS = ("<P>", "<P:>", "<:p>", "<Fail>")
DOCUMENTED_MAUS_FAILURE_MARKERS = ("<notProcessedChunk>",)
AUDIO_SUFFIXES = {".wav", ".wave", ".mp3", ".flac", ".ogg", ".m4a", ".aiff", ".aif"}
MAX_TEXTGRID_MEMBER_BYTES = 8 * 1024 * 1024
MAX_ARCHIVE_TEXTGRID_BYTES = 1024 * 1024 * 1024
MAX_COMPRESSION_RATIO = 1000
MAX_CONTEXT_PER_TIER = 30

ANNOTATION_FIELDS = (
    "reviewer_id",
    "reviewer_qualification_ref",
    "reviewed_at",
    "decision",
    "proposed_xsampa",
    "evidence_note",
    "confidence",
    "abstain_reason",
    "adjudicator_id",
    "adjudicator_decision",
    "adjudicator_note",
)
CSV_FIELDS = (
    "issue_id",
    "event_group_id",
    "source_file",
    "tier",
    "start",
    "end",
    "raw_label",
    "issue_types",
    "markers",
    "known_failure_markers",
    "overlap_context",
    "neighbor_context",
    *ANNOTATION_FIELDS,
)


def _stable_id(*parts: str) -> str:
    payload = "\x1f".join(parts).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def _marker_counts(label: str) -> dict[str, int]:
    return {marker: label.count(marker) for marker in UNRESOLVED_MARKERS if marker in label}


def _known_failure_counts(label: str) -> dict[str, int]:
    return {marker: label.count(marker) for marker in DOCUMENTED_MAUS_FAILURE_MARKERS if marker in label}


def _interval_payload(tier: str, interval: TextGridInterval, relation: str) -> dict[str, Any]:
    return {
        "tier": tier,
        "start": round(interval.xmin, 6),
        "end": round(interval.xmax, 6),
        "label": interval.text,
        "relation": relation,
    }


def _context_for(
    tiers: tuple[TextGridTier, ...],
    target_tier: str,
    target: TextGridInterval,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    overlap: list[dict[str, Any]] = []
    neighbors: list[dict[str, Any]] = []
    for tier in tiers:
        if tier.kind != "IntervalTier":
            continue
        nonempty = [(index, item) for index, item in enumerate(tier.intervals) if item.text.strip()]
        if tier.name == target_tier:
            target_index = next(
                (index for index, item in nonempty if item is target),
                None,
            )
            if target_index is not None:
                positions = [index for index, _ in nonempty]
                position = positions.index(target_index)
                for relation, candidate_position in (
                    ("previous", position - 1),
                    ("next", position + 1),
                ):
                    if 0 <= candidate_position < len(nonempty):
                        _, item = nonempty[candidate_position]
                        neighbors.append(_interval_payload(tier.name, item, relation))
            continue
        matches = [
            item for _, item in nonempty
            if max(item.xmin, target.xmin) < min(item.xmax, target.xmax)
        ]
        for item in matches[:MAX_CONTEXT_PER_TIER]:
            exact = abs(item.xmin - target.xmin) <= 1e-9 and abs(item.xmax - target.xmax) <= 1e-9
            overlap.append(_interval_payload(tier.name, item, "exact_interval" if exact else "overlap"))
        if len(matches) > MAX_CONTEXT_PER_TIER:
            overlap.append({
                "tier": tier.name,
                "relation": "truncated",
                "omitted_intervals": len(matches) - MAX_CONTEXT_PER_TIER,
            })
    overlap.sort(key=lambda item: (item.get("tier", ""), item.get("start", -1), item.get("end", -1)))
    neighbors.sort(key=lambda item: (item["tier"], item["start"], item["relation"]))
    return overlap, neighbors


def build_worklist(paths: list[Path]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    archives: list[dict[str, Any]] = []
    marker_appearances: Counter[str] = Counter()
    known_failure_appearances: Counter[str] = Counter()
    phonetic_failures: Counter[str] = Counter()
    source_files = 0

    for archive_path in sorted(paths):
        if not archive_path.is_file() or not zipfile.is_zipfile(archive_path):
            raise ValueError(f"expected a readable ZIP archive: {archive_path}")
        archive_report = {
            "archive": archive_path.name,
            "members_total": 0,
            "textgrid_members": 0,
            "audio_members_skipped": 0,
            "non_textgrid_members_skipped": 0,
        }
        with zipfile.ZipFile(archive_path) as archive:
            members = [item for item in archive.infolist() if not item.is_dir()]
            textgrid_members = [
                item for item in members if Path(item.filename).suffix.lower() == ".textgrid"
            ]
            total_size = sum(item.file_size for item in textgrid_members)
            if total_size > MAX_ARCHIVE_TEXTGRID_BYTES:
                raise ValueError(f"TextGrid members exceed aggregate safety limit: {archive_path}")
            archive_report.update({
                "members_total": len(members),
                "textgrid_members": len(textgrid_members),
                "audio_members_skipped": sum(
                    Path(item.filename).suffix.lower() in AUDIO_SUFFIXES for item in members
                ),
                "non_textgrid_members_skipped": len(members) - len(textgrid_members),
            })
            for info in textgrid_members:
                if info.file_size > MAX_TEXTGRID_MEMBER_BYTES:
                    raise ValueError(f"TextGrid member exceeds 8 MiB safety limit: {info.filename}")
                if info.compress_size and info.file_size / info.compress_size > MAX_COMPRESSION_RATIO:
                    raise ValueError(f"TextGrid member exceeds compression-ratio safety limit: {info.filename}")
                source_file = f"{archive_path.name}:{info.filename}"
                raw = archive.read(info)
                grid = parse_textgrid_long(raw.decode("utf-8-sig"))
                source_files += 1
                for tier in grid.tiers:
                    if tier.kind != "IntervalTier":
                        continue
                    for interval in tier.intervals:
                        label = interval.text
                        if not label.strip():
                            continue
                        markers = _marker_counts(label)
                        known_failure_markers = _known_failure_counts(label)
                        marker_appearances.update(markers)
                        known_failure_appearances.update(known_failure_markers)
                        issue_types: list[str] = []
                        if markers:
                            issue_types.append("UNRESOLVED_MARKER")
                        if known_failure_markers:
                            issue_types.append("DOCUMENTED_MAUS_PROCESSING_FAILURE")
                        if (
                            tier.name in CCOST_PHONETIC_TIERS
                            and not is_ccost_nonphonetic_label(label)
                            and label not in DOCUMENTED_MAUS_FAILURE_MARKERS
                        ):
                            try:
                                convert_xsampa_label(label)
                            except XSampaConversionError:
                                phonetic_failures[tier.name] += 1
                                if "_8" in label:
                                    issue_types.append("UNDOCUMENTED_CCOST_TONE_SUFFIX_8")
                                else:
                                    issue_types.append("OTHER_UNSUPPORTED_XSAMPA")
                        if not issue_types:
                            continue
                        overlap, neighbors = _context_for(grid.tiers, tier.name, interval)
                        start = f"{interval.xmin:.9f}"
                        end = f"{interval.xmax:.9f}"
                        event_group_id = _stable_id(source_file, start, end)
                        issue_id = _stable_id(source_file, tier.name, start, end, label)
                        records.append({
                            "issue_id": issue_id,
                            "event_group_id": event_group_id,
                            "source_file": source_file,
                            "tier": tier.name,
                            "start": start,
                            "end": end,
                            "raw_label": label,
                            "issue_types": issue_types,
                            "markers": markers,
                            "known_failure_markers": known_failure_markers,
                            "overlap_context": overlap,
                            "neighbor_context": neighbors,
                            **{field: "" for field in ANNOTATION_FIELDS},
                        })
        archives.append(archive_report)

    records.sort(key=lambda row: (
        row["source_file"], float(row["start"]), float(row["end"]), row["tier"], row["raw_label"]
    ))
    tone_rows = [row for row in records if "UNDOCUMENTED_CCOST_TONE_SUFFIX_8" in row["issue_types"]]
    tone_events = {row["event_group_id"] for row in tone_rows}
    tone_label_events = {
        (row["source_file"], row["start"], row["end"], row["raw_label"]) for row in tone_rows
    }
    exact_interval_tone_counterparts: Counter[str] = Counter()
    exact_interval_tone_counterpart_groups: set[str] = set()
    mapped_tone_pattern = re.compile(r"_(1|2|3|4|5)(?![0-9])")
    for row in tone_rows:
        for item in row["overlap_context"]:
            if (
                item.get("relation") == "exact_interval"
                and item.get("tier") in CCOST_PHONETIC_TIERS
                and isinstance(item.get("label"), str)
                and "_8" not in item["label"]
            ):
                suffixes = set(mapped_tone_pattern.findall(item["label"]))
                if suffixes:
                    exact_interval_tone_counterpart_groups.add(row["event_group_id"])
                    for suffix in suffixes:
                        exact_interval_tone_counterparts[f"{item['tier']}:{suffix}"] += 1
    marker_rows = [row for row in records if "UNRESOLVED_MARKER" in row["issue_types"]]
    known_failure_rows = [row for row in records if "DOCUMENTED_MAUS_PROCESSING_FAILURE" in row["issue_types"]]
    marker_interval_counts: Counter[str] = Counter()
    for row in marker_rows:
        marker_interval_counts.update(row["markers"].keys())
    marker_event_groups = {
        marker: len({row["event_group_id"] for row in marker_rows if marker in row["markers"]})
        for marker in UNRESOLVED_MARKERS
    }
    summary = {
        "source_textgrid_files": source_files,
        "records": len(records),
        "phonetic_failure_occurrences_by_tier": dict(sorted(phonetic_failures.items())),
        "tone_suffix_8_occurrences": len(tone_rows),
        "tone_suffix_8_event_groups": len(tone_events),
        "tone_suffix_8_unique_raw_label_events": len(tone_label_events),
        "tone_suffix_8_distinct_raw_strings": len({row["raw_label"] for row in tone_rows}),
        "tone_suffix_8_files": len({row["source_file"] for row in tone_rows}),
        "tone_suffix_8_groups_with_exact_interval_mapped_tone_counterpart": len(exact_interval_tone_counterpart_groups),
        "tone_suffix_8_exact_interval_mapped_tone_counterparts_by_tier_suffix": dict(sorted(exact_interval_tone_counterparts.items())),
        "phonetic_failure_occurrences": sum(phonetic_failures.values()),
        "documented_maus_failure_marker_occurrences": sum(known_failure_appearances.values()),
        "documented_maus_failure_marker_interval_count": len(known_failure_rows),
        "documented_maus_failure_markers": dict(sorted(known_failure_appearances.items())),
        "unresolved_marker_interval_count": len(marker_rows),
        "marker_interval_counts": dict(sorted(marker_interval_counts.items())),
        "marker_event_group_counts": {
            marker: count for marker, count in sorted(marker_event_groups.items()) if count
        },
        "unresolved_marker_event_groups": len({row["event_group_id"] for row in marker_rows}),
        "unresolved_marker_appearances": sum(marker_appearances.values()),
        "markers": dict(sorted(marker_appearances.items())),
        "unique_raw_label_events": len({
            (row["source_file"], row["start"], row["end"], row["raw_label"])
            for row in records
        }),
        "audio_members_read": 0,
    }
    return {
        "schema_version": "1.0",
        "source_license": "CC-BY-NC-SA-4.0",
        "source_attribution": "Pittayaporn et al., The Chulalongkorn Corpus of Spoken Thai (CCOST), LREC 2026; DOI 10.5281/zenodo.17366698",
        "source_scope": "TextGrid labels only; no audio member is opened, extracted, hashed, or copied.",
        "policy": "Blind review worklist. Source labels are immutable; no correction or IPA value is inferred.",
        "archives": archives,
        "summary": summary,
        "records": records,
    }


def _write_tsv(path: Path, records: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in records:
            output = dict(row)
            for field in ("issue_types",):
                output[field] = ";".join(output[field])
            for field in ("markers", "known_failure_markers", "overlap_context", "neighbor_context"):
                output[field] = json.dumps(output[field], ensure_ascii=False, separators=(",", ":"))
            writer.writerow(output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archives", nargs="+", type=Path, help="CCOST ZIP archive(s)")
    parser.add_argument("--output", type=Path, required=True, help="Output TSV worklist path")
    parser.add_argument("--manifest", type=Path, help="Optional JSON summary and provenance manifest")
    args = parser.parse_args()
    report = build_worklist(args.archives)
    _write_tsv(args.output, report["records"])
    if args.manifest:
        args.manifest.write_text(
            json.dumps({key: value for key, value in report.items() if key != "records"}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
