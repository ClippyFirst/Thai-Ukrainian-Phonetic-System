import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CorpusSourceRegistryTests(unittest.TestCase):
    def test_ccost_wordlist_is_separately_catalogued_as_prompts_only(self):
        path = ROOT / "data" / "corpus_sources.csv"
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            rows = {row["source_id"]: row for row in csv.DictReader(stream)}
        row = rows["CORP-CCOST-WORDLIST"]
        self.assertEqual(row["type"], "controlled_wordlist")
        self.assertEqual(row["license_or_access"], "CC BY-NC-SA 4.0; non-commercial use only")
        self.assertIn("orthographic prompts only", row["annotation"])
        self.assertIn("no IPA", row["notes"])
        self.assertIn("source-order consistency must be audited", row["notes"])
        self.assertIn("MD5 e62f500d87b4ff8c6deb4c4595854d34", row["notes"])
        self.assertIn("206 data rows", row["notes"])

    def test_ccost_license_and_textgrid_access_are_explicit(self):
        path = ROOT / "data" / "corpus_sources.csv"
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            rows = {row["source_id"]: row for row in csv.DictReader(stream)}
        row = rows["CORP-CCOST"]
        self.assertEqual(row["license_or_access"], "CC BY-NC-SA 4.0; non-commercial use only")
        self.assertIn("6.2 GB", row["notes"])
        self.assertIn("TextGrid", row["notes"])
        self.assertIn("not bundled", row["notes"])
        self.assertIn("10.5281/zenodo.17366698", row["notes"])
        self.assertIn("10.63317/3ds35jijmgrx", row["notes"])
        self.assertIn("manual correction by trained native Thai research assistants", row["notes"])
        self.assertIn("no formal inter-annotator agreement measures", row["notes"])
        self.assertIn("CCOST_manual.pdf inspected 2026-11-01", row["notes"])
        self.assertIn("LREC 2026 paper specifies intended tiers ORT", row["notes"])
        self.assertIn("X-SAMPA", row["notes"])
        self.assertIn("tone numerals _1=Mid, _2=Low, _3=Falling, _4=High, _5=Rising", row["notes"])
        self.assertIn("no formal inter-annotator agreement", row["notes"])
        self.assertIn("actual released archive tier/label conformance and local sample mapping still require inspection", row["notes"])

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
        self.assertIn("CC-BY-SA-3.0 declared in pinned upstream dataset README", vistec["license_or_access"])
        self.assertIn("attribution/share-alike required", vistec["license_or_access"])
        self.assertIn("without bundling it", vistec["notes"])

    def test_thai_g2p_v4_source_scope_and_non_gold_status_are_explicit(self):
        path = ROOT / "data" / "corpus_sources.csv"
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            rows = {row["source_id"]: row for row in csv.DictReader(stream)}
        row = rows["CORP-THAI-G2P-V4"]
        self.assertIn("CC0-1.0 declared by dataset card", row["license_or_access"])
        self.assertIn("144849 rows", row["notes"])
        self.assertIn("8076 test", row["notes"])
        self.assertIn("Thai W2P and Wiktionary th-pron transliterator", row["notes"])
        self.assertIn("not independent expert/acoustic gold", row["notes"])
        self.assertIn("exclude circular rows", row["notes"])
        self.assertIn("do not bundle raw data", row["notes"])

    def test_best_and_lst20_are_not_silently_treated_as_redistributable(self):
        path = ROOT / "data" / "corpus_sources.csv"
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            rows = {row["source_id"]: row for row in csv.DictReader(stream)}
        lst20 = rows["CORP-LST20"]
        self.assertIn("verify exact upstream terms", lst20["license_or_access"])
        self.assertIn("do not use until license", lst20["notes"])
        self.assertIn("not bundled", lst20["notes"])


if __name__ == "__main__":
    unittest.main()
