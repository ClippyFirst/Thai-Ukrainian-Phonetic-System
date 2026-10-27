import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SourceAttestedIpaRegistryTests(unittest.TestCase):
    def test_source_attested_records_have_pinned_provenance_and_are_not_gold(self):
        path = ROOT / "data" / "benchmark" / "source-attested-ipa.tsv"
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream, delimiter="\t"))
        self.assertEqual(len(rows), 6)
        self.assertEqual(len({row["id"] for row in rows}), 6)
        for row in rows:
            with self.subTest(record=row["id"]):
                self.assertTrue(row["thai"])
                self.assertTrue(row["phonemic_ipa"])
                self.assertTrue(row["source_url"].startswith("https://th.wiktionary.org/w/index.php?title="))
                self.assertTrue(row["source_revision"].isdigit())
                self.assertEqual(row["license"], "CC-BY-SA-4.0")
                self.assertEqual(row["status"], "SOURCE_ATTESTED_NOT_GOLD")
                self.assertIn("not expert-adjudicated", row["independence_note"])

    def test_source_attested_ipa_has_short_long_contrast_for_oe(self):
        path = ROOT / "data" / "benchmark" / "source-attested-ipa.tsv"
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            rows = {row["thai"]: row for row in csv.DictReader(stream, delimiter="\t")}
        self.assertIn("/ŋɤn˧/", rows["เงิน"]["phonemic_ipa"])
        self.assertIn("short /ɤ/", rows["เงิน"]["vowel_length_note"])
        self.assertIn("/dɤːn˧/", rows["เดิน"]["phonemic_ipa"])
        self.assertIn("long /ɤː/", rows["เดิน"]["vowel_length_note"])

    def test_ukraine_lexical_segmentation_source_is_pinned_and_not_gold(self):
        path = ROOT / "data" / "thai" / "text_lexicon_sources.csv"
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            rows = {row["word"]: row for row in csv.DictReader(stream)}
        row = rows["ยูเครน"]
        self.assertEqual(row["syllables"], "ยู|เครน")
        self.assertEqual(row["source_id"], "SRC-WIKTIONARY-EN-TH-ยูเครน")
        self.assertEqual(row["source_url"], "https://en.wiktionary.org/w/index.php?title=ยูเครน&oldid=88025965")
        self.assertEqual(row["source_revision"], "88025965")
        self.assertEqual(row["license"], "CC-BY-SA-4.0")
        self.assertEqual(row["status"], "SOURCE_ATTESTED")
        self.assertIn("not independently adjudicated gold", row["claim_scope"])

    def test_lexical_ipa_override_is_pinned_and_kept_separate_from_source_gold(self):
        path = ROOT / "data" / "thai" / "lexical_ipa_overrides.tsv"
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            overrides = list(csv.DictReader(stream, delimiter="\t"))
        self.assertEqual([row["word"] for row in overrides], ["เงิน", "เดิน"])
        row = overrides[0]
        self.assertEqual(row["segmental_ipa"], "ŋɤn")
        self.assertEqual(row["tone_category"], "mid")
        self.assertEqual(row["vowel_length"], "short")
        self.assertEqual(row["source_revision"], "5759179")
        self.assertEqual(row["license"], "CC-BY-SA-4.0")
        self.assertEqual(row["status"], "ACTIVE_SOURCE_ATTESTED_NOT_GOLD")
        walk = overrides[1]
        self.assertEqual(walk["segmental_ipa"], "dɤːn")
        self.assertEqual(walk["tone_category"], "mid")
        self.assertEqual(walk["vowel_length"], "long")
        self.assertEqual(walk["source_revision"], "1908803")
        self.assertEqual(walk["license"], "CC-BY-SA-4.0")
        self.assertEqual(walk["status"], "ACTIVE_SOURCE_ATTESTED_NOT_GOLD")


    def test_money_override_and_lexicon_source_registry_share_exact_revision(self):
        source_path = ROOT / "data" / "thai" / "text_lexicon_sources.csv"
        with source_path.open("r", encoding="utf-8-sig", newline="") as stream:
            source_rows = {row["word"]: row for row in csv.DictReader(stream)}
        row = source_rows["เงิน"]
        self.assertEqual(row["source_revision"], "5759179")
        self.assertEqual(row["source_url"], "https://th.wiktionary.org/w/index.php?title=เงิน&oldid=5759179")
        self.assertEqual(row["license"], "CC-BY-SA-4.0")
        self.assertEqual(row["status"], "ACTIVE_IPA_OVERRIDE_SOURCE_ATTESTED_NOT_GOLD")
        self.assertIn("not gold", row["claim_scope"])

if __name__ == "__main__":
    unittest.main()
