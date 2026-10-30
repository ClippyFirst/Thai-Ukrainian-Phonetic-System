"""Conservative Thai word segmentation over a pinned lexical dictionary.

This module performs orthographic maximum matching only. It does not infer
pronunciation, syllable structure, IPA, or Ukrainian output.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path
from typing import Any


from ._paths import THAI_DATA_ROOT

_DICTIONARY_PATH = THAI_DATA_ROOT / "words_th_cc0.txt"
_MANIFEST_PATH = THAI_DATA_ROOT / "word-segmentation-dictionary-source.json"
_EXPECTED_ENTRIES = 60963
_END = object()
_PREPOSED_VOWELS = frozenset("เแโใไ")
_THAI_CONSONANTS = frozenset(chr(codepoint) for codepoint in range(0x0E01, 0x0E2F))
_THAI_COMBINING_MARKS = frozenset(
    chr(codepoint)
    for codepoint in (
        0x0E31,
        *range(0x0E34, 0x0E3B),
        *range(0x0E47, 0x0E4F),
    )
)


@dataclass(frozen=True)
class WordSegmentationResult:
    """A lossless word-segmentation result with explicit uncertainty."""

    tokens: tuple[str, ...]
    unknown_clusters: tuple[str, ...]
    complete: bool
    method: str = "clippyfirst-dictionary-max-match-v1"
    evidence_grade: str = "DICTIONARY_SEGMENTATION_NOT_PRONUNCIATION_GOLD"
    token_statuses: tuple[str, ...] = ()


def _is_thai_block_only(value: str) -> bool:
    return bool(value) and all("\u0e00" <= char <= "\u0e7f" for char in value)


def _grapheme_spans(text: str) -> tuple[tuple[int, int], ...]:
    """Return conservative Thai character-cluster spans.

    Preposed vowels are grouped with the following consonant. Combining marks
    are kept with their base so dictionary matching never splits a visible
    orthographic cluster. This is a boundary-safety approximation, not a full
    Unicode grapheme-break implementation.
    """
    spans: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        start = index
        char = text[index]
        if char in _PREPOSED_VOWELS and index + 1 < len(text) and text[index + 1] in _THAI_CONSONANTS:
            index += 2
            while index < len(text) and text[index] in _THAI_COMBINING_MARKS:
                index += 1
        elif char in _THAI_CONSONANTS:
            index += 1
            while index < len(text) and text[index] in _THAI_COMBINING_MARKS:
                index += 1
        else:
            index += 1
            while index < len(text) and text[index] in _THAI_COMBINING_MARKS:
                index += 1
        spans.append((start, index))
    return tuple(spans)


@lru_cache(maxsize=1)
def load_word_dictionary() -> tuple[str, ...]:
    """Load and validate the pinned, source-derived dictionary snapshot."""
    if not _DICTIONARY_PATH.is_file():
        raise FileNotFoundError(f"Pinned Thai word dictionary is missing: {_DICTIONARY_PATH}")
    manifest: dict[str, Any] = json.loads(_MANIFEST_PATH.read_text(encoding="utf-8"))
    words = tuple(_DICTIONARY_PATH.read_text(encoding="utf-8").splitlines())
    if len(words) != _EXPECTED_ENTRIES or len(words) != manifest.get("retained_unique_entries"):
        raise ValueError(
            f"Thai dictionary count mismatch: expected {_EXPECTED_ENTRIES}, found {len(words)}"
        )
    if len(set(words)) != len(words):
        raise ValueError("Thai dictionary contains duplicate entries")
    if not all(_is_thai_block_only(word) for word in words):
        raise ValueError("Thai dictionary contains an empty or non-Thai-block entry")
    if manifest.get("license") != "CC0-1.0":
        raise ValueError("Thai dictionary manifest does not identify the expected CC0-1.0 data license")
    return words


@lru_cache(maxsize=1)
def _dictionary_trie() -> dict:
    root: dict = {}
    for word in load_word_dictionary():
        node = root
        for char in word:
            node = node.setdefault(char, {})
        node[_END] = True
    return root


def dictionary_word_segmentation(text: str) -> WordSegmentationResult:
    """Segment a contiguous text span by longest dictionary match.

    A token is emitted only when it matches a pinned dictionary entry and ends
    at a Thai-cluster boundary. Unknown clusters are preserved verbatim and
    returned separately; no characters are silently deleted.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not text:
        return WordSegmentationResult(tokens=(), unknown_clusters=(), complete=True, token_statuses=())

    spans = _grapheme_spans(text)
    boundaries = {0, *(end for _, end in spans)}
    span_end_by_start = {start: end for start, end in spans}
    trie = _dictionary_trie()
    tokens: list[str] = []
    unknown: list[str] = []
    token_statuses: list[str] = []
    position = 0

    while position < len(text):
        node = trie
        cursor = position
        best_end: int | None = None
        while cursor < len(text) and text[cursor] in node:
            node = node[text[cursor]]
            cursor += 1
            if _END in node and cursor in boundaries:
                best_end = cursor
        if best_end is not None:
            tokens.append(text[position:best_end])
            token_statuses.append("dictionary_match")
            position = best_end
            continue

        next_end = span_end_by_start[position]
        cluster = text[position:next_end]
        tokens.append(cluster)
        unknown.append(cluster)
        token_statuses.append("unknown_cluster_fallback")
        position = next_end

    return WordSegmentationResult(
        tokens=tuple(tokens),
        unknown_clusters=tuple(unknown),
        complete=not unknown,
        token_statuses=tuple(token_statuses),
    )


def segment_text_preserving(text: str) -> tuple[str, ...]:
    """Segment Thai spans while preserving every character of mixed text.

    Unlike the display-oriented text tokenizer, this scanner retains leading,
    trailing, and internal whitespace as explicit tokens. Only ordinary Thai
    spans are passed to dictionary maximum matching; all other runs are copied
    verbatim. The returned tokens concatenate exactly to the original input.
    """
    if not text:
        return ()
    from .text import _kind

    output: list[str] = []
    start = 0
    previous_kind = _kind(text[0])
    for index, char in enumerate(text[1:], 1):
        kind = _kind(char)
        if kind != previous_kind:
            chunk = text[start:index]
            if previous_kind == "thai":
                output.extend(dictionary_word_segmentation(chunk).tokens)
            else:
                output.append(chunk)
            start = index
            previous_kind = kind
    chunk = text[start:]
    if previous_kind == "thai":
        output.extend(dictionary_word_segmentation(chunk).tokens)
    else:
        output.append(chunk)
    if "".join(output) != text:
        raise AssertionError("Segmentation must preserve the input text exactly")
    return tuple(output)
