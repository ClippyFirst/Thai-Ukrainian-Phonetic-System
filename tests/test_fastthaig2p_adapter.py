from __future__ import annotations

from thai_ukrainian.fastthaig2p_adapter import FastThaiG2POutput
from thai_ukrainian.ukrainian_adaptation import adapt_phonetic_result


def _output(syllable: str) -> FastThaiG2POutput:
    return FastThaiG2POutput(
        input_text="กา",
        raw_ipa=f"/{syllable}/",
        word_groups=(syllable,),
        syllable_ipa=(syllable,),
        token_paths=(),
        passthrough_text="",
    )


def test_external_ipa_is_not_mislabelled_as_phonemic_or_surface_ipa() -> None:
    result = _output("kʰaː˧").to_phonetic_results()[0][0]

    assert result.phonemic_ipa is None
    assert result.broad_surface_ipa is None
    assert result.external_ipa == "kʰaː"
    assert result.status == "PROVISIONAL"
    assert result.tone_contour_ipa == "˧"
    assert result.vowel_length == "long"


def test_provisional_external_ipa_flows_through_existing_ipa_to_ukrainian_adapter() -> None:
    result = _output("kʰaː˧").to_phonetic_results()[0][0]

    adapted = adapt_phonetic_result(result)

    assert adapted["status"] == "provisional"
    assert adapted["source_ipa"] == "kʰaː"
    assert adapted["output"] == "к'а"
    assert any("PROVISIONAL" in warning for warning in adapted["warnings"])


def test_unsupported_external_symbol_still_fails_closed() -> None:
    result = _output("za˧").to_phonetic_results()[0][0]

    assert result.status == "UNSUPPORTED"
    assert result.external_ipa is None
    assert adapt_phonetic_result(result)["status"] == "withheld"


def test_external_ipa_is_visible_in_typed_result_serialization() -> None:
    result = _output("kʰaː˧").to_phonetic_results()[0][0]

    assert result.as_dict()["external_ipa"] == "kʰaː"


@pytest.mark.parametrize(
    ("syllable", "expected_ukrainian"),
    [
        # Published FastThaiG2P examples cover unreleased codas, non-syllabic
        # diphthong markers, Chao tones, and tied affricates.
        ("dɔːk̚˨˩", "док"),
        ("bia̯˥˩", "біа"),
        ("t͡ɕut̚˨˩", "чут"),
        ("pɤː˧", "пе"),
    ],
)
def test_upstream_documented_ipa_conventions_reach_ukrainian_adapter(
    syllable: str, expected_ukrainian: str
) -> None:
    result = _output(syllable).to_phonetic_results()[0][0]

    assert result.status == "PROVISIONAL"
    assert result.external_ipa
    assert result.tone_contour_ipa
    adapted = adapt_phonetic_result(result)
    assert adapted["status"] == "provisional"
    assert adapted["output"] == expected_ukrainian
