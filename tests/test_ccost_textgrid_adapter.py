import unittest
from thai_ukrainian.adapters.ccost import (TextGridFormatError, TextGrid, TextGridInterval, TextGridTier, convert_ccost_tier, is_ccost_nonphonetic_label, parse_textgrid_long)
from thai_ukrainian.adapters.xsampa import XSampaConversionError, convert_xsampa_label
from thai_ukrainian.ukrainian_adaptation import adapt_phonetic_result

TEXTGRID = """File type = "ooTextFile"
Object class = "TextGrid"
xmin = 0
xmax = 1.2
tiers? <exists>
size = 2
item []:
    item [1]:
        class = "IntervalTier"
        name = "MAS"
        xmin = 0
        xmax = 1.2
        intervals: size = 2
        intervals [1]:
            xmin = 0
            xmax = 0.5
            text = "k_h a:_1"
        intervals [2]:
            xmin = 0.5
            xmax = 1.2
            text = "n a_3"
    item [2]:
        class = "IntervalTier"
        name = "MAU"
        xmin = 0
        xmax = 1.2
        intervals: size = 1
        intervals [1]:
            xmin = 0
            xmax = 1.2
            text = "k_h"
"""

class CCOSTTextGridAdapterTests(unittest.TestCase):
    def test_parses_long_textgrid_tiers_and_intervals(self):
        grid=parse_textgrid_long(TEXTGRID)
        self.assertEqual(grid.xmax,1.2)
        self.assertEqual(grid.tier("MAS").kind,"IntervalTier")
        self.assertEqual(len(grid.tier("MAS").intervals),2)
        self.assertEqual(grid.tier("MAS").intervals[0].text,"k_h a:_1")
    def test_converts_phonemic_tier_and_preserves_provenance(self):
        grid=parse_textgrid_long(TEXTGRID)
        annotations=convert_ccost_tier(grid,"MAS")
        self.assertEqual(len(annotations),2)
        self.assertEqual(annotations[0].ipa,"kʰaː")
        result=annotations[0].to_phonetic_results()[0]
        self.assertEqual(result.phonemic_ipa,"kʰaː")
        self.assertEqual(result.tone_category,"mid")
        self.assertEqual(result.status,"PROVISIONAL")
        self.assertIn("CCOST@10.5281/zenodo.17366698",result.provenance)
        adapted=adapt_phonetic_result(result)
        self.assertEqual(adapted["status"],"provisional")
        self.assertEqual(adapted["output"],"к'а")
    def test_published_kas_word_interval_splits_syllables_and_retains_tones(self):
        grid=TextGrid(0,1.0,(TextGridTier(
            "KAS","IntervalTier",0,1.0,
            intervals=(TextGridInterval(0,1.0,"n a:_3 . c a_2"),)),))
        annotation=convert_ccost_tier(grid,"KAS")[0]
        results=annotation.to_phonetic_results()
        self.assertEqual(tuple(item.phonemic_ipa for item in results),("naː","ca"))
        self.assertEqual(tuple(item.tone_category for item in results),("falling","low"))
        self.assertTrue(all(item.status=="PROVISIONAL" for item in results))
        self.assertTrue(all("TextGrid interval 0.000000-1.000000" in item.provenance for item in results))
        self.assertTrue(all(any("no per-syllable time alignment" in note for note in item.uncertainty) for item in results))

    def test_surface_phone_tier_does_not_drive_ukrainian_adapter(self):
        grid=parse_textgrid_long(TEXTGRID)
        result=convert_ccost_tier(grid,"MAU")[0].to_phonetic_results()[0]
        self.assertIsNone(result.phonemic_ipa)
        self.assertEqual(result.broad_surface_ipa,"kʰ")
        self.assertEqual(result.status,"UNSUPPORTED")
        self.assertEqual(adapt_phonetic_result(result)["status"],"withheld")
    def test_orthographic_tier_is_not_accepted_as_xsampa(self):
        grid=parse_textgrid_long(TEXTGRID)
        with self.assertRaisesRegex(ValueError,"not a declared"): convert_ccost_tier(grid,"ORT")
    def test_released_maus_tier_aliases_are_phonetic_inputs(self):
        for tier_name, label in (("KAN-MAU", "n a_3"), ("KAS-MAU", "n a_3")):
            grid = TextGrid(0, 1.0, (TextGridTier(
                tier_name, "IntervalTier", 0, 1.0,
                intervals=(TextGridInterval(0, 1.0, label),)),))
            result = convert_ccost_tier(grid, tier_name)[0].to_phonetic_results()[0]
            self.assertEqual(result.phonemic_ipa, "na")
            self.assertEqual(result.tone_category, "falling")
            self.assertEqual(result.status, "PROVISIONAL")

    def test_known_maus_markers_are_not_converted_as_xsampa(self):
        grid = TextGrid(0, 1.0, (TextGridTier(
            "MAS", "IntervalTier", 0, 1.0,
            intervals=(
                TextGridInterval(0, 0.1, "<p:>"),
                TextGridInterval(0.1, 0.2, "<nib>"),
                TextGridInterval(0.2, 0.3, "<usb>"),
                TextGridInterval(0.3, 1.0, "k_h a_3"),
            )),))
        annotations = convert_ccost_tier(grid, "MAS")
        self.assertEqual(len(annotations), 1)
        self.assertEqual(annotations[0].ipa, "kʰa")
        self.assertTrue(is_ccost_nonphonetic_label("<p:>"))
        self.assertTrue(is_ccost_nonphonetic_label("<nib>"))
        self.assertTrue(is_ccost_nonphonetic_label("<usb><nib>"))
        self.assertFalse(is_ccost_nonphonetic_label("<usb><P>"))
        self.assertFalse(is_ccost_nonphonetic_label("<notProcessedChunk>"))
        self.assertFalse(is_ccost_nonphonetic_label("<Fail>"))
        self.assertFalse(is_ccost_nonphonetic_label("<nib>ข้อความ<P>"))

    def test_undocumented_tag_only_labels_fail_closed(self):
        for marker in ("<notProcessedChunk>", "<Fail>", "<P>", "<P:>", "<:p>"):
            grid = TextGrid(0, 1.0, (TextGridTier(
                "MAS", "IntervalTier", 0, 1.0,
                intervals=(TextGridInterval(0, 1.0, marker),)),))
            with self.subTest(marker=marker):
                with self.assertRaises(XSampaConversionError):
                    convert_ccost_tier(grid, "MAS")

    def test_unpublished_tone_number_8_remains_fail_closed(self):
        with self.assertRaises(XSampaConversionError):
            convert_xsampa_label("a_8")

    def test_long_textgrid_supports_multiline_and_escaped_quoted_labels(self):
        textgrid = '''File type = "ooTextFile"
Object class = "TextGrid"
xmin = 0
xmax = 1
item []:
    item [1]:
        class = "IntervalTier"
        name = "TRN"
        xmin = 0
        xmax = 1
        intervals: size = 1
        intervals [1]:
            xmin = 0
            xmax = 1
            text = "first line
second line with ""quoted"" text"
'''
        grid = parse_textgrid_long(textgrid)
        self.assertEqual(grid.tier("TRN").intervals[0].text, 'first line\nsecond line with "quoted" text')

    def test_short_textgrid_is_not_guessed(self):
        with self.assertRaises(TextGridFormatError): parse_textgrid_long('File type = "ooTextFile short"')

    def test_inspector_separates_documented_not_processed_chunk_marker(self):
        import tempfile
        import zipfile
        from pathlib import Path
        from scripts.inspect_ccost_textgrid import inspect

        textgrid = """File type = "ooTextFile"
Object class = "TextGrid"
xmin = 0
xmax = 1
item []:
    item [1]:
        class = "IntervalTier"
        name = "MAU"
        xmin = 0
        xmax = 1
        intervals: size = 1
        intervals [1]:
            xmin = 0
            xmax = 1
            text = "<notProcessedChunk>"
"""
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "fixture.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("labels/sample.TextGrid", textgrid)
            report = inspect([archive_path])

        self.assertEqual(report["failures"], [])
        self.assertEqual(report["processing_failure_marker_counts_by_tier"], {"MAU": 1})
        self.assertEqual(report["processing_failure_markers"][0]["raw_label"], "<notProcessedChunk>")

    def test_zip_inspection_reads_textgrid_member_and_skips_audio(self):
        import tempfile
        import zipfile
        from pathlib import Path
        from scripts.inspect_ccost_textgrid import inspect

        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "fixture.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("labels/sample.TextGrid", TEXTGRID)
                archive.writestr("audio/sample.wav", b"THIS AUDIO MEMBER MUST NOT BE READ")
                archive.writestr("README.txt", "metadata")
                archive.writestr("LICENSE", "unclassified extensionless metadata")
            report = inspect([archive_path], sample_limit=1)

        self.assertEqual(report["files_inspected"], 1)
        self.assertEqual(report["archives"][0]["textgrid_members"], ["labels/sample.TextGrid"])
        self.assertEqual(report["archives"][0]["audio_members_skipped"], 1)
        self.assertEqual(report["archives"][0]["non_textgrid_members_skipped"], 3)
        self.assertEqual(
            report["archives"][0]["non_textgrid_member_metadata"][-1]["name"],
            "LICENSE",
        )
        self.assertIn("MAS", report["tier_nonempty_label_counts"])
        self.assertFalse(report["failures"])

    def test_textgrid_parse_failure_reports_structure_without_label_text(self):
        import tempfile
        import zipfile
        from pathlib import Path
        from scripts.inspect_ccost_textgrid import inspect

        malformed = """File type = "ooTextFile"
Object class = "TextGrid"
xmin = 0
xmax = 1
item []:
    item [1]:
        class = "IntervalTier"
        name = "MAS"
        xmin = 0
        xmax = 1
        intervals [1]:
            xmin = 0
            xmax = 1
"""
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "malformed.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("bad.TextGrid", malformed)
            report = inspect([archive_path])

        diagnostic = report["failures"][0]["structure"]
        self.assertEqual(diagnostic["tier_names"], ["MAS"])
        self.assertEqual(diagnostic["interval_blocks_without_text"], 1)
        self.assertEqual(diagnostic["first_missing_interval_fields"], ["xmin", "xmax"])
        self.assertNotIn("label", diagnostic)

    def test_zip_inspection_rejects_unsupported_textgrid_encoding(self):
        import tempfile
        import zipfile
        from pathlib import Path
        from scripts.inspect_ccost_textgrid import inspect

        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "short.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("short.TextGrid", 'File type = "ooTextFile short"')
            report = inspect([archive_path])

        self.assertEqual(report["files_inspected"], 0)
        self.assertTrue(report["failures"])

if __name__=="__main__": unittest.main()
