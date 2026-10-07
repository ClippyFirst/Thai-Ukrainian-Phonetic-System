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

    def test_preposed_ai_vowel_registry_uses_palatal_glide_ipa(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
        import generate_master_table as gm
        rows = {row["id"]: row for row in gm.rows("vowels.csv")}
        self.assertEqual(rows["V-X-AI"]["ipa"], "aj")

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

    def test_source_registries_declare_separate_ipa_layers(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
        import generate_master_table as gm
        cons = gm.rows("consonants.csv")
        vowels = gm.rows("vowels.csv")
        self.assertEqual(len(cons), 44)
        self.assertEqual(len(vowels), 41)
        self.assertIn("ipa", vowels[0])
        self.assertIn("coda_ipa", cons[0])
        self.assertIn("status", vowels[0])
