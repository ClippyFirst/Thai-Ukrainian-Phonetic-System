"""Completeness guard for the productive Standard Thai tone-rule table.

These are the conventional orthographic tone rules, not acoustic tone contours
or an evaluation of the syllable parser on arbitrary text.
"""
import unittest

from thai_ukrainian.tone import determine_tone, _load_rules


class ToneRuleCoverageTests(unittest.TestCase):
    def test_all_productive_tone_rule_classes_are_present_and_unique(self):
        rows = _load_rules()
        keys = [
            (r["tone_mark"], r["tone_class"], r["live_dead"], r["vowel_length"])
            for r in rows
        ]
        self.assertEqual(len(keys), len(set(keys)), "duplicate tone-rule conditions")
        self.assertEqual(len(rows), 15, "unexpected productive tone-rule table size")

        expected = {
            ("none", "mid", "live", "*"): "mid",
            ("none", "high", "live", "*"): "rising",
            ("none", "low", "live", "*"): "mid",
            ("none", "mid", "dead", "*"): "low",
            ("none", "high", "dead", "*"): "low",
            ("none", "low", "dead", "short"): "high",
            ("none", "low", "dead", "long"): "falling",
            ("mai_ek", "mid", "*", "*"): "low",
            ("mai_ek", "high", "*", "*"): "low",
            ("mai_ek", "low", "*", "*"): "falling",
            ("mai_tho", "mid", "*", "*"): "falling",
            ("mai_tho", "high", "*", "*"): "falling",
            ("mai_tho", "low", "*", "*"): "high",
            ("mai_tri", "mid", "*", "*"): "high",
            ("mai_chattawa", "mid", "*", "*"): "rising",
        }
        actual = {
            (r["tone_mark"], r["tone_class"], r["live_dead"], r["vowel_length"]): r["tone"]
            for r in rows
        }
        self.assertEqual(actual, expected)

    def test_every_declared_rule_resolves_to_its_expected_tone(self):
        for row in _load_rules():
            with self.subTest(rule_id=row["rule_id"]):
                # Pick a concrete value for wildcard dimensions. This exercises
                # the runtime lookup, not merely the CSV's textual schema.
                live_dead = "live" if row["live_dead"] == "*" else row["live_dead"]
                vowel_length = "short" if row["vowel_length"] == "*" else row["vowel_length"]
                result = determine_tone(
                    row["tone_class"], live_dead, vowel_length,
                    None if row["tone_mark"] == "none" else row["tone_mark"],
                )
                self.assertEqual(result.tone, row["tone"])
                self.assertEqual(result.rule_id, row["rule_id"])
                self.assertEqual(result.contour_ipa, row["contour_ipa"])
                self.assertEqual(result.evidence_status, row["evidence_status"])

    def test_tri_and_chattawa_do_not_silently_apply_to_non_mid_classes(self):
        for mark in ("mai_tri", "mai_chattawa"):
            for cls in ("high", "low"):
                with self.subTest(mark=mark, cls=cls):
                    with self.assertRaises(ValueError):
                        determine_tone(cls, "live", "long", mark)


if __name__ == "__main__":
    unittest.main()
