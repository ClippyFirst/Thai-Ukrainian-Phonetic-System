#!/usr/bin/env python3
"""Build or verify the source-attested IPA → Ukrainian candidate registry.

The generated Ukrainian forms are outputs of the project's own adapter, not
independent native-speaker preferences or a Ukrainian gold standard.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "benchmark" / "source-attested-ipa.tsv"
OUTPUT = ROOT / "data" / "benchmark" / "ukrainian-target-candidates.tsv"
FIELDS = [
    "id", "thai", "source_ipa", "segmental_ipa", "tone_sequence",
    "vowel_length_note", "ua_candidate", "adapter_status", "rules_applied_json",
    "neutralized_features_json", "source_id", "source_url", "source_revision",
    "license", "candidate_status", "evidence_note",
]
TONE_MARKS = re.compile(r"[˥˦˧˨˩]")


def build_rows() -> list[dict[str, str]]:
    from thai_ukrainian.phonetic_result import PhoneticResult, _segment_ipa
    from thai_ukrainian.ukrainian_adaptation import adapt_phonetic_result

    with SOURCE.open("r", encoding="utf-8-sig", newline="") as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))
    rows: list[dict[str, str]] = []
    for source in source_rows:
        if source.get("status") != "SOURCE_ATTESTED_NOT_GOLD":
            raise ValueError(f"Unexpected IPA evidence grade for {source.get('id')!r}")
        raw_ipa = source["phonemic_ipa"].strip("/")
        segmental = TONE_MARKS.sub("", raw_ipa).replace("͡", "")
        provenance = (source["source_id"],)
        syllable_segments = [
            _segment_ipa(syllable, provenance)
            for syllable in segmental.split(".")
        ]
        segments = tuple(segment for group in syllable_segments for segment in group)
        if not segments or any(segment.certainty != "SUPPORTED" for segment in segments):
            raise ValueError(f"Unsupported IPA in source row {source['id']}: {segmental}")
        boundaries = [0]
        count = 0
        for group in syllable_segments:
            count += len(group)
            boundaries.append(count)
        phonetic = PhoneticResult(
            phonemic_ipa=segmental,
            broad_surface_ipa=None,
            segments=segments,
            syllable_boundaries=tuple(boundaries),
            vowel_length=source["vowel_length_note"],
            status="SUPPORTED",
            provenance=provenance,
        )
        adapted = adapt_phonetic_result(phonetic)
        if adapted["status"] != "adapted" or not adapted.get("output"):
            raise ValueError(f"IPA→UA adapter withheld candidate for {source['id']}: {adapted}")
        rows.append({
            "id": source["id"].replace("TH-SRC-IPA", "TH-UA-CANDIDATE"),
            "thai": source["thai"],
            "source_ipa": source["phonemic_ipa"],
            "segmental_ipa": segmental,
            "tone_sequence": source["tone_sequence"],
            "vowel_length_note": source["vowel_length_note"],
            "ua_candidate": adapted["output"],
            "adapter_status": adapted["status"],
            "rules_applied_json": json.dumps(adapted["rules_applied"], ensure_ascii=False, separators=(",", ":")),
            "neutralized_features_json": json.dumps(adapted.get("neutralized_features", []), ensure_ascii=False, separators=(",", ":")),
            "source_id": source["source_id"],
            "source_url": source["source_url"],
            "source_revision": source["source_revision"],
            "license": source["license"],
            "candidate_status": "ENGINE_CANDIDATE_NOT_PREFERENCE_GOLD",
            "evidence_note": "Generated from source-attested IPA through the project IPA→Ukrainian adapter; not independently adjudicated and not a target-preference gold form.",
        })
    return rows


def render() -> str:
    import io
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(build_rows())
    return stream.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="write the generated candidate registry")
    mode.add_argument("--check", action="store_true", help="verify the committed registry (default)")
    args = parser.parse_args()
    try:
        rows = build_rows()
        generated = render()
        if args.write:
            OUTPUT.write_text(generated, encoding="utf-8", newline="\n")
            print(f"Wrote {OUTPUT}")
            return 0
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != generated:
            print(f"ERROR: generated target candidates drifted; run {Path(__file__).name} --write", file=sys.stderr)
            return 1
        print(f"PASS: {len(rows)} engine-generated target candidates match the committed registry")
        return 0
    except (OSError, UnicodeError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
