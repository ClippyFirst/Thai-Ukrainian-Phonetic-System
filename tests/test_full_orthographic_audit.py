from thai_ukrainian.api import analyze_syllable
from thai_ukrainian.parser import parse_syllable


def assert_analyzed(text, vowel_id, vowel, onset, coda=None, ua=None):
    a = parse_syllable(text)
    assert a.status == "analyzed", (text, a.status, a.warnings)
    assert a.vowel_id == vowel_id, (text, a.vowel_id)
    assert a.vowel == vowel, (text, a.vowel)
    assert a.onset == onset, (text, a.onset)
    assert a.coda == coda, (text, a.coda)
    if ua is not None:
        practical = analyze_syllable(text).ukrainian_transliteration
        assert practical == ua, (text, practical)
    return a


def test_post_consonant_o_component_is_not_glottal():
    for text, onset, coda in [
        ("พอ", ["พ"], None),
        ("ขอ", ["ข"], None),
        ("คอ", ["ค"], None),
        ("งอ", ["ง"], None),
        ("สอง", ["ส"], "ง"),
        ("ของ", ["ข"], "ง"),
    ]:
        assert_analyzed(text, "V-18", "ɔː", onset, coda)


def test_post_consonant_ue_length_carrier():
    assert_analyzed("คือ", "V-08", "ɯː", ["ค"], None)
    assert_analyzed("มือ", "V-08", "ɯː", ["ม"], None)
    # หนังสือ is a multi-syllable word, not a single input for parse_syllable.
    assert_analyzed("สือ", "V-08", "ɯː", ["ส"], None)


def test_mai_taikhu_shortens_preposed_e():
    for text, onset, coda in [
        ("เป็น", ["ป"], "น"),
        ("เด็ก", ["ด"], "ก"),
        ("เก็บ", ["ก"], "บ"),
    ]:
        assert_analyzed(text, "V-03", "e", onset, coda)


def test_reduced_vowel_spellings_preserve_ambiguity_until_lexical_evidence():
    for text, onset, coda in [
        ("เดิน", ["ด"], "น"),
        ("เงิน", ["ง"], "น"),
        ("เปิด", ["ป"], "ด"),
    ]:
        analysis = parse_syllable(text)
        assert analysis.status == "analysis-dependent:vowel-length", (text, analysis.status)
        assert analysis.onset == onset
        assert analysis.coda == coda
        assert analysis.phonemic_ipa is None

    # The exact, revision-pinned dictionary overrides resolve only the two
    # covered forms; they do not turn the spelling pattern into a productive rule.
    for text, expected_ipa in (("เดิน", "dɤːn"), ("เงิน", "ŋɤn")):
        analysis = analyze_syllable(text)
        assert analysis.status == "analyzed"
        assert analysis.phonemic_ipa == expected_ipa
        assert analysis.phonetic_result["status"] == "SUPPORTED"
        assert analysis.phonetic_result["broad_surface_ipa"] is None
        assert any("source-attested lexical dictionary transcription" in warning
                   for warning in analysis.warnings)

    assert_analyzed("แข็ง", "V-05", "ɛ", ["ข"], "ง")


def test_reduced_ua_uses_w_as_vowel_component():
    for text, onset, coda in [
        ("สวน", ["ส"], "น"),
        ("กวน", ["ก"], "น"),
        ("ควร", ["ค"], "ร"),
        ("รวม", ["ร"], "ม"),
    ]:
        assert_analyzed(text, "V-X-UA", "uaː", onset, coda)


def test_inherent_o_closed_syllables_are_structurally_resolved():
    for text, onset, coda in [
        ("กบ", ["ก"], "บ"),
        ("คน", ["ค"], "น"),
        ("ผล", ["ผ"], "ล"),
        ("ส่ง", ["ส"], "ง"),
        ("กร", ["ก"], "ร"),
        ("กรน", ["ก", "ร"], "น"),
    ]:
        a = assert_analyzed(text, "IV-INHERENT-O", "o", onset, coda)
        assert any("inherent /o/" in w for w in a.warnings)


def test_inherent_o_does_not_turn_a_single_bare_consonant_into_a_guess():
    a = parse_syllable("ก")
    assert a.status in {"unresolved:implicit-vowel", "unresolved:no-onset"}
    assert a.vowel is None


def test_preposed_ai_preserves_real_onsets():
    assert_analyzed("ไก่", "V-X-AI", "aj", ["ก"], None)
    assert_analyzed("ไกล", "V-X-AI", "aj", ["ก", "ล"], None)
    assert_analyzed("ไหม", "V-X-AI", "aj", ["ห", "ม"], None)
    assert_analyzed("ไหว้", "V-X-AI", "aj", ["ห", "ว"], None)


def test_standalone_ai_carrier_uses_zero_ukrainian_onset():
    a = assert_analyzed("ไอ", "V-X-AI", "aj", ["อ"], None, "ай")
    assert a.onset == ["อ"]


def test_existing_o_carrier_and_special_y_remain_distinct():
    assert_analyzed("อา", "V-12", "aː", ["อ"], None, "а")
    assert_analyzed("อัน", "V-11", "a", ["อ"], "น", "ан")
    assert_analyzed("พอ", "V-18", "ɔː", ["พ"], None, "п\u0027о")


def test_hnam_stays_structural_and_tone_bearing():
    a = parse_syllable("หงา")
    assert a.status == "analyzed"
    assert a.onset == ["ห", "ง"]
    assert a.tone_class == "high"


def test_glottal_carrier_is_not_a_final():
    a = parse_syllable("อา")
    assert a.coda is None
    assert a.coda_ipa is None
