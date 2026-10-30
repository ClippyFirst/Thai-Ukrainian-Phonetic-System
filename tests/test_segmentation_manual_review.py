import csv
import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_segmentation_manual_review import build, strata

SOURCE_ID = "WISESIGHT1000-C1D063649ABC"
MODEL = {"model_id": "clippyfirst-tud-unigram-viterbi-v1",
         "source_license": "CC-BY-SA-4.0", "word_counts": {"ไทย": 3}, "token_penalty": 1.0}


class SegmentationManualReviewTests(unittest.TestCase):
    def _fixture(self, directory):
        path = Path(directory) / "gold.tsv"
        records = [
            {"id": "x1", "text": "Toyota ปี 2026!", "gold_tokens_json": json.dumps(["Toyota", " ", "ปี", " ", "2026", "!"], ensure_ascii=False)},
            {"id": "x2", "text": "ภาษาไทย", "gold_tokens_json": json.dumps(["ภาษา", "ไทย"], ensure_ascii=False)},
            {"id": "x3", "text": "brand", "gold_tokens_json": json.dumps(["brand"], ensure_ascii=False)},
            {"id": "x4", "text": "ไทยยาว" * 20, "gold_tokens_json": json.dumps(["ไทยยาว" * 20], ensure_ascii=False)},
        ]
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "text", "gold_tokens_json", "gold_status", "source_id", "license", "split"], delimiter="\t", lineterminator="\n")
            writer.writeheader()
            for row in records:
                writer.writerow({**row, "gold_status": "SOURCE_ANNOTATED", "source_id": SOURCE_ID, "license": "CC0-1.0", "split": "test"})
        report = {
            "report_type": "COMPARATIVE_SEGMENTATION_ERROR_TRIAGE_NOT_GOLD_ADJUDICATION",
            "dataset": {"rows_total": 4, "rows_source_annotated": 4, "rows_expert_adjudicated": 0,
                        "source_id": SOURCE_ID, "license": "CC0-1.0", "split": "test"},
            "models": {"dictionary_max_match": {}, "tud_unigram_viterbi": {}},
        }
        return path, records, report

    def test_strata_are_sampling_hints_not_decisions(self):
        tags = strata("Toyota ปี 2026 https://example.com ไทย!", ["a"], ["b"])
        self.assertIn("NUMERIC_OR_DATE_CANDIDATE", tags)
        self.assertIn("URL_OR_EMAIL_CANDIDATE", tags)
        self.assertIn("MIXED_LATIN_THAI_CANDIDATE", tags)
        self.assertIn("PUNCTUATION_OR_QUOTING_CANDIDATE", tags)
        self.assertIn("ENGINE_DISAGREEMENT", tags)

    def test_stratified_sample_is_deterministic_and_never_adjudicates(self):
        with tempfile.TemporaryDirectory() as d:
            gold, records, report = self._fixture(d)
            dictionary = lambda text: [text]
            tud = lambda text: [text[:2], text[2:]] if len(text) > 2 else [text]
            first = build(report, gold, MODEL, sample_per_stratum=2, control_sample=2,
                          seed="test-seed", dictionary_segmenter=dictionary, tud_segmenter=tud)
            second = build(report, gold, MODEL, sample_per_stratum=2, control_sample=2,
                           seed="test-seed", dictionary_segmenter=dictionary, tud_segmenter=tud)
        self.assertEqual([r["id"] for r in first], [r["id"] for r in second])
        self.assertTrue(first)
        self.assertTrue(any("UNIFORM_CONTROL" in r["sampled_for"] for r in first))
        self.assertEqual({r["id"] for r in first}, {r["id"] for r in second})
        for row in first:
            self.assertEqual(row["gold_status"], "SOURCE_ANNOTATED")
            self.assertEqual(row["adjudicated"], "NO")
            self.assertEqual(row["human_decision"], "")
            self.assertEqual(row["reviewer_id"], "")
            self.assertEqual(row["decision_rationale"], "")
            self.assertEqual("".join(json.loads(row["gold_tokens_json"])), row["text"])
            self.assertEqual("".join(json.loads(row["dictionary_tokens_json"])), row["text"])
            self.assertEqual("".join(json.loads(row["tud_tokens_json"])), row["text"])

    def test_rejects_wrong_model_provenance(self):
        with tempfile.TemporaryDirectory() as d:
            gold, _, report = self._fixture(d)
            with self.assertRaisesRegex(ValueError, "model identity"):
                build(report, gold, {**MODEL, "source_license": "UNKNOWN"},
                      dictionary_segmenter=lambda text: [text], tud_segmenter=lambda text: [text])

    def test_rejects_wrong_source_reconstruction(self):
        with tempfile.TemporaryDirectory() as d:
            gold, _, report = self._fixture(d)
            with self.assertRaisesRegex(ValueError, "reconstruction"):
                build(report, gold, MODEL, dictionary_segmenter=lambda text: ["WRONG"],
                      tud_segmenter=lambda text: [text])

if __name__ == "__main__":
    unittest.main()
