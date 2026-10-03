from thai_ukrainian.orthographic_rules import ORole, classify_o_role


def test_o_carrier():
    assert classify_o_role("อา").role is ORole.VOWEL_CARRIER
    assert classify_o_role("อัน").role is ORole.VOWEL_CARRIER
    assert classify_o_role("เอา").role is ORole.VOWEL_CARRIER


def test_o_vowel_component():
    for word in ("พอ", "ขอ", "คอ", "งอ", "สอง"):
        assert classify_o_role(word).role in {
            ORole.VOWEL_COMPONENT,
            ORole.ORTHOGRAPHIC_COMPONENT,
        }


def test_o_special_y():
    for word in ("อยู่", "อย่า", "อยาก"):
        assert classify_o_role(word).role is ORole.SPECIAL_Y_PATTERN


def test_o_is_not_glottal_by_default():
    assert classify_o_role("พอ").role is not ORole.GLOTTAL_ONSET
    assert classify_o_role("อา").role is not ORole.GLOTTAL_ONSET
