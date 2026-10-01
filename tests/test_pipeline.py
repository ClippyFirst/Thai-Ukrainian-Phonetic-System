import unittest
from thai_ukrainian.api import analyze_syllable
from thai_ukrainian.parser import parse_syllable

class PipelineTests(unittest.TestCase):
    def test_long_open_live(self):
        a=parse_syllable("กา"); self.assertEqual(a.live_dead,"live"); self.assertEqual(a.vowel_length,"long")
    def test_cluster_not_coda(self): self.assertIsNone(parse_syllable("กรา").coda)
    def test_final_n_live(self):
        a=parse_syllable("กาน"); self.assertEqual(a.coda,"น"); self.assertEqual(a.live_dead,"live")
    def test_tone(self):
        a=analyze_syllable("กา"); self.assertEqual(a.tone.tone,"mid")
    def test_feature_candidates(self): self.assertTrue(analyze_syllable("กา").ukrainian_candidates)
    def test_implicit_vowel_flag(self): self.assertTrue(parse_syllable("ก").warnings)
    def test_special_construction_flag(self): self.assertTrue(parse_syllable("หง").warnings)
if __name__=="__main__":unittest.main()
