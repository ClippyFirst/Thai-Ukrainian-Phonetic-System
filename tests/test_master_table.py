from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class MasterTableTests(unittest.TestCase):
    def _generator(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import generate_master_table as gm
        return gm

    def test_generator_produces_exact_structural_cardinality(self):
        gm = self._generator()
        with tempfile.TemporaryDirectory() as d:
            old = gm.OUT
            gm.OUT = Path(d)
            try:
                report = gm.build()
                self.assertEqual(report["rows"], 343200)
                self.assertEqual(report["expected_rows"], 343200)
                with (Path(d)/"thai_ukrainian_master.csv").open(encoding="utf-8",newline="") as f:
                    self.assertEqual(sum(1 for _ in f)-1, 343200)
                with (Path(d)/"thai_ukrainian_master_2col.csv").open(encoding="utf-8",newline="") as f:
                    self.assertEqual(sum(1 for _ in f)-1, 343200)
            finally:
                gm.OUT = old

    def test_two_column_view_is_derived_from_rich_table(self):
        gm = self._generator()
        with tempfile.TemporaryDirectory() as d:
            old = gm.OUT
            gm.OUT = Path(d)
            try:
                gm.build()
                with (Path(d)/"thai_ukrainian_master.csv").open(encoding="utf-8",newline="") as a, (Path(d)/"thai_ukrainian_master_2col.csv").open(encoding="utf-8",newline="") as b:
                    rich, simple = csv.DictReader(a), csv.DictReader(b)
                    for _ in range(50):
                        x, y = next(rich), next(simple)
                        self.assertEqual((x["thai"],x["ukrainian"]), (y["Thai"],y["Ukrainian"]))
            finally:
                gm.OUT = old

    def test_ipa_first_manifest(self):
        gm = self._generator()
        with tempfile.TemporaryDirectory() as d:
            old = gm.OUT
            gm.OUT = Path(d)
            try:
                report = gm.build()
                self.assertEqual(report["principle"], "Thai orthography → phonology → IPA → Ukrainian approximation")
            finally:
                gm.OUT = old

    def test_distinct_rime_records_do_not_collapse_to_same_surface(self):
        gm = self._generator()
        vowels = {v["id"]: v for v in gm.rows("vowels.csv")}
        self.assertEqual(gm.surface_for("ก", vowels["V-X-AJ"], None, ""), "กาย")
        self.assertEqual(gm.surface_for("ก", vowels["V-X-OY"], None, ""), "กอย")
        self.assertNotEqual(
            gm.surface_for("ก", vowels["V-X-AJ"], None, ""),
            gm.surface_for("ก", vowels["V-X-OY"], None, ""),
        )

if __name__ == "__main__":
    unittest.main()
