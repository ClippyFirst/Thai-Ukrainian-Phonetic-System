from __future__ import annotations
import csv
from pathlib import Path
from .models import ToneResult

ROOT = Path(__file__).resolve().parents[2]
RULES_PATH = ROOT / "data" / "thai" / "tone_rules.csv"
TONE_IPA = {"mid": "˧", "low": "˩", "falling": "˥˩", "high": "˥", "rising": "˩˥"}

def _load_rules():
    with RULES_PATH.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def classify_live_dead(vowel_length, coda_ipa, open_syllable=True):
    if coda_ipa in {"p", "t", "k", "ʔ"}:
        return "dead"
    if open_syllable and vowel_length == "short":
        return "dead"
    return "live"

def determine_tone(consonant_class, live_dead, vowel_length, tone_mark=None):
    mark = tone_mark or "none"
    for row in _load_rules():
        if row["tone_mark"] != mark or row["tone_class"] != consonant_class:
            continue
        if row["live_dead"] not in {"*", live_dead}:
            continue
        if row["vowel_length"] not in {"*", vowel_length}:
            continue
        return ToneResult(row["tone"], row["contour_ipa"], row["rule_id"], row["evidence_status"])
    if mark in {"mai_tri", "mai_chattawa"}:
        raise ValueError(f"{mark} is restricted to mid-class spellings in the standard rule system")
    raise ValueError(
        f"No declared tone rule for class={consonant_class}, live_dead={live_dead}, "
        f"vowel_length={vowel_length}, tone_mark={mark}"
    )
