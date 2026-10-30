import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "compare_segmentation_error_review.py"


class ComparativeSegmentationErrorReviewTests(unittest.TestCase):
    def test_tud_wrapper_preserves_mixed_text_and_segments_only_thai_runs(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        from importlib.util import module_from_spec, spec_from_file_location

        spec = spec_from_file_location("compare_segmentation_error_review", SCRIPT)
        module = module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        text = "ไทยABC ไทย"
        result = module.segment_tud_preserving(text, {"ไทย": 100}, 0.5)
        self.assertEqual("".join(result), text)
        self.assertEqual(result, ["ไทย", "ABC", " ", "ไทย"])

    def test_comparison_uses_same_source_annotated_rows_for_both_engines(self):
        with tempfile.TemporaryDirectory() as directory:
            model = Path(directory) / "model.json"
            output = Path(directory) / "report.json"
            model.write_text(json.dumps({
                "model_id": "clippyfirst-tud-unigram-viterbi-v1",
                "source_commit": "67413969add552b7030184f16f24fa9f630913bc",
                "source_license": "CC-BY-SA-4.0",
                "token_penalty": 0.5,
                "word_counts": {"ภาษา": 100, "ไทย": 100, "ประเทศไทย": 10},
            }), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--tud-model", str(model), "--output", str(output), "--examples-per-error", "2"],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(report["report_type"], "COMPARATIVE_SEGMENTATION_ERROR_TRIAGE_NOT_GOLD_ADJUDICATION")
        self.assertEqual(report["dataset"]["rows_total"], 993)
        self.assertTrue(report["dataset"]["same_rows_for_both_engines"])
        self.assertEqual(report["dataset"]["rows_expert_adjudicated"], 0)
        self.assertEqual(set(report["models"]), {"dictionary_max_match", "tud_unigram_viterbi"})
        for model_result in report["models"].values():
            self.assertGreater(model_result["metrics"]["false_split_count"], 0)
            self.assertGreater(model_result["metrics"]["false_merge_count"], 0)
            self.assertLessEqual(len(model_result["false_split_examples"]), 2)
            self.assertLessEqual(len(model_result["false_merge_examples"]), 2)
        self.assertIn("not independently expert-adjudicated", " ".join(report["method"]["caveats"]))


if __name__ == "__main__":
    unittest.main()
