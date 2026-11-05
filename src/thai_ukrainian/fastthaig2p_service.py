"""Pure FastThaiG2P analysis service shared by CPython API and browser/WASM."""
from __future__ import annotations

from typing import Any

from thai_ukrainian.fastthaig2p_adapter import FastThaiG2PAdapter
from thai_ukrainian.ukrainian_adaptation import adapt_phonetic_result

UPSTREAM_COMMIT = "4e82a291b4cf2876326744c6580121e9986ad354"
_engine: FastThaiG2PAdapter | None = None


class FastThaiG2PAnalysisError(ValueError):
    """Expected analysis rejection with an API-compatible status and detail."""

    def __init__(self, status_code: int, detail: Any) -> None:
        super().__init__(str(detail))
        self.status_code = status_code
        self.detail = detail


def _get_engine() -> FastThaiG2PAdapter:
    global _engine
    if _engine is None:
        _engine = FastThaiG2PAdapter()
    return _engine


def analyze_with_fastthaig2p(
    text: str,
    *,
    engine: FastThaiG2PAdapter | None = None,
) -> dict[str, Any]:
    """Return the shared, transport-neutral response used by API and browser."""
    if not text.strip():
        raise FastThaiG2PAnalysisError(400, "Введіть тайський текст.")

    output = (engine if engine is not None else _get_engine()).convert(text)
    if not output.complete_ipa:
        raise FastThaiG2PAnalysisError(
            422,
            {
                "code": "incomplete_ipa",
                "message": "FastThaiG2P не зміг повернути повний IPA для всього введення. "
                "Непідтримані фрагменти не будуть прочитані іншим рушієм.",
                "passthrough": output.passthrough_text,
            },
        )

    typed_groups = output.to_phonetic_results()
    if len(typed_groups) != len(output.word_groups):
        raise FastThaiG2PAnalysisError(
            502, "FastThaiG2P returned inconsistent word groups."
        )

    words: list[dict[str, Any]] = []
    ukrainian_words: list[str] = []
    for word_index, (word_ipa, typed_syllables) in enumerate(
        zip(output.word_groups, typed_groups)
    ):
        raw_syllables = tuple(part for part in word_ipa.split(".") if part)
        if len(raw_syllables) != len(typed_syllables):
            raise FastThaiG2PAnalysisError(
                502, "FastThaiG2P returned inconsistent syllable groups."
            )
        syllables: list[dict[str, Any]] = []
        ukrainian_parts: list[str] = []
        for raw_ipa, typed in zip(raw_syllables, typed_syllables):
            adapted = adapt_phonetic_result(typed)
            syllables.append(
                {
                    "ipa": typed.external_ipa,
                    "raw_ipa": raw_ipa,
                    "tone": typed.tone_category,
                    "tone_ipa": typed.tone_contour_ipa,
                    "vowel_length": typed.vowel_length,
                    "ukrainian": adapted["output"],
                    "adaptation_status": adapted["status"],
                    "rules_applied": adapted.get("rules_applied", []),
                    "neutralized_features": adapted.get("neutralized_features", []),
                    "provenance": list(typed.provenance),
                    "warnings": list(typed.uncertainty)
                    + list(adapted.get("warnings", [])),
                }
            )
            if adapted["output"] is None:
                ukrainian_parts.append(f"⟦НЕВИЗНАЧЕНО: {raw_ipa}⟧")
            else:
                ukrainian_parts.append(adapted["output"])
        ukrainian_word = "".join(ukrainian_parts)
        ukrainian_words.append(ukrainian_word)
        thai_token = (
            output.token_paths[word_index].token
            if word_index < len(output.token_paths)
            else None
        )
        words.append(
            {
                "thai": thai_token,
                "fastthaig2p_ipa": word_ipa,
                "ukrainian": ukrainian_word,
                "syllables": syllables,
            }
        )

    return {
        "input": text,
        "engine": "FastThaiG2P",
        "upstream_commit": UPSTREAM_COMMIT,
        "status": "provisional",
        "raw_ipa": output.raw_ipa,
        "ukrainian": " ".join(ukrainian_words),
        "words": words,
        "coverage": {
            "dictionary_tokens": output.dictionary_hit_count,
            "rule_fallback_tokens": output.oov_rule_fallback_count,
        },
        "warnings": [
            "Український запис є попередньою практичною адаптацією IPA, не підтвердженою незалежними фахівцями.",
            "FastThaiG2P IPA не класифіковано як фонемну або широку поверхневу IPA; сирий результат збережено окремо.",
            "Тони та довгота показані в IPA/метаданих, але не повністю відтворюються українськими літерами.",
        ],
    }
