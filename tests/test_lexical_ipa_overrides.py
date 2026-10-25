import unittest

from thai_ukrainian.api import analyze_syllable
from thai_ukrainian.lexical_ipa import load_lexical_ipa_overrides


class LexicalIpaOverrideTests(unittest.TestCase):
    def test_active_override_is_source_pinned_and_not_gold(self):
        records = load_lexical_ipa_overrides()
        self.assertEqual(set(records), {"เงิน"})
        row = records["เงิน"]
        self.assertEqual(row["segmental_ipa"], "ŋɤn")
        self.assertEqual(row["tone_category"], "mid")
        self.assertEqual(row["tone_contour_ipa"], "˧")
        self.assertEqual(row["vowel_length"], "short")
        self.assertEqual(row["source_revision"], "5759179")
        self.assertEqual(row["license"], "CC-BY-SA-4.0")
        self.assertEqual(row["status"], "ACTIVE_SOURCE_ATTESTED_NOT_GOLD")

    def test_money_override_reaches_typed_ipa_and_ukrainian_adapter(self):
        result = analyze_syllable("เงิน")
        self.assertEqual(result.status, "analyzed")
        self.assertEqual(result.phonemic_ipa, "ŋɤn")
        self.assertEqual(result.vowel_length, "short")
        self.assertEqual(result.tone.tone, "mid")
        self.assertEqual(result.tone.contour_ipa, "˧")
        self.assertIn("SRC-WIKTIONARY-TH-เงิน", result.sources)
        self.assertIn("LEXICAL-IPA-OVERRIDE:SRC-WIKTIONARY-TH-เงิน", result.rules_applied)
        self.assertEqual(result.phonetic_result["phonemic_ipa"], "ŋɤn")
        self.assertEqual(result.phonetic_result["tone_category"], "mid")
        self.assertEqual(result.phonetic_result["vowel_length"], "short")
        self.assertEqual(result.ukrainian_transliteration, "нген")
        self.assertTrue(any("not independently adjudicated" in warning for warning in result.warnings))

    def test_unlisted_forms_do_not_receive_a_lexical_override(self):
        result = analyze_syllable("เดิน")
        self.assertNotIn("LEXICAL-IPA-OVERRIDE:SRC-WIKTIONARY-TH-เงิน", result.rules_applied)
        self.assertNotIn("SRC-WIKTIONARY-TH-เงิน", result.sources)


if __name__ == "__main__":
    unittest.main()
