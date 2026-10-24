import tempfile
import unittest
from pathlib import Path

from scripts.run_external_g2p_benchmark import (
    build_inter_engine_diagnostic,
    has_usable_output,
    load_rows,
    normalized_ipa,
    parse_goruut_response,
    strip_tone_symbols_diagnostic,
    summarize_per_engine,
)


ROOT = Path(__file__).resolve().parents[1]


class ExternalG2PBenchmarkHarnessTests(unittest.TestCase):
    def test_challenge_corpus_is_parseable_and_gold_is_not_fabricated(self):
        rows = load_rows(ROOT / "data" / "benchmark" / "thai_g2p_challenge.jsonl")
        self.assertGreaterEqual(len(rows), 30)
        self.assertEqual(len({row["id"] for row in rows}), len(rows))
        self.assertTrue(all(row.get("gold_phonemic_ipa") is None for row in rows))
        self.assertTrue(all(row.get("gold_broad_surface_ipa") is None for row in rows))

    def test_empty_or_failed_result_is_not_a_successful_smoke_output(self):
        self.assertTrue(has_usable_output({"raw_output": "kaː", "error": None}))
        self.assertFalse(has_usable_output({"raw_output": "", "error": None}))
        self.assertFalse(has_usable_output({"raw_output": None, "error": "empty"}))
        self.assertFalse(has_usable_output({"raw_output": 12, "error": None}))

    def test_tone_stripping_is_diagnostic_only(self):
        self.assertEqual(strip_tone_symbols_diagnostic("/kaː˧/"), "/kaː/")
        self.assertEqual(strip_tone_symbols_diagnostic("/kaː/"), "/kaː/")
        self.assertIsNone(strip_tone_symbols_diagnostic(None))

    def test_inter_engine_diagnostic_separates_tone_only_disagreement(self):
        report = build_inter_engine_diagnostic([
            {"record_id":"tone", "raw_output":"/kaː˧/", "error":None},
            {"record_id":"tone", "raw_output":"/kaː˥/", "error":None},
            {"record_id":"segment", "raw_output":"/kaː/", "error":None},
            {"record_id":"segment", "raw_output":"/kʰaː/", "error":None},
            {"record_id":"failed", "raw_output":None, "error":"failed"},
            {"record_id":"empty", "raw_output":"", "error":None},
            {"record_id":"empty", "raw_output":"kaː", "error":None},
        ])
        self.assertEqual(report["comparable_inputs"], 2)
        self.assertEqual(report["engine_pairs_compared"], 2)
        self.assertEqual(report["exact_agreement_pairs"], 0)
        self.assertEqual(report["tone_stripped_agreement_pairs_diagnostic_only"], 1)
        self.assertEqual(report["tone_only_disagreements_diagnostic_only"], 1)
        self.assertEqual(report["non_tone_or_format_disagreements_requiring_review"], 1)
        self.assertIsNone(report.get("accuracy"))

    def test_goruut_parser_preserves_raw_word_phone_strings(self):
        self.assertEqual(
            parse_goruut_response({"Words": [
                {"CleanWord": "สวัสดี", "Phonetic": "sà.wàt.dii"},
                {"CleanWord": "ครับ", "Phonetic": "kʰráp"},
            ]}),
            "sà.wàt.dii kʰráp",
        )

    def test_goruut_parser_rejects_missing_or_malformed_word_output(self):
        with self.assertRaisesRegex(ValueError, "no Words array"):
            parse_goruut_response({"Words": []})
        with self.assertRaisesRegex(ValueError, "missing/non-string"):
            parse_goruut_response({"Words": [{"CleanWord": "x"}]})

    def test_per_engine_summary_exposes_failures_and_empty_outputs(self):
        report = summarize_per_engine([
            {"engine": "goruut", "record_id": "ok", "input": "กา", "raw_output": "kaː˧", "error": None},
            {"engine": "goruut", "record_id": "empty", "input": "xyz", "raw_output": "", "error": None},
            {"engine": "goruut", "record_id": "failed", "input": "abc", "raw_output": None, "error": "RuntimeError: failed"},
            {"engine": "thaiphon", "record_id": "ok", "input": "กา", "raw_output": "kaː", "error": None},
        ], ["goruut", "thaiphon"])
        self.assertEqual(report["goruut"]["output_rows"], 3)
        self.assertEqual(report["goruut"]["successful_outputs"], 1)
        self.assertEqual(report["goruut"]["failed_outputs"], 1)
        self.assertEqual(report["goruut"]["empty_outputs_without_error"], 1)
        self.assertEqual(report["goruut"]["failure_examples"][0]["record_id"], "failed")
        self.assertEqual(report["thaiphon"]["successful_outputs"], 1)

    def test_empty_challenge_corpus_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            empty = Path(temp_dir) / "empty.jsonl"
            empty.write_text("\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "contains no records"):
                load_rows(empty)

    def test_raw_ipa_normalization_only_trims_outer_whitespace(self):
        self.assertEqual(normalized_ipa("  kʰaː˥˩  "), "kʰaː˥˩")
        self.assertEqual(normalized_ipa("kʰaː.tɕʰa"), "kʰaː.tɕʰa")
        self.assertIsNone(normalized_ipa(None))


if __name__ == "__main__":
    unittest.main()
