"""Optional adapter for the pinned FastThaiG2P Python engine.

Importing this module does not import FastThaiG2P. Construct the adapter only
inside an optional benchmark/runtime that has installed the extra.
The returned result is raw external IPA, not ClippyFirst's typed PhoneticResult.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .phonetic_result import PhoneticResult

UPSTREAM_COMMIT = "4e82a291b4cf2876326744c6580121e9986ad354"
_WORD_IPA = re.compile(r"/([^/]+)/")
_TONE_CATEGORIES = {
    "˧": "mid",
    "˨˩": "low",
    "˥˩": "falling",
    "˦˥": "high",
    "˩˩˦": "rising",
}
_TONE_SUFFIX = re.compile(r"([˥˦˧˨˩]+)$")
_TIE_BARS = ("͡", "͜")


@dataclass(frozen=True)
class FastThaiG2PTokenPath:
    token: str
    path: str


@dataclass(frozen=True)
class FastThaiG2POutput:
    input_text: str
    raw_ipa: str
    word_groups: tuple[str, ...]
    syllable_ipa: tuple[str, ...]
    token_paths: tuple[FastThaiG2PTokenPath, ...]
    passthrough_text: str

    @property
    def complete_ipa(self) -> bool:
        """Require slash-delimited IPA and one source-token path per output word."""
        return (
            bool(self.syllable_ipa)
            and not self.passthrough_text
            and len(self.token_paths) == len(self.word_groups)
        )

    @property
    def dictionary_hit_count(self) -> int:
        return sum(path.path == "dictionary" for path in self.token_paths)

    @property
    def oov_rule_fallback_count(self) -> int:
        return sum(path.path == "rule_fallback" for path in self.token_paths)

    def to_phonetic_results(self) -> tuple[tuple["PhoneticResult", ...], ...]:
        """Return one typed diagnostic result per syllable, grouped by word.

        FastThaiG2P's IPA convention is not independently adjudicated as
        phonemic versus broad-surface IPA. Therefore this conversion preserves
        segment and tone metadata but deliberately leaves both IPA-layer
        strings unset and marks the result UNCERTAIN. The existing Ukrainian
        adapter consequently withholds output rather than promoting an
        unverified external transcription.
        """
        if not self.complete_ipa:
            raise ValueError("Cannot type-convert incomplete IPA or misaligned token paths")
        flattened = tuple(
            syllable
            for group in self.word_groups
            for syllable in group.split(".")
            if syllable
        )
        if flattened != self.syllable_ipa:
            raise ValueError("Word-group and syllable IPA inventories do not agree")

        return tuple(
            tuple(_typed_syllable_result(syllable) for syllable in group.split(".") if syllable)
            for group in self.word_groups
        )


def _typed_syllable_result(raw_syllable: str) -> "PhoneticResult":
    """Preserve external segment/tone features without claiming IPA layer."""
    from .phonetic_result import PhoneticResult, _segment_ipa

    match = _TONE_SUFFIX.search(raw_syllable)
    tone_contour = match.group(1) if match else None
    segmental = raw_syllable[:match.start()] if match else raw_syllable
    # FastThaiG2P uses both Unicode tie-bar forms for its affricates. The
    # project segment inventory stores the equivalent canonical tɕ sequence.
    for tie_bar in _TIE_BARS:
        segmental = segmental.replace(f"t{tie_bar}ɕ", "tɕ")

    provenance = (f"FastThaiG2P@{UPSTREAM_COMMIT}",)
    segments = tuple(_segment_ipa(segmental, provenance))
    unsupported = not segments or any(
        segment.certainty == "UNSUPPORTED" for segment in segments
    )
    uncertainty = [
        "FastThaiG2P output is not independently adjudicated phonetic gold.",
        "Its phonemic-versus-broad-surface status is not established; external IPA is kept separate from phonemic and broad-surface IPA fields.",
        "Ukrainian output is a provisional practical adaptation, not an expert-validated transcription.",
    ]
    if tone_contour and tone_contour not in _TONE_CATEGORIES:
        uncertainty.append("Unrecognized Chao tone contour retained without category mapping.")
    if not tone_contour:
        uncertainty.append("No terminal Chao tone contour was present in this syllable.")

    return PhoneticResult(
        phonemic_ipa=None,
        broad_surface_ipa=None,
        segments=segments,
        syllable_boundaries=(0, len(segments)) if segments else (0,),
        vowel_length="long" if "ː" in segmental else None,
        tone_category=_TONE_CATEGORIES.get(tone_contour or ""),
        tone_contour_ipa=tone_contour,
        status="UNSUPPORTED" if unsupported else "PROVISIONAL",
        provenance=provenance,
        uncertainty=tuple(uncertainty),
        external_ipa=segmental if not unsupported else None,
    )


def parse_ipa_output(raw: str) -> tuple[tuple[str, ...], tuple[str, ...], str]:
    """Parse slash/dot IPA while retaining any non-IPA passthrough text."""
    groups = tuple(match.group(1).strip() for match in _WORD_IPA.finditer(raw))
    syllables = tuple(part for group in groups for part in group.split(".") if part)
    passthrough = _WORD_IPA.sub("", raw).strip()
    return groups, syllables, passthrough


class FastThaiG2PAdapter:
    """Lazy optional wrapper around fastthaig2p.G2P at UPSTREAM_COMMIT."""

    def __init__(self) -> None:
        try:
            from fastthaig2p import G2P
            from fastthaig2p.normalizer import normalize
        except ImportError as exc:
            raise RuntimeError(
                "FastThaiG2P is optional; install the pinned upstream commit "
                f"{UPSTREAM_COMMIT}"
            ) from exc
        self._engine = G2P()
        self._normalize = normalize

    def convert(self, text: str) -> FastThaiG2POutput:
        if not isinstance(text, str):
            raise TypeError("FastThaiG2PAdapter.convert expects str")
        normalized = self._normalize(text)
        tokens = [
            token for token in self._engine._tokenizer.tokenize(normalized)
            if token.strip()
        ]
        paths = tuple(
            FastThaiG2PTokenPath(
                token=token,
                path="dictionary" if self._engine._ipa.get(token) else "rule_fallback",
            )
            for token in tokens
        )
        raw = self._engine.convert(text)
        groups, syllables, passthrough = parse_ipa_output(raw)
        return FastThaiG2POutput(
            input_text=text,
            raw_ipa=raw,
            word_groups=groups,
            syllable_ipa=syllables,
            token_paths=paths,
            passthrough_text=passthrough,
        )
