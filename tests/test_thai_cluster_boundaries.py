import unittest
from unittest.mock import patch

from thai_ukrainian.segmentation import _END, dictionary_word_segmentation


class ThaiClusterBoundaryTests(unittest.TestCase):
    def _assert_no_dictionary_match_can_end_inside_cluster(self, text, dictionary_prefix):
        # Model a dictionary containing only the shorter prefix. The public
        # segmenter must not accept that match when its endpoint falls inside
        # the following Thai base-plus-vowel cluster.
        trie = {}
        node = trie
        for char in dictionary_prefix:
            node = node.setdefault(char, {})
        node[_END] = True
        with patch("thai_ukrainian.segmentation._dictionary_trie", return_value=trie):
            result = dictionary_word_segmentation(text)
        self.assertEqual(result.tokens, (text,))
        self.assertEqual(result.unknown_clusters, (text,))
        self.assertFalse(result.complete)
        self.assertEqual(result.token_statuses, ("unknown_cluster_fallback",))

    def test_postposed_spacing_vowels_block_a_match_ending_after_the_base(self):
        for text in ("กะ", "กา", "กำ"):
            with self.subTest(text=text):
                self._assert_no_dictionary_match_can_end_inside_cluster(text, "ก")

    def test_postposed_vowel_after_preposed_vowel_cluster_blocks_early_match(self):
        self._assert_no_dictionary_match_can_end_inside_cluster("เกา", "เก")

    def test_combining_tone_and_vowel_marks_also_block_early_match(self):
        for text, prefix in (("ก่", "ก"), ("กิ", "ก")):
            with self.subTest(text=text):
                self._assert_no_dictionary_match_can_end_inside_cluster(text, prefix)


if __name__ == "__main__":
    unittest.main()
