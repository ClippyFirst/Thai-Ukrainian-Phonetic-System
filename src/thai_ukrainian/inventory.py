from pathlib import Path
import csv
from .models import Consonant

ROOT = Path(__file__).resolve().parents[2]

def load_consonants(path=None):
    path = Path(path or ROOT / "data" / "thai" / "consonants.csv")
    result = {}
    with path.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            result[r["grapheme"]] = Consonant(
                r["grapheme"], r["codepoint"], r["class"],
                r["onset_ipa"] or None, r["coda_ipa"] or None,
                r["coda_allowed"] == "true", r["notes"]
            )
    return result
