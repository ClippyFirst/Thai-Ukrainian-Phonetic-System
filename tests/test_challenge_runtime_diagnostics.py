from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.run_challenge_diagnostics import build_report, load_challenge


class ChallengeRuntimeDiagnosticsTests(unittest.TestCase):
    def write_jsonl(self, directory: str, rows: list[dict]) -> Path:
        path = Path(directory) / "challenge.jsonl"
        path.write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
            encoding="utf-8",
        )
        return path

    def test_report_is_runtime_diagnostic_not_accuracy_score(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_jsonl(directory, [
                {"id": "known", "input": "กา", "stratum": "test"},
                {"id": "unknown", "input": "ไกล", "stratum": "test"},
            ])
            report = build_report(path)

        self.assertEqual(report["evaluation_kind"], "runtime_diagnostic_not_accuracy_benchmark")
        self.assertEqual(report["gold_status"], "NOT_ADJUDICATED")
        self.assertEqual(report["summary"]["challenge_inputs"], 2)
        self.assertEqual(
            report["summary"]["inputs_with_engine_output"]
            + report["summary"]["inputs_abstained_or_without_complete_output"],
            2,
        )
        self.assertNotIn("accuracy", report["summary"])
        records = {record["id"]: record for record in report["records"]}
        self.assertEqual(records["unknown"]["segmentation_status"], "unresolved")
        self.assertFalse(records["unknown"]["engine_output_emitted"])
        self.assertTrue(records["unknown"]["warnings"])

    def test_empty_challenge_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.jsonl"
            path.write_text("", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "challenge set is empty"):
                load_challenge(path)

    def test_duplicate_ids_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_jsonl(directory, [
                {"id": "same", "input": "กา"},
                {"id": "same", "input": "ไกล"},
            ])
            with self.assertRaisesRegex(ValueError, "duplicate id"):
                load_challenge(path)

    def test_invalid_json_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.jsonl"
            path.write_text('{"id": "x", "input": "กา"}\nnot-json\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "invalid JSON"):
                load_challenge(path)


if __name__ == "__main__":
    unittest.main()
