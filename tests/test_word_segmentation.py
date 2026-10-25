import json
import unittest
from pathlib import Path

from thai_ukrainian.segmentation import (
    dictionary_word_segmentation,
    segment_text_preserving,
    load_word_dictionary,
)

ROOT = Path(__file__).resolve().parents[1]


class ThaiWordSegmentationTests(unittest.TestCase):
    def test_pinned_dictionary_is_large_unique_and_thai_only(self):
        words = load_word_dictionary()
        self.assertGreater(len(words), 60000)
        self.assertEqual(len(words), len(set(words)))
        self.assertTrue(all(word and all("\u0e00" <= ch <= "\u0e7f" for ch in word) for word in words))

    def test_source_manifest_pins_cc0_data_and_transform(self):
        manifest = json.loads((ROOT / "data/thai/word-segmentation-dictionary-source.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["source_commit"], "8b2b9a6d0f69846364f37e8c16ffc31177f6151c")
        self.assertEqual(manifest["source_blob_sha1"], "093dda8a35646281e71a8a434137cb5fac57882e")
        self.assertEqual(manifest["license"], "CC0-1.0")
        self.assertEqual(manifest["retained_unique_entries"], len(load_word_dictionary()))
        self.assertIn("no Wisesight samples", manifest["transformation"])

    def test_known_words_are_segmented_by_dictionary_maximum_matching(self):
        self.assertEqual(dictionary_word_segmentation("ฉันรักแมว").tokens, ("ฉัน", "รัก", "แมว"))
        self.assertEqual(dictionary_word_segmentation("ประเทศไทยมีคน").tokens, ("ประเทศ", "ไทย", "มี", "คน"))

    def test_unknown_graphemes_are_preserved_and_marked(self):
        result = dictionary_word_segmentation("ฉันก฿แมว")
        self.assertEqual("".join(result.tokens), "ฉันก฿แมว")
        self.assertIn("฿", result.unknown_clusters)
        self.assertFalse(result.complete)

    def test_mixed_text_reconstructs_exactly(self):
        text = "ฉันรักแมว, Bangkok 123 ๆ"
        tokens = segment_text_preserving(text)
        self.assertEqual("".join(tokens), text)
        self.assertIn("ฉัน", tokens)
        self.assertIn("Bangkok", tokens)
        self.assertIn("123", tokens)
        self.assertIn("ๆ", tokens)

    def test_dictionary_segmentation_does_not_claim_phonetic_analysis(self):
        result = dictionary_word_segmentation("ภาษาไทย")
        self.assertEqual(result.tokens, ("ภาษาไทย",))
        self.assertTrue(result.method.startswith("clippyfirst-"))
        self.assertEqual(result.evidence_grade, "DICTIONARY_SEGMENTATION_NOT_PRONUNCIATION_GOLD")


if __name__ == "__main__":
    unittest.main()
