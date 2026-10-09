import unittest

from thai_ukrainian.api import analyze_syllable
from thai_ukrainian.text import analyze_text, segment_thai_word, tokenize_text


class TextPipelineTests(unittest.TestCase):
    def test_mixed_tokenization(self):
        tokens = tokenize_text("กรุงเทพ, Bangkok 123! ๆ")
        self.assertEqual(
            [token.kind for token in tokens],
            ["thai", "punctuation", "latin", "number", "punctuation", "thai_marker"],
        )
        self.assertEqual([token.text for token in tokenize_text("ฟิล์ม ๆ")], ["ฟิล์ม", "ๆ"])

    def test_curated_multisyllable_words(self):
        self.assertEqual(segment_thai_word("ครอบครัว"), (("ครอบ", "ครัว"), "lexicon"))
        self.assertEqual(segment_thai_word("รถบัส"), (("รถ", "บัส"), "lexicon"))
        self.assertEqual(segment_thai_word("คอมพิวเตอร์"), (("คอม", "พิว", "เตอร์"), "lexicon"))

    def test_unknown_text_is_not_falsely_segmented(self):
        for text in ("คำใหม่ที่ไม่อยู่ในพจนานุกรม", "กากล้าขายแล้วไหว้แสดง"):
            with self.subTest(text=text):
                syllables, status = segment_thai_word(text)
                self.assertEqual(syllables, (text,))
                self.assertEqual(status, "unresolved")

    def test_text_analysis_preserves_word_boundaries_and_punctuation(self):
        result = analyze_text("ครอบครัว, รถบัส")
        self.assertEqual(
            [(token["input"], token["kind"]) for token in result],
            [("ครอบครัว", "thai"), (",", "punctuation"), ("รถบัส", "thai")],
        )
        self.assertEqual(result[0]["segmentation_status"], "lexicon")
        self.assertEqual(result[0]["syllables"][0]["input"], "ครอบ")
        self.assertEqual(result[2]["segmentation_status"], "lexicon")

    def test_final_velar_stop_is_preserved_in_ukrainian_output(self):
        for word in ("พริก", "ตรอก"):
            with self.subTest(word=word):
                result = analyze_syllable(word)
                self.assertEqual(result.status, "analyzed")
                self.assertTrue(result.phonemic_ipa.endswith("k"), result.phonemic_ipa)
                self.assertTrue(result.ukrainian_transliteration.endswith("к"), result.ukrainian_transliteration)

    def test_medial_ua_glide_is_not_mistaken_for_a_coda(self):
        result = analyze_syllable("กวน")
        self.assertEqual(result.status, "analyzed")
        self.assertEqual(result.onset, ["ก"])
        self.assertEqual(result.coda, "น")
        self.assertTrue(result.phonemic_ipa.endswith("n"), result.phonemic_ipa)
        self.assertTrue(result.ukrainian_transliteration.endswith("н"), result.ukrainian_transliteration)

    def test_w_glides_are_rendered_consistently_as_v(self):
        for word in ("ดาว", "หนาว", "เศร้า"):
            with self.subTest(word=word):
                result = analyze_syllable(word)
                self.assertEqual(result.status, "analyzed")
                self.assertIsNone(result.coda)
                self.assertTrue(result.phonemic_ipa.endswith("w"), result.phonemic_ipa)
                self.assertTrue(result.ukrainian_transliteration.endswith("в"), result.ukrainian_transliteration)
        cold = analyze_syllable("หนาว")
        self.assertEqual(cold.onset, ["ห", "น"])
        self.assertEqual(cold.phonemic_ipa, "naːw")

    def test_lexical_readings_produce_structured_results(self):
        # These are parser smoke tests, not gold-IPA assertions. Gold readings
        # belong in the adjudicated fixture set with cited lexical evidence.
        for word in ("จริง", "สร้าง", "เศร้า", "ไซร้", "จันทร์", "ศุกร์", "เสาร์",
                     "สัตว์", "พันธุ์", "ฟิล์ม", "ฤทธิ์", "เตอร์", "อย่า", "อยู่", "อย่าง", "อยาก"):
            with self.subTest(word=word):
                result = analyze_syllable(word)
                self.assertIsNotNone(result.status)
                self.assertEqual(result.input, word)
                if word == "อย่าง":
                    self.assertEqual(result.normalized, "หย่าง")
                if word == "เตอร์":
                    self.assertEqual(result.normalized, "เตอ")


if __name__ == "__main__":
    unittest.main()
