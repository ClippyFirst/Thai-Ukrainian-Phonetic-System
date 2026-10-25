"""Typed, source-pinned lexical IPA overrides.

These records are source-attested dictionary evidence, not independently adjudicated
phonetic gold. Overrides feed the same PhoneticResult → Ukrainian adapter boundary
as ordinary analysis; they never render Ukrainian directly from Thai graphemes.
"""
from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path

from .models import SyllableAnalysis, ToneResult

ROOT = Path(__file__).resolve().parents[2]
OVERRIDES_PATH = ROOT / "data" / "thai" / "lexical_ipa_overrides.tsv"
FIELDS = (
    "word", "segmental_ipa", "tone_category", "tone_contour_ipa",
    "vowel_length", "source_id", "source_url", "source_revision",
    "license", "status",
)
ACTIVE_STATUS = "ACTIVE_SOURCE_ATTESTED_NOT_GOLD"
ALLOWED_TONES = {"mid", "low", "falling", "high", "rising"}
ALLOWED_LENGTHS = {"short", "long", "diphthong"}


@lru_cache(maxsize=1)
def load_lexical_ipa_overrides() -> dict[str, dict[str, str]]:
    if not OVERRIDES_PATH.exists():
        return {}
    with OVERRIDES_PATH.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\\t")
        missing = set(FIELDS) - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"Lexical IPA override file missing fields: {sorted(missing)}")
        result: dict[str, dict[str, str]] = {}
        for row in reader:
            word = (row.get("word") or "").strip()
            if not word:
                raise ValueError("Lexical IPA override has an empty word")
            if word in result:
                raise ValueError(f"Duplicate lexical IPA override for {word!r}")
            if row.get("status") != ACTIVE_STATUS:
                continue
            for field in ("segmental_ipa", "tone_category", "tone_contour_ipa",
                          "vowel_length", "source_id", "source_url",
                          "source_revision", "license"):
                if not (row.get(field) or "").strip():
                    raise ValueError(f"Active lexical IPA override {word!r} missing {field}")
            if row["tone_category"] not in ALLOWED_TONES:
                raise ValueError(f"Unsupported tone category for {word!r}")
            if row["vowel_length"] not in ALLOWED_LENGTHS:
                raise ValueError(f"Unsupported vowel length for {word!r}")
            if not row["source_url"].startswith("https://"):
                raise ValueError(f"Lexical IPA override {word!r} requires HTTPS provenance")
            if not row["source_revision"].isdigit():
                raise ValueError(f"Lexical IPA override {word!r} requires a pinned numeric revision")
            result[word] = {key: (value or "").strip() for key, value in row.items() if key}
    return result


def apply_lexical_ipa_override(analysis: SyllableAnalysis) -> bool:
    """Apply an exact-form override before typed IPA→Ukrainian adaptation."""
    record = load_lexical_ipa_overrides().get(analysis.normalized)
    if record is None:
        return False

    analysis.phonemic_ipa = record["segmental_ipa"]
    # The source provides a dictionary IPA transcription, not a separate
    # surface-phonetic transcription; do not fabricate one.
    analysis.phonetic_ipa = None
    analysis.vowel_length = record["vowel_length"]
    analysis.vowel = "ɤ" if record["word"] == "เงิน" else analysis.vowel
    analysis.tone = ToneResult(
        tone=record["tone_category"],
        contour_ipa=record["tone_contour_ipa"],
        rule_id="LEXICAL-IPA-OVERRIDE:" + record["source_id"],
        evidence_status="source-attested-not-gold",
    )
    analysis.status = "analyzed"
    analysis.sources.append(record["source_id"])
    rule = "LEXICAL-IPA-OVERRIDE:" + record["source_id"]
    if rule not in analysis.rules_applied:
        analysis.rules_applied.append(rule)
    warning = (
        "IPA is a source-attested lexical dictionary transcription, not independently "
        "adjudicated or acoustically verified gold."
    )
    if warning not in analysis.warnings:
        analysis.warnings.append(warning)
    return True
