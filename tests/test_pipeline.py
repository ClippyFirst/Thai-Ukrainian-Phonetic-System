import unittest
from thai_ukrainian.api import analyze_syllable
from thai_ukrainian.parser import parse_syllable
from thai_ukrainian.orthography import detect_vowel

class PipelineTests(unittest.TestCase):
    def test_long_open_live(self):
        a=parse_syllable("กา"); self.assertEqual(a.live_dead,"live"); self.assertEqual(a.vowel_length,"long")
    def test_cluster_not_coda(self): self.assertIsNone(parse_syllable("กรา").coda)
    def test_final_n_live(self):
        a=parse_syllable("กาน"); self.assertEqual(a.coda,"น"); self.assertEqual(a.live_dead,"live")
    def test_tone(self):
        a=analyze_syllable("กา"); self.assertEqual(a.tone.tone,"mid")
    def test_feature_candidates(self): self.assertTrue(analyze_syllable("กา").ukrainian_candidates)
    def test_implicit_vowel_flag(self): self.assertTrue(parse_syllable("ก").warnings)
    def test_special_construction_flag(self): self.assertTrue(parse_syllable("หง").warnings)
    def test_short_preposed_e(self):
        a=parse_syllable("เกะ"); self.assertEqual(a.vowel,"e"); self.assertEqual(a.vowel_length,"short")
    def test_long_preposed_e(self):
        a=parse_syllable("เก"); self.assertEqual(a.vowel,"eː"); self.assertEqual(a.vowel_length,"long")
    def test_diphthong_ia(self):
        a=parse_syllable("เกีย"); self.assertEqual(a.vowel,"iaː"); self.assertIsNone(a.coda)
    def test_ai_glide_is_not_coda(self):
        a=parse_syllable("ขาย"); self.assertEqual(a.vowel,"aːj"); self.assertIsNone(a.coda); self.assertEqual(a.onset,["ข"])
    def test_implicit_single_consonant_is_onset(self):
        a=parse_syllable("ก"); self.assertEqual(a.onset,["ก"]); self.assertIsNone(a.coda); self.assertTrue(a.warnings)

    def test_longest_match_ao_glide(self):
        a=parse_syllable("เกา"); self.assertEqual(a.vowel,"aw"); self.assertEqual(a.vowel_id,"V-X-AW-S"); self.assertIsNone(a.coda)

    def test_longest_match_iaw_glide(self):
        a=parse_syllable("เกียว"); self.assertEqual(a.vowel,"iaw"); self.assertEqual(a.vowel_id,"V-X-IAW"); self.assertEqual(a.onset,["ก"]); self.assertIsNone(a.coda)

    def test_closed_eoi_vowel_length_requires_lexical_evidence(self):
        for text in ("เงิน", "เดิน"):
            v = detect_vowel(text)
            self.assertTrue(v.get("analysis_dependent"), text)
            self.assertEqual(v.get("id"), "V-AMB-EOI-CLOSED")
            self.assertEqual({x["ipa"] for x in v["alternatives"]}, {"ɤ", "ɤː"})
            a = analyze_syllable(text)
            self.assertEqual(a.status, "analysis-dependent:vowel-length", text)
            self.assertIsNone(a.phonemic_ipa, text)
            self.assertIsNone(a.tone, text)
            self.assertEqual(a.coda, "น", text)

    def test_preposed_glide_patterns(self):
        cases=[("แล้ว","ɛːw"),("เร็ว","ew"),("เลย","ɤːj")]
        for text,ipa in cases:
            a=parse_syllable(text)
            self.assertEqual(a.vowel,ipa,text)
            self.assertEqual(len(a.onset),1,text)
            self.assertIsNone(a.coda,text)

    def test_closed_inherent_vowel_is_resolved_structurally(self):
        a=analyze_syllable("คน")
        self.assertEqual(a.status,"analyzed")
        self.assertEqual(a.vowel,"o")
        self.assertEqual(a.phonemic_ipa,"kʰon")
        self.assertEqual(a.coda,"น")

    def test_invalid_tone_is_structured(self):
        a=analyze_syllable("ข๊า"); self.assertEqual(a.status,"invalid:tone-combination"); self.assertIsNone(a.tone); self.assertTrue(a.warnings)

    def test_unlicensed_coda_is_rejected(self):
        for text in ("กฉ", "กผ"):
            a=analyze_syllable(text)
            self.assertEqual(a.status, "invalid:coda-not-licensed", text)
            self.assertIsNone(a.phonemic_ipa, text)
            self.assertIsNone(a.phonetic_ipa, text)
            self.assertIsNone(a.tone, text)

    def test_hnam(self):
        a=analyze_syllable("หงา"); self.assertEqual(a.tone.tone,"rising"); self.assertEqual(a.tone_class,"high"); self.assertEqual(a.phonemic_ipa,"ŋaː"); self.assertIn("ORTH-H-NAM",a.rules_applied)

    def test_preposed_vowel_hnam_cluster(self):
        a=analyze_syllable("ไหม")
        self.assertEqual(a.onset,["ห","ม"])
        self.assertEqual(a.coda,None)
        self.assertEqual(a.phonemic_ipa,"maj")
        self.assertEqual(a.tone.tone,"rising")

    def test_preposed_vowel_hnam_cluster_with_tone_mark(self):
        a=analyze_syllable("ไหว้")
        self.assertEqual(a.onset,["ห","ว"])
        self.assertEqual(a.coda,None)
        self.assertEqual(a.phonemic_ipa,"waj")
        self.assertEqual(a.tone.tone,"falling")
    def test_true_cluster_is_structurally_licensed(self):
        a=analyze_syllable("กล้า")
        self.assertEqual(a.onset,["ก","ล"])
        self.assertEqual(a.onset_class,"mid")
        self.assertEqual(a.tone_class,"mid")
        self.assertEqual(a.tone.tone,"falling")

    def test_nonconforming_consonant_sequence_is_not_forced_into_cluster(self):
        a=analyze_syllable("แสดง")
        self.assertEqual(a.status,"unresolved:nonconforming-consonant-sequence")
        self.assertTrue(a.warnings)
        self.assertIsNone(a.phonemic_ipa)

    def test_glide_inventory_is_machine_declared(self):
        self.assertIsNotNone(parse_syllable("เกียว").vowel_id)
        self.assertIsNotNone(parse_syllable("เลย").vowel_id)

if __name__=="__main__":unittest.main()
