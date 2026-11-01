import unittest

from thai_ukrainian.api import analyze_word_syllables


class WordPositionTests(unittest.TestCase):
    def test_standalone_position(self):
        w = analyze_word_syllables(["กา"])
        self.assertEqual(w.positions[0].label, "standalone")
        self.assertEqual(w.phonemic_ipa, "kaː")

    def test_initial_medial_final_positions(self):
        w = analyze_word_syllables(["กา", "นา", "มา"])
        self.assertEqual([p.label for p in w.positions], ["initial", "medial", "final"])
        self.assertEqual([p.index for p in w.positions], [0, 1, 2])
        self.assertEqual([p.total for p in w.positions], [3, 3, 3])

    def test_position_does_not_change_syllable_ipa(self):
        w = analyze_word_syllables(["กา", "กา"])
        self.assertEqual(w.syllables[0].phonemic_ipa, w.syllables[1].phonemic_ipa)
        self.assertEqual(w.positions[0].label, "initial")
        self.assertEqual(w.positions[1].label, "final")

    def test_explicit_segmentation_is_preserved(self):
        w = analyze_word_syllables(["กรา", "นา"])
        self.assertEqual(w.syllables[0].input, "กรา")
        self.assertIsNone(w.syllables[0].coda)
        self.assertEqual(w.segmentation_status, "explicit")

    def test_empty_word_rejected(self):
        with self.assertRaises(ValueError):
            analyze_word_syllables([])

    def test_word_analyzer_receives_syllable_analyzer_dependency(self):
        from thai_ukrainian.models import SyllableAnalysis
        from thai_ukrainian.word import analyze_word

        calls = []

        def fake_analyzer(text):
            calls.append(text)
            return SyllableAnalysis(input=text, normalized=text, phonemic_ipa="kaː")

        result = analyze_word(["กา", "นา"], analyze_syllable=fake_analyzer)
        self.assertEqual(calls, ["กา", "นา"])
        self.assertEqual(result.phonemic_ipa, "kaː.kaː")
        self.assertEqual(result.segmentation_status, "explicit")

if __name__ == "__main__":
    unittest.main()
