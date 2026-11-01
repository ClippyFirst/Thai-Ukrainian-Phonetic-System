import unittest

from thai_ukrainian.adjudication import (
    validate_blind_packet,
    validate_independent_pair,
    validate_review_packet,
)


CHALLENGE = [
    {"id": "TH-G2P-001", "input": "กา", "stratum": "core-vowel-length", "probe": "core_contrast"},
    {"id": "TH-G2P-002", "input": "กะ", "stratum": "core-vowel-length", "probe": "core_contrast"},
]
FIELDS = [
    "id", "thai", "stratum", "probe", "orthography_validity", "lexical_reading",
    "word_boundaries", "syllable_boundaries", "phonemic_ipa", "broad_surface_ipa",
    "tone_sequence", "vowel_length", "final_glottal", "transcription_level",
    "uncertainty", "abstention_reason", "reviewer_id", "reviewer_qualification_ref",
    "reviewed_at", "audio_asset_reference", "audio_time_start", "audio_time_end",
    "source_notes",
]


def blank_row(ident, thai, stratum="core-vowel-length", probe="core_contrast"):
    return {
        "id": ident, "thai": thai, "stratum": stratum, "probe": probe,
        **{field: "" for field in FIELDS[4:]},
    }


def completed_row(ident, thai, reviewer_id="TH-PH-01"):
    row = blank_row(ident, thai)
    row.update({
        "orthography_validity": "VALID",
        "transcription_level": "BROAD_PHONEMIC",
        "uncertainty": "LOW",
        "reviewer_id": reviewer_id,
        "reviewer_qualification_ref": f"qualification-record:{reviewer_id}",
        "reviewed_at": "2026-11-01",
        "phonemic_ipa": "/kaː/",
    })
    return row


class AdjudicationPacketTests(unittest.TestCase):
    def test_blind_packet_requires_exact_challenge_coverage(self):
        rows = [blank_row("TH-G2P-001", "กา"), blank_row("TH-G2P-002", "กะ")]
        self.assertEqual(validate_blind_packet(rows, CHALLENGE)["records"], 2)

    def test_blind_packet_rejects_missing_or_changed_input(self):
        with self.assertRaisesRegex(ValueError, "challenge set"):
            validate_blind_packet([blank_row("TH-G2P-001", "กา")], CHALLENGE)
        changed = [blank_row("TH-G2P-001", "กา"), blank_row("TH-G2P-002", "กะผิด")]
        with self.assertRaisesRegex(ValueError, "does not match"):
            validate_blind_packet(changed, CHALLENGE)

    def test_blind_packet_rejects_prefilled_labels_and_duplicate_ids(self):
        rows = [blank_row("TH-G2P-001", "กา"), blank_row("TH-G2P-002", "กะ")]
        rows[0]["phonemic_ipa"] = "/kaː/"
        with self.assertRaisesRegex(ValueError, "must be blank"):
            validate_blind_packet(rows, CHALLENGE)
        rows[0]["phonemic_ipa"] = ""
        rows[1]["id"] = rows[0]["id"]
        with self.assertRaisesRegex(ValueError, "unique"):
            validate_blind_packet(rows, CHALLENGE)

    def test_review_requires_one_identified_reviewer_and_complete_coverage(self):
        rows = [completed_row("TH-G2P-001", "กา"), completed_row("TH-G2P-002", "กะ")]
        result = validate_review_packet(rows, ["TH-G2P-001", "TH-G2P-002"], "TH-PH-01")
        self.assertEqual(result["reviewer_id"], "TH-PH-01")
        rows[1]["reviewer_id"] = "TH-PH-02"
        with self.assertRaisesRegex(ValueError, "same reviewer"):
            validate_review_packet(rows, ["TH-G2P-001", "TH-G2P-002"], "TH-PH-01")

    def test_review_requires_explicit_abstention_reason_when_ipa_missing(self):
        row = blank_row("TH-G2P-001", "กา")
        row.update({
            "orthography_validity": "AMBIGUOUS",
            "transcription_level": "BROAD_PHONEMIC",
            "uncertainty": "ABSTAIN",
            "reviewer_id": "TH-PH-01",
            "reviewer_qualification_ref": "qualification-record:TH-PH-01",
            "reviewed_at": "2026-11-01",
        })
        with self.assertRaisesRegex(ValueError, "abstention_reason"):
            validate_review_packet([row], ["TH-G2P-001"], "TH-PH-01")
        row["abstention_reason"] = "Lexical reading cannot be established from isolated spelling."
        self.assertEqual(validate_review_packet([row], ["TH-G2P-001"], "TH-PH-01")["abstentions"], 1)

    def test_two_reviewer_pair_requires_distinct_ids_and_same_coverage(self):
        a = [completed_row("TH-G2P-001", "กา", "TH-PH-01")]
        b = [completed_row("TH-G2P-001", "กา", "TH-PH-02")]
        self.assertEqual(
            validate_independent_pair(a, b)["status"],
            "TWO_REVIEWERS_PRESENT_ADJUDICATION_STILL_REQUIRED",
        )
        b[0]["reviewer_id"] = "TH-PH-01"
        with self.assertRaisesRegex(ValueError, "distinct"):
            validate_independent_pair(a, b)

    def test_narrow_acoustic_labels_require_audio_asset_and_interval(self):
        row = completed_row("TH-G2P-001", "กา")
        row.update({"transcription_level": "NARROW_ACOUSTIC", "phonemic_ipa": "[kaː]"})
        with self.assertRaisesRegex(ValueError, "audio"):
            validate_review_packet([row], ["TH-G2P-001"], "TH-PH-01")
        row.update({
            "audio_asset_reference": "CCOST:recording-001",
            "audio_time_start": "1.20",
            "audio_time_end": "1.85",
        })
        self.assertEqual(validate_review_packet([row], ["TH-G2P-001"], "TH-PH-01")["records"], 1)


if __name__ == "__main__":
    unittest.main()
