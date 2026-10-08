from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from .word import analyze_word

ROOT = Path(__file__).resolve().parents[2]
LEXICON_PATH = ROOT / "data" / "thai" / "text_lexicon.tsv"

THAI = re.compile(r"[\u0E00-\u0E7F]")
LATIN = re.compile(r"[A-Za-z]")
DIGIT = re.compile(r"[0-9\u0E50-\u0E59]")
THAI_MARKS = set("ฯๆ์")
PUNCT = set(".,!?;:/\\|()[]{}<>"'“”‘’—–-…%$€£₴฿")

@dataclass(frozen=True)
class TextToken:
    text: str
    kind: str
    syllables: tuple[str, ...] = ()
    segmentation: str = "none"

def load_text_lexicon() -> dict[str, tuple[str, ...]]:
    result: dict[str, tuple[str, ...]] = {}
    if not LEXICON_PATH.exists():
        return result
    for line in LEXICON_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        word, syllables = line.split("\t", 1)
        result[word] = tuple(x for x in syllables.split("|") if x)
    return result

LEXICON = load_text_lexicon()

def _kind(ch: str) -> str:
    if ch.isspace(): return "space"
    if ch in THAI_MARKS: return "thai_marker"
    if DIGIT.fullmatch(ch): return "number"
    if THAI.fullmatch(ch): return "thai"
    if LATIN.fullmatch(ch): return "latin"
    return "punctuation"

def tokenize_text(text: str) -> list[TextToken]:
    text = text.strip()
    if not text:
        return []
    out: list[TextToken] = []
    i = 0
    while i < len(text):
        kind = _kind(text[i])
        j = i + 1
        while j < len(text) and _kind(text[j]) == kind:
            j += 1
        chunk = text[i:j]
        if kind != "space":
            out.append(TextToken(chunk, kind))
        i = j
    return out

def _segment_explicit(token: str) -> tuple[str, ...] | None:
    parts = tuple(x for x in token.split() if x)
    return parts if len(parts) > 1 else None

def segment_thai_word(word: str) -> tuple[tuple[str, ...], str]:
    if word in LEXICON:
        return LEXICON[word], "lexicon"
    explicit = _segment_explicit(word)
    if explicit:
        return explicit, "explicit"
    return (word,), "unresolved"

def analyze_text(text: str):
    from .api import analyze_syllable
    tokens = tokenize_text(text)
    result = []
    for token in tokens:
        if token.kind == "thai":
            syllables, segmentation = segment_thai_word(token.text)
            analyses = [analyze_syllable(s) for s in syllables]
            if segmentation == "unresolved" and len(token.text) > 1:
                # Never invent a segmentation from raw grapheme clusters.
                # Preserve the current core behaviour while making the
                # uncertainty explicit at text level.
                result.append({
                    "input": token.text, "kind": "thai",
                    "segmentation_status": "unresolved",
                    "syllables": [a.as_dict() for a in analyses],
                    "warnings": ["No lexical segmentation is available for this Thai word; add a lexicon entry or provide explicit syllable boundaries."]
                })
            else:
                result.append({
                    "input": token.text, "kind": "thai",
                    "segmentation_status": segmentation,
                    "syllables": [a.as_dict() for a in analyses],
                    "warnings": []
                })
        else:
            result.append({"input": token.text, "kind": token.kind, "segmentation_status": "not_applicable", "syllables": [], "warnings": []})
    return result
