import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CorpusSourceRegistryTests(unittest.TestCase):
    def test_segmentation_sources_preserve_license_and_usage_gates(self):
        path = ROOT / "data" / "corpus_sources.csv"
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            rows = {row["source_id"]: row for row in csv.DictReader(stream)}
        wisesight = rows["CORP-WISESIGHT-1000"]
        self.assertEqual(wisesight["license_or_access"], "CC0-1.0")
        self.assertIn("993 source-annotated rows", wisesight["notes"])
        self.assertIn("test-only", wisesight["notes"])
        self.assertIn("not independently expert-adjudicated", wisesight["notes"])

        lst20 = rows["CORP-LST20"]
        self.assertIn("verify exact upstream terms", lst20["license_or_access"])
        self.assertIn("not bundled", lst20["notes"])
        self.assertIn("license", lst20["notes"])

        vistec = rows["CORP-VISTEC-TP-TH-2021"]
        self.assertIn("CC BY-SA 3.0 reported", vistec["license_or_access"])
        self.assertIn("verify upstream terms", vistec["license_or_access"])
        self.assertIn("not bundled", vistec["notes"])


if __name__ == "__main__":
    unittest.main()
