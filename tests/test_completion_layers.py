from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path

from thai_ukrainian.api import analyze_syllable
from thai_ukrainian.lexicon import load_lexicon, segment_word
from thai_ukrainian.source_final import build_manifest
from thai_ukrainian.ua_orthography import candidates_for_ipa


class CompletionLayerTests(unittest.TestCase):
    def test_source_final_manifest(self):
        report = build_manifest()
        self.assertEqual(report["status"], "pass")
        self.assertTrue(all(report["invariants"].values()))

    def test_machine_readable_tone_rules(self):
        for text in ("กา", "ก่า", "ก้า", "ก๊า", "ก๋า"):
            a = analyze_syllable(text)
            self.assertIsNotNone(a.tone)
        self.assertEqual(analyze_syllable("ก๊า").tone.tone, "high")
        self.assertEqual(analyze_syllable("ก๋า").tone.tone, "rising")

    def test_special_orthography_is_not_silently_forced(self):
        for text in ("สรรค์", "ฤ", "ฤๅ", "ฦ", "ฦๅ", "ทร"):
            with self.subTest(text=text):
                a = analyze_syllable(text)
                self.assertTrue(a.status.startswith("analysis-dependent:special-orthography"))
                self.assertTrue(a.special_analyses)
                self.assertIsNone(a.phonemic_ipa)

    def test_unknown_thanthakhat_is_not_silently_deleted(self):
        a = analyze_syllable("ก์")
        self.assertTrue(a.status.startswith("analysis-dependent:special-orthography"))
        self.assertIsNone(a.phonemic_ipa)

    def test_known_thanthakhat_word_uses_explicit_lexical_reading(self):
        a = analyze_syllable("จันทร์")
        self.assertEqual(a.status, "analyzed")
        self.assertEqual(a.normalized, "จัน")
        self.assertIsNotNone(a.phonemic_ipa)

    def test_ukrainian_output_is_explicitly_project_candidate(self):
        result = candidates_for_ipa("tɕʰaː")
        self.assertIn("ча", result)

    def test_lexicon_requires_explicit_external_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "lexicon.tsv"
            path.write_text("word\tsyllables\tsource\nกาแฟ\tกา|แฟ\tfixture\n", encoding="utf-8")
            lexicon = load_lexicon(path)
            self.assertEqual(segment_word("กาแฟ", lexicon), ["กา", "แฟ"])
            with self.assertRaises(KeyError):
                segment_word("ไม่อยู่", lexicon)

    def test_schema_output_contains_final_layers(self):
        a = analyze_syllable("กา").as_dict()
        self.assertIn("special_analyses", a)
        self.assertIn("ukrainian_orthography_candidates", a)
        self.assertIn("selected_ukrainian_orthography", a)


if __name__ == "__main__":
    unittest.main()
