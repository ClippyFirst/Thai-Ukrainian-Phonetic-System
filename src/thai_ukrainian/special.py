from __future__ import annotations
import csv
from functools import lru_cache

from ._paths import THAI_DATA_ROOT

PATH = THAI_DATA_ROOT / "special_orthography.csv"

@lru_cache(maxsize=1)
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
