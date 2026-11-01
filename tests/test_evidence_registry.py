import csv
import tempfile
import unittest
from pathlib import Path

from thai_ukrainian.evidence_registry import (
    load_reviewer_registry, load_source_registry,
    validate_reviewer_reference, validate_source_reference,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FIELDS = ["source_id", "source_url", "license", "allowed_uses", "verification_status", "verified_by", "verified_at", "notes"]
REVIEWER_FIELDS = ["reviewer_id", "language", "roles", "qualification_ref", "verification_status", "verified_by", "verified_at", "scope", "notes"]


def write_registry(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


class EvidenceRegistryTests(unittest.TestCase):
    def test_committed_source_registry_is_valid_and_ccost_is_not_yet_ipa_gold(self):
        registry = load_source_registry(ROOT / "data/benchmark/source-registry.tsv")
        self.assertIn("CORP-CCOST", registry)
        self.assertEqual(registry["CORP-CCOST"]["verification_status"], "BLOCKED")
        with self.assertRaisesRegex(ValueError, "is blocked"):
            validate_source_reference("CORP-CCOST", "https://zenodo.org/records/17366698",
                                      "CC-BY-NC-SA-4.0", "IPA_GOLD_INPUT", registry, row_id="ccost-1")

    def test_project_challenge_inputs_are_approved_for_independent_expert_gold(self):
        registry = load_source_registry(ROOT / "data/benchmark/source-registry.tsv")
        source_id = "CLIPPYFIRST-THAI-CHALLENGE-CC398"
        self.assertIn(source_id, registry)
        source = registry[source_id]
        self.assertEqual(source["license"], "MIT")
        for use in ("BROAD_PHONEMIC_IPA_GOLD_INPUT", "WORD_SEGMENTATION_GOLD_INPUT"):
            validate_source_reference(
                source_id, source["source_url"], "MIT", use, registry, row_id="challenge-001"
            )
        self.assertIn("labels must come from independent reviewers", source["notes"])
        self.assertIn("not acoustic evidence", source["notes"])
        with self.assertRaisesRegex(ValueError, "not approved for BROAD_SURFACE_IPA_GOLD_INPUT"):
            validate_source_reference(
                source_id, source["source_url"], "MIT", "BROAD_SURFACE_IPA_GOLD_INPUT",
                registry, row_id="challenge-surface",
            )

    def test_ccost_wordlist_is_only_approved_as_broad_phonemic_input(self):
        registry = load_source_registry(ROOT / "data/benchmark/source-registry.tsv")
        source_id = "CORP-CCOST-WORDLIST"
        source = registry[source_id]
        self.assertEqual(source["verification_status"], "VERIFIED")
        validate_source_reference(
            source_id, source["source_url"], "CC-BY-NC-SA-4.0",
            "BROAD_PHONEMIC_IPA_GOLD_INPUT", registry, row_id="ccost-word-1"
        )
        with self.assertRaisesRegex(ValueError, "not approved for BROAD_SURFACE_IPA_GOLD_INPUT"):
            validate_source_reference(
                source_id, source["source_url"], "CC-BY-NC-SA-4.0",
                "BROAD_SURFACE_IPA_GOLD_INPUT", registry, row_id="ccost-surface-1"
            )

    def test_source_registry_binds_exact_url_license_and_allowed_use(self):
        registry = load_source_registry(ROOT / "data/benchmark/source-registry.tsv")
        source = registry["SRC-WIKTIONARY-TH-ไกล"]
        with self.assertRaisesRegex(ValueError, "source_url does not match"):
            validate_source_reference("SRC-WIKTIONARY-TH-ไกล", "https://example.org/wrong",
                                      source["license"], "UKRAINIAN_PREFERENCE_INPUT", registry, row_id="ua-1")
        with self.assertRaisesRegex(ValueError, "license does not match"):
            validate_source_reference("SRC-WIKTIONARY-TH-ไกล", source["source_url"],
                                      "CC0-1.0", "UKRAINIAN_PREFERENCE_INPUT", registry, row_id="ua-1")
        with self.assertRaisesRegex(ValueError, "not approved for BROAD_SURFACE_IPA_GOLD_INPUT"):
            validate_source_reference("SRC-WIKTIONARY-TH-ไกล", source["source_url"],
                                      source["license"], "BROAD_SURFACE_IPA_GOLD_INPUT", registry, row_id="ipa-1")

    def test_empty_reviewer_registry_is_valid_but_verifies_no_experts(self):
        self.assertEqual(load_reviewer_registry(ROOT / "data/benchmark/reviewer-qualifications.tsv"), {})

    def test_reviewer_reference_requires_verified_role_language_and_exact_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "reviewers.tsv"
            write_registry(path, REVIEWER_FIELDS, [{
                "reviewer_id": "TH-PH-TEST", "language": "th", "roles": "THAI_PHONETICIAN",
                "qualification_ref": "INTERNAL:TH-PH-TEST", "verification_status": "VERIFIED",
                "verified_by": "maintainer-review", "verified_at": "2026-11-01",
                "scope": "Standard Thai broad phonemic transcription", "notes": "Pseudonymous test fixture only.",
            }])
            registry = load_reviewer_registry(path)
            validate_reviewer_reference("TH-PH-TEST", "INTERNAL:TH-PH-TEST", registry,
                                        language="th", required_role="THAI_PHONETICIAN", row_id="thai-1")
            with self.assertRaisesRegex(ValueError, "language"):
                validate_reviewer_reference("TH-PH-TEST", "INTERNAL:TH-PH-TEST", registry,
                                            language="uk", required_role="THAI_PHONETICIAN", row_id="ua-1")
            with self.assertRaisesRegex(ValueError, "lacks required role"):
                validate_reviewer_reference("TH-PH-TEST", "INTERNAL:TH-PH-TEST", registry,
                                            language="th", required_role="THAI_PHONETICIAN_ADJUDICATOR", row_id="thai-1")
            with self.assertRaisesRegex(ValueError, "does not match verified reviewer registry"):
                validate_reviewer_reference("TH-PH-TEST", "unverified-reference", registry,
                                            language="th", required_role="THAI_PHONETICIAN", row_id="thai-1")

    def test_unverified_reviewer_cannot_be_used(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "reviewers.tsv"
            write_registry(path, REVIEWER_FIELDS, [{
                "reviewer_id": "UK-TEST", "language": "uk", "roles": "UKRAINIAN_NATIVE_REVIEWER",
                "qualification_ref": "INTERNAL:UK-TEST", "verification_status": "BLOCKED",
                "verified_by": "maintainer-review", "verified_at": "2026-11-01",
                "scope": "Native Ukrainian practical transcription", "notes": "Evidence pending.",
            }])
            registry = load_reviewer_registry(path)
            with self.assertRaisesRegex(ValueError, "not VERIFIED"):
                validate_reviewer_reference("UK-TEST", "INTERNAL:UK-TEST", registry,
                                            language="uk", required_role="UKRAINIAN_NATIVE_REVIEWER", row_id="ua-1")


if __name__ == "__main__":
    unittest.main()
