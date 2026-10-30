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

    def test_parser_vowel_ids_are_declared(self):
        import csv
        from pathlib import Path
        root=Path(__file__).resolve().parents[1]
        with (root/"data"/"thai"/"vowels.csv").open(encoding="utf-8",newline="") as f:
            ids={r["id"] for r in csv.DictReader(f)}
        for text in ["เกีย","เกา","เกียว","แล้ว","เร็ว","เลย","ขาย","เอย","อุย"]:
            parsed=parse_syllable(text)
            self.assertIn(parsed.vowel_id,ids,text)

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

    def test_coda_registry_boolean_count(self):
        import csv
        from pathlib import Path
        root=Path(__file__).resolve().parents[1]
        with (root/"data"/"thai"/"consonants.csv").open(encoding="utf-8",newline="") as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(sum(r["coda_allowed"].strip().lower()=="true" for r in rows),38)

    def test_open_long_is_live(self):
        self.assertEqual(parse_syllable("กา").live_dead,"live")

    def test_cluster_is_not_coda(self):
        self.assertIsNone(parse_syllable("กรา").coda)

    def test_post_vowel_consonant_is_coda(self):
        self.assertEqual(parse_syllable("กาน").coda,"น")

    def test_carrier_is_not_a_final_coda(self):
        a=parse_syllable("กาอ")
        self.assertEqual(a.coda,"อ")
        self.assertEqual(a.status,"invalid:coda-not-licensed")

    def test_multiple_tone_marks_are_not_collapsed(self):
        a=parse_syllable("ก่้")
        self.assertEqual(a.status,"unresolved:multiple-tone-marks")
        self.assertIsNone(a.tone)

    def test_unconsumed_vowel_sign_is_not_ignored(self):
        for text in ("กาา","กิี","กาเก","กากา"):
            a=parse_syllable(text)
            self.assertEqual(a.status,"unresolved:multiple-vowel-signs",text)
            self.assertIsNone(a.phonemic_ipa,text)

    def test_unsupported_symbol_is_not_silently_dropped(self):
        a=parse_syllable("กา!")
        self.assertEqual(a.status,"unresolved:unsupported-symbol")
        self.assertIsNone(a.phonemic_ipa)

    def test_supported_thai_punctuation_is_outside_syllable_scope(self):
        a=parse_syllable("กาๆ")
        self.assertEqual(a.status,"unresolved:unsupported-symbol")

if __name__=="__main__":unittest.main()
