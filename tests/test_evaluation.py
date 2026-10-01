import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from thai_ukrainian.evaluation import load_records, evaluate_records


class EvaluationTestsclass EvaluationCliTests(unittest.TestCase):
    def test_loads_jsonl_records(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "gold.jsonl"
            p.write_text(json.dumps({"id":"x1","thai":"กา","ipa":"kaː","tone":"mid","source":"fixture"}, ensure_ascii=False)+"\n", encoding="utf-8")
            self.assertEqual(load_records(p)[0]["id"], "x1")

    def test_rejects_missing_required_fields(self):
        with self.assertRaises(ValueError):
            evaluate_records([{"id":"x1","thai":"กา"}])

    def test_reports_exact_ipa_and_tone_accuracy(self):
        records = [
            {"id":"x1","thai":"กา","ipa":"kaː","tone":"mid","source":"fixture"},
            {"id":"x2","thai":"กา","ipa":"wrong","tone":"low","source":"fixture"},
        ]
        r = evaluate_records(records)
        self.assertEqual(r["records_total"], 2)
        self.assertEqual(r["records_evaluable"], 2)
        self.assertEqual(r["ipa_exact_accuracy"], 0.5)
        self.assertEqual(r["tone_accuracy"], 0.5)

    def test_missing_gold_fields_are_excluded_from_that_metric(self):
        records = [{"id":"x1","thai":"กา","source":"fixture"}]
        r = evaluate_records(records)
        self.assertEqual(r["records_total"], 1)
        self.assertEqual(r["records_evaluable"], 1)
        self.assertIsNone(r["ipa_exact_accuracy"])
        self.assertIsNone(r["tone_accuracy"])


(unittest.TestCase):
    def test_cli_emits_machine_readable_metrics(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "gold.jsonl"
            p.write_text(json.dumps({"id":"x1","thai":"กา","ipa":"kaː","tone":"mid","source":"fixture"}, ensure_ascii=False)+"\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "scripts/evaluate_corpus.py", str(p)],
                capture_output=True, text=True, check=False
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["ipa_exact_accuracy"], 1.0)
            self.assertEqual(payload["tone_accuracy"], 1.0)

if __name__ == "__main__":
    unittest.main()
