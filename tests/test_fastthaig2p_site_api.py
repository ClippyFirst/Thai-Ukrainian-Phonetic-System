from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi import HTTPException

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import index as site_api  # noqa: E402
from thai_ukrainian.fastthaig2p_adapter import FastThaiG2POutput  # noqa: E402


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
        token_paths=(),
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
