from __future__ import annotations
import csv, json
from pathlib import Path
from .orthography import VOWEL_SIGNATURES, SIGNATURES, GLIDE_PATTERNS, TONE_MARKS
from .inventory import load_consonants

ROOT = Path(__file__).resolve().parents[2]
THAI = ROOT / "data" / "thai"
OUT = ROOT / "docs" / "source-final-manifest.json"

def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def _declared_vowel_ids():
    ids = {row[2] for row in VOWEL_SIGNATURES.values()}
    ids.update(row[2] for row in SIGNATURES.values() if row[2])
    ids.update(row[3] for row in GLIDE_PATTERNS)
    return ids

def build_manifest():
    consonants = _rows(THAI / "consonants.csv")
    vowels = _rows(THAI / "vowels.csv")
    phonotactics = _rows(THAI / "phonotactics.csv")
    tones = _rows(THAI / "tone_rules.csv")
    specials = _rows(THAI / "special_orthography.csv")
    vowel_source_ids = {r["id"] for r in vowels}
    vowel_parser_ids = _declared_vowel_ids()
    invariants = {
        "consonant_graphemes_exactly_44": len(consonants) == 44,
        "consonant_graphemes_unique": len({r["grapheme"] for r in consonants}) == 44,
        "vowel_records_exactly_41": len(vowels) == 41,
        "vowel_ids_unique": len(vowel_source_ids) == 41,
        "vowel_ids_match_parser_registry": vowel_source_ids == vowel_parser_ids,
        "tone_rule_records": len(tones) == 15,
        "tone_marks_match_parser": {r["tone_mark"] for r in tones if r["tone_mark"] != "none"} == set(TONE_MARKS.values()),
        "special_rules_unique": len({r["rule_id"] for r in specials}) == len(specials),
        "coda_allowed_exactly_38": sum(r["coda_allowed"].strip().lower() == "true" for r in consonants) == 38,
        "phonotactic_manifest_present": len(phonotactics) >= 5,
        "derived_syllable_space_formula": 44 * 41 * 38 * 5 + 44 * 41 * 5 == 351780,
    }
    return {
        "status": "pass" if all(invariants.values()) else "fail",
        "source_records": {
            "consonants": len(consonants),
            "vowels": len(vowels),
            "phonotactics": len(phonotactics),
            "tone_rules": len(tones),
            "special_orthography": len(specials),
        },
        "parser_registry": {
            "vowel_ids": len(vowel_parser_ids),
            "tone_marks": len(TONE_MARKS),
        },
        "derived_expectations": {
            "initial_graphemes": 44,
            "vowel_records": 41,
            "coda_graphemes": 38,
            "tone_mark_states": 5,
            "combined_structural_upper_bound": 351780,
        },
        "invariants": invariants,
    }

if __name__ == "__main__":
    report = build_manifest()
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
