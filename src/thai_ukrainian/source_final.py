from __future__ import annotations
import csv, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THAI = ROOT / "data" / "thai"
OUT = ROOT / "docs" / "source-final-manifest.json"

def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def _hash_rows(rows):
    payload = json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def build_manifest():
    consonants = _rows(THAI / "consonants.csv")
    vowels = _rows(THAI / "vowels.csv")
    phonotactics = _rows(THAI / "phonotactics.csv")
    tones = _rows(THAI / "tone_rules.csv")
    specials = _rows(THAI / "special_orthography.csv")
    manifest = {
        "status": "source-final-consistency",
        "sources": {
            "consonants": {"records": len(consonants), "sha256": _hash_rows(consonants)},
            "vowels": {"records": len(vowels), "sha256": _hash_rows(vowels)},
            "phonotactics": {"records": len(phonotactics), "sha256": _hash_rows(phonotactics)},
            "tone_rules": {"records": len(tones), "sha256": _hash_rows(tones)},
            "special_orthography": {"records": len(specials), "sha256": _hash_rows(specials)},
        },
        "invariants": {
            "consonant_graphemes": len(consonants) == 44,
            "vowel_records": len(vowels) == 40,
            "tone_rule_records": len(tones) == 15,
            "special_rule_records": len(specials) == 8,
            "tone_categories": 5,
            "coda_allowed": sum(r["coda_allowed"].strip().lower() == "true" for r in consonants) == 38,
        },
    }
    manifest["status"] = "pass" if all(manifest["invariants"].values()) else "fail"
    return manifest

if __name__ == "__main__":
    report = build_manifest()
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
