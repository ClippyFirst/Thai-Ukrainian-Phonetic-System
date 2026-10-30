"""Tests for repeatability diagnostics and machine-readable CLI output."""
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from scripts import probe_goruut_repeatability as probe


class GoruutRepeatabilityTests(unittest.TestCase):
    def test_repeatability_reports_distinct_outputs_without_claiming_accuracy(self):
        case = probe.summarize_case("TH-G2P-001", "กา", [
            {"repeat_index": 1, "phonetic_output": "kaː˧", "error": None},
            {"repeat_index": 2, "phonetic_output": "ka", "error": None},
            {"repeat_index": 3, "phonetic_output": "kaː˧", "error": None},
        ])
        self.assertEqual(case["successful_nonempty_calls"], 3)
        self.assertEqual(case["unique_nonempty_outputs"], 2)
        self.assertTrue(case["varies_across_repetitions"])
        self.assertEqual(case["distinct_outputs"], ["ka", "kaː˧"])
        self.assertEqual(case["status"], "VARIABLE_OUTPUT")

    def test_repeatability_does_not_count_empty_or_failed_outputs_as_success(self):
        case = probe.summarize_case("TH-G2P-015", "ทฤษฎี", [
            {"repeat_index": 1, "phonetic_output": None, "error": None},
            {"repeat_index": 2, "phonetic_output": None, "error": "RuntimeError"},
        ])
        self.assertEqual(case["successful_nonempty_calls"], 0)
        self.assertEqual(case["unique_nonempty_outputs"], 0)
        self.assertEqual(case["status"], "NO_NONEMPTY_OUTPUT")

    def test_cli_stdout_and_uploaded_summary_are_valid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "repeatability.json"
            stdout, stderr = io.StringIO(), io.StringIO()
            argv = [
                "probe_goruut_repeatability.py", "--url", "http://127.0.0.1:18080/test",
                "--input", str(Path(tmp) / "unused.jsonl"), "--output", str(output_path), "--repeats", "2",
            ]
            with patch.object(probe.sys, "argv", argv), \
                 patch.object(probe, "load_rows", return_value=[{"id": "TH-TEST-1", "input": "กา"}]), \
                 patch.object(probe, "query", return_value={"Words": [{"Phonetic": "kaː˧"}],
                     "RandomizationWordsCount": 0, "RandomizationWordsChoices": []}), \
                 redirect_stdout(stdout), redirect_stderr(stderr):
                result = probe.main()
            self.assertEqual(result, 0)
            summary = json.loads(stdout.getvalue())
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(summary["attempt_count"], 2)
            self.assertEqual(report["input_count"], 1)
            self.assertIn("Repeatability report:", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
