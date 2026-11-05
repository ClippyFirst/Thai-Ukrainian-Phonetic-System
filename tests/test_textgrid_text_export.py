import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.export_textgrid_text import export_records


def textgrid(tiers: list[tuple[str, str]]) -> str:
    blocks = []
    for index, (name, label) in enumerate(tiers, start=1):
        blocks.append(
            f'''    item [{index}]:
        class = "IntervalTier"
        name = "{name}"
        xmin = 0
        xmax = 1
        intervals: size = 1
        intervals [1]:
            xmin = 0
            xmax = 1
            text = "{label}"
'''
        )
    return (
        'File type = "ooTextFile"\n'
        'Object class = "TextGrid"\n'
        "xmin = 0\nxmax = 1\ntiers? <exists>\n"
        f"size = {len(tiers)}\nitem []:\n"
        + "".join(blocks)
    )


class TextGridTextExportTests(unittest.TestCase):
    def test_exports_only_explicit_transcript_tiers_with_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ccost = root / "CCOST textgrid.zip"
            lotus = root / "nectecLOTUSDIS textgrid.zip"
            with zipfile.ZipFile(ccost, "w") as archive:
                archive.writestr(
                    "ccost/sample.TextGrid",
                    textgrid([
                        ("ORT-MAU", "ภาษาไทย"),
                        ("TRN", "ภาษาไทย<nib>"),
                        ("MAS", "k_h a_3"),
                    ]),
                )
                archive.writestr("audio/sample.wav", b"must never be read")
            with zipfile.ZipFile(lotus, "w") as archive:
                archive.writestr(
                    "textgrid/Hijack_S001_T001_Con123.TextGrid",
                    textgrid([("Hijack_S001_T001_Con123", "สวัสดี ครับ")]),
                )

            records, summary = export_records(
                [ccost, lotus],
                {"ORT-MAU", "TRN"},
                ("Hijack_",),
            )

        self.assertEqual(summary["files_parsed"], 2)
        self.assertEqual(summary["records_exported"], 3)
        self.assertEqual(summary["records_by_source"], {"CCOST": 2, "LOTUSDIS": 1})
        self.assertFalse(summary["audio_read"])
        self.assertFalse(summary["gold_promoted"])
        self.assertEqual({row["tier"] for row in records}, {
            "ORT-MAU", "TRN", "Hijack_S001_T001_Con123"
        })
        self.assertNotIn("MAS", {row["tier"] for row in records})
        ccost_row = next(row for row in records if row["tier"] == "ORT-MAU")
        self.assertEqual(ccost_row["text"], "ภาษาไทย")
        self.assertEqual(ccost_row["license"], "CC-BY-NC-SA-4.0")
        self.assertEqual(ccost_row["source_id"], "CORP-CCOST")
        self.assertEqual(ccost_row["annotation_role"], "orthographic_word")
        self.assertEqual(
            ccost_row["source_archive_git_blob_sha1"],
            "3b1e3978c2b3a232dce4fdcfd137bb572ce5467f",
        )
        self.assertEqual(ccost_row["evidence_grade"], "SOURCE_ANNOTATED_NOT_GOLD")
        self.assertEqual(ccost_row["start"], 0)
        self.assertEqual(ccost_row["end"], 1)
        self.assertEqual(len({row["id"] for row in records}), 3)

    def test_requires_explicit_tier_selection(self):
        with self.assertRaisesRegex(ValueError, "select at least one"):
            export_records([], set(), ())


if __name__ == "__main__":
    unittest.main()
