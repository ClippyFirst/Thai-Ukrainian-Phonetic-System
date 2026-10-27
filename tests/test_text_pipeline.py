import unittest

from thai_ukrainian.api import analyze_syllable
from thai_ukrainian.text import analyze_text, segment_thai_word, tokenize_text


class TextPipelineTests(unittest.TestCase):
    def test_mixed_tokenization(self):
        tokens = tokenize_text("กรุงเทพ, Bangkok 123! ๆ")
        self.assertEqual(
            [token.kind for token in tokens],
            ["thai", "punctuation", "latin", "number", "punctuation", "thai_marker"],
        )
        self.assertEqual([token.text for token in tokenize_text("ฟิล์ม ๆ")], ["ฟิล์ม", "ๆ"])

    def test_curated_multisyllable_words(self):
        self.assertEqual(segment_thai_word("ครอบครัว"), (("ครอบ", "ครัว"), "lexicon"))
        self.assertEqual(segment_thai_word("รถบัส"), (("รถ", "บัส"), "lexicon"))
        self.assertEqual(segment_thai_word("คอมพิวเตอร์"), (("คอม", "พิว", "เตอร์"), "lexicon"))

    def test_source_attested_ukraine_name_uses_two_syllable_lexicon(self):
        # en.wiktionary Thai entry oldid 88025965 attests /juː˧.kʰreːn˧/.
        # This is a pinned source reading, not independent expert/acoustic gold.
        self.assertEqual(segment_thai_word("ยูเครน"), (("ยู", "เครน"), "lexicon"))
        token = analyze_text("ยูเครน")[0]
        self.assertEqual(token["segmentation_status"], "lexicon")
        self.assertEqual([s["input"] for s in token["syllables"]], ["ยู", "เครน"])
        self.assertEqual([s["phonemic_ipa"] for s in token["syllables"]], ["juː", "kʰreːn"])
        self.assertEqual([s["tone"]["tone"] for s in token["syllables"]], ["mid", "mid"])
        self.assertTrue(all(s["ukrainian_transliteration"] for s in token["syllables"]))

    def test_unknown_text_is_not_falsely_segmented(self):
        for text in ("คำใหม่ที่ไม่อยู่ในพจนานุกรม", "กากล้าขายแล้วไหว้แสดง"):
            with self.subTest(text=text):
                syllables, status = segment_thai_word(text)
                self.assertEqual(syllables, (text,))
                self.assertEqual(status, "unresolved")

    def test_text_analysis_preserves_word_boundaries_and_punctuation(self):
        result = analyze_text("ครอบครัว, รถบัส")
        self.assertEqual(
            [(token["input"], token["kind"]) for token in result],
            [("ครอบครัว", "thai"), (",", "punctuation"), ("รถบัส", "thai")],
        )
        self.assertEqual(result[0]["segmentation_status"], "lexicon")
        self.assertEqual(result[0]["syllables"][0]["input"], "ครอบ")
        self.assertEqual(result[2]["segmentation_status"], "lexicon")

    def test_unresolved_word_segmentation_withholds_phonetic_output(self):
        for text in ("คำใหม่ที่ไม่อยู่ในพจนานุกรม", "กากล้าขายแล้วไหว้แสดง"):
            with self.subTest(text=text):
                token = analyze_text(text)[0]
                self.assertEqual(token["segmentation_status"], "unresolved")
                self.assertEqual(token["syllables"], [])
                self.assertTrue(any("IPA and Ukrainian output are withheld" in w for w in token["warnings"]))

    def test_source_attested_lexical_ipa_override_flows_through_text_pipeline(self):
        syllables, segmentation = segment_thai_word("เงิน")
        self.assertEqual(syllables, ("เงิน",))
        self.assertEqual(segmentation, "lexical_ipa_override")
        result = analyze_text("เงิน")[0]
        self.assertEqual(result["segmentation_status"], "lexical_ipa_override")
        self.assertEqual(len(result["syllables"]), 1)
        analysis = result["syllables"][0]
        self.assertEqual(analysis["phonemic_ipa"], "ŋɤn")
        self.assertEqual(analysis["vowel_length"], "short")
        self.assertEqual(analysis["tone"]["tone"], "mid")
        self.assertEqual(analysis["ukrainian_transliteration"], "нген")

    def test_source_attested_long_vowel_override_resolves_walk_word(self):
        # The grapheme-only parser remains conservative. This exact lexical
        # reading is separately sourced and is not independent IPA gold.
        from thai_ukrainian.lexical_ipa import load_lexical_ipa_overrides
        self.assertEqual(load_lexical_ipa_overrides()["เดิน"]["segmental_ipa"], "dɤːn")
        self.assertEqual(load_lexical_ipa_overrides()["เดิน"]["vowel_length"], "long")
        token = analyze_text("เดิน")[0]
        self.assertEqual(token["segmentation_status"], "lexical_ipa_override")
        analysis = token["syllables"][0]
        self.assertEqual(analysis["phonemic_ipa"], "dɤːn")
        self.assertEqual(analysis["vowel_length"], "long")
        self.assertEqual(analysis["tone"]["tone"], "mid")
        self.assertEqual(analysis["ukrainian_transliteration"], "ден")
        self.assertEqual(analysis["onset"], ["ด"])
        self.assertEqual(analysis["coda"], "น")
        self.assertTrue(any("not independently adjudicated" in w for w in analysis["warnings"]))

    def test_final_velar_stop_is_preserved_in_ukrainian_output(self):
        for word in ("พริก", "ตรอก"):
            with self.subTest(word=word):
                result = analyze_syllable(word)
                self.assertEqual(result.status, "analyzed")
                self.assertTrue(result.phonemic_ipa.endswith("k"), result.phonemic_ipa)
                self.assertTrue(result.ukrainian_transliteration.endswith("к"), result.ukrainian_transliteration)
                if word == "ตรอก":
                    self.assertEqual(result.onset, ["ต", "ร"])
                    self.assertEqual(result.coda, "ก")

    def test_medial_ua_glide_is_not_mistaken_for_a_coda(self):
        result = analyze_syllable("กวน")
        self.assertEqual(result.status, "analyzed")
        self.assertEqual(result.onset, ["ก"])
        self.assertEqual(result.coda, "น")
        self.assertTrue(result.phonemic_ipa.endswith("n"), result.phonemic_ipa)
        self.assertTrue(result.ukrainian_transliteration.endswith("н"), result.ukrainian_transliteration)

    def test_w_glides_are_rendered_consistently_as_vocalic_u(self):
        for word in ("ดาว", "หนาว", "เศร้า"):
            with self.subTest(word=word):
                result = analyze_syllable(word)
                self.assertEqual(result.status, "analyzed")
                self.assertIsNone(result.coda)
                self.assertTrue(result.phonemic_ipa.endswith("w"), result.phonemic_ipa)
                self.assertTrue(result.ukrainian_transliteration.endswith("у"), result.ukrainian_transliteration)
        cold = analyze_syllable("หนาว")
        self.assertEqual(cold.onset, ["ห", "น"])
        self.assertEqual(cold.phonemic_ipa, "naːw")

    def test_sense_ambiguous_thray_withholds_lexical_guess(self):
        # The Royal Institute's 2011 article distinguishes ทราย meaning sand
        # (false cluster, initial /s/) from ทราย meaning a deer (true cluster).
        # The parser has no semantic context, so the bare homograph is unresolved.
        result = analyze_syllable("ทราย")
        self.assertEqual(result.status, "analysis-dependent:special-orthography")
        self.assertIsNone(result.phonemic_ipa)
        self.assertIsNone(result.phonetic_ipa)
        self.assertIsNone(result.ukrainian_transliteration)
        self.assertTrue(any(rule.get("rule_id") == "SP-THR-001" for rule in result.special_analyses))

    def test_attested_false_cluster_sri_uses_lexical_reading(self):
        # The Royal Institute Dictionary entry (mirrored by Longdo) gives
        # ศรี as สี. This tests a lexical orthography override, not IPA gold.
        result = analyze_syllable("ศรี")
        self.assertEqual(result.status, "analyzed")
        self.assertEqual(result.normalized, "สี")
        self.assertEqual(result.phonemic_ipa, "siː")
        self.assertEqual(result.ukrainian_transliteration, "сі")

    def test_lexical_readings_produce_structured_results(self):
        # These are parser smoke tests, not gold-IPA assertions. Gold readings
        # belong in the adjudicated fixture set with cited lexical evidence.
        # The Royal Institute article "เรื่องยุ่ง ๆ เกี่ยวกับอักษรควบ"
        # (2011, vol. 36 no. 4, pp. 556-557) documents these lexical ทร readings.
        source_attested_thr = {
            "ทราบ": "ซาบ",
            "ทรง": "ซง",
            "ทรัพย์": "ซับ",
            "แทรก": "แซก",
        }
        words = (
            "จริง", "สร้าง", "เศร้า", "ไซร้", "จันทร์", "ศุกร์", "เสาร์",
            "สัตว์", "พันธุ์", "ฟิล์ม", "ฤทธิ์", "เตอร์", "อย่า", "อยู่",
            "อย่าง", "อยาก", *source_attested_thr.keys(),
        )
        for word in words:
            with self.subTest(word=word):
                result = analyze_syllable(word)
                self.assertIsNotNone(result.status)
                self.assertEqual(result.input, word)
                if word in source_attested_thr:
                    self.assertEqual(result.normalized, source_attested_thr[word])
                if word == "อย่าง":
                    self.assertEqual(result.normalized, "หย่าง")
                if word == "เตอร์":
                    self.assertEqual(result.normalized, "เตอ")

    def test_unlisted_rr_form_remains_unresolved(self):
        # The OBEC source gives lexical readings for specific words, but also
        # documents several readings and syllabifications for different words.
        # A source-backed lexicon must not become a productive universal rule.
        syllable = analyze_syllable("สรร")
        self.assertEqual(syllable.status, "analysis-dependent:special-orthography")
        self.assertIsNone(syllable.phonemic_ipa)
        self.assertIsNone(syllable.phonetic_ipa)
        self.assertIsNone(syllable.ukrainian_transliteration)

        token = analyze_text("สรร")[0]
        self.assertEqual(token["segmentation_status"], "unresolved")
        self.assertEqual(token["syllables"], [])
        self.assertTrue(any("IPA and Ukrainian output are withheld" in w for w in token["warnings"]))

    def test_source_attested_rr_words_are_segmented_conservatively(self):
        # The Office of the Basic Education Commission gives:
        # สรรพคุณ = สับ-พะ-คุน; สรรพสินค้า = สับ-พะ-สิน-ค้า;
        # สรรพนาม = สับ-พะ-นาม. These are source-backed syllabification
        # entries, not independently adjudicated IPA gold labels.
        expected = {
            "สรรพคุณ": ("สับ", "พะ", "คุน"),
            "สรรพสินค้า": ("สับ", "พะ", "สิน", "ค้า"),
            "สรรพนาม": ("สับ", "พะ", "นาม"),
        }
        for word, syllables in expected.items():
            with self.subTest(word=word):
                self.assertEqual(segment_thai_word(word), (syllables, "lexicon"))
                token = analyze_text(word)[0]
                self.assertEqual(token["segmentation_status"], "lexicon")
                self.assertEqual(tuple(item["input"] for item in token["syllables"]), syllables)
                self.assertTrue(all(item["phonemic_ipa"] for item in token["syllables"]))
                self.assertTrue(all(item["ukrainian_transliteration"] for item in token["syllables"]))



    def test_source_attested_challenge_lexicon_entries(self):
        expected = {
            "ไกล": (("ไกล",), "lexicon"),
            "ใกล้": (("ใกล้",), "lexicon"),
            "เดิน": (("เดิน",), "lexical_ipa_override"),
            "กรรม": (("กำ",), "lexicon"),
            "บรรจุ": (("บัน", "จุ"), "lexicon"),
        }
        for word, segmentation in expected.items():
            with self.subTest(word=word):
                self.assertEqual(segment_thai_word(word), segmentation)


    def test_special_vowel_letters_remain_lexically_unresolved_without_word_evidence(self):
        for spelling in ("ฤ", "ฤๅ", "ฦ", "ฦๅ"):
            with self.subTest(spelling=spelling):
                result = analyze_syllable(spelling)
                self.assertEqual(result.status, "analysis-dependent:special-orthography")
                self.assertIsNone(result.phonemic_ipa)
                self.assertIsNone(result.phonetic_ipa)
                self.assertIsNone(result.ukrainian_transliteration)
                self.assertTrue(result.special_analyses)


if __name__ == "__main__":
    unittest.main()
