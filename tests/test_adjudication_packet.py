import unittest
import csv
import json
from pathlib import Path

from thai_ukrainian.adjudication import (
    validate_blind_packet,
    validate_independent_pair,
    validate_review_packet,
    validate_ukrainian_blind_packet,
    validate_ukrainian_independent_pair,
    validate_ukrainian_review_packet,
)


CHALLENGE = [
    {"id": "TH-G2P-001", "input": "กา", "stratum": "core-vowel-length", "probe": "core_contrast"},
    {"id": "TH-G2P-002", "input": "กะ", "stratum": "core-vowel-length", "probe": "core_contrast"},
]
FIELDS = [
    "id", "thai", "orthography_validity", "lexical_reading",
    "word_boundaries", "syllable_boundaries", "phonemic_ipa", "broad_surface_ipa", "narrow_ipa",
    "tone_sequence", "vowel_length", "final_glottal", "transcription_level",
    "uncertainty", "abstention_reason", "reviewer_id", "reviewer_qualification_ref",
    "reviewed_at", "audio_asset_reference", "audio_time_start", "audio_time_end",
    "source_notes",
]


def blank_row(ident, thai):
    return {
        "id": ident, "thai": thai,
        **{field: "" for field in FIELDS[2:]},
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
        "lexical_reading": thai,
        "word_boundaries": thai,
        "syllable_boundaries": thai,
        "tone_sequence": "MID",
        "vowel_length": "LONG",
        "final_glottal": "ABSENT",
    })
    return row


class AdjudicationPacketTests(unittest.TestCase):
    def test_repository_supplemental_user_regression_packet_is_blind_and_complete(self):
        root = Path(__file__).resolve().parents[1]
        challenge = [
            json.loads(line)
            for line in (root / "data/benchmark/thai_g2p_supplemental_challenge.jsonl")
            .read_text(encoding="utf-8").splitlines()
        ]
        with (root / "data/benchmark/ipa-adjudication-supplemental-blind.tsv").open(
            "r", encoding="utf-8", newline=""
        ) as stream:
            blind = list(csv.DictReader(stream, delimiter="\t"))
        result = validate_blind_packet(blind, challenge)
        self.assertEqual(result["records"], 6)
        self.assertEqual(result["labels_prefilled"], 0)
        self.assertEqual(
            {row["thai"] for row in blind},
            {"วันนี้", "ฉันเห็นสัตว์ในฟิล์มเรื่องหนึ่ง", "อย่าเพิ่งเศร้า",
             "อะไรบ้าง", "อธิบายทฤษฎี", "ฤๅษีอธิบายทฤษฎีเรื่องเสียงไทยอย่างไร"},
        )
        self.assertTrue(all(row["gold_phonemic_ipa"] is None for row in challenge))
        self.assertTrue(all(row["gold_word_boundaries"] is None for row in challenge))
        self.assertTrue(all(not row["phonemic_ipa"] and not row["reviewer_id"] for row in blind))

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



    def test_blind_packet_rejects_prefilled_lexical_or_orthographic_labels(self):
        rows = [blank_row("TH-G2P-001", "กา"), blank_row("TH-G2P-002", "กะ")]
        rows[0]["lexical_reading"] = "กา"
        with self.assertRaisesRegex(ValueError, "must be blank"):
            validate_blind_packet(rows, CHALLENGE)
        rows[0]["lexical_reading"] = ""
        rows[0]["orthography_validity"] = "VALID"
        with self.assertRaisesRegex(ValueError, "must be blank"):
            validate_blind_packet(rows, CHALLENGE)

    def test_blind_packet_rejects_unexpected_engine_output_column(self):
        rows = [blank_row("TH-G2P-001", "กา"), blank_row("TH-G2P-002", "กะ")]
        rows[0]["engine_output"] = "/kaː/"
        with self.assertRaisesRegex(ValueError, "fields mismatch"):
            validate_blind_packet(rows, CHALLENGE)

    def test_abstention_cannot_smuggle_surface_ipa(self):
        row = blank_row("TH-G2P-001", "กา")
        row.update({
            "orthography_validity": "AMBIGUOUS",
            "transcription_level": "BROAD_PHONEMIC",
            "uncertainty": "ABSTAIN",
            "abstention_reason": "Reading not established.",
            "reviewer_id": "TH-PH-01",
            "reviewer_qualification_ref": "qualification-record:TH-PH-01",
            "reviewed_at": "2026-11-01",
            "broad_surface_ipa": "[kaː]",
        })
        with self.assertRaisesRegex(ValueError, "must not contain IPA labels"):
            validate_review_packet([row], ["TH-G2P-001"], "TH-PH-01")

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


    def test_thai_independent_pair_reports_field_agreement_and_abstentions(self):
        a = [completed_row("TH-G2P-001", "กา", "TH-PH-01")]
        b = [completed_row("TH-G2P-001", "กา", "TH-PH-02")]
        b[0]["tone_sequence"] = "LOW"
        result = validate_independent_pair(a, b)
        self.assertEqual(result["agreement"]["fields"]["phonemic_ipa"]["exact_agreements"], 1)
        self.assertEqual(result["agreement"]["fields"]["tone_sequence"]["exact_agreements"], 0)
        self.assertEqual(result["agreement"]["fields"]["tone_sequence"]["exact_agreement_rate"], 0.0)
        self.assertEqual(result["agreement"]["joint_abstentions"], 0)

    def test_ukrainian_preference_packet_is_candidate_blind_and_source_bound(self):
        source = [{
            "id": "TH-UA-001", "thai": "ไกล", "phonemic_ipa": "/klaj˧/",
            "source_id": "SRC-1", "source_url": "https://example.org/source",
            "license": "CC-BY-SA-4.0",
        }]
        packet = [{
            "id": "TH-UA-001", "thai": "ไกล", "source_ipa": "/klaj˧/",
            "ipa_reference_status": "SOURCE_ATTESTED_NOT_GOLD",
            "source_id": "SRC-1", "source_url": "https://example.org/source",
            "license": "CC-BY-SA-4.0",
            "criteria_version": "UA-PRACTICAL-TRANSCRIPTION-0.1",
            "reviewer_id": "", "reviewer_qualification_ref": "",
            "preferred_ukrainian_form": "", "syllable_boundary_policy": "",
            "tone_rendering_policy": "", "uncertainty": "", "abstention_reason": "",
            "reviewed_at": "", "rationale": "",
        }]
        self.assertEqual(validate_ukrainian_blind_packet(packet, source)["records"], 1)
        packet[0]["preferred_ukrainian_form"] = "клай"
        with self.assertRaisesRegex(ValueError, "reviewer fields must be blank"):
            validate_ukrainian_blind_packet(packet, source)


    def test_reviewer_pair_rejects_changed_source_input(self):
        a = [completed_row("TH-G2P-001", "กา")]
        b = [completed_row("TH-G2P-001", "กะ", "TH-PH-02")]
        with self.assertRaisesRegex(ValueError, "input mismatch"):
            validate_independent_pair(a, b)


    def test_review_requires_aligned_per_syllable_tone_length_and_glottal_labels(self):
        row = completed_row("TH-G2P-001", "กา")
        row["tone_sequence"] = "MID,LOW"
        with self.assertRaisesRegex(ValueError, "must align with syllables"):
            validate_review_packet([row], ["TH-G2P-001"], "TH-PH-01")
        row = completed_row("TH-G2P-001", "กา")
        row["word_boundaries"] = "กะ"
        with self.assertRaisesRegex(ValueError, "reconstruct the Thai input"):
            validate_review_packet([row], ["TH-G2P-001"], "TH-PH-01")


    def test_boundary_metadata_uses_nfc_reconstruction_without_losing_syllables(self):
        row = completed_row("TH-G2P-001", "กา")
        row["syllable_boundaries"] = "ก.า"
        row["phonemic_ipa"] = "/k.aː/"
        row["tone_sequence"] = "MID"
        row["vowel_length"] = "SHORT,LONG"
        row["final_glottal"] = "ABSENT,ABSENT"
        with self.assertRaisesRegex(ValueError, "must align with syllables"):
            validate_review_packet([row], ["TH-G2P-001"], "TH-PH-01")


    def test_ukrainian_review_requires_conditional_status_and_native_reviewer_trace(self):
        row = {
            "id": "TH-UA-001", "thai": "ไกล", "source_ipa": "/klaj˧/",
            "ipa_reference_status": "SOURCE_ATTESTED_NOT_GOLD",
            "source_id": "SRC-1", "source_url": "https://example.org/source",
            "license": "CC-BY-SA-4.0", "criteria_version": "UA-PRACTICAL-TRANSCRIPTION-0.1",
            "reviewer_id": "UK-UA-01", "reviewer_qualification_ref": "qualification:UK-UA-01",
            "preferred_ukrainian_form": "клай", "syllable_boundary_policy": "DISPLAY_ONLY",
            "tone_rendering_policy": "NO_ORTHOGRAPHIC_TONE_MARK", "uncertainty": "LOW",
            "abstention_reason": "", "reviewed_at": "2026-11-01", "rationale": "Readable and segmentally faithful.",
        }
        self.assertEqual(
            validate_ukrainian_review_packet([row], ["TH-UA-001"], "UK-UA-01")["status"],
            "UKRAINIAN_REVIEW_VALID_CONDITIONAL_NOT_GOLD",
        )
        row["ipa_reference_status"] = "ADJUDICATED"
        with self.assertRaisesRegex(ValueError, "source-attested-not-gold"):
            validate_ukrainian_review_packet([row], ["TH-UA-001"], "UK-UA-01")

    def test_ukrainian_reviewer_pair_requires_distinct_native_reviewer_ids(self):
        base = {
            "id": "TH-UA-001", "thai": "ไกล", "source_ipa": "/klaj˧/",
            "ipa_reference_status": "SOURCE_ATTESTED_NOT_GOLD",
            "source_id": "SRC-1", "source_url": "https://example.org/source",
            "license": "CC-BY-SA-4.0", "criteria_version": "UA-PRACTICAL-TRANSCRIPTION-0.1",
            "reviewer_qualification_ref": "qualification", "preferred_ukrainian_form": "клай",
            "syllable_boundary_policy": "DISPLAY_ONLY",
            "tone_rendering_policy": "NO_ORTHOGRAPHIC_TONE_MARK", "uncertainty": "LOW",
            "abstention_reason": "", "reviewed_at": "2026-11-01", "rationale": "Reasoned preference.",
        }
        a = [{**base, "reviewer_id": "UK-UA-01"}]
        b = [{**base, "reviewer_id": "UK-UA-02"}]
        self.assertEqual(
            validate_ukrainian_independent_pair(a, b)["status"],
            "TWO_UKRAINIAN_REVIEWERS_PRESENT_CONDITIONAL_NOT_GOLD",
        )
        b[0]["reviewer_id"] = "UK-UA-01"
        with self.assertRaisesRegex(ValueError, "distinct"):
            validate_ukrainian_independent_pair(a, b)


    def test_ukrainian_pair_reports_preference_and_policy_agreement(self):
        base = {
            "id": "TH-UA-001", "thai": "ไกล", "source_ipa": "/klaj˧/",
            "ipa_reference_status": "SOURCE_ATTESTED_NOT_GOLD",
            "source_id": "SRC-1", "source_url": "https://example.org/source",
            "license": "CC-BY-SA-4.0", "criteria_version": "UA-PRACTICAL-TRANSCRIPTION-0.1",
            "reviewer_qualification_ref": "qualification", "preferred_ukrainian_form": "клай",
            "syllable_boundary_policy": "DISPLAY_ONLY",
            "tone_rendering_policy": "NO_ORTHOGRAPHIC_TONE_MARK", "uncertainty": "LOW",
            "abstention_reason": "", "reviewed_at": "2026-11-01", "rationale": "Reasoned preference.",
        }
        a = [{**base, "reviewer_id": "UK-UA-01"}]
        b = [{**base, "reviewer_id": "UK-UA-02", "preferred_ukrainian_form": "кляй"}]
        result = validate_ukrainian_independent_pair(a, b)
        self.assertEqual(result["agreement"]["fields"]["preferred_ukrainian_form"]["exact_agreements"], 0)
        self.assertEqual(result["agreement"]["fields"]["syllable_boundary_policy"]["exact_agreements"], 1)
        self.assertEqual(result["agreement"]["fields"]["tone_rendering_policy"]["exact_agreement_rate"], 1.0)

    def test_phonemic_packet_does_not_accept_surface_only_primary_level(self):
        row = completed_row("TH-G2P-001", "กา")
        row["transcription_level"] = "BROAD_SURFACE"
        with self.assertRaisesRegex(ValueError, "invalid transcription_level"):
            validate_review_packet([row], ["TH-G2P-001"], "TH-PH-01")

    def test_narrow_acoustic_labels_require_separate_narrow_ipa_and_audio_interval(self):
        row = completed_row("TH-G2P-001", "กา")
        row.update({"transcription_level": "NARROW_ACOUSTIC"})
        with self.assertRaisesRegex(ValueError, "separate bracketed narrow_ipa"):
            validate_review_packet([row], ["TH-G2P-001"], "TH-PH-01")
        row["narrow_ipa"] = "[kʰaː]"
        with self.assertRaisesRegex(ValueError, "audio"):
            validate_review_packet([row], ["TH-G2P-001"], "TH-PH-01")
        row.update({
            "audio_asset_reference": "CCOST:recording-001",
            "audio_time_start": "1.20",
            "audio_time_end": "1.85",
        })
        self.assertEqual(validate_review_packet([row], ["TH-G2P-001"], "TH-PH-01")["records"], 1)

    def test_narrow_ipa_syllable_count_must_match_phonemic_boundaries(self):
        row = completed_row("TH-G2P-001", "กา")
        row.update({
            "transcription_level": "NARROW_ACOUSTIC",
            "narrow_ipa": "[kʰaː.t]",
            "audio_asset_reference": "CCOST:recording-001",
            "audio_time_start": "1.20",
            "audio_time_end": "1.85",
        })
        with self.assertRaisesRegex(ValueError, "narrow IPA syllabification"):
            validate_review_packet([row], ["TH-G2P-001"], "TH-PH-01")


    def test_thai_review_requires_verified_phonetician_registry(self):
        row = completed_row("TH-G2P-001", "กา")
        registry = {"TH-PH-01": {
            "language": "th", "roles": "THAI_PHONETICIAN",
            "qualification_ref": "qualification-record:TH-PH-01", "verification_status": "VERIFIED",
            "verified_by": "test", "verified_at": "2026-11-01",
            "scope": "Standard Thai broad phonemic transcription",
        }}
        result = validate_review_packet([row], ["TH-G2P-001"], "TH-PH-01", reviewer_registry=registry)
        self.assertEqual(result["status"], "REVIEW_PACKET_VALID_NOT_GOLD")
        registry["TH-PH-01"]["language"] = "uk"
        with self.assertRaisesRegex(ValueError, "language"):
            validate_review_packet([row], ["TH-G2P-001"], "TH-PH-01", reviewer_registry=registry)

    def test_ukrainian_review_requires_verified_native_reviewer_and_registered_source(self):
        row = {
            "id": "TH-UA-001", "thai": "ไกล", "source_ipa": "/klaj˧/",
            "ipa_reference_status": "SOURCE_ATTESTED_NOT_GOLD", "source_id": "SRC-1",
            "source_url": "https://example.org/source", "license": "CC-BY-SA-4.0",
            "criteria_version": "UA-PRACTICAL-TRANSCRIPTION-0.1", "reviewer_id": "UK-UA-01",
            "reviewer_qualification_ref": "qualification:UK-UA-01", "preferred_ukrainian_form": "клай",
            "syllable_boundary_policy": "DISPLAY_ONLY", "tone_rendering_policy": "NO_ORTHOGRAPHIC_TONE_MARK",
            "uncertainty": "LOW", "abstention_reason": "", "reviewed_at": "2026-11-01",
            "rationale": "Reasoned preference.",
        }
        reviewers = {"UK-UA-01": {
            "language": "uk", "roles": "UKRAINIAN_NATIVE_REVIEWER",
            "qualification_ref": "qualification:UK-UA-01", "verification_status": "VERIFIED",
            "verified_by": "test", "verified_at": "2026-11-01",
            "scope": "Native Ukrainian practical transcription",
        }}
        sources = {"SRC-1": {
            "source_url": "https://example.org/source", "license": "CC-BY-SA-4.0",
            "allowed_uses": "UKRAINIAN_PREFERENCE_INPUT", "verification_status": "VERIFIED",
            "notes": "Test fixture source.",
        }}
        result = validate_ukrainian_review_packet(
            [row], ["TH-UA-001"], "UK-UA-01", reviewer_registry=reviewers, source_registry=sources,
        )
        self.assertEqual(result["status"], "UKRAINIAN_REVIEW_VALID_CONDITIONAL_NOT_GOLD")
        reviewers["UK-UA-01"]["roles"] = "THAI_PHONETICIAN"
        with self.assertRaisesRegex(ValueError, "lacks required role"):
            validate_ukrainian_review_packet(
                [row], ["TH-UA-001"], "UK-UA-01", reviewer_registry=reviewers, source_registry=sources,
            )
        reviewers["UK-UA-01"]["roles"] = "UKRAINIAN_NATIVE_REVIEWER"
        sources["SRC-1"]["source_url"] = "https://example.org/wrong"
        with self.assertRaisesRegex(ValueError, "source_url does not match"):
            validate_ukrainian_review_packet(
                [row], ["TH-UA-001"], "UK-UA-01", reviewer_registry=reviewers, source_registry=sources,
            )


if __name__ == "__main__":
    unittest.main()
