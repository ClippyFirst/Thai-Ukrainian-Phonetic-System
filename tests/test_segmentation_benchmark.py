import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "evaluate_segmentation.py"
GOLD_FIELDS = ["id", "text", "gold_tokens_json", "gold_status", "source_id", "license", "split"]
PRED_FIELDS = ["id", "engine", "predicted_tokens_json", "status", "version"]


def write_tsv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


class SegmentationBenchmarkTests(unittest.TestCase):
    def run_benchmark(self, gold_rows, pred_rows, expected=0):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            gold, predictions, output = root / "gold.tsv", root / "pred.tsv", root / "report.json"
            write_tsv(gold, GOLD_FIELDS, gold_rows)
            write_tsv(predictions, PRED_FIELDS, pred_rows)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--gold", str(gold), "--predictions", str(predictions), "--output", str(output)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(result.returncode, expected, result.stderr)
            if expected:
                return result.stderr
            return json.loads(output.read_text(encoding="utf-8"))

    @staticmethod
    def gold(row_id="g1", text="ภาษาไทย", tokens=None, **overrides):
        row = {
            "id": row_id, "text": text, "gold_tokens_json": json.dumps(tokens if tokens is not None else ["ภาษา", "ไทย"], ensure_ascii=False),
            "gold_status": "ADJUDICATED", "source_id": "fixture#1", "license": "CC0-1.0", "split": "test",
        }
        row.update(overrides)
        return row

    @staticmethod
    def prediction(row_id="g1", tokens=None, **overrides):
        row = {
            "id": row_id, "engine": "test-engine",
            "predicted_tokens_json": json.dumps(tokens if tokens is not None else ["ภาษา", "ไทย"], ensure_ascii=False),
            "status": "ok", "version": "test",
        }
        row.update(overrides)
        return row

    def test_adjudicated_gold_requires_nonempty_text(self):
        self.assertIn("requires non-empty text", self.run_benchmark([self.gold(text="")], [], expected=1))

    def test_prediction_requires_status_and_version(self):
        bad = self.prediction(version="")
        self.assertIn("status and version must be non-empty", self.run_benchmark([self.gold()], [bad], expected=1))

    def test_duplicate_nonadjudicated_gold_ids_are_rejected(self):
        first = self.gold(gold_status="SOURCE_ATTESTED")
        second = self.gold(gold_status="ADJUDICATED")
        self.assertIn("must be non-empty and unique", self.run_benchmark([first, second], [], expected=1))

    def test_exact_segmentation_scores_one(self):
        report = self.run_benchmark([self.gold()], [self.prediction()])
        metrics = report["engines"]["test-engine"]
        self.assertEqual(metrics["exact_sequence_rate"], 1.0)
        self.assertEqual(metrics["boundary_f1"], 1.0)
        self.assertEqual(metrics["coverage"], 1.0)

    def test_boundary_error_and_exact_sequence_are_separate(self):
        gold = self.gold(text="ภาษาไทย", tokens=["ภาษา", "ไทย"])
        pred = self.prediction(tokens=["ภา", "ษาไทย"])
        report = self.run_benchmark([gold], [pred])
        metrics = report["engines"]["test-engine"]
        self.assertEqual(metrics["exact_sequence_rate"], 0.0)
        self.assertEqual(metrics["boundary_tp"], 0)
        self.assertEqual(metrics["boundary_fp"], 1)
        self.assertEqual(metrics["boundary_fn"], 1)

    def test_missing_prediction_stays_in_denominator(self):
        report = self.run_benchmark([self.gold()], [])
        self.assertEqual(report["gold"]["rows_adjudicated"], 1)
        self.assertEqual(report["engines"], {})
        # An engine represented elsewhere must still score the omitted gold item as a miss.
        gold = [self.gold(), self.gold(row_id="g2", text="ภาษาไทยดี", tokens=["ภาษา", "ไทย", "ดี"])]
        pred = [self.prediction(row_id="g2", tokens=["ภาษา", "ไทย", "ดี"])]
        metrics = self.run_benchmark(gold, pred)["engines"]["test-engine"]
        self.assertEqual(metrics["n_adjudicated_gold_rows"], 2)
        self.assertEqual(metrics["nonempty_predictions"], 1)
        self.assertEqual(metrics["exact_sequence_rate"], 0.5)

    def test_non_success_status_cannot_score_stale_prediction_tokens(self):
        # Even an exact-looking token array is not a prediction when the engine
        # reported an error/abstention; stale or partial data must not score.
        failed = self.prediction(status="error", tokens=["ภาษา", "ไทย"])
        metrics = self.run_benchmark([self.gold()], [failed])["engines"]["test-engine"]
        self.assertEqual(metrics["coverage"], 0.0)
        self.assertEqual(metrics["exact_sequence_rate"], 0.0)
        self.assertEqual(metrics["boundary_tp"], 0)
        self.assertEqual(metrics["boundary_fn"], 1)
        self.assertEqual(metrics["non_success_status_rows"], 1)

    def test_empty_prediction_array_is_counted_as_abstention(self):
        report = self.run_benchmark([self.gold()], [self.prediction(tokens=[])])
        metrics = report["engines"]["test-engine"]
        self.assertEqual(metrics["coverage"], 0.0)
        self.assertEqual(metrics["exact_sequence_rate"], 0.0)
        self.assertEqual(metrics["boundary_fn"], 1)

    def test_zero_predicted_boundaries_with_gold_boundaries_has_zero_f1(self):
        gold = self.gold(text="ภาษาไทย", tokens=["ภาษา", "ไทย"])
        pred = self.prediction(tokens=["ภาษาไทย"])
        metrics = self.run_benchmark([gold], [pred])["engines"]["test-engine"]
        self.assertEqual(metrics["boundary_tp"], 0)
        self.assertEqual(metrics["boundary_fp"], 0)
        self.assertEqual(metrics["boundary_fn"], 1)
        self.assertIsNone(metrics["boundary_precision"])
        self.assertEqual(metrics["boundary_recall"], 0.0)
        self.assertEqual(metrics["boundary_f1"], 0.0)

    def test_single_token_without_boundaries_reports_undefined_boundary_metrics(self):
        gold = self.gold(text="ไทย", tokens=["ไทย"])
        pred = self.prediction(tokens=["ไทย"])
        metrics = self.run_benchmark([gold], [pred])["engines"]["test-engine"]
        self.assertEqual(metrics["exact_sequence_rate"], 1.0)
        self.assertIsNone(metrics["boundary_precision"])
        self.assertIsNone(metrics["boundary_recall"])
        self.assertIsNone(metrics["boundary_f1"])

    def test_no_gold_is_not_zero_accuracy(self):
        report = self.run_benchmark([self.gold(gold_status="SOURCE_ATTESTED")], [self.prediction()])
        self.assertEqual(report["gold"]["status"], "NOT_MEASURED")
        self.assertIsNone(report["engines"]["test-engine"]["exact_sequence_rate"])

    def test_adjudicated_rows_require_provenance_and_valid_concatenation(self):
        bad_source = self.gold(source_id="")
        self.assertIn("requires source_id", self.run_benchmark([bad_source], [], expected=1))
        bad_tokens = self.gold(tokens=["ภาษา", "ไท"])
        self.assertIn("does not concatenate", self.run_benchmark([bad_tokens], [], expected=1))

    def test_unicode_is_not_silently_normalized_away(self):
        # Decomposed input is NFC-normalized, but token boundaries must still cover the same text.
        decomposed = "e\u0301x"
        row = self.gold(text=decomposed, tokens=["é", "x"])
        report = self.run_benchmark([row], [self.prediction(tokens=["é", "x"])])
        self.assertEqual(report["engines"]["test-engine"]["exact_sequence_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
