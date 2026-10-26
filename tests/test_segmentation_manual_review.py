import csv, json, tempfile, unittest
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_segmentation_manual_review import build, strata

class SegmentationManualReviewTests(unittest.TestCase):
    def test_strata_are_hints_not_decisions(self):
        tags = strata("Toyota ปี 2026 https://example.com ไทย", ["a"], ["b"])
        self.assertIn("NUMERIC_OR_DATE_CANDIDATE", tags)
        self.assertIn("URL_OR_EMAIL_CANDIDATE", tags)
        self.assertIn("MIXED_LATIN_THAI_CANDIDATE", tags)
        self.assertIn("ENGINE_DISAGREEMENT", tags)

    def test_review_rows_require_both_predictions_and_keep_unadjudicated_state(self):
        with tempfile.TemporaryDirectory() as d:
            gold = Path(d) / "gold.tsv"
            text = "ไทยABC 2026"
            with gold.open("w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=["id","text","gold_tokens_json"], delimiter="\t")
                w.writeheader()
                w.writerow({"id":"x","text":text,"gold_tokens_json":json.dumps(["ไทย","ABC"," ","2026"],ensure_ascii=False)})
            ex = {"id":"x","predicted_tokens":["ไทย","ABC"," ","2026"]}
            report = {"report_type":"COMPARATIVE_SEGMENTATION_ERROR_TRIAGE_NOT_GOLD_ADJUDICATION",
              "dataset":{"rows_expert_adjudicated":0,"rows_source_annotated":993},
              "models":{"dictionary_max_match":{"false_split_examples":[ex],"false_merge_examples":[]},
                        "tud_unigram_viterbi":{"false_split_examples":[],"false_merge_examples":[ex]}}}
            rows = build(report, gold)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["gold_status"], "SOURCE_ANNOTATED")
        self.assertEqual(rows[0]["adjudicated"], "NO")
        self.assertEqual(rows[0]["human_decision"], "")
        self.assertEqual(rows[0]["text"], text)

    def test_empty_intersection_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            gold = Path(d) / "gold.tsv"
            gold.write_text("id\ttext\tgold_tokens_json\n", encoding="utf-8")
            report = {"report_type":"COMPARATIVE_SEGMENTATION_ERROR_TRIAGE_NOT_GOLD_ADJUDICATION",
              "dataset":{"rows_expert_adjudicated":0,"rows_source_annotated":993},
              "models":{"dictionary_max_match":{"false_split_examples":[],"false_merge_examples":[]},
                        "tud_unigram_viterbi":{"false_split_examples":[],"false_merge_examples":[]}}}
            with self.assertRaisesRegex(ValueError, "no row"):
                build(report, gold)

if __name__ == "__main__":
    unittest.main()
