import unittest
from thai_ukrainian.tone import determine_tone
class NegativeTests(unittest.TestCase):
    def test_invalid_tri_class(self):
        with self.assertRaises(ValueError): determine_tone("high","live","long","mai_tri")
    def test_invalid_chattawa_class(self):
        with self.assertRaises(ValueError): determine_tone("low","live","long","mai_chattawa")
if __name__=="__main__":unittest.main()
