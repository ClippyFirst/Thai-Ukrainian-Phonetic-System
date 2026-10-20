import unittest
from pathlib import Path

from scripts.run_external_g2p_benchmark import load_rows, normalized_ipa


ROOT = Path(__file__).resolve().parents[1]


class ExternalG2PBenchmarkHarnessTests(unittest.TestCase):
    def test_challenge_corpus_is_parseable_and_gold_is_not_fabricated(self):
        rows = load_rows(ROOT / "data" / "benchmark" / "thai_g2p_challenge.jsonl")
        self.assertGreaterEqual(len(rows), 30)
        self.assertEqual(len({row["id"] for row in rows}), len(rows))
        self.assertTrue(all(row.get("gold_phonemic_ipa") is None for row in rows))
        self.assertTrue(all(row.get("gold_broad_surface_ipa") is None for row in rows))

    def test_raw_ipa_normalization_only_trims_outer_whitespace(self):
        self.assertEqual(normalized_ipa("  kʰaː˥˩  "), "kʰaː˥˩")
        self.assertEqual(normalized_ipa("kʰaː.tɕʰa"), "kʰaː.tɕʰa")
        self.assertIsNone(normalized_ipa(None))


if __name__ == "__main__":
    unittest.main()
