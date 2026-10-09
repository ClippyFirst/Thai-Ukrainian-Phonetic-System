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
        self.assertEqual(result[1]["segmentation_status"], "lexicon")

    def test_lexical_readings_produce_structured_results(self):
        # These are parser smoke tests, not gold-IPA assertions. Gold readings
        # belong in the adjudicated fixture set with cited lexical evidence.
        for word in ("จริง", "สร้าง", "เศร้า", "ไซร้", "จันทร์", "ศุกร์", "เสาร์",
                     "สัตว์", "พันธุ์", "ฟิล์ม", "ฤทธิ์", "อย่า", "อยู่", "อย่าง", "อยาก"):
            with self.subTest(word=word):
                result = analyze_syllable(word)
                self.assertIsNotNone(result.status)
                self.assertEqual(result.input, word)
                if word == "อย่าง":
                    self.assertEqual(result.normalized, "หย่าง")


if __name__ == "__main__":
    unittest.main()
