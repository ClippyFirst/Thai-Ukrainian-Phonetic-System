from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "data" / "thai" / "special_orthography.csv"

def load_special_rules() -> list[dict[str, str]]:
    with PATH.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def detect_special_orthography(text: str) -> list[dict[str, str]]:
    rules = load_special_rules()
    out = []
    for rule in rules:
        pattern = rule["pattern"]
        if pattern == "์":
            if "์" in text:
                out.append(rule)
        elif pattern == "รร":
            if "รร" in text:
                out.append(rule)
        elif pattern == "ทร":
            if "ทร" in text:
                out.append(rule)
        elif pattern == "อย":
            if text.startswith("อย"):
                out.append(rule)
        elif pattern in text:
            out.append(rule)
    return out
