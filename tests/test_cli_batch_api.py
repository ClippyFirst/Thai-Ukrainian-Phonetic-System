from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from thai_ukrainian.batch import analyze_input, load_batch, write_batch
from thai_ukrainian.cli import main


class CliBatchApiTests(unittest.TestCase):
    def test_analyze_input_has_stable_top_level_fields(self):
        result = analyze_input("กา")
        for key in ("input", "status", "analyses", "ipa", "phonetic_ipa", "tones", "tone_ipa", "ukrainian_orthography", "warnings"):
            self.assertIn(key, result)

    def test_txt_batch_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = root / "input.txt"
            output = root / "output.jsonl"
            source.write_text("กา\nนา\n", encoding="utf-8")
            rows = load_batch(source)
            self.assertEqual([r["thai"] for r in rows], ["กา", "นา"])
            results = [analyze_input(r["thai"]) | {"id": r["id"]} for r in rows]
            write_batch(results, output)
            records = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(records), 2)
            self.assertEqual(records[0]["input"], "กา")

    def test_csv_batch(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = root / "input.csv"
            output = root / "output.csv"
            with source.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["thai", "note"])
                writer.writeheader()
                writer.writerow({"thai": "กา", "note": "fixture"})
            main(["batch", str(source), "-o", str(output)])
            with output.open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["input"], "กา")

    def test_cli_analyze(self):
        with patch("builtins.print") as mocked:
            self.assertEqual(main(["analyze", "กา", "--compact"]), 0)
            payload = json.loads(mocked.call_args.args[0])
            self.assertEqual(payload["input"], "กา")


if __name__ == "__main__":
    unittest.main()
