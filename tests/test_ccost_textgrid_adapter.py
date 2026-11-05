import unittest
from thai_ukrainian.adapters.ccost import TextGridFormatError, convert_ccost_tier, parse_textgrid_long
from thai_ukrainian.ukrainian_adaptation import adapt_phonetic_result

TEXTGRID = """File type = "ooTextFile"
Object class = "TextGrid"
xmin = 0
xmax = 1.2
tiers? <exists>
size = 2
item []:
    item [1]:
        class = "IntervalTier"
        name = "MAS"
        xmin = 0
        xmax = 1.2
        intervals: size = 2
        intervals [1]:
            xmin = 0
            xmax = 0.5
            text = "k_h a:_1"
        intervals [2]:
            xmin = 0.5
            xmax = 1.2
            text = "n a_3"
    item [2]:
        class = "IntervalTier"
        name = "MAU"
        xmin = 0
        xmax = 1.2
        intervals: size = 1
        intervals [1]:
            xmin = 0
            xmax = 1.2
            text = "k_h"
"""

class CCOSTTextGridAdapterTests(unittest.TestCase):
    def test_parses_long_textgrid_tiers_and_intervals(self):
        grid=parse_textgrid_long(TEXTGRID)
        self.assertEqual(grid.xmax,1.2)
        self.assertEqual(grid.tier("MAS").kind,"IntervalTier")
        self.assertEqual(len(grid.tier("MAS").intervals),2)
        self.assertEqual(grid.tier("MAS").intervals[0].text,"k_h a:_1")
    def test_converts_phonemic_tier_and_preserves_provenance(self):
        grid=parse_textgrid_long(TEXTGRID)
        annotations=convert_ccost_tier(grid,"MAS")
        self.assertEqual(len(annotations),2)
        self.assertEqual(annotations[0].ipa,"kʰaː")
        result=annotations[0].to_phonetic_results()[0]
        self.assertEqual(result.phonemic_ipa,"kʰaː")
        self.assertEqual(result.tone_category,"mid")
        self.assertEqual(result.status,"PROVISIONAL")
        self.assertIn("CCOST@10.5281/zenodo.17366698",result.provenance)
        adapted=adapt_phonetic_result(result)
        self.assertEqual(adapted["status"],"provisional")
        self.assertEqual(adapted["output"],"к'а")
    def test_surface_phone_tier_does_not_drive_ukrainian_adapter(self):
        grid=parse_textgrid_long(TEXTGRID)
        result=convert_ccost_tier(grid,"MAU")[0].to_phonetic_results()[0]
        self.assertIsNone(result.phonemic_ipa)
        self.assertEqual(result.broad_surface_ipa,"kʰ")
        self.assertEqual(result.status,"UNSUPPORTED")
        self.assertEqual(adapt_phonetic_result(result)["status"],"withheld")
    def test_orthographic_tier_is_not_accepted_as_xsampa(self):
        grid=parse_textgrid_long(TEXTGRID)
        with self.assertRaisesRegex(ValueError,"not a declared"): convert_ccost_tier(grid,"ORT")
    def test_short_textgrid_is_not_guessed(self):
        with self.assertRaises(TextGridFormatError): parse_textgrid_long('File type = "ooTextFile short"')

if __name__=="__main__": unittest.main()
