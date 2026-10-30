from __future__ import annotations

import unittest
from unittest.mock import patch

from thai_ukrainian.parser import _split_onset_coda, parse_syllable
from thai_ukrainian.inventory import load_consonants


class ParserStructuralEdgeCaseTests(unittest.TestCase):
    def test_preposed_ai_with_y_onset_keeps_y_as_onset(self):
        analysis = parse_syllable("ไย")
        self.assertEqual(analysis.status, "analyzed")
        self.assertEqual(analysis.onset, ["ย"])
        self.assertEqual(analysis.vowel_id, "V-X-AI")
        self.assertEqual(analysis.vowel, "aj")

    def test_empty_onset_is_explicitly_unresolved_instead_of_crashing(self):
        vowel = {
            "explicit": True,
            "id": "V-X-AJ",
            "terminal_glide": None,
        }
        onset, coda = _split_onset_coda("ย", load_consonants(), vowel)
        self.assertEqual(onset, [])
        self.assertIsNone(coda)

        with patch(
            "thai_ukrainian.parser.detect_vowel",
            return_value={
                "explicit": True,
                "id": "V-X-AJ",
                "terminal_glide": None,
                "ipa": "aːj",
                "length": "long",
                "matched_text": "ย",
            },
        ):
            analysis = parse_syllable("ย")
        self.assertEqual(
            analysis.status,
            "unresolved:empty-onset-after-vowel-analysis",
        )
        self.assertEqual(analysis.onset, [])
