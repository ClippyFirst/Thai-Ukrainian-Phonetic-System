import unittest
from thai_ukrainian.orthography import normalize_thai,decompose_thai
class UnicodeTests(unittest.TestCase):
    def test_nfc(self): self.assertEqual(normalize_thai("กา"),"กา")
    def test_roles(self):
        roles=[x["role"] for x in decompose_thai("ก่า")]
        self.assertIn("consonant",roles); self.assertIn("tone_mark",roles)
if __name__=="__main__":unittest.main()
