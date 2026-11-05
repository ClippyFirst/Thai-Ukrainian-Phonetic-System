import unittest
from thai_ukrainian.adapters.xsampa import XSampaConversionError, convert_xsampa_label

class XSampaAdapterTests(unittest.TestCase):
    def test_ccost_tone_suffixes_and_multisyllable_label(self):
        converted=convert_xsampa_label("n a:_3 c a_2")
        self.assertEqual(converted.ipa,"naː.ca")
        self.assertEqual(converted.tone_categories,("falling","low"))
        self.assertEqual(tuple(x.tone_number for x in converted.syllables),("3","2"))
    def test_standard_symbols_aspiration_and_length(self):
        self.assertEqual(convert_xsampa_label("k_h a: N").ipa,"kʰaːŋ")
    def test_thai_vowel_and_palatal_stop_symbols(self):
        self.assertEqual(convert_xsampa_label("c_h E: M 7").ipa,"cʰɛːɯɤ")
    def test_multi_character_xsampa_symbols_use_longest_match(self):
        label = "J" + chr(92) + " N" + chr(92)
        self.assertEqual(convert_xsampa_label(label).ipa,"ɟɴ")

    def test_all_five_ccost_tone_suffixes_are_typed(self):
        expected={"1":"mid","2":"low","3":"falling","4":"high","5":"rising"}
        for number,category in expected.items():
            with self.subTest(number=number):
                converted=convert_xsampa_label("a_"+number)
                self.assertEqual(converted.syllables[0].tone_category,category)

    def test_published_ccost_figure2_kas_example(self):
        converted=convert_xsampa_label("n a:_3 . c a_2")
        self.assertEqual(converted.ipa,"naː.ca")
        self.assertEqual(converted.tone_categories,("falling","low"))

    def test_explicit_period_preserves_syllable_boundary(self):
        converted=convert_xsampa_label("k a . n a")
        self.assertEqual(converted.ipa,"ka.na")
        self.assertEqual(converted.tone_categories,(None,None))
    def test_common_diacritics_are_preserved(self):
        self.assertEqual(convert_xsampa_label("a_~ n_}").ipa,"ãn̚")
    def test_unknown_symbols_fail_closed(self):
        for label in ("z$","a$","k_h ə","ก"):
            with self.subTest(label=label):
                with self.assertRaises(XSampaConversionError): convert_xsampa_label(label)
    def test_tone_suffix_without_segment_is_rejected(self):
        with self.assertRaisesRegex(XSampaConversionError,"tone suffix without"): convert_xsampa_label("_3")
    def test_empty_label_is_rejected(self):
        with self.assertRaises(XSampaConversionError): convert_xsampa_label("  ")

if __name__=="__main__": unittest.main()
