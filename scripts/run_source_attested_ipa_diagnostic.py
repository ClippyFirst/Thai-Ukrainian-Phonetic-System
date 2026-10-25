#!/usr/bin/env python3
"""Compare source-attested dictionary IPA with the current text pipeline.

This is a discrepancy/abstention diagnostic, not an accuracy benchmark: source
records are dictionary-attested, not independently adjudicated or acoustically
verified gold.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "benchmark" / "source-attested-ipa.tsv"
SOURCE_GRADE = "SOURCE_ATTESTED_NOT_GOLD"
TONE_MARKS = re.compile(r"[˥˦˧˨˩]")
CANONICAL_EQUIVALENTS = (("t͡ɕ", "tɕ"), ("d͡ʑ", "dʑ"))


def segmental_only(ipa: str) -> str:
    value = ipa.strip().strip("/")
    for old, new in CANONICAL_EQUIVALENTS:
        value = value.replace(old, new)
    return TONE_MARKS.sub("", value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("/tmp/source-attested-ipa-diagnostic.json"))
    args = parser.parse_args()

    from thai_ukrainian.text import analyze_text

    with SOURCE.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\\t"))
    if not rows:
        raise ValueError("Source-attested IPA registry is empty")

    results = []
    for row in rows:
        tokens = analyze_text(row["thai"])
        thai_token = next((token for token in tokens if token["kind"] == "thai"), None)
        syllables = thai_token.get("syllables", []) if thai_token else []
        complete = bool(syllables) and all(
            syllable.get("status") == "analyzed" and syllable.get("phonemic_ipa")
            for syllable in syllables
        )
        engine_ipa = ".".join(syllable["phonemic_ipa"] for syllable in syllables) if complete else None
        engine_tones = [
            syllable.get("tone", {}).get("tone") if isinstance(syllable.get("tone"), dict) else None
            for syllable in syllables
        ]
        source_tones = [item.strip() for item in row["tone_sequence"].split(",") if item.strip()]
        source_segmental = segmental_only(row["phonemic_ipa"])
        engine_segmental = segmental_only(engine_ipa) if engine_ipa else None
        segmental_match = (engine_segmental == source_segmental) if complete else None
        tone_match = (engine_tones == source_tones) if complete and all(engine_tones) else None
        if not complete:
            status = "WITHHELD_OR_INCOMPLETE"
        elif segmental_match and tone_match:
            status = "SOURCE_AGREEMENT_SEGMENTAL_AND_TONE"
        elif segmental_match:
            status = "SOURCE_AGREEMENT_SEGMENTAL_TONE_DIFFERENCE"
        else:
            status = "SOURCE_DISAGREEMENT_REQUIRES_REVIEW"
        results.append({
            "id": row["id"],
            "thai": row["thai"],
            "source_ipa": row["phonemic_ipa"],
            "source_segmental_ipa": source_segmental,
            "source_tone_sequence": source_tones,
            "source_vowel_length_note": row["vowel_length_note"],
            "source_revision": row["source_revision"],
            "source_status": row["status"],
            "engine_status": [syllable.get("status") for syllable in syllables],
            "engine_segmental_ipa": engine_segmental,
            "engine_tone_sequence": engine_tones,
            "segmental_match": segmental_match,
            "tone_match": tone_match,
            "diagnostic_status": status,
        })

    summary = {
        "source_records": len(rows),
        "complete_engine_outputs": sum(record["engine_segmental_ipa"] is not None for record in results),
        "withheld_or_incomplete": sum(record["engine_segmental_ipa"] is None for record in results),
        "segmental_agreements": sum(record["segmental_match"] is True for record in results),
        "tone_agreements": sum(record["tone_match"] is True for record in results),
        "accuracy_claimed": False,
    }
    report = {
        "schema_version": "1.0",
        "source_evidence_grade": SOURCE_GRADE,
        "evaluation_kind": "source_attested_dictionary_discrepancy_and_abstention_diagnostic",
        "method": {
            "normalization": "strip IPA slashes; canonicalize tied affricate notation t͡ɕ→tɕ and d͡ʑ→dʑ for segmental comparison; remove tone letters only from segmental comparison",
            "tone": "compare source tone categories with engine tone categories separately",
            "limitation": "dictionary source agreement is not independent expert adjudication or acoustic validation",
            "accuracy_claim": "none",
        },
        "summary": summary,
        "records": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
