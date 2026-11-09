from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.build_geographic_dictionary import analyze_geographic_name, main, romanize_rtgs, _external_ipa_candidate


class GeographicDictionaryTests(unittest.TestCase):
    def test_rtgs_uses_newmm_tokens_and_royin(self):
        calls = []
        def tokenize(text, **kwargs):
            calls.append(("tokenize", text, kwargs))
            return ["กรุงเทพ", " ", "มหานคร"]
        def romanize(text, **kwargs):
            calls.append(("romanize", text, kwargs))
            return {"กรุงเทพ": "krungthep", "มหานคร": "mahanakhon"}[text]
        self.assertEqual(romanize_rtgs("กรุงเทพมหานคร", romanize, tokenize), "krungthep mahanakhon")
        self.assertEqual(calls[0][2], {"engine": "newmm", "keep_whitespace": True})
        self.assertTrue(all(call[2] == {"engine": "royin"} for call in calls[1:]))

    def test_non_thai_input_does_not_call_romanizer(self):
        def fail(*args, **kwargs):
            raise AssertionError("must not be called")
        self.assertEqual(romanize_rtgs("Bangkok", fail, fail), "")

    def test_supported_single_syllable_uses_typed_ipa_adapter(self):
        def tokenize(text, **kwargs):
            return [text]
        def romanize(text, **kwargs):
            return "ka"
        result = analyze_geographic_name("กา", romanize, tokenize)
        self.assertEqual(result["romanization_rtgs"], "ka")
        self.assertEqual(result["pipeline_status"], "COMPLETE_MODEL_OUTPUT_NOT_ADJUDICATED")
        self.assertTrue(result["ipa_phonemic"])
        self.assertTrue(result["ukrainian_from_ipa"])
        self.assertEqual(result["romanization_method"], "PyThaiNLP 5.4.0 newmm + royin RTGS")

    def test_missing_surface_ipa_is_not_filled_from_phonemic_ipa(self):
        analysis = [{
            "kind": "thai",
            "input": "กา",
            "word_segmentation_complete": True,
            "word_segmentation_method": "fixture",
            "syllables": [{
                "status": "analyzed",
                "phonemic_ipa": "kaː",
                "phonetic_ipa": None,
                "ukrainian_transliteration": "กา",
                "phonetic_result": {
                    "phonemic_ipa": "kaː",
                    "broad_surface_ipa": None,
                    "status": "SUPPORTED",
                    "uncertainty": [],
                },
            }],
        }]
        with patch("thai_ukrainian.text.analyze_text_with_word_segmentation", return_value=analysis):
            result = analyze_geographic_name("กา", lambda *_a, **_k: "ka", lambda text, **_k: [text])
        self.assertEqual(result["ipa_phonemic"], "kaː")
        self.assertEqual(result["ipa_broad_surface"], "")
        self.assertEqual(result["ukrainian_from_ipa"], "กา")

    def test_csv_cli_preserves_source_columns_and_adds_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "places.csv"
            target = root / "places-enriched.csv"
            source.write_text("id,name_th,source_url\n1,กา,https://example.org/1\n", encoding="utf-8")
            with patch("scripts.build_geographic_dictionary._load_pythainlp") as loader:
                loader.return_value = (
                    lambda text, **kwargs: "ka",
                    lambda text, **kwargs: [text],
                )
                self.assertEqual(main([str(source), "--output", str(target)]), 0)
            with target.open(encoding="utf-8-sig", newline="") as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(row["id"], "1")
            self.assertEqual(row["source_url"], "https://example.org/1")
            self.assertEqual(row["romanization_rtgs"], "ka")
            self.assertIn("ipa_phonemic", row)
            self.assertIn("ukrainian_from_ipa", row)

    def test_input_file_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "places.csv"
            path.write_text("name_th\nกา\n", encoding="utf-8")
            with patch("scripts.build_geographic_dictionary._load_pythainlp"):
                with self.assertRaises(SystemExit):
                    main([str(path), "--output", str(path)])

    def test_external_g2p_fallback_is_explicitly_provisional_and_ipa_driven(self):
        from types import SimpleNamespace
        from thai_ukrainian.phonetic_result import PhoneticResult

        typed = PhoneticResult(
            phonemic_ipa=None,
            broad_surface_ipa=None,
            segments=(),
            status="PROVISIONAL",
            provenance=("FastThaiG2P@test-pin",),
            uncertainty=("External IPA layer is unclassified.",),
            external_ipa="kaː",
        )
        class FakeAdapter:
            def convert(self, text):
                self.text = text
                return SimpleNamespace(
                    complete_ipa=True,
                    raw_ipa="/kaː˧/",
                    word_groups=("kaː˧",),
                    dictionary_hit_count=1,
                    oov_rule_fallback_count=0,
                    to_phonetic_results=lambda: ((typed,),),
                )

        result = _external_ipa_candidate("กา", FakeAdapter())
        self.assertEqual(result["ipa_external_fastthaig2p"], "/kaː˧/")
        self.assertEqual(result["ukrainian_from_ipa"], "ка")
        self.assertEqual(result["pipeline_status"], "PROVISIONAL_EXTERNAL_IPA_NOT_ADJUDICATED")
        self.assertEqual(result["analysis_confidence"], "PROVISIONAL_EXTERNAL_G2P")


if __name__ == "__main__":
    unittest.main()
