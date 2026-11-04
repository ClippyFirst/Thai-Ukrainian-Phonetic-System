from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from thai_ukrainian.fastthaig2p_adapter import FastThaiG2PAdapter  # noqa: E402
from thai_ukrainian.ukrainian_adaptation import adapt_phonetic_result  # noqa: E402

WEB_DIR = ROOT / "web"
app = FastAPI(title="Thai → Ukrainian · FastThaiG2P", version="0.1.0")
_engine: FastThaiG2PAdapter | None = None


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


def _get_engine() -> FastThaiG2PAdapter:
    global _engine
    if _engine is None:
        _engine = FastThaiG2PAdapter()
    return _engine


def analyze_with_fastthaig2p(text: str) -> dict[str, Any]:
    output = _get_engine().convert(text)
    if not output.complete_ipa:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "incomplete_ipa",
                "message": "FastThaiG2P не зміг повернути повний IPA для всього введення. "
                "Непідтримані фрагменти не будуть прочитані іншим рушієм.",
                "passthrough": output.passthrough_text,
            },
        )

    typed_groups = output.to_phonetic_results()
    if len(typed_groups) != len(output.word_groups):
        raise HTTPException(status_code=502, detail="FastThaiG2P returned inconsistent word groups.")

    words: list[dict[str, Any]] = []
    ukrainian_words: list[str] = []
    for word_ipa, typed_syllables in zip(output.word_groups, typed_groups):
        raw_syllables = tuple(part for part in word_ipa.split(".") if part)
        if len(raw_syllables) != len(typed_syllables):
            raise HTTPException(status_code=502, detail="FastThaiG2P returned inconsistent syllable groups.")
        syllables: list[dict[str, Any]] = []
        ukrainian_parts: list[str] = []
        for raw_ipa, typed in zip(raw_syllables, typed_syllables):
            adapted = adapt_phonetic_result(typed)
            syllables.append({
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
                "warnings": list(typed.uncertainty) + list(adapted.get("warnings", [])),
            })
            if adapted["output"] is None:
                ukrainian_parts.append(f"⟦НЕВИЗНАЧЕНО: {raw_ipa}⟧")
            else:
                ukrainian_parts.append(adapted["output"])
        ukrainian_word = "".join(ukrainian_parts)
        ukrainian_words.append(ukrainian_word)
        words.append({
            "fastthaig2p_ipa": word_ipa,
            "ukrainian": ukrainian_word,
            "syllables": syllables,
        })

    return {
        "input": text,
        "engine": "FastThaiG2P",
        "upstream_commit": "4e82a291b4cf2876326744c6580121e9986ad354",
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


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "engine": "FastThaiG2P"}


@app.post("/api/analyze")
def analyze(request: AnalyzeRequest) -> dict[str, Any]:
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Введіть тайський текст.")
    try:
        return analyze_with_fastthaig2p(request.text)
    except HTTPException:
        raise
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")
