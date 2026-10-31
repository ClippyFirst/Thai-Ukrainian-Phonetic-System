from dataclasses import replace

from thai_ukrainian.api import analyze_syllable
from thai_ukrainian.phonetic_result import PhoneticResult
from thai_ukrainian.ukrainian_adaptation import adapt_phonetic_result
from thai_ukrainian.ua_orthography import candidates_for_phonetic_result
from thai_ukrainian.ua_orthography import candidates_for_ipa


def test_ukrainian_output_is_adapted_from_typed_ipa_result():
    for text, expected in [
        ("อา", "а"),
        ("อัน", "ан"),
        ("พอ", "п\u0027о"),
        ("ขอ", "к\u0027о"),
        ("งอ", "нго"),
        ("สอง", "сонг"),
    ]:
        analysis = analyze_syllable(text)
        result = PhoneticResult.from_syllable_analysis(analysis)
        assert analysis.ukrainian_transliteration == expected
        assert result.status == "SUPPORTED"
        assert adapt_phonetic_result(result)["output"] == expected


def test_glottal_carrier_has_no_independent_ukrainian_grapheme():
    result = PhoneticResult.from_syllable_analysis(analyze_syllable("อา"))
    assert result.phonemic_ipa == "ʔaː"
    assert adapt_phonetic_result(result)["output"] == "а"


def test_changing_ipa_changes_ukrainian_output_via_same_adapter():
    original = PhoneticResult.from_syllable_analysis(analyze_syllable("กา"))
    assert original.phonemic_ipa == "kaː"
    changed = replace(original, phonemic_ipa="paː")
    assert adapt_phonetic_result(original)["output"] == "ка"
    assert adapt_phonetic_result(changed)["output"] == "па"


def test_unsupported_ipa_is_withheld_instead_of_guessed():
    result = replace(
        PhoneticResult.from_syllable_analysis(analyze_syllable("กา")),
        phonemic_ipa="k☃a",
    )
    adapted = adapt_phonetic_result(result)
    assert adapted["status"] == "withheld"
    assert adapted["output"] is None


def test_unsupported_surface_ipa_invalidates_typed_result_and_withholds_target():
    analysis = replace(analyze_syllable("กา"), phonetic_ipa="k☃a")
    result = PhoneticResult.from_syllable_analysis(analysis)

    assert result.phonemic_ipa == "kaː"
    assert result.broad_surface_ipa == "k☃a"
    assert result.status == "UNSUPPORTED"
    adapted = adapt_phonetic_result(result)
    assert adapted["status"] == "withheld"
    assert adapted["output"] is None


def test_empty_surface_ipa_invalidates_typed_result_and_withholds_target():
    analysis = replace(analyze_syllable("กา"), phonetic_ipa="")
    result = PhoneticResult.from_syllable_analysis(analysis)

    assert result.phonemic_ipa == "kaː"
    assert result.broad_surface_ipa == ""
    assert result.status == "UNSUPPORTED"
    adapted = adapt_phonetic_result(result)
    assert adapted["status"] == "withheld"
    assert adapted["output"] is None


def test_tone_and_provenance_survive_in_typed_phonetic_result():
    result = PhoneticResult.from_syllable_analysis(analyze_syllable("ไกล"))
    assert result.tone_category == "mid"
    assert result.vowel_length is not None
    assert result.provenance
    # The pinned dictionary source attests segmental IPA and tone, not a
    # separate surface-phonetic transcription; absence must remain explicit.
    assert result.broad_surface_ipa is None
    assert result.segments
    assert all(segment.surface_ipa is None for segment in result.segments)
    assert any("not independently adjudicated or acoustically verified gold" in item
               for item in result.uncertainty)
    assert result.syllable_boundaries == (0, len(result.segments))



def test_common_external_thai_ipa_notation_is_normalized_before_adaptation():
    base = PhoneticResult.from_syllable_analysis(analyze_syllable("กา"))
    cases = [
        ("[kʰaː˩˩˦]", "к'а"),
        ("haː", "га"),
        ("kʰaː", "к'а"),
        ("pʰaː", "п'а"),
        ("tʰaː", "т'а"),
        ("tɕa", "ча"),
        ("tɕʰa", "ч'а"),
        ("/kʰaː/", "к'а"),
        ("kʰàː", "к'а"),
        ("ˈkʰaː", "к'а"),
        ("t͡ɕʰa˥", "ч'а"),
        ("t͜ɕʰa˦˥", "ч'а"),
        ("ŋɤːn˧", "нген"),
        ("k̚aː˧", "ка"),
    ]
    for ipa, expected in cases:
        adapted = adapt_phonetic_result(replace(base, phonemic_ipa=ipa))
        assert adapted["status"] == "adapted", ipa
        assert adapted["output"] == expected, ipa
        if ipa in {"tɕa", "tɕʰa"}:
            assert adapted["input_notes"] == [], ipa  # already canonical segmental IPA
        else:
            assert adapted["input_notes"], ipa
    h_result = adapt_phonetic_result(replace(base, phonemic_ipa="haː"))
    assert h_result["output"] == "га"
    assert "glottal place and voicing" in h_result["neutralized_features"]
    voiced_affricate = adapt_phonetic_result(replace(base, phonemic_ipa="dʒa"))
    assert voiced_affricate["status"] == "withheld"
    assert voiced_affricate["output"] is None


def test_tone_only_ipa_and_unknown_symbols_are_not_guessed():
    base = PhoneticResult.from_syllable_analysis(analyze_syllable("กา"))
    tone_only = adapt_phonetic_result(replace(base, phonemic_ipa="˥˩"))
    assert tone_only["status"] == "withheld"
    assert tone_only["output"] is None
    for malformed in ("[kʰaː/", "/kʰaː]", "[kʰaː", "kʰaː]"):
        result = adapt_phonetic_result(replace(base, phonemic_ipa=malformed))
        assert result["status"] == "withheld", malformed
        assert result["output"] is None, malformed
    unknown = adapt_phonetic_result(replace(base, phonemic_ipa="[kʰaː☃]"))
    assert unknown["status"] == "withheld"
    assert unknown["output"] is None


def test_ambiguous_breve_is_not_silently_discarded_as_tone():
    base = PhoneticResult.from_syllable_analysis(analyze_syllable("กา"))
    # U+0306 can mark extra-shortness; it is not safe to assume it is tone.
    adapted = adapt_phonetic_result(replace(base, phonemic_ipa="kʰă"))
    assert adapted["status"] == "withheld"
    assert adapted["output"] is None


def test_aspiration_is_marked_by_apostrophe_not_h_and_not_added_to_plain_stops():
    base = PhoneticResult.from_syllable_analysis(analyze_syllable("กา"))
    cases = [("ka", "ка"), ("kʰa", "к'а"), ("kʰra", "к'ра"),
             ("pa", "па"), ("pʰa", "п'а"), ("ta", "та"), ("tʰa", "т'а"),
             ("tɕa", "ча"), ("tɕʰa", "ч'а"), ("ha", "га"), ("ʔa", "а")]
    for ipa, expected in cases:
        adapted = adapt_phonetic_result(replace(base, phonemic_ipa=ipa))
        assert adapted["status"] == "adapted", ipa
        assert adapted["output"] == expected, ipa
    assert "aspiration" not in adapt_phonetic_result(replace(base, phonemic_ipa="kʰa")).get("neutralized_features", [])


def test_ipa_candidate_renderer_preserves_aspiration_with_apostrophe():
    assert candidates_for_ipa("ka") == ["ка"]
    assert candidates_for_ipa("kʰa") == ["к'а"]
    assert candidates_for_ipa("pʰa") == ["п'а"]
    assert candidates_for_ipa("tʰa") == ["т'а"]
    assert candidates_for_ipa("tɕa") == ["ча"]
    assert candidates_for_ipa("tɕʰa") == ["ч'а"]
    assert candidates_for_ipa("ha") == ["га"]


def test_secondary_orthography_candidates_require_supported_typed_ipa():
    result = PhoneticResult.from_syllable_analysis(analyze_syllable("กา"))
    assert candidates_for_phonetic_result(result) == ["ка"]
    assert candidates_for_phonetic_result(replace(result, status="UNCERTAIN")) == []
    assert candidates_for_phonetic_result(replace(result, status="UNSUPPORTED")) == []
    assert candidates_for_phonetic_result(replace(result, phonemic_ipa=None)) == []
    assert candidates_for_phonetic_result(replace(result, phonemic_ipa="k☃a")) == []


def test_api_routes_secondary_candidates_through_typed_phonetic_result(monkeypatch):
    import thai_ukrainian.api as api

    received = []

    def capture(result):
        received.append(result)
        return []

    monkeypatch.setattr(api, "candidates_for_phonetic_result", capture)
    api.analyze_syllable("กา")

    assert len(received) == 1
    assert isinstance(received[0], PhoneticResult)
    assert received[0].status == "SUPPORTED"
