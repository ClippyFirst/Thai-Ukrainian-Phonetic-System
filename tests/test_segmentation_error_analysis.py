import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "analyze_segmentation_errors.py"


class SegmentationErrorAnalysisTests(unittest.TestCase):
    def test_whitespace_boundaries_are_not_lexical_boundaries(self):
        # The boundary around the space is excluded, while the Thai word
        # boundary after ภาษา is retained.
        from importlib.util import module_from_spec, spec_from_file_location

        spec = spec_from_file_location("segmentation_error_analysis", SCRIPT)
        module = module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        self.assertEqual(module.boundary_offsets(["ภาษา", " ", "ไทย"]), set())
        self.assertEqual(module.boundary_offsets(["ภาษา", "ไทย"]), {4})

    def test_report_preserves_source_annotation_grade_and_error_examples(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "error-review.json"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--output", str(output), "--examples-per-error", "3"],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(report["report_type"], "SEGMENTATION_ERROR_TRIAGE_NOT_GOLD_ADJUDICATION")
        self.assertEqual(report["dataset"]["rows_total"], 993)
        self.assertEqual(report["dataset"]["rows_source_annotated"], 993)
        self.assertEqual(report["dataset"]["rows_expert_adjudicated"], 0)
        self.assertEqual(report["dataset"]["license"], "CC0-1.0")
        self.assertGreater(report["metrics"]["false_split_count"], 0)
        self.assertGreater(report["metrics"]["false_merge_count"], 0)
        self.assertEqual(len(report["false_split_examples"]), 3)
        self.assertEqual(len(report["false_merge_examples"]), 3)
        self.assertIn("not independently expert-adjudicated", " ".join(report["method"]["caveats"]))


if __name__ == "__main__":
    unittest.main()
