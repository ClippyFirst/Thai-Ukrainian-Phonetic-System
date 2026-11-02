from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from thai_ukrainian.fastthaig2p_adapter import (
    FastThaiG2POutput,
    parse_ipa_output,
)
from thai_ukrainian.ukrainian_adaptation import adapt_phonetic_result

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
    assert MODULE.segmental_projection("t͜ɕʰaː˥˩") == "tɕʰaː"
    assert MODULE.segmental_projection("kʰaː8˧") == "kʰaː"


def test_adapter_result_does_not_mark_passthrough_as_complete_ipa() -> None:
    result = FastThaiG2POutput(
        input_text="word",
        raw_ipa="/kaː˧/ ฦ",
        word_groups=("kaː˧",),
        syllable_ipa=("kaː˧",),
        token_paths=(),
        passthrough_text="ฦ",
    )
    assert not result.complete_ipa


def test_typed_results_preserve_word_syllable_tone_and_length_metadata() -> None:
    result = FastThaiG2POutput(
        input_text="สวัสดีครับ",
        raw_ipa="/sa˨˩.wat̚˨˩.diː˧/ /kʰrap̚˦˥/",
        word_groups=("sa˨˩.wat̚˨˩.diː˧", "kʰrap̚˦˥"),
        syllable_ipa=("sa˨˩", "wat̚˨˩", "diː˧", "kʰrap̚˦˥"),
        token_paths=(),
        passthrough_text="",
    )

    groups = result.to_phonetic_results()

    assert tuple(len(group) for group in groups) == (3, 1)
    first, second, third = groups[0]
    assert first.tone_category == "low"
    assert first.tone_contour_ipa == "˨˩"
    assert first.phonemic_ipa is None
    assert first.broad_surface_ipa is None
    assert first.status == "UNCERTAIN"
    assert second.segments[-1].ipa == "t̚"
    assert third.vowel_length == "long"
    assert third.tone_category == "mid"
    assert groups[1][0].tone_category == "high"
    assert groups[1][0].segments[0].ipa == "kʰ"


def test_typed_results_keep_affricate_and_diphthong_features() -> None:
    result = FastThaiG2POutput(
        input_text="",
        raw_ipa="/t͡ɕʰaː˧/ /bia̯˥˩/",
        word_groups=("t͡ɕʰaː˧", "bia̯˥˩"),
        syllable_ipa=("t͡ɕʰaː˧", "bia̯˥˩"),
        token_paths=(),
        passthrough_text="",
    )

    first, second = (group[0] for group in result.to_phonetic_results())
    assert first.segments[0].ipa == "tɕʰ"
    assert first.tone_contour_ipa == "˧"
    assert second.segments[-1].ipa == "a̯"
    assert second.tone_category == "falling"


def test_unknown_fallback_sentinel_is_not_promoted_to_ipa_or_ukrainian() -> None:
    result = FastThaiG2POutput(
        input_text="",
        raw_ipa="/kʰaː8˧/",
        word_groups=("kʰaː8˧",),
        syllable_ipa=("kʰaː8˧",),
        token_paths=(),
        passthrough_text="",
    )
    typed = result.to_phonetic_results()[0][0]

    assert typed.status == "UNSUPPORTED"
    assert any(segment.ipa == "8" and segment.certainty == "UNSUPPORTED"
               for segment in typed.segments)
    adapted = adapt_phonetic_result(typed)
    assert adapted["status"] == "withheld"
    assert adapted["output"] is None


def test_uncertain_external_ipa_never_enters_ukrainian_adapter() -> None:
    result = FastThaiG2POutput(
        input_text="",
        raw_ipa="/kʰaː˥˩/",
        word_groups=("kʰaː˥˩",),
        syllable_ipa=("kʰaː˥˩",),
        token_paths=(),
        passthrough_text="",
    )
    typed = result.to_phonetic_results()[0][0]
    adapted = adapt_phonetic_result(typed)

    assert typed.status == "UNCERTAIN"
    assert typed.phonemic_ipa is None
    assert adapted["status"] == "withheld"
    assert adapted["output"] is None


def test_partial_ipa_is_rejected_by_typed_conversion() -> None:
    result = FastThaiG2POutput(
        input_text="",
        raw_ipa="/kaː˧/ ฦ",
        word_groups=("kaː˧",),
        syllable_ipa=("kaː˧",),
        token_paths=(),
        passthrough_text="ฦ",
    )
    with pytest.raises(ValueError, match="incomplete IPA"):
        result.to_phonetic_results()
