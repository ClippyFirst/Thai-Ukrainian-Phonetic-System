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

            self.assertEqual((data / "dict.txt").read_text(encoding="utf-8"), "สวน\nคำแก้\n")
            self.assertEqual(
                json.loads((data / "ipa.json").read_text(encoding="utf-8")),
                {
                    "สวน": "/sua̯n˩˩˦/",
                    "คำแก้": "/kʰam˧.kɛː˥˩/",
                },
            )
            self.assertEqual(report["retained_counts"], {"manual": 1, "wiktionary": 1})
            self.assertEqual(report["excluded_counts"], {"generated": 1})
            self.assertEqual(report["retained_entries"], 2)

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
