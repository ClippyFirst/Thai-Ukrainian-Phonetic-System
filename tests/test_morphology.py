import unittest

from thai_ukrainian.morphology import analyze_morphology


class ConservativeMorphologyTests(unittest.TestCase):
    def test_future_and_negation_are_contextual_candidates(self):
        result = analyze_morphology(["ฉัน", "ไม่", "จะ", "ไป"])
        by_token = {item["token"]: item for item in result["candidates"]}
        self.assertEqual(by_token["ไม่"]["rule_id"], "TH-MORPH-NEG-001")
        self.assertEqual(by_token["จะ"]["rule_id"], "TH-MORPH-MOD-001")
        self.assertEqual(by_token["ไม่"]["status"], "contextual-candidate")
        self.assertEqual(result["status"], "research-only")

    def test_progressive_pair_is_not_reported_as_inflection(self):
        result = analyze_morphology(["เขา", "กำลัง", "วิ่ง", "อยู่"])
        by_token = {item["token"]: item for item in result["candidates"]}
        self.assertEqual(by_token["กำลัง"]["rule_id"], "TH-MORPH-ASP-001")
        self.assertEqual(by_token["อยู่"]["rule_id"], "TH-MORPH-ASP-002")
        self.assertIn("may span กำลัง … อยู่", by_token["อยู่"]["scope"])

    def test_ambiguous_lexical_function_is_not_forced(self):
        result = analyze_morphology(["บ้าน", "อยู่"])
        candidate = result["candidates"][0]
        self.assertEqual(candidate["rule_id"], "TH-MORPH-AMB-001")
        self.assertEqual(candidate["status"], "analysis-dependent")

    def test_clause_final_question_and_politeness_candidates(self):
        result = analyze_morphology(["ไป", "ไหม", "ครับ"])
        by_token = {item["token"]: item for item in result["candidates"]}
        self.assertEqual(by_token["ไหม"]["rule_id"], "TH-MORPH-Q-001")
        self.assertEqual(by_token["ครับ"]["rule_id"], "TH-MORPH-POL-001")

    def test_ignores_non_thai_tokens_and_preserves_original_indices(self):
        result = analyze_morphology([
            {"input": "ไม่", "kind": "thai"},
            {"input": " ", "kind": "space"},
            {"input": "go", "kind": "latin"},
            {"input": "ไป", "kind": "thai"},
        ])
        self.assertEqual([c["token_index"] for c in result["candidates"]], [0])
        self.assertEqual(result["input_token_count"], 2)

    def test_annotations_do_not_claim_full_morphology_or_scores(self):
        result = analyze_morphology(["การ", "เรียน"])
        self.assertEqual(result["mode"], "conservative-function-marker-candidates")
        self.assertTrue(any("not a complete Thai morphological analyzer" in item
                            for item in result["limitations"]))
        self.assertNotIn("confidence", result["candidates"][0])
        self.assertNotIn("ipa", result["candidates"][0])


if __name__ == "__main__":
    unittest.main()
