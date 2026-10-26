from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from .word import analyze_word
from .lexical_ipa import load_lexical_ipa_overrides

ROOT = Path(__file__).resolve().parents[2]
LEXICON_PATH = ROOT / "data" / "thai" / "text_lexicon.tsv"

THAI = re.compile(r"[\u0E00-\u0E7F]")
LATIN = re.compile(r"[A-Za-z]")
DIGIT = re.compile(r"[0-9\u0E50-\u0E59]")
THAI_MARKS = set("ฯๆ")
PUNCT = set(".,!?;:/\\\\|()[]{}<>\\\"'“”‘’—–-…%$€£₴฿")

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
    if ch in " \t\r\n": return "space"
    if ch in THAI_MARKS: return "thai_marker"
    if DIGIT.fullmatch(ch): return "number"
    if THAI.fullmatch(ch): return "thai"
    if LATIN.fullmatch(ch): return "latin"
    return "punctuation"

def tokenize_text(text: str) -> list[TextToken]:
    text = text.strip(" \t\r\n")
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
    # A typed IPA override has precedence over graphemic syllabification: do
    # not let a generic lexicon entry mask a source-attested pronunciation.
    if word in load_lexical_ipa_overrides():
        return (word,), "lexical_ipa_override"
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
            if segmentation == "unresolved" and len(token.text) > 1:
                # A word-level phonetic analysis is not safe without lexical
                # segmentation: do not run the syllable engine on the whole
                # word and accidentally expose a partial/false pronunciation.
                result.append({
                    "input": token.text, "kind": "thai",
                    "segmentation_status": "unresolved",
                    "syllables": [],
                    "warnings": ["The conservative text endpoint does not apply automatic word segmentation; use analyze_text_with_word_segmentation for dictionary-based word boundaries. IPA and Ukrainian output are withheld until syllable segmentation and pronunciation are supported."]
                })
            else:
                analyses = [analyze_syllable(s) for s in syllables]
                result.append({
                    "input": token.text, "kind": "thai",
                    "segmentation_status": segmentation,
                    "syllables": [a.as_dict() for a in analyses],
                    "warnings": []
                })
        else:
            result.append({"input": token.text, "kind": token.kind, "segmentation_status": "not_applicable", "syllables": [], "warnings": []})
    return result


def analyze_text_with_word_segmentation(text: str):
    """Return lossless mixed-text tokens with explicit dictionary word boundaries.

    This opt-in path is separate from the conservative legacy endpoint. It
    records source character spans and unknown-cluster fallbacks; it does not
    treat a dictionary word boundary as evidence that the word's syllables or
    pronunciation are known.
    """
    from .segmentation import dictionary_word_segmentation

    if not text:
        return []
    result = []
    start = 0
    previous_kind = _kind(text[0])

    def emit(chunk: str, kind: str, offset: int) -> None:
        if kind != "thai":
            result.append({
                "input": chunk,
                "kind": kind,
                "segmentation_status": "not_applicable",
                "syllables": [],
                "warnings": [],
                "source_span": [offset, offset + len(chunk)],
                "word_segmentation_status": "not_applicable",
                "word_segmentation_method": None,
                "word_segmentation_complete": None,
                "word_segmentation_evidence_grade": None,
            })
            return

        segmented = dictionary_word_segmentation(chunk)
        local_offset = 0
        for word, word_status in zip(segmented.tokens, segmented.token_statuses):
            if word_status == "unknown_cluster_fallback":
                item = {
                    "input": word,
                    "kind": "thai",
                    "segmentation_status": "unresolved",
                    "syllables": [],
                    "warnings": ["Unknown grapheme cluster in dictionary segmentation; IPA and Ukrainian output are withheld."],
                }
            else:
                analysis = analyze_text(word)
                if len(analysis) != 1:
                    raise AssertionError("A single dictionary token must produce one conservative analysis")
                item = analysis[0].copy()
            item["source_span"] = [offset + local_offset, offset + local_offset + len(word)]
            item["source_run"] = chunk
            item["word_segmentation_status"] = word_status
            item["word_segmentation_method"] = segmented.method
            item["word_segmentation_complete"] = segmented.complete
            item["word_segmentation_evidence_grade"] = segmented.evidence_grade
            result.append(item)
            local_offset += len(word)
        if local_offset != len(chunk):
            raise AssertionError("Word tokens did not cover the Thai source run")

    for index, char in enumerate(text[1:], 1):
        kind = _kind(char)
        if kind != previous_kind:
            emit(text[start:index], previous_kind, start)
            start = index
            previous_kind = kind
    emit(text[start:], previous_kind, start)

    if "".join(item["input"] for item in result) != text:
        raise AssertionError("Word-segmented text analysis must preserve every input character")
    return result
