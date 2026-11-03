import unittest

from thai_ukrainian.segmentation import _grapheme_spans


class ThaiClusterBoundaryTests(unittest.TestCase):
    def test_postposed_spacing_vowels_stay_with_their_base_cluster(self):
        # These Thai vowel letters are spacing code points, not Unicode
        # combining marks, but the browser's dictionary matcher keeps them
        # attached to the preceding Thai base for safe match boundaries.
        for text in ("กะ", "กา", "กำ"):
            with self.subTest(text=text):
                self.assertEqual(_grapheme_spans(text), ((0, len(text)),))

    def test_postposed_vowel_after_preposed_vowel_cluster_stays_attached(self):
        self.assertEqual(_grapheme_spans("เกา"), ((0, len("เกา")),))

    def test_combining_tone_and_vowel_marks_remain_in_the_same_cluster(self):
        for text in ("ก่", "กิ", "เก่ง"):
            with self.subTest(text=text):
                spans = _grapheme_spans(text)
                self.assertEqual(spans[0][0], 0)
                self.assertGreaterEqual(spans[0][1], 2)


if __name__ == "__main__":
    unittest.main()
