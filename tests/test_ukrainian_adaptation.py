from thai_ukrainian.api import analyze_syllable


def test_ukrainian_output_comes_from_structured_thai_analysis():
    assert analyze_syllable("อา").ukrainian_transliteration == "а"
    assert analyze_syllable("อัน").ukrainian_transliteration == "ан"
    assert analyze_syllable("พอ").ukrainian_transliteration == "по"
    assert analyze_syllable("ขอ").ukrainian_transliteration == "ко"
    assert analyze_syllable("งอ").ukrainian_transliteration == "нго"
    assert analyze_syllable("สอง").ukrainian_transliteration == "сонг"


def test_glottal_carrier_has_no_independent_ukrainian_grapheme():
    a = analyze_syllable("อา")
    assert a.phonemic_ipa == "ʔaː"
    assert a.ukrainian_transliteration == "а"
