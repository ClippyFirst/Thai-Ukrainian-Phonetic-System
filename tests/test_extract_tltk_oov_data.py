from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.extract_tltk_oov_data import ASSET_NAMES, build


class TltkOovDataExtractionTests(unittest.TestCase):
    def test_extracts_pinned_oov_tables_to_json_safe_records(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fallback = Path(temporary)
            (fallback / "sylrule.lts").write_bytes("XOO,abc,T\n# ignored\n".encode("cp874"))
            (fallback / "thaisyl.dict").write_bytes("กา\tkaa0\n".encode("cp874"))
            (fallback / "PhSTrigram.sts").write_bytes("|-กา-กา/kaa0\t5\n".encode("cp874"))
            with (fallback / "sylseg.3g").open("wb") as target:
                pickle.dump({("|", "|", "กา"): 5, ("|", "กา", "|"): 2}, target)
            with (fallback / "thdict").open("wb") as target:
                pickle.dump({"กา": 1, "ขา": 1}, target)

            data, report = build(fallback)

            self.assertEqual(set(ASSET_NAMES), {
                "sylrule.lts", "thaisyl.dict", "PhSTrigram.sts",
                "sylseg.3g", "thdict",
            })
            self.assertNotIn("sylform_var.pkl", ASSET_NAMES)
            self.assertEqual(data["tltk_package_license"], "BSD-3-Clause")
            self.assertEqual(len(data["syllable_patterns"]), 1)
            self.assertEqual(data["syllable_dictionary"], [["กา", "kaa0"]])
            self.assertEqual(data["phone_trigrams"], [["|", "กา", "กา", "kaa0", 5.0]])
            self.assertEqual(len(data["syllable_trigrams"]), 2)
            self.assertEqual(data["word_dictionary"], ["ขา", "กา"])
            self.assertEqual(report["record_counts"]["word_dictionary"], 2)
            self.assertEqual(len(report["source_assets"]), 5)
            self.assertIn("sylform_var.pkl", report["excluded_assets"])

    def test_rejects_missing_source_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(FileNotFoundError):
                build(Path(temporary))


if __name__ == "__main__":
    unittest.main()
