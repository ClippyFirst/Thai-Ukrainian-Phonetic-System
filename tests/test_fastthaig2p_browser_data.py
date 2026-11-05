from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.prepare_fastthaig2p_browser_source import prepare_source


class FastThaiG2PBrowserDataTests(unittest.TestCase):
    def test_only_source_attributed_entries_are_retained(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary)
            data = source / "data"
            data.mkdir()
            (source / "pyproject.toml").write_text('"data/fallback" = "fastthaig2p/data/fallback"\n', encoding="utf-8")
            (data / "dict.txt").write_text("สวน\nโมเดล\nคำแก้\n", encoding="utf-8")
            (data / "ipa.json").write_text(
                json.dumps({
                    "สวน": "/sua̯n˩˩˦/",
                    "โมเดล": "/moː˧.deːl˧/",
                    "คำแก้": "/kʰam˧.kɛː˥˩/",
                }, ensure_ascii=False),
                encoding="utf-8",
            )
            (data / "ipa_metadata.json").write_text(
                json.dumps({
                    "สวน": {"ipa": "/sua̯n˩˩˦/", "source": "wiktionary"},
                    "โมเดล": {"ipa": "/moː˧.deːl˧/", "source": "generated"},
                    "คำแก้": {"ipa": "/kʰam˧.kɛː˥˩/", "source": "manual"},
                }, ensure_ascii=False),
                encoding="utf-8",
            )

            report = prepare_source(source)

            self.assertEqual((data / "dict.txt").read_text(encoding="utf-8"), "สวน\n")
            self.assertEqual(
                json.loads((data / "ipa.json").read_text(encoding="utf-8")),
                {
                    "สวน": "/sua̯n˩˩˦/",
                },
            )
            self.assertEqual(report["retained_counts"], {"wiktionary": 1})
            self.assertEqual(report["excluded_counts"], {"generated": 1, "manual": 1})
            self.assertEqual(report["retained_entries"], 1)
            self.assertTrue((data / "browser-data-provenance.json").is_file())
            self.assertTrue((data / "WIKTIONARY-ATTRIBUTION.md").is_file())
            self.assertIn("WIKTIONARY-ATTRIBUTION.md", (source / "pyproject.toml").read_text(encoding="utf-8"))

    def test_reports_stale_metadata_ipa_without_losing_source_label(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary)
            data = source / "data"
            data.mkdir()
            (source / "pyproject.toml").write_text('"data/fallback" = "fastthaig2p/data/fallback"\n', encoding="utf-8")
            (data / "dict.txt").write_text("สวน\n", encoding="utf-8")
            (data / "ipa.json").write_text('{"สวน": "/sua̯n˩˩˦/"}', encoding="utf-8")
            (data / "ipa_metadata.json").write_text(
                '{"สวน": {"ipa": "/suaːn/", "source": "wiktionary"}}',
                encoding="utf-8",
            )
            report = prepare_source(source)
            self.assertEqual(report["retained_entries"], 1)
            self.assertEqual(report["metadata_ipa_mismatch_count"], 1)
            self.assertEqual(report["metadata_ipa_mismatch_examples"], ["สวน"])

    def test_rejects_missing_provenance_and_invalid_ipa(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary)
            data = source / "data"
            data.mkdir()
            (data / "dict.txt").write_text("สวน\n", encoding="utf-8")
            (data / "ipa.json").write_text('{"สวน": "suan"}', encoding="utf-8")
            (data / "ipa_metadata.json").write_text(
                '{"สวน": {"ipa": "suan", "source": "wiktionary"}}',
                encoding="utf-8",
            )
            with self.assertRaises(SystemExit):
                prepare_source(source)


if __name__ == "__main__":
    unittest.main()
