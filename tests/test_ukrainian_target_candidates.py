import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "benchmark" / "ukrainian-target-candidates.tsv"


class UkrainianTargetCandidateRegistryTests(unittest.TestCase):
    def test_registry_is_source_backed_and_not_mislabeled_as_gold(self):
        with REGISTRY.open("r", encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream, delimiter="\t"))
        self.assertEqual(len(rows), 6)
        self.assertEqual({row["candidate_status"] for row in rows}, {"ENGINE_CANDIDATE_NOT_PREFERENCE_GOLD"})
        self.assertTrue(all(row["source_url"].startswith("https://th.wiktionary.org/") for row in rows))
        self.assertTrue(all(row["source_revision"] for row in rows))
        self.assertTrue(all(row["license"] == "CC-BY-SA-4.0" for row in rows))
        self.assertEqual(next(row for row in rows if row["thai"] == "เงิน")["ua_candidate"], "нген")
        self.assertEqual(next(row for row in rows if row["thai"] == "บรรจุ")["ua_candidate"], "бан.чу")
        self.assertTrue(all("not independently adjudicated" in row["evidence_note"] for row in rows))


if __name__ == "__main__":
    unittest.main()
