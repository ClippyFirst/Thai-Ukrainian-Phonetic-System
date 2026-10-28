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
                # Guard the positional CSV schema as well as provenance: a
                # shifted row can silently turn candidate IPA into a status.
                expected_patterns = {
                    "SP-RUE-001": "ฤ",
                    "SP-RUE-LONG-001": "ฤๅ",
                    "SP-LUE-001": "ฦ",
                    "SP-LUE-LONG-001": "ฦๅ",
                }
                expected_candidates = {
                    "SP-RUE-001": "rɯ|ri|rɤ",
                    "SP-RUE-LONG-001": "rɯː",
                    "SP-LUE-001": "lɯ",
                    "SP-LUE-LONG-001": "lɯː",
                }
                self.assertEqual(rule["pattern"], expected_patterns[rule_id])
                self.assertEqual(rule["analysis_status"], "analysis-dependent")
                self.assertEqual(rule["candidate_ipa"], expected_candidates[rule_id])

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


    def test_ambiguous_orthography_fails_closed_for_unlisted_forms(self):
        from thai_ukrainian.parser import parse_syllable

        # These are ambiguity sentinels, not proposed pronunciations. Each
        # family has source-backed lexical exceptions, but the spelling alone
        # is insufficient to choose one reading for these generic probes.
        cases = {
            "ทราย": "ทร lexical reading is sense/context dependent",
            "จร": "written ร may be silent in established lexical forms",
            "สร": "written ร may be silent in established lexical forms",
            "ศร": "written ร may be silent in established lexical forms",
            "ซร": "written ร may be silent in established lexical forms",
            "ฤ": "special vowel letter requires word-level evidence",
            "ฤๅ": "special vowel letter requires word-level evidence",
            "ฦ": "rare special vowel letter requires word-level evidence",
            "ฦๅ": "rare special vowel letter requires word-level evidence",
            "ก์": "thanthakhat scope cannot be guessed from the mark alone",
        }
        for text, reason in cases.items():
            with self.subTest(text=text):
                result = parse_syllable(text)
                self.assertEqual(result.status, "analysis-dependent:special-orthography", (text, result.status, result.warnings))
                self.assertIsNone(result.phonemic_ipa, (text, reason, result.phonemic_ipa))
                self.assertIsNone(result.phonetic_ipa, (text, reason, result.phonetic_ipa))

    def test_exact_lexical_thor_reading_does_not_become_a_productive_rule(self):
        from thai_ukrainian.api import analyze_syllable

        known = analyze_syllable("ทราบ")
        ambiguous = analyze_syllable("ทราย")
        self.assertEqual(known.status, "analyzed")
        self.assertEqual(known.normalized, "ซาบ")
        self.assertIsNotNone(known.phonemic_ipa)
        self.assertEqual(ambiguous.status, "analysis-dependent:special-orthography")
        self.assertIsNone(ambiguous.phonemic_ipa)


    def test_source_attested_false_cluster_and_thor_lexemes_are_exact_not_productive(self):
        from thai_ukrainian.parser import parse_syllable

        # The Royal Institute article discusses these as lexical readings,
        # not a productive replacement rule for every spelling containing ร.
        # This guards the known exceptions while the generic-family sentinels
        # above continue to fail closed.
        expected = {
            "จริง": "จิง",
            "สร้าง": "ส้าง",
            "ศรี": "สี",
            "เศร้า": "เส้า",
            "ไซร้": "ไซ้",
            "ทราบ": "ซาบ",
            "ทรง": "ซง",
            "ทรัพย์": "ซับ",
            "แทรก": "แซก",
        }
        source_rows = {row["source_id"]: row for row in _rows(ROOT / "data/thai/sources.csv")}
        source_id = "SRC-ORST-CLUSTER-2011"
        self.assertIn(source_id, source_rows)
        self.assertIn("2011", source_rows[source_id]["url"])
        self.assertIn("lexical reading evidence only", source_rows[source_id]["notes"])

        for word, normalized in expected.items():
            with self.subTest(word=word):
                result = parse_syllable(word)
                self.assertEqual(result.status, "analyzed", (word, result.status, result.warnings))
                self.assertEqual(result.normalized, normalized)
                self.assertIsNotNone(result.phonemic_ipa, (word, result.warnings))


if __name__ == "__main__":
    unittest.main()
