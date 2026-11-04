from __future__ import annotations

import sys
from pathlib import Path

import pytest
pytest.importorskip("fastapi")
from fastapi import HTTPException

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import index as site_api  # noqa: E402
from thai_ukrainian.fastthaig2p_adapter import FastThaiG2POutput, FastThaiG2PTokenPath  # noqa: E402


class FakeFastThaiG2P:
    def __init__(self, output: FastThaiG2POutput) -> None:
        self.output = output
        self.seen: list[str] = []

    def convert(self, text: str) -> FastThaiG2POutput:
        self.seen.append(text)
        return self.output


def _output(*, passthrough: str = "") -> FastThaiG2POutput:
    return FastThaiG2POutput(
        input_text="กา",
        raw_ipa="/kʰaː˧/",
        word_groups=("kʰaː˧",),
        syllable_ipa=("kʰaː˧",),
        token_paths=(FastThaiG2PTokenPath(token="กา", path="dictionary"),),
        passthrough_text=passthrough,
    )


def test_api_uses_only_fastthaig2p_and_returns_provisional_ua() -> None:
    engine = FakeFastThaiG2P(_output())
    site_api._engine = engine

    result = site_api.analyze_with_fastthaig2p("กา")

    assert engine.seen == ["กา"]
    assert result["engine"] == "FastThaiG2P"
    assert result["status"] == "provisional"
    assert result["raw_ipa"] == "/kʰaː˧/"
    assert result["ukrainian"] == "к'а"
    assert result["words"][0]["thai"] == "กา"
    assert result["words"][0]["syllables"][0]["adaptation_status"] == "provisional"
    assert result["words"][0]["syllables"][0]["ipa"] == "kʰaː"


def test_api_refuses_partial_external_output_without_fallback() -> None:
    site_api._engine = FakeFastThaiG2P(_output(passthrough="unsupported"))

    with pytest.raises(HTTPException) as caught:
        site_api.analyze_with_fastthaig2p("กา")

    assert caught.value.status_code == 422
    assert caught.value.detail["code"] == "incomplete_ipa"
    assert "іншим рушієм" in caught.value.detail["message"]


def test_api_health_identifies_the_single_engine() -> None:
    assert site_api.health() == {"status": "ok", "engine": "FastThaiG2P"}

def test_pinned_fastthaig2p_engine_returns_complete_bangkok_ipa() -> None:
    from thai_ukrainian.fastthaig2p_adapter import FastThaiG2PAdapter

    output = FastThaiG2PAdapter().convert("กรุงเทพมหานคร")

    assert output.complete_ipa
    assert output.word_groups
    assert output.syllable_ipa
    assert all(result.external_ipa for group in output.to_phonetic_results() for result in group)

def test_fastapi_app_registers_same_origin_api_and_static_routes() -> None:
    routes = {route.path for route in site_api.app.routes}

    assert "/api/health" in routes
    assert "/api/analyze" in routes
    assert "" in routes, "the root static mount is registered at the empty path"


def test_pinned_fastthaig2p_contains_merged_suan_ipa_correction() -> None:
    """Protect the upstream-merged correction for สวน against regression."""
    from thai_ukrainian.fastthaig2p_adapter import FastThaiG2PAdapter

    output = FastThaiG2PAdapter().convert("สวน")

    # Upstream PR #3 was merged as the exact FastThaiG2P pin used by this site.
    # It replaces the incorrect three-syllable "sawana" form with /sua̯n˩˩˦/.
    assert output.raw_ipa == "/sua̯n˩˩˦/"
    typed = output.to_phonetic_results()[0][0]
    assert typed.external_ipa == "sua̯n"
    assert typed.tone_contour_ipa == "˩˩˦"
    assert typed.tone_category == "rising"
    assert typed.status == "PROVISIONAL"


def test_api_rejects_whitespace_only_input_before_calling_engine() -> None:
    engine = FakeFastThaiG2P(_output())
    site_api._engine = engine

    with pytest.raises(HTTPException) as caught:
        site_api.analyze(site_api.AnalyzeRequest(text=" \\t\\n "))

    assert caught.value.status_code == 400
    assert engine.seen == []


def test_api_request_schema_rejects_input_over_2000_characters() -> None:
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        site_api.AnalyzeRequest(text="ก" * 2001)
