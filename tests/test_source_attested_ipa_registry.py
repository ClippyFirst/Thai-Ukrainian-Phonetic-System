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


if __name__ == "__main__":
    unittest.main()
