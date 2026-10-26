import unittest

from scripts.train_tud_word_segmenter import (
    evaluation_groups,
    parse_conllu_sentences,
    segment,
    training_counts,
)


class TUDSegmenterTests(unittest.TestCase):
    def test_frequency_viterbi_prefers_supported_word_sequence(self):
        counts = {"ฉัน": 10, "รัก": 8, "เธอ": 7, "ฉันรัก": 1}
        self.assertEqual(segment("ฉันรักเธอ", counts, penalty=1.0), ["ฉัน", "รัก", "เธอ"])

    def test_unknown_characters_are_preserved(self):
        self.assertEqual(segment("กขฃ", {"กข": 10}, penalty=1.0), ["กข", "ฃ"])

    def test_conllu_training_split_respects_no_space_annotations(self):
        sample = """# text = ฉันรักเธอ
1\tฉัน\t_\tPRON\t_\t_\t2\tnsubj\t_\tSpaceAfter=No
2\tรัก\t_\tVERB\t_\t_\t0\troot\t_\tSpaceAfter=No
3\tเธอ\t_\tPRON\t_\t_\t2\tobj\t_\t_
"""
        sentences = parse_conllu_sentences(sample)
        self.assertEqual(len(sentences), 1)
        self.assertEqual([word for word, _ in sentences[0][1]], ["ฉัน", "รัก", "เธอ"])
        groups = evaluation_groups(sentences)
        self.assertEqual(groups, [["ฉัน", "รัก", "เธอ"]])
        self.assertEqual(training_counts(sentences)["ฉัน"], 1)

    def test_split_by_space_does_not_create_false_thai_group(self):
        sample = """# text = ฉัน รัก
1\tฉัน\t_\tPRON\t_\t_\t0\troot\t_\t_
2\tรัก\t_\tVERB\t_\t_\t1\tobj\t_\t_
"""
        self.assertEqual(evaluation_groups(parse_conllu_sentences(sample)), [])


if __name__ == "__main__":
    unittest.main()
