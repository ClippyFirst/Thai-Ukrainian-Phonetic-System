from __future__ import annotations

import importlib.util
from pathlib import Path

from thai_ukrainian.fastthaig2p_adapter import parse_ipa_output

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "run_fastthaig2p_challenge.py"
SPEC = importlib.util.spec_from_file_location("fastthaig2p_challenge", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_parse_ipa_output_preserves_syllable_symbols_and_boundaries() -> None:
    raw = "/sa˨˩.wat̚˨˩.diː˧/ /kʰrap̚˦˥/"
    groups, syllables, passthrough = parse_ipa_output(raw)
    assert groups == ("sa˨˩.wat̚˨˩.diː˧", "kʰrap̚˦˥")
    assert syllables == ("sa˨˩", "wat̚˨˩", "diː˧", "kʰrap̚˦˥")
    assert passthrough == ""


def test_parse_ipa_output_does_not_invent_syllables() -> None:
    assert parse_ipa_output("unparsed output") == ((), (), "unparsed output")


def test_parse_ipa_output_detects_partial_fallback_passthrough() -> None:
    groups, syllables, passthrough = parse_ipa_output("/kaː˧/ ฦ")
    assert groups == ("kaː˧",)
    assert syllables == ("kaː˧",)
    assert passthrough == "ฦ"


def test_ipa_feature_inventory_counts_distinct_features() -> None:
    result = MODULE.summarize_ipa(["kʰaː˥˩", "t̚ɕʰaʔ"])
    assert result == {
        "syllable_count": 2,
        "tone_contour_codepoints": 2,
        "vowel_length_marks": 1,
        "aspiration_marks": 2,
        "unreleased_stop_marks": 1,
        "affricate_tie_bars": 0,
        "glottal_stops": 1,
    }


def test_segmental_projection_removes_only_notation_differences() -> None:
    assert MODULE.segmental_projection("t͡ɕʰaː˥˩") == "tɕʰaː"
    assert MODULE.segmental_projection("kʰaː8˧") == "kʰaː"
