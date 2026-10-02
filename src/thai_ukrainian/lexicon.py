from __future__ import annotations
import csv
from pathlib import Path

def load_lexicon(path: str | Path) -> dict[str, list[str]]:
    path = Path(path)
    result: dict[str, list[str]] = {}
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            word = row["word"].strip()
            syllables = [x for x in row["syllables"].split("|") if x]
            if word and syllables:
                result[word] = syllables
    return result

def segment_word(word: str, lexicon: dict[str, list[str]]) -> list[str]:
    if word not in lexicon:
        raise KeyError(f"No lexicon entry for {word!r}; explicit segmentation is required.")
    return list(lexicon[word])

def segment_text(words: list[str], lexicon: dict[str, list[str]]) -> list[list[str]]:
    return [segment_word(word, lexicon) for word in words]
