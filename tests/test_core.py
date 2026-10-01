import unittest
from thai_ukrainian.inventory import load_consonants
from thai_ukrainian.tone import determine_tone
from thai_ukrainian.parser import parse_syllable

class CoreTests(unittest.TestCase):
    def test_inventory_counts(self):
        x=load_consonants()
        self.assertEqual(len(x),44)
        self.assertEqual(sum(v.class_=="mid" for v in x.values()),9)
        self.assertEqual(sum(v.class_=="high" for v in x.values()),11)
        self.assertEqual(sum(v.class_=="low" for v in x.values()),24)

    def test_tone_rules(self):
        cases=[
            ("mid","live","long",None,"mid"),
            ("mid","dead","short",None,"low"),
            ("high","live","long",None,"rising"),
            ("high","dead","short",None,"low"),
            ("low","live","long",None,"mid"),
            ("low","dead","short",None,"high"),
            ("low","dead","long",None,"falling"),
            ("mid","live","long","mai_ek","low"),
            ("low","live","long","mai_ek","falling"),
            ("low","live","long","mai_tho","high"),
            ("mid","live","long","mai_tri","high"),
            ("mid","live","long","mai_chattawa","rising"),
        ]
        for args in cases:self.assertEqual(determine_tone(*args[:-1]).tone,args[-1],args)

    def test_correspondence_inventory_matches_consonants(self):
        import csv
        from pathlib import Path
        root=Path(__file__).resolve().parents[1]
        with (root/"data"/"thai"/"consonants.csv").open(encoding="utf-8",newline="") as f:
            consonants={r["grapheme"] for r in csv.DictReader(f)}
        with (root/"data"/"thai"/"correspondences.csv").open(encoding="utf-8",newline="") as f:
            rows=list(csv.DictReader(f))
        self.assertEqual({r["thai_grapheme"] for r in rows},consonants)
        self.assertEqual(len(rows),len(consonants))

    def test_open_long_is_live(self):
        self.assertEqual(parse_syllable("กา").live_dead,"live")

    def test_cluster_is_not_coda(self):
        self.assertIsNone(parse_syllable("กรา").coda)

    def test_post_vowel_consonant_is_coda(self):
        self.assertEqual(parse_syllable("กาน").coda,"น")

if __name__=="__main__":unittest.main()
