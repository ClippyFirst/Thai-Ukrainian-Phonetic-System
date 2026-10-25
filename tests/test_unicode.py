import unittest
from thai_ukrainian.orthography import normalize_thai, decompose_thai
from thai_ukrainian import analyze_syllable, tokenize_text, parse_thai


class UnicodeTests(unittest.TestCase):
    def test_nfc_and_trim_are_idempotent(self):
        normalized = normalize_thai("  ก่า  ")
        self.assertEqual(normalized, "ก่า")
        self.assertEqual(normalize_thai(normalized), normalized)

    def test_only_ascii_layout_whitespace_is_trimmed(self):
        self.assertEqual(normalize_thai("\tกา\r\n"), "กา")
        # Python str.strip() treats U+0085 as whitespace, unlike the browser's
        # ECMAScript trim set. Preserve it so the parser rejects it as input.
        self.assertEqual(normalize_thai("\u0085กา\u0085"), "\u0085กา\u0085")

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

    def test_text_tokenizer_preserves_non_ascii_whitespace_controls(self):
        tokens = tokenize_text("\u0085กา\u0085")
        self.assertEqual([(token.text, token.kind) for token in tokens], [
            ("\u0085", "punctuation"), ("กา", "thai"), ("\u0085", "punctuation")
        ])

    def test_parse_thai_splits_only_ascii_layout_boundaries(self):
        results = parse_thai(" \tกา\r\nขา ")
        self.assertEqual([item.input for item in results], ["กา", "ขา"])
        self.assertTrue(all(item.phonemic_ipa for item in results))
        self.assertTrue(all(item.ukrainian_transliteration for item in results))

    def test_vertical_tab_and_form_feed_are_not_syllable_separators(self):
        for control in ("\x0b", "\x0c"):
            with self.subTest(codepoint=f"U+{ord(control):04X}"):
                results = parse_thai("กา" + control + "ขา")
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0].status, "unresolved:unsupported-symbol")
                self.assertIsNone(results[0].phonemic_ipa)
                self.assertIsNone(results[0].ukrainian_transliteration)

    def test_syllable_api_does_not_split_on_non_ascii_whitespace_controls(self):
        for source in ("\u0085กา", "กา\u0085", "กา\u0085กา"):
            with self.subTest(source=source):
                results = parse_thai(source)
                self.assertTrue(results)
                self.assertTrue(all(item.status == "unresolved:unsupported-symbol" for item in results))
                self.assertTrue(all(item.phonemic_ipa is None for item in results))
                self.assertTrue(all(item.phonetic_ipa is None for item in results))
                self.assertTrue(all(item.ukrainian_transliteration is None for item in results))

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
