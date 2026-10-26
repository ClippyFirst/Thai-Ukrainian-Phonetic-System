"""Validate source scope for Thai special orthography.

The teaching source supports the syllabic/lexical status of these letters; it
does not provide a universal IPA mapping for every word containing them.
"""
import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class SpecialOrthographyEvidenceTests(unittest.TestCase):
    def test_special_vowel_letter_rules_link_to_official_source_without_overclaiming(self):
        sources = {row["source_id"]: row for row in _rows(ROOT / "data/thai/sources.csv")}
        claims = {row["claim_id"]: row for row in _rows(ROOT / "data/claims.csv")}
        rules = {row["rule_id"]: row for row in _rows(ROOT / "data/thai/special_orthography.csv")}

        source_id = "SRC-OBEC-SPECIAL-VOWELS-2022"
        self.assertIn(source_id, sources)
        source = sources[source_id]
        self.assertEqual(source["url"], "https://academic.obec.go.th/images/document/1649040986_d_1.pdf")
        self.assertIn("p. 5", source["notes"])
        claim = claims["CLM-SPECIAL-VOWEL-LETTERS"]
        self.assertEqual(claim["status"], "analysis-dependent")
        self.assertIn(source_id, claim["evidence_ids"].split(";"))

        for rule_id in ("SP-RUE-001", "SP-RUE-LONG-001", "SP-LUE-001", "SP-LUE-LONG-001"):
            with self.subTest(rule_id=rule_id):
                rule = rules[rule_id]
                self.assertEqual(rule["analysis_status"], "analysis-dependent")
                self.assertIn(source_id, rule["source_ids"].split(";"))
                self.assertIn("word-level evidence", rule["notes"])

    def test_leading_o_claim_is_scoped_to_the_attested_lexical_family(self):
        sources = {row["source_id"]: row for row in _rows(ROOT / "data/thai/sources.csv")}
        claims = {row["claim_id"]: row for row in _rows(ROOT / "data/claims.csv")}
        rules = {row["rule_id"]: row for row in _rows(ROOT / "data/thai/special_orthography.csv")}

        source_id = "SRC-OBEC-O-NAM-2022"
        claim = claims["CLM-O-NAM-LEXICAL"]
        rule = rules["SP-O-NAM-001"]
        self.assertIn(source_id, sources)
        self.assertEqual(claim["status"], "analysis-dependent")
        self.assertIn(source_id, claim["evidence_ids"].split(";"))
        self.assertIn(source_id, rule["source_ids"].split(";"))
        self.assertIn("p. 275", rule["notes"])
        self.assertIn("do not generalize", rule["notes"])
        self.assertEqual(sources[source_id]["url"], "https://academic.obec.go.th/web/images/document/1650944942_d_1.pdf")
        self.assertIn("printed p. 275", sources[source_id]["notes"])


if __name__ == "__main__":
    unittest.main()
