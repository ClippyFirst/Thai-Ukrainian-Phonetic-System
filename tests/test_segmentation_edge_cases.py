import unittest

from thai_ukrainian.segmentation import dictionary_word_segmentation, segment_text_preserving


class ThaiSegmentationEdgeCaseTests(unittest.TestCase):
    def test_combining_marks_are_never_split_off_from_their_base(self):
        result = dictionary_word_segmentation("ก่฿")
        self.assertEqual("".join(result.tokens), "ก่฿")
        self.assertNotIn("่", result.tokens)
        self.assertIn("฿", result.unknown_clusters)

    def test_empty_input_is_a_complete_empty_result(self):
        result = dictionary_word_segmentation("")
        self.assertEqual(result.tokens, ())
        self.assertEqual(result.unknown_clusters, ())
        self.assertTrue(result.complete)

    def test_lossless_mixed_text_even_with_unknown_thai_cluster(self):
        source = "ภาษาไทย! ฿ Bangkok"
        tokens = segment_text_preserving(source)
        self.assertEqual("".join(tokens), source)
        self.assertIn("Bangkok", tokens)

    def test_unknowns_are_explicit_not_silently_rewritten(self):
        source = "ฉันก฿แมว"
        result = dictionary_word_segmentation(source)
        self.assertEqual("".join(result.tokens), source)
        self.assertFalse(result.complete)
        self.assertIn("฿", result.unknown_clusters)


if __name__ == "__main__":
    unittest.main()
