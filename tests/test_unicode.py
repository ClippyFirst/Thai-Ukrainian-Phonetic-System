import unittest
from thai_ukrainian.orthography import normalize_thai, decompose_thai
from thai_ukrainian import analyze_syllable


class UnicodeTests(unittest.TestCase):
    def test_nfc_and_trim_are_idempotent(self):
        normalized = normalize_thai("  ก่า  ")
        self.assertEqual(normalized, "ก่า")
        self.assertEqual(normalize_thai(normalized), normalized)

    def test_roles(self):
        roles = [x["role"] for x in decompose_thai("ก่า")]
        self.assertIn("consonant", roles)
        self.assertIn("tone_mark", roles)

    def test_normalized_indices_match_the_normalized_source(self):
        source = "  ก่า  "
        normalized = normalize_thai(source)
        parts = decompose_thai(source)
        self.assertEqual("".join(item["char"] for item in parts), normalized)
        self.assertEqual([item["index"] for item in parts], list(range(len(normalized))))

    def test_controls_format_controls_and_zero_width_space_withhold_output(self):
        # These code points are not ordinary Thai orthographic material. They
        # must not disappear during normalization or permit a partial reading.
        for character, codepoint in (
            ("\x01", "U+0001"),
            ("\x7f", "U+007F"),
            ("\x85", "U+0085"),
            ("\u200b", "U+200B"),
            ("\u202e", "U+202E"),
        ):
            with self.subTest(codepoint=codepoint):
                result = analyze_syllable("กา" + character)
                self.assertEqual(result.status, "unresolved:unsupported-symbol")
                self.assertIsNone(result.phonemic_ipa)
                self.assertIsNone(result.phonetic_ipa)
                self.assertIsNone(result.ukrainian_transliteration)


if __name__ == "__main__":
    unittest.main()
