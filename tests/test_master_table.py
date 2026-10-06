from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MasterTableTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(ROOT / "scripts"))
        cls.gm = __import__("generate_master_table")
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name)
        old = cls.gm.OUT
        cls.gm.OUT = cls.out
        try:
            cls.report = cls.gm.build()
        finally:
            cls.gm.OUT = old

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_generator_produces_exact_structural_cardinality(self):
        self.assertEqual(self.report["rows"], 351780)
        self.assertEqual(self.report["expected_rows"], 351780)
        with (self.out / "thai_ukrainian_master.csv").open(encoding="utf-8", newline="") as f:
            self.assertEqual(sum(1 for _ in f) - 1, 351780)
        with (self.out / "thai_ukrainian_master_2col.csv").open(encoding="utf-8", newline="") as f:
            self.assertEqual(sum(1 for _ in f) - 1, 351780)

    def test_two_column_view_is_derived_from_rich_table(self):
        with (
            (self.out / "thai_ukrainian_master.csv").open(encoding="utf-8", newline="") as a,
            (self.out / "thai_ukrainian_master_2col.csv").open(encoding="utf-8", newline="") as b,
        ):
            rich, simple = csv.DictReader(a), csv.DictReader(b)
            for _ in range(100):
                x, y = next(rich), next(simple)
                self.assertEqual((x["thai"], x["ukrainian"]), (y["Thai"], y["Ukrainian"]))

    def test_ipa_first_manifest(self):
        self.assertIn("IPA-first", self.report["principle"])
        self.assertIn("phonology → tone", self.report["principle"])
        self.assertIn("IPA → Ukrainian phonetic target", self.report["principle"])

    def test_surface_rows_are_revalidated_not_trusted_blindly(self):
        vowels = {v["id"]: v for v in self.gm.rows("vowels.csv")}
        self.assertEqual(self.gm.surface_for("ก", vowels["V-X-AJ"], None, ""), "กาย")
        self.assertEqual(self.gm.surface_for("ก", vowels["V-X-OY"], None, ""), "กอย")
        self.assertNotEqual(
            self.gm.surface_for("ก", vowels["V-X-AJ"], None, ""),
            self.gm.surface_for("ก", vowels["V-X-OY"], None, ""),
        )
