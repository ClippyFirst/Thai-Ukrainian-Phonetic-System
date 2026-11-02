import unittest

from thai_ukrainian.api import analyze_syllable
from thai_ukrainian.lexical_ipa import load_lexical_ipa_overrides


class LexicalIpaOverrideTests(unittest.TestCase):
    def test_active_override_is_source_pinned_and_not_gold(self):
        records = load_lexical_ipa_overrides()
        self.assertEqual(set(records), {"เงิน", "เดิน", "ออก", "ไกล", "ใกล้", "เพิ่ง"})
        row = records["เงิน"]
        self.assertEqual(row["segmental_ipa"], "ŋɤn")
        self.assertEqual(row["tone_category"], "mid")
        self.assertEqual(row["tone_contour_ipa"], "˧")
        self.assertEqual(row["vowel_length"], "short")
        self.assertEqual(row["source_revision"], "5759179")
        self.assertEqual(row["license"], "CC-BY-SA-4.0")
        self.assertEqual(row["status"], "ACTIVE_SOURCE_ATTESTED_NOT_GOLD")

    def test_walk_override_is_pinned_and_kept_distinct_from_money(self):
        row = load_lexical_ipa_overrides()["เดิน"]
        self.assertEqual(row["segmental_ipa"], "dɤːn")
        self.assertEqual(row["tone_category"], "mid")
        self.assertEqual(row["tone_contour_ipa"], "˧")
        self.assertEqual(row["vowel_length"], "long")
        self.assertEqual(row["source_revision"], "1908803")
        self.assertEqual(row["license"], "CC-BY-SA-4.0")
        self.assertEqual(row["status"], "ACTIVE_SOURCE_ATTESTED_NOT_GOLD")
        result = analyze_syllable("เดิน")
        self.assertEqual(result.status, "analyzed")
        self.assertEqual(result.phonemic_ipa, "dɤːn")
        self.assertEqual(result.vowel_length, "long")
        self.assertEqual(result.tone.tone, "mid")
        self.assertEqual(result.ukrainian_transliteration, "ден")
        self.assertTrue(any("not independently adjudicated" in warning for warning in result.warnings))

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

    def test_source_attested_final_coda_override_closes_eastern_direction_pipeline_gap(self):
        row = load_lexical_ipa_overrides()["ออก"]
        self.assertEqual(row["segmental_ipa"], "ʔɔːk")
        self.assertEqual(row["tone_category"], "low")
        self.assertEqual(row["tone_contour_ipa"], "˩")
        self.assertEqual(row["vowel_length"], "long")
        self.assertEqual(row["source_revision"], "86398986")
        self.assertEqual(row["source_url"], "https://en.wiktionary.org/w/index.php?title=ตะวันออก&oldid=86398986")
        self.assertEqual(row["license"], "CC-BY-SA-4.0")
        self.assertEqual(row["status"], "ACTIVE_SOURCE_ATTESTED_NOT_GOLD")
        result = analyze_syllable("ออก")
        self.assertEqual(result.status, "analyzed")
        self.assertEqual(result.phonemic_ipa, "ʔɔːk")
        self.assertEqual(result.vowel_length, "long")
        self.assertEqual(result.tone.tone, "low")
        self.assertEqual(result.tone.contour_ipa, "˩")
        self.assertIn("SRC-WIKTIONARY-EN-TH-ตะวันออก-ออก", result.sources)
        self.assertEqual(result.ukrainian_transliteration, "ок")
        self.assertTrue(any("not independently adjudicated" in warning for warning in result.warnings))


    def test_pinned_near_far_pair_preserves_source_attested_tone_and_diphthong(self):
        records = load_lexical_ipa_overrides()
        expected = {
            "ไกล": ("klaj", "mid", "˧", "5688545", "клай"),
            "ใกล้": ("klaj", "falling", "˥˩", "5721860", "клай"),
        }
        for word, (ipa, tone, contour, revision, ua) in expected.items():
            with self.subTest(word=word):
                row = records[word]
                self.assertEqual(row["segmental_ipa"], ipa)
                self.assertEqual(row["tone_category"], tone)
                self.assertEqual(row["tone_contour_ipa"], contour)
                self.assertEqual(row["vowel_length"], "diphthong")
                self.assertEqual(row["source_revision"], revision)
                self.assertEqual(row["license"], "CC-BY-SA-4.0")
                self.assertEqual(row["status"], "ACTIVE_SOURCE_ATTESTED_NOT_GOLD")
                result = analyze_syllable(word)
                self.assertEqual(result.status, "analyzed")
                self.assertEqual(result.phonemic_ipa, ipa)
                self.assertEqual(result.tone.tone, tone)
                self.assertEqual(result.ukrainian_transliteration, ua)
                self.assertTrue(any("not independently adjudicated" in warning for warning in result.warnings))

    def test_pering_uses_pinned_source_attested_short_vowel_and_falling_tone(self):
        row = load_lexical_ipa_overrides()["เพิ่ง"]
        self.assertEqual(row["segmental_ipa"], "pʰɤŋ")
        self.assertEqual(row["tone_category"], "falling")
        self.assertEqual(row["tone_contour_ipa"], "˥˩")
        self.assertEqual(row["vowel_length"], "short")
        self.assertEqual(row["source_revision"], "1885200")
        self.assertEqual(row["source_url"], "https://th.wiktionary.org/w/index.php?title=เพิ่ง&oldid=1885200")
        self.assertEqual(row["license"], "CC-BY-SA-4.0")
        self.assertEqual(row["status"], "ACTIVE_SOURCE_ATTESTED_NOT_GOLD")

        result = analyze_syllable("เพิ่ง")
        self.assertEqual(result.status, "analyzed")
        self.assertEqual(result.phonemic_ipa, "pʰɤŋ")
        self.assertIsNone(result.phonetic_ipa)
        self.assertEqual(result.vowel_length, "short")
        self.assertEqual(result.tone.tone, "falling")
        self.assertEqual(result.tone.contour_ipa, "˥˩")
        self.assertIn("SRC-WIKTIONARY-TH-เพิ่ง", result.sources)
        self.assertIn("LEXICAL-IPA-OVERRIDE:SRC-WIKTIONARY-TH-เพิ่ง", result.rules_applied)
        self.assertEqual(result.ukrainian_transliteration, "п'енг")
        self.assertTrue(any("not independently adjudicated" in warning for warning in result.warnings))

    def test_unlisted_forms_do_not_receive_a_lexical_override(self):
        result = analyze_syllable("เดิน")
        self.assertIn("LEXICAL-IPA-OVERRIDE:SRC-WIKTIONARY-TH-เดิน", result.rules_applied)
        self.assertIn("SRC-WIKTIONARY-TH-เดิน", result.sources)


if __name__ == "__main__":
    unittest.main()
