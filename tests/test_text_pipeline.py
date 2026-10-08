import unittest
from thai_ukrainian.text import tokenize_text, segment_thai_word\nfrom thai_ukrainian.api import analyze_syllable

class TextPipelineTests(unittest.TestCase):
    def test_mixed_tokenization(self):
        tokens = tokenize_text("กรุงเทพ, Bangkok 123! ๆ")
        self.assertEqual([x.kind for x in tokens], ["thai","punctuation","latin","number","punctuation","thai_marker"])\n        self.assertEqual([x.text for x in tokenize_text("ฟิล์ม ๆ")], ["ฟิล์ม","ๆ"])

    def test_curated_multisyllable_words(self):
        self.assertEqual(segment_thai_word("ครอบครัว"), (("ครอบ","ครัว"), "lexicon"))
        self.assertEqual(segment_thai_word("รถบัส"), (("รถ","บัส"), "lexicon"))

    def test_lexical_reading_regressions(self):\n        cases = {\n            "พริก": "pʰrik",\n            "ตรอก": "trɔːk",\n            "กล้วย": "kluajn",\n            "จริง": "tɕiŋ",\n            "สร้าง": "saːŋ",\n            "เศร้า": "saːw",\n            "จันทร์": "tan",\n            "ศุกร์": "suk",\n            "เสาร์": "sau",\n            "สัตว์": "sat",\n            "ฟิล์ม": "fim",\n            "ฤทธิ์": "rit",\n            "อย่า": "jaː",\n            "อยู่": "juː",\n            "อยาก": "jak",\n        }\n        for word, ipa in cases.items():\n            with self.subTest(word=word):\n                a = analyze_syllable(word)\n                self.assertEqual(a.status, "analyzed")\n                self.assertIsNotNone(a.phonemic_ipa)\n                self.assertTrue(a.phonemic_ipa.startswith(ipa))\n\n    def test_phrase(self):
        self.assertEqual(segment_thai_word("กากล้าขายแล้วไหว้แสดง"), (("กา","กล้า","ขาย","แล้ว","ไหว้","แส","ดง"), "lexicon"))

if __name__ == "__main__":
    unittest.main()
