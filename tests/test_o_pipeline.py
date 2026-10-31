from thai_ukrainian.api import analyze_syllable
from thai_ukrainian.orthographic_rules import ORole, classify_o_role


def test_carrier_forms_have_glottal_only_in_ipa_audit():
    for thai, expected_ipa, expected_ua in (
        ("อา", "ʔaː", "а"),
        ("อัน", "ʔan", "ан"),
        ("อาย", "ʔaːj", "ай"),
    ):
        a = analyze_syllable(thai)
        assert a.status == "analyzed"
        assert a.orthographic_interpretations[0]["role"] == ORole.VOWEL_CARRIER.value
        assert a.phonemic_ipa == expected_ipa
        assert a.ukrainian_transliteration == expected_ua


def test_o_component_does_not_create_glottal_onset():
    for thai, expected_ipa, expected_ua in (
        ("พอ", "pʰɔː", "п\u0027о"),
        ("ขอ", "kʰɔː", "к\u0027о"),
        ("คอ", "kʰɔː", "к\u0027о"),
        ("งอ", "ŋɔː", "нго"),
        ("สอง", "sɔːŋ", "сонг"),
    ):
        a = analyze_syllable(thai)
        assert a.status == "analyzed"
        assert a.orthographic_interpretations[0]["role"] in {
            ORole.VOWEL_COMPONENT.value,
            ORole.ORTHOGRAPHIC_COMPONENT.value,
        }
        assert not a.phonemic_ipa.startswith("ʔ")
        assert a.selected_ukrainian_orthography == expected_ua


def test_special_y_has_higher_structural_priority_than_carrier():
    for thai in ("อยู่", "อย่า", "อยาก"):
        # The original spelling is classified before its exact lexical reading
        # is applied by the parser; inspect the classifier on the original form.
        assert classify_o_role(thai).role == ORole.SPECIAL_Y_PATTERN
        analysis = analyze_syllable(thai)
        assert analysis.orthographic_interpretations[0]["role"] == ORole.SPECIAL_Y_PATTERN.value
        assert analysis.status == "analyzed"
