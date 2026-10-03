from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

from thai_ukrainian.contextual import surface_ipa_for_consonant, vowel_surface_context
from thai_ukrainian.inventory import load_consonants
from thai_ukrainian.api import analyze_syllable

class PositionalCorrespondenceTests(unittest.TestCase):
    def test_voiced_stop_has_distinct_final_surface_realization(self):
        inv = load_consonants()
        self.assertEqual(surface_ipa_for_consonant(inv['ด'], 'onset'), 'd')
        self.assertEqual(surface_ipa_for_consonant(inv['ด'], 'coda'), 't̚')

    def test_final_b_and_g_stops_are_realized_as_unreleased_voiceless_stops(self):
        inv = load_consonants()
        self.assertEqual(surface_ipa_for_consonant(inv['บ'], 'coda'), 'p̚')
        self.assertEqual(surface_ipa_for_consonant(inv['ก'], 'coda'), 'k̚')

    def test_vowel_surface_layer_does_not_invent_unattested_quality_change(self):
        self.assertEqual(vowel_surface_context('aː', 'open'), 'aː')
        self.assertEqual(vowel_surface_context('aː', 'closed'), 'aː')

    def test_syllable_exposes_phonemic_and_surface_ipa_separately(self):
        open_analysis = analyze_syllable('กา')
        closed_analysis = analyze_syllable('กัด')
        self.assertEqual(open_analysis.phonemic_ipa, 'kaː')
        self.assertEqual(open_analysis.phonetic_ipa, 'kaː')
        self.assertEqual(closed_analysis.phonemic_ipa, 'kat')
        self.assertEqual(closed_analysis.phonetic_ipa, 'kat̚')
        self.assertNotEqual(open_analysis.phonetic_ipa, closed_analysis.phonetic_ipa)

    def test_master_generator_declares_separate_ipa_layers(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
        import generate_master_table as gm
        with tempfile.TemporaryDirectory() as d:
            old = gm.OUT
            gm.OUT = Path(d)
            try:
                gm.build()
                with (Path(d) / 'thai_ukrainian_master.csv').open(encoding='utf-8', newline='') as f:
                    header = next(csv.reader(f))
                required = {
                    'onset_phonemic_ipa', 'onset_surface_ipa',
                    'vowel_phonemic_ipa', 'vowel_surface_ipa',
                    'coda_phonemic_ipa', 'coda_surface_ipa',
                    'syllable_phonemic_ipa', 'syllable_surface_ipa',
                    'ukrainian', 'ukrainian_from_ipa',
                }
                self.assertTrue(required.issubset(set(header)))
            finally:
                gm.OUT = old
