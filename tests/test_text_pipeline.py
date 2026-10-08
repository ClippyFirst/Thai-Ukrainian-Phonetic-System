import unittest
from thai_ukrainian.text import tokenize_text, segment_thai_word

class TextPipelineTests(unittest.TestCase):
    def test_mixed_tokenization(self):
        tokens = tokenize_text("กรุงเทพ, Bangkok 123! ๆ")
        self.assertEqual([x.kind for x in tokens], ["thai","punctuation","latin","number","punctuation","thai_marker"])

    def test_curated_multisyllable_words(self):
        self.assertEqual(segment_thai_word("ครอบครัว"), (("ครอบ","ครัว"), "lexicon"))
        self.assertEqual(segment_thai_word("รถบัส"), (("รถ","บัส"), "lexicon"))

    def test_phrase(self):
        self.assertEqual(segment_thai_word("กากล้าขายแล้วไหว้แสดง"), (("กา","กล้า","ขาย","แล้ว","ไหว้","แส","ดง"), "lexicon"))

if __name__ == "__main__":
    unittest.main()
