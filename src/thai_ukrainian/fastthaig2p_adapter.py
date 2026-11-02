"""Optional adapter for the pinned FastThaiG2P Python engine.

Importing this module does not import FastThaiG2P. Construct the adapter only
inside an optional benchmark/runtime that has installed the extra dependency.
The returned result is raw external IPA, not ClippyFirst's typed PhoneticResult.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

UPSTREAM_COMMIT = "4e82a291b4cf2876326744c6580121e9986ad354"
_WORD_IPA = re.compile(r"/([^/]+)/")


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
        """True only when all non-whitespace output is slash-delimited IPA."""
        return bool(self.syllable_ipa) and not self.passthrough_text

    @property
    def dictionary_hit_count(self) -> int:
        return sum(path.path == "dictionary" for path in self.token_paths)

    @property
    def oov_rule_fallback_count(self) -> int:
        return sum(path.path == "rule_fallback" for path in self.token_paths)


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
        groups = tuple(match.group(1).strip() for match in _WORD_IPA.finditer(raw))
        syllables = tuple(
            part for group in groups for part in group.split(".") if part
        )
        passthrough = _WORD_IPA.sub("", raw).strip()
        return FastThaiG2POutput(
            input_text=text,
            raw_ipa=raw,
            word_groups=groups,
            syllable_ipa=syllables,
            token_paths=paths,
            passthrough_text=passthrough,
        )
