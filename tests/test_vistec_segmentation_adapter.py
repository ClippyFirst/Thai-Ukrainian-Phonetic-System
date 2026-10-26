import csv
import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from evaluate_vistec_segmentation import parse_submission_text, write_benchmark_files

MODEL = {"model_id": "clippyfirst-tud-unigram-viterbi-v1",
         "source_license": "CC-BY-SA-4.0", "word_counts": {"ไทย": 3}, "token_penalty": 1.0}


class VistecSegmentationAdapterTests(unittest.TestCase):
    def test_pipe_tokens_and_annotation_markup_are_lossless(self):
        text, tokens = parse_submission_text("<ne>สวัสดี</ne>| |<msp='ผิด'>ถูก</msp>")
        self.assertEqual(text, "สวัสดี ถูก")
        self.assertEqual(tokens, ["สวัสดี", " ", "ถูก"])
        self.assertEqual("".join(tokens), text)

    def test_empty_and_unannotated_inputs_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "empty submissionText"):
            parse_submission_text("")
        with self.assertRaisesRegex(ValueError, "no text"):
            parse_submission_text("||")

    def test_small_csv_conversion_preserves_source_and_provenance(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / "source.csv"
            gold = Path(d) / "gold.tsv"
            predictions = Path(d) / "predictions.tsv"
            with source.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["questionText", "submissionText"])
                writer.writeheader()
                writer.writerow({"questionText": "different raw text", "submissionText": "<ne>สวัสดี</ne>| |โลก"})
                writer.writerow({"questionText": "hello world", "submissionText": "hello| |world"})
            count = write_benchmark_files(source, gold, predictions, MODEL, expected_rows=2, expected_blob_sha1=None)
            self.assertEqual(count, 2)
            with gold.open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f, delimiter="\t"))
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["text"], "สวัสดี โลก")
            self.assertEqual(rows[0]["gold_status"], "SOURCE_ANNOTATED")
            self.assertEqual(rows[0]["license"], "CC-BY-SA-3.0")
            self.assertTrue(all("".join(json.loads(row["gold_tokens_json"])) == row["text"] for row in rows))
            with predictions.open(encoding="utf-8", newline="") as f:
                pred_rows = list(csv.DictReader(f, delimiter="\t"))
            self.assertEqual(len(pred_rows), 4)
            self.assertEqual({r["engine"] for r in pred_rows}, {"dictionary_max_match", "tud_unigram_viterbi"})
            self.assertTrue(all(r["status"] == "ok" for r in pred_rows))
            self.assertTrue(all("".join(json.loads(r["predicted_tokens_json"])) in {"สวัสดี โลก", "hello world"} for r in pred_rows))


    def test_rejects_unpinned_csv_blob(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / "source.csv"
            source.write_text("submissionText\\nhello\\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Git blob SHA-1"):
                write_benchmark_files(source, Path(d)/"g.tsv", Path(d)/"p.tsv",
                                      MODEL, expected_rows=1, expected_blob_sha1="not-the-pinned-hash")

    def test_rejects_wrong_tud_model_license(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / "source.csv"
            source.write_text("submissionText\nhello\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "model identity or license"):
                write_benchmark_files(source, Path(d)/"g.tsv", Path(d)/"p.tsv",
                                      {**MODEL, "source_license": "UNKNOWN"}, expected_rows=1)


if __name__ == "__main__":
    unittest.main()
