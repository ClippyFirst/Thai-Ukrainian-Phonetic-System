import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.build_ccost_review_worklist import build_worklist


TEXTGRID = """File type = "ooTextFile"
Object class = "TextGrid"
xmin = 0
xmax = 2
item []:
    item [1]:
        class = "IntervalTier"
        name = "ORT-MAU"
        xmin = 0
        xmax = 2
        intervals: size = 2
        intervals [1]:
            xmin = 0
            xmax = 1
            text = "ภาษา"
        intervals [2]:
            xmin = 1
            xmax = 2
            text = "ไทย"
    item [2]:
        class = "IntervalTier"
        name = "KAN-MAU"
        xmin = 0
        xmax = 2
        intervals: size = 1
        intervals [1]:
            xmin = 0
            xmax = 1
            text = "? a_8"
    item [3]:
        class = "IntervalTier"
        name = "KAS-MAU"
        xmin = 0
        xmax = 2
        intervals: size = 1
        intervals [1]:
            xmin = 0
            xmax = 1
            text = "? a_8"
    item [4]:
        class = "IntervalTier"
        name = "MAS"
        xmin = 0
        xmax = 2
        intervals: size = 2
        intervals [1]:
            xmin = 0
            xmax = 1
            text = "<P>"
        intervals [2]:
            xmin = 1
            xmax = 2
            text = "<Fail>"
    item [5]:
        class = "IntervalTier"
        name = "TRN"
        xmin = 0
        xmax = 2
        intervals: size = 1
        intervals [1]:
            xmin = 0
            xmax = 2
            text = "ภาษาไทย"
"""


class CCOSTReviewWorklistTests(unittest.TestCase):
    def test_groups_repeated_tier_failures_and_preserves_cross_tier_context(self):
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "ccost.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("labels/sample.TextGrid", TEXTGRID)
                archive.writestr("audio/sample.wav", b"must never be read")
            report = build_worklist([archive_path])

        tone_rows = [row for row in report["records"] if "TONE_SUFFIX_8" in row["issue_types"]]
        self.assertEqual(len(tone_rows), 2)
        self.assertEqual(len({row["event_group_id"] for row in tone_rows}), 1)
        self.assertEqual(report["summary"]["tone_suffix_8_occurrences"], 2)
        self.assertEqual(report["summary"]["tone_suffix_8_event_groups"], 1)
        self.assertEqual(report["summary"]["unique_raw_label_events"], 1)
        self.assertTrue(any("ภาษา" in item["label"] for item in tone_rows[0]["overlap_context"]))
        self.assertTrue(any("ภาษาไทย" in item["label"] for item in tone_rows[0]["overlap_context"]))
        self.assertEqual(report["archives"][0]["audio_members_skipped"], 1)
        self.assertEqual(report["summary"]["audio_members_read"], 0)

    def test_finds_unresolved_markers_in_non_phonetic_tiers(self):
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "ccost.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("labels/sample.TextGrid", TEXTGRID)
            report = build_worklist([archive_path])

        marker_rows = [row for row in report["records"] if "UNRESOLVED_MARKER" in row["issue_types"]]
        self.assertEqual({marker for row in marker_rows for marker in row["markers"]}, {"<P>", "<Fail>"})
        self.assertEqual(report["summary"]["unresolved_marker_interval_count"], 2)
        self.assertEqual(report["summary"]["unresolved_marker_appearances"], 2)
        self.assertEqual(report["summary"]["markers"]["<P>"], 1)
        self.assertEqual(report["summary"]["markers"]["<Fail>"], 1)

    def test_keeps_source_labels_and_blank_expert_decision_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "ccost.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("labels/sample.TextGrid", TEXTGRID)
            report = build_worklist([archive_path])

        row = next(row for row in report["records"] if row["raw_label"] == "? a_8")
        self.assertEqual(row["raw_label"], "? a_8")
        self.assertEqual(row["decision"], "")
        self.assertEqual(row["proposed_xsampa"], "")
        self.assertEqual(row["adjudicator_decision"], "")
        self.assertIn("CC-BY-NC-SA-4.0", report["source_license"])


if __name__ == "__main__":
    unittest.main()
